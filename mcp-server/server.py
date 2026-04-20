#!/usr/bin/env python3
"""
korean-contracts MCP Server

개인정보(이름·주민번호·주소·급여 등)를 로컬에서만 처리.
Claude에는 마스킹된 데이터만 전달하고, 계약서 완성 후 로컬에서 실제 값 복원 저장.
"""

import re
import json
import uuid
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any

from mcp.server.fastmcp import FastMCP

# ── 경로 설정 ─────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
SHARED_DIR = BASE_DIR / "shared"
OUTPUT_DIR = Path.home() / "Desktop"

# ── 세션 저장소 (메모리, 프로세스 종료 시 소멸) ──────────────
_sessions: dict[str, dict] = {}

mcp = FastMCP("korean-contracts")


# ══════════════════════════════════════════════════════════
# TOOL 1 — 개인정보 마스킹
# ══════════════════════════════════════════════════════════

@mcp.tool()
def mask_personal_info(contract_data: dict) -> dict:
    """
    계약서 입력 데이터에서 개인정보를 마스킹 토큰으로 치환한다.
    Claude에게 전달할 안전한 사본과 복원용 매핑을 반환한다.

    입력 예시:
    {
      "employeeName": "홍길동",
      "employeeIdFront": "950101",
      "employeeAddress": "서울 강남구 테헤란로 123",
      "baseSalary": 3000000,
      ...
    }

    반환:
    {
      "session_id": "abc123",
      "masked": { "employeeName": "PERSON_A", ... },
      "message": "마스킹 완료. session_id를 보관하세요."
    }
    """
    session_id = uuid.uuid4().hex[:12]
    masked = {}
    mapping = {}

    # 마스킹 규칙 정의
    MASK_RULES = {
        # 인적 정보
        "employeeName":          ("PERSON_A",    "name"),
        "employerRepresentative":("PERSON_B",    "name"),
        "employeeIdFront":       ("ID_FRONT",    "id"),
        "employeeAddress":       ("ADDRESS_A",   "address"),
        "employerAddress":       ("ADDRESS_B",   "address"),
        "employeeContact":       ("CONTACT_A",   "contact"),
        "employerContact":       ("CONTACT_B",   "contact"),
        "employerBizNo":         ("BIZ_NO",      "bizno"),
        # 계약 상대방 (프리랜서·외주)
        "freelancerName":        ("PERSON_C",    "name"),
        "freelancerIdFront":     ("ID_FRONT_C",  "id"),
        "clientName":            ("PERSON_D",    "name"),
        "vendorRepresentative":  ("PERSON_E",    "name"),
        # 금액 — 실제 금액은 로컬 보관, Claude에는 레인지 힌트만 전달
        "baseSalary":            None,
        "totalSalary":           None,
        "dailyWage":             None,
        "contractAmount":        None,
        "probationSalary":       None,
    }

    for key, value in contract_data.items():
        if key in MASK_RULES:
            rule = MASK_RULES[key]
            if rule is None:
                # 금액: 실제 값 보관, Claude에는 범위 힌트
                mapping[key] = value
                if isinstance(value, (int, float)):
                    # 백만원 단위 힌트만 노출
                    hint = f"AMOUNT_{int(value) // 1_000_000}M"
                    masked[key] = hint
                else:
                    masked[key] = "AMOUNT_UNDISCLOSED"
            else:
                token, _ = rule
                mapping[key] = value
                masked[key] = token
        else:
            # 민감하지 않은 항목은 그대로
            masked[key] = value

    # 세션 저장
    _sessions[session_id] = {
        "mapping": mapping,
        "masked":  masked,
        "created": datetime.now().isoformat(),
    }

    return {
        "session_id": session_id,
        "masked":     masked,
        "message":    (
            f"마스킹 완료. session_id={session_id} 를 보관하세요. "
            "이 masked 데이터만 Claude에 전달하세요. "
            "실제 개인정보는 로컬 세션에만 저장됩니다."
        ),
    }


# ══════════════════════════════════════════════════════════
# TOOL 2 — 계약서 로컬 저장 (마스킹 복원 후)
# ══════════════════════════════════════════════════════════

