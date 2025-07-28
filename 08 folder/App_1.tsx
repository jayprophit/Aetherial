import { useState, useEffect } from 'react';
import { 
  Brain, 
  Zap, 
  Shield, 
  Globe, 
  Cpu, 
  Database, 
  Cloud,
  Users,
  ShoppingCart,
  GraduationCap,
  Briefcase,
  Code,
  Palette,
  Gamepad2,
  ChevronDown,
  Menu,
  X,
  ArrowRight,
  CheckCircle,
  Sparkles,
  Rocket,
  Lock,
  Infinity
} from 'lucide-react';
import './App.css';

const UnifiedPlatform = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrollY, setScrollY] = useState(0);
  const [currentFeature, setCurrentFeature] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % features.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "Quantum Virtual Assistant",
      description: "3D avatar interface with advanced AI capabilities and emotional intelligence"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Social Network Hub",
      description: "Unified interface for 31+ social media platforms with cross-posting"
    },
    {
      icon: <ShoppingCart className="w-8 h-8" />,
      title: "E-commerce Marketplace",
      description: "Multi-vendor platform with AI optimization and global commerce"
    },
    {
      icon: <GraduationCap className="w-8 h-8" />,
      title: "Education Hub",
      description: "World-class LMS with AI-powered personalization and blockchain certificates"
    },
    {
      icon: <Briefcase className="w-8 h-8" />,
      title: "Job Marketplace",
      description: "AI-powered matching with 85%+ accuracy and comprehensive career tools"
    },
    {
      icon: <Code className="w-8 h-8" />,
      title: "Developer Tools",
      description: "Multi-language IDE with AI assistance and deployment automation"
    },
    {
      icon: <Palette className="w-8 h-8" />,
      title: "Store & Page Builder",
      description: "Professional website creation with drag-and-drop interface"
    },
    {
      icon: <Gamepad2 className="w-8 h-8" />,
      title: "Metaverse Module",
      description: "Virtual worlds with NFT integration and physics simulation"
    }
  ];

  const stats = [
    { number: "10M+", label: "Concurrent Users" },
    { number: "99.99%", label: "Uptime" },
    { number: "<100ms", label: "Response Time" },
    { number: "31+", label: "Platform Integrations" }
  ];

  const technologies = [
    { name: "Quantum Computing", icon: <Cpu className="w-6 h-6" /> },
    { name: "AI & Machine Learning", icon: <Brain className="w-6 h-6" /> },
    { name: "Blockchain", icon: <Database className="w-6 h-6" /> },
    { name: "Cloud Native", icon: <Cloud className="w-6 h-6" /> },
    { name: "Edge Computing", icon: <Zap className="w-6 h-6" /> },
    { name: "Quantum Security", icon: <Shield className="w-6 h-6" /> }
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white overflow-x-hidden">
      {/* Scroll Progress Indicator */}
      <div 
        className="scroll-indicator"
        style={{ transform: `scaleX(${scrollY / (document.body.scrollHeight - window.innerHeight)})` }}
      />

      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass-effect">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Infinity className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gradient">Unified Platform</span>
            </div>
            
            <div className="hidden md:flex space-x-8">
              <a href="#features" className="hover:text-blue-400 transition-colors">Features</a>
              <a href="#technology" className="hover:text-blue-400 transition-colors">Technology</a>
              <a href="#enterprise" className="hover:text-blue-400 transition-colors">Enterprise</a>
              <a href="#contact" className="hover:text-blue-400 transition-colors">Contact</a>
            </div>

            <button
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden glass-effect">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <a href="#features" className="block px-3 py-2 hover:text-blue-400">Features</a>
              <a href="#technology" className="block px-3 py-2 hover:text-blue-400">Technology</a>
              <a href="#enterprise" className="block px-3 py-2 hover:text-blue-400">Enterprise</a>
              <a href="#contact" className="block px-3 py-2 hover:text-blue-400">Contact</a>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center gradient-bg">
        <div className="absolute inset-0 blockchain-grid opacity-20"></div>
        <div className="relative z-10 text-center px-4 max-w-6xl mx-auto">
          <div className="float-animation mb-8">
            <div className="w-32 h-32 mx-auto bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full flex items-center justify-center quantum-glow">
              <Brain className="w-16 h-16 text-white ai-pulse" />
            </div>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="text-gradient">Unified Platform</span>
          </h1>
          
          <p className="text-xl md:text-2xl mb-8 typing-effect">
            Next-Generation Digital Infrastructure
          </p>
          
          <p className="text-lg md:text-xl text-gray-300 mb-12 max-w-4xl mx-auto">
            Revolutionary AI-powered platform combining social networking, e-commerce, education, 
            blockchain, quantum computing, and metaverse capabilities in one comprehensive ecosystem.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-4 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-all hover-lift pulse-glow">
              Explore Platform
              <ArrowRight className="inline ml-2 w-5 h-5" />
            </button>
            <button className="px-8 py-4 border border-white/20 hover:border-white/40 rounded-lg font-semibold transition-all hover-lift glass-effect">
              Watch Demo
            </button>
          </div>
        </div>
        
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <ChevronDown className="w-8 h-8 text-white/60" />
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gray-800/50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl md:text-5xl font-bold text-gradient mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="text-gradient">Platform Features</span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Comprehensive suite of integrated modules designed to revolutionize 
              how you work, learn, create, and connect in the digital world.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div 
                key={index} 
                className={`feature-card rounded-xl p-6 hover-lift quantum-border ${
                  index === currentFeature ? 'quantum-glow' : ''
                }`}
              >
                <div className="text-blue-400 mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section id="technology" className="py-20 bg-gray-800/30">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="text-gradient">Cutting-Edge Technology</span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Built on the latest advancements in quantum computing, artificial intelligence, 
              and distributed systems for unparalleled performance and security.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {technologies.map((tech, index) => (
              <div key={index} className="feature-card rounded-xl p-8 text-center hover-lift">
                <div className="text-purple-400 mb-4 flex justify-center">
                  {tech.icon}
                </div>
                <h3 className="text-xl font-semibold">{tech.name}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Enterprise Section */}
      <section id="enterprise" className="py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold mb-6">
                <span className="text-gradient">Enterprise Ready</span>
              </h2>
              <p className="text-xl text-gray-300 mb-8">
                Scalable, secure, and compliant infrastructure designed for 
                organizations of all sizes, from startups to Fortune 500 companies.
              </p>
              
              <div className="space-y-4">
                {[
                  "99.99% Uptime SLA",
                  "Quantum-Safe Security",
                  "Global CDN Network",
                  "24/7 Expert Support",
                  "SOC 2 & ISO 27001 Compliant",
                  "Auto-Scaling Infrastructure"
                ].map((item, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-400" />
                    <span className="text-lg">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="relative">
              <div className="security-shield">
                <div className="security-shield-inner text-center">
                  <Lock className="w-16 h-16 mx-auto mb-4 text-blue-400" />
                  <h3 className="text-2xl font-bold mb-2">Quantum Security</h3>
                  <p className="text-gray-400">
                    Advanced encryption and biometric authentication 
                    with quantum-resistant algorithms.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4">
          <Sparkles className="w-16 h-16 mx-auto mb-6 text-white" />
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Transform Your Digital Experience?
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of organizations already using the Unified Platform 
            to revolutionize their digital operations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-4 bg-white text-blue-600 hover:bg-gray-100 rounded-lg font-semibold transition-all hover-lift">
              Start Free Trial
              <Rocket className="inline ml-2 w-5 h-5" />
            </button>
            <button className="px-8 py-4 border border-white/20 hover:border-white/40 rounded-lg font-semibold transition-all hover-lift text-white">
              Schedule Demo
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="py-16 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Infinity className="w-6 h-6 text-white" />
                </div>
                <span className="text-xl font-bold text-gradient">Unified Platform</span>
              </div>
              <p className="text-gray-400 mb-6 max-w-md">
                The next generation of digital infrastructure, combining AI, quantum computing, 
                and blockchain technology in one comprehensive platform.
              </p>
              <div className="flex space-x-4">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                    <Globe className="w-5 h-5" />
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Platform</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Docs</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2025 Unified Platform
(Content truncated due to size limit. Use line ranges to read in chunks)