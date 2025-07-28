import React, { useState, useEffect } from 'react';
import {
  Menu,
  X,
  Users,
  ShoppingCart,
  GraduationCap,
  Briefcase,
  TrendingUp,
  Bot,
  Database,
  Cpu,
  Home,
  Search,
  Bell,
  User,
  Heart,
  MessageCircle,
  Share2,
  Camera,
  Video,
  Star,
  Filter,
  MapPin,
  Settings,
  LogOut,
  Activity,
  DollarSign,
  Shield,
  Globe,
  Zap,
  Calendar,
  Mail,
  Phone
} from 'lucide-react';

interface MobileAppProps {
  orientation: 'portrait' | 'landscape';
  deviceType: 'phone' | 'tablet';
}

const MobileApp: React.FC<MobileAppProps> = ({ orientation, deviceType }) => {
  const [currentView, setCurrentView] = useState('home');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [notifications, setNotifications] = useState(5);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Touch gesture handlers
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) {
      // Handle left swipe (next view)
      handleSwipeNavigation('next');
    }
    if (isRightSwipe) {
      // Handle right swipe (previous view)
      handleSwipeNavigation('prev');
    }
  };

  const handleSwipeNavigation = (direction: 'next' | 'prev') => {
    const views = ['home', 'social', 'marketplace', 'education', 'jobs', 'trading', 'ai-assistant'];
    const currentIndex = views.indexOf(currentView);
    
    if (direction === 'next' && currentIndex < views.length - 1) {
      setCurrentView(views[currentIndex + 1]);
    } else if (direction === 'prev' && currentIndex > 0) {
      setCurrentView(views[currentIndex - 1]);
    }
  };

  // Mobile-optimized navigation items
  const getNavigationItems = () => [
    { id: 'home', label: 'Home', icon: Home, color: 'blue' },
    { id: 'social', label: 'Social', icon: Users, color: 'green' },
    { id: 'marketplace', label: 'Shop', icon: ShoppingCart, color: 'orange' },
    { id: 'education', label: 'Learn', icon: GraduationCap, color: 'purple' },
    { id: 'jobs', label: 'Jobs', icon: Briefcase, color: 'indigo' },
    { id: 'trading', label: 'Trade', icon: TrendingUp, color: 'emerald' },
    { id: 'research', label: 'Research', icon: Database, color: 'red' },
    { id: 'ai-assistant', label: 'AI', icon: Bot, color: 'pink' },
    { id: 'manufacturing', label: 'Make', icon: Cpu, color: 'cyan' }
  ];

  // Mobile header with status bar
  const renderMobileHeader = () => (
    <div className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200">
      {/* Status bar */}
      <div className="flex items-center justify-between px-4 py-1 text-xs text-gray-600 bg-gray-50">
        <div className="flex items-center space-x-2">
          <span>9:41 AM</span>
          <div className="flex space-x-1">
            <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
            <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
            <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
          </div>
        </div>
        <div className="flex items-center space-x-1">
          <span>100%</span>
          <div className="w-6 h-3 border border-gray-400 rounded-sm">
            <div className="w-full h-full bg-green-500 rounded-sm"></div>
          </div>
        </div>
      </div>
      
      {/* App header */}
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsMenuOpen(true)}
            className="p-2 rounded-full hover:bg-gray-100 active:bg-gray-200"
          >
            <Menu size={20} />
          </button>
          <h1 className="text-lg font-bold text-gray-900 capitalize">
            {currentView.replace('-', ' ')}
          </h1>
        </div>
        
        <div className="flex items-center space-x-2">
          <button className="relative p-2 rounded-full hover:bg-gray-100 active:bg-gray-200">
            <Bell size={20} />
            {notifications > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                {notifications}
              </span>
            )}
          </button>
          
          <button className="p-2 rounded-full hover:bg-gray-100 active:bg-gray-200">
            <Search size={20} />
          </button>
          
          {isAuthenticated ? (
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-medium">
                {user?.first_name?.[0] || 'U'}
              </span>
            </div>
          ) : (
            <button className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
              Sign In
            </button>
          )}
        </div>
      </div>
    </div>
  );

  // Bottom navigation with haptic feedback simulation
  const renderBottomNavigation = () => (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="grid grid-cols-5 gap-1 p-2">
        {getNavigationItems().slice(0, 5).map((item) => {
          const IconComponent = item.icon;
          const isActive = currentView === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => {
                setCurrentView(item.id);
                // Simulate haptic feedback
                if (navigator.vibrate) {
                  navigator.vibrate(10);
                }
              }}
              className={`flex flex-col items-center p-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? `bg-${item.color}-100 text-${item.color}-600 scale-105`
                  : 'text-gray-600 hover:bg-gray-100 active:scale-95'
              }`}
            >
              <IconComponent size={20} />
              <span className="text-xs mt-1 font-medium">{item.label}</span>
              {isActive && (
                <div className={`w-1 h-1 bg-${item.color}-600 rounded-full mt-1`}></div>
              )}
            </button>
          );
        })}
      </div>
      
      {/* Home indicator for iPhone-style devices */}
      <div className="flex justify-center pb-2">
        <div className="w-32 h-1 bg-gray-300 rounded-full"></div>
      </div>
    </div>
  );

  // Slide-out menu
  const renderSlideMenu = () => (
    <div className={`fixed inset-0 z-60 transition-opacity duration-300 ${
      isMenuOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
    }`}>
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={() => setIsMenuOpen(false)} />
      <div className={`absolute left-0 top-0 bottom-0 w-80 bg-white transform transition-transform duration-300 ${
        isMenuOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="p-6">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-lg">U</span>
              </div>
              <div>
                <h2 className="text-lg font-bold text-gray-900">Unified Platform</h2>
                <p className="text-sm text-gray-500">Mobile App</p>
              </div>
            </div>
            <button
              onClick={() => setIsMenuOpen(false)}
              className="p-2 rounded-full hover:bg-gray-100"
            >
              <X size={20} />
            </button>
          </div>
          
          <nav className="space-y-2">
            {getNavigationItems().map((item) => {
              const IconComponent = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setCurrentView(item.id);
                    setIsMenuOpen(false);
                  }}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-colors ${
                    currentView === item.id
                      ? `bg-${item.color}-100 text-${item.color}-600`
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <IconComponent size={20} />
                  <span className="font-medium">{item.label}</span>
                </button>
              );
            })}
          </nav>
          
          <div className="mt-8 pt-8 border-t border-gray-200">
            <div className="space-y-2">
              <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-gray-100">
                <Settings size={20} />
                <span className="font-medium">Settings</span>
              </button>
              <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-gray-100">
                <User size={20} />
                <span className="font-medium">Profile</span>
              </button>
              {isAuthenticated && (
                <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-red-600 hover:bg-red-50">
                  <LogOut size={20} />
                  <span className="font-medium">Sign Out</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Main content with swipe gestures
  const renderMainContent = () => (
    <div 
      className="pt-24 pb-24 px-4"
      onTouchStart={onTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
    >
      {renderViewContent()}
    </div>
  );

  // View-specific content optimized for mobile
  const renderViewContent = () => {
    switch (currentView) {
      case 'home':
        return renderMobileHomeView();
      case 'social':
        return renderMobileSocialView();
      case 'marketplace':
        return renderMobileMarketplaceView();
      case 'education':
        return renderMobileEducationView();
      case 'jobs':
        return renderMobileJobsView();
      case 'trading':
        return renderMobileTradingView();
      case 'research':
        return renderMobileResearchView();
      case 'ai-assistant':
        return renderMobileAIAssistantView();
      case 'manufacturing':
        return renderMobileManufacturingView();
      default:
        return renderMobileHomeView();
    }
  };

  const renderMobileHomeView = () => (
    <div className="space-y-6">
      {/* Welcome card */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">Welcome Back!</h1>
        <p className="opacity-90 mb-4">Your unified digital ecosystem awaits</p>
        <div className="flex space-x-3">
          <div className="bg-white bg-opacity-20 px-3 py-1 rounded-full">
            <span className="text-sm">📱 Mobile Optimized</span>
          </div>
          <div className="bg-white bg-opacity-20 px-3 py-1 rounded-full">
            <span className="text-sm">🚀 Fast & Secure</span>
          </div>
        </div>
      </div>
      
      {/* Quick stats */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white rounded-2xl p-4 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="w-6 h-6 text-green-600" />
            <span className="text-green-600 text-sm font-medium">+12.5%</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">$62,981</p>
          <p className="text-sm text-gray-600">Portfolio</p>
        </div>
        
        <div className="bg-white rounded-2xl p-4 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <Users className="w-6 h-6 text-blue-600" />
            <span className="text-blue-600 text-sm font-medium">+234</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">12.5K</p>
          <p className="text-sm text-gray-600">Followers</p>
        </div>
      </div>
      
      {/* Quick actions */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 gap-4">
          {getNavigationItems().slice(1, 5).map((item) => {
            const IconComponent = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id)}
                className={`bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow active:scale-95`}
              >
                <IconComponent className={`w-8 h-8 text-${item.color}-600 mb-3`} />
                <h4 className="font-medium text-gray-900">{item.label}</h4>
                <p className="text-sm text-gray-600 mt-1">Tap to explore</p>
              </button>
            );
          })}
        </div>
      </div>
      
      {/* Recent activity */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {[
            { icon: TrendingUp, text: 'Trading bot earned $234', time: '2h ago', color: 'green' },
            { icon: Users, text: 'New follower: @techuser', time: '4h ago', color: 'blue' },
            { icon: GraduationCap, text: 'Course completed: AI Basics', time: '1d ago', color: 'purple' }
          ].map((activity, index) => (
            <div key={index} className="bg-white rounded-xl p-4 shadow-sm">
              <div className="flex items-start space-x-3">
                <div className={`w-10 h-10 bg-${activity.color}-100 rounded-full flex items-center justify-center`}>
                  <activity.icon className={`w-5 h-5 text-${activity.color}-600`} />
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{activity.text}</p>
                  <p className="text-sm text-gray-500">{activity.time}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderMobileSocialView = () => (
    <div className="space-y-4">
      {/* Create post */}
      <div className="bg-white rounded-2xl p-4 shadow-sm">
        <div className="flex items-start space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white font-medium">U</span>
          </div>
          <div className="flex-1">
            <textarea
              placeholder="What's on your mind?"
              className="w-full p-3 border border-gray-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
            <div className="flex items-center justify-between mt-3">
              <div className="flex space-x-4">
                <button className="flex items-center space-x-2 text-gray-600 active:scale-95">
                  <Camera size={18} />
                  <span className="text-sm">Photo</span>
                </button>
                <button className="flex items-center space-x-2 text-gray-600 active:scale-95">

(Content truncated due to size limit. Use line ranges to read in chunks)