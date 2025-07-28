import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Brain, 
  Blocks, 
  Bot, 
  Heart, 
  Truck, 
  Users, 
  ShoppingCart, 
  MessageCircle, 
  GraduationCap,
  Building,
  Shield,
  Smartphone,
  Globe,
  Zap,
  TrendingUp,
  Star,
  Play,
  Search,
  Bell,
  Settings,
  User,
  Menu,
  X,
  ChevronRight,
  Activity,
  DollarSign,
  Target,
  Award,
  Briefcase,
  Camera,
  Video,
  Mic,
  Phone,
  Mail,
  Calendar,
  FileText,
  Download,
  Upload,
  Share,
  ThumbsUp,
  MessageSquare,
  Send,
  Eye,
  Lock,
  Unlock,
  Home,
  Bookmark,
  Trending,
  Compass,
  PlusCircle,
  MoreHorizontal
} from 'lucide-react'
import './App.css'

// Mock API base URL (in production, this would be your backend URL)
const API_BASE = 'http://localhost:5000'

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [activeTab, setActiveTab] = useState('home')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [darkMode, setDarkMode] = useState(false)
  const [notifications, setNotifications] = useState(3)
  const [platformStats, setPlatformStats] = useState({
    totalUsers: 125420,
    activeProjects: 8934,
    totalRevenue: 4550000,
    coursesCompleted: 23456
  })

  // Simulate user login
  useEffect(() => {
    setCurrentUser({
      id: 'user001',
      name: 'John Doe',
      email: 'john@example.com',
      avatar: '/api/placeholder/40/40',
      role: 'Premium User',
      joinDate: '2024-01-15'
    })
  }, [])

  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    document.documentElement.classList.toggle('dark')
  }

  // Navigation items with all platform features
  const navigationItems = [
    { id: 'home', label: 'Home', icon: Home, description: 'Platform overview and dashboard' },
    { id: 'ai-hub', label: 'AI Hub', icon: Brain, description: 'Multi-model AI with virtual accelerator' },
    { id: 'blockchain', label: 'Blockchain', icon: Blocks, description: 'DeFi, NFTs, and decentralized search' },
    { id: 'robotics', label: 'Robotics', icon: Bot, description: 'Text2Robot and fleet management' },
    { id: 'healthcare', label: 'Healthcare', icon: Heart, description: 'AI diagnosis and telemedicine' },
    { id: 'supply-chain', label: 'Supply Chain', icon: Truck, description: 'Automated procurement and logistics' },
    { id: 'social', label: 'Social Media', icon: Users, description: 'Facebook-like social networking' },
    { id: 'ecommerce', label: 'E-Commerce', icon: ShoppingCart, description: 'Amazon-style marketplace' },
    { id: 'communication', label: 'Communication', icon: MessageCircle, description: 'WhatsApp/Telegram/Zoom features' },
    { id: 'learning', label: 'E-Learning', icon: GraduationCap, description: 'Udemy-like educational platform' },
    { id: 'business', label: 'Business Tools', icon: Building, description: 'ERP, CRM, and analytics' },
    { id: 'security', label: 'Security & Privacy', icon: Shield, description: 'VPN, encryption, and identity' }
  ]

  // Feature showcase data
  const featuredContent = {
    'ai-hub': {
      title: 'AI Hub - Multi-Model Intelligence',
      stats: { models: 15, accuracy: '94.2%', users: '25K+' },
      features: ['GPT-4 Integration', 'Virtual Accelerator', 'Text2Robot', 'Quantum Computing']
    },
    'blockchain': {
      title: 'Blockchain & DeFi Platform',
      stats: { tvl: '$4.55B', transactions: '2.3M', apy: '12.5%' },
      features: ['Decentralized Search', 'DeFi Protocols', 'NFT Marketplace', 'Smart Contracts']
    },
    'social': {
      title: 'Social Media Platform',
      stats: { users: '125K', posts: '2.3M', engagement: '89%' },
      features: ['News Feed', 'Communities', 'Messaging', 'Live Streaming']
    },
    'ecommerce': {
      title: 'E-Commerce Marketplace',
      stats: { products: '500K+', sellers: '15K', revenue: '$2.4M' },
      features: ['AI Search', 'Multi-Seller', 'Global Shipping', 'Secure Payments']
    }
  }

  // Render main content based on active tab
  const renderMainContent = () => {
    switch (activeTab) {
      case 'home':
        return <HomePage />
      case 'ai-hub':
        return <AIHubPage />
      case 'blockchain':
        return <BlockchainPage />
      case 'social':
        return <SocialMediaPage />
      case 'ecommerce':
        return <ECommercePage />
      case 'learning':
        return <LearningPage />
      default:
        return <ComingSoonPage feature={activeTab} />
    }
  }

  // Home Page Component
  const HomePage = () => (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-8 rounded-lg">
        <h1 className="text-4xl font-bold mb-4">Welcome to the Ultimate Unified Platform</h1>
        <p className="text-xl mb-6">Your all-in-one solution for AI, blockchain, social media, e-commerce, learning, and more!</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold">{platformStats.totalUsers.toLocaleString()}</div>
            <div className="text-sm opacity-90">Total Users</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold">{platformStats.activeProjects.toLocaleString()}</div>
            <div className="text-sm opacity-90">Active Projects</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold">${(platformStats.totalRevenue / 1000000).toFixed(1)}M</div>
            <div className="text-sm opacity-90">Total Revenue</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold">{platformStats.coursesCompleted.toLocaleString()}</div>
            <div className="text-sm opacity-90">Courses Completed</div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {navigationItems.slice(1, 5).map((item) => (
          <Card key={item.id} className="cursor-pointer hover:shadow-lg transition-shadow" onClick={() => setActiveTab(item.id)}>
            <CardHeader className="pb-3">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                  <item.icon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <CardTitle className="text-lg">{item.label}</CardTitle>
                  <CardDescription className="text-sm">{item.description}</CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>
        ))}
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <Avatar>
                <AvatarImage src="/api/placeholder/40/40" />
                <AvatarFallback>AI</AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <p className="text-sm font-medium">AI model training completed</p>
                <p className="text-xs text-muted-foreground">Supply chain optimization model achieved 94.2% accuracy</p>
              </div>
              <Badge>AI Hub</Badge>
            </div>
            <div className="flex items-center space-x-4">
              <Avatar>
                <AvatarImage src="/api/placeholder/40/40" />
                <AvatarFallback>BC</AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <p className="text-sm font-medium">New DeFi protocol launched</p>
                <p className="text-xs text-muted-foreground">Decentralized search with $4.55B TVL now live</p>
              </div>
              <Badge>Blockchain</Badge>
            </div>
            <div className="flex items-center space-x-4">
              <Avatar>
                <AvatarImage src="/api/placeholder/40/40" />
                <AvatarFallback>EC</AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <p className="text-sm font-medium">Marketplace milestone reached</p>
                <p className="text-xs text-muted-foreground">500K+ products now available from 15K sellers</p>
              </div>
              <Badge>E-Commerce</Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  // AI Hub Page Component
  const AIHubPage = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">AI Hub</h1>
        <Badge variant="secondary">15 Models Available</Badge>
      </div>

      <Tabs defaultValue="chat" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="chat">AI Chat</TabsTrigger>
          <TabsTrigger value="accelerator">Virtual Accelerator</TabsTrigger>
          <TabsTrigger value="text2robot">Text2Robot</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="chat" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Multi-Model AI Chat</CardTitle>
              <CardDescription>Chat with GPT-4, Claude, DeepSeek, and more</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {['GPT-4', 'Claude', 'DeepSeek', 'Qwen'].map((model) => (
                    <Button key={model} variant="outline" className="h-20 flex flex-col">
                      <Brain className="h-6 w-6 mb-2" />
                      {model}
                    </Button>
                  ))}
                </div>
                <div className="border rounded-lg p-4 h-64 bg-muted/50">
                  <p className="text-muted-foreground">AI chat interface would be here...</p>
                </div>
                <div className="flex space-x-2">
                  <Input placeholder="Ask anything..." className="flex-1" />
                  <Button><Send className="h-4 w-4" /></Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="accelerator" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Virtual Accelerator</CardTitle>
              <CardDescription>Ultra-low precision training: FP32 to Binary</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {['FP32', 'FP16', 'FP8', 'FP4', 'FP2', 'FP1', 'Binary'].map((precision) => (
                  <Card key={precision} className="text-center p-4">
                    <div className="text-2xl font-bold">{precision}</div>
                    <div className="text-sm text-muted-foreground">
                      {precision === 'Binary' ? '98.4% Energy Savings' : 'High Performance'}
                    </div>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="text2robot" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Text2Robot System</CardTitle>
              <CardDescription>Natural language to robot design</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Textarea placeholder="Describe the robot you want to create..." />
                <Button className="w-full">Generate Robot Design</Button>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {['Quadruped', 'Bipedal', 'Wheeled', 'Flying'].map((type) => (
                    <Card key={type} className="text-center p-4">
                      <Bot className="h-8 w-8 mx-auto mb-2" />
                      <div className="font-medium">{type}</div>
                    </Card>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Model Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">94.2%</div>
                <p className="text-muted-foreground">Average Accuracy</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Active Users</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">25,420</div>
                <p className="text-muted-foreground">Monthly Active</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Energy Savings</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">98.4%</div>
                <p className="text-muted-foreground">With Binary Training</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )

  // Blockchain Page Component
  const BlockchainPage = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Blockchain & DeFi</h1>
        <Badge variant="secondary">$4.55B TVL</Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Total Value Locked</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">$4.55B</div>
            <p className="text-muted-foreground">+12.5% APY</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Transactions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">2.3M</div>
            <p className="text-muted-foreground">This month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Search Rewards</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">$0.05</div>
            <p className="text-muted-foreground">Per search</p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="search" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="search">Decentralized Search</TabsTrigger>
          <TabsTrigger value="defi">DeFi Protocols</TabsTrigger>
          <TabsTrigger value="nft">NFT Marketplace</TabsTrigger>
          <TabsTrigger value="mining">Mining & Staking</TabsTrigger>
        </TabsList>

        <TabsContent value="search" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Privacy-Focused Search Engine</CardTitle>
              <CardDescription>Earn tokens for every search</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex space-x-2 mb-4">
                <Input placeholder="Search the decentralized web..." className="flex-1" />
                <Button><Search className="h-4 w-4" /></Button>
              </div>
              <div className="text-sm text-muted-foreground">
                Earn $0.05 in tokens for each search • Privacy protected • No tracking
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="defi" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Liquidity Pools</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>ETH/USDC</span>
                    <span className="text-green-600">15.2% APY</span>
                  </div>
                  <div className="flex justify-between">
                    <span>BTC/ETH</span>
                    <span className="text-green-600">12.8% APY</span>
                  </div>
                  <div className="flex justify-between">
                    <span>SEARCH/ETH</span>
                    <span className="text-green-600">25.5% APY</span>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Governance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="text-sm">Active Proposals: 3</div>
                  <div className="text-sm">Your Voting Power: 1,250 tokens</div>
                  <Button className="w-full">View Proposals</Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )

  // Social Media Page Component
  const SocialMediaPage = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Social Media</h1>
        <Button><PlusCircle className="h-4 w-4 mr-2" />Create Post</Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Feed */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <Avatar>
                  <AvatarImage src="/api/placeholder/40/40" />
                  <AvatarFallback>JD</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium">John Doe</p>
                  <p className="text-sm text-muted-foreground">2 hours ago</p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="mb-4">Just completed the AI course on supply chain optimization! The results are incredible - 25% cost reduction achieved. 🚀</p>
              <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                <Button variant="ghost" size="sm"><ThumbsUp className="h-4 w-4 mr-1" />42</Button>
                <Button variant="ghost" size="sm"><MessageSquare className="h-4 w-4 mr-1" />8</Button>
                <Button variant="ghost" size="sm"><Share className="h-4 w-4 mr-1" />Share</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <Avatar>
                  <AvatarImage src="/api/placeholder/40/40" />
                  <AvatarFallback>SJ</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium">Sarah Johnson</p>
                  <p className="text-sm text-muted-foreground">4 hours ago</p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="mb-4">Our robotics team just deployed the first Text2Robot system! Natural language to robot design is now reality. Check out this demo:</p>
              <div className="bg-muted rounded-lg p-4 mb-4">
                <div className="flex items-center justify-center h-32">
                  <Play className="h-12 w-12 text-muted-foreground" />
                </div>
              </div>
              <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                <Button variant="ghost" size="sm"><ThumbsUp className="h-4 w-4 mr-1" />156</Button>
                <Button variant="ghost" size="sm"><MessageSquare className="h-4 w-4 mr-1" />23</Button>
                <Button variant="ghost" size="sm"><Share className="h-4 w-4 mr-1" />Share</Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Trending Topics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm">#AIRevolution</span>
                  <Badge variant="secondary">15.2K</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">#Text2Robot</span>
                  <Badge variant="secondary">8.9K</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">#DeFiProtocols</span>
                  <Badge variant="secondary">6.1K</Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Suggested Communities</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium">AI Developers</p>
                    <p className="text-xs text-muted-foreground">25.4K members</p>
                  </div>
                  <Button size="sm">Join</Button>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium">Robotics Engineers</p>
                    <p className="text-xs text-muted-foreground">18.2K members</p>
                  </div>
                  <Button size="sm">Join</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )

  // E-Commerce Page Component
  const ECommercePage = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">E-Commerce Marketplace</h1>
        <div className="flex space-x-2">
          <Button variant="outline"><Search className="h-4 w-4" /></Button>
          <Button><ShoppingCart className="h-4 w-4 mr-2" />Cart (3)</Button>
        </div>
      </div>

      <div className="flex space-x-2 mb-6">
        <Input placeholder="Search products..." className="flex-1" />
        <Button><Search className="h-4 w-4" /></Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { name: 'AI-Powered Smart Robot', price: '$1,299.99', rating: 4.8, image: '/api/placeholder/200/200' },
          { name: 'Construction Toolkit Pro', price: '$899.99', rating: 4.9, image: '/api/placeholder/200/200' },
          { name: 'Underwater Exploration Drone', price: '$2,499.99', rating: 4.5, image: '/api/placeholder/200/200' },
          { name: 'Quantum Computing Kit', price: '$4,999.99', rating: 4.7, image: '/api/placeholder/200/200' }
        ].map((product, index) => (
          <Card key={index} className="cursor-pointer hover:shadow-lg transition-shadow">
            <div className="aspect-square bg-muted rounded-t-lg"></div>
            <CardContent className="p-4">
              <h3 className="font-medium mb-2">{product.name}</h3>
              <div className="flex items-center justify-between mb-2">
                <span className="text-lg font-bold">{product.price}</span>
                <div className="flex items-center">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-sm ml-1">{product.rating}</span>
                </div>
              </div>
              <Button className="w-full">Add to Cart</Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Marketplace Analytics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold">500K+</div>
              <div className="text-sm text-muted-foreground">Products</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">15K</div>
              <div className="text-sm text-muted-foreground">Sellers</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">$2.4M</div>
              <div className="text-sm text-muted-foreground">Monthly Revenue</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">4.7★</div>
              <div className="text-sm text-muted-foreground">Avg Rating</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  // Learning Page Component
  const LearningPage = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">E-Learning Platform</h1>
        <Button><PlusCircle className="h-4 w-4 mr-2" />Create Course</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[
          { 
            title: 'Advanced AI & Machine Learning', 
            instructor: 'Dr. John Smith', 
            price: '$199.99', 
            rating: 4.8, 
            students: '15.4K',
            duration: '45.5 hours'
          },
          { 
            title: 'Robotics Engineering', 
            instructor: 'Prof. Sarah Johnson', 
            price: '$179.99', 
            rating: 4.7, 
            students: '12.3K',
            duration: '38 hours'
          },
          { 
            title: 'Blockchain Development', 
            instructor: 'Alex Chen', 
            price: '$159.99', 
            rating: 4.9, 
            students: '9.8K',
            duration: '32 hours'
          }
        ].map((course, index) => (
          <Card key={index} className="cursor-pointer hover:shadow-lg transition-shadow">
            <div className="aspect-video bg-muted rounded-t-lg"></div>
            <CardContent className="p-4">
              <h3 className="font-medium mb-2">{course.title}</h3>
              <p className="text-sm text-muted-foreground mb-2">by {course.instructor}</p>
              <div className="flex items-center justify-between mb-2">
                <span className="text-lg font-bold">{course.price}</span>
                <div className="flex items-center">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-sm ml-1">{course.rating}</span>
                </div>
              </div>
              <div className="flex justify-between text-xs text-muted-foreground mb-3">
                <span>{course.students} students</span>
                <span>{course.duration}</span>
              </div>
              <Button className="w-full">Enroll Now</Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Your Learning Progress</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">AI & Machine Learning</span>
                <span className="text-sm text-muted-foreground">75%</span>
              </div>
              <Progress value={75} />
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Robotics Engineering</span>
                <span className="text-sm text-muted-foreground">45%</span>
              </div>
              <Progress value={45} />
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Blockchain Development</span>
                <span className="text-sm text-muted-foreground">20%</span>
              </div>
              <Progress value={20} />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  // Coming Soon Page Component
  const ComingSoonPage = ({ feature }) => (
    <div className="flex flex-col items-center justify-center h-64 space-y-4">
      <div className="text-6xl">🚀</div>
      <h2 className="text-2xl font-bold">Coming Soon</h2>
      <p className="text-muted-foreground text-center max-w-md">
        The {feature.replace('-', ' ')} feature is currently under development. 
        Stay tuned for amazing updates!
      </p>
      <Button>Get Notified</Button>
    </div>
  )

  return (
    <div className={`min-h-screen bg-background ${darkMode ? 'dark' : ''}`}>
      {/* Top Navigation */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="flex h-16 items-center px-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="mr-4"
          >
            <Menu className="h-5 w-5" />
          </Button>
          
          <div className="flex items-center space-x-2 flex-1">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <span className="font-bold text-xl">Ultimate Platform</span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="sm" onClick={toggleDarkMode}>
              {darkMode ? '☀️' : '🌙'}
            </Button>
            <Button variant="ghost" size="sm" className="relative">
              <Bell className="h-5 w-5" />
              {notifications > 0 && (
                <Badge className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 text-xs">
                  {notifications}
                </Badge>
              )}
            </Button>
            <Avatar className="h-8 w-8">
              <AvatarImage src={currentUser?.avatar} />
              <AvatarFallback>{currentUser?.name?.split(' ').map(n => n[0]).join('')}</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 overflow-hidden border-r bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60`}>
          <div className="p-4 space-y-2">
            {navigationItems.map((item) => (
              <Button
                key={item.id}
                variant={activeTab === item.id ? "default" : "ghost"}
                className="w-full justify-start"
                onClick={() => setActiveTab(item.id)}
              >
                <item.icon className="h-4 w-4 mr-3" />
                {item.label}
              </Button>
            ))}
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {renderMainContent()}
        </main>
      </div>
    </div>
  )
}

export default App

