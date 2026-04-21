# korean-contracts 설치 스크립트 (Windows PowerShell)
# 사용법: powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"

# 환경 변수
$SkillsDir = if ($env:CLAUDE_SKILLS_DIR) { $env:CLAUDE_SKILLS_DIR } else { Join-Path $HOME ".claude\skills" }
$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "설치 경로: $SkillsDir"
Write-Host "소스 경로: $RepoDir"
Write-Host ""

# skills 디렉토리 확인
if (-not (Test-Path $SkillsDir)) {
    New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null
    Write-Host "skills 디렉토리 생성: $SkillsDir"
}

$Skills = @(
    "korean-contracts",
    "employment-contract",
    "parttime-contract",
    "flexible-contract",
    "freelancer-contract",
    "outsourcing-contract",
    "contract-amendment",
    "salary-renewal",
    "daily-worker-contract"
)

# {SKILL_DIR}, {REPO_DIR}, {REPO_DIR_WIN} 치환
# Windows 환경 — POSIX 경로는 슬래시, Windows 경로는 백슬래시
$repoDirPosix = $RepoDir.Replace('\', '/')
$repoDirWin = $RepoDir  # 백슬래시 유지

foreach ($skill in $Skills) {
    $skillMd = Join-Path $RepoDir "$skill\SKILL.md"
    if (Test-Path $skillMd) {
        $actualDir = (Join-Path $RepoDir $skill).Replace('\', '/')
        $content = Get-Content $skillMd -Raw
        $content = $content -replace '\{SKILL_DIR\}', $actualDir
        $content = $content -replace '\{REPO_DIR_WIN\}', $repoDirWin.Replace('\', '\\')
        $content = $content -replace '\{REPO_DIR\}', $repoDirPosix
        $content | Set-Content $skillMd -NoNewline
    }
}

Write-Host "경로 치환 완료"

# 심링크 생성 (관리자 권한 또는 개발자 모드 필요)
foreach ($skill in $Skills) {
    $target = Join-Path $SkillsDir $skill
    $source = Join-Path $RepoDir $skill

    if (Test-Path $target) {
        $item = Get-Item $target -Force
        if ($item.LinkType -eq "SymbolicLink" -or $item.LinkType -eq "Junction") {
            Remove-Item $target -Force
        } else {
            Write-Host "경고: $target 이 일반 디렉토리로 존재합니다. 건너뜁니다."
            continue
        }
    }

    try {
        # Junction은 관리자 권한 없이도 가능 (디렉토리 전용)
        New-Item -ItemType Junction -Path $target -Value $source -Force | Out-Null
        Write-Host "설치됨: $skill"
    } catch {
        Write-Host "오류: $skill 설치 실패. 관리자 권한 또는 개발자 모드가 필요합니다."
        Write-Host $_.Exception.Message
    }
}

Write-Host ""
Write-Host "─────────────────────────────────"
Write-Host "  MCP 개인정보 보호 서버 설치"
Write-Host "─────────────────────────────────"

# Python 명령 감지
$pythonCmd = $null
foreach ($cmd in @("python", "python3")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $pythonCmd = $cmd
        break
    }
}

if ($pythonCmd) {
    # Python 의존성 설치
    Write-Host "[1/2] Python 의존성 설치 (mcp, python-docx) ..."
    try {
        & $pythonCmd -m pip install --quiet --upgrade mcp python-docx 2>&1 | Select-Object -Last 3
    } catch {
        Write-Host "  경고: pip 설치 실패. 수동 실행 필요:"
        Write-Host "      $pythonCmd -m pip install mcp python-docx"
    }

    # MCP 등록 대상 자동 감지
    Write-Host "[2/2] MCP 서버 등록 ..."
    $installTarget = "claude"
    if (Get-Command codex -ErrorAction SilentlyContinue) {
        $installTarget = "both"
        Write-Host "  Codex CLI 감지됨 -> Claude Desktop + Codex 양쪽 등록"
    }

    $configScript = Join-Path $RepoDir "mcp-server\install-config.py"
    if (Test-Path $configScript) {
        & $pythonCmd $configScript "--target" $installTarget
    } else {
        Write-Host "  경고: install-config.py 파일이 없어 MCP 등록을 건너뜁니다."
    }
} else {
    Write-Host "  경고: python 명령을 찾을 수 없습니다. Python 3 설치 후 재시도하세요."
    Write-Host "        https://www.python.org/downloads/"
}

Write-Host ""
Write-Host "─────────────────────────────────"
Write-Host "  설치 완료"
Write-Host "─────────────────────────────────"
Write-Host ""
Write-Host "1) Claude Desktop 재시작 (트레이 우클릭 → Quit → 재실행) — MCP 서버 자동 연결"
Write-Host "2) Claude Code에서 아래 명령어 사용 가능:"
Write-Host ""
Write-Host "  /korean-contracts         계약서 유형 안내 (진입점)"
Write-Host "  /employment-contract      근로계약서 (주40시간)"
Write-Host "  /parttime-contract        알바계약서 (단시간)"
Write-Host "  /flexible-contract        유연근무 계약서"
Write-Host "  /freelancer-contract      프리랜서 계약서"
Write-Host "  /outsourcing-contract     외주용역계약서"
Write-Host "  /contract-amendment       근로조건 변경 합의서"
Write-Host "  /salary-renewal           연봉계약서"
Write-Host "  /daily-worker-contract    일용근로자 계약서"
Write-Host ""
Write-Host "[보안] 개인정보(이름·주민번호·급여)는 MCP 서버가 마스킹 후 처리합니다."
