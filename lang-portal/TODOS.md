# German Learning Portal - TODOs

## 🚨 Critical Missing Implementations

### 1. Study Session Creation Endpoint
**File:** `backend-flask/routes/study_sessions.py:7`
```python
# todo /study_sessions POST
```
**Issue:** Frontend calls `createStudySession()` but backend endpoint doesn't exist
**Implementation needed:**
- Create `POST /study_sessions` or `POST /api/study-sessions` endpoint
- Accept `group_id` and `study_activity_id` parameters
- Create new study session record in database
- Return `{ session_id: number }`

### 2. Study Session Review Submission
**File:** `backend-flask/routes/study_sessions.py:156`
```python
# todo POST /study_sessions/:id/review
```
**Issue:** Frontend calls `submitStudySessionReview()` but backend endpoint doesn't exist
**Implementation needed:**
- Create `POST /study_sessions/{id}/review` endpoint
- Accept array of word reviews (word_id, correct/incorrect)
- Update `word_review_items` table
- Update `word_reviews` aggregate counts
- Return success confirmation

## 🔧 Missing Backend Routes

### 3. Raw Group Words Endpoint
**File:** `backend-flask/routes/groups.py:160`
```python
# todo GET /groups/:id/words/raw
```
**Implementation needed:**
- Create `GET /groups/{id}/words/raw` endpoint
- Return unformatted word data without pagination
- Useful for study activities that need all words at once

## 🧹 Code Cleanup Tasks

### 4. Remove Debug Logging
**File:** `frontend-react/src/services/api.ts:247`
```typescript
console.log('Raw response from recent session:', data);
```
**Task:** Remove or replace with proper logging mechanism

### 5. Fix Duplicate Interface Definitions
**File:** `frontend-react/src/services/api.ts`
**Issue:** `StudySessionsResponse` interface defined twice (lines 198 and 219) with different structures
**Task:** Consolidate into single interface or rename appropriately

## 🔄 API Consistency Issues

### 6. Standardize API URL Patterns
**Issue:** Inconsistent URL patterns across endpoints
- Some use `/api/` prefix: `/api/study-sessions`, `/api/study-activities`
- Others don't: `/groups`, `/words`, `/dashboard/stats`

**Recommendation:** Choose one pattern and apply consistently
- Option A: Add `/api/` prefix to all endpoints
- Option B: Remove `/api/` prefix from study-related endpoints

## 🛡️ Security and Validation

### 7. Input Validation
**Files:** Various backend routes
**Task:** Add proper input validation for:
- Request parameters (page numbers, sort fields)
- Request body data (study session creation, reviews)
- Database query parameters

### 8. Error Handling Enhancement
**Files:** All backend routes
**Task:** Improve error handling with:
- Specific error messages for different failure cases
- Proper HTTP status codes
- Consistent error response format

## 📊 Dashboard Enhancements

### 9. Dashboard Statistics Implementation
**File:** `backend-flask/routes/dashboard.py`
**Current status:** Basic implementation exists
**Potential improvements:**
- More detailed learning statistics
- Progress tracking over time
- Streak calculations
- Mastery level indicators

## 🇩🇪 German-Specific Features

### 10. Advanced German Grammar Support
**Priority:** Low (Future enhancement)
**Features to consider:**
- Verb conjugation tables
- Noun declension (Nominativ, Akkusativ, Dativ, Genitiv)
- Separable verb indicators
- Irregular verb patterns

### 11. Pronunciation Audio Support
**Priority:** Medium
**Implementation:**
- Add audio file paths to word schema
- Integrate text-to-speech API
- Audio playback controls in UI

## 🧪 Testing Requirements

### 12. Backend API Tests
**Status:** Test framework installed (pytest) but no tests written
**Needed:**
- Unit tests for all route handlers
- Integration tests for database operations
- Test data fixtures for German vocabulary

### 13. Frontend Component Tests
**Status:** No testing framework configured
**Needed:**
- Set up Jest/Vitest testing
- Component unit tests
- API integration tests

## 🚀 Deployment and Production

### 14. Production Configuration
**Tasks:**
- Environment variable configuration
- Production database setup
- CORS configuration for production domains
- Remove debug mode settings

### 15. Performance Optimization
**Areas to optimize:**
- Database query optimization
- Frontend bundle size
- Image and asset optimization
- Caching strategies

## 📱 Mobile and Accessibility

### 16. Mobile Responsiveness
**Status:** Basic responsive design implemented
**Improvements needed:**
- Touch-friendly study interfaces
- Mobile-optimized navigation
- Performance on mobile devices

### 17. Accessibility Enhancements
**Current:** Basic Radix UI accessibility
**Improvements:**
- Keyboard navigation for all features
- Screen reader optimization
- High contrast mode support
- Font size adjustability

## Priority Levels

🚨 **Critical (Blocks core functionality):**
- Items 1-2: Study session endpoints

🔧 **High (Important for stability):**
- Items 3-6: API consistency and cleanup

🛡️ **Medium (Quality improvements):**
- Items 7-11: Security, validation, features

🧪 **Low (Future enhancements):**
- Items 12-17: Testing, deployment, optimization

---

## Quick Implementation Order

1. **Implement study session creation endpoint**
2. **Implement study session review submission endpoint** 
3. **Standardize API URL patterns**
4. **Clean up debug logging and duplicate interfaces**
5. **Add input validation and error handling**
6. **Implement raw group words endpoint**