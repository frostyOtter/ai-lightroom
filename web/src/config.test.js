import { describe, it, expect, beforeEach, vi } from 'vitest'
import config, { validateConfig } from './config.js'

describe('config', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  describe('default values', () => {
    it('has default apiUrl', () => {
      expect(config.apiUrl).toBe('http://localhost:8000')
    })

    it('has default apiTimeout', () => {
      expect(config.apiTimeout).toBe(30000)
    })

    it('has default maxFileSize', () => {
      expect(config.maxFileSize).toBe(10485760)
    })

    it('has default enableBatchProcessing', () => {
      expect(config.enableBatchProcessing).toBe(false)
    })

    it('has default enableUserAccounts', () => {
      expect(config.enableUserAccounts).toBe(false)
    })

    it('has isDev property', () => {
      expect(typeof config.isDev).toBe('boolean')
    })

    it('has isProd property', () => {
      expect(typeof config.isProd).toBe('boolean')
    })
  })

  describe('validateConfig', () => {
    it('returns config object when valid', () => {
      const result = validateConfig()
      expect(result).toHaveProperty('apiUrl')
      expect(result).toHaveProperty('apiTimeout')
      expect(result).toHaveProperty('maxFileSize')
    })

    it('does not throw when configuration is valid', () => {
      expect(() => {
        validateConfig()
      }).not.toThrow()
    })
  })

  describe('environment variable loading', () => {
    it('loads VITE_API_URL from environment', () => {
      expect(config.apiUrl).toBeDefined()
      expect(typeof config.apiUrl).toBe('string')
    })

    it('loads VITE_API_TIMEOUT from environment', () => {
      expect(config.apiTimeout).toBeDefined()
      expect(typeof config.apiTimeout).toBe('number')
    })

    it('loads VITE_MAX_FILE_SIZE from environment', () => {
      expect(config.maxFileSize).toBeDefined()
      expect(typeof config.maxFileSize).toBe('number')
    })

    it('converts VITE_ENABLE_BATCH_PROCESSING to boolean', () => {
      expect(typeof config.enableBatchProcessing).toBe('boolean')
    })

    it('converts VITE_ENABLE_USER_ACCOUNTS to boolean', () => {
      expect(typeof config.enableUserAccounts).toBe('boolean')
    })
  })

  describe('type validation', () => {
    it('apiUrl is a string', () => {
      expect(typeof config.apiUrl).toBe('string')
    })

    it('apiTimeout is a number', () => {
      expect(typeof config.apiTimeout).toBe('number')
    })

    it('maxFileSize is a number', () => {
      expect(typeof config.maxFileSize).toBe('number')
    })

    it('enableBatchProcessing is a boolean', () => {
      expect(typeof config.enableBatchProcessing).toBe('boolean')
    })

    it('enableUserAccounts is a boolean', () => {
      expect(typeof config.enableUserAccounts).toBe('boolean')
    })
  })

  describe('config structure', () => {
    it('has all required properties', () => {
      expect(config).toHaveProperty('apiUrl')
      expect(config).toHaveProperty('apiTimeout')
      expect(config).toHaveProperty('maxFileSize')
      expect(config).toHaveProperty('enableBatchProcessing')
      expect(config).toHaveProperty('enableUserAccounts')
      expect(config).toHaveProperty('isDev')
      expect(config).toHaveProperty('isProd')
    })
  })

  describe('dev/prod mode', () => {
    it('isDev and isProd are mutually exclusive', () => {
      expect(config.isDev !== config.isProd).toBe(true)
    })

    it('at least one of isDev or isProd is true', () => {
      expect(config.isDev || config.isProd).toBe(true)
    })
  })

  describe('validation edge cases', () => {
    it('accepts default maxFileSize value', () => {
      expect(config.maxFileSize).toBeGreaterThan(0)
    })

    it('accepts default apiTimeout value', () => {
      expect(config.apiTimeout).toBeGreaterThanOrEqual(1000)
    })
  })
})
