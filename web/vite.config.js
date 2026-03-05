import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react()],
    server: {
      port: 5173,
      host: true,
    },
    test: {
      globals: true,
      environment: 'happy-dom',
      setupFiles: './src/test/setup.js',
      env: {
        VITE_API_URL: env.VITE_API_URL || 'http://localhost:8000',
        VITE_API_TIMEOUT: env.VITE_API_TIMEOUT || '30000',
        VITE_MAX_FILE_SIZE: env.VITE_MAX_FILE_SIZE || '10485760',
        VITE_ENABLE_BATCH_PROCESSING: env.VITE_ENABLE_BATCH_PROCESSING || 'false',
        VITE_ENABLE_USER_ACCOUNTS: env.VITE_ENABLE_USER_ACCOUNTS || 'false',
      },
    },
  }
})
