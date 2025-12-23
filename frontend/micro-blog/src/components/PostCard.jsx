import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { postsAPI, favoritesAPI } from '../api';
import { useAuth } from '../context/AuthContext';
import Markdown from './Markdown';
import { ChatBubbleIcon, ChevronUpIcon, ChevronDownIcon, StarIcon } from './Icons';

export default function PostCard({ post, onUpdate }) {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [ratingLoading, setRatingLoading] = useState(false);
  const [localPost, setLocalPost] = useState(post);

  useEffect(() => {
    setLocalPost(post);
  }, [post]);

  const handleRate = async (value) => {
    if (!user || ratingLoading) return;
    setRatingLoading(true);
    try {
      const newValue = localPost.user_rating === value ? 0 : value;
      await postsAPI.rate(localPost.id, newValue);
      if (onUpdate) {
        await onUpdate();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setRatingLoading(false);
    }
  };

  const handleFavorite = async () => {
    if (!user || loading) return;
    setLoading(true);
    try {
      if (localPost.is_favorited) {
        await favoritesAPI.remove(localPost.id);
      } else {
        await favoritesAPI.add(localPost.id);
      }
      setLocalPost({ ...localPost, is_favorited: !localPost.is_favorited });
      onUpdate?.();
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  };

  return (
    <article className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-md transition-shadow">
      <div className="p-6">
        <div className="flex items-center mb-4">
          <Link to={`/user/${localPost.authorId}`} className="flex items-center space-x-3">
            {localPost.authorAvatar ? (
              <img
                src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${localPost.authorAvatar}`}
                alt={localPost.authorLogin}
                className="w-10 h-10 rounded-full object-cover"
              />
            ) : (
              <div className="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
                <span className="text-indigo-600 dark:text-indigo-400 font-medium">
                  {localPost.authorLogin?.[0]?.toUpperCase() || '?'}
                </span>
              </div>
            )}
            <div>
              <p className="font-medium text-gray-900 dark:text-white hover:text-indigo-600 dark:hover:text-indigo-400">
                {localPost.authorLogin}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {formatDate(localPost.createdAt)}
              </p>
            </div>
          </Link>
        </div>

        <Link to={`/post/${localPost.id}`}>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 hover:text-indigo-600 dark:hover:text-indigo-400">
            {localPost.title}
          </h2>
        </Link>

        <div className="text-gray-700 dark:text-gray-100 mb-4 line-clamp-3 prose prose-sm dark:prose-invert max-w-none">
          <Markdown content={localPost.content.slice(0, 300) + (localPost.content.length > 300 ? '...' : '')} />
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-700">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <button
                onClick={() => handleRate(1)}
                disabled={!user || ratingLoading}
                className={`p-1 rounded transition-colors ${
                  localPost.user_rating === 1
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-gray-400 hover:text-green-600 dark:hover:text-green-400'
                } ${!user || ratingLoading ? 'cursor-not-allowed opacity-50' : ''}`}
              >
                <ChevronUpIcon className="w-5 h-5" />
              </button>
              <span className={`font-medium ${
                localPost.rating > 0 ? 'text-green-600 dark:text-green-400' :
                localPost.rating < 0 ? 'text-red-600 dark:text-red-400' :
                'text-gray-500 dark:text-gray-400'
              }`}>
                {localPost.rating}
              </span>
              <button
                onClick={() => handleRate(-1)}
                disabled={!user || ratingLoading}
                className={`p-1 rounded transition-colors ${
                  localPost.user_rating === -1
                    ? 'text-red-600 dark:text-red-400'
                    : 'text-gray-400 hover:text-red-600 dark:hover:text-red-400'
                } ${!user || ratingLoading ? 'cursor-not-allowed opacity-50' : ''}`}
              >
                <ChevronDownIcon className="w-5 h-5" />
              </button>
            </div>

            <Link
              to={`/post/${localPost.id}`}
              className="flex items-center space-x-1 text-gray-500 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400"
            >
              <ChatBubbleIcon className="w-5 h-5" />
              <span>{localPost.comments_count || 0}</span>
            </Link>
          </div>

          <button
            onClick={handleFavorite}
            disabled={!user}
            className={`p-2 rounded-lg transition-colors ${
              localPost.is_favorited
                ? 'text-yellow-500 dark:text-yellow-400'
                : 'text-gray-400 hover:text-yellow-500 dark:hover:text-yellow-400'
            } ${!user ? 'cursor-not-allowed opacity-50' : ''}`}
          >
            <StarIcon className="w-5 h-5" filled={localPost.is_favorited} />
          </button>
        </div>
      </div>
    </article>
  );
}


