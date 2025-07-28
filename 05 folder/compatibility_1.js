// Cross-browser compatibility utilities for the Unified Platform
import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for detecting browser and device information
 * @returns {Object} Browser and device information
 */
export const useDeviceDetection = () => {
  const [deviceInfo, setDeviceInfo] = useState({
    browser: null,
    browserVersion: null,
    os: null,
    osVersion: null,
    deviceType: null,
    isMobile: false,
    isTablet: false,
    isDesktop: false,
    isTouchDevice: false
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Detect browser and version
    const detectBrowser = () => {
      const userAgent = navigator.userAgent;
      let browser = null;
      let browserVersion = null;

      // Chrome
      if (/Chrome/.test(userAgent) && !/Chromium|Edge|Edg|OPR|Opera/.test(userAgent)) {
        browser = 'Chrome';
        browserVersion = userAgent.match(/Chrome\/(\d+\.\d+)/)?.[1];
      }
      // Firefox
      else if (/Firefox/.test(userAgent)) {
        browser = 'Firefox';
        browserVersion = userAgent.match(/Firefox\/(\d+\.\d+)/)?.[1];
      }
      // Safari
      else if (/Safari/.test(userAgent) && !/Chrome|Chromium|Edge|Edg|OPR|Opera/.test(userAgent)) {
        browser = 'Safari';
        browserVersion = userAgent.match(/Version\/(\d+\.\d+)/)?.[1];
      }
      // Edge
      else if (/Edge|Edg/.test(userAgent)) {
        browser = 'Edge';
        browserVersion = userAgent.match(/Edge\/(\d+\.\d+)|Edg\/(\d+\.\d+)/)?.[1] || userAgent.match(/Edge\/(\d+\.\d+)|Edg\/(\d+\.\d+)/)?.[2];
      }
      // Opera
      else if (/OPR|Opera/.test(userAgent)) {
        browser = 'Opera';
        browserVersion = userAgent.match(/OPR\/(\d+\.\d+)|Opera\/(\d+\.\d+)/)?.[1] || userAgent.match(/OPR\/(\d+\.\d+)|Opera\/(\d+\.\d+)/)?.[2];
      }
      // IE
      else if (/MSIE|Trident/.test(userAgent)) {
        browser = 'Internet Explorer';
        browserVersion = userAgent.match(/MSIE (\d+\.\d+)/)?.[1] || userAgent.match(/rv:(\d+\.\d+)/)?.[1];
      }

      return { browser, browserVersion };
    };

    // Detect OS and version
    const detectOS = () => {
      const userAgent = navigator.userAgent;
      let os = null;
      let osVersion = null;

      // Windows
      if (/Windows/.test(userAgent)) {
        os = 'Windows';
        if (/Windows NT 10.0/.test(userAgent)) osVersion = '10';
        else if (/Windows NT 6.3/.test(userAgent)) osVersion = '8.1';
        else if (/Windows NT 6.2/.test(userAgent)) osVersion = '8';
        else if (/Windows NT 6.1/.test(userAgent)) osVersion = '7';
        else if (/Windows NT 6.0/.test(userAgent)) osVersion = 'Vista';
        else if (/Windows NT 5.1/.test(userAgent)) osVersion = 'XP';
        else osVersion = 'Unknown';
      }
      // macOS
      else if (/Macintosh/.test(userAgent)) {
        os = 'macOS';
        osVersion = userAgent.match(/Mac OS X (\d+[._]\d+)/)?.[1]?.replace('_', '.');
      }
      // iOS
      else if (/iPhone|iPad|iPod/.test(userAgent)) {
        os = 'iOS';
        osVersion = userAgent.match(/OS (\d+[._]\d+)/)?.[1]?.replace('_', '.');
      }
      // Android
      else if (/Android/.test(userAgent)) {
        os = 'Android';
        osVersion = userAgent.match(/Android (\d+\.\d+)/)?.[1];
      }
      // Linux
      else if (/Linux/.test(userAgent)) {
        os = 'Linux';
        osVersion = 'Unknown';
      }

      return { os, osVersion };
    };

    // Detect device type
    const detectDeviceType = () => {
      const userAgent = navigator.userAgent;
      const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
      const isTablet = /iPad|Android(?!.*Mobile)/i.test(userAgent) || (window.innerWidth >= 768 && window.innerWidth <= 1024);
      const isDesktop = !isMobile && !isTablet;
      const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

      let deviceType = 'unknown';
      if (isDesktop) deviceType = 'desktop';
      else if (isTablet) deviceType = 'tablet';
      else if (isMobile) deviceType = 'mobile';

      return { deviceType, isMobile, isTablet, isDesktop, isTouchDevice };
    };

    const browserInfo = detectBrowser();
    const osInfo = detectOS();
    const deviceTypeInfo = detectDeviceType();

    setDeviceInfo({
      ...browserInfo,
      ...osInfo,
      ...deviceTypeInfo
    });
  }, []);

  return deviceInfo;
};

