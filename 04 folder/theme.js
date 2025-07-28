import React from 'react';
import styled from 'styled-components';

// Create a theme object for styling consistency
export const theme = {
  colors: {
    primary: '#3498db',
    primaryDark: '#2980b9',
    secondary: '#2ecc71',
    secondaryDark: '#27ae60',
    tertiary: '#9b59b6',
    tertiaryDark: '#8e44ad',
    danger: '#e74c3c',
    dangerDark: '#c0392b',
    warning: '#f39c12',
    warningDark: '#d35400',
    success: '#2ecc71',
    successDark: '#27ae60',
    info: '#3498db',
    infoDark: '#2980b9',
    white: '#ffffff',
    black: '#000000',
    gray: '#95a5a6',
    lightGray: '#ecf0f1',
    darkGray: '#7f8c8d',
    background: '#f9f9f9',
    text: '#2c3e50',
    border: '#dfe6e9'
  },
  fonts: {
    body: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    heading: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    monospace: "SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"
  },
  fontSizes: {
    xs: '0.75rem',
    sm: '0.875rem',
    md: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
    '4xl': '2.25rem',
    '5xl': '3rem',
    '6xl': '3.75rem'
  },
  fontWeights: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800
  },
  lineHeights: {
    normal: 'normal',
    none: 1,
    shorter: 1.25,
    short: 1.375,
    base: 1.5,
    tall: 1.625,
    taller: 2
  },
  space: {
    px: '1px',
    0: '0',
    1: '0.25rem',
    2: '0.5rem',
    3: '0.75rem',
    4: '1rem',
    5: '1.25rem',
    6: '1.5rem',
    8: '2rem',
    10: '2.5rem',
    12: '3rem',
    16: '4rem',
    20: '5rem',
    24: '6rem',
    32: '8rem',
    40: '10rem',
    48: '12rem',
    56: '14rem',
    64: '16rem'
  },
  sizes: {
    full: '100%',
    '3xs': '14rem',
    '2xs': '16rem',
    xs: '20rem',
    sm: '24rem',
    md: '28rem',
    lg: '32rem',
    xl: '36rem',
    '2xl': '42rem',
    '3xl': '48rem',
    '4xl': '56rem',
    '5xl': '64rem',
    '6xl': '72rem'
  },
  radii: {
    none: '0',
    sm: '0.125rem',
    base: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    '2xl': '1rem',
    '3xl': '1.5rem',
    full: '9999px'
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    outline: '0 0 0 3px rgba(66, 153, 225, 0.5)',
    none: 'none'
  },
  zIndices: {
    hide: -1,
    auto: 'auto',
    base: 0,
    docked: 10,
    dropdown: 1000,
    sticky: 1100,
    banner: 1200,
    overlay: 1300,
    modal: 1400,
    popover: 1500,
    skipLink: 1600,
    toast: 1700,
    tooltip: 1800
  },
  transitions: {
    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      sharp: 'cubic-bezier(0.4, 0, 0.6, 1)'
    },
    duration: {
      ultra_fast: '0.05s',
      faster: '0.1s',
      fast: '0.2s',
      normal: '0.3s',
      slow: '0.5s',
      slower: '0.7s',
      ultra_slow: '1s'
    }
  },
  borderRadius: '0.25rem',
  borderWidth: '1px',
  borderStyle: 'solid',
  borderColor: '#dfe6e9',
  breakpoints: {
    xs: '0px',
    sm: '576px',
    md: '768px',
    lg: '992px',
    xl: '1200px',
    '2xl': '1400px'
  }
};

// Media queries for responsive design
export const media = {
  xs: `@media (min-width: ${theme.breakpoints.xs})`,
  sm: `@media (min-width: ${theme.breakpoints.sm})`,
  md: `@media (min-width: ${theme.breakpoints.md})`,
  lg: `@media (min-width: ${theme.breakpoints.lg})`,
  xl: `@media (min-width: ${theme.breakpoints.xl})`,
  '2xl': `@media (min-width: ${theme.breakpoints['2xl']})`
};

// Global styles
export const GlobalStyles = styled.createGlobalStyle`
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html, body {
    font-family: ${theme.fonts.body};
    font-size: 16px;
    line-height: ${theme.lineHeights.base};
    color: ${theme.colors.text};
    background-color: ${theme.colors.background};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  a {
    color: ${theme.colors.primary};
    text-decoration: none;
    transition: color ${theme.transitions.duration.fast} ${theme.transitions.easing.easeInOut};
    
    &:hover {
      color: ${theme.colors.primaryDark};
      text-decoration: underline;
    }
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: ${theme.fonts.heading};
    font-weight: ${theme.fontWeights.bold};
    line-height: ${theme.lineHeights.shorter};
    margin-bottom: ${theme.space[4]};
  }

  h1 {
    font-size: ${theme.fontSizes['4xl']};
  }

  h2 {
    font-size: ${theme.fontSizes['3xl']};
  }

  h3 {
    font-size: ${theme.fontSizes['2xl']};
  }

  h4 {
    font-size: ${theme.fontSizes.xl};
  }

  h5 {
    font-size: ${theme.fontSizes.lg};
  }

  h6 {
    font-size: ${theme.fontSizes.md};
  }

  p {
    margin-bottom: ${theme.space[4]};
  }

  button, input, select, textarea {
    font-family: inherit;
    font-size: 100%;
    line-height: 1.15;
  }

  img {
    max-width: 100%;
    height: auto;
  }
`;

export default theme;
