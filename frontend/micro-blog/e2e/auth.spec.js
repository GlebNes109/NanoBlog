import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should display login form by default', async ({ page }) => {
    await page.goto('/auth');
    
    await expect(page.getByRole('heading', { name: /microblog/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /вход/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /регистрация/i })).toBeVisible();
    await expect(page.getByPlaceholder('username')).toBeVisible();
    await expect(page.getByPlaceholder('••••••••')).toBeVisible();
  });

  test('should switch between login and registration forms', async ({ page }) => {
    await page.goto('/auth');
    
    // Initially on login form - no email field
    await expect(page.getByPlaceholder('your@email.com')).not.toBeVisible();
    
    // Click registration tab
    await page.getByRole('button', { name: /регистрация/i }).click();
    
    // Now email field should be visible
    await expect(page.getByPlaceholder('your@email.com')).toBeVisible();
    
    // Switch back to login
    await page.getByRole('button', { name: /вход/i }).click();
    await expect(page.getByPlaceholder('your@email.com')).not.toBeVisible();
  });

  test('should show validation errors on empty submit', async ({ page }) => {
    await page.goto('/auth');
    
    // Click submit without filling form
    await page.getByRole('button', { name: /войти/i }).click();
    
    // Should show validation errors
    await expect(page.getByText(/логин обязателен/i)).toBeVisible();
    await expect(page.getByText(/пароль обязателен/i)).toBeVisible();
  });

  test('should show validation error for short login', async ({ page }) => {
    await page.goto('/auth');
    
    await page.getByPlaceholder('username').fill('ab');
    await page.getByPlaceholder('••••••••').fill('password');
    await page.getByRole('button', { name: /войти/i }).click();
    
    await expect(page.getByText(/минимум 3 символа/i)).toBeVisible();
  });

  test('should validate email format on registration', async ({ page }) => {
    await page.goto('/auth');
    
    // Switch to registration
    await page.getByRole('button', { name: /регистрация/i }).click();
    
    await page.getByPlaceholder('your@email.com').fill('invalid-email');
    await page.getByPlaceholder('username').fill('testuser');
    await page.getByPlaceholder('••••••••').fill('password');
    await page.getByRole('button', { name: /зарегистрироваться/i }).click();
    
    await expect(page.getByText(/некорректный email/i)).toBeVisible();
  });
});


