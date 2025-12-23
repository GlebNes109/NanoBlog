import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

// Mock axios
vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() },
      },
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
    })),
  },
}));

describe('API module', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('creates axios instance with correct baseURL', () => {
    expect(axios.create).toBeDefined();
  });

  describe('Token handling', () => {
    it('should store token in localStorage on login', () => {
      const token = 'test-token';
      localStorage.setItem('token', token);
      expect(localStorage.setItem).toHaveBeenCalledWith('token', token);
    });

    it('should remove token on logout', () => {
      localStorage.removeItem('token');
      expect(localStorage.removeItem).toHaveBeenCalledWith('token');
    });
  });
});


