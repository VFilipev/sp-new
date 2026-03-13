export const useAdminEditMode = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const isEditMode = useState('is-edit-mode-enabled', () => false)

  const { data, error, pending, refresh } = useFetch(`${apiBase}/auth/admin-status/`, {
    key: 'admin-status',
    method: 'GET',
    server: false,
    credentials: 'include',
    retry: 0,
    default: () => ({
      is_authenticated: false,
      is_staff: false,
      is_superuser: false,
      can_edit: false,
      username: '',
    }),
  })

  const isAdmin = computed(() => Boolean(data.value?.can_edit))
  const adminName = computed(() => data.value?.username || '')

  const enableEditMode = () => {
    if (isAdmin.value) isEditMode.value = true
  }

  const disableEditMode = () => {
    isEditMode.value = false
  }

  const toggleEditMode = () => {
    if (!isAdmin.value) return
    isEditMode.value = !isEditMode.value
  }

  return {
    isAdmin,
    adminName,
    isEditMode,
    pending,
    error,
    refresh,
    enableEditMode,
    disableEditMode,
    toggleEditMode,
  }
}