/**
 * Custom hook for handling browser-specific CSS
 * @returns {Object} CSS compatibility utilities
 */
export const useCssCompatibility = () => {
  const deviceInfo = useDeviceDetection();

  // Generate browser-specific CSS prefixes
  const getPrefixedCss = useCallback((property, value) => {
    const prefixes = ['-webkit-', '-moz-', '-ms-', '-o-', ''];
    
    return prefixes.reduce((result, prefix) => {
      result[`${prefix}${property}`] = value;
      return result;
    }, {});
  }, []);

  // Check if a CSS feature is supported
  const isCssFeatureSupported = useCallback((feature) => {
    if (typeof window === 'undefined' || !window.CSS || !window.CSS.supports) {
      // Fallback for browsers without CSS.supports
      const dummyElement = document.createElement('div');
      
      try {
        dummyElement.style[feature] = 'initial';
        return dummyElement.style[feature] !== '';
      } catch (e) {
        return false;
      }
    }
    
    return window.CSS.supports(feature, 'initial');
  }, []);

  // Get fallback styles for unsupported features
  const getFallbackStyles = useCallback((styles) => {
    const fallbacks = {
      'display: grid': { display: 'flex', flexWrap: 'wrap' },
      'display: flex': { display: 'block' },
      'position: sticky': { position: 'relative' }
      // Add more fallbacks as needed
    };

    const result = { ...styles };
    
    Object.entries(fallbacks).forEach(([feature, fallbackStyle]) => {
      const [property, value] = feature.split(': ');
      
      if (styles[property] === value && !isCssFeatureSupported(property)) {
        Object.assign(result, fallbackStyle);
      }
    });
    
    return result;
  }, [isCssFeatureSupported]);

  // Generate browser-specific styles
  const getBrowserSpecificStyles = useCallback(() => {
    const { browser, browserVersion } = deviceInfo;
    
    // Example browser-specific styles
    if (browser === 'Safari') {
      return {
        // Safari-specific fixes
        '.scrollable-container': {
          '-webkit-overflow-scrolling': 'touch'
        },
        // Fix for flexbox gap issues in Safari < 14.1
        ...(parseFloat(browserVersion) < 14.1 ? {
          '.flex-gap-container': {
            display: 'flex',
            marginLeft: '-10px',
            marginTop: '-10px',
            '& > *': {
              marginLeft: '10px',
              marginTop: '10px'
            }
          }
        } : {})
      };
    }
    
    if (browser === 'Internet Explorer' || (browser === 'Edge' && parseFloat(browserVersion) < 79)) {
      return {
        // IE and Legacy Edge fixes
        '.grid-container': {
          display: 'flex',
          flexWrap: 'wrap'
        },
        '.flex-container': {
          ...getPrefixedCss('display', 'flex')
        }
      };
    }
    
    return {};
  }, [deviceInfo, getPrefixedCss]);

  return {
    getPrefixedCss,
    isCssFeatureSupported,
    getFallbackStyles,
    getBrowserSpecificStyles
  };
};

