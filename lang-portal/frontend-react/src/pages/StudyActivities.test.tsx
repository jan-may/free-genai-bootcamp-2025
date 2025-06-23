import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import StudyActivities from './StudyActivities'

// Mock fetch globally
global.fetch = vi.fn()

const mockActivities = [
  {
    id: 1,
    preview_url: '/assets/flashcards.png',
    title: 'Flashcards',
    launch_url: 'https://flashcards.example.com',
  },
  {
    id: 2,
    preview_url: '/assets/quiz.png',
    title: 'Quiz App',
    launch_url: 'https://quiz.example.com',
  },
]

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>)
}

describe('StudyActivities Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render loading state initially', () => {
    global.fetch = vi.fn().mockImplementation(() => new Promise(() => {}))
    renderWithRouter(<StudyActivities />)
    
    expect(screen.getByText('Loading study activities...')).toBeInTheDocument()
  })

  it('should fetch and display activities', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => mockActivities,
    } as Response)

    renderWithRouter(<StudyActivities />)

    await waitFor(() => {
      expect(screen.getByText('Flashcards')).toBeInTheDocument()
      expect(screen.getByText('Quiz App')).toBeInTheDocument()
    })

    expect(global.fetch).toHaveBeenCalledWith('http://localhost:5000/api/study-activities')
  })

  it('should display error message on fetch failure', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
    } as Response)

    renderWithRouter(<StudyActivities />)

    await waitFor(() => {
      expect(screen.getByText('Error: Failed to fetch study activities')).toBeInTheDocument()
    })
  })

  it('should display error message on network error', async () => {
    global.fetch = vi.fn().mockRejectedValueOnce(new Error('Network error'))

    renderWithRouter(<StudyActivities />)

    await waitFor(() => {
      expect(screen.getByText('Error: Network error')).toBeInTheDocument()
    })
  })

  it('should render activities in grid layout', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => mockActivities,
    } as Response)

    const { container } = renderWithRouter(<StudyActivities />)

    await waitFor(() => {
      const grid = container.querySelector('.grid')
      expect(grid).toHaveClass('grid-cols-1', 'md:grid-cols-2', 'lg:grid-cols-3')
    })
  })

  it('should render multiple StudyActivity components', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => mockActivities,
    } as Response)

    renderWithRouter(<StudyActivities />)

    await waitFor(() => {
      const launchButtons = screen.getAllByText('Launch')
      expect(launchButtons).toHaveLength(2)
      
      const viewButtons = screen.getAllByText('View')
      expect(viewButtons).toHaveLength(2)
    })
  })

  it('should handle empty activities array', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    } as Response)

    const { container } = renderWithRouter(<StudyActivities />)

    await waitFor(() => {
      const grid = container.querySelector('.grid')
      expect(grid).toBeInTheDocument()
      expect(grid?.children).toHaveLength(0)
    })
  })

  it('should pass correct props to StudyActivity components', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => mockActivities,
    } as Response)

    renderWithRouter(<StudyActivities />)

    await waitFor(() => {
      // Check that activity titles are rendered
      expect(screen.getByText('Flashcards')).toBeInTheDocument()
      expect(screen.getByText('Quiz App')).toBeInTheDocument()
      
      // Check that images are rendered with correct alt text
      expect(screen.getByAltText('Flashcards')).toBeInTheDocument()
      expect(screen.getByAltText('Quiz App')).toBeInTheDocument()
    })
  })
})