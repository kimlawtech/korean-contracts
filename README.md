# korean-contracts

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-orange)](https://claude.ai/code)
[![Version](https://img.shields.io/badge/version-2.0.0-green)](https://github.com/kimlawtech/korean-contracts)
[![Discord](https://img.shields.io/badge/Discord-SpeciAI-5865F2)](https://discord.gg/3gYGuMcqgb)

**한국 사업자를 위한 AI 계약서 자동 작성 도구**

창업자·HR 담당자·소상공인이 근로계약서, 알바계약서, 프리랜서 계약서, 외주용역계약서 등 8종의 계약서를 Claude Code에서 대화형으로 작성할 수 있는 스킬 모음입니다.
2026년 최저임금·최신 대법원 판례를 반영하고, RULE 1~14 법률 검증을 통과한 계약서 초안을 `.txt` + `.docx` 두 가지 형식으로 자동 생성합니다.

> 한국 법률 AI 허브 **SpeciAI**에서 만들고 있습니다.
> 계약·노동·투자·지재권을 AI로 해결하는 창업자·변호사 커뮤니티에 초대합니다.
> → [discord.gg/3gYGuMcqgb](https://discord.gg/3gYGuMcqgb) | [@kimlawtech](https://github.com/kimlawtech)

---

## 지원 계약서 8종

| 명령어 | 계약서 | 주요 대상 |
|--------|--------|-----------|
| `/korean-contracts` | 계약서 유형 진단 | 어떤 계약서가 필요한지 모를 때 |
| `/employment-contract` | 근로계약서 | 정규직·계약직, 5인이상/미만, 고정OT, 수습 |
| `/parttime-contract` | 알바·단시간 계약서 | 카페·편의점·일반, 주15시간 이상/미만 분기 |
| `/flexible-contract` | 유연근무 계약서 | 탄력근로·선택근로·재택·원격근무 |
| `/freelancer-contract` | 프리랜서 계약서 | 개인 프리랜서·1인 사업자, 3.3% 원천징수 |
| `/outsourcing-contract` | 외주용역계약서 | 법인 간 발주, 세금계산서, 불법파견 방지 |
| `/contract-amendment` | 근로조건 변경 합의서 | 임금·근무장소·업무내용·근무시간 변경 |
| `/salary-renewal` | 연봉계약서 | 연봉 갱신, 고정OT 포괄임금제 |
| `/daily-worker-contract` | 일용근로자 계약서 | 건설·행사·단기, 원천징수, 산재보험 |

---

## 계약서 생성 예시

아래는 `/employment-contract` 스킬이 실제로 생성한 근로계약서입니다.
인터뷰 응답만 입력하면 조항이 자동 완성되고, RULE 1~14 법률 검증을 거쳐 `.txt` + `.docx` 파일로 저장됩니다.

![근로계약서 생성 예시 — 제1조~제4조, 임금 구성·최저임금 자동 계산](assets/sample-employment-contract.png)

**이 화면에서 확인할 수 있는 것:**
- 법적 면책 고지 자동 삽입
- 근로기준법 §17 필수 5항목(계약기간·업무·근로시간·임금·휴가) 자동 구성
- 임금 구성 항목 분리 기재 (기본급 + 수당 + 합계)
- 최저임금 10,320원/시 자동 검증 (미달 시 계약서 생성 차단)
- 통상임금 재직조건부 상여금 포함 문구 (대법원 2024.12.19.)

---

## 핵심 기능

### 20년 경력 공인노무사·변호사 페르소나
각 계약 유형마다 전문 페르소나가 인터뷰를 진행합니다. 법적 리스크를 먼저 설명하고 사용자가 이해한 뒤 입력할 수 있게 안내합니다.

### RULE 1~14 자동 법률 검증
계약서 생성 전·후 14개 체크리스트를 자동 적용합니다.

| 검증 항목 | 내용 |
|-----------|------|
| RULE 1~5 | 근로기준법 §17 필수 5항목, 계약기간, 임금 구성 |
| RULE 6~9 | 해고예고, 서명란, 최저임금, 5인 분기 |
| RULE 10~11 | 면책 문구, 4대보험 |
| RULE 12 | 통상임금 재직조건부 상여금 (대법원 2024.12.19.) |
| RULE 13 | 임금명세서 교부 의무 (§48②) |
| RULE 14 | 위장 프리랜서 7대 요소 (대법원 2006다49830) |

### 기존 계약서 분석·보완
사용 중인 계약서를 붙여넣으면 법적 문제점을 먼저 안내하고, 누락·오류 항목만 추가 보완합니다.

### 자동 분기 처리
- **5인 이상/미만** — 가산수당·공휴일 유급·연차·부당해고 조항 자동 분기
- **주 15시간 이상/미만** — 주휴수당·4대보험 가입 기준 자동 적용
- **계약직 갱신기대권 방지** — 기간제 계약서에 자동 삽입

### 최신 법령·판례 반영
- **2026년 최저임금 10,320원/시** 자동 검증 (미달 시 생성 차단)
- **대법원 2024.12.19.** — 재직조건부 상여금 통상임금 포함 (고정성 폐지)
- **대법원 2024.12.26.** — 포괄임금 최저임금 미달 부분 무효
- **배우자 출산휴가 20일** (남녀고용평등법 §18의2, 2025년 시행)
- **하도급법 2024.8.28.** — 기술자료 유용 5배 손해배상
- **임금명세서 교부 의무** (근로기준법 §48②, 과태료 100만원)

---

## 설치

### 요구 사항
- [Claude Code](https://claude.ai/code) 설치
- Git
- Python 3 (`.docx` 변환용, `python-docx` 패키지)

### 설치 명령

```bash
git clone https://github.com/kimlawtech/korean-contracts
cd korean-contracts
bash install.sh
```

`install.sh`는 각 스킬을 `~/.claude/skills/`에 심링크로 연결합니다.
설치 후 Claude Code를 재시작하면 명령어가 활성화됩니다.

설치 경로를 변경하려면:

```bash
CLAUDE_SKILLS_DIR=/your-project/.claude/skills bash install.sh
```

python-docx 설치:

```bash
pip install python-docx
```

---

## 사용법

### 슬래시 명령어로 바로 시작

```
/korean-contracts         # 어떤 계약서가 필요한지 진단 (처음이면 여기서 시작)
/employment-contract      # 근로계약서
/parttime-contract        # 알바·단시간 계약서
/flexible-contract        # 유연근무 계약서
/freelancer-contract      # 프리랜서 계약서
/outsourcing-contract     # 외주용역계약서
/contract-amendment       # 근로조건 변경 합의서
/salary-renewal           # 연봉계약서
/daily-worker-contract    # 일용근로자 계약서
```

### 자연어로도 가능

```
"근로계약서 만들어줘"
"알바 계약서 필요해"
"프리랜서한테 맡기려는데 계약서 작성해줘"
"외주 계약서 만들어줘"
"연봉 인상했는데 계약서 갱신해줘"
"기존 계약서 검토해줘"
```

### 진행 흐름

```
1. 스킬 시작
2. 기존 계약서 여부 확인 (있으면 자동 분석)
3. 유형별 인터뷰 (1~2문항씩, 전문용어 풀어서 설명)
4. 입력 내용 요약 확인
5. RULE 1~14 법률 검증
6. .txt + .docx 파일 생성 및 저장
```

---

## 파일 구조

```
korean-contracts/
├── README.md
├── DISCLAIMER.md
├── install.sh
│
├── korean-contracts/           ← /korean-contracts (진입점 라우터)
│   └── SKILL.md
│
├── employment-contract/        ← /employment-contract
│   └── SKILL.md
│
├── parttime-contract/          ← /parttime-contract
│   └── SKILL.md
│
├── flexible-contract/          ← /flexible-contract
│   └── SKILL.md
│
├── freelancer-contract/        ← /freelancer-contract
│   └── SKILL.md
│
├── outsourcing-contract/       ← /outsourcing-contract
│   └── SKILL.md
│
├── contract-amendment/         ← /contract-amendment
│   └── SKILL.md
│
├── salary-renewal/             ← /salary-renewal
│   └── SKILL.md
│
├── daily-worker-contract/      ← /daily-worker-contract
│   └── SKILL.md
│
├── assets/
│   └── sample-employment-contract.png
│
└── shared/                     ← 8개 스킬 공용 리소스
    ├── interview-all.md          유형별 인터뷰 질문 전체
    ├── render.md                 템플릿 치환 프로토콜
    ├── docx-generator.py         .docx 변환 스크립트
    ├── references/
    │   ├── labor-law-checklist.md    근로기준법 §17 + 5인 비교표
    │   ├── minimum-wage-2026.md      2026 최저임금 10,320원 기준
    │   ├── four-insurance.md         4대보험 가입 기준
    │   ├── legal-validation-rules.md RULE 1~14 법률 검증 체계
    │   ├── freelancer-tax.md         원천징수·위장프리랜서
    │   ├── outsourcing-law.md        도급·위임·불법파견
    │   ├── contract-glossary.md      전문용어 사전
    │   └── penalty-risks.md          위반 제재 표
    └── templates/
        ├── employment-contract.tmpl
        ├── parttime-contract.tmpl
        ├── flexible-contract.tmpl
        ├── freelancer-contract.tmpl
        ├── outsourcing-contract.tmpl
        ├── contract-amendment.tmpl
        ├── salary-renewal.tmpl
        └── daily-worker-contract.tmpl
```

---

## 법적 면책

본 스킬이 생성하는 문서는 **참고용 초안**이며 법률 자문이 아닙니다.
실제 서명 전 반드시 공인노무사·변호사 검토를 받으세요.

---

## 커뮤니티 — SpeciAI

한국 법률 AI 허브 **SpeciAI** 디스코드에서 만나세요.
노동·계약·투자·지재권 법률 이슈를 AI와 함께 풀어가는 창업자·변호사 커뮤니티입니다.

**초대 링크**: [discord.gg/3gYGuMcqgb](https://discord.gg/3gYGuMcqgb)

이 프로젝트를 만들고 있습니다: [@kimlawtech](https://github.com/kimlawtech)
질문·기여·버그 제보를 환영합니다. Issue 또는 PR로 참여해주세요.

---

## License

**Apache License 2.0** — Copyright 2026 kimlawtech (SpeciAI).
