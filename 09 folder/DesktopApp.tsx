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
  Minimize2,
  Monitor,
  Sidebar,
  Layout,
  PanelLeft,
  PanelRight,
  Split,
  Fullscreen,
  Download,
  Upload,
  RefreshCw,
  HelpCircle,
  Bookmark,
  Archive,
  Trash2,
  Edit,
  Copy,
  ExternalLink
} from 'lucide-react';

interface DesktopAppProps {
  screenSize: {
    width: number;
    height: number;
  };
}

const DesktopApp: React.FC<DesktopAppProps> = ({ screenSize }) => {
  const [currentView, setCurrentView] = useState('home');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [notifications, setNotifications] = useState(12);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list' | 'kanban'>('grid');
  const [layoutMode, setLayoutMode] = useState<'single' | 'split' | 'triple'>('single');
  const [secondaryView, setSecondaryView] = useState<string | null>(null);
  const [tertiaryView, setTertiaryView] = useState<string | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [activeWorkspace, setActiveWorkspace] = useState('main');
  const [openWindows, setOpenWindows] = useState<string[]>(['home']);

  // Desktop-specific dimensions
  const isLargeScreen = screenSize.width >= 1440;
  const isUltraWide = screenSize.width >= 1920;
  const sidebarWidth = sidebarCollapsed ? 80 : 320;

  // Workspaces for desktop productivity
  const workspaces = [
    { id: 'main', label: 'Main', icon: Home },
    { id: 'productivity', label: 'Productivity', icon: Briefcase },
    { id: 'creative', label: 'Creative', icon: Camera },
    { id: 'analytics', label: 'Analytics', icon: Activity },
    { id: 'development', label: 'Development', icon: Cpu }
  ];

  // Enhanced navigation with categories
  const getNavigationItems = () => [
    // Core
    { id: 'home', label: 'Home', icon: Home, color: 'blue', category: 'core', hotkey: 'Ctrl+H' },
    { id: 'dashboard', label: 'Dashboard', icon: Activity, color: 'indigo', category: 'core', hotkey: 'Ctrl+D' },
    
    // Social & Communication
    { id: 'social', label: 'Social Network', icon: Users, color: 'green', category: 'social', hotkey: 'Ctrl+S' },
    { id: 'messages', label: 'Messages', icon: MessageCircle, color: 'blue', category: 'social', hotkey: 'Ctrl+M' },
    { id: 'calendar', label: 'Calendar', icon: Calendar, color: 'purple', category: 'social', hotkey: 'Ctrl+L' },
    
    // Commerce & Finance
    { id: 'marketplace', label: 'Marketplace', icon: ShoppingCart, color: 'orange', category: 'commerce', hotkey: 'Ctrl+P' },
    { id: 'trading', label: 'Trading Platform', icon: TrendingUp, color: 'emerald', category: 'finance', hotkey: 'Ctrl+T' },
    { id: 'wallet', label: 'Digital Wallet', icon: DollarSign, color: 'green', category: 'finance', hotkey: 'Ctrl+W' },
    
    // Learning & Career
    { id: 'education', label: 'Education Hub', icon: GraduationCap, color: 'purple', category: 'learning', hotkey: 'Ctrl+E' },
    { id: 'jobs', label: 'Job Marketplace', icon: Briefcase, color: 'indigo', category: 'career', hotkey: 'Ctrl+J' },
    
    // Research & Development
    { id: 'research', label: 'R&D Laboratory', icon: Database, color: 'red', category: 'research', hotkey: 'Ctrl+R' },
    { id: 'ai-assistant', label: 'AI Assistant', icon: Bot, color: 'pink', category: 'ai', hotkey: 'Ctrl+A' },
    
    // Technology & Innovation
    { id: 'manufacturing', label: 'Manufacturing', icon: Cpu, color: 'cyan', category: 'iot', hotkey: 'Ctrl+F' },
    { id: 'metaverse', label: 'Metaverse', icon: Globe, color: 'violet', category: 'virtual', hotkey: 'Ctrl+V' },
    { id: 'blockchain', label: 'Blockchain', icon: Shield, color: 'amber', category: 'crypto', hotkey: 'Ctrl+B' },
    
    // Tools & Settings
    { id: 'settings', label: 'Settings', icon: Settings, color: 'gray', category: 'tools', hotkey: 'Ctrl+,' },
    { id: 'help', label: 'Help & Support', icon: HelpCircle, color: 'blue', category: 'tools', hotkey: 'F1' }
  ];

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyboard = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        const items = getNavigationItems();
        const item = items.find(item => 
          item.hotkey === `${e.ctrlKey ? 'Ctrl' : 'Cmd'}+${e.key.toUpperCase()}`
        );
        if (item) {
          e.preventDefault();
          setCurrentView(item.id);
        }
      }
      
      // Function keys
      if (e.key === 'F1') {
        e.preventDefault();
        setCurrentView('help');
      }
    };

    window.addEventListener('keydown', handleKeyboard);
    return () => window.removeEventListener('keydown', handleKeyboard);
  }, []);

  // Desktop sidebar with advanced features
  const renderDesktopSidebar = () => (
    <div className={`fixed left-0 top-0 bottom-0 bg-white border-r border-gray-200 z-40 transition-all duration-300 ${
      sidebarCollapsed ? 'w-20' : 'w-80'
    }`}>
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="p-6 border-b border-gray-100">
          <div className={`flex items-center ${sidebarCollapsed ? 'justify-center' : 'space-x-3'}`}>
            <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-lg">U</span>
            </div>
            {!sidebarCollapsed && (
              <div className="flex-1">
                <h1 className="text-xl font-bold text-gray-900">Unified Platform</h1>
                <p className="text-sm text-gray-500">Desktop Experience</p>
              </div>
            )}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="p-2 rounded-lg hover:bg-gray-100"
              title={sidebarCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
            >
              {sidebarCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
            </button>
          </div>
        </div>
        
        {/* Workspaces */}
        {!sidebarCollapsed && (
          <div className="p-4 border-b border-gray-100">
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Workspaces
            </h3>
            <div className="flex space-x-2">
              {workspaces.map((workspace) => {
                const IconComponent = workspace.icon;
                return (
                  <button
                    key={workspace.id}
                    onClick={() => setActiveWorkspace(workspace.id)}
                    className={`flex-1 p-2 rounded-lg text-xs font-medium transition-colors ${
                      activeWorkspace === workspace.id
                        ? 'bg-blue-100 text-blue-600'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                    title={workspace.label}
                  >
                    <IconComponent size={16} className="mx-auto mb-1" />
                    {workspace.label}
                  </button>
                );
              })}
            </div>
          </div>
        )}
        
        {/* Navigation */}
        <div className="flex-1 overflow-y-auto p-4">
          {!sidebarCollapsed ? (
            <div className="space-y-6">
              {Object.entries(
                getNavigationItems().reduce((acc, item) => {
                  if (!acc[item.category]) acc[item.category] = [];
                  acc[item.category].push(item);
                  return acc;
                }, {} as Record<string, any>)
              ).map(([category, items]) => (
                <div key={category}>
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                    {category}
                  </h3>
                  <div className="space-y-1">
                    {items.map((item) => {
                      const IconComponent = item.icon;
                      const isActive = currentView === item.id;
                      const isOpen = openWindows.includes(item.id);
                      
                      return (
                        <div key={item.id} className="group relative">
                          <button
                            onClick={() => setCurrentView(item.id)}
                            onContextMenu={(e) => {
                              e.preventDefault();
                              // Context menu logic
                            }}
                            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-all duration-200 ${
                              isActive
                                ? `bg-${item.color}-100 text-${item.color}-600`
                                : 'text-gray-700 hover:bg-gray-100'
                            }`}
                          >
                            <IconComponent size={18} />
                            <span className="font-medium text-sm flex-1 text-left">{item.label}</span>
                            {isOpen && (
                              <div className={`w-2 h-2 bg-${item.color}-600 rounded-full`}></div>
                            )}
                          </button>
                          
                          {/* Hotkey tooltip */}
                          <div className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <span className="text-xs text-gray-400">{item.hotkey}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              {getNavigationItems().map((item) => {
                const IconComponent = item.icon;
                const isActive = currentView === item.id;
                
                return (
                  <button
                    key={item.id}
                    onClick={() => setCurrentView(item.id)}
                    className={`w-full p-3 rounded-lg transition-colors ${
                      isActive
                        ? `bg-${item.color}-100 text-${item.color}-600`
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                    title={`${item.label} (${item.hotkey})`}
                  >
                    <IconComponent size={20} />
                  </button>
                );
              })}
            </div>
          )}
        </div>
        
        {/* User section */}
        <div className="p-4 border-t border-gray-100">
          {!sidebarCollapsed ? (
            <div>
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
                  <div className="flex space-x-1">
                    <button className="p-1 rounded hover:bg-gray-100" title="Settings">
                      <Settings size={14} />
                    </button>
                    <button className="p-1 rounded hover:bg-gray-100" title="Sign Out">
                      <LogOut size={14} />
                    </button>
                  </div>
                </div>
              ) : (
                <button className="w-full bg-blue-600 text-white py-3 rounded-xl font-medium hover:bg-blue-700">
                  Sign In
                </button>
              )}
            </div>
          ) : (
            <div className="text-center">
              {isAuthenticated ? (
                <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center mx-auto">
                  <span className="text-white font-medium">
                    {user?.first_name?.[0] || 'U'}
                  </span>
                </div>
              ) : (
                <button className="w-10 h-10 bg-blue-600 text-white rounded-full hover:bg-blue-700">
                  <User size={16} />
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );

  // Advanced desktop header with toolbar
  const renderDesktopHeader = () => (
    <div className={`fixed top-0 bg-white border-b border-gray-200 z-30 transition-all duration-300 ${
      sidebarCollapsed ? 'left-20' : 'left-80'
    } right-0`}>
      <div className="flex items-center justify-between px-6 py-3">
        <div className="flex items-center space-x-6">
          {/* Breadcrumb */}
          <div className="flex items-center space-x-2 text-sm">
            <span className="text-gray-500">Workspace</span>
            <ChevronRight size={14} className="text-gray-400" />
            <span className="text-gray-500 capitalize">{activeWorkspace}</span>
            <ChevronRight size={14} className="text-gray-400" />
            <span className="font-medium text-gray-900 capitalize">
              {currentView.replace('-', ' ')}
            </span>
          </div>
          
          {/* View controls */}
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded-md transition-colors ${
                  viewMode === 'grid' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
                }`}
                title="Grid View"
              >
                <Grid3X3 size={14} />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded-md transition-colors ${
                  viewMode === 'list' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
                }`}
                title="List View"
              >
                <List size={14} />
              </button>
              <button
                onClick={() => setViewMode('kanban')}
                className={`p-2 rounded-md transition-colors ${
                  viewMode === 'kanban' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
                }`}
                title="Kanban View"
              >
                <Layout size={14} />
              </button>
            </div>
            
            {/* Layout controls */}
            <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setLayoutMode('single')}
                className={`p-2 rounded-md transition-colors ${
                  layoutMode === 'single' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
                }`}
                title="Single View"
              >
                <Monitor size={14} />
              </button>
              <button
                onClick={() => setLayoutMode('split')}
                className={`p-2 rounded-md transition-colors 
(Content truncated due to size limit. Use line ranges to read in chunks)