import { test, expect } from '@playwright/test';

test.describe('Search', () => {
  test.beforeEach(async ({ page }) => {
    // Mock API responses
    await page.route('**/auth/token', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ access_token: 'mock-token', token_type: 'bearer' })
      });
    });

    await page.route('**/users/me', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: '1',
          email: 'test@example.com',
          login: 'testuser',
          createdAt: '2024-01-01T00:00:00Z',
          updatedAt: '2024-01-01T00:00:00Z'
        })
      });
    });

    // Login
    await page.goto('/auth');
    await page.getByPlaceholder('username').fill('testuser');
    await page.getByPlaceholder('••••••••').fill('password');
    await page.getByRole('button', { name: /войти/i }).click();
    await page.waitForURL('/');
  });

  test('should search posts', async ({ page }) => {
    await page.route('**/search/posts?query=test', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: '1',
            authorId: '1',
            authorLogin: 'testuser',
            title: 'Test Post',
            content: 'Test content',
            rating: 0,
            user_rating: null,
            is_favorited: false,
            comments_count: 0,
            createdAt: '2024-01-01T00:00:00Z',
            updatedAt: '2024-01-01T00:00:00Z'
          }
        ])
      });
    });

    await page.goto('/search');
    
    const searchInput = page.getByPlaceholder(/поиск/i);
    await searchInput.fill('test');
    await searchInput.press('Enter');
    
    await expect(page.getByText('Test Post')).toBeVisible();
  });

  test('should search users', async ({ page }) => {
    await page.route('**/search/users?query=test', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: '2',
            email: 'other@example.com',
            login: 'otheruser',
            createdAt: '2024-01-01T00:00:00Z',
            updatedAt: '2024-01-01T00:00:00Z'
          }
        ])
      });
    });

    await page.goto('/search');
    
    // Switch to users tab
    await page.getByRole('button', { name: /пользователи/i }).click();
    
    const searchInput = page.getByPlaceholder(/поиск/i);
    await searchInput.fill('test');
    await searchInput.press('Enter');
    
    await expect(page.getByText('otheruser')).toBeVisible();
  });
});

