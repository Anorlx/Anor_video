import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

const backendPort = process.env.VITE_BACKEND_PORT || process.env.BACKEND_PORT || '8010'
const frontendPort = Number.parseInt(
  process.env.VITE_FRONTEND_PORT || process.env.FRONTEND_PORT || '5180',
  10,
)

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    port: frontendPort,
    strictPort: true,
    proxy: {
      '/api': {
        target: `http://localhost:${backendPort}`,
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
})
