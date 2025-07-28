import React, { useState, useEffect } from 'react';
import {
  Menu,
  X,
  Users,
  Shield,
  Cpu,
  Database,
  Briefcase,
  ShoppingCart,
  TrendingUp,
  Bot,
  GraduationCap,
  User,
  LogIn,
  LogOut,
  Search,
  Heart,
  Share2,
  Star,
  Eye,
  EyeOff,
  DollarSign,
  MessageCircle,
  Video,
  Camera,
  Filter,
  MapPin,
  Smartphone,
  Tablet,
  Monitor,
  Globe,
  Wifi,
  Download,
  Settings,
  Bell,
  Home,
  Calendar,
  Mail,
  Phone,
  Zap,
  Activity
} from 'lucide-react';

interface CrossPlatformAppProps {
  platform: 'web' | 'mobile' | 'tablet' | 'desktop';
  deviceType: 'phone' | 'tablet' | 'laptop' | 'desktop' | 'tv';
  orientation: 'portrait' | 'landscape';
  screenSize: {
    width: number;
    height: number;
  };
}

const CrossPlatformApp: React.FC<CrossPlatformAppProps> = ({
  platform,
  deviceType,
  orientation,
  screenSize
}) => {
  const [currentView, setCurrentView] = useState('home');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [notifications, setNotifications] = useState(12);

  // Responsive breakpoints
  const isMobile = screenSize.width < 768;
  const isTablet = screenSize.width >= 768 && screenSize.width < 1024;
  const isDesktop = screenSize.width >= 1024;
  const isLargeScreen = screenSize.width >= 1440;

  // Platform-specific styling
  const getPlatformStyles = () => {
    const baseStyles = "min-h-screen bg-gray-50";
    
    switch (platform) {
      case 'mobile':
        return `${baseStyles} mobile-app touch-optimized`;
      case 'tablet':
        return `${baseStyles} tablet-app touch-optimized`;
      case 'desktop':
        return `${baseStyles} desktop-app mouse-optimized`;
      default:
        return `${baseStyles} web-app responsive`;
    }
  };

  // Navigation items based on platform
  const getNavigationItems = () => {
    const allItems = [
      { id: 'home', label: 'Home', icon: Home },
      { id: 'dashboard', label: 'Dashboard', icon: Activity },
      { id: 'social', label: 'Social', icon: Users },
      { id: 'marketplace', label: 'Shop', icon: ShoppingCart },
      { id: 'education', label: 'Learn', icon: GraduationCap },
      { id: 'jobs', label: 'Jobs', icon: Briefcase },
      { id: 'trading', label: 'Trading', icon: TrendingUp },
      { id: 'research', label: 'Research', icon: Database },
      { id: 'ai-assistant', label: 'AI', icon: Bot },
      { id: 'manufacturing', label: 'Make', icon: Cpu },
      { id: 'metaverse', label: 'Metaverse', icon: Globe },
      { id: 'blockchain', label: 'Blockchain', icon: Shield }
    ];

    // Limit items on mobile
    if (isMobile) {
      return allItems.slice(0, 8);
    }
    
    return allItems;
  };

  // Render mobile navigation
  const renderMobileNavigation = () => (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="grid grid-cols-5 gap-1 p-2">
        {getNavigationItems().slice(0, 5).map((item) => {
          const IconComponent = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`flex flex-col items-center p-2 rounded-lg transition-colors ${
                currentView === item.id
                  ? 'bg-blue-100 text-blue-600'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <IconComponent size={20} />
              <span className="text-xs mt-1">{item.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );

  // Render tablet navigation
  const renderTabletNavigation = () => (
    <div className="fixed left-0 top-0 bottom-0 w-20 bg-white border-r border-gray-200 z-40">
      <div className="flex flex-col items-center py-4 space-y-4">
        <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center">
          <span className="text-white font-bold text-lg">U</span>
        </div>
        {getNavigationItems().map((item) => {
          const IconComponent = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`w-12 h-12 rounded-xl flex items-center justify-center transition-colors ${
                currentView === item.id
                  ? 'bg-blue-100 text-blue-600'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
              title={item.label}
            >
              <IconComponent size={20} />
            </button>
          );
        })}
      </div>
    </div>
  );

  // Render desktop navigation
  const renderDesktopNavigation = () => (
    <div className="fixed left-0 top-0 bottom-0 w-64 bg-white border-r border-gray-200 z-40">
      <div className="p-6">
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold">U</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">Unified Platform</h1>
            <p className="text-sm text-gray-500">World-Class Digital Infrastructure</p>
          </div>
        </div>
        
        <nav className="space-y-2">
          {getNavigationItems().map((item) => {
            const IconComponent = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  currentView === item.id
                    ? 'bg-blue-100 text-blue-600'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <IconComponent size={20} />
                <span className="font-medium">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );

  // Render top header
  const renderHeader = () => (
    <div className={`fixed top-0 right-0 bg-white border-b border-gray-200 z-30 ${
      isDesktop ? 'left-64' : isTablet ? 'left-20' : 'left-0'
    }`}>
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center space-x-4">
          {isMobile && (
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-lg hover:bg-gray-100"
            >
              <Menu size={20} />
            </button>
          )}
          <h2 className="text-lg font-semibold text-gray-900 capitalize">
            {currentView.replace('-', ' ')}
          </h2>
        </div>
        
        <div className="flex items-center space-x-3">
          <button className="relative p-2 rounded-lg hover:bg-gray-100">
            <Bell size={20} />
            {notifications > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                {notifications > 9 ? '9+' : notifications}
              </span>
            )}
          </button>
          
          <button className="p-2 rounded-lg hover:bg-gray-100">
            <Search size={20} />
          </button>
          
          {isAuthenticated ? (
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">
                  {user?.first_name?.[0] || 'U'}
                </span>
              </div>
              {!isMobile && (
                <span className="text-sm font-medium text-gray-700">
                  {user?.first_name || 'User'}
                </span>
              )}
            </div>
          ) : (
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
              Sign In
            </button>
          )}
        </div>
      </div>
    </div>
  );

  // Render main content area
  const renderMainContent = () => {
    const contentPadding = isDesktop ? 'pl-64' : isTablet ? 'pl-20' : 'pl-0';
    const topPadding = 'pt-16';
    const bottomPadding = isMobile ? 'pb-20' : 'pb-0';
    
    return (
      <div className={`${contentPadding} ${topPadding} ${bottomPadding}`}>
        <div className="p-4">
          {renderViewContent()}
        </div>
      </div>
    );
  };

  // Render view-specific content
  const renderViewContent = () => {
    switch (currentView) {
      case 'home':
        return renderHomeView();
      case 'dashboard':
        return renderDashboardView();
      case 'social':
        return renderSocialView();
      case 'marketplace':
        return renderMarketplaceView();
      case 'education':
        return renderEducationView();
      case 'jobs':
        return renderJobsView();
      case 'trading':
        return renderTradingView();
      case 'research':
        return renderResearchView();
      case 'ai-assistant':
        return renderAIAssistantView();
      case 'manufacturing':
        return renderManufacturingView();
      case 'metaverse':
        return renderMetaverseView();
      case 'blockchain':
        return renderBlockchainView();
      default:
        return renderHomeView();
    }
  };

  // View components
  const renderHomeView = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">Welcome to Unified Platform</h1>
        <p className="opacity-90">Your complete digital ecosystem for social media, e-commerce, education, and more.</p>
      </div>
      
      <div className={`grid gap-4 ${
        isMobile ? 'grid-cols-2' : isTablet ? 'grid-cols-3' : 'grid-cols-4'
      }`}>
        {getNavigationItems().slice(1).map((item) => {
          const IconComponent = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className="bg-white p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow"
            >
              <IconComponent className="w-8 h-8 text-blue-600 mb-2" />
              <h3 className="font-medium text-gray-900">{item.label}</h3>
            </button>
          );
        })}
      </div>
    </div>
  );

  const renderDashboardView = () => (
    <div className="space-y-6">
      <div className={`grid gap-4 ${
        isMobile ? 'grid-cols-1' : isTablet ? 'grid-cols-2' : 'grid-cols-4'
      }`}>
        <div className="bg-white p-4 rounded-xl shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Portfolio Value</p>
              <p className="text-2xl font-bold text-gray-900">$62,981</p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-600" />
          </div>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Social Followers</p>
              <p className="text-2xl font-bold text-gray-900">12.5K</p>
            </div>
            <Users className="w-8 h-8 text-blue-600" />
          </div>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Courses</p>
              <p className="text-2xl font-bold text-gray-900">8</p>
            </div>
            <GraduationCap className="w-8 h-8 text-purple-600" />
          </div>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Products Sold</p>
              <p className="text-2xl font-bold text-gray-900">156</p>
            </div>
            <ShoppingCart className="w-8 h-8 text-orange-600" />
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <p className="font-medium">Trading bot generated $234 profit</p>
              <p className="text-sm text-gray-500">2 hours ago</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
              <Users className="w-4 h-4 text-green-600" />
            </div>
            <div>
              <p className="font-medium">New follower on social media</p>
              <p className="text-sm text-gray-500">4 hours ago</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderSocialView = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm p-4">
        <textarea
          placeholder="What's on your mind?"
          className="w-full p-3 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={3}
        />
        <div className="flex items-center justify-between mt-3">
          <div className="flex space-x-3">
            <button className="flex items-center space-x-2 text-gray-600 hover:text-blue-600">
              <Camera size={16} />
              <span className="text-sm">Photo</span>
            </button>
            <button className="flex items-center space-x-2 text-gray-600 hover:text-blue-600">
              <Video size={16} />
              <span className="text-sm">Video</span>
            </button>
          </div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
            Post
          </button>
        </div>
      </div>
      
      <div className="space-y-4">
        {[1, 2, 3].map((post) => (
          <div key={post} className="bg-white rounded-xl shadow-sm p-4">
            <div className="flex items-start space-x-3">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white font-medium">U</span>
              </div>
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <h4 className="font-medium">Demo User</h4>
                  <span className="text-sm text-gray-500">2h ago</span>
                </div>
                <p className="text-gray-800 mb-3">
                  Just launched my new project on the Unified Platform! The integration is amazing.
                </p>
                <div className="flex items-center space-x-4 text-gray-500">
                  <button className="flex items-center space-x-1 hover:text-red-600">
                    <Heart size={16} />
                    <span className="text-sm">24</span>
                  </button>
                  <button className="flex items-center space-x-1 hover:text-blue-600">
                    <MessageCircle size={16} />
                    <span className="text-sm">8</span>
                  </button>
                  <button className="flex items-center space-x-1 hover:text-green-600">
                    <Share2 size={16} />
                    <span className=
(Content truncated due to size limit. Use line ranges to read in chunks)