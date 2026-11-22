export const isRequestCanceled = (err: any): boolean => {
  return err?.name === 'CanceledError' || err?.code === 'ERR_CANCELED' || err?.message === 'canceled'
}

export interface SafeApiErrorDetails {
  operation: string
  params: Record<string, any>
  statusCode: number | null
  statusText: string | null
  serverMessage: string | null
  errorMessage: string
  timestamp: string
}

export interface SafeApiResult<T = any> {
  status: 'success' | 'canceled' | 'error'
  data: T[]
  raw: any
  count: number
  isEmpty: boolean
  error: SafeApiErrorDetails | null
}

/**
 * Executes an API fetch function safely with:
 * 1. Distinction between 3 states: Data exists, Data genuinely empty, and Data load error.
 * 2. Structured diagnostic logging (Operation, params, HTTP status, server message, timestamp).
 * 3. Graceful handling of AbortController cancellations without false error alerts.
 */
export const safeApiFetch = async <T = any>(
  operationName: string,
  fetchFn: () => Promise<any>,
  params: Record<string, any> = {}
): Promise<SafeApiResult<T>> => {
  try {
    const res = await fetchFn()
    const rawData = res?.data
    let results: T[] = []
    if (rawData && Array.isArray(rawData.results)) {
      results = rawData.results
    } else if (Array.isArray(rawData)) {
      results = rawData
    } else if (rawData && typeof rawData === 'object' && rawData.data && Array.isArray(rawData.data)) {
      results = rawData.data
    }

    return {
      status: 'success',
      data: results,
      raw: rawData,
      count: results.length,
      isEmpty: results.length === 0,
      error: null,
    }
  } catch (err: any) {
    if (isRequestCanceled(err)) {
      return {
        status: 'canceled',
        data: [],
        raw: null,
        count: 0,
        isEmpty: false,
        error: null,
      }
    }

    const errDetails: SafeApiErrorDetails = {
      operation: operationName,
      params,
      statusCode: err?.response?.status || null,
      statusText: err?.response?.statusText || null,
      serverMessage: err?.response?.data?.message || err?.response?.data?.detail || err?.response?.data?.error || null,
      errorMessage: err?.message || 'تعذر الاتصال بالخادم',
      timestamp: new Date().toISOString(),
    }

    console.error(`[OMR Registry API Error] فشل في عملية: ${operationName}`, errDetails)

    return {
      status: 'error',
      data: [],
      raw: null,
      count: 0,
      isEmpty: false,
      error: errDetails,
    }
  }
}
