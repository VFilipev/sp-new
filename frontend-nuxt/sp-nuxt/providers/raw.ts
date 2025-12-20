import { joinURL } from 'ufo'

/**
 * Кастомный провайдер для Nuxt Image.
 * Возвращает функцию (setup), которая возвращает объект провайдера.
 * Это исправляет ошибку "setup is not a function".
 */
export default function () {
  return {
    getImage: (src: string, { modifiers = {}, baseURL = '' } = {}) => {
      const resolvedSrc =
        src.startsWith('http') || src.startsWith('//') || src.startsWith('/')
          ? src
          : `/${src}`

      const url = joinURL(baseURL, resolvedSrc)

      return {
        url,
        // Если переданы sizes, создаем srcset, где все варианты ведут на один и тот же оригинал.
        // Это предотвращает попытки NuxtImg сделать ресайз через IPX.
        srcset: (modifiers as Record<string, any>)?.sizes
          ? String((modifiers as Record<string, any>).sizes)
              .split(',')
              .map((size) => `${url} ${size.trim()}`)
              .join(', ')
          : undefined,
      }
    },
  }
}
