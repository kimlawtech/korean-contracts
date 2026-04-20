# 템플릿 치환 프로토콜

## 원칙

1. 직렬 처리: 인터뷰로 전체 변수 수집 → 변수 맵 구성 → 템플릿 읽기 → 치환본 Write
2. 무결성 우선: 빈 `{{}}` placeholder가 최종 파일에 남으면 안 된다
3. 조건부 섹션: `{{#if}}...{{/if}}` 는 조건 불충족 시 블록 전체 제거
4. 반복: `{{#each}}...{{/each}}` 는 배열 원소 수만큼 복제

## 치환 순서

### Step A: 변수 맵 준비

근로계약서 예시:
```yaml
contractType: employment
employerName: "주식회사 모카"
employerRepresentative: "홍길동"
employerAddress: "서울 강남구 테헤란로 123"
employerBizNo: "123-45-67890"
employeeName: "이직원"
employeeIdFront: "950101"
jobTitle: "마케터"
jobDescription: "SNS 콘텐츠 기획·운영, Instagram·블로그 관리"
workPlace: "서울 강남구 본사"
contractForm: "정규직"  # 정규직 | 계약직 | 단시간
contractStartDate: "2026-05-01"
contractEndDate: ""  # 계약직일 때만
workDays: "월~금 (주 5일)"
workHours: "09:00~18:00"
breakTime: "12:00~13:00 (1시간)"
weeklyHours: 40
baseSalary: 2700000
allowances:
  - { name: "식대", amount: 200000 }
  - { name: "교통비", amount: 100000 }
totalSalary: 3000000
payDay: "매월 25일"
annualLeave: 15
weeklyHoliday: "매주 일요일"
probationPeriod: 3
probationSalary: 2700000
hasFourInsurance: true
hasSecrecyClause: true
hasNonCompete: false
hasConcurrentJobBan: true
hasIPClause: true
effectiveDate: "2026-05-01"
```

### Step B: 최저임금 검증 (2026년 기준: 10,320원/시)

```
# 월급제
hourlyWage = totalSalary / (weeklyHours * 4.345)
if hourlyWage < 10320:
    경고 출력: "시급 환산 X원으로 2026년 최저임금(10,320원)에 미달합니다. 수정 필요."
    Write 금지

# 시급제 (알바·단시간)
if hourlyWage < 10320:
    경고 출력: "입력 시급 X원이 2026년 최저임금(10,320원)에 미달합니다."
    Write 금지

# 고정OT 포함 포괄임금제
baseHourlyWage = baseSalary / (weeklyHours * 4.345)
if baseHourlyWage < 10320:
    경고 출력: "기본급 시급 환산 X원이 최저임금 미달. 기본급 기준으로도 최저임금 이상이어야 합니다."
    Write 금지
```

### Step C: 템플릿 Read 후 라인별 치환

Handlebars 문법:
- `{{변수}}` → 값 대입
- `{{#if 조건}}...{{/if}}` → 조건 평가 후 해당 블록 유지/제거
- `{{#each 배열}}...{{/each}}` → 배열 수만큼 복제
- `{{this.필드}}` → 반복 컨텍스트 내 속성

### Step D: 검증 (Write 전 필수)

- [ ] `{{` 패턴이 남아있지 않은가
- [ ] 근로계약서: 근로기준법 §17 5개 항목 포함 여부
- [ ] 최저임금 이상 여부
- [ ] 면책 문구 최상단 포함 여부

### Step E: 파일명 결정

```
근로계약서 (주40시간): employment-contract-{employeeName}-{YYYYMMDD}.md
알바·단시간:          parttime-contract-{employeeName}-{YYYYMMDD}.md
유연근무:             flexible-contract-{employeeName}-{YYYYMMDD}.md
프리랜서:             freelancer-contract-{freelancerName}-{YYYYMMDD}.md
외주용역:             outsourcing-contract-{vendorCompany}-{YYYYMMDD}.md
근로조건 변경:        contract-amendment-{employeeName}-{YYYYMMDD}.md
연봉계약서:           salary-renewal-{employeeName}-{YYYYMMDD}.md
일용근로자:           daily-worker-contract-{employeeName}-{YYYYMMDD}.md
```

### Step F: DOCX 변환 (필수 — 마크다운 저장 후 반드시 실행)

마크다운(.md) 저장이 완료되면 즉시 아래 명령으로 Word 파일을 생성한다.

```bash
python3 "$(dirname $0)/../shared/docx-generator.py" "{생성된.md파일경로}"
```

예시:
```bash
python3 ~/.claude/skills/korean-contracts/shared/docx-generator.py \
  employment-contract-이직원-20260420.md
```

- 출력 파일명: 동일 경로에 `.docx` 확장자로 자동 저장
- 폰트: 굴림 (본문 10pt, 제목 16/13/11pt)
- 스타일: 면책문구 회색, 제목 진한 네이비, 표 헤더 배경색
- `.md` 파일은 임시 파일이므로 `.docx` 생성 후 사용자에게 `.docx` 경로만 안내

사용자에게 전달할 멘트:
```
계약서가 Word 파일로 저장됐습니다.
파일: {파일명}.docx

서명 전 내용을 확인하시고, 필요하면 수정해서 사용하세요.
실제 서명 전 노무사·변호사 검토를 권장합니다.
```

## 흔한 실수

- 조건부 블록 태그 그대로 출력하면 안 됨
- 최저임금 미달 시 경고 없이 생성 금지
- 빈 배열 반복 블록은 전체 삭제
- 필수 변수 누락 시 인터뷰로 복귀
- DOCX 변환 없이 마크다운만 저장하면 안 됨
