import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import Pagination from './Pagination'

describe('Pagination', () => {
  it('should render current page and total pages', () => {
    render(
      <Pagination
        currentPage={3}
        totalPages={10}
        onPageChange={vi.fn()}
      />
    )

    expect(screen.getByText('Page 3 of 10')).toBeInTheDocument()
  })

  it('should call onPageChange when Previous is clicked', () => {
    const onPageChange = vi.fn()
    render(
      <Pagination
        currentPage={3}
        totalPages={10}
        onPageChange={onPageChange}
      />
    )

    fireEvent.click(screen.getByText('Previous'))
    expect(onPageChange).toHaveBeenCalledWith(2)
  })

  it('should call onPageChange when Next is clicked', () => {
    const onPageChange = vi.fn()
    render(
      <Pagination
        currentPage={3}
        totalPages={10}
        onPageChange={onPageChange}
      />
    )

    fireEvent.click(screen.getByText('Next'))
    expect(onPageChange).toHaveBeenCalledWith(4)
  })

  it('should disable Previous button on first page', () => {
    render(
      <Pagination
        currentPage={1}
        totalPages={10}
        onPageChange={vi.fn()}
      />
    )

    const previousButton = screen.getByText('Previous')
    expect(previousButton).toBeDisabled()
  })

  it('should disable Next button on last page', () => {
    render(
      <Pagination
        currentPage={10}
        totalPages={10}
        onPageChange={vi.fn()}
      />
    )

    const nextButton = screen.getByText('Next')
    expect(nextButton).toBeDisabled()
  })

  it('should not call onPageChange when disabled buttons are clicked', () => {
    const onPageChange = vi.fn()
    
    // Test first page
    const { rerender } = render(
      <Pagination
        currentPage={1}
        totalPages={10}
        onPageChange={onPageChange}
      />
    )

    fireEvent.click(screen.getByText('Previous'))
    expect(onPageChange).not.toHaveBeenCalled()

    // Test last page
    rerender(
      <Pagination
        currentPage={10}
        totalPages={10}
        onPageChange={onPageChange}
      />
    )

    fireEvent.click(screen.getByText('Next'))
    expect(onPageChange).not.toHaveBeenCalled()
  })

  it('should not render when there is only one page', () => {
    const { container } = render(
      <Pagination
        currentPage={1}
        totalPages={1}
        onPageChange={vi.fn()}
      />
    )

    // Should render nothing (null) when totalPages <= 1
    expect(container.firstChild).toBeNull()
  })
})