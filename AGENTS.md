# korean-contracts — AI 에이전트용 가이드

이 파일은 Codex CLI·기타 AI 에이전트가 이 레포에서 작업할 때 따라야 할 지침입니다.
(Claude Code 사용자는 SKILL.md 시스템이 자동 작동하므로 이 파일을 읽지 않아도 됩니다.)

---

## 프로젝트 개요

한국 사업자용 9종 계약서 자동 생성 도구.
2026년 최저임금·최신 대법원 판례·근로기준법 §17 자동 검증.
MCP 서버로 개인정보 마스킹 처리.

**지원 계약서:** 근로·알바·유연근무·일용·프리랜서·외주용역·근로조건 변경·연봉계약서

---

## 핵심 디렉토리

```
korean-contracts/        진입점 스킬 (메뉴 + 라우팅)
{contract-type}/         각 계약 유형별 스킬 (8종)
shared/
  interview-all.md       모든 계약서 인터뷰 질문 모음
  render.md              템플릿 치환 프로토콜
  templates/*.tmpl       Handlebars 템플릿 8종
  references/            법령·판례·검증 룰
  docx-generator.py      .docx 변환 스크립트
mcp-server/
  server.py              개인정보 보호 MCP 서버
  install-config.py      MCP 자동 등록 스크립트
```

---

## Codex CLI에서 이 레포 사용하기

### 시나리오 A: 계약서 작성 작업 위임

```bash
cd ~/Desktop/skill/korean-contracts
codex "근로계약서를 작성해줘. shared/interview-all.md 의 [근로계약서] 인터뷰를 따라 진행하고, 답변 받은 뒤 shared/templates/employment-contract.tmpl 을 사용해. shared/render.md 의 치환 프로토콜과 shared/references/legal-validation-rules.md 의 RULE 1~10 을 적용해."
```

### 시나리오 B: 기존 계약서 검토

```bash
codex "이 계약서 파일을 shared/references/contract-review.md 의 체크리스트 A~I 로 검토해줘: <파일 경로>"
```

### 시나리오 C: 새 계약 유형 추가 (개발 작업)

```bash
codex "shared/templates/employment-contract.tmpl 구조를 참고해서 외국인 근로자 특례 계약서 템플릿을 만들어줘. 출입국관리법 §18 + 외국인고용법 §9 반영."
```

---

## 작업 시 반드시 따를 규칙

### 법률 관련

1. **2026년 최저임금**: 시간당 10,320원. 미달 시 계약서 생성 차단.
2. **근로기준법 §17 필수 5항목**: 임금·소정근로시간·휴일·연차·근무장소·업무내용. 누락 시 인터뷰로 복귀.
3. **면책 문구**: 모든 생성 문서 최상단에 "본 문서는 법률 자문이 아닙니다" 유지. 절대 삭제 금지.
4. **개정법령 반영 기준**:
   - 통상임금: 대법원 2024.12.19. 전원합의체 (재직조건부 상여금 포함)
   - 포괄임금: 대법원 2024.12.26. (기본급 시급 환산도 최저임금 이상)
   - 배우자 출산휴가: 20일 (2025년 시행)
   - 임금명세서 교부 의무: 근로기준법 §48② (과태료 100만원)

### 개인정보

1. **MCP 서버 연결 시**: `mask_personal_info` → `save_contract` 호출 흐름 준수.
2. **MCP 서버 미연결 시**: 민감 필드를 `[근로자 이름]`, `[기본급]` 형태 플레이스홀더로 처리.
3. **예시 데이터**: 가명만 사용 (`홍길동`, `이직원`, `주식회사 모카`, `123-45-67890`).
4. **실제 인물·사업자번호·주민번호 절대 입력 금지**.

### 코드 변경

1. `{REPO_DIR}` 플레이스홀더는 하드코딩 절대 금지. install.sh가 치환함.
2. SKILL.md 수정 시 `version` semver 증가.
3. 커밋 메시지: `[ADD]` / `[FIX]` / `[UPDATE]` / `[REMOVE]` + 한국어 단문.
4. AI 도구 언급 금지 (Codex·Claude·GPT·Copilot 등 commit message에 쓰지 말 것).
5. `Co-Authored-By` 줄 추가 금지.

---

## MCP 서버 사용 (선택)

Codex CLI에서 MCP를 쓰려면 `~/.codex/config.toml` 에 등록:

```toml
[mcp_servers.korean-contracts]
command = "python3"
args = ["{REPO_DIR}/mcp-server/server.py"]
```

`{REPO_DIR}` 은 실제 클론 경로로 치환할 것 (예: `/Users/<사용자>/Projects/korean-contracts`).

자동 등록 스크립트:

```bash
python3 mcp-server/install-config.py --target codex
```

(주의: 현재 install-config.py 는 Claude Desktop 전용. Codex 지원은 별도 PR 필요.)

---

## 자주 하는 실수

| 실수 | 올바른 방법 |
|------|------------|
| Handlebars 태그를 그대로 출력 (`{{employerName}}`) | render.md Step C 에 따라 모두 치환 |
| 최저임금 미달 무시하고 계약서 생성 | render.md Step B 에서 차단 |
| 빈 배열을 `{{#each}}` 블록 그대로 둠 | 블록 전체 삭제 |
| .txt만 저장하고 .docx 변환 누락 | 반드시 docx-generator.py 실행 |
| 면책 문구 삭제 | 모든 생성 문서 최상단 유지 |

---

## 참고 문서

- 사람용 가이드: `README.md`
- 기여 규칙: `CONTRIBUTING.md`
- 법령 검증 룰: `shared/references/legal-validation-rules.md`
- 법령 글로사리: `shared/references/contract-glossary.md`
- 테스트 케이스: `examples/TEST-CASES.md`

---

## 문제 발생 시

1. 변수 누락 → `shared/interview-all.md` 인터뷰로 복귀
2. 최저임금 미달 → 사용자에게 경고 후 수정 요청
3. 법령 해석 불확실 → 노무사·변호사 검토 권장 문구 강조
4. MCP 도구 호출 실패 → 플레이스홀더 모드로 전환
