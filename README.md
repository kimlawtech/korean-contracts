# korean-contracts

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange)
[![Discord](https://img.shields.io/badge/Discord-SpeciAI-5865F2)](https://discord.gg/3gYGuMcqgb)

한국 사업자를 위한 근로계약서·알바계약서·유연근무·프리랜서·외주용역계약서·연봉계약·근로조건변경·일용직 자동 작성 Claude Code 스킬.
근로기준법·민법·4대보험 의무를 반영한 실무 계약서 초안 자동 생성.

> 한국 법률 AI 허브 **SpeciAI** 에서 만들고 있어요.
> 계약·노동·투자·지재권을 AI로 해결하는 창업자·변호사 커뮤니티에 초대합니다.
> → [discord.gg/3gYGuMcqgb](https://discord.gg/3gYGuMcqgb)

**라이선스**: Apache-2.0
**버전**: 1.2.0
**저자**: [@kimlawtech](https://github.com/kimlawtech)

## 지원 계약서

| 슬래시 명령어 | 계약서 | 대상 |
|-------------|--------|------|
| `/employment-contract` | 근로계약서 (주40시간) | 정규직·계약직, 5인이상/미만, 고정OT, 수습 |
| `/parttime-contract` | 알바계약서 (단시간) | 카페·편의점·일반, 주15시간 이상/미만 분기 |
| `/flexible-contract` | 유연근무 계약서 | 탄력근로·선택근로·재택·원격 |
| `/freelancer-contract` | 프리랜서 계약서 | 개인 프리랜서·1인 사업자, 3.3% 원천징수 |
| `/outsourcing-contract` | 외주용역계약서 | 법인 간 발주, 세금계산서, 불법파견 방지 |
| `/contract-amendment` | 근로조건 변경 합의서 | 임금·근무장소·업무내용·근무시간 변경 |
| `/salary-renewal` | 연봉계약서 | 연봉 갱신, 고정OT 포괄임금제 |
| `/daily-worker-contract` | 일용근로자 계약서 | 건설·행사·단기, 원천징수 2.7%, 산재보험 |

## 특징

- **2026년 기준 법령 반영**
  - 근로기준법 2024.10 최신 개정
  - **2026년 최저임금 10,320원/시 자동 검증** (2025년 10,030원에서 인상)
  - 임금체불 처벌 강화 (5년 이하 징역) 반영
  - 4대보험 의무 가입 기준 체크 (주15시간 분기)
  - 프리랜서 3.3% 원천징수 조항 자동 포함
  - 불법파견 방지 조항 (외주용역)
  - 유연근무제 서면합의 요건 안내 (§51·§52)

- **인터뷰 기반 자동 생성**
  - 비법조인 창업자도 쉽게 사용 가능
  - 전문용어 쉬운 말로 설명
  - 필수 항목 누락 자동 검증

- **파일 생성**
  - 마크다운(.md) 형식으로 생성
  - 양 당사자 서명란 포함
  - 면책 고지 자동 삽입

## 설치

```bash
git clone https://github.com/kimlawtech/korean-contracts
cd korean-contracts
bash install.sh
```

`install.sh`는 각 하위 스킬을 `~/.claude/skills/`에 심링크로 연결합니다.
설치 후 Claude Code를 재시작하면 `/employment-contract` 등 명령어가 활성화됩니다.

설치 경로를 변경하려면:

```bash
CLAUDE_SKILLS_DIR=/your-project/.claude/skills bash install.sh
```

## 사용법

각 계약서마다 별도 명령어를 사용:

```
/employment-contract      # 근로계약서 (주40시간, 정규직·계약직)
/parttime-contract        # 알바계약서 (단시간·파트타임)
/flexible-contract        # 유연근무 계약서 (탄력근로·선택근로·재택)
/freelancer-contract      # 프리랜서 계약서
/outsourcing-contract     # 외주용역계약서
/contract-amendment       # 근로조건 변경 합의서
/salary-renewal           # 연봉계약서 (연봉 갱신)
/daily-worker-contract    # 일용근로자 계약서
```

또는 자연어로:

```
"근로계약서 만들어줘"
"알바 계약서 필요해"
"유연근무 계약서 작성해줘"
"프리랜서 계약서 만들어줘"
"외주용역 계약서 작성해줘"
"근로조건 변경 합의서 만들어줘"
"연봉계약서 필요해"
"일용직 계약서 작성해줘"
```

## 디렉토리 구조

```
korean-contracts/
├── README.md
├── DISCLAIMER.md
│
├── employment-contract/        ← /employment-contract
│   └── SKILL.md                  주40시간 정규직·계약직, 고정OT, 수습
│
├── parttime-contract/          ← /parttime-contract
│   └── SKILL.md                  카페·편의점·일반 알바, 주15시간 분기
│
├── flexible-contract/          ← /flexible-contract
│   └── SKILL.md                  탄력근로·선택근로·재택근무
│
├── freelancer-contract/        ← /freelancer-contract
│   └── SKILL.md                  개인 프리랜서·1인 사업자
│
├── outsourcing-contract/       ← /outsourcing-contract
│   └── SKILL.md                  법인 간 외주용역
│
├── contract-amendment/         ← /contract-amendment
│   └── SKILL.md                  임금·근무장소·업무내용·근무시간 변경
│
├── salary-renewal/             ← /salary-renewal
│   └── SKILL.md                  연봉 갱신, 포괄임금제
│
├── daily-worker-contract/      ← /daily-worker-contract
│   └── SKILL.md                  건설·행사·단기 일용직
│
└── shared/                     ← 8개 스킬 공용
    ├── interview-all.md          유형별 인터뷰 질문 전체
    ├── render.md                 템플릿 치환 프로토콜
    ├── references/
    │   ├── labor-law-checklist.md   근로기준법 §17 + 5인 비교표
    │   ├── minimum-wage-2026.md     2026 최저임금 10,320원 기준
    │   ├── four-insurance.md        4대보험 가입 기준
    │   ├── freelancer-tax.md        원천징수·위장프리랜서
    │   ├── outsourcing-law.md       도급·위임·불법파견
    │   ├── contract-glossary.md     전문용어 사전
    │   └── penalty-risks.md         위반 제재 표
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

## 법적 면책

본 스킬이 생성하는 문서는 **참고용 초안**이며, 법률 자문이 아닙니다.
실제 서명 전 반드시 노무사·변호사 검토를 받으세요.

## 커뮤니티 — SpeciAI

한국 법률 AI 허브 **SpeciAI** 디스코드에서 만나요.
노동·계약·투자·지재권 법률 이슈를 AI와 함께 풀어가는 창업자·변호사 커뮤니티입니다.

**초대 링크**: [discord.gg/3gYGuMcqgb](https://discord.gg/3gYGuMcqgb)

운영: [@kimlawtech](https://github.com/kimlawtech)

## License

**Apache License 2.0** — Copyright 2026 kimlawtech (SpeciAI).
