import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

// ---------------------------------------------------------------------------
// Helper: import the api module fresh for each test group that needs isolation
// ---------------------------------------------------------------------------

describe('API Service', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  // -------------------------------------------------------------------------
  // Module contract
  // -------------------------------------------------------------------------

  describe('module contract', () => {
    it('can be imported', async () => {
      const api = (await import('./api.js')).default
      expect(api).toBeDefined()
    })

    it('exports a callable function (axios instance)', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api).toBe('function')
    })

    it('has a .get method', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.get).toBe('function')
    })

    it('has a .post method', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.post).toBe('function')
    })

    it('has a .put method', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.put).toBe('function')
    })

    it('has a .delete method', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.delete).toBe('function')
    })

    it('has a .patch method', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.patch).toBe('function')
    })

    it('has a .head method', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.head).toBe('function')
    })

    it('has a .options method', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.options).toBe('function')
    })

    it('has a .request method', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.request).toBe('function')
    })

    it('is a default export', async () => {
      const mod = await import('./api.js')
      expect(mod.default).toBeDefined()
    })

    it('has no named exports', async () => {
      const mod = await import('./api.js')
      const namedExports = Object.keys(mod).filter((k) => k !== 'default')
      expect(namedExports).toHaveLength(0)
    })
  })

  // -------------------------------------------------------------------------
  // Axios instance configuration (defaults)
  // -------------------------------------------------------------------------

  describe('axios instance configuration', () => {
    it('has defaults object', async () => {
      const api = (await import('./api.js')).default
      expect(api.defaults).toBeDefined()
    })

    it('defaults.baseURL is set', async () => {
      const api = (await import('./api.js')).default
      expect(api.defaults.baseURL).toBeDefined()
    })

    it('defaults.baseURL is the expected backend URL', async () => {
      const api = (await import('./api.js')).default
      // Vite test env injects VITE_API_URL=http://localhost:8000 (from vite.config.js)
      expect(api.defaults.baseURL).toBe('http://localhost:8000')
    })

    it('defaults.baseURL is a string', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.defaults.baseURL).toBe('string')
    })

    it('defaults.baseURL starts with http', async () => {
      const api = (await import('./api.js')).default
      expect(api.defaults.baseURL).toMatch(/^https?:\/\//)
    })

    it('defaults.timeout is set', async () => {
      const api = (await import('./api.js')).default
      expect(api.defaults.timeout).toBeDefined()
    })

    it('defaults.timeout is a number', async () => {
      const api = (await import('./api.js')).default
      expect(typeof api.defaults.timeout).toBe('number')
    })

    it('defaults.timeout is 30000 (matches VITE_API_TIMEOUT default)', async () => {
      const api = (await import('./api.js')).default
      expect(api.defaults.timeout).toBe(30000)
    })

    it('defaults.timeout is at least 1000ms', async () => {
      const api = (await import('./api.js')).default
      expect(api.defaults.timeout).toBeGreaterThanOrEqual(1000)
    })
  })

  // -------------------------------------------------------------------------
  // Request headers
  // -------------------------------------------------------------------------

  describe('default request headers', () => {
    it('sets Content-Type to application/json', async () => {
      const api = (await import('./api.js')).default
      // Axios stores per-method and common headers on defaults.headers
      const headers = api.defaults.headers
      const contentType =
        headers?.['Content-Type'] ||
        headers?.common?.['Content-Type'] ||
        headers?.post?.['Content-Type']
      expect(contentType).toBe('application/json')
    })
  })

  // -------------------------------------------------------------------------
  // Interceptors scaffold
  // -------------------------------------------------------------------------

  describe('interceptor infrastructure', () => {
    it('exposes interceptors.request', async () => {
      const api = (await import('./api.js')).default
      expect(api.interceptors).toBeDefined()
      expect(api.interceptors.request).toBeDefined()
    })

    it('exposes interceptors.response', async () => {
      const api = (await import('./api.js')).default
      expect(api.interceptors.response).toBeDefined()
    })
  })

  // -------------------------------------------------------------------------
  // Singleton: same instance across multiple imports in same module scope
  // -------------------------------------------------------------------------

  describe('singleton instance', () => {
    it('returns the same instance on repeated imports', async () => {
      const { default: api1 } = await import('./api.js')
      const { default: api2 } = await import('./api.js')
      expect(api1).toBe(api2)
    })
  })
})
