const express = require('express');
const path = require('path');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3002; // Changed from 3001 to 3002
// Enable CORS
app.use(cors());
// Parse JSON bodies
app.use(express.json());
// Mock API endpoints
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', mode: 'demo' });
});
// Mock user data
const users = [
  { id: 'user-1', name: 'Demo User', email: 'demo@example.com', age: 25, isKYCVerified: true },
  { id: 'user-2', name: 'Young User', email: 'young@example.com', age: 16, isKYCVerified: false },
];
// Mock digital assets
const digitalAssets = {
  'user-1': {
    totalValue: 5000,
    lockedValue: 0,
    stakedValue: 1500,
    assets: [
      {
        id: 'asset-1',
        name: 'Premium Token',
        type: 'Token',
        description: 'Platform premium token',
        value: 2500,
        status: 'ACTIVE'
      },
      {
        id: 'asset-2',
        name: 'Staked Rewards',
        type: 'Stake',
        description: 'Staked reward points',
        value: 1500,
        status: 'STAKED'
      },
      {
        id: 'asset-3',
        name: 'Demo NFT',
        type: 'NFT',
        description: 'Demonstration NFT asset',
        value: 1000,
        status: 'ACTIVE'
      }
    ]
  },
  'user-2': {
    totalValue: 1200,
    lockedValue: 1200,
    stakedValue: 0,
    assets: [
      {
        id: 'asset-4',
        name: 'Youth Rewards',
        type: 'Token',
        description: 'Locked rewards for underage user',
        value: 1200,
        status: 'LOCKED',
        lockInfo: {
          lockedUntil: new Date(Date.now() + 63072000000).toISOString(), // 2 years in the future
          reason: 'Age restriction - unlocks at 18'
        }
      }
    ]
  }
};
// User endpoints
app.get('/api/users/:userId', (req, res) => {
  const user = users.find(u => u.id === req.params.userId);
  if (user) {
    res.json(user);
  } else {
    res.status(404).json({ error: 'User not found' });
  }
});
// Digital assets endpoints
app.get('/api/assets/:userId', (req, res) => {
  const assets = digitalAssets[req.params.userId];
  if (assets) {
    res.json(assets);
  } else {
    res.status(404).json({ error: 'Assets not found' });
  }
});
// Content moderation endpoints
app.post('/api/moderation/check', (req, res) => {
  const { content, contentType, userAge } = req.body;
  
  // Simple mock moderation logic
  const hasInappropriateContent = content && (
    content.toLowerCase().includes('inappropriate') || 
    content.toLowerCase().includes('adult') ||
    content.toLowerCase().includes('violence')
  );
  
  const isAgeRestricted = userAge < 18 && (
    content.toLowerCase().includes('mature') ||
    content.toLowerCase().includes('advanced')
  );
  
  res.json({
    isApproved: !hasInappropriateContent && !isAgeRestricted,
    contentRating: hasInappropriateContent ? 'Adult' : isAgeRestricted ? 'Teen' : 'Everyone',
    moderationAction: hasInappropriateContent ? 'Block' : isAgeRestricted ? 'Age-restrict' : 'Allow',
    reason: hasInappropriateContent ? 'Inappropriate content detected' : 
            isAgeRestricted ? 'Content not suitable for users under 18' : '',
    ageRestriction: hasInappropriateContent ? 18 : isAgeRestricted ? 18 : 0,
    moderationId: 'mod-' + Date.now()
  });
});
// AI business agent endpoints
app.post('/api/ai/question', (req, res) => {
  const { question } = req.body;
  
  // Mock AI responses
  const responses = {
    'sales': 'To improve sales, consider optimizing your product listings, implementing targeted promotions, and leveraging customer data for personalized marketing campaigns.',
    'inventory': 'Effective inventory management involves regular stock audits, implementing just-in-time ordering, and using predictive analytics to forecast demand.',
    'customer': 'To enhance customer service, focus on quick response times, personalized interactions, and proactive issue resolution.',
    'default': 'I can help you with sales, inventory management, customer service, digital assets, and other business operations. Please ask a specific question.'
  };
  
  let response = responses.default;
  
  if (question.toLowerCase().includes('sales')) {
    response = responses.sales;
  } else if (question.toLowerCase().includes('inventory')) {
    response = responses.inventory;
  } else if (question.toLowerCase().includes('customer')) {
    response = responses.customer;
  }
  
  res.json({ answer: response });
});
// Serve static frontend in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../frontend')));
  
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
  });
}
app.listen(PORT, () => {
  console.log(`Demo server running on port ${PORT}`);
});
