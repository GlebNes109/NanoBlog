import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { usersAPI } from '../api';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import PostCard from '../components/PostCard';

export default function UserPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user: currentUser } = useAuth();
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (currentUser && id === currentUser.id) {
      navigate('/profile');
      return;
    }
    
    loadUser();
  }, [id, currentUser, navigate]);

  const loadUser = async () => {
    setLoading(true);
    setError('');
    try {
      const [userData, userPosts] = await Promise.all([
        usersAPI.getUser(id),
        usersAPI.getUserPosts(id),
      ]);
      setUser(userData);
      setPosts(userPosts);
    } catch {
      setError('Пользователь не найден');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (currentUser && id === currentUser.id) {
      navigate('/profile');
      return;
    }
    
    loadUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, currentUser, navigate]);

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="max-w-2xl mx-auto text-center py-12">
          <p className="text-gray-500 dark:text-gray-400 text-lg mb-4">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="text-indigo-600 dark:text-indigo-400 hover:underline"
          >
            Вернуться на главную
          </button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 mb-8">
          <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
            {user.avatar_url ? (
              <img
                src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${user.avatar_url}`}
                alt={user.login}
                className="w-24 h-24 rounded-full object-cover"
              />
            ) : (
              <div className="w-24 h-24 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
                <span className="text-indigo-600 dark:text-indigo-400 font-bold text-3xl">
                  {user.login?.[0]?.toUpperCase() || '?'}
                </span>
              </div>
            )}

            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                {user.login}
              </h1>
              <p className="text-gray-500 dark:text-gray-400 mt-1">{user.email}</p>
              {user.bio && (
                <p className="text-gray-700 dark:text-gray-300 mt-3">{user.bio}</p>
              )}
              <div className="flex items-center gap-6 mt-4 text-sm text-gray-500 dark:text-gray-400">
                <span>{user.posts_count || 0} постов</span>
                <span>
                  На платформе с {new Date(user.createdAt).toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Посты пользователя
          </h2>

          {posts.length === 0 ? (
            <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
              <p className="text-gray-500 dark:text-gray-400">
                У пользователя пока нет постов
              </p>
            </div>
          ) : (
            <div className="space-y-6">
              {posts.map((post) => (
                <PostCard key={post.id} post={post} />
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}


