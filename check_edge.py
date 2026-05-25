import json

out = open(r"C:\개인\wooahouse\wooaGosa\edge_out.txt", "w", encoding="utf-8")

# Q509 확인 (면허1,2종)
with open(r"C:\개인\wooahouse\wooaGosa\data\license_1_2.json", encoding="utf-8") as f:
    qs1 = json.load(f)

q509 = qs1[508]
out.write("=== Q509 ===\n")
out.write(f"질문: {q509['question']}\n")
out.write(f"보기: {q509['choices']}\n")
out.write(f"정답: {q509['answers']}\n")
out.write(f"해설: {q509['explanation'][:300]}\n")

# Q3 확인 (이륜자동차)
with open(r"C:\개인\wooahouse\wooaGosa\data\motorcycle.json", encoding="utf-8") as f:
    qs2 = json.load(f)

q2 = qs2[1]
q3 = qs2[2]
out.write("\n=== 이륜Q2 ===\n")
out.write(f"질문: {q2['question'][:100]}\n")
out.write(f"보기: {q2['choices']}\n")
out.write(f"정답: {q2['answers']}\n")
out.write(f"해설 끝: {q2['explanation'][-300:]}\n")

out.write("\n=== 이륜Q3 ===\n")
out.write(f"질문: {q3['question'][:100]}\n")
out.write(f"보기: {q3['choices']}\n")
out.write(f"정답: {q3['answers']}\n")

out.close()
print("done")
