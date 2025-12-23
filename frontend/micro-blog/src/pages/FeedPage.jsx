import { useState, useEffect } from 'react';
import { postsAPI, searchAPI } from '../api';
import PostCard from '../components/PostCard';
import SearchBar from '../components/SearchBar';
import Layout from '../components/Layout';

export default function FeedPage() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const loadPosts = async () => {
    setError('');
    try {
      const data = await postsAPI.getAll();
      setPosts(data);
    } catch (err) {
      setError('Не удалось загрузить посты');
    }
  };

  const handleSearch = async (query) => {
    if (!query.trim()) {
      setSearchQuery('');
      loadPosts();
      return;
    }
    
    setSearchQuery(query);
    setIsSearching(true);
    setError('');
    try {
      const data = await searchAPI.posts(query);
      setPosts(data);
    } catch (err) {
      setError('Ошибка поиска');
    } finally {
      setIsSearching(false);
    }
  };

  useEffect(() => {
    const initialLoad = async () => {
      setLoading(true);
      await loadPosts();
      setLoading(false);
    };
    initialLoad();
  }, []);

  return (
    <Layout>
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
            Лента постов
          </h1>
          <SearchBar onSearch={handleSearch} placeholder="Поиск по постам..." />
          {searchQuery && (
            <div className="mt-4 flex items-center justify-between">
              <p className="text-gray-600 dark:text-gray-400">
                Результаты по запросу: <span className="font-medium">"{searchQuery}"</span>
              </p>
              <button
                onClick={() => { setSearchQuery(''); loadPosts(); }}
                className="text-indigo-600 dark:text-indigo-400 hover:underline text-sm"
              >
                Сбросить
              </button>
            </div>
          )}
        </div>

        {loading || isSearching ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
        ) : error ? (
          <div className="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-6 py-4 rounded-xl">
            {error}
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400 text-lg">
              {searchQuery ? 'Ничего не найдено' : 'Пока нет постов'}
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {posts.map((post) => (
              <PostCard key={post.id} post={post} onUpdate={loadPosts} />
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}


