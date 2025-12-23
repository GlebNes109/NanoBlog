import { describe, it, expect } from 'vitest';

// Validation functions
export function validateEmail(email) {
  if (!email) return 'Email обязателен';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Некорректный email';
  return null;
}

export function validateLogin(login) {
  if (!login) return 'Логин обязателен';
  if (login.length < 3) return 'Минимум 3 символа';
  return null;
}

export function validatePassword(password) {
  if (!password) return 'Пароль обязателен';
  if (password.length < 4) return 'Минимум 4 символа';
  return null;
}

export function validatePostTitle(title) {
  if (!title?.trim()) return 'Заголовок обязателен';
  if (title.length < 3) return 'Минимум 3 символа';
  if (title.length > 200) return 'Максимум 200 символов';
  return null;
}

export function validatePostContent(content) {
  if (!content?.trim()) return 'Содержимое обязательно';
  if (content.length < 10) return 'Минимум 10 символов';
  return null;
}

describe('Validation functions', () => {
  describe('validateEmail', () => {
    it('returns error for empty email', () => {
      expect(validateEmail('')).toBe('Email обязателен');
      expect(validateEmail(null)).toBe('Email обязателен');
      expect(validateEmail(undefined)).toBe('Email обязателен');
    });

    it('returns error for invalid email format', () => {
      expect(validateEmail('invalid')).toBe('Некорректный email');
      expect(validateEmail('invalid@')).toBe('Некорректный email');
      expect(validateEmail('@domain.com')).toBe('Некорректный email');
    });

    it('returns null for valid email', () => {
      expect(validateEmail('test@example.com')).toBeNull();
      expect(validateEmail('user.name@domain.org')).toBeNull();
    });
  });

  describe('validateLogin', () => {
    it('returns error for empty login', () => {
      expect(validateLogin('')).toBe('Логин обязателен');
    });

    it('returns error for short login', () => {
      expect(validateLogin('ab')).toBe('Минимум 3 символа');
    });

    it('returns null for valid login', () => {
      expect(validateLogin('abc')).toBeNull();
      expect(validateLogin('username')).toBeNull();
    });
  });

  describe('validatePassword', () => {
    it('returns error for empty password', () => {
      expect(validatePassword('')).toBe('Пароль обязателен');
    });

    it('returns error for short password', () => {
      expect(validatePassword('abc')).toBe('Минимум 4 символа');
    });

    it('returns null for valid password', () => {
      expect(validatePassword('abcd')).toBeNull();
      expect(validatePassword('password123')).toBeNull();
    });
  });

  describe('validatePostTitle', () => {
    it('returns error for empty title', () => {
      expect(validatePostTitle('')).toBe('Заголовок обязателен');
      expect(validatePostTitle('   ')).toBe('Заголовок обязателен');
    });

    it('returns error for short title', () => {
      expect(validatePostTitle('ab')).toBe('Минимум 3 символа');
    });

    it('returns error for long title', () => {
      expect(validatePostTitle('a'.repeat(201))).toBe('Максимум 200 символов');
    });

    it('returns null for valid title', () => {
      expect(validatePostTitle('Valid title')).toBeNull();
    });
  });

  describe('validatePostContent', () => {
    it('returns error for empty content', () => {
      expect(validatePostContent('')).toBe('Содержимое обязательно');
      expect(validatePostContent('   ')).toBe('Содержимое обязательно');
    });

    it('returns error for short content', () => {
      expect(validatePostContent('short')).toBe('Минимум 10 символов');
    });

    it('returns null for valid content', () => {
      expect(validatePostContent('This is valid content')).toBeNull();
    });
  });
});


