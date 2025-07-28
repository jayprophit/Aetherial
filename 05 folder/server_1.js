// This file sets up the deployment configuration for the demo preview

const express = require('express');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');
const authRoutes = require('./api/auth');

// Create Express app
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// API Routes
app.use('/api/auth', authRoutes);

// Basic API routes for demo
app.get('/api/social/posts', (req, res) => {
  // Mock data for social posts
  const posts = [
    {
      id: '1',
      user: {
        id: '1',
        name: 'Demo User',
        avatar: 'https://via.placeholder.com/40'
      },
      content: 'Excited to try out this new unified platform! The integration between social, e-commerce, and learning looks promising.',
      likes: 24,
      comments: 5,
      createdAt: '2025-05-18T14:22:00Z'
    },
    {
      id: '2',
      user: {
        id: '2',
        name: 'Jane Smith',
        avatar: 'https://via.placeholder.com/40'
      },
      content: 'Just completed an amazing course on AI development. The platform made it so easy to learn and apply the concepts immediately.',
      likes: 42,
      comments: 8,
      createdAt: '2025-05-18T12:15:00Z'
    },
    {
      id: '3',
      user: {
        id: '3',
        name: 'Alex Johnson',
        avatar: 'https://via.placeholder.com/40'
      },
      content: 'Found an incredible product through the AI recommendation engine. It knew exactly what I needed before I did!',
      likes: 18,
      comments: 3,
      createdAt: '2025-05-18T10:05:00Z'
    }
  ];
  
  res.json({ posts });
});

app.get('/api/ecommerce/products', (req, res) => {
  // Mock data for products
  const products = [
    {
      id: '1',
      name: 'Smart Home Hub',
      description: 'Control all your smart devices from one central hub with AI assistance.',
      price: 129.99,
      rating: 4.7,
      imageUrl: 'https://via.placeholder.com/300',
      category: 'Electronics',
      stock: 15
    },
    {
      id: '2',
      name: 'Learning Tablet Pro',
      description: 'The perfect tablet for e-learning with adaptive AI tutoring built in.',
      price: 349.99,
      rating: 4.9,
      imageUrl: 'https://via.placeholder.com/300',
      category: 'Education',
      stock: 8
    },
    {
      id: '3',
      name: 'Professional Camera Kit',
      description: 'Everything you need to start your photography or content creation journey.',
      price: 899.99,
      rating: 4.8,
      imageUrl: 'https://via.placeholder.com/300',
      category: 'Photography',
      stock: 5
    }
  ];
  
  res.json({ products });
});

app.get('/api/learning/courses', (req, res) => {
  // Mock data for courses
  const courses = [
    {
      id: '1',
      title: 'Introduction to AI Development',
      description: 'Learn the fundamentals of artificial intelligence and machine learning.',
      instructor: 'Dr. Alan Turing',
      duration: '8 weeks',
      level: 'Beginner',
      rating: 4.9,
      enrollments: 1245,
      imageUrl: 'https://via.placeholder.com/300',
      category: 'technology',
      price: 49.99
    },
    {
      id: '2',
      title: 'Advanced Web Development',
      description: 'Master modern web technologies and frameworks for building scalable applications.',
      instructor: 'Sarah Johnson',
      duration: '10 weeks',
      level: 'Intermediate',
      rating: 4.7,
      enrollments: 983,
      imageUrl: 'https://via.placeholder.com/300',
      category: 'technology',
      price: 59.99
    },
    {
      id: '3',
      title: 'Digital Marketing Mastery',
      description: 'Comprehensive guide to digital marketing strategies and analytics.',
      instructor: 'Michael Chen',
      duration: '6 weeks',
      level: 'All Levels',
      rating: 4.8,
      enrollments: 1567,
      imageUrl: 'https://via.placeholder.com/300',
      category: 'business',
      price: 39.99
    }
  ];
  
  res.json({ courses });
});

app.get('/api/jobs/listings', (req, res) => {
  // Mock data for job listings
  const jobs = [
    {
      id: '1',
      title: 'Full Stack Developer',
      company: 'Tech Innovations Inc.',
      location: 'San Francisco, CA (Remote)',
      salary: '$120,000 - $150,000',
      description: 'Seeking an experienced full stack developer to join our growing team.',
      requirements: ['5+ years experience', 'React', 'Node.js', 'PostgreSQL'],
      postedAt: '2025-05-15T09:00:00Z',
      category: 'development'
    },
    {
      id: '2',
      title: 'AI Research Scientist',
      company: 'Future AI Labs',
      location: 'Boston, MA',
      salary: '$150,000 - $180,000',
      description: 'Join our cutting-edge research team developing next-generation AI models.',
      requirements: ['PhD in Computer Science or related field', 'Machine Learning expertise', 'PyTorch or TensorFlow'],
      postedAt: '2025-05-16T14:30:00Z',
      category: 'ai'
    },
    {
      id: '3',
      title: 'UX/UI Designer',
      company: 'Creative Digital Agency',
      location: 'Remote',
      salary: '$90,000 - $110,000',
      description: 'Design beautiful and intuitive user experiences for our clients.',
      requirements: ['3+ years experience', 'Figma', 'User Research', 'Prototyping'],
      postedAt: '2025-05-17T11:15:00Z',
      category: 'design'
    }
  ];
  
  res.json({ jobs });
});

app.get('/api/ai/assistant', (req, res) => {
  // Mock AI assistant response
  const query = req.query.query || '';
  
  const response = {
    text: `This is a demo response from the AI assistant for query: "${query}". In the full implementation, this would be generated by the multi-model AI system with contextual awareness of the platform features and user preferences.`,
    suggestions: [
      'Tell me more about the e-learning courses',
      'How does the job marketplace work?',
      'Show me popular products'
    ]
  };
  
  // Simulate processing time
  setTimeout(() => {
    res.json(response);
  }, 500);
});

// Serve static files from the frontend build directory in production
if (process.env.NODE_ENV === 'production') {
  // Serve static files
  app.use(express.static(path.join(__dirname, '../../frontend/build')));

  // Handle React routing, return all requests to React app
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../../frontend/build', 'index.html'));
  });
}

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;
