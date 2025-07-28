import React, { createContext, useState, useEffect, useContext } from 'react';

// Create Authentication Context
const AuthContext = createContext(null);

// Authentication Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [ageVerified, setAgeVerified] = useState(false);
  const [kycStatus, setKycStatus] = useState('none'); // 'none', 'pending', 'verified'
  const [userRestrictions, setUserRestrictions] = useState({
    isMinor: false,
    noKyc: true,
    contentRestrictions: 'general', // 'general', 'restricted', 'educational'
    digitalAssetLocked: false
  });

  // Initialize auth state
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Check for token in localStorage
        const token = localStorage.getItem('auth_token');
        
        if (token) {
          // In a real implementation, this would validate the token with the backend
          // For demo purposes, we'll simulate a successful auth
          const mockUser = {
            id: '1',
            username: 'demo_user',
            email: 'demo@example.com',
            firstName: 'Demo',
            lastName: 'User',
            displayName: 'Demo User',
            avatar: 'https://via.placeholder.com/150',
            role: 'user',
            createdAt: new Date().toISOString()
          };
          
          setUser(mockUser);
          
          // Simulate age verification and KYC status
          setAgeVerified(true);
          setKycStatus('verified');
          setUserRestrictions({
            isMinor: false,
            noKyc: false,
            contentRestrictions: 'general',
            digitalAssetLocked: false
          });
        }
      } catch (err) {
        console.error('Authentication error:', err);
        setError('Failed to authenticate');
        // Clear any invalid tokens
        localStorage.removeItem('auth_token');
      } finally {
        setLoading(false);
      }
    };
    
    checkAuth();
  }, []);

  // Login function
  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      // In a real implementation, this would call the backend API
      // For demo purposes, we'll simulate a successful login
      const mockUser = {
        id: '1',
        username: 'demo_user',
        email,
        firstName: 'Demo',
        lastName: 'User',
        displayName: 'Demo User',
        avatar: 'https://via.placeholder.com/150',
        role: 'user',
        createdAt: new Date().toISOString()
      };
      
      // Simulate successful login
      localStorage.setItem('auth_token', 'mock_token_12345');
      setUser(mockUser);
      
      // Simulate age verification check
      const isAdult = true; // This would be determined by KYC process
      setAgeVerified(isAdult);
      
      // Set KYC status
      setKycStatus('verified');
      
      // Set user restrictions based on age and KYC
      setUserRestrictions({
        isMinor: !isAdult,
        noKyc: false,
        contentRestrictions: isAdult ? 'general' : 'restricted',
        digitalAssetLocked: !isAdult
      });
      
      return { success: true };
    } catch (err) {
      console.error('Login error:', err);
      setError('Invalid credentials');
      return { success: false, error: 'Invalid credentials' };
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      
      // In a real implementation, this would call the backend API
      // For demo purposes, we'll simulate a successful registration
      const { email, password, firstName, lastName, dateOfBirth } = userData;
      
      // Calculate age from date of birth
      const birthDate = new Date(dateOfBirth);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      
      const isAdult = age >= 18;
      const isMinor = age < 18;
      const isUnder13 = age < 13;
      
      // Create mock user
      const mockUser = {
        id: Date.now().toString(),
        username: `${firstName.toLowerCase()}_${lastName.toLowerCase()}`,
        email,
        firstName,
        lastName,
        displayName: `${firstName} ${lastName}`,
        avatar: 'https://via.placeholder.com/150',
        role: 'user',
        createdAt: new Date().toISOString(),
        dateOfBirth,
        age
      };
      
      // Set age verification status
      setAgeVerified(true); // We know their age from registration
      
      // Set KYC status - initially none for new users
      setKycStatus('none');
      
      // Set user restrictions based on age
      setUserRestrictions({
        isMinor,
        noKyc: true,
        contentRestrictions: isUnder13 ? 'educational' : (isMinor ? 'restricted' : 'general'),
        digitalAssetLocked: isMinor
      });
      
      // Simulate successful registration
      localStorage.setItem('auth_token', 'mock_token_' + Date.now());
      setUser(mockUser);
      
      return { success: true };
    } catch (err) {
      console.error('Registration error:', err);
      setError('Registration failed');
      return { success: false, error: 'Registration failed' };
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
    setAgeVerified(false);
    setKycStatus('none');
    setUserRestrictions({
      isMinor: false,
      noKyc: true,
      contentRestrictions: 'general',
      digitalAssetLocked: false
    });
  };

  // Start KYC verification process
  const startKycVerification = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      
      // In a real implementation, this would call the KYC provider API
      // For demo purposes, we'll simulate a pending KYC status
      setKycStatus('pending');
      
      // Simulate KYC processing time
      setTimeout(() => {
        // Simulate successful KYC verification
        setKycStatus('verified');
        
        // Update user restrictions based on verified age
        const isAdult = userData.age >= 18;
        const isMinor = userData.age < 18;
        
        setUserRestrictions({
          isMinor,
          noKyc: false,
          contentRestrictions: isMinor ? 'restricted' : 'general',
          digitalAssetLocked: isMinor
        });
      }, 3000);
      
      return { success: true, status: 'pending' };
    } catch (err) {
      console.error('KYC verification error:', err);
      setError('KYC verification failed');
      return { success: false, error: 'KYC verification failed' };
    } finally {
      setLoading(false);
    }
  };

  // Check content access based on age and KYC status
  const checkContentAccess = (contentType) => {
    // Content types: 'general', 'age_restricted', 'educational', 'financial'
    
    switch (contentType) {
      case 'general':
        return true; // Everyone can access general content
        
      case 'age_restricted':
        // Only verified adults can access age-restricted content
        return ageVerified && !userRestrictions.isMinor;
        
      case 'educational':
        // Educational content is available to all, but minors get a filtered version
        return true;
        
      case 'financial':
        // Financial services require KYC verification and adult status
        return kycStatus === 'verified' && !userRestrictions.isMinor;
        
      default:
        return true;
    }
  };

  // Check if user can access digital assets (tokens, rewards, etc.)
  const canAccessDigitalAssets = () => {
    return !userRestrictions.digitalAssetLocked;
  };

  // Value object to be provided by context
  const value = {
    user,
    loading,
    error,
    ageVerified,
    kycStatus,
    userRestrictions,
    login,
    register,
    logout,
    startKycVerification,
    checkContentAccess,
    canAccessDigitalAssets
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
