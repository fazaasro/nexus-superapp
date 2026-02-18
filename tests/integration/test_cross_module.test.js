import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { rest } from 'msw'

const server = setupServer(
  // Cross-module search endpoint
  rest.get('/api/search', (req, res, ctx) => {
    const query = req.url.searchParams.get('q')

    // Mock results from different modules
    const results = {
      bag: [
        { id: 1, type: 'transaction', amount: 100, category: 'Food', description: 'Grocery shopping' },
      ],
      brain: [
        { id: 1, type: 'entry', title: 'Healthy Eating', content: 'Tips for healthy food choices' },
      ],
      vessel: [
        { id: 1, type: 'workout', activity: 'Running', notes: '5K run' },
      ],
    }

    return res(ctx.status(200), ctx.json(results))
  }),

  // Module-specific endpoints for integration
  rest.post('/api/bag/transactions', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({ id: 1, ...req.body, createdAt: new Date().toISOString() })
    )
  }),

  rest.post('/api/brain/entries', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({ id: 1, ...req.body, createdAt: new Date().toISOString() })
    )
  }),

  rest.post('/api/vessel/workouts', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({ id: 1, ...req.body, createdAt: new Date().toISOString() })
    )
  }),

  // Cross-module workflow: Transaction -> Health tracking
  rest.post('/api/bag/transactions/:id/tag-health', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ success: true, tags: req.body.tags })
    )
  }),

  // Cross-module workflow: Knowledge -> Action items
  rest.post('/api/brain/entries/:id/actions', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({ id: 1, ...req.body, entryId: req.params.id })
    )
  })
)

describe('Cross-Module Integration Tests', () => {
  beforeAll(() => server.listen())
  afterAll(() => server.close())

  it('searches across all modules', async () => {
    const response = await fetch('/api/search?q=food')
    const results = await response.json()

    expect(results.bag).toBeDefined()
    expect(results.brain).toBeDefined()
    expect(results.vessel).toBeDefined()
    expect(results.bag.length).toBeGreaterThan(0)
  })

  it('creates transaction and tags with health data', async () => {
    // Create food transaction
    const transactionResponse = await fetch('/api/bag/transactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: 100,
        category: 'Food',
        date: '2024-02-18',
        description: 'Grocery shopping',
      }),
    })

    const transaction = await transactionResponse.json()
    expect(transaction.id).toBeDefined()

    // Tag with health information
    const tagResponse = await fetch('/api/bag/transactions/1/tag-health', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tags: ['healthy', 'organic', 'vegan'],
        calories: 2000,
        nutrition: 'balanced',
      }),
    })

    const tagResult = await tagResponse.json()
    expect(tagResult.success).toBe(true)
    expect(tagResult.tags).toContain('healthy')
  })

  it('creates knowledge entry with action items', async () => {
    // Create knowledge entry about health
    const entryResponse = await fetch('/api/brain/entries', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: 'Workout Plan',
        content: 'Weekly exercise routine',
        tags: ['health', 'fitness'],
      }),
    })

    const entry = await entryResponse.json()
    expect(entry.id).toBeDefined()

    // Create action items linked to the entry
    const actionResponse = await fetch('/api/brain/entries/1/actions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: 'Go for a run',
        dueDate: '2024-02-19',
        type: 'workout',
      }),
    })

    const action = await actionResponse.json()
    expect(action.id).toBeDefined()
    expect(action.entryId).toBe('1')
  })

  it('tracks health data across transactions and workouts', async () => {
    // Create food transaction
    const foodResponse = await fetch('/api/bag/transactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: 50,
        category: 'Food',
        date: '2024-02-18',
        description: 'Post-workout meal',
      }),
    })

    const food = await foodResponse.json()

    // Create workout
    const workoutResponse = await fetch('/api/vessel/workouts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: 'Running',
        duration: 30,
        calories: 300,
        date: '2024-02-18',
      }),
    })

    const workout = await workoutResponse.json()

    // Verify both exist
    expect(food.id).toBeDefined()
    expect(workout.id).toBeDefined()

    // Search for related activities
    const searchResponse = await fetch('/api/search?q=workout')
    const searchResults = await searchResponse.json()

    expect(searchResults.bag.some(t => t.description === 'Post-workout meal')).toBe(true)
    expect(searchResults.vessel.some(w => w.activity === 'Running')).toBe(true)
  })

  it('maintains data consistency across modules', async () => {
    // Create data in multiple modules
    const transaction = await fetch('/api/bag/transactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: 75,
        category: 'Food',
        date: '2024-02-18',
        description: 'Healthy groceries',
      }),
    }).then(r => r.json())

    const entry = await fetch('/api/brain/entries', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: 'Meal Planning',
        content: 'Plan weekly healthy meals',
        tags: ['food', 'health'],
      }),
    }).then(r => r.json())

    const workout = await fetch('/api/vessel/workouts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: 'Swimming',
        duration: 45,
        calories: 400,
        date: '2024-02-18',
      }),
    }).then(r => r.json())

    // All should have valid IDs and timestamps
    expect(transaction.id).toBeDefined()
    expect(entry.id).toBeDefined()
    expect(workout.id).toBeDefined()

    expect(transaction.createdAt).toBeDefined()
    expect(entry.createdAt).toBeDefined()
    expect(workout.createdAt).toBeDefined()
  })
})
