/**
 * Форматирует число, добавляя пробелы в качестве разделителей тысяч
 * @param {number|string} num - Число для форматирования
 * @returns {string} Отформатированное число
 */
export function formatNumber(num) {
  if (num === null || num === undefined) return '0'
  return Number(num).toLocaleString('ru-RU', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
}

