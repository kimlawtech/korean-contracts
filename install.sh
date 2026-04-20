#!/bin/bash
# korean-contracts 설치 스크립트
# 사용법: bash install.sh

set -e

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "설치 경로: $SKILLS_DIR"
echo "소스 경로: $REPO_DIR"
echo ""

# skills 디렉토리 확인
if [ ! -d "$SKILLS_DIR" ]; then
  echo "오류: $SKILLS_DIR 디렉토리가 없습니다."
  echo "Claude Code가 설치되어 있는지 확인하세요."
  exit 1
fi

# 기존 심링크 제거 후 재생성
SKILLS=(
  "employment-contract"
  "parttime-contract"
  "flexible-contract"
  "freelancer-contract"
  "outsourcing-contract"
  "contract-amendment"
  "salary-renewal"
  "daily-worker-contract"
)

for skill in "${SKILLS[@]}"; do
  TARGET="$SKILLS_DIR/$skill"
  SOURCE="$REPO_DIR/$skill"

  if [ -L "$TARGET" ]; then
    rm "$TARGET"
    echo "기존 심링크 제거: $TARGET"
  elif [ -d "$TARGET" ]; then
    echo "경고: $TARGET 이 일반 디렉토리로 존재합니다. 건너뜁니다."
    continue
  fi

  ln -s "$SOURCE" "$TARGET"
  echo "설치됨: $skill"
done

echo ""
echo "설치 완료! Claude Code에서 다음 명령어를 사용할 수 있습니다:"
echo ""
echo "  /employment-contract      근로계약서 (주40시간)"
echo "  /parttime-contract        알바계약서 (단시간)"
echo "  /flexible-contract        유연근무 계약서"
echo "  /freelancer-contract      프리랜서 계약서"
echo "  /outsourcing-contract     외주용역계약서"
echo "  /contract-amendment       근로조건 변경 합의서"
echo "  /salary-renewal           연봉계약서"
echo "  /daily-worker-contract    일용근로자 계약서"
