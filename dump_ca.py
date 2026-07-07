import json

def dump_file(json_path, out_path):
    data = json.load(open(json_path, encoding='utf-8'))
    lines = []
    for q in data:
        lines.append(f"id={q['id']} date={q['date']} sub={q['subject']} A={q['answers']}")
        lines.append(f"  Q: {q['question']}")
        for k, v in sorted(q['choices'].items()):
            lines.append(f"    {k}: {v}")
        lines.append("")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"{json_path}: {len(data)}문항 저장")

dump_file('data/컴퓨터활용능력_1급.json', 'C:/Users/ingma/AppData/Local/Temp/ca_1.txt')
dump_file('data/컴퓨터활용능력_2급.json', 'C:/Users/ingma/AppData/Local/Temp/ca_2.txt')
