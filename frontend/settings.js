const url = (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE_URL)
  ? import.meta.env.VITE_API_BASE_URL
  : "http://localhost:5001/"

function remove_http(rawUrl) {
  return rawUrl.replace(/^https?:\/\//, '')
}

const websocket_url = (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_WS_URL)
  ? import.meta.env.VITE_WS_URL
  : remove_http(url)

var settings = {
  port: (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_PORT)
    ? Number(import.meta.env.VITE_PORT)
    : 3094,
  CLIENT_SECRET: (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_CLIENT_SECRET)
    ? import.meta.env.VITE_CLIENT_SECRET
    : '0b174bccbb1205107c86b85ce96f933698835335e3dd2c3565daeaf48e0406c9',
  url: url,
  websocket_url: websocket_url,
  url_sidbar: url,
  url_login: url,
  multiple_company: false,
  url_field: "screens/screen/",
  api_key: (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_KEY)
    ? import.meta.env.VITE_API_KEY
    : "qwertyuiop",
  current_year: {},
  drawer: {
    type: 'nav-bar',
    width: '300',
    height: ''
  },
  dialog: {
    width: '500',
    height: '500'
  }
}

export default settings
