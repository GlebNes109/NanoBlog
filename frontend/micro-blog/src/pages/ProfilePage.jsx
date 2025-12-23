import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usersAPI, postsAPI, uploadsAPI } from '../api';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import PostCard from '../components/PostCard';

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [email, setEmail] = useState('');
  const [login, setLogin] = useState('');
  const [bio, setBio] = useState('');
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [saving, setSaving] = useState(false);
  const [uploadingAvatar, setUploadingAvatar] = useState(false);

  useEffect(() => {
    if (!user) {
      navigate('/auth');
      return;
    }
    
    setEmail(user.email || '');
    setLogin(user.login || '');
    setBio(user.bio || '');
    
    loadPosts();
  }, [user, navigate]);

  const loadPosts = async () => {
    setLoading(true);
    try {
      const data = await postsAPI.getMy();
      setPosts(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const validate = () => {
    const newErrors = {};
    
    if (!email) {
      newErrors.email = 'Email обязателен';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Некорректный email';
    }
    
    if (!login) {
      newErrors.login = 'Логин обязателен';
    } else if (login.length < 3) {
      newErrors.login = 'Минимум 3 символа';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    setServerError('');
    if (!validate()) return;
    
    setSaving(true);
    try {
      const updated = await usersAPI.updateMe({ email, login, bio });
      updateUser(updated);
      setEditing(false);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setServerError(typeof detail === 'string' ? detail : 'Не удалось сохранить');
    } finally {
      setSaving(false);
    }
  };

  const handleAvatarChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    if (file.size > 5 * 1024 * 1024) {
      setServerError('Файл слишком большой (макс. 5MB)');
      return;
    }
    
    setUploadingAvatar(true);
    setServerError('');
    try {
      await uploadsAPI.avatar(file);
      const updated = await usersAPI.getMe();
      updateUser(updated);
    } catch {
      setServerError('Не удалось загрузить аватар');
    } finally {
      setUploadingAvatar(false);
    }
  };

  if (!user) return null;

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 mb-8">
          <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
            <div className="relative">
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
              <label className="absolute bottom-0 right-0 p-2 bg-indigo-600 rounded-full cursor-pointer hover:bg-indigo-700 transition-colors">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleAvatarChange}
                  className="hidden"
                  disabled={uploadingAvatar}
                />
                {uploadingAvatar ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                )}
              </label>
            </div>

            <div className="flex-1">
              {editing ? (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Логин
                    </label>
                    <input
                      type="text"
                      value={login}
                      onChange={(e) => setLogin(e.target.value)}
                      className={`w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none text-gray-900 dark:text-white ${
                        errors.login ? 'border-red-500' : 'border-gray-200 dark:border-gray-600'
                      }`}
                    />
                    {errors.login && <p className="mt-1 text-sm text-red-500">{errors.login}</p>}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Email
                    </label>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className={`w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none text-gray-900 dark:text-white ${
                        errors.email ? 'border-red-500' : 'border-gray-200 dark:border-gray-600'
                      }`}
                    />
                    {errors.email && <p className="mt-1 text-sm text-red-500">{errors.email}</p>}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      О себе
                    </label>
                    <textarea
                      value={bio}
                      onChange={(e) => setBio(e.target.value)}
                      rows={3}
                      className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none text-gray-900 dark:text-white resize-none"
                      placeholder="Расскажите о себе..."
                    />
                  </div>
                  {serverError && (
                    <div className="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-2 rounded-lg text-sm">
                      {serverError}
                    </div>
                  )}
                  <div className="flex space-x-3">
                    <button
                      onClick={handleSave}
                      disabled={saving}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50"
                    >
                      {saving ? 'Сохранение...' : 'Сохранить'}
                    </button>
                    <button
                      onClick={() => {
                        setEditing(false);
                        setEmail(user.email || '');
                        setLogin(user.login || '');
                        setBio(user.bio || '');
                        setErrors({});
                        setServerError('');
                      }}
                      className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
                    >
                      Отмена
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between">
                    <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {user.login}
                    </h1>
                    <button
                      onClick={() => setEditing(true)}
                      className="px-4 py-2 text-sm text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/50 rounded-lg transition-colors"
                    >
                      Редактировать
                    </button>
                  </div>
                  <p className="text-gray-500 dark:text-gray-400 mt-1">{user.email}</p>
                  {user.bio && (
                    <p className="text-gray-700 dark:text-gray-300 mt-3">{user.bio}</p>
                  )}
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">
                    На платформе с {new Date(user.createdAt).toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })}
                  </p>
                </>
              )}
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Мои посты ({posts.length})
          </h2>

          {loading ? (
            <div className="flex justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
          ) : posts.length === 0 ? (
            <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
              <p className="text-gray-500 dark:text-gray-400 mb-4">У вас пока нет постов</p>
              <button
                onClick={() => navigate('/create')}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors"
              >
                Написать первый пост
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              {posts.map((post) => (
                <PostCard key={post.id} post={post} onUpdate={loadPosts} />
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}


