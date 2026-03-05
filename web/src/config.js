const requiredEnvVars = [
  'VITE_API_URL',
]

const config = {
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  apiTimeout: Number(import.meta.env.VITE_API_TIMEOUT) || 30000,
  
  maxFileSize: Number(import.meta.env.VITE_MAX_FILE_SIZE) || 10485760,
  
  enableBatchProcessing: import.meta.env.VITE_ENABLE_BATCH_PROCESSING === 'true',
  enableUserAccounts: import.meta.env.VITE_ENABLE_USER_ACCOUNTS === 'true',
  
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
}

export function validateConfig() {
  const errors = []
  
  for (const envVar of requiredEnvVars) {
    if (!import.meta.env[envVar]) {
      errors.push(`Missing required environment variable: ${envVar}`)
    }
  }
  
  if (config.maxFileSize < 1) {
    errors.push('VITE_MAX_FILE_SIZE must be positive')
  }
  
  if (config.apiTimeout < 1000) {
    errors.push('VITE_API_TIMEOUT should be at least 1000ms')
  }
  
  if (errors.length > 0) {
    console.error('\n❌ Configuration Errors:\n')
    errors.forEach(error => console.error(`  • ${error}`))
    console.error('\nPlease check your .env file and try again.\n')
    throw new Error('Invalid configuration')
  }
  
  return config
}

export default config
