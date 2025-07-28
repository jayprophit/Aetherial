// Performance optimization utilities for the Unified Platform
import { useEffect, useState, useCallback } from 'react';

/**
 * Custom hook for lazy loading components
 * @param {Function} importFunc - Dynamic import function
 * @returns {Object} Component and loading state
 */
export const useLazyComponent = (importFunc) => {
  const [component, setComponent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    
    importFunc()
      .then(module => {
        if (mounted) {
          setComponent(module.default || module);
          setLoading(false);
        }
      })
      .catch(error => {
        console.error('Error loading component:', error);
        if (mounted) {
          setLoading(false);
        }
      });
      
    return () => {
      mounted = false;
    };
  }, [importFunc]);

  return { component, loading };
};

/**
 * Custom hook for debouncing function calls
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
export const useDebounce = (func, delay) => {
  const [timeoutId, setTimeoutId] = useState(null);

  const debouncedFunc = useCallback((...args) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    
    const newTimeoutId = setTimeout(() => {
      func(...args);
    }, delay);
    
    setTimeoutId(newTimeoutId);
  }, [func, delay, timeoutId]);

  useEffect(() => {
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [timeoutId]);

  return debouncedFunc;
};

/**
 * Custom hook for memoizing expensive calculations
 * @param {Function} computeFunc - Function to memoize
 * @param {Array} dependencies - Dependencies array
 * @returns {any} Computed value
 */
export const useMemoizedValue = (computeFunc, dependencies) => {
  const [value, setValue] = useState(null);
  
  useEffect(() => {
    setValue(computeFunc());
  }, dependencies);
  
  return value;
};

/**
 * Custom hook for intersection observer (lazy loading images, infinite scroll)
 * @param {Object} options - IntersectionObserver options
 * @returns {Object} ref and isIntersecting state
 */
export const useIntersectionObserver = (options = {}) => {
  const [ref, setRef] = useState(null);
  const [isIntersecting, setIsIntersecting] = useState(false);

  useEffect(() => {
    if (!ref) return;

    const observer = new IntersectionObserver(([entry]) => {
      setIsIntersecting(entry.isIntersecting);
    }, options);

    observer.observe(ref);

    return () => {
      observer.disconnect();
    };
  }, [ref, options]);

  return { ref: setRef, isIntersecting };
};

/**
 * Image optimization utility
 * @param {string} src - Image source
 * @param {Object} options - Optimization options
 * @returns {string} Optimized image URL
 */
export const optimizeImage = (src, options = {}) => {
  const { width, height, quality = 80, format = 'webp' } = options;
  
  // For demo purposes, we're just returning the original src
  // In production, this would connect to an image optimization service
  return src;
};

/**
 * Utility for code splitting and prefetching
 * @param {string} path - Module path
 * @returns {Promise} Module import promise
 */
export const prefetchComponent = (path) => {
  return import(`../components/${path}`);
};

/**
 * Cache utility for API responses
 */
export class APICache {
  constructor(ttl = 5 * 60 * 1000) { // 5 minutes default TTL
    this.cache = new Map();
    this.ttl = ttl;
  }

  set(key, value) {
    const item = {
      value,
      expiry: Date.now() + this.ttl
    };
    this.cache.set(key, item);
    return value;
  }

  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }
    
    return item.value;
  }

  invalidate(key) {
    this.cache.delete(key);
  }

  clear() {
    this.cache.clear();
  }
}

// Create a singleton instance
export const apiCache = new APICache();

/**
 * Utility for measuring component render performance
 * @param {string} componentName - Name of the component
 * @returns {Function} Cleanup function
 */
export const measurePerformance = (componentName) => {
  if (process.env.NODE_ENV !== 'development') return () => {};
  
  const startTime = performance.now();
  console.log(`${componentName} render started`);
  
  return () => {
    const endTime = performance.now();
    console.log(`${componentName} rendered in ${endTime - startTime}ms`);
  };
};
