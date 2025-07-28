import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  TrendingUp,
  Users,
  BookOpen,
  Briefcase,
  ShoppingBag,
  Bot,
  Code,
  Terminal,
  Database,
  Cloud,
  Server,
  Container,
  GitBranch,
  Zap,
  Activity,
  Award,
  Clock,
  Star,
  ArrowRight,
  Play,
  Cpu,
  Layers,
  Globe,
  Shield
} from 'lucide-react';

const DashboardHome: React.FC = () => {
  const { user } = useAuth();
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Modern tech stack with current industry usage
  const techStack = {
    languages: [
      { name: 'Rust', icon: '🦀', usage: '95%', trend: '+12%', description: 'Systems programming, WebAssembly' },
      { name: 'Go', icon: '🐹', usage: '92%', trend: '+8%', description: 'Microservices, Cloud native' },
      { name: 'TypeScript', icon: '📘', usage: '98%', trend: '+15%', description: 'Frontend, Full-stack development' },
      { name: 'Python', icon: '🐍', usage: '96%', trend: '+10%', description: 'AI/ML, Data science, Backend' },
      { name: 'Java', icon: '☕', usage: '89%', trend: '+5%', description: 'Enterprise, Android development' },
      { name: 'Kotlin', icon: '🎯', usage: '87%', trend: '+18%', description: 'Android, Multiplatform' },
      { name: 'Swift', icon: '🍎', usage: '91%', trend: '+7%', description: 'iOS, macOS development' },
      { name: 'C#', icon: '🔷', usage: '85%', trend: '+6%', description: '.NET, Game development' }
    ],
    frameworks: [
      { name: 'Django', icon: '🎸', usage: '88%', trend: '+9%', description: 'Python web framework' },
      { name: 'Flask', icon: '🌶️', usage: '82%', trend: '+7%', description: 'Lightweight Python framework' },
      { name: 'Flutter', icon: '💙', usage: '89%', trend: '+22%', description: 'Cross-platform mobile' },
      { name: 'React', icon: '⚛️', usage: '94%', trend: '+11%', description: 'Frontend library' }
    ],
    devops: [
      { name: 'Kubernetes', icon: '☸️', usage: '91%', trend: '+16%', description: 'Container orchestration' },
      { name: 'Docker', icon: '🐳', usage: '96%', trend: '+8%', description: 'Containerization' },
      { name: 'OpenShift', icon: '🔴', usage: '78%', trend: '+12%', description: 'Enterprise Kubernetes' }
    ],
    infrastructure: [
      { name: 'Bare Metal', icon: '🔧', usage: '72%', trend: '+5%', description: 'Direct hardware access' },
      { name: 'Hypervisors', icon: '💻', usage: '85%', trend: '+3%', description: 'Virtualization layer' }
    ]
  };

  const quickStats = [
    { label: 'Active Projects', value: '12', icon: Code, color: 'bg-blue-500' },
    { label: 'Learning Progress', value: '78%', icon: BookOpen, color: 'bg-green-500' },
    { label: 'Network Connections', value: '156', icon: Users, color: 'bg-purple-500' },
    { label: 'Marketplace Sales', value: '$2,340', icon: ShoppingBag, color: 'bg-orange-500' }
  ];

  const recentActivity = [
    { type: 'code', message: 'Completed Rust microservice tutorial', time: '2 hours ago', icon: Code },
    { type: 'social', message: 'Connected with 3 new developers', time: '4 hours ago', icon: Users },
    { type: 'job', message: 'Applied to Senior Go Developer position', time: '6 hours ago', icon: Briefcase },
    { type: 'learning', message: 'Finished Kubernetes deployment course', time: '1 day ago', icon: BookOpen }
  ];

  const recommendedCourses = [
    {
      title: 'Advanced Rust Programming',
      instructor: 'Systems Expert',
      duration: '8 hours',
      rating: 4.9,
      students: 1234,
      image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=300&h=200&fit=crop'
    },
    {
      title: 'Kubernetes in Production',
      instructor: 'DevOps Master',
      duration: '12 hours',
      rating: 4.8,
      students: 2156,
      image: 'https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=300&h=200&fit=crop'
    },
    {
      title: 'TypeScript for Large Applications',
      instructor: 'Frontend Guru',
      duration: '6 hours',
      rating: 4.9,
      students: 3421,
      image: 'https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=300&h=200&fit=crop'
    }
  ];

  const getGreeting = () => {
    const hour = currentTime.getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              {getGreeting()}, {user?.first_name}! 👋
            </h1>
            <p className="text-indigo-100 text-lg">
              Ready to build something amazing with modern technologies?
            </p>
            <div className="mt-4 flex items-center space-x-4 text-sm text-indigo-100">
              <div className="flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                {currentTime.toLocaleTimeString()}
              </div>
              <div className="flex items-center">
                <Activity className="w-4 h-4 mr-1" />
                All systems operational
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="w-32 h-32 bg-white/10 rounded-full flex items-center justify-center">
              <Zap className="w-16 h-16 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {quickStats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 ${stat.color} rounded-lg flex items-center justify-center`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Modern Tech Stack Overview */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900 flex items-center">
            <Cpu className="w-6 h-6 mr-2 text-indigo-600" />
            Current Industry Tech Stack
          </h2>
          <Link
            to="/dashboard/dev-tools"
            className="text-indigo-600 hover:text-indigo-700 font-medium flex items-center"
          >
            Explore Tools
            <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Programming Languages */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Code className="w-5 h-5 mr-2 text-blue-600" />
              Programming Languages
            </h3>
            <div className="space-y-3">
              {techStack.languages.slice(0, 4).map((lang, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{lang.icon}</span>
                    <div>
                      <p className="font-medium text-gray-900">{lang.name}</p>
                      <p className="text-sm text-gray-600">{lang.description}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">{lang.usage}</p>
                    <p className="text-xs text-green-600">{lang.trend}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* DevOps & Infrastructure */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Server className="w-5 h-5 mr-2 text-green-600" />
              DevOps & Infrastructure
            </h3>
            <div className="space-y-3">
              {[...techStack.devops, ...techStack.infrastructure].map((tech, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{tech.icon}</span>
                    <div>
                      <p className="font-medium text-gray-900">{tech.name}</p>
                      <p className="text-sm text-gray-600">{tech.description}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">{tech.usage}</p>
                    <p className="text-xs text-green-600">{tech.trend}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
            <Activity className="w-6 h-6 mr-2 text-purple-600" />
            Recent Activity
          </h2>
          <div className="space-y-4">
            {recentActivity.map((activity, index) => {
              const Icon = activity.icon;
              return (
                <div key={index} className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                    <Icon className="w-4 h-4 text-gray-600" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-900">{activity.message}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              );
            })}
          </div>
          <Link
            to="/dashboard/social"
            className="block mt-4 text-center text-indigo-600 hover:text-indigo-700 font-medium"
          >
            View all activity
          </Link>
        </div>

        {/* Recommended Courses */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
            <BookOpen className="w-6 h-6 mr-2 text-green-600" />
            Recommended for You
          </h2>
          <div className="space-y-4">
            {recommendedCourses.map((course, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
                <img
                  src={course.image}
                  alt={course.title}
                  className="w-16 h-12 object-cover rounded-lg"
                />
                <div className="flex-1">
                  <h3 className="font-medium text-gray-900 text-sm">{course.title}</h3>
                  <p className="text-xs text-gray-600">{course.instructor} • {course.duration}</p>
                  <div className="flex items-center space-x-2 mt-1">
                    <div className="flex items-center">
                      <Star className="w-3 h-3 text-yellow-400 fill-current" />
                      <span className="text-xs text-gray-600 ml-1">{course.rating}</span>
                    </div>
                    <span className="text-xs text-gray-500">({course.students} students)</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <Link
            to="/dashboard/education"
            className="block mt-4 text-center text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Browse all courses
          </Link>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            to="/dashboard/dev-tools"
            className="flex items-center space-x-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg hover:from-blue-100 hover:to-indigo-100 transition-colors group"
          >
            <Terminal className="w-8 h-8 text-blue-600 group-hover:scale-110 transition-transform" />
            <div>
              <p className="font-medium text-gray-900">Start Coding</p>
              <p className="text-sm text-gray-600">Open IDE</p>
            </div>
          </Link>

          <Link
            to="/dashboard/ai-assistant"
            className="flex items-center space-x-3 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg hover:from-purple-100 hover:to-pink-100 transition-colors group"
          >
            <Bot className="w-8 h-8 text-purple-600 group-hover:scale-110 transition-transform" />
            <div>
              <p className="font-medium text-gray-900">AI Assistant</p>
              <p className="text-sm text-gray-600">Get help</p>
            </div>
          </Link>

          <Link
            to="/dashboard/jobs"
            className="flex items-center space-x-3 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg hover:from-green-100 hover:to-emerald-100 transition-colors group"
          >
            <Briefcase className="w-8 h-8 text-green-600 group-hover:scale-110 transition-transform" />
            <div>
              <p className="font-medium text-gray-900">Find Jobs</p>
              <p className="text-sm text-gray-600">Browse opportunities</p>
            </div>
          </Link>

          <Link
            to="/dashboard/marketplace"
            className="flex items-center space-x-3 p-4 bg-gradient-to-r from-orange-50 to-red-50 rounded-lg hover:from-orange-100 hover:to-red-100 transition-colors group"
          >
            <ShoppingBag className="w-8 h-8 text-orange-600 group-hover:scale-110 transition-transform" />
            <div>
              <p className="font-medium text-gray-900">Marketplace</p>
              <p className="text-sm text-gray-600">Buy & sell</p>
            </div>
          </Link>
        </div>
      </div>

      {/* Platform Status */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Shield className="w-8 h-8 text-green-600" />
            <div>
              <h3 className="font-semibold text-green-900">Platform Status: All Systems Operational</h3>
              <p className="text-sm text-green-700">
                All services running smoothly with 99.9% uptime. Latest security updates applied.
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-green-700">Live</s
(Content truncated due to size limit. Use line ranges to read in chunks)