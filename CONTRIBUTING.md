# Contributing to korean-contracts

한국 계약서 AI 스킬 프로젝트에 기여해주셔서 감사합니다.
이 문서는 PR·Issue 제출 시 따라야 할 규칙을 정리합니다.

---

## 기여 유형

| 유형 | 설명 | 라벨 |
|------|------|------|
| 버그 수정 | 스킬 작동 오류, 템플릿 변수 누락 등 | `bug` |
| 신규 계약 유형 | 기존 9종에 없는 계약서 유형 추가 | `new-contract` |
| 법령·판례 업데이트 | 개정 법령·최신 판례 반영 | `legal-update` |
| 번역·현지화 | 영문·중문 인터뷰 버전 | `i18n` |
| MCP 서버 개선 | 보안 서버 도구 추가·개선 | `mcp` |
| 문서 개선 | README·주석·예시 보완 | `docs` |
| 테스트 케이스 | `examples/TEST-CASES.md` 추가 | `tests` |

---

## 시작하기

### 1. Fork & Clone

```bash
git clone https://github.com/<your-username>/korean-contracts
cd korean-contracts
bash install.sh   # macOS / Linux
# powershell -ExecutionPolicy Bypass -File install.ps1   # Windows
```

### 2. 브랜치 생성

```bash
git checkout -b <타입>/<간단한-설명>

# 예시
git checkout -b fix/minimum-wage-validation
git checkout -b add/foreign-worker-contract
git checkout -b legal-update/2026-overtime-rule
```

### 3. 변경사항 작성 → 커밋 → PR

---

## 커밋 메시지 규칙 (필수 준수)

### 형식

```
[LABEL] 한국어 단문
```

라벨 4종만 사용. 한국어 설명은 변경 대상만 **짧게**. 이유·세부 내용 설명 금지.

| 라벨 | 용도 |
|------|------|
| `[ADD]` | 새 파일·기능·내용 추가 |
| `[FIX]` | 버그·오류 수정 |
| `[UPDATE]` | 기존 내용 변경·개선 |
| `[REMOVE]` | 파일·기능·내용 삭제 |

### 좋은 예시

```
[ADD] 외국인 근로자 특례 계약서 템플릿
[FIX] symlink 경로 버그
[UPDATE] 2026년 최저임금 10,320원 반영
[REMOVE] 구버전 포괄임금 검증 로직
```

### 나쁜 예시 (리젝트됨)

```
❌ update some files
❌ [feat] add something new (영어 금지)
❌ [ADD] 2026년 최저임금 반영을 위해 근로기준법 §5와 대법원 판례를 참고하여 기본급 검증 로직을 개선함 (너무 김)
❌ 커밋 (라벨 없음)
```

### 금지 사항

- `Co-Authored-By` 줄 추가 금지
- 커밋 메시지에 Claude·AI 도구 언급 금지
- 라벨 없는 커밋 금지
- 영어 커밋 메시지 금지 (프로젝트 언어는 한국어)

---

## 법률 관련 PR 필수 요건

이 프로젝트는 **실제 법적 문서를 생성**하기 때문에 법령·판례 관련 PR은 추가 규칙을 따릅니다.

### 1. 출처 명시 필수

법령·판례를 인용·반영하는 PR은 **PR 본문에 출처를 반드시 명시**하세요.

```markdown
## 법적 근거

- 근로기준법 §48②
- 대법원 2024.12.19. 선고 2020다247190 전원합의체 판결
- 고용노동부 2025.4.21. 행정해석 근로기준정책과-1234
```

### 2. 시행일 확인

개정 법령은 **시행일**을 반드시 확인하고 반영 시점을 명시합니다.

### 3. 법률 자문 아님 고지 유지

각 SKILL.md·계약서 템플릿에 포함된 **"본 문서는 법률 자문이 아니다"** 면책 문구는 **절대 삭제하지 마세요**.

### 4. 민감 예시 데이터 금지

예시·테스트 케이스에 **실제 사람의 이름·주민번호·사업자번호·연락처**를 포함하지 마세요.

