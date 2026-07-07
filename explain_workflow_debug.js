export const meta = {
  name: 'gosa-explain-debug',
  description: 'debug args shape',
  phases: [{ title: 'Debug' }],
}

log(`args=${JSON.stringify(args).slice(0,200)}`)
log(`typeof args=${typeof args}`)
const ranges = args && args.ranges
log(`isArray ranges=${Array.isArray(ranges)}`)

return { ok: true, ranges }
