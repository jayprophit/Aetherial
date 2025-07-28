import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';

interface Job {
  id: string;
  title: string;
  description: string;
  company: string;
  location: string;
  remote: boolean;
  type: 'full-time' | 'part-time' | 'contract' | 'freelance' | 'internship';
  category: string;
  skills: string[];
  salaryMin: number;
  salaryMax: number;
  currency: string;
  experience: 'entry' | 'mid' | 'senior' | 'lead';
  postedDate: string;
  deadline: string;
  applicants: number;
  verified: boolean;
  featured: boolean;
  urgent: boolean;
  companyLogo?: string;
  benefits: string[];
  requirements: string[];
  responsibilities: string[];
  marketSalaryMin: number;
  marketSalaryMax: number;
  region: string;
  country: string;
  timezone?: string;
  languages: string[];
  rating: number;
  reviews: number;
}

interface JobFilters {
  search: string;
  location: string;
  remote: boolean | null;
  type: string[];
  category: string;
  experience: string[];
  salaryMin: number;
  salaryMax: number;
  currency: string;
  skills: string[];
  region: string;
  sortBy: 'relevance' | 'date' | 'salary' | 'rating';
}

const JobMarketplace: React.FC = () => {
  const { user } = useAuth();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filteredJobs, setFilteredJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [showJobDetails, setShowJobDetails] = useState(false);
  const [loading, setLoading] = useState(true);
  const [userOptedIn, setUserOptedIn] = useState(false);
  const [userSalaryRange, setUserSalaryRange] = useState({ min: 50000, max: 150000 });
  const [filters, setFilters] = useState<JobFilters>({
    search: '',
    location: '',
    remote: null,
    type: [],
    category: '',
    experience: [],
    salaryMin: 0,
    salaryMax: 500000,
    currency: 'USD',
    skills: [],
    region: '',
    sortBy: 'relevance'
  });

  // Mock job data with comprehensive information
  const mockJobs: Job[] = [
    {
      id: '1',
      title: 'Senior Full Stack Developer (React + Node.js)',
      description: 'We are looking for an experienced Full Stack Developer to join our growing team. You will be responsible for developing and maintaining web applications using modern technologies.',
      company: 'TechCorp Solutions',
      location: 'San Francisco, CA',
      remote: true,
      type: 'full-time',
      category: 'Software Development',
      skills: ['React', 'Node.js', 'TypeScript', 'PostgreSQL', 'AWS', 'Docker'],
      salaryMin: 120000,
      salaryMax: 180000,
      currency: 'USD',
      experience: 'senior',
      postedDate: '2025-06-20',
      deadline: '2025-07-20',
      applicants: 45,
      verified: true,
      featured: true,
      urgent: false,
      benefits: ['Health Insurance', 'Dental Coverage', '401k Matching', 'Flexible PTO', 'Remote Work', 'Learning Budget'],
      requirements: [
        '5+ years of experience with React and Node.js',
        'Strong understanding of TypeScript',
        'Experience with cloud platforms (AWS preferred)',
        'Knowledge of containerization (Docker, Kubernetes)',
        'Excellent problem-solving skills'
      ],
      responsibilities: [
        'Develop and maintain web applications',
        'Collaborate with cross-functional teams',
        'Write clean, maintainable code',
        'Participate in code reviews',
        'Mentor junior developers'
      ],
      marketSalaryMin: 115000,
      marketSalaryMax: 185000,
      region: 'North America',
      country: 'United States',
      timezone: 'PST',
      languages: ['English'],
      rating: 4.8,
      reviews: 127
    },
    {
      id: '2',
      title: 'Blockchain Developer - DeFi Protocol',
      description: 'Join our innovative DeFi team to build the next generation of decentralized financial applications. Experience with Solidity and Web3 technologies required.',
      company: 'CryptoFinance Labs',
      location: 'Remote',
      remote: true,
      type: 'contract',
      category: 'Blockchain',
      skills: ['Solidity', 'Web3.js', 'Ethereum', 'Smart Contracts', 'DeFi', 'Rust'],
      salaryMin: 150000,
      salaryMax: 250000,
      currency: 'USD',
      experience: 'mid',
      postedDate: '2025-06-22',
      deadline: '2025-07-15',
      applicants: 23,
      verified: true,
      featured: false,
      urgent: true,
      benefits: ['Crypto Bonuses', 'Flexible Hours', 'Conference Budget', 'Hardware Allowance'],
      requirements: [
        '3+ years of Solidity development',
        'Experience with DeFi protocols',
        'Understanding of blockchain security',
        'Knowledge of gas optimization',
        'Experience with testing frameworks'
      ],
      responsibilities: [
        'Develop smart contracts for DeFi protocols',
        'Audit and optimize existing contracts',
        'Integrate with frontend applications',
        'Ensure security best practices',
        'Document technical specifications'
      ],
      marketSalaryMin: 140000,
      marketSalaryMax: 260000,
      region: 'Global',
      country: 'Remote',
      languages: ['English'],
      rating: 4.6,
      reviews: 89
    },
    {
      id: '3',
      title: 'AI/ML Engineer - Computer Vision',
      description: 'Work on cutting-edge computer vision projects using deep learning and neural networks. Experience with PyTorch and TensorFlow required.',
      company: 'VisionAI Inc',
      location: 'London, UK',
      remote: false,
      type: 'full-time',
      category: 'Artificial Intelligence',
      skills: ['Python', 'PyTorch', 'TensorFlow', 'OpenCV', 'Computer Vision', 'Deep Learning'],
      salaryMin: 80000,
      salaryMax: 120000,
      currency: 'GBP',
      experience: 'mid',
      postedDate: '2025-06-21',
      deadline: '2025-07-25',
      applicants: 67,
      verified: true,
      featured: true,
      urgent: false,
      benefits: ['Visa Sponsorship', 'Health Insurance', 'Pension', 'Gym Membership', 'Learning Budget'],
      requirements: [
        'MSc in Computer Science or related field',
        '3+ years of ML/AI experience',
        'Strong Python programming skills',
        'Experience with computer vision libraries',
        'Knowledge of deep learning frameworks'
      ],
      responsibilities: [
        'Develop computer vision algorithms',
        'Train and optimize neural networks',
        'Collaborate with research team',
        'Deploy models to production',
        'Stay updated with latest AI research'
      ],
      marketSalaryMin: 75000,
      marketSalaryMax: 125000,
      region: 'Europe',
      country: 'United Kingdom',
      timezone: 'GMT',
      languages: ['English'],
      rating: 4.7,
      reviews: 156
    },
    {
      id: '4',
      title: 'DevOps Engineer - Kubernetes & AWS',
      description: 'Seeking a DevOps engineer to manage our cloud infrastructure and CI/CD pipelines. Strong experience with Kubernetes and AWS required.',
      company: 'CloudScale Systems',
      location: 'Berlin, Germany',
      remote: true,
      type: 'full-time',
      category: 'DevOps',
      skills: ['Kubernetes', 'AWS', 'Docker', 'Terraform', 'Jenkins', 'Python'],
      salaryMin: 70000,
      salaryMax: 95000,
      currency: 'EUR',
      experience: 'senior',
      postedDate: '2025-06-19',
      deadline: '2025-07-30',
      applicants: 34,
      verified: true,
      featured: false,
      urgent: false,
      benefits: ['Relocation Package', 'Health Insurance', 'Flexible Hours', 'Professional Development'],
      requirements: [
        '5+ years of DevOps experience',
        'Expert knowledge of Kubernetes',
        'AWS certification preferred',
        'Experience with Infrastructure as Code',
        'Strong scripting skills'
      ],
      responsibilities: [
        'Manage Kubernetes clusters',
        'Optimize CI/CD pipelines',
        'Monitor system performance',
        'Implement security best practices',
        'Automate deployment processes'
      ],
      marketSalaryMin: 68000,
      marketSalaryMax: 98000,
      region: 'Europe',
      country: 'Germany',
      timezone: 'CET',
      languages: ['English', 'German'],
      rating: 4.5,
      reviews: 203
    },
    {
      id: '5',
      title: 'Mobile App Developer - Flutter',
      description: 'Develop cross-platform mobile applications using Flutter. Experience with both iOS and Android development required.',
      company: 'MobileFirst Studio',
      location: 'Toronto, Canada',
      remote: true,
      type: 'contract',
      category: 'Mobile Development',
      skills: ['Flutter', 'Dart', 'iOS', 'Android', 'Firebase', 'REST APIs'],
      salaryMin: 80000,
      salaryMax: 110000,
      currency: 'CAD',
      experience: 'mid',
      postedDate: '2025-06-23',
      deadline: '2025-08-01',
      applicants: 28,
      verified: true,
      featured: false,
      urgent: true,
      benefits: ['Health Benefits', 'Flexible Schedule', 'Equipment Provided', 'Professional Development'],
      requirements: [
        '3+ years of Flutter development',
        'Published apps on App Store and Play Store',
        'Experience with state management',
        'Knowledge of mobile UI/UX principles',
        'Strong debugging skills'
      ],
      responsibilities: [
        'Develop Flutter mobile applications',
        'Integrate with backend APIs',
        'Optimize app performance',
        'Collaborate with designers',
        'Maintain code quality'
      ],
      marketSalaryMin: 75000,
      marketSalaryMax: 115000,
      region: 'North America',
      country: 'Canada',
      timezone: 'EST',
      languages: ['English', 'French'],
      rating: 4.4,
      reviews: 92
    }
  ];

  const categories = [
    'Software Development',
    'Blockchain',
    'Artificial Intelligence',
    'DevOps',
    'Mobile Development',
    'Data Science',
    'Cybersecurity',
    'UI/UX Design',
    'Product Management',
    'Quality Assurance'
  ];

  const regions = [
    'North America',
    'Europe',
    'Asia Pacific',
    'Latin America',
    'Middle East & Africa',
    'Global'
  ];

  const currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF', 'SEK', 'NOK', 'DKK'];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setJobs(mockJobs);
      setFilteredJobs(mockJobs);
      setLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    filterJobs();
  }, [filters, jobs]);

  const filterJobs = () => {
    let filtered = [...jobs];

    // Search filter
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      filtered = filtered.filter(job =>
        job.title.toLowerCase().includes(searchLower) ||
        job.description.toLowerCase().includes(searchLower) ||
        job.company.toLowerCase().includes(searchLower) ||
        job.skills.some(skill => skill.toLowerCase().includes(searchLower))
      );
    }

    // Location filter
    if (filters.location) {
      filtered = filtered.filter(job =>
        job.location.toLowerCase().includes(filters.location.toLowerCase()) ||
        job.country.toLowerCase().includes(filters.location.toLowerCase())
      );
    }

    // Remote filter
    if (filters.remote !== null) {
      filtered = filtered.filter(job => job.remote === filters.remote);
    }

    // Job type filter
    if (filters.type.length > 0) {
      filtered = filtered.filter(job => filters.type.includes(job.type));
    }

    // Category filter
    if (filters.category) {
      filtered = filtered.filter(job => job.category === filters.category);
    }

    // Experience filter
    if (filters.experience.length > 0) {
      filtered = filtered.filter(job => filters.experience.includes(job.experience));
    }

    // Salary filter
    filtered = filtered.filter(job =>
      job.salaryMax >= filters.salaryMin && job.salaryMin <= filters.salaryMax
    );

    // Region filter
    if (filters.region) {
      filtered = filtered.filter(job => job.region === filters.region);
    }

    // Sort
    filtered.sort((a, b) => {
      switch (filters.sortBy) {
        case 'date':
          return new Date(b.postedDate).getTime() - new Date(a.postedDate).getTime();
        case 'salary':
          return b.salaryMax - a.salaryMax;
        case 'rating':
          return b.rating - a.rating;
        default:
          return 0;
      }
    });

    setFilteredJobs(filtered);
  };

  const formatSalary = (min: number, max: number, currency: string) => {
    const formatter = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });
    return `${formatter.format(min)} - ${formatter.format(max)}`;
  };

  const getTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return '1 day ago';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
    return `${Math.ceil(diffDays / 30)} months ago`;
  };

  const handleJobClick = (job: Job) => {
    setSelectedJob(job);
    setShowJobDetails(true);
  };

  const handleApplyJob = (jobId: string) => {
    if (!user) {
      alert('Please log in to apply for jobs');
      return;
    }
    
    if (!userOptedIn) {
      alert('Please opt in to job search to apply for positions');
      return;
    }

    // Simulate job application
    alert('Application submitted successfully!');
  };

  const toggleOptIn = () => {
    setUserOptedIn(!userOptedIn);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Job Marketplace
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-400">
                Find your next opportunity with fair market-rate salaries
              </p>
            </div>
            
            {user && (
              <div className="flex items-center space-x-4">
                <div className="flex items-center">
                  <label className="flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={userOptedIn}
                      onChange={toggleOptIn}
                      className="sr-only"
                    />
                    <div className={`relative w-11 h-6 rounded-full transition-colors duration-200 ${
                      userOptedIn ? 'bg-blue-600' : 'bg-gray-300 dark:bg-gray-600'
                    }`}>
                      <div className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform duration-200 ${
                        userOptedIn ? 'translate-x-5' : 'translate-x-0'
                      }`}></div>
                    </div>
                    <span className="ml-3 text-sm font-medium text-gray-700 dark:text-gray-300">
                      {userOptedIn ? 'Opted In' : 'Opt In to Job Search'}
                    </span>
                  </label>
                </div>
                
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
           
(Content truncated due to size limit. Use line ranges to read in chunks)