| 허용 | 금지 |
|------|------|
| `홍길동`, `이직원`, `주식회사 모카` (가명) | 실제 인물·회사명 |
| `950101` (6자리 앞자리만) | 전체 주민번호 13자리 |
| `123-45-67890` (가상 사업자번호) | 실제 등록된 사업자번호 |
| `010-1234-5678` (예시용) | 실제 사용 중인 번호 |

---

## 파일별 변경 가이드

### SKILL.md 수정 시

- YAML frontmatter의 `version` 은 **semver 증가** 필수 (`2.1.0` → `2.2.0`)
- `{REPO_DIR}` 플레이스홀더는 **하드코딩 경로로 덮어쓰지 말 것** (install.sh가 자동 치환)
- 한 스킬만 수정할 때도 다른 스킬의 일관성(용어·톤) 확인

### shared/templates/*.tmpl 수정 시

- Handlebars 문법 유지 (`{{변수}}`, `{{#if}}...{{/if}}`)
- 변수명 변경 시 render.md·interview-all.md 에도 반영
- 법률 조항 번호 변경 시 `legal-validation-rules.md` 의 RULE도 함께 업데이트

### mcp-server/ 수정 시

- 개인정보 마스킹·복원 로직 변경은 **반드시 테스트 케이스 추가**
- `server.py` 반환 필드명 변경 시 `render.md`의 MCP 호출 문서도 동기화
- 의존성 추가 시 `requirements.txt` 업데이트

---

## PR 제출 전 체크리스트

- [ ] 커밋 메시지가 `[LABEL] 한국어 단문` 형식
- [ ] 법령·판례 인용 시 출처 명시
- [ ] 가명·가상 데이터만 사용
- [ ] `{REPO_DIR}` 플레이스홀더 유지
- [ ] `install.sh` / `install.ps1` 정상 실행 확인
- [ ] 관련 SKILL.md 버전 증가
- [ ] 면책 문구 삭제 여부 재확인
- [ ] README 또는 CHANGELOG 업데이트 (해당되는 경우)

---

## Issue 제출

### 버그 리포트

`.github/ISSUE_TEMPLATE/bug_report.md` 양식 사용.

### 신규 계약 유형 제안

`.github/ISSUE_TEMPLATE/contract-type.md` 양식 사용.
법률적 근거와 실제 사용 빈도 함께 제시해주세요.

### 법령 업데이트

`.github/ISSUE_TEMPLATE/legal-update.md` 양식 사용.
관보·판례 원문 링크 첨부 필수.

---

## Code of Conduct

이 프로젝트는 [Contributor Covenant](CODE_OF_CONDUCT.md) 를 따릅니다. 모든 참여자는 상호 존중 의무가 있습니다.

---

## 라이선스

기여한 내용은 프로젝트 라이선스인 **Apache License 2.0** 을 따릅니다. PR 제출 시 이에 동의한 것으로 간주합니다.

---

## 질문·논의 채널

| 채널 | 용도 |
|------|------|
| **GitHub Issues** | 버그 리포트·기능 제안·신규 계약 유형 제안 |
| **GitHub Discussions** | 자유 토론·사용 후기·법령 해석 토론·아이디어 브레인스토밍 |
| **Discord** | 빠른 질문·실시간 채팅: [discord.gg/3gYGuMcqgb](https://discord.gg/3gYGuMcqgb) |
| **Maintainer** | [@kimlawtech](https://github.com/kimlawtech) |

### Issue vs Discussion 어디에 올릴까?

- **Issue로**: 명확한 버그·구체적 기능 요청·법령 업데이트 요청 (실행 가능한 작업)
- **Discussion으로**: "이렇게 해도 될까요?", 사용 사례 공유, 법령 해석 의견 교환 (대화)

---

## 자동 검증 워크플로우

PR을 열면 GitHub Actions가 자동 실행됩니다:

| 워크플로우 | 검증 내용 |
|-----------|----------|
| `commit-lint` | 모든 커밋이 `[LABEL] 한국어 단문` 형식인지 |
| `commit-lint` | `Co-Authored-By` 줄 없는지 |
| `commit-lint` | Claude·GPT·Copilot 등 AI 도구 언급 없는지 |
| `auto-label` | PR 제목·본문 기반 자동 라벨 부여 |

검증 실패 시 PR 머지 차단. 커밋 메시지 수정 후 재푸시하세요.

---

감사합니다.
