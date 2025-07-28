import { DefaultTheme } from 'styled-components';

const theme = {
  colors: {
    primary: '#4CAF50',
    secondary: '#2196F3',
    secondaryDark: '#1565C0',
    text: '#333333',
    textLight: '#666666',
    background: '#F5F5F5',
    backgroundLight: '#E8F5E9',
    backgroundDark: '#C8E6C9',
    backgroundAlt: '#F1F8E9',
    border: '#DDDDDD',
    error: '#F44336',
    danger: '#F44336',
    success: '#4CAF50',
    warning: '#FF9800',
    info: '#2196F3'
  },
  fonts: {
    body: "'Roboto', sans-serif",
    heading: "'Roboto', sans-serif"
  },
  fontSizes: {
    small: '0.875rem',
    medium: '1rem',
    large: '1.25rem',
    xlarge: '1.5rem',
    xxlarge: '2rem'
  },
  fontWeights: {
    normal: 400,
    medium: 500,
    bold: 700
  },
  lineHeights: {
    body: 1.5,
    heading: 1.2
  },
  space: {
    xxsmall: '0.25rem',
    xsmall: '0.5rem',
    small: '0.75rem',
    medium: '1rem',
    large: '1.5rem',
    xlarge: '2rem',
    xxlarge: '3rem'
  },
  spacing: {
    xxsmall: '0.25rem',
    xsmall: '0.5rem',
    small: '0.75rem',
    medium: '1rem',
    large: '1.5rem',
    xlarge: '2rem',
    xxlarge: '3rem'
  },
  sizes: {
    maxWidth: '1200px'
  },
  borderRadius: '8px',
  shadows: {
    small: '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
    medium: '0 3px 6px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.12)',
    large: '0 10px 20px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.10)'
  },
  breakpoints: {
    mobile: '480px',
    tablet: '768px',
    desktop: '992px',
    largeDesktop: '1200px'
  }
};

export default theme;
