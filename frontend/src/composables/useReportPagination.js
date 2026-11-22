import { ref } from 'vue'

export function useReportPagination(defaultPageSize = 20) {
  const loading = ref(false)
  const items = ref({
    results: [],
    count: 0,
    pagination: {
      count: 0,
      total: 0,
      num_pages: 1,
      current_page: 1,
      page_size: defaultPageSize
    }
  })

  const currentTableParams = ref({
    page: 1,
    page_size: defaultPageSize,
    search: '',
    sort_by: ''
  })

  /**
   * Extracts pagination, search, and sorting parameters from custom-data-table or direct call.
   * If tableParams has params object (from custom-data-table), extracts them.
   * If tableParams has page or page_size directly, extracts them.
   * Otherwise (filter button click), keeps page_size and resets page to 1.
   */
  const extractParams = (tableParams = {}) => {
    if (tableParams && tableParams.params) {
      currentTableParams.value = {
        page: tableParams.params.page || 1,
        page_size: tableParams.params.page_size || defaultPageSize,
        search: tableParams.params.search || '',
        sort_by: tableParams.params.sort_by || ''
      }
    } else if (tableParams && (tableParams.page || tableParams.page_size)) {
      currentTableParams.value = {
        page: tableParams.page || 1,
        page_size: tableParams.page_size || defaultPageSize,
        search: tableParams.search || currentTableParams.value.search || '',
        sort_by: tableParams.sort_by || currentTableParams.value.sort_by || ''
      }
    } else {
      currentTableParams.value.page = 1
    }
    return { ...currentTableParams.value }
  }

  /**
   * Sets API response into items object with unified pagination metadata for custom-data-table.
   */
  const setResponse = (res) => {
    const results = Array.isArray(res) ? res : (res?.results || [])
    const totalCount = res?.pagination?.count ?? res?.count ?? results.length
    const pageSize = res?.pagination?.page_size ?? currentTableParams.value.page_size ?? defaultPageSize
    const currentPage = res?.pagination?.current_page ?? currentTableParams.value.page ?? 1
    const numPages = res?.pagination?.num_pages ?? Math.max(1, Math.ceil(totalCount / (pageSize || 1)))

    items.value = {
      results,
      count: totalCount,
      pagination: {
        count: totalCount,
        total: totalCount,
        num_pages: numPages,
        current_page: currentPage,
        page_size: pageSize
      }
    }
  }

  const resetPagination = () => {
    currentTableParams.value.page = 1
    currentTableParams.value.search = ''
    currentTableParams.value.sort_by = ''
  }

  return {
    loading,
    items,
    currentTableParams,
    extractParams,
    setResponse,
    resetPagination
  }
}
