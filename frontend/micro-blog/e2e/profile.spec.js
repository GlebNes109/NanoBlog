import { test, expect } from '@playwright/test';

test.describe('Profile', () => {
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
          bio: 'Test bio',
          avatar_url: null,
          createdAt: '2024-01-01T00:00:00Z',
          updatedAt: '2024-01-01T00:00:00Z'
        })
      });
    });

    await page.route('**/users/1/posts', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([])
      });
    });

    // Login
    await page.goto('/auth');
    await page.getByPlaceholder('username').fill('testuser');
    await page.getByPlaceholder('••••••••').fill('password');
    await page.getByRole('button', { name: /войти/i }).click();
    await page.waitForURL('/');
  });

  test('should display profile page', async ({ page }) => {
    await page.goto('/profile');
    
    await expect(page.getByText('testuser')).toBeVisible();
    await expect(page.getByText('test@example.com')).toBeVisible();
  });

  test('should edit profile', async ({ page }) => {
    await page.route('**/users/me', route => {
      if (route.request().method() === 'PUT') {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            id: '1',
            email: 'test@example.com',
            login: 'updateduser',
            bio: 'Updated bio',
            avatar_url: null,
            createdAt: '2024-01-01T00:00:00Z',
            updatedAt: '2024-01-01T00:00:00Z'
          })
        });
      } else {
        route.continue();
      }
    });

    await page.goto('/profile');
    
    await page.getByRole('button', { name: /редактировать/i }).click();
    
    const bioField = page.getByPlaceholder(/биография/i);
    await bioField.clear();
    await bioField.fill('Updated bio');
    
    await page.getByRole('button', { name: /сохранить/i }).click();
    
    await expect(page.getByText('Updated bio')).toBeVisible();
  });

  test('should display user posts', async ({ page }) => {
    await page.route('**/users/1/posts', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: '1',
            authorId: '1',
            authorLogin: 'testuser',
            title: 'My Post',
            content: 'Content',
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

    await page.goto('/profile');
    
    await expect(page.getByText('My Post')).toBeVisible();
  });
});

