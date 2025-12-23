import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Layout from '../../components/Layout';

const mockUseAuth = vi.fn();
const mockUseTheme = vi.fn();

vi.mock('../../context/AuthContext', () => ({
  useAuth: () => mockUseAuth(),
  AuthProvider: ({ children }) => children,
}));

vi.mock('../../context/ThemeContext', () => ({
  useTheme: () => mockUseTheme(),
  ThemeProvider: ({ children }) => children,
}));

const renderWithProviders = (component, user = null) => {
  mockUseAuth.mockReturnValue({ 
    user, 
    loading: false, 
    login: vi.fn(), 
    logout: vi.fn(), 
    updateUser: vi.fn() 
  });
  mockUseTheme.mockReturnValue({ theme: 'light', setTheme: vi.fn() });
  
  return render(
    <BrowserRouter>
      <Layout>{component}</Layout>
    </BrowserRouter>
  );
};

describe('Layout', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders navigation links for authenticated user', () => {
    const user = { id: '1', login: 'testuser' };
    renderWithProviders(<div>Test content</div>, user);
    
    expect(screen.getByText('Лента')).toBeInTheDocument();
    expect(screen.getByText('Написать')).toBeInTheDocument();
  });
  
  it('renders login link for unauthenticated user', () => {
    renderWithProviders(<div>Test content</div>, null);
    
    expect(screen.getByText('Войти')).toBeInTheDocument();
    expect(screen.queryByText('Лента')).not.toBeInTheDocument();
  });

  it('renders children content', () => {
    renderWithProviders(<div>Test content</div>);
    
    expect(screen.getByText('Test content')).toBeInTheDocument();
  });
});

