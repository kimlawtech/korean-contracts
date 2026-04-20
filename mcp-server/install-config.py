#!/usr/bin/env python3
"""
Claude Desktop 설정 파일(claude_desktop_config.json)에
korean-contracts MCP 서버를 자동 등록한다.

지원 OS:
  - macOS:   ~/Library/Application Support/Claude/
  - Windows: %APPDATA%\\Claude\\
  - Linux:   Claude Desktop 미지원 (스킬만 사용 가능)

특징:
  - 기존 mcpServers 항목은 보존
  - 기존 preferences 등 최상위 키도 보존
  - 중복 등록 시 경로만 갱신
  - OS별 Python 실행 명령 자동 선택 (macOS/Linux: python3, Windows: python)
"""
from pathlib import Path
import json
import os
import platform
import shutil
import sys


def resolve_config_path() -> Path:
    """OS별 Claude Desktop 설정 파일 경로를 반환."""
    system = platform.system()

    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"

    if system == "Windows":
        # %APPDATA% 는 보통 C:\Users\<user>\AppData\Roaming
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
        return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"

    # Linux 등 미지원
    return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def resolve_python_command() -> str:
    """OS별로 사용할 Python 실행 명령을 반환 (실제 PATH 확인)."""
    system = platform.system()

    if system == "Windows":
        # Windows: python, python3 순서로 확인
        for cmd in ("python", "python3"):
            if shutil.which(cmd):
                return cmd
        return "python"

    # macOS, Linux: python3, python 순서로 확인
    for cmd in ("python3", "python"):
        if shutil.which(cmd):
            return cmd
    return "python3"


def main() -> int:
    system = platform.system()

    if system not in ("Darwin", "Windows"):
        print(f"[경고] Claude Desktop은 {system} 에서 공식 지원되지 않습니다.")
        print("        설정 파일은 생성하지만 Claude Desktop이 인식하지 못할 수 있습니다.")
        print()

    config_path = resolve_config_path()
    python_cmd = resolve_python_command()

    # MCP 서버 스크립트 경로 (이 파일과 같은 폴더의 server.py)
    server_path = Path(__file__).resolve().parent / "server.py"

    if not server_path.exists():
        print(f"[ERROR] MCP 서버 파일을 찾을 수 없습니다: {server_path}")
        return 1

    # 설정 파일 로드 (없으면 빈 dict)
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[ERROR] 기존 설정 파일 JSON 파싱 실패: {e}")
            print(f"        파일을 직접 확인하세요: {config_path}")
            return 1
    else:
        config = {}
        config_path.parent.mkdir(parents=True, exist_ok=True)

    # mcpServers 항목에 korean-contracts 등록
    mcp_servers = config.setdefault("mcpServers", {})
    prev = mcp_servers.get("korean-contracts")

    new_entry = {
        "command": python_cmd,
        "args": [str(server_path)],
    }
    mcp_servers["korean-contracts"] = new_entry

    # 저장
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 결과 출력
    if prev is None:
        print(f"[OK] MCP 서버 신규 등록")
    elif prev != new_entry:
        print(f"[OK] MCP 서버 설정 갱신 (python 명령 또는 경로 변경)")
    else:
        print(f"[OK] MCP 서버 이미 등록되어 있습니다")

    print(f"     OS:        {system}")
    print(f"     Python:    {python_cmd}")
    print(f"     서버 경로: {server_path}")
    print(f"     설정 파일: {config_path}")
    print()

    # OS별 재시작 안내
    if system == "Windows":
        print("다음 단계: Claude Desktop을 완전히 종료(트레이 우클릭 → Quit)한 뒤 다시 실행하세요.")
    elif system == "Darwin":
        print("다음 단계: Claude Desktop을 완전히 종료(Cmd+Q)한 뒤 다시 실행하세요.")
    else:
        print("다음 단계: Claude Desktop을 완전히 종료한 뒤 다시 실행하세요.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
