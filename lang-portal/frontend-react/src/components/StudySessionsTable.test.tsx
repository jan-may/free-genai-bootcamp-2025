import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import StudySessionsTable from './StudySessionsTable'
import type { StudySession } from '../services/api'

const mockSessions: StudySession[] = [
  {
    id: 1,
    group_id: 1,
    group_name: 'Nouns',
    activity_id: 1,
    activity_name: 'Flashcards',
    start_time: '2024-01-20T10:30:00Z',
    end_time: '2024-01-20T11:00:00Z',
    review_items_count: 20,
  },
  {
    id: 2,
    group_id: 2,
    group_name: 'Verbs',
    activity_id: 2,
    activity_name: 'Quiz',
    start_time: '2024-01-19T14:15:00Z',
    end_time: '2024-01-19T14:45:00Z',
    review_items_count: 15,
  },
]

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>)
}

describe('StudySessionsTable', () => {
  it('should render sessions correctly', () => {
    renderWithRouter(
      <StudySessionsTable
        sessions={mockSessions}
        sortKey="id"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    // Check if session IDs are displayed as links
    expect(screen.getByRole('link', { name: '1' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: '2' })).toBeInTheDocument()
    
    // Check if activity names are displayed
    expect(screen.getByText('Flashcards')).toBeInTheDocument()
    expect(screen.getByText('Quiz')).toBeInTheDocument()
    
    // Check if group names are displayed
    expect(screen.getByText('Nouns')).toBeInTheDocument()
    expect(screen.getByText('Verbs')).toBeInTheDocument()
  })

  it('should display review items count', () => {
    renderWithRouter(
      <StudySessionsTable
        sessions={mockSessions}
        sortKey="id"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    expect(screen.getByText('20')).toBeInTheDocument()
    expect(screen.getByText('15')).toBeInTheDocument()
  })

  it('should show sort indicators', () => {
    const { rerender } = renderWithRouter(
      <StudySessionsTable
        sessions={mockSessions}
        sortKey="id"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    // Check for ascending sort indicator on ID column
    const idHeader = screen.getByText('id').closest('th')
    expect(idHeader?.querySelector('svg')).toBeInTheDocument()

    // Rerender with descending sort
    rerender(
      <BrowserRouter>
        <StudySessionsTable
          sessions={mockSessions}
          sortKey="id"
          sortDirection="desc"
          onSort={vi.fn()}
        />
      </BrowserRouter>
    )

    // Sort indicator should still be present
    expect(idHeader?.querySelector('svg')).toBeInTheDocument()
  })

  it('should call onSort when column header is clicked', () => {
    const onSort = vi.fn()
    renderWithRouter(
      <StudySessionsTable
        sessions={mockSessions}
        sortKey="id"
        sortDirection="asc"
        onSort={onSort}
      />
    )

    // Click on Activity Name column header
    fireEvent.click(screen.getByText('activity name'))
    expect(onSort).toHaveBeenCalledWith('activity_name')

    // Click on Group Name column header
    fireEvent.click(screen.getByText('group name'))
    expect(onSort).toHaveBeenCalledWith('group_name')
  })

  it('should render links to session details', () => {
    renderWithRouter(
      <StudySessionsTable
        sessions={mockSessions}
        sortKey="id"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    const session1Link = screen.getByRole('link', { name: '1' })
    expect(session1Link).toHaveAttribute('href', '/sessions/1')

    const session2Link = screen.getByRole('link', { name: '2' })
    expect(session2Link).toHaveAttribute('href', '/sessions/2')
  })

  it('should handle empty sessions array', () => {
    renderWithRouter(
      <StudySessionsTable
        sessions={[]}
        sortKey="id"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    // Table should still render with headers
    expect(screen.getByText('id')).toBeInTheDocument()
    expect(screen.getByText('activity name')).toBeInTheDocument()
    expect(screen.getByText('group name')).toBeInTheDocument()
  })

  it('should format header labels correctly', () => {
    renderWithRouter(
      <StudySessionsTable
        sessions={mockSessions}
        sortKey="id"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    expect(screen.getByText('id')).toBeInTheDocument()
    expect(screen.getByText('activity name')).toBeInTheDocument()
    expect(screen.getByText('group name')).toBeInTheDocument()
    expect(screen.getByText('start time')).toBeInTheDocument()
    expect(screen.getByText('end time')).toBeInTheDocument()
    expect(screen.getByText('# Review Items')).toBeInTheDocument()
  })

  it('should display timestamps correctly', () => {
    renderWithRouter(
      <StudySessionsTable
        sessions={mockSessions}
        sortKey="id"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    // Should display formatted timestamps
    expect(screen.getByText('2024-01-20T10:30:00Z')).toBeInTheDocument()
    expect(screen.getByText('2024-01-20T11:00:00Z')).toBeInTheDocument()
    expect(screen.getByText('2024-01-19T14:15:00Z')).toBeInTheDocument()
    expect(screen.getByText('2024-01-19T14:45:00Z')).toBeInTheDocument()
  })
})