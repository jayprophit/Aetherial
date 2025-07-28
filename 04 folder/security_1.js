// Security utilities for the Unified Platform
import { useState, useEffect, useCallback } from 'react';
import CryptoJS from 'crypto-js';

/**
 * Custom hook for managing authentication tokens securely
 * @returns {Object} Authentication utilities
 */
export const useSecureAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  // Check authentication status on mount
  useEffect(() => {
    const token = getSecureToken();
    if (token) {
      validateToken(token)
        .then(valid => {
          setIsAuthenticated(valid);
        })
        .catch(() => {
          setIsAuthenticated(false);
          clearSecureToken();
        });
    }
  }, []);
  
  // Store token securely
  const setSecureToken = useCallback((token, expiresIn = 3600) => {
    if (!token) return false;
    
    try {
      // Encrypt token before storing
      const encryptedToken = encryptData(token);
      
      // Calculate expiry time
      const expiryTime = Date.now() + expiresIn * 1000;
      
      // Store in sessionStorage with expiry
      const tokenData = JSON.stringify({
        token: encryptedToken,
        expires: expiryTime
      });
      
      sessionStorage.setItem('auth_token', tokenData);
      setIsAuthenticated(true);
      return true;
    } catch (error) {
      console.error('Error storing token:', error);
      return false;
    }
  }, []);
  
  // Retrieve token
  const getSecureToken = useCallback(() => {
    try {
      const tokenData = sessionStorage.getItem('auth_token');
      if (!tokenData) return null;
      
      const { token, expires } = JSON.parse(tokenData);
      
      // Check if token has expired
      if (Date.now() > expires) {
        clearSecureToken();
        return null;
      }
      
      // Decrypt token
      return decryptData(token);
    } catch (error) {
      console.error('Error retrieving token:', error);
      return null;
    }
  }, []);
  
  // Clear token
  const clearSecureToken = useCallback(() => {
    sessionStorage.removeItem('auth_token');
    setIsAuthenticated(false);
  }, []);
  
  // Validate token with backend
  const validateToken = useCallback(async (token) => {
    // In a real implementation, this would make an API call to validate the token
    // For demo purposes, we'll just check if the token exists
    return !!token;
  }, []);
  
  return {
    isAuthenticated,
    setSecureToken,
    getSecureToken,
    clearSecureToken
  };
};

/**
 * Encrypt sensitive data
 * @param {string} data - Data to encrypt
 * @returns {string} Encrypted data
 */
export const encryptData = (data) => {
  try {
    // In a real implementation, the secret key would be stored securely
    // and potentially rotated regularly
    const secretKey = 'unified-platform-secret-key';
    return CryptoJS.AES.encrypt(data, secretKey).toString();
  } catch (error) {
    console.error('Encryption error:', error);
    return null;
  }
};

/**
 * Decrypt sensitive data
 * @param {string} encryptedData - Data to decrypt
 * @returns {string} Decrypted data
 */
export const decryptData = (encryptedData) => {
  try {
    const secretKey = 'unified-platform-secret-key';
    const bytes = CryptoJS.AES.decrypt(encryptedData, secretKey);
    return bytes.toString(CryptoJS.enc.Utf8);
  } catch (error) {
    console.error('Decryption error:', error);
    return null;
  }
};

/**
 * Custom hook for CSRF protection
 * @returns {Object} CSRF token and validation function
 */
export const useCsrfProtection = () => {
  const [csrfToken, setCsrfToken] = useState(null);
  
  // Generate or fetch CSRF token on mount
  useEffect(() => {
    // In a real implementation, this would fetch from the server
    // For demo purposes, we'll generate a random token
    const token = generateRandomToken();
    setCsrfToken(token);
    
    // Store in a cookie or localStorage for server validation
    document.cookie = `XSRF-TOKEN=${token}; path=/; SameSite=Strict`;
  }, []);
  
  // Validate CSRF token
  const validateCsrfToken = useCallback((token) => {
    return token === csrfToken;
  }, [csrfToken]);
  
  return { csrfToken, validateCsrfToken };
};

/**
 * Generate a random token
 * @param {number} length - Token length
 * @returns {string} Random token
 */
export const generateRandomToken = (length = 32) => {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let token = '';
  
  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    token += characters.charAt(randomIndex);
  }
  
  return token;
};

