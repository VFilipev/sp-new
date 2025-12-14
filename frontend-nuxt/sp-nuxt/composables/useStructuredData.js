export const useStructuredData = (data) => {
  useHead({
    script: [
      {
        type: 'application/ld+json',
        children: JSON.stringify(data),
      },
    ],
  })
}