/**
 * Custom hook for handling browser-specific JavaScript
 * @returns {Object} JavaScript compatibility utilities
 */
export const useJsCompatibility = () => {
  const deviceInfo = useDeviceDetection();

  // Check if a JavaScript feature is supported
  const isFeatureSupported = useCallback((feature) => {
    const featureTests = {
      'Promise': () => typeof Promise !== 'undefined',
      'async/await': () => {
        try {
          eval('(async function() {})');
          return true;
        } catch (e) {
          return false;
        }
      },
      'fetch': () => typeof fetch !== 'undefined',
      'IntersectionObserver': () => typeof IntersectionObserver !== 'undefined',
      'localStorage': () => {
        try {
          return typeof localStorage !== 'undefined';
        } catch (e) {
          return false;
        }
      },
      'sessionStorage': () => {
        try {
          return typeof sessionStorage !== 'undefined';
        } catch (e) {
          return false;
        }
      },
      'WebSocket': () => typeof WebSocket !== 'undefined',
      'ServiceWorker': () => typeof navigator !== 'undefined' && 'serviceWorker' in navigator,
      'WebWorker': () => typeof Worker !== 'undefined',
      'Geolocation': () => typeof navigator !== 'undefined' && 'geolocation' in navigator,
      'WebGL': () => {
        try {
          const canvas = document.createElement('canvas');
          return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
        } catch (e) {
          return false;
        }
      },
      'WebRTC': () => typeof RTCPeerConnection !== 'undefined',
      'CSS Variables': () => window.CSS && window.CSS.supports && window.CSS.supports('--var', '0'),
      'ES6': () => {
        try {
          eval('class Test {}; const test = (x) => x; let y = 1; const obj = { ...{a: 1} };');
          return true;
        } catch (e) {
          return false;
        }
      }
    };
    
    return featureTests[feature] ? featureTests[feature]() : false;
  }, []);

  // Load polyfills for unsupported features
  const loadPolyfills = useCallback(async (features) => {
    const polyfillsToLoad = [];
    
    features.forEach(feature => {
      if (!isFeatureSupported(feature)) {
        switch (feature) {
          case 'Promise':
            polyfillsToLoad.push('https://cdn.jsdelivr.net/npm/promise-polyfill@8/dist/polyfill.min.js');
            break;
          case 'fetch':
            polyfillsToLoad.push('https://cdn.jsdelivr.net/npm/whatwg-fetch@3.6.2/dist/fetch.umd.min.js');
            break;
          case 'IntersectionObserver':
            polyfillsToLoad.push('https://cdn.jsdelivr.net/npm/intersection-observer@0.12.2/intersection-observer.js');
            break;
          // Add more polyfills as needed
        }
      }
    });
    
    // Load polyfills sequentially
    for (const polyfillUrl of polyfillsToLoad) {
      await new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = polyfillUrl;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    }
    
    return polyfillsToLoad.length > 0;
  }, [isFeatureSupported]);

  // Get browser-specific workarounds
  const getBrowserWorkarounds = useCallback(() => {
    const { browser, browserVersion } = deviceInfo;
    const workarounds = {};
    
    // Safari-specific workarounds
    if (browser === 'Safari') {
      // Fix for Safari date input issues
      workarounds.formatDateForInput = (date) => {
        if (!date) return '';
        const d = new Date(date);
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      };
      
      // Fix for Safari audio playback issues
      workarounds.initAudioContext = () => {
        // Safari requires user interaction to start audio context
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        const resumeAudioContext = () => {
          if (audioContext.state !== 'running') {
            audioContext.resume();
          }
          
          document.removeEventListener('click', resumeAudioContext);
          document.removeEventListener('touchstart', resumeAudioContext);
        };
        
        document.addEventListener('click', resumeAudioContext);
        document.addEventListener('touchstart', resumeAudioContext);
        
        return audioContext;
      };
    }
    
    // IE and Legacy Edge workarounds
    if (browser === 'Internet Explorer' || (browser === 'Edge' && parseFloat(browserVersion) < 79)) {
      // Fix for IE/Edge event handling
      workarounds.addEventListenerWithOptions = (element, type, listener, options) => {
        if (options && typeof options !== 'boolean') {
          const capture = options.capture || false;
          element.addEventListener(type, listener, capture);
          
          return () => element.removeEventListener(type, listener, capture);
        } else {
          element.addEventListener(type, listener, options);
          return () => element.removeEventListener(type, listener, options);
        }
      };
      
      // Fix for IE/Edge form submission
      workarounds.safeFormSubmit = (form) => {
        // IE doesn't properly trigger submit event for forms
        if (form.checkValidity()) {
          const event = document.createEvent('Event');
          event.initEvent('submit', true, true);
          form.dispatchEvent(event);
          
          // If the event wasn't prevented, submit the form
          if (!event.defaultPrevented) {
            form.submit();
          }
        } else {
          form.reportValidity();
        }
      };
    }
    
    return workarounds;
  }, [deviceInfo]);

  return {
    isFeatureSupported,
    loadPolyfills,
    getBrowserWorkarounds
  };
};

