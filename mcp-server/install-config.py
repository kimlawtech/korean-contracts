#!/usr/bin/env python3
"""
korean-contracts MCP 서버를 AI 에이전트 도구의 설정 파일에 자동 등록한다.

지원 도구:
  --target claude   Claude Desktop (기본값)
  --target codex    Codex CLI
  --target both     양쪽 모두

지원 OS:
  - macOS / Windows: Claude Desktop·Codex CLI 모두 지원
  - Linux:          Codex CLI 만 지원 (Claude Desktop 미지원)

특징:
  - 기존 설정(다른 MCP 서버·preferences 등) 모두 보존
  - 중복 등록 시 경로만 갱신
  - OS별 Python 실행 명령 자동 선택 (macOS/Linux: python3, Windows: python)
"""
from pathlib import Path
import argparse
import json
import os
import platform
import shutil
import sys


def resolve_claude_config_path() -> Path:
    """OS별 Claude Desktop 설정 파일 경로."""
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
        return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def resolve_codex_config_path() -> Path:
    """Codex CLI 설정 파일 경로 (macOS/Linux/Windows 모두 ~/.codex/config.toml)."""
    return Path.home() / ".codex" / "config.toml"


def resolve_python_command() -> str:
    """OS별 사용할 Python 실행 명령."""
    system = platform.system()
    if system == "Windows":
        for cmd in ("python", "python3"):
            if shutil.which(cmd):
                return cmd
        return "python"
    for cmd in ("python3", "python"):
        if shutil.which(cmd):
            return cmd
    return "python3"


def install_claude(server_path: Path, python_cmd: str) -> int:
    """Claude Desktop 설정에 등록 (JSON)."""
    system = platform.system()
    config_path = resolve_claude_config_path()

    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[ERROR] Claude 설정 JSON 파싱 실패: {e}")
            return 1
    else:
        config = {}
        config_path.parent.mkdir(parents=True, exist_ok=True)

    mcp_servers = config.setdefault("mcpServers", {})
    prev = mcp_servers.get("korean-contracts")
    new_entry = {"command": python_cmd, "args": [str(server_path)]}
    mcp_servers["korean-contracts"] = new_entry

    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    status = (
        "신규 등록" if prev is None else
        "설정 갱신" if prev != new_entry else
        "이미 등록됨"
    )
    print(f"[Claude] {status}")
    print(f"         설정 파일: {config_path}")

    if system == "Windows":
        print("         재시작: Claude Desktop 트레이 우클릭 → Quit → 재실행")
    elif system == "Darwin":
        print("         재시작: Claude Desktop Cmd+Q → 재실행")
    return 0


def install_codex(server_path: Path, python_cmd: str) -> int:
    """Codex CLI 설정에 등록 (TOML — 단순 append/replace)."""
    config_path = resolve_codex_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    section_header = "[mcp_servers.korean-contracts]"
    args_str = json.dumps([str(server_path)])  # TOML 배열도 JSON과 호환
    new_section = (
        f"\n{section_header}\n"
        f'command = "{python_cmd}"\n'
        f"args = {args_str}\n"
    )

    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""

    if section_header in existing:
        # 기존 섹션 교체 — 다음 섹션([...]) 또는 EOF 까지를 찾아 치환
        lines = existing.splitlines()
        out = []
        skip = False
        for line in lines:
            stripped = line.strip()
            if stripped == section_header:
                skip = True
                continue
            if skip:
                if stripped.startswith("[") and stripped.endswith("]"):
                    # 다음 섹션 시작 — 여기서부터는 그대로 유지
                    skip = False
                    out.append(line)
                # skip=True 동안의 본문 라인은 버림
                continue
            out.append(line)
        rebuilt = "\n".join(out).rstrip() + "\n" + new_section
        config_path.write_text(rebuilt, encoding="utf-8")
        print(f"[Codex]  설정 갱신")
    else:
        # 신규 추가 — 끝에 append
        config_path.write_text(existing.rstrip() + "\n" + new_section, encoding="utf-8")
        print(f"[Codex]  신규 등록")

    print(f"         설정 파일: {config_path}")
    print(f"         재시작: codex 명령 다시 실행하면 자동 로드")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="korean-contracts MCP 서버 자동 등록")
    parser.add_argument(
        "--target",
        choices=("claude", "codex", "both"),
        default="claude",
        help="등록할 대상 도구 (기본: claude)",
    )
    args = parser.parse_args()

    server_path = Path(__file__).resolve().parent / "server.py"
    if not server_path.exists():
        print(f"[ERROR] MCP 서버 파일을 찾을 수 없습니다: {server_path}")
        return 1

    system = platform.system()
    python_cmd = resolve_python_command()

    print(f"OS:        {system}")
    print(f"Python:    {python_cmd}")
    print(f"서버 경로: {server_path}")
    print()

    rc = 0
    if args.target in ("claude", "both"):
        if system not in ("Darwin", "Windows"):
            print("[Claude] 경고: Linux는 Claude Desktop 미지원 — 건너뜁니다.")
        else:
            rc |= install_claude(server_path, python_cmd)
            print()

    if args.target in ("codex", "both"):
        rc |= install_codex(server_path, python_cmd)
        print()

    return rc


if __name__ == "__main__":
    sys.exit(main())
