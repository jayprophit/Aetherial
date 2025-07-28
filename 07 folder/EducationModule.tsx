import React, { useState } from 'react';
import { 
  BookOpen, 
  Play, 
  Clock, 
  Users, 
  Star, 
  Award, 
  Search, 
  Filter, 
  ChevronRight,
  Code,
  Database,
  Cloud,
  Server,
  Zap,
  TrendingUp,
  CheckCircle,
  Lock,
  Globe,
  Video,
  FileText,
  Download,
  Heart,
  Share2
} from 'lucide-react';

const EducationModule: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState('grid');

  // Modern technology categories aligned with industry standards
  const categories = [
    { id: 'all', name: 'All Courses', icon: BookOpen, count: 156 },
    { id: 'rust', name: 'Rust', icon: Code, count: 24 },
    { id: 'go', name: 'Go', icon: Server, count: 18 },
    { id: 'typescript', name: 'TypeScript', icon: Code, count: 32 },
    { id: 'python', name: 'Python', icon: Code, count: 45 },
    { id: 'devops', name: 'DevOps', icon: Cloud, count: 28 },
    { id: 'mobile', name: 'Mobile Dev', icon: Globe, count: 19 }
  ];

  // Course data with modern tech focus
  const courses = [
    {
      id: 1,
      title: 'Complete Rust Programming: From Beginner to Systems Expert',
      instructor: 'Alex Chen',
      rating: 4.9,
      students: 12543,
      duration: '18 hours',
      lessons: 156,
      price: 89.99,
      originalPrice: 199.99,
      level: 'Beginner to Advanced',
      category: 'rust',
      image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=250&fit=crop',
      description: 'Master Rust programming for systems development, WebAssembly, and high-performance applications.',
      skills: ['Memory Safety', 'Concurrency', 'WebAssembly', 'Systems Programming'],
      bestseller: true,
      updated: '2024-01-15'
    },
    {
      id: 2,
      title: 'Go Microservices: Building Cloud-Native Applications',
      instructor: 'Sarah Johnson',
      rating: 4.8,
      students: 8932,
      duration: '14 hours',
      lessons: 98,
      price: 79.99,
      originalPrice: 159.99,
      level: 'Intermediate',
      category: 'go',
      image: 'https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=400&h=250&fit=crop',
      description: 'Build scalable microservices with Go, Docker, and Kubernetes for cloud deployment.',
      skills: ['Microservices', 'Docker', 'Kubernetes', 'gRPC'],
      bestseller: false,
      updated: '2024-01-10'
    },
    {
      id: 3,
      title: 'TypeScript Mastery: Large-Scale Application Development',
      instructor: 'David Rodriguez',
      rating: 4.9,
      students: 15678,
      duration: '22 hours',
      lessons: 187,
      price: 94.99,
      originalPrice: 189.99,
      level: 'Intermediate to Advanced',
      category: 'typescript',
      image: 'https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=400&h=250&fit=crop',
      description: 'Advanced TypeScript patterns for enterprise applications and modern frameworks.',
      skills: ['Advanced Types', 'Design Patterns', 'Testing', 'Performance'],
      bestseller: true,
      updated: '2024-01-20'
    },
    {
      id: 4,
      title: 'Python Full-Stack: Django, Flask & AI Integration',
      instructor: 'Maria Garcia',
      rating: 4.7,
      students: 23456,
      duration: '28 hours',
      lessons: 234,
      price: 99.99,
      originalPrice: 249.99,
      level: 'All Levels',
      category: 'python',
      image: 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400&h=250&fit=crop',
      description: 'Complete Python development with Django, Flask, and modern AI/ML integration.',
      skills: ['Django', 'Flask', 'AI/ML', 'REST APIs'],
      bestseller: true,
      updated: '2024-01-18'
    },
    {
      id: 5,
      title: 'Kubernetes in Production: DevOps Mastery',
      instructor: 'James Wilson',
      rating: 4.8,
      students: 11234,
      duration: '16 hours',
      lessons: 124,
      price: 84.99,
      originalPrice: 169.99,
      level: 'Advanced',
      category: 'devops',
      image: 'https://images.unsplash.com/photo-1667372335962-5fd503a8ae5b?w=400&h=250&fit=crop',
      description: 'Master Kubernetes deployment, scaling, and management for production environments.',
      skills: ['Kubernetes', 'Docker', 'CI/CD', 'Monitoring'],
      bestseller: false,
      updated: '2024-01-12'
    },
    {
      id: 6,
      title: 'Flutter & Kotlin Multiplatform: Cross-Platform Mastery',
      instructor: 'Lisa Park',
      rating: 4.9,
      students: 9876,
      duration: '20 hours',
      lessons: 165,
      price: 89.99,
      originalPrice: 179.99,
      level: 'Intermediate',
      category: 'mobile',
      image: 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400&h=250&fit=crop',
      description: 'Build native mobile apps with Flutter and Kotlin Multiplatform for iOS and Android.',
      skills: ['Flutter', 'Kotlin', 'iOS', 'Android'],
      bestseller: true,
      updated: '2024-01-16'
    }
  ];

  const filteredCourses = courses.filter(course => {
    const matchesCategory = selectedCategory === 'all' || course.category === selectedCategory;
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         course.instructor.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         course.skills.some(skill => skill.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const learningPaths = [
    {
      title: 'Systems Programming Track',
      description: 'Master low-level programming with Rust and C++',
      courses: 8,
      duration: '120 hours',
      technologies: ['Rust', 'C++', 'Assembly', 'WebAssembly'],
      color: 'bg-orange-500'
    },
    {
      title: 'Cloud Native Developer',
      description: 'Build scalable cloud applications with Go and Kubernetes',
      courses: 12,
      duration: '180 hours',
      technologies: ['Go', 'Kubernetes', 'Docker', 'Microservices'],
      color: 'bg-blue-500'
    },
    {
      title: 'Full-Stack TypeScript',
      description: 'End-to-end development with modern TypeScript stack',
      courses: 15,
      duration: '200 hours',
      technologies: ['TypeScript', 'React', 'Node.js', 'Next.js'],
      color: 'bg-indigo-500'
    },
    {
      title: 'AI/ML Engineer',
      description: 'Python-based machine learning and AI development',
      courses: 18,
      duration: '250 hours',
      technologies: ['Python', 'TensorFlow', 'PyTorch', 'Django'],
      color: 'bg-green-500'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">Education Hub</h1>
            <p className="text-indigo-100">
              Master modern technologies with industry-expert courses
            </p>
          </div>
          <div className="hidden md:block">
            <div className="flex items-center space-x-6 text-indigo-100">
              <div className="text-center">
                <div className="text-2xl font-bold">156</div>
                <div className="text-sm">Courses</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">45K+</div>
                <div className="text-sm">Students</div>
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
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex-1 max-w-md">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search courses, instructors, or technologies..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              <Filter className="w-4 h-4" />
              <span>Filters</span>
            </button>
            <select className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option>Most Popular</option>
              <option>Newest</option>
              <option>Highest Rated</option>
              <option>Price: Low to High</option>
            </select>
          </div>
        </div>
      </div>

      {/* Learning Paths */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Learning Paths</h2>
          <button className="text-indigo-600 hover:text-indigo-700 font-medium">View All</button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {learningPaths.map((path, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4 hover:border-indigo-300 transition-colors cursor-pointer">
              <div className={`w-12 h-12 ${path.color} rounded-lg flex items-center justify-center mb-4`}>
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">{path.title}</h3>
              <p className="text-sm text-gray-600 mb-3">{path.description}</p>
              <div className="space-y-2 text-xs text-gray-500">
                <div className="flex justify-between">
                  <span>{path.courses} courses</span>
                  <span>{path.duration}</span>
                </div>
                <div className="flex flex-wrap gap-1">
                  {path.technologies.slice(0, 3).map((tech, techIndex) => (
                    <span key={techIndex} className="bg-gray-100 px-2 py-1 rounded text-xs">
                      {tech}
                    </span>
                  ))}
                  {path.technologies.length > 3 && (
                    <span className="text-gray-400">+{path.technologies.length - 3}</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Categories */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Browse by Technology</h2>
        <div className="flex flex-wrap gap-3">
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                  selectedCategory === category.id
                    ? 'bg-indigo-50 border-indigo-500 text-indigo-700'
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

      {/* Course Grid */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">
            {selectedCategory === 'all' ? 'All Courses' : categories.find(c => c.id === selectedCategory)?.name + ' Courses'}
            <span className="text-gray-500 font-normal ml-2">({filteredCourses.length} results)</span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course) => (
            <div key={course.id} className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow cursor-pointer group">
              <div className="relative">
                <img
                  src={course.image}
                  alt={course.title}
                  className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                {course.bestseller && (
                  <div className="absolute top-3 left-3 bg-orange-500 text-white px-2 py-1 rounded text-xs font-medium">
                    Bestseller
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
                <div className="absolute bottom-3 left-3 bg-black/70 text-white px-2 py-1 rounded text-xs">
                  {course.duration}
                </div>
              </div>

              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-indigo-600 font-medium uppercase tracking-wide">
                    {course.level}
                  </span>
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="text-sm font-medium text-gray-900">{course.rating}</span>
                    <span className="text-sm text-gray-500">({course.students.toLocaleString()})</span>
                  </div>
                </div>

                <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-indigo-600 transition-colors">
                  {course.title}
                </h3>

                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                  {course.description}
                </p>

                <div className="flex items-center space-x-2 mb-3 text-sm text-gray-500">
                  <Users className="w-4 h-4" />
                  <span>{course.students.toLocaleString()} students</span>
                  <span>•</span>
                  <Clock className="w-4 h-4" />
                  <span>{course.lessons} lessons</span>
                </div>

                <div className="flex flex-wrap gap-1 mb-4">
                  {course.skills.slice(0, 3).map((skill, index) => (
                    <span key={index} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                      {skill}
                    </span>
                  ))}
                  {course.skills.length > 3 && (
                    <span className="text-gray-400 text-xs">+{course.skil
(Content truncated due to size limit. Use line ranges to read in chunks)