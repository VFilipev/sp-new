const getCookieValue = (name) => {
  if (!import.meta.client) return null
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${name}=`))
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : null
}

export const useAdminContentApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const ensureCsrf = async () => {
    await $fetch(`${apiBase}/auth/csrf/`, {
      method: "GET",
      credentials: "include",
    })
  }

  const patch = async (endpoint, payload) => {
    await ensureCsrf()
    const csrfToken = getCookieValue("csrftoken")

    return await $fetch(`${apiBase}${endpoint}`, {
      method: "PATCH",
      body: payload,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
      },
    })
  }

  const get = async (endpoint) => {
    await ensureCsrf()
    return await $fetch(`${apiBase}${endpoint}`, {
      method: "GET",
      credentials: "include",
    })
  }

  const post = async (endpoint, payload) => {
    await ensureCsrf()
    const csrfToken = getCookieValue("csrftoken")

    return await $fetch(`${apiBase}${endpoint}`, {
      method: "POST",
      body: payload,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
      },
    })
  }

  const postForm = async (endpoint, formData) => {
    await ensureCsrf()
    const csrfToken = getCookieValue("csrftoken")

    return await $fetch(`${apiBase}${endpoint}`, {
      method: "POST",
      body: formData,
      credentials: "include",
      headers: {
        ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
      },
    })
  }

  return { get, patch, post, postForm }
}
