import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App.jsx'

describe('App Component', () => {
  it('renders without crashing', () => {
    render(<App />)
  })

  it('renders main heading', () => {
    render(<App />)
    const heading = screen.getByText('AI Lightroom')
    expect(heading).toBeInTheDocument()
  })

  it('renders subtitle', () => {
    render(<App />)
    const subtitle = screen.getByText('AI-powered image color adjustment tool')
    expect(subtitle).toBeInTheDocument()
  })

  it('has correct styling classes', () => {
    render(<App />)
    const container = screen.getByText('AI Lightroom').closest('.min-h-screen')
    expect(container).toHaveClass('min-h-screen', 'bg-gray-50', 'flex', 'items-center', 'justify-center')
  })

  it('renders text center container', () => {
    render(<App />)
    const textCenter = screen.getByText('AI Lightroom').closest('.text-center')
    expect(textCenter).toBeInTheDocument()
  })

  it('heading has correct text styling', () => {
    render(<App />)
    const heading = screen.getByText('AI Lightroom')
    expect(heading).toHaveClass('text-4xl', 'font-bold', 'text-primary-600', 'mb-4')
  })

  it('subtitle has correct text styling', () => {
    render(<App />)
    const subtitle = screen.getByText('AI-powered image color adjustment tool')
    expect(subtitle).toHaveClass('text-gray-600')
  })

  it('renders in document body', () => {
    render(<App />)
    const container = document.querySelector('.min-h-screen')
    expect(container).toBeInTheDocument()
  })

  it('has correct page structure', () => {
    const { container } = render(<App />)
    const rootDiv = container.firstChild
    expect(rootDiv).toHaveClass('min-h-screen', 'bg-gray-50', 'flex', 'items-center', 'justify-center')
  })

  it('text content is accessible', () => {
    render(<App />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
    expect(heading).toHaveTextContent('AI Lightroom')
  })

  it('heading is h1 element', () => {
    render(<App />)
    const heading = screen.getByText('AI Lightroom')
    expect(heading.tagName).toBe('H1')
  })

  it('subtitle is paragraph element', () => {
    render(<App />)
    const subtitle = screen.getByText('AI-powered image color adjustment tool')
    expect(subtitle.tagName).toBe('P')
  })

  it('does not have console errors', () => {
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    render(<App />)
    expect(consoleErrorSpy).not.toHaveBeenCalled()
    consoleErrorSpy.mockRestore()
  })

  it('renders correctly multiple times', () => {
    const { unmount } = render(<App />)
    expect(screen.getByText('AI Lightroom')).toBeInTheDocument()
    
    unmount()
    
    render(<App />)
    expect(screen.getByText('AI Lightroom')).toBeInTheDocument()
  })
})
