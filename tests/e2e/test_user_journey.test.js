import { test, expect } from '@playwright/test'

test.describe('User Journey E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173')
  })

  test('complete Bag workflow: add transaction and view balance', async ({ page }) => {
    // Navigate to Bag module
    await page.click('text=Bag')

    // Wait for page to load
    await page.waitForSelector('.transactions-list')

    // Add new transaction
    await page.click('button:has-text("Add Transaction")')
    await page.fill('input[name="amount"]', '100')
    await page.selectOption('select[name="category"]', 'Food')
    await page.fill('input[name="date"]', '2024-02-18')
    await page.click('button:has-text("Save")')

    // Verify transaction appears in list
    await expect(page.locator('.transaction-card').first()).toContainText('Food')
    await expect(page.locator('.transaction-card').first()).toContainText('100')

    // Check total balance updates
    await expect(page.locator('.total-balance')).toBeVisible()
  })

  test('upload receipt and view OCR results', async ({ page }) => {
    await page.click('text=Bag')
    await page.waitForSelector('.transactions-list')

    // Click upload receipt button
    await page.click('button:has-text("Upload Receipt")')

    // Upload file (use test file)
    const fileInput = page.locator('input[type="file"]')
    await fileInput.setInputFiles('tests/fixtures/receipt.jpg')

    // Wait for OCR to complete
    await page.waitForSelector('.ocr-results', { timeout: 10000 })

    // Verify OCR results are displayed
    await expect(page.locator('.ocr-results')).toBeVisible()
    await expect(page.locator('.extracted-amount')).toBeVisible()
  })

  test('complete Brain workflow: create knowledge entry', async ({ page }) => {
    await page.click('text=Brain')
    await page.waitForSelector('.entries-list')

    // Click create new entry
    await page.click('button:has-text("New Entry")')

    // Fill in entry details
    await page.fill('input[name="title"]', 'Vue.js Testing')
    await page.fill('textarea[name="content"]', 'How to test Vue components with Vitest')
    await page.fill('input[name="tags"]', 'vue,testing,javascript')

    // Save entry
    await page.click('button:has-text("Save")')

    // Verify entry appears in list
    await expect(page.locator('.entry-card').first()).toContainText('Vue.js Testing')
  })

  test('generate Anki cards from knowledge entry', async ({ page }) => {
    await page.click('text=Brain')
    await page.waitForSelector('.entries-list')

    // Create entry first
    await page.click('button:has-text("New Entry")')
    await page.fill('input[name="title"]', 'JavaScript Basics')
    await page.fill('textarea[name="content"]', 'Key concepts: let, const, arrow functions')
    await page.fill('input[name="tags"]', 'javascript,programming')
    await page.click('button:has-text("Save")')

    // Generate Anki cards
    await page.click('.entry-card .generate-anki-button')

    // Wait for cards to generate
    await page.waitForSelector('.anki-cards-preview', { timeout: 10000 })

    // Verify cards are displayed
    await expect(page.locator('.anki-card').first()).toBeVisible()
  })

  test('complete Circle workflow: add contact', async ({ page }) => {
    await page.click('text=Circle')
    await page.waitForSelector('.contacts-list')

    // Add new contact
    await page.click('button:has-text("Add Contact")')

    await page.fill('input[name="name"]', 'John Doe')
    await page.fill('input[name="email"]', 'john@example.com')
    await page.fill('input[name="phone"]', '+1234567890')
    await page.click('button:has-text("Save")')

    // Verify contact appears
    await expect(page.locator('.contact-card').first()).toContainText('John Doe')
  })

  test('log health episode in Circle module', async ({ page }) => {
    await page.click('text=Circle')
    await page.waitForSelector('.health-section')

    // Click log health episode
    await page.click('button:has-text("Log Health Episode")')

    await page.selectOption('select[name="type"]', 'Checkup')
    await page.fill('input[name="date"]', '2024-02-18')
    await page.fill('textarea[name="notes"]', 'Regular annual checkup')
    await page.click('button:has-text("Save")')

    // Verify episode appears in list
    await expect(page.locator('.health-episode-card').first()).toContainText('Checkup')
  })

  test('update mood in Circle module', async ({ page }) => {
    await page.click('text=Circle')
    await page.waitForSelector('.mood-tracker')

    // Click on a mood
    await page.click('.mood-option[data-mood="happy"]')

    // Verify mood is updated
    await expect(page.locator('.current-mood')).toContainText('happy')
  })

  test('complete Vessel workflow: log workout', async ({ page }) => {
    await page.click('text=Vessel')
    await page.waitForSelector('.workouts-list')

    // Log workout
    await page.click('button:has-text("Log Workout")')

    await page.selectOption('select[name="type"]', 'Running')
    await page.fill('input[name="duration"]', '30')
    await page.fill('input[name="calories"]', '300')
    await page.fill('input[name="date"]', '2024-02-18')
    await page.click('button:has-text("Save")')

    // Verify workout appears
    await expect(page.locator('.workout-card').first()).toContainText('Running')
  })

  test('add biometrics in Vessel module', async ({ page }) => {
    await page.click('text=Vessel')
    await page.waitForSelector('.biometrics-section')

    // Add biometric
    await page.click('button:has-text("Add Biometric")')

    await page.selectOption('select[name="type"]', 'Weight')
    await page.fill('input[name="value"]', '70')
    await page.selectOption('select[name="unit"]', 'kg')
    await page.fill('input[name="date"]', '2024-02-18')
    await page.click('button:has-text("Save")')

    // Verify biometric appears
    await expect(page.locator('.biometric-card').first()).toContainText('Weight')
  })

  test('dark mode toggle persists across pages', async ({ page }) => {
    // Check initial state
    const isDarkMode = await page.locator('body').getAttribute('class')
    expect(isDarkMode).not.toContain('dark')

    // Toggle dark mode
    await page.click('.dark-mode-toggle')

    // Verify dark mode is active
    const darkModeActive = await page.locator('body').getAttribute('class')
    expect(darkModeActive).toContain('dark')

    // Navigate to different module
    await page.click('text=Bag')

    // Verify dark mode persists
    const darkModePersisted = await page.locator('body').getAttribute('class')
    expect(darkModePersisted).toContain('dark')

    // Navigate to home
    await page.click('text=Home')

    // Verify dark mode still active
    const darkModeHome = await page.locator('body').getAttribute('class')
    expect(darkModeHome).toContain('dark')
  })

  test('responsive layout on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })

    // Check navigation adapts
    await expect(page.locator('.mobile-nav')).toBeVisible()

    // Navigate to module
    await page.click('.mobile-nav button:has-text("Bag")')

    // Verify content is mobile-friendly
    await expect(page.locator('.mobile-transaction-card').first()).toBeVisible()
  })

  test('search across modules', async ({ page }) => {
    // Click search button
    await page.click('.search-toggle')

    // Enter search query
    await page.fill('.search-input', 'food')

    // Wait for results
    await page.waitForSelector('.search-results')

    // Verify results from different modules
    await expect(page.locator('.search-results')).toContainText('Bag')
  })
})
