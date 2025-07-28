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
  Phone,
  Grid3X3,
  List,
  MoreHorizontal,
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Minimize2
} from 'lucide-react';

interface TabletAppProps {
  orientation: 'portrait' | 'landscape';
  screenSize: {
    width: number;
    height: number;
  };
}

const TabletApp: React.FC<TabletAppProps> = ({ orientation, screenSize }) => {
  const [currentView, setCurrentView] = useState('home');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [notifications, setNotifications] = useState(8);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [splitView, setSplitView] = useState(false);
  const [secondaryView, setSecondaryView] = useState<string | null>(null);

  // Tablet-specific dimensions
  const isLandscape = orientation === 'landscape';
  const sidebarWidth = sidebarCollapsed ? 80 : 280;
  const contentWidth = splitView ? (screenSize.width - sidebarWidth) / 2 : screenSize.width - sidebarWidth;

  // Navigation items optimized for tablet
  const getNavigationItems = () => [
    { id: 'home', label: 'Home', icon: Home, color: 'blue', category: 'main' },
    { id: 'dashboard', label: 'Dashboard', icon: Activity, color: 'indigo', category: 'main' },
    { id: 'social', label: 'Social Network', icon: Users, color: 'green', category: 'social' },
    { id: 'marketplace', label: 'Marketplace', icon: ShoppingCart, color: 'orange', category: 'commerce' },
    { id: 'education', label: 'Education Hub', icon: GraduationCap, color: 'purple', category: 'learning' },
    { id: 'jobs', label: 'Job Marketplace', icon: Briefcase, color: 'indigo', category: 'career' },
    { id: 'trading', label: 'Trading Platform', icon: TrendingUp, color: 'emerald', category: 'finance' },
    { id: 'research', label: 'R&D Laboratory', icon: Database, color: 'red', category: 'research' },
    { id: 'ai-assistant', label: 'AI Assistant', icon: Bot, color: 'pink', category: 'ai' },
    { id: 'manufacturing', label: 'Manufacturing', icon: Cpu, color: 'cyan', category: 'iot' },
    { id: 'metaverse', label: 'Metaverse', icon: Globe, color: 'violet', category: 'virtual' },
    { id: 'blockchain', label: 'Blockchain', icon: Shield, color: 'amber', category: 'crypto' }
  ];

  // Tablet sidebar with categories
  const renderTabletSidebar = () => (
    <div className={`fixed left-0 top-0 bottom-0 bg-white border-r border-gray-200 z-40 transition-all duration-300 ${
      sidebarCollapsed ? 'w-20' : 'w-70'
    }`}>
      <div className="p-4">
        {/* Logo and brand */}
        <div className={`flex items-center mb-8 ${sidebarCollapsed ? 'justify-center' : 'space-x-3'}`}>
          <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-lg">U</span>
          </div>
          {!sidebarCollapsed && (
            <div>
              <h1 className="text-lg font-bold text-gray-900">Unified Platform</h1>
              <p className="text-xs text-gray-500">Tablet Experience</p>
            </div>
          )}
        </div>
        
        {/* Collapse toggle */}
        <button
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          className="absolute top-4 right-4 p-2 rounded-lg hover:bg-gray-100"
        >
          {sidebarCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
        
        {/* Navigation */}
        <nav className="space-y-1">
          {getNavigationItems().map((item) => {
            const IconComponent = item.icon;
            const isActive = currentView === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id)}
                className={`w-full flex items-center rounded-xl transition-all duration-200 ${
                  sidebarCollapsed ? 'justify-center p-3' : 'space-x-3 px-4 py-3'
                } ${
                  isActive
                    ? `bg-${item.color}-100 text-${item.color}-600`
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
                title={sidebarCollapsed ? item.label : undefined}
              >
                <IconComponent size={20} />
                {!sidebarCollapsed && (
                  <span className="font-medium text-sm">{item.label}</span>
                )}
                {!sidebarCollapsed && isActive && (
                  <div className={`w-2 h-2 bg-${item.color}-600 rounded-full ml-auto`}></div>
                )}
              </button>
            );
          })}
        </nav>
        
        {/* User section */}
        {!sidebarCollapsed && (
          <div className="absolute bottom-4 left-4 right-4">
            <div className="border-t border-gray-200 pt-4">
              {isAuthenticated ? (
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium">
                      {user?.first_name?.[0] || 'U'}
                    </span>
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900 text-sm">
                      {user?.first_name || 'User'}
                    </p>
                    <p className="text-xs text-gray-500">Premium Account</p>
                  </div>
                  <button className="p-2 rounded-lg hover:bg-gray-100">
                    <Settings size={16} />
                  </button>
                </div>
              ) : (
                <button className="w-full bg-blue-600 text-white py-3 rounded-xl font-medium">
                  Sign In
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );

  // Tablet header with enhanced controls
  const renderTabletHeader = () => (
    <div className={`fixed top-0 bg-white border-b border-gray-200 z-30 transition-all duration-300 ${
      sidebarCollapsed ? 'left-20' : 'left-70'
    } right-0`}>
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center space-x-4">
          <h2 className="text-xl font-semibold text-gray-900 capitalize">
            {currentView.replace('-', ' ')}
          </h2>
          
          {/* View mode toggles */}
          <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'grid' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
              }`}
            >
              <Grid3X3 size={16} />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'list' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
              }`}
            >
              <List size={16} />
            </button>
          </div>
          
          {/* Split view toggle */}
          <button
            onClick={() => setSplitView(!splitView)}
            className={`p-2 rounded-lg transition-colors ${
              splitView ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'
            }`}
            title="Split View"
          >
            {splitView ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
          </button>
        </div>
        
        <div className="flex items-center space-x-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-3 text-gray-400" size={16} />
            <input
              type="text"
              placeholder="Search..."
              className="pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-64"
            />
          </div>
          
          {/* Notifications */}
          <button className="relative p-2 rounded-lg hover:bg-gray-100">
            <Bell size={20} />
            {notifications > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                {notifications > 9 ? '9+' : notifications}
              </span>
            )}
          </button>
          
          {/* User menu */}
          {isAuthenticated ? (
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">
                  {user?.first_name?.[0] || 'U'}
                </span>
              </div>
              <span className="text-sm font-medium text-gray-700">
                {user?.first_name || 'User'}
              </span>
              <button className="p-1 rounded hover:bg-gray-100">
                <MoreHorizontal size={16} />
              </button>
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

  // Main content area with split view support
  const renderMainContent = () => (
    <div className={`transition-all duration-300 ${
      sidebarCollapsed ? 'pl-20' : 'pl-70'
    } pt-20`}>
      {splitView ? (
        <div className="flex h-screen">
          <div className="flex-1 border-r border-gray-200 overflow-y-auto">
            <div className="p-6">
              {renderViewContent(currentView)}
            </div>
          </div>
          <div className="flex-1 overflow-y-auto">
            <div className="p-6">
              {secondaryView ? renderViewContent(secondaryView) : renderSecondaryViewSelector()}
            </div>
          </div>
        </div>
      ) : (
        <div className="p-6 overflow-y-auto">
          {renderViewContent(currentView)}
        </div>
      )}
    </div>
  );

  // Secondary view selector for split view
  const renderSecondaryViewSelector = () => (
    <div className="text-center py-12">
      <div className="text-6xl mb-4">📱</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Select Secondary View</h3>
      <p className="text-gray-600 mb-6">Choose a view to display alongside the main content</p>
      <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
        {getNavigationItems().slice(0, 6).map((item) => {
          const IconComponent = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => setSecondaryView(item.id)}
              className={`p-4 border border-gray-200 rounded-xl hover:border-${item.color}-300 hover:bg-${item.color}-50 transition-colors`}
            >
              <IconComponent className={`w-6 h-6 text-${item.color}-600 mx-auto mb-2`} />
              <span className="text-sm font-medium text-gray-900">{item.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );

  // View content renderer
  const renderViewContent = (view: string) => {
    switch (view) {
      case 'home':
        return renderTabletHomeView();
      case 'dashboard':
        return renderTabletDashboardView();
      case 'social':
        return renderTabletSocialView();
      case 'marketplace':
        return renderTabletMarketplaceView();
      case 'education':
        return renderTabletEducationView();
      case 'jobs':
        return renderTabletJobsView();
      case 'trading':
        return renderTabletTradingView();
      case 'research':
        return renderTabletResearchView();
      case 'ai-assistant':
        return renderTabletAIAssistantView();
      case 'manufacturing':
        return renderTabletManufacturingView();
      case 'metaverse':
        return renderTabletMetaverseView();
      case 'blockchain':
        return renderTabletBlockchainView();
      default:
        return renderTabletHomeView();
    }
  };

  // Tablet-optimized view components
  const renderTabletHomeView = () => (
    <div className="space-y-8">
      {/* Hero section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-3">Welcome to Unified Platform</h1>
            <p className="text-lg opacity-90 mb-6">
              Your complete digital ecosystem optimized for tablet experience
            </p>
            <div className="flex space-x-4">
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="text-sm font-medium">📱 Tablet Optimized</span>
              </div>
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="text-sm font-medium">🚀 High Performance</span>
              </div>
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="text-sm font-medium">🔒 Secure</span>
              </div>
            </div>
          </div>
          <div className="text-8xl opacity-20">🚀</div>
        </div>
      </div>
      
      {/* Quick stats */}
      <div className={`grid gap-6 ${viewMode === 'grid' ? 'grid-cols-4' : 'grid-cols-2'}`}>
        {[
          { label: 'Portfolio Value', value: '$62,981', change: '+12.5%', icon: TrendingUp, color: 'green' },
          { label: 'Social Followers', value: '12.5K', change: '+234', icon: Users, color: 'blue' },
          { label: 'Courses Completed', value: '8', change: '+2', icon: GraduationCap, color: 'purple' },
          { label: 'Products Sold', value: '156', change: '+23', icon: ShoppingCart, color: 'orange' }
        ].map((stat) => (
          <div key={stat.label} className="bg-white rounded-2xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <stat.icon className={`w-8 h-8 text-${stat.color}-600`} />
              <span className={`text-${stat.color}-600 text-sm font-medium`}>
                {stat.change}
              </span>
            </div>
            <p className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</p>
            <p className="text-sm text-gray-600">{stat.label}</p>
          </div>
        ))}
      </div>
      
      {/* Platform modules */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-semibold text-gray-900">Platform Modules</h3>
          <button className="text-blue-600 hover:text-blue-700 font-medium">
            View All →
          </button>
        </div>
        <div className={`grid gap-6 ${
          viewMode === 'grid' 
            ? (isLandscape ? 'grid-cols-4' : 'grid-cols-3')
            : 'grid-cols-1'
        }`}>
          {getNavigationItems().slice(1).map((item) => {
            const IconComponent = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id)}
                className={`bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-200 text-left ${
                  viewMode === 'list' ? 'flex items-center space-x-4' : ''
                }`}
(Content truncated due to size limit. Use line ranges to read in chunks)