import axios from 'axios'

import { getToken } from './auth.js'

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function fetchHistory({ offset = 0, limit = 20 } = {}) {
  const { data } = await axios.get('/api/history', {
    params: { offset, limit },
    headers: authHeaders(),
  })
  return data
}
