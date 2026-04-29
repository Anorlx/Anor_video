import axios from 'axios'
import { getToken } from './auth.js'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000,
})

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function parseVideo(url) {
  const { data } = await api.post('/parse', { url }, { headers: authHeaders() })
  return data
}

export async function getDirectUrl(url, formatId) {
  const { data } = await api.post('/direct-url', { url, format_id: formatId })
  return data
}

export function getDownloadUrl() {
  return '/api/download'
}

export async function downloadViaServer(url, formatId) {
  const response = await api.post(
    '/download',
    { url, format_id: formatId },
    { responseType: 'blob', timeout: 600000 }
  )
  return response
}
