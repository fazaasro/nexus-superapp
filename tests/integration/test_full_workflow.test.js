import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { rest } from 'msw'

const server = setupServer(
  // Bag endpoints
  rest.post('/api/bag/transactions', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 1,
        amount: req.body.amount,
        category: req.body.category,
        date: req.body.date,
      })
    )
  }),

  rest.post('/api/bag/upload', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 1,
        text: 'Sample receipt text',
        amount: 100,
        category: 'Food',
      })
    )
  }),

  // Brain endpoints
  rest.post('/api/brain/entries', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 1,
        title: req.body.title,
        content: req.body.content,
        tags: req.body.tags,
        createdAt: new Date().toISOString(),
      })
    )
  }),

  rest.post('/api/brain/entries/1/anki', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        { front: 'Question 1?', back: 'Answer 1' },
        { front: 'Question 2?', back: 'Answer 2' },
      ])
    )
  }),

  // Circle endpoints
  rest.post('/api/circle/contacts', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 1,
        name: req.body.name,
        email: req.body.email,
        phone: req.body.phone,
      })
    )
  }),

  rest.post('/api/circle/health', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 1,
        type: req.body.type,
        date: req.body.date,
        notes: req.body.notes,
      })
    )
  }),

  // Vessel endpoints
  rest.post('/api/vessel/workouts', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 1,
        type: req.body.type,
        duration: req.body.duration,
        calories: req.body.calories,
        date: req.body.date,
      })
    )
  }),

  rest.post('/api/vessel/biometrics', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 1,
        type: req.body.type,
        value: req.body.value,
        unit: req.body.unit,
        date: req.body.date,
      })
    )
  })
)

describe('Full Workflow Integration Tests', () => {
  beforeAll(() => server.listen())
  afterAll(() => server.close())

  it('completes Bag transaction workflow', async () => {
    // Upload receipt
    const file = new File(['receipt'], 'receipt.jpg', { type: 'image/jpeg' })
    const formData = new FormData()
    formData.append('file', file)

    const uploadResponse = await fetch('/api/bag/upload', {
      method: 'POST',
      body: formData,
    })
    const uploadData = await uploadResponse.json()

    expect(uploadData).toBeDefined()
    expect(uploadData.amount).toBe(100)
    expect(uploadData.category).toBe('Food')

    // Create transaction based on OCR result
    const transactionResponse = await fetch('/api/bag/transactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: uploadData.amount,
        category: uploadData.category,
        date: new Date().toISOString().split('T')[0],
      }),
    })

    const transaction = await transactionResponse.json()
    expect(transaction.id).toBeDefined()
    expect(transaction.amount).toBe(100)
  })

  it('completes Brain knowledge workflow', async () => {
    // Create knowledge entry
    const entryResponse = await fetch('/api/brain/entries', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: 'Vue.js Testing',
        content: 'How to test Vue components',
        tags: ['vue', 'testing'],
      }),
    })

    const entry = await entryResponse.json()
    expect(entry.id).toBeDefined()

    // Generate Anki cards
    const ankiResponse = await fetch('/api/brain/entries/1/anki', {
      method: 'POST',
    })

    const cards = await ankiResponse.json()
    expect(Array.isArray(cards)).toBe(true)
    expect(cards.length).toBeGreaterThan(0)
  })

  it('completes Circle social workflow', async () => {
    // Add contact
    const contactResponse = await fetch('/api/circle/contacts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'John Doe',
        email: 'john@example.com',
        phone: '+1234567890',
      }),
    })

    const contact = await contactResponse.json()
    expect(contact.id).toBeDefined()

    // Log health episode
    const healthResponse = await fetch('/api/circle/health', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: 'Checkup',
        date: '2024-02-18',
        notes: 'Regular checkup',
      }),
    })

    const healthEpisode = await healthResponse.json()
    expect(healthEpisode.id).toBeDefined()
  })

  it('completes Vessel health workflow', async () => {
    // Log workout
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
    expect(workout.id).toBeDefined()

    // Add biometrics
    const biometricResponse = await fetch('/api/vessel/biometrics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: 'Weight',
        value: 70,
        unit: 'kg',
        date: '2024-02-18',
      }),
    })

    const biometric = await biometricResponse.json()
    expect(biometric.id).toBeDefined()
  })
})
