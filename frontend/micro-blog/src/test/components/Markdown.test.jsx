import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Markdown from '../../components/Markdown';

describe('Markdown', () => {
  it('renders plain text', () => {
    render(<Markdown content="Hello world" />);
    expect(screen.getByText(/Hello world/)).toBeInTheDocument();
  });

  it('renders bold text', () => {
    render(<Markdown content="**bold text**" />);
    const strong = document.querySelector('strong');
    expect(strong).toBeInTheDocument();
    expect(strong.textContent).toBe('bold text');
  });

  it('renders italic text', () => {
    render(<Markdown content="*italic text*" />);
    const em = document.querySelector('em');
    expect(em).toBeInTheDocument();
    expect(em.textContent).toBe('italic text');
  });

  it('renders inline code', () => {
    render(<Markdown content="`code`" />);
    const code = document.querySelector('code');
    expect(code).toBeInTheDocument();
    expect(code.textContent).toBe('code');
  });

  it('renders headers', () => {
    render(<Markdown content="# Header 1" />);
    const h1 = document.querySelector('h1');
    expect(h1).toBeInTheDocument();
    expect(h1.textContent).toBe('Header 1');
  });

  it('renders links', () => {
    render(<Markdown content="[link](https://example.com)" />);
    const link = document.querySelector('a');
    expect(link).toBeInTheDocument();
    expect(link.getAttribute('href')).toBe('https://example.com');
    expect(link.textContent).toBe('link');
  });

  it('handles empty content', () => {
    render(<Markdown content="" />);
    const container = document.querySelector('.markdown-content');
    expect(container).toBeInTheDocument();
  });

  it('handles null content', () => {
    render(<Markdown content={null} />);
    const container = document.querySelector('.markdown-content');
    expect(container).toBeInTheDocument();
  });
});


