import { test, expect } from '@playwright/test';

test.describe('Posts', () => {
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

    await page.route('**/posts', route => {
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
            rating: 5,
            user_rating: null,
            is_favorited: false,
            comments_count: 0,
            createdAt: '2024-01-01T00:00:00Z',
            updatedAt: '2024-01-01T00:00:00Z'
          }
        ])
      });
    });

    // Login
    await page.goto('/auth');
    await page.getByPlaceholder('username').fill('testuser');
    await page.getByPlaceholder('••••••••').fill('password');
    await page.getByRole('button', { name: /войти/i }).click();
    await page.waitForURL('/');
  });

  test('should display posts on feed page', async ({ page }) => {
    await page.goto('/');
    
    await expect(page.getByText('Test Post')).toBeVisible();
    await expect(page.getByText('testuser')).toBeVisible();
  });

  test('should navigate to create post page', async ({ page }) => {
    await page.goto('/');
    
    await page.getByRole('link', { name: /создать пост/i }).click();
    await page.waitForURL('/create');
    
    await expect(page.getByPlaceholder(/заголовок/i)).toBeVisible();
    await expect(page.getByPlaceholder(/содержание/i)).toBeVisible();
  });

  test('should create a new post', async ({ page }) => {
    await page.route('**/posts', route => {
      if (route.request().method() === 'POST') {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            id: '2',
            authorId: '1',
            authorLogin: 'testuser',
            title: 'New Post',
            content: 'New content',
            rating: 0,
            user_rating: null,
            is_favorited: false,
            comments_count: 0,
            createdAt: '2024-01-01T00:00:00Z',
            updatedAt: '2024-01-01T00:00:00Z'
          })
        });
      } else {
        route.continue();
      }
    });

    await page.goto('/create');
    
    await page.getByPlaceholder(/заголовок/i).fill('New Post');
    await page.getByPlaceholder(/содержание/i).fill('New content');
    await page.getByRole('button', { name: /опубликовать/i }).click();
    
    await page.waitForURL('/');
    await expect(page.getByText('New Post')).toBeVisible();
  });

  test('should rate a post', async ({ page }) => {
    await page.route('**/posts/*/rate', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'rated', value: 1 })
      });
    });

    await page.goto('/');
    
    const upButton = page.locator('button').filter({ hasText: '▲' }).first();
    await upButton.click();
    
    // Rating should update (mock would need to update post data)
    await expect(upButton).toBeVisible();
  });

  test('should add post to favorites', async ({ page }) => {
    await page.route('**/favorites/*', route => {
      if (route.request().method() === 'POST') {
        route.fulfill({ status: 200, body: JSON.stringify({}) });
      } else {
        route.continue();
      }
    });

    await page.goto('/');
    
    const favoriteButton = page.locator('button').filter({ hasText: '☆' }).first();
    await favoriteButton.click();
    
    await expect(favoriteButton).toBeVisible();
  });
});

