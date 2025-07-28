import React, { useState } from 'react';
import { 
  Users, 
  MessageSquare, 
  Heart, 
  Share2, 
  Send, 
  Image, 
  Video, 
  Smile, 
  MoreHorizontal,
  UserPlus,
  Search,
  Filter,
  TrendingUp,
  Globe,
  Lock,
  Eye,
  Clock,
  Star,
  Code,
  Zap,
  Award,
  Camera,
  Mic,
  Play,
  Pause,
  Volume2
} from 'lucide-react';

const SocialModule: React.FC = () => {
  const [activeTab, setActiveTab] = useState('feed');
  const [postContent, setPostContent] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // Social posts with tech focus
  const posts = [
    {
      id: 1,
      user: {
        name: 'Alex Chen',
        username: 'alexdev',
        avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=60&h=60&fit=crop',
        verified: true,
        title: 'Senior Rust Developer'
      },
      content: 'Just shipped a new Rust microservice that handles 100k+ requests per second! 🦀 The memory safety and performance are incredible. Here\'s what I learned about optimizing async code...',
      timestamp: '2 hours ago',
      likes: 234,
      comments: 45,
      shares: 12,
      tags: ['Rust', 'Performance', 'Microservices'],
      image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=400&fit=crop',
      type: 'post'
    },
    {
      id: 2,
      user: {
        name: 'Sarah Johnson',
        username: 'sarahgo',
        avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=60&h=60&fit=crop',
        verified: true,
        title: 'Go Cloud Architect'
      },
      content: 'Kubernetes deployment patterns that every Go developer should know. Thread 🧵\n\n1. Use multi-stage Docker builds\n2. Implement health checks\n3. Configure resource limits\n4. Set up proper logging...',
      timestamp: '4 hours ago',
      likes: 567,
      comments: 89,
      shares: 34,
      tags: ['Go', 'Kubernetes', 'DevOps'],
      type: 'thread'
    },
    {
      id: 3,
      user: {
        name: 'David Rodriguez',
        username: 'davidts',
        avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&h=60&fit=crop',
        verified: false,
        title: 'TypeScript Enthusiast'
      },
      content: 'Live coding session: Building a real-time chat app with TypeScript, Socket.io, and React! Join me as we implement type-safe WebSocket communication 🚀',
      timestamp: '6 hours ago',
      likes: 123,
      comments: 28,
      shares: 15,
      tags: ['TypeScript', 'React', 'WebSockets'],
      type: 'live',
      isLive: true
    },
    {
      id: 4,
      user: {
        name: 'Maria Garcia',
        username: 'mariapython',
        avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=60&h=60&fit=crop',
        verified: true,
        title: 'AI/ML Engineer'
      },
      content: 'New Python library for distributed machine learning just dropped! 🐍✨ It makes training models across multiple GPUs so much easier. Check out the benchmarks...',
      timestamp: '8 hours ago',
      likes: 445,
      comments: 67,
      shares: 23,
      tags: ['Python', 'AI/ML', 'GPU'],
      video: 'https://example.com/demo-video.mp4',
      type: 'video'
    },
    {
      id: 5,
      user: {
        name: 'James Wilson',
        username: 'jamesk8s',
        avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=60&h=60&fit=crop',
        verified: true,
        title: 'DevOps Engineer'
      },
      content: 'Kubernetes security best practices every developer should follow. Saved me from a major security incident last week! 🔒',
      timestamp: '12 hours ago',
      likes: 789,
      comments: 156,
      shares: 67,
      tags: ['Kubernetes', 'Security', 'DevOps'],
      type: 'post'
    }
  ];

  const trendingTopics = [
    { tag: 'Rust', posts: 1234, growth: '+45%' },
    { tag: 'TypeScript', posts: 2345, growth: '+32%' },
    { tag: 'Kubernetes', posts: 1567, growth: '+28%' },
    { tag: 'Go', posts: 987, growth: '+41%' },
    { tag: 'Python', posts: 3456, growth: '+19%' },
    { tag: 'Flutter', posts: 876, growth: '+67%' }
  ];

  const suggestedConnections = [
    {
      name: 'Lisa Park',
      username: 'lisaflutter',
      avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=60&h=60&fit=crop',
      title: 'Flutter Developer',
      mutualConnections: 12,
      tags: ['Flutter', 'Mobile', 'Dart']
    },
    {
      name: 'Michael Brown',
      username: 'mikejava',
      avatar: 'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?w=60&h=60&fit=crop',
      title: 'Java Architect',
      mutualConnections: 8,
      tags: ['Java', 'Spring', 'Microservices']
    },
    {
      name: 'Emily Davis',
      username: 'emilyswift',
      avatar: 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=60&h=60&fit=crop',
      title: 'iOS Developer',
      mutualConnections: 15,
      tags: ['Swift', 'iOS', 'SwiftUI']
    }
  ];

  const tabs = [
    { id: 'feed', name: 'Feed', icon: Globe },
    { id: 'connections', name: 'Network', icon: Users },
    { id: 'messages', name: 'Messages', icon: MessageSquare },
    { id: 'trending', name: 'Trending', icon: TrendingUp }
  ];

  const handleLike = (postId: number) => {
    // Handle like functionality
    console.log('Liked post:', postId);
  };

  const handleShare = (postId: number) => {
    // Handle share functionality
    console.log('Shared post:', postId);
  };

  const handleComment = (postId: number) => {
    // Handle comment functionality
    console.log('Comment on post:', postId);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">Social Network</h1>
            <p className="text-cyan-100">
              Connect with developers and share your tech journey
            </p>
          </div>
          <div className="hidden md:block">
            <div className="flex items-center space-x-6 text-cyan-100">
              <div className="text-center">
                <div className="text-2xl font-bold">2.4K</div>
                <div className="text-sm">Connections</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">156</div>
                <div className="text-sm">Posts</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">89%</div>
                <div className="text-sm">Engagement</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-cyan-500 text-cyan-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'feed' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Main Feed */}
              <div className="lg:col-span-2 space-y-6">
                {/* Create Post */}
                <div className="bg-white border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full flex items-center justify-center">
                      <Users className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <textarea
                        value={postContent}
                        onChange={(e) => setPostContent(e.target.value)}
                        placeholder="Share your latest tech discovery..."
                        className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500"
                        rows={3}
                      />
                      <div className="flex items-center justify-between mt-3">
                        <div className="flex items-center space-x-3">
                          <button className="flex items-center space-x-2 text-gray-500 hover:text-cyan-600">
                            <Image className="w-5 h-5" />
                            <span>Photo</span>
                          </button>
                          <button className="flex items-center space-x-2 text-gray-500 hover:text-cyan-600">
                            <Video className="w-5 h-5" />
                            <span>Video</span>
                          </button>
                          <button className="flex items-center space-x-2 text-gray-500 hover:text-cyan-600">
                            <Code className="w-5 h-5" />
                            <span>Code</span>
                          </button>
                        </div>
                        <button className="bg-cyan-600 text-white px-6 py-2 rounded-lg hover:bg-cyan-700 transition-colors font-medium">
                          Post
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Posts Feed */}
                <div className="space-y-6">
                  {posts.map((post) => (
                    <div key={post.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                      {/* Post Header */}
                      <div className="p-4 border-b border-gray-200">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <img
                              src={post.user.avatar}
                              alt={post.user.name}
                              className="w-10 h-10 rounded-full object-cover"
                            />
                            <div>
                              <div className="flex items-center space-x-2">
                                <h3 className="font-semibold text-gray-900">{post.user.name}</h3>
                                {post.user.verified && (
                                  <div className="w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                                    <Star className="w-2 h-2 text-white fill-current" />
                                  </div>
                                )}
                              </div>
                              <div className="flex items-center space-x-2 text-sm text-gray-500">
                                <span>@{post.user.username}</span>
                                <span>•</span>
                                <span>{post.user.title}</span>
                                <span>•</span>
                                <span>{post.timestamp}</span>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            {post.type === 'live' && post.isLive && (
                              <div className="flex items-center space-x-1 bg-red-500 text-white px-2 py-1 rounded text-xs font-medium">
                                <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                                <span>LIVE</span>
                              </div>
                            )}
                            <button className="p-2 text-gray-400 hover:text-gray-600">
                              <MoreHorizontal className="w-5 h-5" />
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Post Content */}
                      <div className="p-4">
                        <p className="text-gray-900 mb-3">{post.content}</p>
                        
                        {/* Tags */}
                        <div className="flex flex-wrap gap-2 mb-3">
                          {post.tags.map((tag, index) => (
                            <span key={index} className="bg-cyan-100 text-cyan-700 px-2 py-1 rounded text-sm font-medium">
                              #{tag}
                            </span>
                          ))}
                        </div>

                        {/* Media */}
                        {post.image && (
                          <img
                            src={post.image}
                            alt="Post content"
                            className="w-full h-64 object-cover rounded-lg mb-3"
                          />
                        )}

                        {post.type === 'video' && (
                          <div className="relative bg-gray-900 rounded-lg mb-3">
                            <div className="aspect-video flex items-center justify-center">
                              <button className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center hover:bg-white/30 transition-colors">
                                <Play className="w-8 h-8 text-white ml-1" />
                              </button>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Post Actions */}
                      <div className="px-4 py-3 border-t border-gray-200">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-6">
                            <button
                              onClick={() => handleLike(post.id)}
                              className="flex items-center space-x-2 text-gray-500 hover:text-red-500 transition-colors"
                            >
                              <Heart className="w-5 h-5" />
                              <span>{post.likes}</span>
                            </button>
                            <button
                              onClick={() => handleComment(post.id)}
                              className="flex items-center space-x-2 text-gray-500 hover:text-blue-500 transition-colors"
                            >
                              <MessageSquare className="w-5 h-5" />
                              <span>{post.comments}</span>
                            </button>
                            <button
                              onClick={() => handleShare(post.id)}
                              className="flex items-center space-x-2 text-gray-500 hover:text-green-500 transition-colors"
                            >
                              <Share2 className="w-5 h-5" />
                              <span>{post.shares}</span>
                            </button>
                          </div>
                          <div className="flex items-center space-x-2 text-sm text-gray-500">
                            <Eye className="w-4 h-4" />
                            <span>{post.likes + post.comments * 3} views</
(Content truncated due to size limit. Use line ranges to read in chunks)