/**
 * Custom hook for content security
 * @returns {Object} Content security utilities
 */
export const useContentSecurity = () => {
  // Sanitize HTML to prevent XSS
  const sanitizeHtml = useCallback((html) => {
    // In a real implementation, this would use a library like DOMPurify
    // For demo purposes, we'll use a simple regex-based approach
    return html
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }, []);
  
  // Validate file uploads
  const validateFileUpload = useCallback((file, allowedTypes, maxSize) => {
    if (!file) return { valid: false, error: 'No file provided' };
    
    // Check file type
    if (allowedTypes && !allowedTypes.includes(file.type)) {
      return { 
        valid: false, 
        error: `Invalid file type. Allowed types: ${allowedTypes.join(', ')}` 
      };
    }
    
    // Check file size
    if (maxSize && file.size > maxSize) {
      return { 
        valid: false, 
        error: `File too large. Maximum size: ${formatFileSize(maxSize)}` 
      };
    }
    
    return { valid: true };
  }, []);
  
  return { sanitizeHtml, validateFileUpload };
};

/**
 * Format file size for display
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
export const formatFileSize = (bytes) => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
};

/**
 * Custom hook for age verification
 * @returns {Object} Age verification utilities
 */
export const useAgeVerification = () => {
  const [ageVerified, setAgeVerified] = useState(false);
  const [userAge, setUserAge] = useState(null);
  
  // Check if user has previously verified age
  useEffect(() => {
    const storedVerification = localStorage.getItem('age_verification');
    if (storedVerification) {
      try {
        const { verified, age, timestamp } = JSON.parse(storedVerification);
        
        // Verification expires after 30 days
        const isExpired = Date.now() - timestamp > 30 * 24 * 60 * 60 * 1000;
        
        if (!isExpired && verified) {
          setAgeVerified(true);
          setUserAge(age);
        } else {
          // Clear expired verification
          localStorage.removeItem('age_verification');
        }
      } catch (error) {
        console.error('Error parsing age verification:', error);
      }
    }
  }, []);
  
  // Verify user's age
  const verifyAge = useCallback((birthDate) => {
    if (!birthDate) return false;
    
    const birthTimestamp = new Date(birthDate).getTime();
    const now = Date.now();
    
    // Calculate age
    const ageDate = new Date(now - birthTimestamp);
    const age = Math.abs(ageDate.getUTCFullYear() - 1970);
    
    const verified = age >= 13; // Minimum age is 13
    
    if (verified) {
      // Store verification
      const verificationData = {
        verified,
        age,
        timestamp: now
      };
      
      localStorage.setItem('age_verification', JSON.stringify(verificationData));
      setAgeVerified(true);
      setUserAge(age);
    }
    
    return { verified, age };
  }, []);
  
  // Check if user meets minimum age requirement
  const meetsAgeRequirement = useCallback((minimumAge) => {
    if (!ageVerified || userAge === null) return false;
    return userAge >= minimumAge;
  }, [ageVerified, userAge]);
  
  return { 
    ageVerified, 
    userAge, 
    verifyAge, 
    meetsAgeRequirement 
  };
};

/**
 * Custom hook for KYC verification status
 * @returns {Object} KYC verification utilities
 */
export const useKycVerification = () => {
  const [kycStatus, setKycStatus] = useState('none'); // none, pending, verified, rejected
  
  // Check KYC status on mount
  useEffect(() => {
    // In a real implementation, this would fetch from the server
    // For demo purposes, we'll check localStorage
    const storedStatus = localStorage.getItem('kyc_status');
    if (storedStatus) {
      setKycStatus(storedStatus);
    }
  }, []);
  
  // Start KYC verification process
  const startKycVerification = useCallback((userData) => {
    // In a real implementation, this would submit data to a KYC provider
    // For demo purposes, we'll just update the status
    setKycStatus('pending');
    localStorage.setItem('kyc_status', 'pending');
    
    // Simulate KYC verification process
    setTimeout(() => {
      const newStatus = Math.random() > 0.2 ? 'verified' : 'rejected';
      setKycStatus(newStatus);
      localStorage.setItem('kyc_status', newStatus);
    }, 3000);
    
    return true;
  }, []);
  
  return { kycStatus, startKycVerification };
};
