import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { postsAPI, commentsAPI, favoritesAPI } from '../api';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import Markdown from '../components/Markdown';
import { ChatBubbleIcon, ChevronUpIcon, ChevronDownIcon, StarIcon } from '../components/Icons';

export default function PostPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [commentError, setCommentError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [ratingLoading, setRatingLoading] = useState(false);

  const loadPost = async () => {
    try {
      const data = await postsAPI.getOne(id);
      setPost(data);
    } catch (err) {
      setError('Пост не найден');
    }
  };

  const loadComments = async () => {
    try {
      const data = await commentsAPI.getAll(id);
      setComments(data);
    } catch (err) {
      console.error('Failed to load comments', err);
    }
  };

  useEffect(() => {
    setLoading(true);
    Promise.all([loadPost(), loadComments()]).finally(() => setLoading(false));
  }, [id]);

  const handleRate = async (value) => {
    if (!user || !post || ratingLoading) return;
    setRatingLoading(true);
    try {
      const newValue = post.user_rating === value ? 0 : value;
      await postsAPI.rate(post.id, newValue);
      await loadPost();
    } catch (err) {
      console.error(err);
    } finally {
      setRatingLoading(false);
    }
  };

  const handleFavorite = async () => {
    if (!user || !post) return;
    try {
      if (post.is_favorited) {
        await favoritesAPI.remove(post.id);
      } else {
        await favoritesAPI.add(post.id);
      }
      setPost({ ...post, is_favorited: !post.is_favorited });
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) {
      setCommentError('Комментарий не может быть пустым');
      return;
    }
    
    setSubmitting(true);
    setCommentError('');
    try {
      const comment = await commentsAPI.create(id, newComment);
      setComments([comment, ...comments]);
      setNewComment('');
    } catch (err) {
      setCommentError('Не удалось добавить комментарий');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteComment = async (commentId) => {
    try {
      await commentsAPI.delete(id, commentId);
      setComments(comments.filter(c => c.id !== commentId));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeletePost = async () => {
    if (!confirm('Удалить этот пост?')) return;
    try {
      await postsAPI.delete(id);
      navigate('/');
    } catch (err) {
      console.error(err);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

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
      <article className="max-w-3xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="p-8">
            <div className="flex items-center justify-between mb-6">
              <Link to={`/user/${post.authorId}`} className="flex items-center space-x-4">
                {post.authorAvatar ? (
                  <img
                    src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${post.authorAvatar}`}
                    alt={post.authorLogin}
                    className="w-12 h-12 rounded-full object-cover"
                  />
                ) : (
                  <div className="w-12 h-12 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
                    <span className="text-indigo-600 dark:text-indigo-400 font-medium text-lg">
                      {post.authorLogin?.[0]?.toUpperCase() || '?'}
                    </span>
                  </div>
                )}
                <div>
                  <p className="font-medium text-gray-900 dark:text-white hover:text-indigo-600 dark:hover:text-indigo-400">
                    {post.authorLogin}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {formatDate(post.createdAt)}
                  </p>
                </div>
              </Link>
              
              {user && user.id === post.authorId && (
                <div className="flex items-center space-x-2">
                  <Link
                    to={`/edit/${post.id}`}
                    className="px-4 py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400"
                  >
                    Редактировать
                  </Link>
                  <button
                    onClick={handleDeletePost}
                    className="px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:text-red-700"
                  >
                    Удалить
                  </button>
                </div>
              )}
            </div>

            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
              {post.title}
            </h1>

            <div className="prose dark:prose-invert max-w-none mb-8 text-gray-700 dark:text-gray-100">
              <Markdown content={post.content} />
            </div>

            <div className="flex items-center justify-between pt-6 border-t border-gray-100 dark:border-gray-700">
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleRate(1)}
                    disabled={!user || ratingLoading}
                    className={`p-2 rounded-lg transition-colors ${
                      post.user_rating === 1
                        ? 'text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/50'
                        : 'text-gray-400 hover:text-green-600 dark:hover:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/50'
                    } ${!user || ratingLoading ? 'cursor-not-allowed opacity-50' : ''}`}
                  >
                    <ChevronUpIcon className="w-5 h-5" />
                  </button>
                  <span className={`text-lg font-medium ${
                    post.rating > 0 ? 'text-green-600 dark:text-green-400' :
                    post.rating < 0 ? 'text-red-600 dark:text-red-400' :
                    'text-gray-500 dark:text-gray-400'
                  }`}>
                    {post.rating}
                  </span>
                  <button
                    onClick={() => handleRate(-1)}
                    disabled={!user || ratingLoading}
                    className={`p-2 rounded-lg transition-colors ${
                      post.user_rating === -1
                        ? 'text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/50'
                        : 'text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/50'
                    } ${!user || ratingLoading ? 'cursor-not-allowed opacity-50' : ''}`}
                  >
                    <ChevronDownIcon className="w-5 h-5" />
                  </button>
                </div>

                <div className="flex items-center space-x-1 text-gray-500 dark:text-gray-400">
                  <ChatBubbleIcon className="w-5 h-5" />
                  <span>{comments.length} комментариев</span>
                </div>
              </div>

              <button
                onClick={handleFavorite}
                disabled={!user}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                  post.is_favorited
                    ? 'text-yellow-500 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/50'
                    : 'text-gray-400 hover:text-yellow-500 dark:hover:text-yellow-400 hover:bg-yellow-50 dark:hover:bg-yellow-900/50'
                } ${!user ? 'cursor-not-allowed opacity-50' : ''}`}
              >
                <StarIcon className="w-5 h-5" filled={post.is_favorited} />
                <span className="text-sm">{post.is_favorited ? 'В избранном' : 'В избранное'}</span>
              </button>
            </div>
          </div>
        </div>

        <div className="mt-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Комментарии
          </h2>

          {user && (
            <form onSubmit={handleAddComment} className="mb-8">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                rows={3}
                className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition text-gray-900 dark:text-white resize-none"
                placeholder="Написать комментарий..."
              />
              {commentError && (
                <p className="mt-1 text-sm text-red-500">{commentError}</p>
              )}
              <div className="mt-3 flex justify-end">
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50"
                >
                  {submitting ? 'Отправка...' : 'Отправить'}
                </button>
              </div>
            </form>
          )}

          {comments.length === 0 ? (
            <p className="text-center text-gray-500 dark:text-gray-400 py-8">
              Пока нет комментариев
            </p>
          ) : (
            <div className="space-y-4">
              {comments.map((comment) => (
                <div
                  key={comment.id}
                  className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700"
                >
                  <div className="flex items-start justify-between">
                    <Link to={`/user/${comment.authorId}`} className="flex items-center space-x-3">
                      {comment.authorAvatar ? (
                        <img
                          src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${comment.authorAvatar}`}
                          alt={comment.authorLogin}
                          className="w-8 h-8 rounded-full object-cover"
                        />
                      ) : (
                        <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
                          <span className="text-indigo-600 dark:text-indigo-400 text-sm font-medium">
                            {comment.authorLogin?.[0]?.toUpperCase() || '?'}
                          </span>
                        </div>
                      )}
                      <div>
                        <p className="font-medium text-gray-900 dark:text-white text-sm">
                          {comment.authorLogin}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {formatDate(comment.createdAt)}
                        </p>
                      </div>
                    </Link>
                    {user && user.id === comment.authorId && (
                      <button
                        onClick={() => handleDeleteComment(comment.id)}
                        className="text-gray-400 hover:text-red-500 text-sm"
                      >
                        Удалить
                      </button>
                    )}
                  </div>
                  <p className="mt-3 text-gray-700 dark:text-gray-100">
                    {comment.content}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </article>
    </Layout>
  );
}


