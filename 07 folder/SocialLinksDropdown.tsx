import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';

interface SocialNetwork {
  id: string;
  name: string;
  icon: string;
  color: string;
  placeholder: string;
  urlPattern: string;
  description: string;
  category: 'professional' | 'social' | 'creative' | 'developer' | 'gaming' | 'business';
  isConnected?: boolean;
  username?: string;
  profileUrl?: string;
}

interface SocialLinksDropdownProps {
  trigger: React.ReactNode;
  onConnect?: (network: SocialNetwork, username: string) => void;
  onDisconnect?: (network: SocialNetwork) => void;
  className?: string;
}

const SocialLinksDropdown: React.FC<SocialLinksDropdownProps> = ({
  trigger,
  onConnect,
  onDisconnect,
  className = ''
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [connectingNetwork, setConnectingNetwork] = useState<string | null>(null);
  const [usernameInput, setUsernameInput] = useState('');
  const dropdownRef = useRef<HTMLDivElement>(null);

  const socialNetworks: SocialNetwork[] = [
    // Professional Networks
    {
      id: 'linkedin',
      name: 'LinkedIn',
      icon: '💼',
      color: '#0077B5',
      placeholder: 'your-linkedin-username',
      urlPattern: 'https://linkedin.com/in/{username}',
      description: 'Professional networking platform',
      category: 'professional'
    },
    {
      id: 'github',
      name: 'GitHub',
      icon: '🐙',
      color: '#181717',
      placeholder: 'your-github-username',
      urlPattern: 'https://github.com/{username}',
      description: 'Code repositories and collaboration',
      category: 'developer'
    },
    {
      id: 'stackoverflow',
      name: 'Stack Overflow',
      icon: '📚',
      color: '#F58025',
      placeholder: 'your-stackoverflow-id',
      urlPattern: 'https://stackoverflow.com/users/{username}',
      description: 'Programming Q&A community',
      category: 'developer'
    },
    {
      id: 'behance',
      name: 'Behance',
      icon: '🎨',
      color: '#1769FF',
      placeholder: 'your-behance-username',
      urlPattern: 'https://behance.net/{username}',
      description: 'Creative portfolio showcase',
      category: 'creative'
    },
    {
      id: 'dribbble',
      name: 'Dribbble',
      icon: '🏀',
      color: '#EA4C89',
      placeholder: 'your-dribbble-username',
      urlPattern: 'https://dribbble.com/{username}',
      description: 'Design community and portfolio',
      category: 'creative'
    },

    // Social Media
    {
      id: 'twitter',
      name: 'Twitter/X',
      icon: '🐦',
      color: '#1DA1F2',
      placeholder: 'your-twitter-handle',
      urlPattern: 'https://twitter.com/{username}',
      description: 'Microblogging and news',
      category: 'social'
    },
    {
      id: 'instagram',
      name: 'Instagram',
      icon: '📷',
      color: '#E4405F',
      placeholder: 'your-instagram-username',
      urlPattern: 'https://instagram.com/{username}',
      description: 'Photo and video sharing',
      category: 'social'
    },
    {
      id: 'facebook',
      name: 'Facebook',
      icon: '👥',
      color: '#1877F2',
      placeholder: 'your-facebook-username',
      urlPattern: 'https://facebook.com/{username}',
      description: 'Social networking platform',
      category: 'social'
    },
    {
      id: 'tiktok',
      name: 'TikTok',
      icon: '🎵',
      color: '#000000',
      placeholder: 'your-tiktok-username',
      urlPattern: 'https://tiktok.com/@{username}',
      description: 'Short-form video content',
      category: 'social'
    },
    {
      id: 'snapchat',
      name: 'Snapchat',
      icon: '👻',
      color: '#FFFC00',
      placeholder: 'your-snapchat-username',
      urlPattern: 'https://snapchat.com/add/{username}',
      description: 'Multimedia messaging',
      category: 'social'
    },

    // Creative Platforms
    {
      id: 'youtube',
      name: 'YouTube',
      icon: '📺',
      color: '#FF0000',
      placeholder: 'your-channel-name',
      urlPattern: 'https://youtube.com/@{username}',
      description: 'Video content creation',
      category: 'creative'
    },
    {
      id: 'twitch',
      name: 'Twitch',
      icon: '🎮',
      color: '#9146FF',
      placeholder: 'your-twitch-username',
      urlPattern: 'https://twitch.tv/{username}',
      description: 'Live streaming platform',
      category: 'gaming'
    },
    {
      id: 'pinterest',
      name: 'Pinterest',
      icon: '📌',
      color: '#BD081C',
      placeholder: 'your-pinterest-username',
      urlPattern: 'https://pinterest.com/{username}',
      description: 'Visual discovery and ideas',
      category: 'creative'
    },
    {
      id: 'deviantart',
      name: 'DeviantArt',
      icon: '🎭',
      color: '#05CC47',
      placeholder: 'your-deviantart-username',
      urlPattern: 'https://deviantart.com/{username}',
      description: 'Art community and gallery',
      category: 'creative'
    },

    // Developer Platforms
    {
      id: 'gitlab',
      name: 'GitLab',
      icon: '🦊',
      color: '#FC6D26',
      placeholder: 'your-gitlab-username',
      urlPattern: 'https://gitlab.com/{username}',
      description: 'DevOps and code collaboration',
      category: 'developer'
    },
    {
      id: 'bitbucket',
      name: 'Bitbucket',
      icon: '🪣',
      color: '#0052CC',
      placeholder: 'your-bitbucket-username',
      urlPattern: 'https://bitbucket.org/{username}',
      description: 'Git repository hosting',
      category: 'developer'
    },
    {
      id: 'codepen',
      name: 'CodePen',
      icon: '✏️',
      color: '#000000',
      placeholder: 'your-codepen-username',
      urlPattern: 'https://codepen.io/{username}',
      description: 'Frontend code playground',
      category: 'developer'
    },
    {
      id: 'replit',
      name: 'Replit',
      icon: '🔄',
      color: '#F26207',
      placeholder: 'your-replit-username',
      urlPattern: 'https://replit.com/@{username}',
      description: 'Online coding environment',
      category: 'developer'
    },
    {
      id: 'hackerrank',
      name: 'HackerRank',
      icon: '🏆',
      color: '#2EC866',
      placeholder: 'your-hackerrank-username',
      urlPattern: 'https://hackerrank.com/{username}',
      description: 'Coding challenges and skills',
      category: 'developer'
    },
    {
      id: 'leetcode',
      name: 'LeetCode',
      icon: '🧩',
      color: '#FFA116',
      placeholder: 'your-leetcode-username',
      urlPattern: 'https://leetcode.com/{username}',
      description: 'Algorithm and data structure practice',
      category: 'developer'
    },

    // Business & Professional
    {
      id: 'medium',
      name: 'Medium',
      icon: '📝',
      color: '#000000',
      placeholder: 'your-medium-username',
      urlPattern: 'https://medium.com/@{username}',
      description: 'Publishing and blogging platform',
      category: 'professional'
    },
    {
      id: 'substack',
      name: 'Substack',
      icon: '📰',
      color: '#FF6719',
      placeholder: 'your-substack-name',
      urlPattern: 'https://{username}.substack.com',
      description: 'Newsletter and subscription platform',
      category: 'professional'
    },
    {
      id: 'angellist',
      name: 'AngelList',
      icon: '👼',
      color: '#000000',
      placeholder: 'your-angellist-username',
      urlPattern: 'https://angel.co/u/{username}',
      description: 'Startup and investment platform',
      category: 'business'
    },
    {
      id: 'producthunt',
      name: 'Product Hunt',
      icon: '🚀',
      color: '#DA552F',
      placeholder: 'your-producthunt-username',
      urlPattern: 'https://producthunt.com/@{username}',
      description: 'Product discovery platform',
      category: 'business'
    },

    // Gaming
    {
      id: 'steam',
      name: 'Steam',
      icon: '🎮',
      color: '#171A21',
      placeholder: 'your-steam-id',
      urlPattern: 'https://steamcommunity.com/id/{username}',
      description: 'Gaming platform and community',
      category: 'gaming'
    },
    {
      id: 'discord',
      name: 'Discord',
      icon: '💬',
      color: '#5865F2',
      placeholder: 'username#1234',
      urlPattern: 'discord://{username}',
      description: 'Gaming and community chat',
      category: 'gaming'
    },

    // Additional Platforms
    {
      id: 'reddit',
      name: 'Reddit',
      icon: '🤖',
      color: '#FF4500',
      placeholder: 'your-reddit-username',
      urlPattern: 'https://reddit.com/u/{username}',
      description: 'Discussion and community platform',
      category: 'social'
    },
    {
      id: 'telegram',
      name: 'Telegram',
      icon: '✈️',
      color: '#0088CC',
      placeholder: 'your-telegram-username',
      urlPattern: 'https://t.me/{username}',
      description: 'Messaging and channels',
      category: 'social'
    },
    {
      id: 'whatsapp',
      name: 'WhatsApp',
      icon: '📱',
      color: '#25D366',
      placeholder: 'your-phone-number',
      urlPattern: 'https://wa.me/{username}',
      description: 'Messaging platform',
      category: 'social'
    },
    {
      id: 'spotify',
      name: 'Spotify',
      icon: '🎵',
      color: '#1DB954',
      placeholder: 'your-spotify-username',
      urlPattern: 'https://open.spotify.com/user/{username}',
      description: 'Music streaming and playlists',
      category: 'creative'
    }
  ];

  const categories = [
    { id: 'all', name: 'All Networks', icon: '🌐' },
    { id: 'professional', name: 'Professional', icon: '💼' },
    { id: 'developer', name: 'Developer', icon: '💻' },
    { id: 'social', name: 'Social Media', icon: '👥' },
    { id: 'creative', name: 'Creative', icon: '🎨' },
    { id: 'gaming', name: 'Gaming', icon: '🎮' },
    { id: 'business', name: 'Business', icon: '🏢' }
  ];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setConnectingNetwork(null);
        setUsernameInput('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const filteredNetworks = socialNetworks.filter(network => {
    const matchesCategory = activeCategory === 'all' || network.category === activeCategory;
    const matchesSearch = network.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         network.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const handleConnect = (network: SocialNetwork) => {
    if (network.isConnected) {
      if (onDisconnect) {
        onDisconnect(network);
      }
    } else {
      setConnectingNetwork(network.id);
      setUsernameInput('');
    }
  };

  const handleSubmitConnection = (network: SocialNetwork) => {
    if (usernameInput.trim() && onConnect) {
      onConnect(network, usernameInput.trim());
      setConnectingNetwork(null);
      setUsernameInput('');
    }
  };

  const handleCancelConnection = () => {
    setConnectingNetwork(null);
    setUsernameInput('');
  };

  return (
    <div ref={dropdownRef} className={`relative ${className}`}>
      <div onClick={() => setIsOpen(!isOpen)} className="cursor-pointer">
        {trigger}
      </div>

      {isOpen && (
        <div className="absolute top-full right-0 mt-2 w-96 bg-white dark:bg-gray-900 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50">
          {/* Header */}
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Connect Social Networks
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Link your profiles to showcase your presence across platforms
            </p>
          </div>

          {/* Search */}
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="relative">
              <input
                type="text"
                placeholder="Search networks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
          </div>

          {/* Categories */}
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex flex-wrap gap-2">
              {categories.map(category => (
                <button
                  key={category.id}
                  onClick={() => setActiveCategory(category.id)}
                  className={`
                    px-3 py-1 rounded-full text-xs font-medium transition-colors
                    ${activeCategory === category.id
                      ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                      : 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                    }
                  `}
                >
                  {category.icon} {category.name}
                </button>
              ))}
            </div>
          </div>

          {/* Networks List */}
          <div className="max-h-96 overflow-y-auto">
            {filteredNetworks.length === 0 ? (
              <div className="p-8 text-center text-gray-500 dark:text-gray-400">
                <div className="text-4xl mb-2">🔍</div>
                <p>No networks found matching your search.</p>
              </div>
            ) : (
              <div className="p-2">
                {filteredNetworks.map(network => (
                  <div key={network.id} className="p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                    {connectingNetwork === network.id ? (
                      // Connection Form
                      <div className="space-y-3">
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">{network.icon}</span>
                          <div>
                            <h4 className="font-medium text-gray-900 dark:text-white">
                              Connect {network.name}
                            </h4>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                              {network.description}
                            </p>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          <input
                            type="text"
                            placeholder={network.placeholder}
                            value={usernameInput}
                            onChange={(e) => setUsernameInput(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
                            autoFocus
            
(Content truncated due to size limit. Use line ranges to read in chunks)