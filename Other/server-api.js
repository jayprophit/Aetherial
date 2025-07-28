// src/api/index.js
// Core API router for SoundSync Hub server

const express = require('express');
const morgan = require('morgan');
const helmet = require('helmet');
const cors = require('cors');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const mongoose = require('mongoose');
const passport = require('passport');
const { Strategy: JwtStrategy, ExtractJwt } = require('passport-jwt');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

// Import routes
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const speakerRoutes = require('./routes/speakers');
const sessionRoutes = require('./routes/sessions');
const subscriptionRoutes = require('./routes/subscriptions');
const contentRoutes = require('./routes/content');
const socialRoutes = require('./routes/social');

// Import middleware
const { errorHandler } = require('./middleware/errorHandler');
const { authenticate } = require('./middleware/authenticate');

// Import models
const User = require('./models/User');

// Load environment variables
require('dotenv').config();

// Initialize Express app
const app = express();
const router = express.Router();

// Configure Swagger documentation
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'SoundSync Hub API',
      version: '1.0.0',
      description: 'API for SoundSync Hub multi-speaker audio synchronization platform',
    },
    servers: [
      {
        url: process.env.API_URL || 'http://localhost:5000/api/v1',
        description: 'Development server',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
        },
      },
    },
    security: [
      {
        bearerAuth: [],
      },
    ],
  },
  apis: ['./routes/*.js', './models/*.js'],
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);

// Configure passport JWT strategy
const jwtOptions = {
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  secretOrKey: process.env.JWT_SECRET || 'your-secret-key',
};

passport.use(
  new JwtStrategy(jwtOptions, async (jwtPayload, done) => {
    try {
      const user = await User.findById(jwtPayload.id);
      
      if (user) {
        return done(null, user);
      }
      
      return done(null, false);
    } catch (error) {
      return done(error, false);
    }
  })
);

// Configure middleware
app.use(helmet());
app.use(compression());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));
app.use(passport.initialize());

// Configure rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
});

// Apply rate limiting to all routes
app.use(limiter);

// API routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/users', authenticate, userRoutes);
app.use('/api/v1/speakers', authenticate, speakerRoutes);
app.use('/api/v1/sessions', authenticate, sessionRoutes);
app.use('/api/v1/subscriptions', authenticate, subscriptionRoutes);
app.use('/api/v1/content', authenticate, contentRoutes);
app.use('/api/v1/social', authenticate, socialRoutes);

// Swagger documentation route
app.use('/api/v1/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// Health check route
app.get('/api/v1/health', (req, res) => {
  res.status(200).json({
    status: 'success',
    message: 'SoundSync Hub API is running',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
  });
});

// Error handling middleware
app.use(errorHandler);

// Connect to MongoDB
mongoose
  .connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/soundsync-hub', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch((err) => {
    console.error('MongoDB connection error:', err);
    process.exit(1);
  });

// WebSocket setup for real-time communication
const setupWebsocket = (server) => {
  const io = require('socket.io')(server, {
    cors: {
      origin: process.env.CLIENT_URL || '*',
      methods: ['GET', 'POST'],
    },
  });

  // Socket.io middleware for authentication
  io.use(async (socket, next) => {
    const token = socket.handshake.auth.token;
    
    if (!token) {
      return next(new Error('Authentication error'));
    }
    
    try {
      // Verify JWT token
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      const user = await User.findById(decoded.id);
      
      if (!user) {
        return next(new Error('User not found'));
      }
      
      socket.user = user;
      next();
    } catch (error) {
      return next(new Error('Authentication error'));
    }
  });

  // Handle WebSocket connections
  io.on('connection', (socket) => {
    console.log(`User connected: ${socket.user.email}`);
    
    // Join user's own room for private messages
    socket.join(`user:${socket.user._id}`);
    
    // Handle session events
    socket.on('session:join', async (sessionId) => {
      try {
        // Verify session exists and user has access
        const session = await Session.findById(sessionId);
        
        if (!session) {
          socket.emit('error', { message: 'Session not found' });
          return;
        }
        
        // Join session room
        socket.join(`session:${sessionId}`);
        console.log(`User ${socket.user.email} joined session ${sessionId}`);
        
        // Notify others in the session
        socket.to(`session:${sessionId}`).emit('user:joined', {
          userId: socket.user._id,
          username: socket.user.username,
        });
        
        // Send current session state to the user
        socket.emit('session:state', {
          id: session._id,
          name: session.name,
          owner: session.owner,
          speakers: session.speakers,
          currentTrack: session.currentTrack,
          isPlaying: session.isPlaying,
          participants: await getSessionParticipants(sessionId),
        });
      } catch (error) {
        socket.emit('error', { message: 'Failed to join session' });
      }
    });
    
    // Handle speaker events
    socket.on('speaker:connect', (data) => {
      const { sessionId, speaker } = data;
      
      // Broadcast to all users in the session
      io.to(`session:${sessionId}`).emit('speaker:connected', {
        userId: socket.user._id,
        speaker,
      });
    });
    
    socket.on('speaker:disconnect', (data) => {
      const { sessionId, speakerId } = data;
      
      // Broadcast to all users in the session
      io.to(`session:${sessionId}`).emit('speaker:disconnected', {
        userId: socket.user._id,
        speakerId,
      });
    });
    
    // Handle playback events
    socket.on('playback:play', (data) => {
      const { sessionId, track } = data;
      
      // Broadcast to all users in the session
      io.to(`session:${sessionId}`).emit('playback:playing', {
        userId: socket.user._id,
        track,
        timestamp: Date.now(),
      });
    });
    
    socket.on('playback:pause', (data) => {
      const { sessionId } = data;
      
      // Broadcast to all users in the session
      io.to(`session:${sessionId}`).emit('playback:paused', {
        userId: socket.user._id,
        timestamp: Date.now(),
      });
    });
    
    socket.on('playback:seek', (data) => {
      const { sessionId, position } = data;
      
      // Broadcast to all users in the session
      io.to(`session:${sessionId}`).emit('playback:seek', {
        userId: socket.user._id,
        position,
        timestamp: Date.now(),
      });
    });
    
    // Handle volume events
    socket.on('volume:change', (data) => {
      const { sessionId, speakerId, volume } = data;
      
      // Broadcast to all users in the session
      io.to(`session:${sessionId}`).emit('volume:changed', {
        userId: socket.user._id,
        speakerId,
        volume,
      });
    });
    
    // Handle latency sync events
    socket.on('sync:latency', (data) => {
      const { sessionId, measurements } = data;
      
      // Broadcast to all users in the session
      io.to(`session:${sessionId}`).emit('sync:update', {
        userId: socket.user._id,
        measurements,
        timestamp: Date.now(),
      });
    });
    
    // Handle disconnect
    socket.on('disconnect', async () => {
      console.log(`User disconnected: ${socket.user.email}`);
      
      // Find all sessions the user is in
      const userSessions = await getUserSessions(socket.user._id);
      
      // Notify others in each session
      userSessions.forEach((sessionId) => {
        socket.to(`session:${sessionId}`).emit('user:left', {
          userId: socket.user._id,
          username: socket.user.username,
        });
      });
    });
  });

  return io;
};

// Helper to get session participants
async function getSessionParticipants(sessionId) {
  // This would be implemented to get all users in a session
  return [];
}

// Helper to get user's sessions
async function getUserSessions(userId) {
  // This would be implemented to get all sessions a user is in
  return [];
}

// Export the app and WebSocket setup function
module.exports = { app, setupWebsocket };
