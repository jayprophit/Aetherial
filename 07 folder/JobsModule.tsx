import React, { useState } from 'react';
import { 
  Briefcase, 
  MapPin, 
  Clock, 
  DollarSign, 
  Users, 
  Star, 
  Search, 
  Filter, 
  Building,
  Code,
  Server,
  Cloud,
  Database,
  Globe,
  Zap,
  TrendingUp,
  CheckCircle,
  Heart,
  Share2,
  ExternalLink,
  Calendar,
  Award,
  Target,
  ArrowRight,
  Plus,
  Eye,
  MessageSquare
} from 'lucide-react';

const JobsModule: React.FC = () => {
  const [activeTab, setActiveTab] = useState('browse');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [jobType, setJobType] = useState('all');
  const [experienceLevel, setExperienceLevel] = useState('all');

  // Job categories aligned with modern tech stack
  const categories = [
    { id: 'all', name: 'All Jobs', icon: Briefcase, count: 2847 },
    { id: 'rust', name: 'Rust Developer', icon: Code, count: 156 },
    { id: 'go', name: 'Go Developer', icon: Server, count: 234 },
    { id: 'typescript', name: 'TypeScript', icon: Code, count: 445 },
    { id: 'python', name: 'Python', icon: Code, count: 567 },
    { id: 'devops', name: 'DevOps/SRE', icon: Cloud, count: 289 },
    { id: 'mobile', name: 'Mobile Dev', icon: Globe, count: 178 },
    { id: 'fullstack', name: 'Full Stack', icon: Database, count: 334 }
  ];

  // Featured job listings
  const jobs = [
    {
      id: 1,
      title: 'Senior Rust Systems Engineer',
      company: 'TechCorp Inc.',
      location: 'San Francisco, CA',
      type: 'Full-time',
      remote: true,
      salary: '$180,000 - $250,000',
      experience: 'Senior',
      posted: '2 days ago',
      applicants: 23,
      description: 'Build high-performance systems using Rust for our next-generation infrastructure platform.',
      requirements: ['5+ years Rust experience', 'Systems programming', 'WebAssembly', 'Concurrency'],
      technologies: ['Rust', 'WebAssembly', 'Docker', 'Kubernetes'],
      companyLogo: 'https://images.unsplash.com/photo-1549923746-c502d488b3ea?w=100&h=100&fit=crop',
      featured: true,
      urgent: false,
      rating: 4.8,
      employees: '1000-5000'
    },
    {
      id: 2,
      title: 'Go Microservices Architect',
      company: 'CloudNative Solutions',
      location: 'Austin, TX',
      type: 'Full-time',
      remote: true,
      salary: '$160,000 - $220,000',
      experience: 'Senior',
      posted: '1 day ago',
      applicants: 18,
      description: 'Design and implement scalable microservices architecture using Go and cloud-native technologies.',
      requirements: ['Go expertise', 'Microservices', 'Kubernetes', 'gRPC'],
      technologies: ['Go', 'Kubernetes', 'Docker', 'gRPC', 'PostgreSQL'],
      companyLogo: 'https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=100&h=100&fit=crop',
      featured: true,
      urgent: true,
      rating: 4.9,
      employees: '500-1000'
    },
    {
      id: 3,
      title: 'TypeScript Full-Stack Developer',
      company: 'StartupXYZ',
      location: 'New York, NY',
      type: 'Full-time',
      remote: false,
      salary: '$120,000 - $180,000',
      experience: 'Mid-level',
      posted: '3 days ago',
      applicants: 45,
      description: 'Join our team to build modern web applications using TypeScript, React, and Node.js.',
      requirements: ['TypeScript proficiency', 'React/Next.js', 'Node.js', 'Database design'],
      technologies: ['TypeScript', 'React', 'Next.js', 'Node.js', 'PostgreSQL'],
      companyLogo: 'https://images.unsplash.com/photo-1572021335469-31706a17aaef?w=100&h=100&fit=crop',
      featured: false,
      urgent: false,
      rating: 4.6,
      employees: '50-200'
    },
    {
      id: 4,
      title: 'Python AI/ML Engineer',
      company: 'AI Innovations Lab',
      location: 'Seattle, WA',
      type: 'Full-time',
      remote: true,
      salary: '$140,000 - $200,000',
      experience: 'Mid-level',
      posted: '1 week ago',
      applicants: 67,
      description: 'Develop cutting-edge AI/ML solutions using Python, TensorFlow, and modern MLOps practices.',
      requirements: ['Python expertise', 'TensorFlow/PyTorch', 'MLOps', 'Data engineering'],
      technologies: ['Python', 'TensorFlow', 'Docker', 'Kubernetes', 'AWS'],
      companyLogo: 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=100&h=100&fit=crop',
      featured: true,
      urgent: false,
      rating: 4.7,
      employees: '200-500'
    },
    {
      id: 5,
      title: 'DevOps Engineer - Kubernetes Specialist',
      company: 'Enterprise Solutions',
      location: 'Chicago, IL',
      type: 'Contract',
      remote: true,
      salary: '$90 - $130/hour',
      experience: 'Senior',
      posted: '4 days ago',
      applicants: 29,
      description: 'Lead Kubernetes infrastructure and CI/CD pipeline implementation for enterprise clients.',
      requirements: ['Kubernetes expertise', 'CI/CD', 'Infrastructure as Code', 'Monitoring'],
      technologies: ['Kubernetes', 'Docker', 'Terraform', 'Jenkins', 'Prometheus'],
      companyLogo: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=100&h=100&fit=crop',
      featured: false,
      urgent: true,
      rating: 4.5,
      employees: '5000+'
    },
    {
      id: 6,
      title: 'Flutter Mobile Developer',
      company: 'MobileFirst Inc.',
      location: 'Los Angeles, CA',
      type: 'Full-time',
      remote: false,
      salary: '$110,000 - $160,000',
      experience: 'Mid-level',
      posted: '5 days ago',
      applicants: 34,
      description: 'Build beautiful cross-platform mobile applications using Flutter and modern development practices.',
      requirements: ['Flutter/Dart', 'Mobile UI/UX', 'State management', 'API integration'],
      technologies: ['Flutter', 'Dart', 'Firebase', 'REST APIs', 'Git'],
      companyLogo: 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=100&h=100&fit=crop',
      featured: false,
      urgent: false,
      rating: 4.4,
      employees: '100-500'
    }
  ];

  const filteredJobs = jobs.filter(job => {
    const matchesCategory = selectedCategory === 'all' || 
      job.technologies.some(tech => tech.toLowerCase().includes(selectedCategory)) ||
      job.title.toLowerCase().includes(selectedCategory);
    const matchesSearch = job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         job.technologies.some(tech => tech.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesType = jobType === 'all' || job.type.toLowerCase().includes(jobType.toLowerCase());
    const matchesExperience = experienceLevel === 'all' || job.experience.toLowerCase().includes(experienceLevel.toLowerCase());
    
    return matchesCategory && matchesSearch && matchesType && matchesExperience;
  });

  const topCompanies = [
    { name: 'TechCorp Inc.', logo: 'https://images.unsplash.com/photo-1549923746-c502d488b3ea?w=80&h=80&fit=crop', jobs: 45, rating: 4.8 },
    { name: 'CloudNative Solutions', logo: 'https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=80&h=80&fit=crop', jobs: 23, rating: 4.9 },
    { name: 'AI Innovations Lab', logo: 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=80&h=80&fit=crop', jobs: 18, rating: 4.7 },
    { name: 'StartupXYZ', logo: 'https://images.unsplash.com/photo-1572021335469-31706a17aaef?w=80&h=80&fit=crop', jobs: 12, rating: 4.6 }
  ];

  const salaryRanges = [
    { range: '$80K - $120K', count: 234, percentage: 25 },
    { range: '$120K - $160K', count: 445, percentage: 35 },
    { range: '$160K - $200K', count: 356, percentage: 28 },
    { range: '$200K+', count: 178, percentage: 12 }
  ];

  const tabs = [
    { id: 'browse', name: 'Browse Jobs', icon: Search },
    { id: 'saved', name: 'Saved Jobs', icon: Heart },
    { id: 'applied', name: 'Applications', icon: CheckCircle },
    { id: 'profile', name: 'My Profile', icon: Users }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">Job Marketplace</h1>
            <p className="text-blue-100">
              Find your next opportunity in modern technology
            </p>
          </div>
          <div className="hidden md:block">
            <div className="flex items-center space-x-6 text-blue-100">
              <div className="text-center">
                <div className="text-2xl font-bold">2,847</div>
                <div className="text-sm">Active Jobs</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">1,234</div>
                <div className="text-sm">Companies</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">$165K</div>
                <div className="text-sm">Avg Salary</div>
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
                      ? 'border-blue-500 text-blue-600'
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
          {activeTab === 'browse' && (
            <div className="space-y-6">
              {/* Search and Filters */}
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
                <div className="flex-1 max-w-md">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      placeholder="Search jobs, companies, or technologies..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <select 
                    value={jobType}
                    onChange={(e) => setJobType(e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Types</option>
                    <option value="full-time">Full-time</option>
                    <option value="contract">Contract</option>
                    <option value="part-time">Part-time</option>
                  </select>
                  <select 
                    value={experienceLevel}
                    onChange={(e) => setExperienceLevel(e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Levels</option>
                    <option value="entry">Entry Level</option>
                    <option value="mid">Mid Level</option>
                    <option value="senior">Senior Level</option>
                  </select>
                  <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                    <Filter className="w-4 h-4" />
                    <span>More Filters</span>
                  </button>
                </div>
              </div>

              {/* Categories */}
              <div className="flex flex-wrap gap-3">
                {categories.map((category) => {
                  const Icon = category.icon;
                  return (
                    <button
                      key={category.id}
                      onClick={() => setSelectedCategory(category.id)}
                      className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                        selectedCategory === category.id
                          ? 'bg-blue-50 border-blue-500 text-blue-700'
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

              {/* Job Listings */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {filteredJobs.length} jobs found
                  </h3>
                  <select className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option>Most Relevant</option>
                    <option>Newest</option>
                    <option>Salary: High to Low</option>
                    <option>Company Rating</option>
                  </select>
                </div>

                {filteredJobs.map((job) => (
                  <div key={job.id} className={`border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer ${
                    job.featured ? 'border-blue-200 bg-blue-50/30' : 'border-gray-200'
                  }`}>
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4 flex-1">
                        <img
                          src={job.companyLogo}
                          alt={job.company}
                          className="w-12 h-12 rounded-lg object-cover"
                        />
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <h3 className="text-lg font-semibold text-gray-900 hover:text-blue-600 transition-colors">
                              {job.title}
                            </h3>
                            {job.featured && (
                              <span className="bg-blue-500 text-white px-2 py-1 rounded text-xs font-medium">
                                Featured
                              </span>
                            )}
                            {job.urgent && (
                              <span className="bg-red-500 text-white px-2 py-1 rounded text-xs font-medium">
                                Urgent
                              </span>
                            )}
                          </div>
                          
                          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                            <di
(Content truncated due to size limit. Use line ranges to read in chunks)