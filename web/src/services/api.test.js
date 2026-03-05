import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

describe('API Service', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('module exists', () => {
    it('can be imported', async () => {
      const api = (await import('./api.js')).default
      expect(api).toBeDefined()
    })
  })

  describe('default configuration', () => {
    it('has expected configuration structure', async () => {
      const api = (await import('./api.js')).default
      expect(api).toBeDefined()
      expect(typeof api).toBe('function')
      expect(api.get).toBeDefined()
      expect(api.post).toBeDefined()
    })
  })
})
