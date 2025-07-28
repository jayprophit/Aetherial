import React, { useState } from 'react';
import { 
  ShoppingBag, 
  Search, 
  Filter, 
  Star, 
  Heart, 
  Share2, 
  ShoppingCart,
  Eye,
  TrendingUp,
  Award,
  Zap,
  Package,
  Truck,
  Shield,
  CreditCard,
  Users,
  Clock,
  DollarSign,
  Tag,
  Grid,
  List,
  SortAsc
} from 'lucide-react';

const MarketplaceModule: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState('grid');
  const [priceRange, setPriceRange] = useState('all');
  const [sortBy, setSortBy] = useState('popular');

  // Product categories aligned with tech ecosystem
  const categories = [
    { id: 'all', name: 'All Products', icon: ShoppingBag, count: 1247 },
    { id: 'software', name: 'Software Tools', icon: Package, count: 234 },
    { id: 'courses', name: 'Courses & Training', icon: Award, count: 156 },
    { id: 'templates', name: 'Code Templates', icon: Zap, count: 89 },
    { id: 'assets', name: 'Digital Assets', icon: Eye, count: 178 },
    { id: 'services', name: 'Dev Services', icon: Users, count: 145 },
    { id: 'hardware', name: 'Hardware', icon: Shield, count: 67 }
  ];

  // Featured products with modern tech focus
  const products = [
    {
      id: 1,
      title: 'Rust Performance Monitoring Tool',
      description: 'Advanced performance monitoring and profiling tool built specifically for Rust applications.',
      price: 149.99,
      originalPrice: 299.99,
      rating: 4.9,
      reviews: 234,
      sales: 1543,
      category: 'software',
      seller: 'RustDev Solutions',
      sellerRating: 4.8,
      image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=300&fit=crop',
      tags: ['Rust', 'Performance', 'Monitoring', 'DevOps'],
      featured: true,
      bestseller: true,
      discount: 50,
      deliveryTime: 'Instant Download',
      lastUpdated: '2024-01-15'
    },
    {
      id: 2,
      title: 'Go Microservices Starter Kit',
      description: 'Complete starter kit for building scalable microservices with Go, Docker, and Kubernetes.',
      price: 89.99,
      originalPrice: 179.99,
      rating: 4.8,
      reviews: 156,
      sales: 892,
      category: 'templates',
      seller: 'CloudNative Dev',
      sellerRating: 4.9,
      image: 'https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=400&h=300&fit=crop',
      tags: ['Go', 'Microservices', 'Docker', 'Kubernetes'],
      featured: true,
      bestseller: false,
      discount: 50,
      deliveryTime: 'Instant Download',
      lastUpdated: '2024-01-12'
    },
    {
      id: 3,
      title: 'TypeScript Full-Stack Course',
      description: 'Comprehensive course covering TypeScript, React, Node.js, and modern development practices.',
      price: 199.99,
      originalPrice: 399.99,
      rating: 4.9,
      reviews: 567,
      sales: 2341,
      category: 'courses',
      seller: 'TypeScript Academy',
      sellerRating: 4.9,
      image: 'https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=400&h=300&fit=crop',
      tags: ['TypeScript', 'React', 'Node.js', 'Full-Stack'],
      featured: true,
      bestseller: true,
      discount: 50,
      deliveryTime: 'Lifetime Access',
      lastUpdated: '2024-01-18'
    },
    {
      id: 4,
      title: 'Python AI/ML Development Service',
      description: 'Custom AI/ML solution development using Python, TensorFlow, and modern MLOps practices.',
      price: 2499.99,
      originalPrice: null,
      rating: 4.7,
      reviews: 89,
      sales: 234,
      category: 'services',
      seller: 'AI Solutions Pro',
      sellerRating: 4.8,
      image: 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400&h=300&fit=crop',
      tags: ['Python', 'AI/ML', 'TensorFlow', 'Custom Development'],
      featured: false,
      bestseller: false,
      discount: 0,
      deliveryTime: '2-4 weeks',
      lastUpdated: '2024-01-10'
    },
    {
      id: 5,
      title: 'Kubernetes Deployment Templates',
      description: 'Production-ready Kubernetes deployment templates for various application architectures.',
      price: 79.99,
      originalPrice: 159.99,
      rating: 4.6,
      reviews: 123,
      sales: 456,
      category: 'templates',
      seller: 'DevOps Masters',
      sellerRating: 4.7,
      image: 'https://images.unsplash.com/photo-1667372335962-5fd503a8ae5b?w=400&h=300&fit=crop',
      tags: ['Kubernetes', 'DevOps', 'Templates', 'Production'],
      featured: false,
      bestseller: false,
      discount: 50,
      deliveryTime: 'Instant Download',
      lastUpdated: '2024-01-08'
    },
    {
      id: 6,
      title: 'Flutter UI Component Library',
      description: 'Beautiful, customizable UI components for Flutter applications with modern design patterns.',
      price: 129.99,
      originalPrice: 259.99,
      rating: 4.8,
      reviews: 234,
      sales: 789,
      category: 'assets',
      seller: 'Flutter Design Co',
      sellerRating: 4.9,
      image: 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400&h=300&fit=crop',
      tags: ['Flutter', 'UI Components', 'Design', 'Mobile'],
      featured: true,
      bestseller: false,
      discount: 50,
      deliveryTime: 'Instant Download',
      lastUpdated: '2024-01-14'
    }
  ];

  const filteredProducts = products.filter(product => {
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    const matchesSearch = product.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const topSellers = [
    { name: 'RustDev Solutions', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=60&h=60&fit=crop', rating: 4.9, sales: 1543 },
    { name: 'TypeScript Academy', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&h=60&fit=crop', rating: 4.9, sales: 2341 },
    { name: 'CloudNative Dev', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=60&h=60&fit=crop', rating: 4.8, sales: 892 },
    { name: 'Flutter Design Co', avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=60&h=60&fit=crop', rating: 4.9, sales: 789 }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">Digital Marketplace</h1>
            <p className="text-purple-100">
              Discover tools, courses, and services for modern development
            </p>
          </div>
          <div className="hidden md:block">
            <div className="flex items-center space-x-6 text-purple-100">
              <div className="text-center">
                <div className="text-2xl font-bold">1,247</div>
                <div className="text-sm">Products</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">456</div>
                <div className="text-sm">Sellers</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">4.8</div>
                <div className="text-sm">Avg Rating</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div className="flex-1 max-w-md">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search products, tools, or technologies..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <select 
              value={priceRange}
              onChange={(e) => setPriceRange(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="all">All Prices</option>
              <option value="free">Free</option>
              <option value="under-50">Under $50</option>
              <option value="50-200">$50 - $200</option>
              <option value="over-200">Over $200</option>
            </select>
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="popular">Most Popular</option>
              <option value="newest">Newest</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="rating">Highest Rated</option>
            </select>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded-lg ${viewMode === 'grid' ? 'bg-purple-100 text-purple-600' : 'text-gray-400'}`}
              >
                <Grid className="w-5 h-5" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded-lg ${viewMode === 'list' ? 'bg-purple-100 text-purple-600' : 'text-gray-400'}`}
              >
                <List className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Categories */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Browse Categories</h2>
        <div className="flex flex-wrap gap-3">
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                  selectedCategory === category.id
                    ? 'bg-purple-50 border-purple-500 text-purple-700'
                    : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{category.name}</span>
                <span className="bg-gray-200 text-gray-600 px-2 py-1 rounded-full text-xs">
                  {category.count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Product Grid */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">
                {selectedCategory === 'all' ? 'All Products' : categories.find(c => c.id === selectedCategory)?.name}
                <span className="text-gray-500 font-normal ml-2">({filteredProducts.length} results)</span>
              </h2>
            </div>

            <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6' : 'space-y-4'}>
              {filteredProducts.map((product) => (
                <div key={product.id} className={`border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow cursor-pointer group ${
                  viewMode === 'list' ? 'flex' : ''
                } ${product.featured ? 'border-purple-200 bg-purple-50/30' : ''}`}>
                  <div className={`relative ${viewMode === 'list' ? 'w-48 flex-shrink-0' : ''}`}>
                    <img
                      src={product.image}
                      alt={product.title}
                      className={`object-cover group-hover:scale-105 transition-transform duration-300 ${
                        viewMode === 'list' ? 'w-full h-32' : 'w-full h-48'
                      }`}
                    />
                    {product.featured && (
                      <div className="absolute top-3 left-3 bg-purple-500 text-white px-2 py-1 rounded text-xs font-medium">
                        Featured
                      </div>
                    )}
                    {product.bestseller && (
                      <div className="absolute top-3 right-3 bg-orange-500 text-white px-2 py-1 rounded text-xs font-medium">
                        Bestseller
                      </div>
                    )}
                    {product.discount > 0 && (
                      <div className="absolute bottom-3 left-3 bg-red-500 text-white px-2 py-1 rounded text-xs font-medium">
                        -{product.discount}%
                      </div>
                    )}
                    <div className="absolute top-3 right-3 flex space-x-2">
                      <button className="w-8 h-8 bg-white/80 rounded-full flex items-center justify-center hover:bg-white transition-colors">
                        <Heart className="w-4 h-4 text-gray-600" />
                      </button>
                      <button className="w-8 h-8 bg-white/80 rounded-full flex items-center justify-center hover:bg-white transition-colors">
                        <Share2 className="w-4 h-4 text-gray-600" />
                      </button>
                    </div>
                  </div>

                  <div className="p-4 flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-purple-600 font-medium uppercase tracking-wide">
                        {categories.find(c => c.id === product.category)?.name}
                      </span>
                      <div className="flex items-center space-x-1">
                        <Star className="w-4 h-4 text-yellow-400 fill-current" />
                        <span className="text-sm font-medium text-gray-900">{product.rating}</span>
                        <span className="text-sm text-gray-500">({product.reviews})</span>
                      </div>
                    </div>

                    <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-purple-600 transition-colors">
                      {product.title}
                    </h3>

                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {product.description}
                    </p>

                    <div className="flex flex-wrap gap-1 mb-3">
                      {product.tags.slice(0, 3).map((tag, index) => (
                        <span key={index} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                      {product.tags.length > 3 && (
                        <span className="text-gray-400 text-xs">+{product.tags.length - 3} more</span>
                      )}

(Content truncated due to size limit. Use line ranges to read in chunks)