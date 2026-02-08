#!/usr/bin/env python3
"""Gemini CLI wrapper with automatic model fallback and JSON parsing.

Usage:
  python gemini_call.py INPUT_FILE -p DETAILED_PROMPT [-o OUTPUT] [-m MODEL] [--resume [SESSION_ID]] [--context FILE ...] [--timeout N]

DETAILED_PROMPT: Detailed instructions (prepended to stdin input. Fixed prompt is automatically applied to -p option)
INPUT_FILE: Input file content (appended after detailed prompt in stdin)

stdout: JSON result with success, model, fallback, session_id, resume_failed, web_searched, search_count, stats, response fields
stderr: Warning/error messages for logging
Exit: 0=success, 1=all models failed
"""

import subprocess
import json
import sys
import argparse
import os
import shutil

# Fixed prompt always sent to gemini CLI -p option
FIXED_PROMPT = "입력된 자료에 대한 답변요청. 필요한 경우 웹 검색을 통해 최신 정보를 조사하여 활용하고, 출처를 함께 제시. ultrathink"

# Fallback chain in priority order. When a model fails, try the next one.
FALLBACK_CHAIN = [
    "gemini-3-pro-preview",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]
DEFAULT_MODEL = FALLBACK_CHAIN[0]
DEFAULT_TIMEOUT = 120


def build_fallback_chain(selected_model):
    """Build fallback chain starting from the selected model downward."""
    if selected_model not in FALLBACK_CHAIN:
        return [selected_model] + FALLBACK_CHAIN
    idx = FALLBACK_CHAIN.index(selected_model)
    return FALLBACK_CHAIN[idx:]


def find_gemini_cli():
    """Resolve the full path to the gemini CLI executable.

    On Windows, npm global installs create .cmd wrappers that subprocess
    cannot find without shell=True. Using shutil.which resolves the full
    path including .cmd extensions via PATHEXT.
    """
    path = shutil.which("gemini")
    if path:
        return path
    return None


def try_models(gemini_bin, models, input_data, resume=None, timeout=DEFAULT_TIMEOUT):
    """Try each model in order. Returns (success, result_dict) or (False, None)."""
    for i, model in enumerate(models):
        is_fallback = i > 0

        cmd = [gemini_bin, "-m", model, "-p", FIXED_PROMPT, "-o", "json"]
        if resume:
            cmd.extend(["--resume", resume])

        try:
            proc = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            print(f"[WARN] {model}: timeout ({timeout}s)", file=sys.stderr)
            continue
        except FileNotFoundError:
            print(f"[ERROR] Failed to execute: {gemini_bin}", file=sys.stderr)
            return False, None

        if proc.returncode != 0:
            print(f"[WARN] {model}: exit code {proc.returncode}", file=sys.stderr)
            if proc.stderr:
                print(f"  stderr: {proc.stderr[:200]}", file=sys.stderr)
            continue

        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            print(f"[WARN] {model}: invalid JSON response", file=sys.stderr)
            continue

        response = data.get("response", "")
        if not response:
            print(f"[WARN] {model}: empty response field", file=sys.stderr)
            continue

        stats = data.get("stats", {})
        tools_by_name = stats.get("tools", {}).get("byName", {})
        web_search_info = tools_by_name.get("google_web_search", {})

        return True, {
            "model": model,
            "fallback": is_fallback,
            "session_id": data.get("session_id", ""),
            "response": response,
            "web_searched": "google_web_search" in tools_by_name,
            "search_count": web_search_info.get("count", 0),
            "stats": stats,
        }

    return False, None


def call_gemini(input_file, prompt, output_file=None, model=None, resume=None, context_files=None, timeout=DEFAULT_TIMEOUT):
    gemini_bin = find_gemini_cli()
    if not gemini_bin:
        print("[ERROR] gemini CLI not found. Install: npm install -g @google/gemini-cli", file=sys.stderr)
        result = {
            "success": False,
            "model": None,
            "fallback": True,
            "resume_failed": False,
            "web_searched": False,
            "search_count": 0,
            "stats": {},
            "error": "All models failed. Claude should proceed independently.",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    # Read input file content
    with open(input_file, "r", encoding="utf-8") as f:
        input_content = f.read()

    # Prepend detailed prompt to input data
    input_data = f"""# 지시사항

{prompt}

---

# 입력 자료

{input_content}
"""

    selected = model or DEFAULT_MODEL
    models = build_fallback_chain(selected)
    resume_failed = False

    # Attempt 1: with --resume (if specified)
    success, result_data = try_models(gemini_bin, models, input_data, resume=resume, timeout=timeout)

    # Attempt 2: if resume failed, retry without --resume but with context
    if not success and resume and resume != "latest":
        print(f"[WARN] --resume {resume} failed. Retrying as new session with context.", file=sys.stderr)
        resume_failed = True

        combined_parts = []
        combined_parts.append(f"# 지시사항\n\n{prompt}\n")

        if context_files:
            combined_parts.append("---\n\n# 이전 맥락\n")
            for cf in context_files:
                if os.path.exists(cf):
                    with open(cf, "r", encoding="utf-8") as f:
                        combined_parts.append(f"## {os.path.basename(cf)}\n\n{f.read()}\n")
                else:
                    print(f"[WARN] Context file not found: {cf}", file=sys.stderr)

        combined_parts.append(f"---\n\n# 후속 질문\n\n{input_content}")
        combined_input = "\n".join(combined_parts)

        success, result_data = try_models(gemini_bin, models, combined_input, resume=None, timeout=timeout)

    if success:
        if output_file:
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result_data["response"])

        result = {
            "success": True,
            "model": result_data["model"],
            "fallback": result_data["fallback"],
            "session_id": result_data["session_id"],
            "resume_failed": resume_failed,
            "web_searched": result_data["web_searched"],
            "search_count": result_data["search_count"],
            "stats": result_data["stats"],
            "response": result_data["response"],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # All attempts failed
    result = {
        "success": False,
        "model": None,
        "fallback": True,
        "resume_failed": resume_failed,
        "web_searched": False,
        "search_count": 0,
        "stats": {},
        "error": "All models failed. Claude should proceed independently.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1


def main():
    parser = argparse.ArgumentParser(description="Gemini CLI wrapper with automatic fallback")
    parser.add_argument("input_file", help="Path to input file to send to Gemini")
    parser.add_argument("-p", "--prompt", required=True, help="Detailed instructions (prepended to input file content in stdin)")
    parser.add_argument("-o", "--output", help="Save response text to this file")
    parser.add_argument("-m", "--model", default=None,
                        choices=FALLBACK_CHAIN,
                        help=f"Primary model to use (default: {DEFAULT_MODEL}). Falls back to lower-priority models on failure.")
    parser.add_argument("--resume", nargs="?", const="latest", default=None, help="Resume Gemini session (session_id or 'latest')")
    parser.add_argument("--context", nargs="*", default=None, help="Context files to include when --resume fails")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"[ERROR] Input file not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    sys.exit(call_gemini(
        input_file=args.input_file,
        prompt=args.prompt,
        output_file=args.output,
        model=args.model,
        resume=args.resume,
        context_files=args.context,
        timeout=args.timeout,
    ))


if __name__ == "__main__":
    main()
