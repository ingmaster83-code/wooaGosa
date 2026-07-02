"""
전체 재파싱(경계판단 순번 기준 + 빈 보기 제외) 이후에도 남는,
복구 불가능한 소수 문제 유형을 정리한다.

1) 개수형 문제("몇 개인가?") 본문이 통째로 누락되고 보기가 '1개~N개'만 남은 경우
2) 정답이 가리키는 보기 번호 자체가 존재하지 않는 경우 (5번 보기가 파싱 중 누락됨)
"""
import json
import sys
import glob
import os

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = r"C:\개인\wooahouse\wooaGosa\data"
COUNT_ONLY_SETS = [
    {"1": "1개", "2": "2개", "3": "3개", "4": "4개", "5": "5개"},
    {"1": "1개", "2": "2개", "3": "3개", "4": "4개"},
]

total_removed = 0
files_touched = 0

for f in sorted(glob.glob(os.path.join(DATA_DIR, "*.json"))):
    try:
        data = json.loads(open(f, encoding="utf-8").read())
    except Exception:
        continue
    if not isinstance(data, list):
        continue

    kept = []
    removed_here = 0
    for q in data:
        ch = q.get("choices") or {}
        if ch in COUNT_ONLY_SETS:
            removed_here += 1
            continue
        answers = q.get("answers") or []
        if any(str(a) not in ch for a in answers):
            removed_here += 1
            continue
        kept.append(q)

    if removed_here:
        with open(f, "w", encoding="utf-8") as out:
            out.write(json.dumps(kept, ensure_ascii=False))
        print(f"{os.path.basename(f)}: {len(data)} -> {len(kept)} ({removed_here}건 제거)")
        total_removed += removed_here
        files_touched += 1

print(f"\n총 {files_touched}개 파일에서 {total_removed}건 제거")
