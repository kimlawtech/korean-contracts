#!/bin/bash
# korean-contracts 설치 스크립트
# 사용법: bash install.sh

set -e

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SHARED_DIR="$REPO_DIR/shared"

echo "설치 경로: $SKILLS_DIR"
echo "소스 경로: $REPO_DIR"
echo ""

# skills 디렉토리 확인
if [ ! -d "$SKILLS_DIR" ]; then
  echo "오류: $SKILLS_DIR 디렉토리가 없습니다."
  echo "Claude Code가 설치되어 있는지 확인하세요."
  exit 1
fi

SKILLS=(
  "korean-contracts"
  "employment-contract"
  "parttime-contract"
  "flexible-contract"
  "freelancer-contract"
  "outsourcing-contract"
  "contract-amendment"
  "salary-renewal"
  "daily-worker-contract"
)

# {SKILL_DIR}을 실제 절대 경로로 치환
for skill in "${SKILLS[@]}"; do
  SKILL_MD="$REPO_DIR/$skill/SKILL.md"
  if [ -f "$SKILL_MD" ]; then
    ACTUAL_DIR="$REPO_DIR/$skill"
    sed -i '' "s|{SKILL_DIR}|$ACTUAL_DIR|g" "$SKILL_MD"
  fi
done

echo "경로 치환 완료"

# 심링크 생성
for skill in "${SKILLS[@]}"; do
  TARGET="$SKILLS_DIR/$skill"
  SOURCE="$REPO_DIR/$skill"

  if [ -L "$TARGET" ]; then
    rm "$TARGET"
  elif [ -d "$TARGET" ]; then
    echo "경고: $TARGET 이 일반 디렉토리로 존재합니다. 건너뜁니다."
    continue
  fi

  ln -s "$SOURCE" "$TARGET"
  echo "설치됨: $skill"
done

echo ""
echo "─────────────────────────────────"
echo "  MCP 개인정보 보호 서버 설치"
echo "─────────────────────────────────"

# Python 의존성 설치
if command -v pip3 &> /dev/null; then
  echo "[1/2] Python 의존성 설치 (mcp, python-docx) ..."
  pip3 install --quiet --upgrade mcp python-docx 2>&1 | tail -3 || {
    echo "  ⚠️  pip 설치 실패. 수동 실행 필요:"
    echo "      pip3 install mcp python-docx"
  }
else
  echo "  ⚠️  pip3 명령을 찾을 수 없습니다. Python3 설치 후 재시도하세요."
fi

# Claude Desktop 설정 파일에 MCP 서버 등록
echo "[2/2] Claude Desktop 설정 등록 ..."
if [ -f "$REPO_DIR/mcp-server/install-config.py" ]; then
  python3 "$REPO_DIR/mcp-server/install-config.py" || {
    echo "  ⚠️  MCP 설정 등록 실패. 수동 등록이 필요합니다."
    echo "      python3 $REPO_DIR/mcp-server/install-config.py"
  }
else
  echo "  ⚠️  install-config.py 파일이 없어 MCP 등록을 건너뜁니다."
fi

echo ""
echo "─────────────────────────────────"
echo "  설치 완료"
echo "─────────────────────────────────"
echo ""
echo "1) Claude Desktop 재시작 (Cmd+Q 후 재실행) — MCP 서버 자동 연결"
echo "2) Claude Code에서 아래 명령어 사용 가능:"
echo ""
echo "  /korean-contracts         계약서 유형 안내 (진입점)"
echo "  /employment-contract      근로계약서 (주40시간)"
echo "  /parttime-contract        알바계약서 (단시간)"
echo "  /flexible-contract        유연근무 계약서"
echo "  /freelancer-contract      프리랜서 계약서"
echo "  /outsourcing-contract     외주용역계약서"
echo "  /contract-amendment       근로조건 변경 합의서"
echo "  /salary-renewal           연봉계약서"
echo "  /daily-worker-contract    일용근로자 계약서"
echo ""
echo "🔒 개인정보(이름·주민번호·급여)는 MCP 서버가 마스킹 후 처리합니다."
