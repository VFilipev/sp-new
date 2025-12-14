export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.hook('app:error', (error) => {
    console.error('App error:', error)
    // Здесь можно добавить отправку ошибок в систему мониторинга
    // Например, Sentry, LogRocket и т.д.
  })

  // Обработка ошибок при загрузке данных
  nuxtApp.hook('vue:error', (error, instance, info) => {
    console.error('Vue error:', error, info)
  })
})

