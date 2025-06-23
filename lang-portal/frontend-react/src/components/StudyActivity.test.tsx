import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import StudyActivity from './StudyActivity'

const mockActivity = {
  id: 1,
  preview_url: '/assets/flashcards.png',
  title: 'Flashcards',
  launch_url: 'https://flashcards.example.com',
}

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>)
}

describe('StudyActivity', () => {
  it('should render activity information', () => {
    renderWithRouter(<StudyActivity activity={mockActivity} />)

    expect(screen.getByText('Flashcards')).toBeInTheDocument()
    expect(screen.getByAltText('Flashcards')).toBeInTheDocument()
  })

  it('should render preview image with correct src', () => {
    renderWithRouter(<StudyActivity activity={mockActivity} />)

    const image = screen.getByAltText('Flashcards') as HTMLImageElement
    expect(image.src).toContain('/assets/flashcards.png')
  })

  it('should render Launch button with correct link', () => {
    renderWithRouter(<StudyActivity activity={mockActivity} />)

    const launchLink = screen.getByRole('link', { name: 'Launch' })
    expect(launchLink).toHaveAttribute('href', '/study-activities/1/launch')
  })

  it('should render View button with correct link', () => {
    renderWithRouter(<StudyActivity activity={mockActivity} />)

    const viewLink = screen.getByRole('link', { name: 'View' })
    expect(viewLink).toHaveAttribute('href', '/study-activities/1')
  })

  it('should have proper styling classes', () => {
    const { container } = renderWithRouter(<StudyActivity activity={mockActivity} />)

    const card = container.firstChild
    expect(card).toHaveClass('bg-sidebar', 'rounded-lg', 'shadow-md', 'overflow-hidden')
  })

  it('should handle activities with different IDs', () => {
    const activity2 = {
      id: 42,
      preview_url: '/assets/quiz.png',
      title: 'Quiz App',
      launch_url: 'https://quiz.example.com',
    }

    renderWithRouter(<StudyActivity activity={activity2} />)

    const launchLink = screen.getByRole('link', { name: 'Launch' })
    expect(launchLink).toHaveAttribute('href', '/study-activities/42/launch')

    const viewLink = screen.getByRole('link', { name: 'View' })
    expect(viewLink).toHaveAttribute('href', '/study-activities/42')
  })
})