@mcp.tool()
def save_contract(
    session_id: str,
    contract_text: str,
    contract_type: str,
    output_dir: str = "",
) -> dict:
    """
    Claude가 생성한 마스킹된 계약서 텍스트에 실제 개인정보를 복원한 뒤
    로컬 파일로 저장한다. Anthropic 서버에는 복원된 계약서가 전달되지 않는다.

    Args:
        session_id:     mask_personal_info 가 반환한 세션 ID
        contract_text:  Claude가 생성한 마스킹 상태 계약서 텍스트
        contract_type:  파일명 prefix (예: employment-contract)
        output_dir:     저장 경로 (기본: ~/Desktop)
    """
    if session_id not in _sessions:
        return {"error": f"session_id '{session_id}' 를 찾을 수 없습니다. 세션이 만료됐거나 잘못된 ID입니다."}

    session  = _sessions[session_id]
    mapping  = session["mapping"]
    restored = contract_text

    # 마스킹 토큰 → 실제 값 복원
    TOKEN_MAP = {
        "PERSON_A":    "employeeName",
        "PERSON_B":    "employerRepresentative",
        "PERSON_C":    "freelancerName",
        "PERSON_D":    "clientName",
        "PERSON_E":    "vendorRepresentative",
        "ID_FRONT":    "employeeIdFront",
        "ID_FRONT_C":  "freelancerIdFront",
        "ADDRESS_A":   "employeeAddress",
        "ADDRESS_B":   "employerAddress",
        "CONTACT_A":   "employeeContact",
        "CONTACT_B":   "employerContact",
        "BIZ_NO":      "employerBizNo",
    }

    for token, data_key in TOKEN_MAP.items():
        if data_key in mapping:
            restored = restored.replace(token, str(mapping[data_key]))

    # 금액 힌트 복원 (AMOUNT_3M → 3,000,000원 형식)
    for data_key, real_value in mapping.items():
        if isinstance(real_value, (int, float)) and any(k in data_key for k in ("Salary", "Amount", "Wage")):
            hint = f"AMOUNT_{int(real_value) // 1_000_000}M"
            formatted = f"{int(real_value):,}"
            restored = restored.replace(hint, formatted)

    # 저장 경로
    out_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    date_str  = datetime.now().strftime("%Y%m%d")
    person_id = mapping.get("employeeName") or mapping.get("freelancerName") or "unknown"
    stem      = f"{contract_type}-{person_id}-{date_str}"

    txt_path  = out_dir / f"{stem}.txt"
    txt_path.write_text(restored, encoding="utf-8")

    # DOCX 변환
    docx_path = None
    generator = SHARED_DIR / "docx-generator.py"
    if generator.exists():
        import subprocess
        result = subprocess.run(
            ["python3", str(generator), str(txt_path)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            docx_path = str(out_dir / f"{stem}.docx")

    # 세션 정리 (1회 사용 후 삭제)
    del _sessions[session_id]

    return {
        "status":    "saved",
        "txt_path":  str(txt_path),
        "docx_path": docx_path or "변환 실패 — txt만 저장됨",
        "message":   "개인정보는 로컬에서만 복원·저장됐습니다. Anthropic 서버에 전송되지 않았습니다.",
    }


# ══════════════════════════════════════════════════════════
# TOOL 3 — 기존 계약서 로컬 읽기 + 마스킹 후 반환
# ══════════════════════════════════════════════════════════

@mcp.tool()
def load_contract_for_review(file_path: str) -> dict:
    """
    로컬 계약서 파일을 읽어 개인정보를 마스킹한 뒤 Claude에 전달할 안전한 텍스트를 반환한다.
    원본 파일은 로컬에만 유지된다.

    Args:
        file_path: 검토할 계약서 파일 경로 (txt, docx, md)
    """
    path = Path(file_path).expanduser()
    if not path.exists():
        return {"error": f"파일을 찾을 수 없습니다: {file_path}"}

    # 파일 읽기
    if path.suffix == ".docx":
        try:
            from docx import Document
            doc  = Document(path)
            text = "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            return {"error": f"docx 읽기 실패: {e}"}
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")

    # 정규식 기반 자동 마스킹
    session_id = uuid.uuid4().hex[:12]
    masked_text = text
    reverse_map: dict[str, str] = {}

    def _replace(pattern: str, token_prefix: str, flags=0) -> None:
        counter = [0]
        def _sub(m: re.Match) -> str:
            val   = m.group(0)
            token = f"{token_prefix}_{counter[0]}"
            counter[0] += 1
            reverse_map[token] = val
            return token
        nonlocal masked_text
        masked_text = re.sub(pattern, _sub, masked_text, flags=flags)

    # 주민등록번호 앞 6자리 패턴
    _replace(r"\b\d{6}[-–]\d{7}\b",       "RRN")
    _replace(r"\b\d{6}\b(?=\s*\(생년월일)", "DOB")
    # 전화번호
    _replace(r"0\d{1,2}[-–]\d{3,4}[-–]\d{4}", "PHONE")
    # 사업자등록번호
    _replace(r"\d{3}-\d{2}-\d{5}", "BIZNO")
    # 금액 (숫자+원, 콤마 포함)
    _replace(r"\d{1,3}(?:,\d{3})+원", "AMOUNT")
    _replace(r"\d+,\d{3}원",          "AMOUNT")
    # 이름 패턴 (성 + 2~3자) — 보수적 적용
    _replace(r"(?<=[가-힣]{1})[가-힣]{1,3}(?=\s*\(이하)", "NAME")

    _sessions[session_id] = {
        "type":        "review",
        "source_path": str(path),
        "reverse_map": reverse_map,
        "original":    text,
        "created":     datetime.now().isoformat(),
    }

    return {
        "session_id":  session_id,
        "masked_text": masked_text,
        "message": (
            f"계약서를 마스킹했습니다 (session_id={session_id}). "
            "masked_text 를 Claude에 붙여넣어 검토를 요청하세요. "
            "원본 파일과 개인정보는 로컬에만 유지됩니다."
        ),
    }


# ══════════════════════════════════════════════════════════
# TOOL 4 — 검토 결과 + 원본 복원 후 수정본 저장
# ══════════════════════════════════════════════════════════

@mcp.tool()
def save_reviewed_contract(
    session_id: str,
    reviewed_text: str,
    output_dir: str = "",
) -> dict:
    """
    Claude가 수정·검토한 마스킹 계약서 텍스트에 원본 개인정보를 복원한 뒤 저장한다.

    Args:
        session_id:     load_contract_for_review 가 반환한 세션 ID
        reviewed_text:  Claude가 수정한 마스킹 상태 계약서 텍스트
        output_dir:     저장 경로 (기본: 원본 파일과 동일 폴더)
    """
    if session_id not in _sessions:
        return {"error": f"session_id '{session_id}' 를 찾을 수 없습니다."}

    session     = _sessions[session_id]
    reverse_map = session.get("reverse_map", {})
    source_path = Path(session.get("source_path", ""))
    restored    = reviewed_text

    # 마스킹 토큰 → 원본 값 복원
    for token, original_val in reverse_map.items():
        # 토큰에 번호 suffix 있음 (예: AMOUNT_0, PHONE_1)
        restored = restored.replace(token, original_val)

    # 저장 경로
    if output_dir:
        out_dir = Path(output_dir).expanduser()
    elif source_path.exists():
        out_dir = source_path.parent
    else:
        out_dir = OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    date_str  = datetime.now().strftime("%Y%m%d_%H%M")
    stem      = f"{source_path.stem}_reviewed_{date_str}" if source_path.stem else f"contract_reviewed_{date_str}"
    txt_path  = out_dir / f"{stem}.txt"
    txt_path.write_text(restored, encoding="utf-8")

    # DOCX 변환
    docx_path = None
    generator = SHARED_DIR / "docx-generator.py"
    if generator.exists():
        import subprocess
        result = subprocess.run(
            ["python3", str(generator), str(txt_path)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            docx_path = str(out_dir / f"{stem}.docx")

    del _sessions[session_id]

    return {
        "status":  "saved",
        "txt":     str(txt_path),
        "docx":    docx_path or "변환 실패 — txt만 저장됨",
        "message": "개인정보 복원 완료. 수정본이 로컬에 저장됐습니다.",
    }


# ══════════════════════════════════════════════════════════
# TOOL 5 — 세션 상태 확인 (디버그용)
# ══════════════════════════════════════════════════════════

@mcp.tool()
def list_sessions() -> dict:
    """현재 활성 세션 목록을 반환한다 (개인정보 값은 포함하지 않음)."""
    result = {}
    for sid, sess in _sessions.items():
        result[sid] = {
            "type":    sess.get("type", "new"),
            "created": sess.get("created"),
            "keys":    list(sess.get("mapping", sess.get("reverse_map", {})).keys()),
        }
    return {"sessions": result, "count": len(result)}


# ══════════════════════════════════════════════════════════
# 엔트리포인트
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    mcp.run(transport="stdio")
