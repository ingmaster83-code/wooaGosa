"""
문제 JSON(data/*.json)에 DeepSeek API로 생성한 해설을 explanation 필드로 채워넣는다.

사용법:
  python generate_explanations.py data/gas_craft.json              # 파일 하나 전체
  python generate_explanations.py data/gas_craft.json --limit 20   # 테스트로 20문제만
  python generate_explanations.py --all                            # data/ 폴더 전체
  python generate_explanations.py --all --workers 10               # 동시 10개 요청

환경변수:
  DEEPSEEK_API_KEY : DeepSeek API 키 (필수)

동작:
  - explanation 필드가 이미 채워진 문제는 건너뜀 (재실행해도 안전, 이어서 처리)
  - 실패한 문제는 로그만 남기고 건너뜀 (전체 중단 없음)
  - SAVE_EVERY개마다 파일에 중간 저장 (중간에 멈춰도 그때까지 결과 유지)
"""
import os
import sys
import json
import glob
import time
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-flash"  # deepseek-chat 별칭은 2026-07-24 폐기 예정
DATA_DIR = r"C:\개인\wooahouse\wooaGosa\data"
SAVE_EVERY = 20
MAX_RETRIES = 2

PROMPT_TMPL = """다음은 자격증 시험 기출문제입니다. 정답이 왜 맞고 나머지 보기가 왜 틀렸는지
수험생이 이해하기 쉽게 3~5문장으로 간결하게 해설해 주세요. 해설 본문만 출력하고 다른 말은 하지 마세요.

문제: {question}
보기:
{choices}
정답: {answer_no}번 ({answer_text})"""


def build_prompt(q: dict) -> str:
    choices = "\n".join(
        f"{k}. {v}" for k, v in sorted(q["choices"].items(), key=lambda x: int(x[0]))
    )
    answer_no = q["answers"][0]
    answer_text = q["choices"].get(str(answer_no), "")
    return PROMPT_TMPL.format(
        question=q["question"], choices=choices, answer_no=answer_no, answer_text=answer_text
    )


def call_deepseek(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 400,
    }
    last_err = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.post(API_URL, headers=headers, json=body, timeout=60)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last_err = e
            if attempt < MAX_RETRIES:
                time.sleep(2 * (attempt + 1))
    raise last_err


def process_file(path: str, limit: int | None, workers: int):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    targets = [q for q in data if not (q.get("explanation") or "").strip()]
    if limit:
        targets = targets[:limit]

    fname = os.path.basename(path)
    if not targets:
        print(f"[{fname}] 이미 전부 해설 있음, 스킵")
        return

    print(f"[{fname}] 대상 {len(targets)}개 / 전체 {len(data)}개")

    done = failed = 0
    save_lock = threading.Lock()
    progress = {"n": 0}

    def work(q):
        try:
            explanation = call_deepseek(build_prompt(q))
            return q, explanation, None
        except Exception as e:
            return q, None, e

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(work, q) for q in targets]
        for fut in as_completed(futures):
            q, explanation, err = fut.result()
            with save_lock:
                progress["n"] += 1
                if err:
                    failed += 1
                    print(f"  [실패] id={q.get('id')} qno={q.get('question_no')}: {err}")
                else:
                    q["explanation"] = explanation
                    done += 1

                if progress["n"] % SAVE_EVERY == 0:
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False)
                    print(f"  진행 {progress['n']}/{len(targets)} (성공 {done}, 실패 {failed}) - 중간저장")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"  완료: 성공 {done}, 실패 {failed}")


def main():
    if not API_KEY:
        print("환경변수 DEEPSEEK_API_KEY가 설정되어 있지 않습니다.")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", help="처리할 JSON 파일 경로(들)")
    parser.add_argument("--all", action="store_true", help="data/ 폴더 전체 처리")
    parser.add_argument("--limit", type=int, default=None, help="파일당 처리할 최대 문제 수 (테스트용)")
    parser.add_argument("--workers", type=int, default=5, help="동시 요청 수 (기본 5)")
    args = parser.parse_args()

    if args.all:
        targets = sorted(glob.glob(os.path.join(DATA_DIR, "*.json")))
    elif args.files:
        targets = args.files
    else:
        print("처리할 파일을 지정하거나 --all 옵션을 사용하세요.")
        sys.exit(1)

    for path in targets:
        process_file(path, limit=args.limit, workers=args.workers)


if __name__ == "__main__":
    main()
