import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';

interface MenuItem {
  id: string;
  label?: string;
  icon?: string;
  href?: string;
  onClick?: () => void;
  children?: MenuItem[];
  badge?: string | number;
  disabled?: boolean;
  divider?: boolean;
  description?: string;
}

interface CascadingMenuProps {
  items: MenuItem[];
  trigger: React.ReactNode;
  position?: 'bottom-left' | 'bottom-right' | 'top-left' | 'top-right';
  className?: string;
  onItemClick?: (item: MenuItem) => void;
}

const CascadingMenu: React.FC<CascadingMenuProps> = ({
  items,
  trigger,
  position = 'bottom-left',
  className = '',
  onItemClick
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeSubmenu, setActiveSubmenu] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const submenuTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setActiveSubmenu(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      if (submenuTimeoutRef.current) {
        clearTimeout(submenuTimeoutRef.current);
      }
    };
  }, []);

  const handleItemClick = (item: MenuItem) => {
    if (item.disabled) return;
    
    if (item.children && item.children.length > 0) {
      setActiveSubmenu(activeSubmenu === item.id ? null : item.id);
    } else {
      if (item.onClick) {
        item.onClick();
      }
      if (onItemClick) {
        onItemClick(item);
      }
      setIsOpen(false);
      setActiveSubmenu(null);
    }
  };

  const handleSubmenuEnter = (itemId: string) => {
    if (submenuTimeoutRef.current) {
      clearTimeout(submenuTimeoutRef.current);
    }
    setActiveSubmenu(itemId);
  };

  const handleSubmenuLeave = () => {
    submenuTimeoutRef.current = setTimeout(() => {
      setActiveSubmenu(null);
    }, 300);
  };

  const getPositionClasses = () => {
    switch (position) {
      case 'bottom-right':
        return 'top-full right-0';
      case 'top-left':
        return 'bottom-full left-0';
      case 'top-right':
        return 'bottom-full right-0';
      default:
        return 'top-full left-0';
    }
  };

  const renderMenuItem = (item: MenuItem, level: number = 0) => {
    const hasChildren = item.children && item.children.length > 0;
    const isActive = activeSubmenu === item.id;

    if (item.divider) {
      return (
        <div key={item.id} className="border-t border-gray-200 dark:border-gray-700 my-1" />
      );
    }

    return (
      <div
        key={item.id}
        className="relative"
        onMouseEnter={() => hasChildren && handleSubmenuEnter(item.id)}
        onMouseLeave={() => hasChildren && handleSubmenuLeave()}
      >
        <button
          className={`
            w-full flex items-center justify-between px-4 py-2 text-left text-sm
            transition-colors duration-150 ease-in-out
            ${item.disabled 
              ? 'text-gray-400 dark:text-gray-600 cursor-not-allowed' 
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
            }
            ${isActive ? 'bg-gray-100 dark:bg-gray-800' : ''}
          `}
          onClick={() => handleItemClick(item)}
          disabled={item.disabled}
        >
          <div className="flex items-center space-x-3">
            {item.icon && (
              <span className="text-gray-500 dark:text-gray-400">
                {item.icon}
              </span>
            )}
            <div className="flex-1">
              <div className="font-medium">{item.label || ''}</div>
              {item.description && (
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {item.description}
                </div>
              )}
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            {item.badge && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                {item.badge}
              </span>
            )}
            {hasChildren && (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            )}
          </div>
        </button>

        {/* Submenu */}
        {hasChildren && isActive && (
          <div className="absolute left-full top-0 ml-1 w-64 bg-white dark:bg-gray-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50">
            {item.children!.map(child => renderMenuItem(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div ref={menuRef} className={`relative ${className}`}>
      <div onClick={() => setIsOpen(!isOpen)} className="cursor-pointer">
        {trigger}
      </div>

      {isOpen && (
        <div className={`
          absolute ${getPositionClasses()} mt-1 w-64 bg-white dark:bg-gray-900 
          rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50
        `}>
          {items.map(item => renderMenuItem(item))}
        </div>
      )}
    </div>
  );
};

// Navigation menu configuration
export const useNavigationMenus = () => {
  const { user, logout } = useAuth();

  const mainMenuItems: MenuItem[] = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: '🏠',
      href: '/dashboard'
    },
    {
      id: 'education',
      label: 'Education Hub',
      icon: '🎓',
      children: [
        {
          id: 'courses',
          label: 'Browse Courses',
          icon: '📚',
          href: '/education/courses',
          description: 'Explore available courses'
        },
        {
          id: 'my-courses',
          label: 'My Courses',
          icon: '📖',
          href: '/education/my-courses',
          badge: '3'
        },
        {
          id: 'create-course',
          label: 'Create Course',
          icon: '➕',
          href: '/education/create'
        },
        {
          id: 'divider-1',
          divider: true
        },
        {
          id: 'certificates',
          label: 'Certificates',
          icon: '🏆',
          href: '/education/certificates'
        },
        {
          id: 'learning-paths',
          label: 'Learning Paths',
          icon: '🛤️',
          children: [
            {
              id: 'web-dev',
              label: 'Web Development',
              href: '/education/paths/web-dev'
            },
            {
              id: 'ai-ml',
              label: 'AI & Machine Learning',
              href: '/education/paths/ai-ml'
            },
            {
              id: 'blockchain',
              label: 'Blockchain Development',
              href: '/education/paths/blockchain'
            },
            {
              id: 'mobile-dev',
              label: 'Mobile Development',
              href: '/education/paths/mobile'
            }
          ]
        }
      ]
    },
    {
      id: 'jobs',
      label: 'Job Marketplace',
      icon: '💼',
      children: [
        {
          id: 'browse-jobs',
          label: 'Browse Jobs',
          icon: '🔍',
          href: '/jobs/browse'
        },
        {
          id: 'my-applications',
          label: 'My Applications',
          icon: '📄',
          href: '/jobs/applications',
          badge: '5'
        },
        {
          id: 'post-job',
          label: 'Post a Job',
          icon: '📝',
          href: '/jobs/post'
        },
        {
          id: 'divider-2',
          divider: true
        },
        {
          id: 'job-categories',
          label: 'Categories',
          icon: '🏷️',
          children: [
            {
              id: 'frontend',
              label: 'Frontend Development',
              href: '/jobs/category/frontend'
            },
            {
              id: 'backend',
              label: 'Backend Development',
              href: '/jobs/category/backend'
            },
            {
              id: 'fullstack',
              label: 'Full Stack Development',
              href: '/jobs/category/fullstack'
            },
            {
              id: 'mobile',
              label: 'Mobile Development',
              href: '/jobs/category/mobile'
            },
            {
              id: 'devops',
              label: 'DevOps & Cloud',
              href: '/jobs/category/devops'
            },
            {
              id: 'ai-jobs',
              label: 'AI & Machine Learning',
              href: '/jobs/category/ai'
            }
          ]
        },
        {
          id: 'salary-insights',
          label: 'Salary Insights',
          icon: '💰',
          href: '/jobs/salary-insights'
        }
      ]
    },
    {
      id: 'marketplace',
      label: 'Marketplace',
      icon: '🛒',
      children: [
        {
          id: 'browse-products',
          label: 'Browse Products',
          icon: '🔍',
          href: '/marketplace/browse'
        },
        {
          id: 'my-orders',
          label: 'My Orders',
          icon: '📦',
          href: '/marketplace/orders',
          badge: '2'
        },
        {
          id: 'sell-product',
          label: 'Sell Product',
          icon: '💰',
          href: '/marketplace/sell'
        },
        {
          id: 'divider-3',
          divider: true
        },
        {
          id: 'categories',
          label: 'Categories',
          icon: '📂',
          children: [
            {
              id: 'dev-tools',
              label: 'Developer Tools',
              href: '/marketplace/category/dev-tools'
            },
            {
              id: 'courses-market',
              label: 'Courses & Tutorials',
              href: '/marketplace/category/courses'
            },
            {
              id: 'templates',
              label: 'Templates & Themes',
              href: '/marketplace/category/templates'
            },
            {
              id: 'plugins',
              label: 'Plugins & Extensions',
              href: '/marketplace/category/plugins'
            },
            {
              id: 'ebooks',
              label: 'E-books & Guides',
              href: '/marketplace/category/ebooks'
            }
          ]
        },
        {
          id: 'wishlist',
          label: 'Wishlist',
          icon: '❤️',
          href: '/marketplace/wishlist'
        }
      ]
    },
    {
      id: 'social',
      label: 'Social Network',
      icon: '👥',
      children: [
        {
          id: 'feed',
          label: 'News Feed',
          icon: '📰',
          href: '/social/feed'
        },
        {
          id: 'connections',
          label: 'My Connections',
          icon: '🤝',
          href: '/social/connections',
          badge: '47'
        },
        {
          id: 'messages',
          label: 'Messages',
          icon: '💬',
          href: '/social/messages',
          badge: '3'
        },
        {
          id: 'divider-4',
          divider: true
        },
        {
          id: 'communities',
          label: 'Communities',
          icon: '🏘️',
          children: [
            {
              id: 'my-communities',
              label: 'My Communities',
              href: '/social/communities/mine'
            },
            {
              id: 'discover-communities',
              label: 'Discover Communities',
              href: '/social/communities/discover'
            },
            {
              id: 'create-community',
              label: 'Create Community',
              href: '/social/communities/create'
            }
          ]
        },
        {
          id: 'events',
          label: 'Events',
          icon: '📅',
          href: '/social/events'
        },
        {
          id: 'groups',
          label: 'Groups',
          icon: '👥',
          href: '/social/groups'
        }
      ]
    },
    {
      id: 'dev-tools',
      label: 'Developer Tools',
      icon: '⚙️',
      children: [
        {
          id: 'code-editor',
          label: 'Cloud IDE',
          icon: '💻',
          href: '/dev-tools/ide',
          description: 'Full-featured cloud IDE'
        },
        {
          id: 'my-projects',
          label: 'My Projects',
          icon: '📁',
          href: '/dev-tools/projects',
          badge: '8'
        },
        {
          id: 'create-project',
          label: 'Create Project',
          icon: '➕',
          href: '/dev-tools/create'
        },
        {
          id: 'divider-5',
          divider: true
        },
        {
          id: 'templates-dev',
          label: 'Project Templates',
          icon: '📋',
          children: [
            {
              id: 'web-app-template',
              label: 'Web Application',
              href: '/dev-tools/templates/web-app'
            },
            {
              id: 'mobile-app-template',
              label: 'Mobile App',
              href: '/dev-tools/templates/mobile-app'
            },
            {
              id: 'api-template',
              label: 'REST API',
              href: '/dev-tools/templates/api'
            },
            {
              id: 'dapp-template',
              label: 'DApp (Blockchain)',
              href: '/dev-tools/templates/dapp'
            },
            {
              id: 'ai-template',
              label: 'AI/ML Project',
              href: '/dev-tools/templates/ai-ml'
            },
            {
              id: 'game-template',
              label: 'Game Development',
              href: '/dev-tools/templates/game'
            }
          ]
        },
        {
          id: 'deployment',
          label: 'Deployment',
          icon: '🚀',
          children: [
            {
              id: 'deploy-heroku',
              label: 'Deploy to Heroku',
              href: '/dev-tools/deploy/heroku'
            },
            {
              id: 'deploy-vercel',
              label: 'Deploy to Vercel',
              href: '/dev-tools/deploy/vercel'
            },
            {
              id: 'deploy-netlify',
              label: 'Deploy to Netlify',
              href: '/dev-tools/deploy/netlify'
            },
            {
              id: 'deploy-aws',
              label: 'Deploy to AWS',
              href: '/dev-tools/deploy/aws'
            }
          ]
        }
      ]
    },
    {
      id: 'quantum-ai',
      label: 'Quantum AI',
      icon: '🤖',
      href: '/quantum-ai'
    }
  ];

  const userMenuItems: MenuItem[] = [
    {
      id: 'profile',
      label: 'Profile',
      icon: '👤',
      href: '/profile'
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: '⚙️',
      children: [
        {
          id: 'general-settings',
          label: 'General',
          icon: '🔧',
          href: '/settings/general'
        },
        {
          id: 'theme-settings',
          label: 'Theme & Appearance',
          icon: '🎨',
          children: [
            {
              id: 'theme-light',
              label: 'Light Theme',
              onClick: () => console.log('Switch to light theme')
            },
            {
              id: 'theme-dark',
              label: 'Dark Theme',
              onClick: () => console.log('Switch to dark theme')
            },
            {
              id: 'theme-auto',
              label: 'Auto (System)',
              onClick: () => console.log('Switch to auto theme')
            },
            {
              id: 'theme-high-contrast',
              label: 'High Con
(Content truncated due to size limit. Use line ranges to read in chunks)