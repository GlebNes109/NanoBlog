import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SearchBar from '../../components/SearchBar';

describe('SearchBar', () => {
  it('renders input with placeholder', () => {
    render(<SearchBar onSearch={() => {}} placeholder="Search..." />);
    expect(screen.getByPlaceholderText('Search...')).toBeInTheDocument();
  });

  it('calls onSearch when form is submitted', async () => {
    const onSearch = vi.fn();
    const user = userEvent.setup();
    
    render(<SearchBar onSearch={onSearch} />);
    
    const input = screen.getByRole('textbox');
    await user.type(input, 'test query');
    
    const button = screen.getByRole('button', { name: /найти/i });
    await user.click(button);
    
    expect(onSearch).toHaveBeenCalledWith('test query');
  });

  it('does not call onSearch when query is empty', async () => {
    const onSearch = vi.fn();
    const user = userEvent.setup();
    
    render(<SearchBar onSearch={onSearch} />);
    
    const button = screen.getByRole('button', { name: /найти/i });
    await user.click(button);
    
    expect(onSearch).not.toHaveBeenCalled();
  });

  it('trims whitespace from query', async () => {
    const onSearch = vi.fn();
    const user = userEvent.setup();
    
    render(<SearchBar onSearch={onSearch} />);
    
    const input = screen.getByRole('textbox');
    await user.type(input, '  test  ');
    
    const button = screen.getByRole('button', { name: /найти/i });
    await user.click(button);
    
    expect(onSearch).toHaveBeenCalledWith('test');
  });
});


