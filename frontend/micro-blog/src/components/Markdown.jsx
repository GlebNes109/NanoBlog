export default function Markdown({ content }) {
  const renderMarkdown = (text) => {
    if (!text) return '';
    
    let html = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/^### (.+)$/gm, '<h3 class="text-lg font-semibold mt-4 mb-2 text-gray-900 dark:text-gray-100">$1</h3>')
      .replace(/^## (.+)$/gm, '<h2 class="text-xl font-semibold mt-4 mb-2 text-gray-900 dark:text-gray-100">$1</h2>')
      .replace(/^# (.+)$/gm, '<h1 class="text-2xl font-bold mt-4 mb-2 text-gray-900 dark:text-gray-100">$1</h1>')
      .replace(/\*\*(.+?)\*\*/g, '<strong class="text-gray-900 dark:text-gray-100">$1</strong>')
      .replace(/\*(.+?)\*/g, '<em class="text-gray-900 dark:text-gray-200">$1</em>')
      .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre class="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-x-auto my-4"><code class="text-gray-800 dark:text-gray-200">$2</code></pre>')
      .replace(/`([^`]+)`/g, '<code class="bg-gray-100 dark:bg-gray-900 px-1 py-0.5 rounded text-sm text-gray-800 dark:text-gray-200">$1</code>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-indigo-600 dark:text-indigo-400 hover:underline" target="_blank" rel="noopener">$1</a>')
      .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="max-w-full rounded-lg my-4" />')
      .replace(/^- (.+)$/gm, '<li class="ml-4 text-gray-700 dark:text-gray-100">• $1</li>')
      .replace(/^\d+\. (.+)$/gm, '<li class="ml-4 list-decimal text-gray-700 dark:text-gray-100">$1</li>')
      .replace(/^> (.+)$/gm, '<blockquote class="border-l-4 border-gray-300 dark:border-gray-600 pl-4 italic my-4 text-gray-700 dark:text-gray-200">$1</blockquote>')
      .replace(/\n\n/g, '</p><p class="my-2 text-gray-700 dark:text-gray-100">')
      .replace(/\n/g, '<br />');
    
    return `<p class="my-2 text-gray-700 dark:text-gray-100">${html}</p>`;
  };

  return (
    <div 
      className="markdown-content"
      dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
    />
  );
}


