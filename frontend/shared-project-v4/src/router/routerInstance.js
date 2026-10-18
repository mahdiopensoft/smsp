let _router = null

export function setRouter(router) {
  _router = router
}

export function getRouter() {
  if (!_router) {
    throw new Error('Router is not initialized yet')
  }
  return _router
}
