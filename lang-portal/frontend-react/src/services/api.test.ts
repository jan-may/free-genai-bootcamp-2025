import { describe, it, expect, vi, beforeEach } from 'vitest'
import {
  fetchGroups,
  fetchGroupDetails,
  fetchGroupWords,
  fetchWords,
  fetchWordDetails,
  createStudySession,
  submitStudySessionReview,
  fetchStudySessions,
  fetchGroupStudySessions,
  fetchRecentStudySession,
  fetchStudyStats,
} from './api'

// Mock fetch globally
global.fetch = vi.fn()

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('fetchGroups', () => {
    it('should fetch groups successfully', async () => {
      const mockResponse = {
        groups: [{ id: 1, group_name: 'Test Group', word_count: 10 }],
        total_pages: 1,
        current_page: 1,
      }
      
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response)

      const result = await fetchGroups(1, 'name', 'asc')
      
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/groups?page=1&sort_by=name&order=asc'
      )
      expect(result).toEqual(mockResponse)
    })

    it('should throw error when fetch fails', async () => {
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
      } as Response)

      await expect(fetchGroups()).rejects.toThrow('Failed to fetch groups')
    })
  })

  describe('fetchWords', () => {
    it('should fetch words with default parameters', async () => {
      const mockResponse = {
        words: [
          {
            id: 1,
            german: 'Haus',
            pronunciation: '/haʊs/',
            english: 'house',
            gender: 'das',
            plural: 'Häuser',
            correct_count: 5,
            wrong_count: 2,
          },
        ],
        total_pages: 1,
        current_page: 1,
        total_words: 1,
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response)

      const result = await fetchWords()
      
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/words?page=1&sort_by=german&order=asc'
      )
      expect(result).toEqual(mockResponse)
    })

    it('should fetch words with custom parameters', async () => {
      const mockResponse = {
        words: [],
        total_pages: 0,
        current_page: 2,
        total_words: 0,
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response)

      const result = await fetchWords(2, 'english', 'desc')
      
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/words?page=2&sort_by=english&order=desc'
      )
      expect(result).toEqual(mockResponse)
    })
  })

  describe('fetchWordDetails', () => {
    it('should fetch word details', async () => {
      const mockWord = {
        id: 1,
        german: 'Haus',
        pronunciation: '/haʊs/',
        english: 'house',
        gender: 'das',
        plural: 'Häuser',
        correct_count: 5,
        wrong_count: 2,
        groups: [{ id: 1, name: 'Nouns' }],
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({ word: mockWord }),
      } as Response)

      const result = await fetchWordDetails(1)
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:5000/api/words/1')
      expect(result).toEqual(mockWord)
    })
  })

  describe('createStudySession', () => {
    it('should create a study session', async () => {
      const mockResponse = { session_id: 123 }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response)

      const result = await createStudySession(1, 2)
      
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/study_sessions',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            group_id: 1,
            study_activity_id: 2,
          }),
        }
      )
      expect(result).toEqual(mockResponse)
    })

    it('should throw error when creation fails', async () => {
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
      } as Response)

      await expect(createStudySession(1, 2)).rejects.toThrow('Failed to create study session')
    })
  })

  describe('submitStudySessionReview', () => {
    it('should submit review successfully', async () => {
      const reviews = [
        { word_id: 1, is_correct: true },
        { word_id: 2, is_correct: false },
      ]

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({}),
      } as Response)

      await submitStudySessionReview(123, reviews)
      
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/study_sessions/123/review',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ reviews }),
        }
      )
    })
  })

  describe('fetchStudyStats', () => {
    it('should fetch study statistics', async () => {
      const mockStats = {
        total_vocabulary: 100,
        total_words_studied: 50,
        mastered_words: 20,
        success_rate: 75,
        total_sessions: 10,
        active_groups: 3,
        current_streak: 5,
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockStats,
      } as Response)

      const result = await fetchStudyStats()
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:5000/api/dashboard/stats')
      expect(result).toEqual(mockStats)
    })
  })

  describe('fetchGroupDetails', () => {
    it('should fetch group details', async () => {
      const mockGroup = {
        id: 1,
        group_name: 'Nouns',
        word_count: 50,
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockGroup,
      } as Response)

      const result = await fetchGroupDetails(1)
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:5000/api/groups/1')
      expect(result).toEqual(mockGroup)
    })
  })

  describe('fetchGroupWords', () => {
    it('should fetch words for a group', async () => {
      const mockResponse = {
        words: [
          {
            id: 1,
            german: 'Haus',
            pronunciation: '/haʊs/',
            english: 'house',
            gender: 'das',
            plural: 'Häuser',
            correct_count: 0,
            wrong_count: 0,
          },
        ],
        total_pages: 1,
        current_page: 1,
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response)

      const result = await fetchGroupWords(1, 2, 'pronunciation', 'desc')
      
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/groups/1/words?page=2&sort_by=pronunciation&order=desc'
      )
      expect(result).toEqual(mockResponse)
    })
  })

  describe('fetchRecentStudySession', () => {
    it('should fetch recent study session', async () => {
      const mockSession = {
        id: 1,
        group_id: 1,
        activity_name: 'Flashcards',
        created_at: '2024-01-01T10:00:00Z',
        correct_count: 8,
        wrong_count: 2,
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockSession,
      } as Response)

      const result = await fetchRecentStudySession()
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:5000/api/dashboard/recent-session')
      expect(result).toEqual(mockSession)
    })

    it('should handle null response', async () => {
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => null,
      } as Response)

      const result = await fetchRecentStudySession()
      expect(result).toBeNull()
    })
  })
})