import json

for label, path in [
    ("면허1,2종", r"C:\개인\wooahouse\wooaGosa\data\license_1_2.json"),
    ("이륜자동차", r"C:\개인\wooahouse\wooaGosa\data\motorcycle.json"),
]:
    with open(path, encoding="utf-8") as f:
        qs = json.load(f)

    out = open(path.replace(".json", "_verify.txt"), "w", encoding="utf-8")
    out.write(f"=== {label} 검증 ===\n")
    out.write(f"총 문제 수: {len(qs)}\n\n")

    # 보기 없는 문제
    no_choices = [q for q in qs if len(q['choices']) == 0]
    out.write(f"보기 없는 문제: {len(no_choices)}개\n")
    for q in no_choices[:3]:
        out.write(f"  Q{q['id']}: {q['question'][:60]}\n")

    # 정답 없는 문제
    no_ans = [q for q in qs if len(q['answers']) == 0]
    out.write(f"\n정답 없는 문제: {len(no_ans)}개\n")
    for q in no_ans[:3]:
        out.write(f"  Q{q['id']}: {q['question'][:60]}\n")

    # 다중 정답 문제
    multi = [q for q in qs if len(q['answers']) >= 2]
    out.write(f"\n다중 정답 문제: {len(multi)}개\n")

    # 상황 문제
    situation = [q for q in qs if q['situation']]
    out.write(f"상황 제시 문제: {len(situation)}개\n")

    # 비디오 문제
    video = [q for q in qs if q['is_video']]
    out.write(f"동영상 문제(홈페이지 참조): {len(video)}개\n")

    out.write("\n=== 샘플 문제 ===\n")
    for idx in [0, 7, 14, 99, 499, 770, 996, len(qs)-1]:
        if idx < len(qs):
            q = qs[idx]
            out.write(f"\n[Q{q['id']}] {q['question'][:80]}\n")
            for k, v in q['choices'].items():
                out.write(f"  {k}: {v[:50]}\n")
            out.write(f"  정답: {q['answers']}\n")
            if q['situation']:
                out.write(f"  상황: {q['situation'][:60]}\n")
            out.write(f"  해설: {q['explanation'][:80]}\n")

    out.close()
    print(f"[{label}] 검증 파일 저장 완료")
