import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import WordsTable from './WordsTable'
import type { Word } from '../services/api'

const mockWords: Word[] = [
  {
    id: 1,
    german: 'Haus',
    pronunciation: '/haʊs/',
    english: 'house',
    gender: 'das',
    plural: 'Häuser',
    correct_count: 10,
    wrong_count: 2,
  },
  {
    id: 2,
    german: 'Baum',
    pronunciation: '/baʊm/',
    english: 'tree',
    gender: 'der',
    plural: 'Bäume',
    correct_count: 5,
    wrong_count: 1,
  },
]

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>)
}

describe('WordsTable', () => {
  it('should render words correctly', () => {
    renderWithRouter(
      <WordsTable
        words={mockWords}
        sortKey="german"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    // Check if words are displayed
    expect(screen.getByText('Haus')).toBeInTheDocument()
    expect(screen.getByText('Baum')).toBeInTheDocument()
    expect(screen.getByText('house')).toBeInTheDocument()
    expect(screen.getByText('tree')).toBeInTheDocument()
  })

  it('should display pronunciation and gender', () => {
    renderWithRouter(
      <WordsTable
        words={mockWords}
        sortKey="german"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    expect(screen.getByText('/haʊs/')).toBeInTheDocument()
    expect(screen.getByText('/baʊm/')).toBeInTheDocument()
    expect(screen.getByText('das')).toBeInTheDocument()
    expect(screen.getByText('der')).toBeInTheDocument()
  })

  it('should display correct and wrong counts', () => {
    renderWithRouter(
      <WordsTable
        words={mockWords}
        sortKey="german"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    expect(screen.getByText('10')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByText('5')).toBeInTheDocument()
    expect(screen.getByText('1')).toBeInTheDocument()
  })

  it('should show sort indicators', () => {
    const { rerender } = renderWithRouter(
      <WordsTable
        words={mockWords}
        sortKey="german"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    // Check for ascending sort indicator on german column
    const germanHeader = screen.getByText('German').closest('th')
    expect(germanHeader?.querySelector('svg')).toBeInTheDocument()

    // Rerender with descending sort
    rerender(
      <BrowserRouter>
        <WordsTable
          words={mockWords}
          sortKey="german"
          sortDirection="desc"
          onSort={vi.fn()}
        />
      </BrowserRouter>
    )

    // Sort indicator should still be present
    expect(germanHeader?.querySelector('svg')).toBeInTheDocument()
  })

  it('should call onSort when column header is clicked', () => {
    const onSort = vi.fn()
    renderWithRouter(
      <WordsTable
        words={mockWords}
        sortKey="german"
        sortDirection="asc"
        onSort={onSort}
      />
    )

    // Click on English column header
    fireEvent.click(screen.getByText('English'))
    expect(onSort).toHaveBeenCalledWith('english')

    // Click on Correct column header
    fireEvent.click(screen.getByText('Correct'))
    expect(onSort).toHaveBeenCalledWith('correct_count')
  })

  it('should render links to word details', () => {
    renderWithRouter(
      <WordsTable
        words={mockWords}
        sortKey="german"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    const hausLink = screen.getByRole('link', { name: 'Haus' })
    expect(hausLink).toHaveAttribute('href', '/words/1')

    const baumLink = screen.getByRole('link', { name: 'Baum' })
    expect(baumLink).toHaveAttribute('href', '/words/2')
  })

  it('should handle empty words array', () => {
    renderWithRouter(
      <WordsTable
        words={[]}
        sortKey="german"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    // Table should still render with headers
    expect(screen.getByText('German')).toBeInTheDocument()
    expect(screen.getByText('English')).toBeInTheDocument()
  })

  it('should display dash for missing gender and plural', () => {
    const wordsWithMissingData: Word[] = [
      {
        id: 3,
        german: 'laufen',
        pronunciation: '/ˈlaʊfən/',
        english: 'to run',
        correct_count: 0,
        wrong_count: 0,
      },
    ]

    renderWithRouter(
      <WordsTable
        words={wordsWithMissingData}
        sortKey="german"
        sortDirection="asc"
        onSort={vi.fn()}
      />
    )

    // Should show dashes for missing gender and plural
    const dashes = screen.getAllByText('-')
    expect(dashes).toHaveLength(2)
  })
})