import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('should redirect to auth when accessing protected routes', async ({ page }) => {
    await page.goto('/profile');
    await expect(page).toHaveURL(/\/auth/);
  });

  test('should allow access to feed without auth', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: /лента постов/i })).toBeVisible();
  });

  test('should show search bar on feed page', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByPlaceholder(/поиск/i)).toBeVisible();
  });

  test('should navigate to search page', async ({ page }) => {
    await page.goto('/search');
    await expect(page.getByRole('heading', { name: /поиск/i })).toBeVisible();
  });
});


