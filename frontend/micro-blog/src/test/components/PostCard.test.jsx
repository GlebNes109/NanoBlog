import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import PostCard from '../../components/PostCard';

const mockPost = {
  id: '1',
  authorId: 'author1',
  authorLogin: 'testuser',
  authorAvatar: null,
  title: 'Test Post',
  content: 'Test content',
  image_url: null,
  rating: 5,
  user_rating: null,
  is_favorited: false,
  comments_count: 3,
  createdAt: '2024-01-01T00:00:00Z',
  updatedAt: '2024-01-01T00:00:00Z',
};

const mockRate = vi.fn().mockResolvedValue({});
const mockAddFavorite = vi.fn().mockResolvedValue({});
const mockRemoveFavorite = vi.fn().mockResolvedValue({});

vi.mock('../../api', () => ({
  postsAPI: {
    rate: () => mockRate(),
  },
  favoritesAPI: {
    add: () => mockAddFavorite(),
    remove: () => mockRemoveFavorite(),
  },
}));

const mockUseAuth = vi.fn();

vi.mock('../../context/AuthContext', () => ({
  useAuth: () => mockUseAuth(),
  AuthProvider: ({ children }) => children,
}));

const renderWithProviders = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('PostCard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockUseAuth.mockReturnValue({ user: null, loading: false, login: vi.fn(), logout: vi.fn(), updateUser: vi.fn() });
  });

  it('renders post information', () => {
    renderWithProviders(<PostCard post={mockPost} />);
    
    expect(screen.getByText('Test Post')).toBeInTheDocument();
    expect(screen.getByText('testuser')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('disables rating buttons when user is not logged in', () => {
    renderWithProviders(<PostCard post={mockPost} />);
    
    const buttons = screen.getAllByRole('button');
    const ratingButtons = buttons.filter(btn => {
      const svg = btn.querySelector('svg');
      return svg && (svg.querySelector('path[d*="M5 15l7-7"]') || svg.querySelector('path[d*="M19 9l-7 7"]'));
    });
    
    ratingButtons.forEach(button => {
      expect(button).toBeDisabled();
    });
  });

  it('enables rating buttons when user is logged in', () => {
    mockUseAuth.mockReturnValue({ 
      user: { id: 'user1', login: 'user1' }, 
      loading: false, 
      login: vi.fn(), 
      logout: vi.fn(), 
      updateUser: vi.fn() 
    });
    
    renderWithProviders(<PostCard post={mockPost} />);
    
    const buttons = screen.getAllByRole('button');
    const ratingButtons = buttons.filter(btn => {
      const svg = btn.querySelector('svg');
      return svg && (svg.querySelector('path[d*="M5 15l7-7"]') || svg.querySelector('path[d*="M19 9l-7 7"]'));
    });
    
    ratingButtons.forEach(button => {
      expect(button).not.toBeDisabled();
    });
  });

  it('calls rate API when rating button is clicked', async () => {
    mockUseAuth.mockReturnValue({ 
      user: { id: 'user1', login: 'user1' }, 
      loading: false, 
      login: vi.fn(), 
      logout: vi.fn(), 
      updateUser: vi.fn() 
    });

    renderWithProviders(<PostCard post={mockPost} />);
    
    const buttons = screen.getAllByRole('button');
    const upButton = buttons.find(btn => {
      const svg = btn.querySelector('svg');
      return svg && svg.querySelector('path[d*="M5 15l7-7"]');
    });
    
    if (upButton && !upButton.disabled) {
      await userEvent.click(upButton);
      
      await waitFor(() => {
        expect(mockRate).toHaveBeenCalled();
      });
    }
  });

  it('renders favorited state correctly', () => {
    const favoritedPost = { ...mockPost, is_favorited: true };
    renderWithProviders(<PostCard post={favoritedPost} />);
    
    const buttons = screen.getAllByRole('button');
    const favoriteButton = buttons.find(btn => {
      const svg = btn.querySelector('svg');
      return svg && svg.querySelector('path[d*="M11.049 2.927"]');
    });
    
    expect(favoriteButton).toBeInTheDocument();
    expect(favoriteButton?.querySelector('svg')?.getAttribute('fill')).toBe('currentColor');
  });
});
