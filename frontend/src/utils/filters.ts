/** Reject repeated parameters, non-integers and values outside the supported range. */
export function parseFilterInteger(value: unknown, maximum = Number.MAX_SAFE_INTEGER): number | null {
  if (typeof value !== 'string' || !/^\d+$/.test(value)) return null
  const number = Number(value)
  return Number.isSafeInteger(number) && number > 0 && number <= maximum ? number : null
}
