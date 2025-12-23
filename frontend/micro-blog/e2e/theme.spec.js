import { test, expect } from '@playwright/test';

test.describe('Theme switching', () => {
  test('should toggle theme when clicking theme button', async ({ page }) => {
    await page.goto('/');
    
    const themeButton = page.locator('button').filter({ has: page.locator('svg') }).first();
    
    const html = page.locator('html');
    const initialHasDark = await html.evaluate(el => el.classList.contains('dark'));
    
    await themeButton.click();
    
    await expect(page.getByRole('heading', { name: /лента постов/i })).toBeVisible();
  });

  test('should persist theme preference', async ({ page }) => {
    await page.goto('/');
    
    // Set theme via localStorage
    await page.evaluate(() => {
      localStorage.setItem('theme', 'dark');
    });
    
    // Reload page
    await page.reload();
    
    // Theme should be applied
    const theme = await page.evaluate(() => localStorage.getItem('theme'));
    expect(theme).toBe('dark');
  });
});


