#!/usr/bin/env python3
"""
Claude Desktop 설정 파일(claude_desktop_config.json)에
korean-contracts MCP 서버를 자동 등록한다.

- 기존 mcpServers 항목은 보존
- 기존 preferences 등 최상위 키도 보존
- 중복 등록 시 경로만 갱신
"""
from pathlib import Path
import json
import sys


def main() -> int:
    home = Path.home()
    config_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"

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

    mcp_servers["korean-contracts"] = {
        "command": "python3",
        "args": [str(server_path)],
    }

    # 저장
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if prev is None:
        print(f"[OK] MCP 서버 신규 등록: {server_path}")
    elif prev.get("args") != [str(server_path)]:
        print(f"[OK] MCP 서버 경로 갱신: {server_path}")
    else:
        print(f"[OK] MCP 서버 이미 등록되어 있습니다: {server_path}")

    print(f"     설정 파일: {config_path}")
    print()
    print("다음 단계: Claude Desktop을 완전히 종료(Cmd+Q)한 뒤 다시 실행하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
