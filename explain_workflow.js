export const meta = {
  name: 'gosa-explain-batch',
  description: 'Generate Korean explanations for a range of exam questions from a JSON file',
  phases: [{ title: 'Generate' }],
}

const SCHEMA = {
  type: 'object',
  properties: {
    explanations: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'number' },
          explanation: { type: 'string' },
        },
        required: ['id', 'explanation'],
      },
    },
  },
  required: ['explanations'],
}

phase('Generate')

const parsedArgs = typeof args === 'string' ? JSON.parse(args) : args
const { examName, filePath, ranges } = parsedArgs

log(`debug: typeof ranges=${typeof ranges} isArray=${Array.isArray(ranges)} len=${ranges && ranges.length}`)

const results = await pipeline(
  ranges,
  async (range, _item, idx) => {
    const [start, end] = range
    const prompt = `파일 "${filePath}"을 Read 도구로 읽으세요. 이 파일은 "${examName}" 자격증 시험의 기출문제 JSON 배열입니다. 배열 인덱스 ${start}번부터 ${end - 1}번까지(0-based)의 문제들 중 explanation 필드가 비어있는 문제에 대해서만, 정답이 왜 맞고 나머지 보기가 왜 틀렸는지 수험생이 이해하기 쉽게 3~5문장으로 간결하게 한국어 해설을 작성하세요. 파일은 수정하지 말고, 각 문제의 id와 explanation을 결과로 반환하세요.`

    const out = await agent(prompt, { label: `${examName}:${start}-${end}`, schema: SCHEMA })
    return { idx, range, explanations: out?.explanations || [] }
  }
)

return { examName, batchResults: results.filter(Boolean) }
