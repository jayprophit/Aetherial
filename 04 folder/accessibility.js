// Accessibility utilities for the Unified Platform
import React, { useEffect, useRef } from 'react';

/**
 * Custom hook for managing focus trapping within modals
 * @param {boolean} isActive - Whether the focus trap is active
 * @returns {Object} ref to attach to the container element
 */
export const useFocusTrap = (isActive = true) => {
  const containerRef = useRef(null);
  
  useEffect(() => {
    if (!isActive || !containerRef.current) return;
    
    const container = containerRef.current;
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length === 0) return;
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    // Focus the first element when the trap becomes active
    firstElement.focus();
    
    const handleKeyDown = (e) => {
      if (e.key !== 'Tab') return;
      
      // Shift + Tab
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } 
      // Tab
      else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };
    
    container.addEventListener('keydown', handleKeyDown);
    
    return () => {
      container.removeEventListener('keydown', handleKeyDown);
    };
  }, [isActive]);
  
  return containerRef;
};

/**
 * Custom hook for managing focus restoration
 * @returns {Object} Functions to save and restore focus
 */
export const useFocusReturn = () => {
  const lastFocusedElement = useRef(null);
  
  const saveFocus = () => {
    lastFocusedElement.current = document.activeElement;
  };
  
  const restoreFocus = () => {
    if (lastFocusedElement.current) {
      lastFocusedElement.current.focus();
    }
  };
  
  return { saveFocus, restoreFocus };
};

/**
 * Higher-order component for adding keyboard navigation to components
 * @param {React.Component} Component - Component to enhance
 * @returns {React.Component} Enhanced component with keyboard navigation
 */
export const withKeyboardNavigation = (Component) => {
  return function WithKeyboardNavigation(props) {
    const handleKeyDown = (e) => {
      // Add keyboard navigation logic here
      // Example: Arrow keys for navigation, Enter for selection, etc.
    };
    
    return (
      <div onKeyDown={handleKeyDown} tabIndex={0}>
        <Component {...props} />
      </div>
    );
  };
};

/**
 * Component for creating accessible announcements for screen readers
 */
export const ScreenReaderAnnouncement = ({ message, assertive = false }) => {
  const announcementRef = useRef(null);
  
  useEffect(() => {
    if (!message || !announcementRef.current) return;
    
    // Update the content to trigger screen reader announcement
    announcementRef.current.textContent = '';
    
    // Use setTimeout to ensure the DOM update is processed
    setTimeout(() => {
      if (announcementRef.current) {
        announcementRef.current.textContent = message;
      }
    }, 50);
  }, [message]);
  
  return (
    <div
      ref={announcementRef}
      role="status"
      aria-live={assertive ? 'assertive' : 'polite'}
      aria-atomic="true"
      style={{
        position: 'absolute',
        width: '1px',
        height: '1px',
        padding: 0,
        margin: '-1px',
        overflow: 'hidden',
        clip: 'rect(0, 0, 0, 0)',
        whiteSpace: 'nowrap',
        border: 0
      }}
    />
  );
};

/**
 * Hook for managing ARIA attributes
 * @param {Object} initialAttributes - Initial ARIA attributes
 * @returns {Object} ARIA attributes and update function
 */
export const useAriaAttributes = (initialAttributes = {}) => {
  const [attributes, setAttributes] = React.useState(initialAttributes);
  
  const updateAttributes = (newAttributes) => {
    setAttributes(prev => ({ ...prev, ...newAttributes }));
  };
  
  return { attributes, updateAttributes };
};

/**
 * Component for creating skip links for keyboard users
 */
export const SkipLink = ({ targetId, children = 'Skip to main content' }) => {
  return (
    <a
      href={`#${targetId}`}
      style={{
        position: 'absolute',
        top: '-40px',
        left: 0,
        padding: '8px',
        backgroundColor: '#4A6CF7',
        color: 'white',
        zIndex: 1000,
        transition: 'top 0.2s',
        ':focus': {
          top: 0
        }
      }}
    >
      {children}
    </a>
  );
};

/**
 * Utility for checking color contrast
 * @param {string} foreground - Foreground color in hex
 * @param {string} background - Background color in hex
 * @returns {Object} Contrast ratio and WCAG compliance
 */
export const checkColorContrast = (foreground, background) => {
  // Convert hex to RGB
  const hexToRgb = (hex) => {
    const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    const fullHex = hex.replace(shorthandRegex, (m, r, g, b) => r + r + g + g + b + b);
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(fullHex);
    
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  };
  
  // Calculate relative luminance
  const getLuminance = (rgb) => {
    const { r, g, b } = rgb;
    
    const [R, G, B] = [r, g, b].map(c => {
      const value = c / 255;
      return value <= 0.03928
        ? value / 12.92
        : Math.pow((value + 0.055) / 1.055, 2.4);
    });
    
    return 0.2126 * R + 0.7152 * G + 0.0722 * B;
  };
  
  const rgb1 = hexToRgb(foreground);
  const rgb2 = hexToRgb(background);
  
  if (!rgb1 || !rgb2) return null;
  
  const l1 = getLuminance(rgb1);
  const l2 = getLuminance(rgb2);
  
  const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  
  return {
    ratio: ratio.toFixed(2),
    AA_normal: ratio >= 4.5,
    AA_large: ratio >= 3,
    AAA_normal: ratio >= 7,
    AAA_large: ratio >= 4.5
  };
};

/**
 * Utility for creating accessible form labels
 * @param {string} id - Input element ID
 * @param {string} label - Label text
 * @param {boolean} required - Whether the field is required
 * @returns {JSX.Element} Accessible label element
 */
export const AccessibleLabel = ({ id, label, required = false }) => {
  return (
    <label htmlFor={id} style={{ display: 'block', marginBottom: '0.5rem' }}>
      {label}
      {required && (
        <span
          style={{ color: '#EF4444', marginLeft: '0.25rem' }}
          aria-hidden="true"
        >
          *
        </span>
      )}
      {required && (
        <span style={{ position: 'absolute', width: '1px', height: '1px', padding: 0, margin: '-1px', overflow: 'hidden', clip: 'rect(0, 0, 0, 0)', whiteSpace: 'nowrap', border: 0 }}>
          Required
        </span>
      )}
    </label>
  );
};

/**
 * Utility for creating accessible error messages
 * @param {string} id - Input element ID
 * @param {string} error - Error message
 * @returns {JSX.Element} Accessible error message element
 */
export const AccessibleErrorMessage = ({ id, error }) => {
  if (!error) return null;
  
  return (
    <div
      id={`${id}-error`}
      role="alert"
      style={{ color: '#EF4444', fontSize: '0.875rem', marginTop: '0.25rem' }}
    >
      {error}
    </div>
  );
};
