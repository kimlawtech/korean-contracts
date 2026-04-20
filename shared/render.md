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

### Step A2: MCP 개인정보 마스킹 (필수 — Step B 전에 반드시 실행)

변수 맵이 준비되면 MCP 도구 `mask_personal_info`를 호출해 개인정보를 마스킹한다.

```
MCP 호출:
  도구: mask_personal_info
  입력: 변수 맵 전체 (Step A에서 준비한 dict)

반환값:
  session_id: 세션 ID (Step F에서 save_contract 호출 시 필요 — 반드시 보관)
  masked:     마스킹된 변수 맵 (이후 모든 처리는 이 값으로 진행)
```

**MCP 서버가 실행 중이지 않으면:**
→ 사용자에게 안내:
```
⚠️  보안 모드(MCP 서버) 미연결 상태입니다.
    개인정보가 포함된 계약서를 생성하려면 MCP 서버가 필요합니다.

    실행 방법:
      터미널에서: python3 ~/Desktop/skill/korean-contracts/mcp-server/server.py
      또는 Claude Desktop 재시작 (자동 연결)

    [계속하시겠어요?]
    1) MCP 서버 연결 후 재시도 (권장)
    2) 이름·주민번호·급여 등 민감 정보를 직접 입력하지 않고 계속 진행
       (계약서 생성 후 [ ] 괄호 안에 직접 기입)
```
2번 선택 시: 민감 필드를 `[근로자 이름]`, `[주민번호 앞 6자리]`, `[기본급]` 형태의 괄호 플레이스홀더로 처리.

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

### Step D: 1차 검증 (Write 전 필수)

- [ ] `{{` 패턴이 남아있지 않은가
- [ ] 근로계약서: 근로기준법 §17 5개 항목 포함 여부
- [ ] 최저임금 이상 여부
- [ ] 면책 문구 최상단 포함 여부

### Step D2: 법률 검증 패스 (Write 후 필수)

파일 저장 후 `/Users/sarangcho/Desktop/skill/korean-contracts/shared/references/legal-validation-rules.md` 를 Read 툴로 읽고 RULE 1~10을 순서대로 적용해 생성된 계약서를 검토한다.

- 오류 발견 시: 계약서 내용을 수정하고 파일을 덮어쓴 뒤 수정 내역을 사용자에게 알림
- 확인 필요 항목: 사용자에게 명시적으로 고지
- 모든 룰 통과 시: 검증 결과 요약 출력

### Step E: 파일명 및 저장 경로 결정

저장 경로는 인터뷰 Step SAVE에서 수집한 `outputDir` 사용. 미수집 시 `~/Desktop` 기본값.

```
근로계약서 (주40시간): {outputDir}/employment-contract-{employeeName}-{YYYYMMDD}
알바·단시간:          {outputDir}/parttime-contract-{employeeName}-{YYYYMMDD}
유연근무:             {outputDir}/flexible-contract-{employeeName}-{YYYYMMDD}
프리랜서:             {outputDir}/freelancer-contract-{freelancerName}-{YYYYMMDD}
외주용역:             {outputDir}/outsourcing-contract-{vendorCompany}-{YYYYMMDD}
근로조건 변경:        {outputDir}/contract-amendment-{employeeName}-{YYYYMMDD}
연봉계약서:           {outputDir}/salary-renewal-{employeeName}-{YYYYMMDD}
일용근로자:           {outputDir}/daily-worker-contract-{employeeName}-{YYYYMMDD}
```

각 계약서마다 `.txt` 와 `.docx` 두 파일 모두 생성.

### Step F: TXT + DOCX 생성 (필수)

MCP 서버 연결 여부에 따라 두 경로로 분기한다.

#### F-A: MCP 서버 연결된 경우 (권장 — 개인정보 보호)

`save_contract` MCP 도구를 호출한다.

```
MCP 호출:
  도구: save_contract
  입력:
    session_id:    Step A2에서 받은 세션 ID
    contract_text: 치환 완료된 계약서 전체 텍스트
    contract_type: 파일명 prefix (예: "employment-contract-이직원-20260501")
    output_dir:    Step SAVE에서 수집한 outputDir (기본값: ~/Desktop)

반환값:
  txt_path:  저장된 .txt 파일 경로
  docx_path: 저장된 .docx 파일 경로
```

MCP 서버가 내부적으로 처리하는 것:
1. 마스킹 토큰(PERSON_A, AMOUNT_3M 등)을 실제 값으로 복원
2. .txt 파일 저장
3. docx-generator.py 실행 → .docx 생성

#### F-B: MCP 서버 미연결된 경우 (플레이스홀더 모드)

Step A2에서 플레이스홀더 처리를 선택한 경우.

**F-B-1: TXT 저장**

```
저장 경로: {outputDir}/{파일명}.txt
```

Write 툴로 직접 저장한다.

**F-B-2: DOCX 변환**

```bash
python3 /Users/sarangcho/Desktop/skill/korean-contracts/shared/docx-generator.py \
  "{outputDir}/{파일명}.txt"
```

- 출력 파일: `{outputDir}/{파일명}.docx` (자동 저장)
- 폰트: 굴림 (본문 10pt, 제목 16/13/11pt)
- 스타일: 면책문구 회색, 제목 진한 네이비, 표 헤더 배경색

#### 완료 후 사용자에게 전달할 멘트

```
계약서 두 파일이 저장됐습니다.

  📄 {파일명}.txt
  📄 {파일명}.docx

저장 위치: {outputDir}

서명 전 내용을 확인하시고, 필요하면 수정해서 사용하세요.
실제 서명 전 노무사·변호사 검토를 권장합니다.
```

## 흔한 실수

- 조건부 블록 태그 그대로 출력하면 안 됨
- 최저임금 미달 시 경고 없이 생성 금지
- 빈 배열 반복 블록은 전체 삭제
- 필수 변수 누락 시 인터뷰로 복귀
- DOCX 변환 없이 마크다운만 저장하면 안 됨