/**
 * Custom hook for handling touch and mobile interactions
 * @returns {Object} Touch interaction utilities
 */
export const useTouchInteractions = () => {
  const deviceInfo = useDeviceDetection();
  
  // Add touch-friendly event listeners
  const addTouchEventListeners = useCallback((element, events) => {
    if (!element) return () => {};
    
    const { onClick, onHover, onLongPress } = events;
    const listeners = [];
    
    if (onClick) {
      const clickHandler = (e) => onClick(e);
      element.addEventListener('click', clickHandler);
      listeners.push({ type: 'click', handler: clickHandler });
    }
    
    if (onHover && deviceInfo.isTouchDevice) {
      // For touch devices, convert hover to touch events
      let touchTimeout;
      
      const touchStartHandler = () => {
        touchTimeout = setTimeout(() => {
          onHover();
        }, 100);
      };
      
      const touchEndHandler = () => {
        if (touchTimeout) {
          clearTimeout(touchTimeout);
        }
      };
      
      element.addEventListener('touchstart', touchStartHandler);
      element.addEventListener('touchend', touchEndHandler);
      element.addEventListener('touchcancel', touchEndHandler);
      
      listeners.push(
        { type: 'touchstart', handler: touchStartHandler },
        { type: 'touchend', handler: touchEndHandler },
        { type: 'touchcancel', handler: touchEndHandler }
      );
    } else if (onHover) {
      // For non-touch devices, use mouseenter/mouseleave
      const mouseEnterHandler = () => onHover(true);
      const mouseLeaveHandler = () => onHover(false);
      
      element.addEventListener('mouseenter', mouseEnterHandler);
      element.addEventListener('mouseleave', mouseLeaveHandler);
      
      listeners.push(
        { type: 'mouseenter', handler: mouseEnterHandler },
        { type: 'mouseleave', handler: mouseLeaveHandler }
      );
    }
    
    if (onLongPress && deviceInfo.isTouchDevice) {
      let longPressTimeout;
      
      const touchStartHandler = (e) => {
        longPressTimeout = setTimeout(() => {
          onLongPress(e);
        }, 500);
      };
      
      const touchEndHandler = () => {
        if (longPressTimeout) {
          clearTimeout(longPressTimeout);
        }
      };
      
      element.addEventListener('touchstart', touchStartHandler);
      element.addEventListener('touchend', touchEndHandler);
      element.addEventListener('touchcancel', touchEndHandler);
      
      listeners.push(
        { type: 'touchsta
(Content truncated due to size limit. Use line ranges to read in chunks)