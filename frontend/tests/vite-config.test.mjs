// @vitest-environment node
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import { describe, expect, it } from 'vitest'

const configUrl = pathToFileURL(resolve('vite.config.js'))

async function loadConfig(cacheKey) {
  const url = new URL(configUrl)
  url.search = cacheKey
  const { default: config } = await import(url.href)
  return config
}

describe('vite config', () => {
  it('frontend dev server defaults to port 5180', async () => {
    const originalVitePort = process.env.VITE_FRONTEND_PORT
    const originalPort = process.env.FRONTEND_PORT

    delete process.env.VITE_FRONTEND_PORT
    delete process.env.FRONTEND_PORT

    try {
      const config = await loadConfig('?default-port')
      expect(config.server.port).toBe(5180)
      expect(config.server.strictPort).toBe(true)
    } finally {
      if (originalVitePort === undefined) delete process.env.VITE_FRONTEND_PORT
      else process.env.VITE_FRONTEND_PORT = originalVitePort

      if (originalPort === undefined) delete process.env.FRONTEND_PORT
      else process.env.FRONTEND_PORT = originalPort
    }
  })

  it('frontend dev server port can be overridden with env', async () => {
    const originalVitePort = process.env.VITE_FRONTEND_PORT
    const originalPort = process.env.FRONTEND_PORT

    process.env.VITE_FRONTEND_PORT = '5199'
    delete process.env.FRONTEND_PORT

    try {
      const config = await loadConfig('?override-port')
      expect(config.server.port).toBe(5199)
    } finally {
      if (originalVitePort === undefined) delete process.env.VITE_FRONTEND_PORT
      else process.env.VITE_FRONTEND_PORT = originalVitePort

      if (originalPort === undefined) delete process.env.FRONTEND_PORT
      else process.env.FRONTEND_PORT = originalPort
    }
  })
})
