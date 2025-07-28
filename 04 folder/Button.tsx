import React from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';

// Define types for button props
interface ButtonStyleProps {
  $variant?: 'primary' | 'secondary' | 'tertiary' | 'danger';
  $size?: 'small' | 'medium' | 'large';
  $fullWidth?: boolean;
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, ButtonStyleProps {
  children: React.ReactNode;
}

// Use transient props with $ prefix to avoid DOM warnings
const getButtonStyles = ($variant = 'primary', $size = 'medium', $fullWidth = false) => {
  let styles = '';
  
  // Variant styles
  switch ($variant) {
    case 'primary':
      styles += `
        background-color: ${theme.colors.primary};
        color: ${theme.colors.white};
        border: none;
        &:hover {
          background-color: ${theme.colors.primaryDark};
        }
      `;
      break;
    case 'secondary':
      styles += `
        background-color: ${theme.colors.secondary};
        color: ${theme.colors.white};
        border: none;
        &:hover {
          background-color: ${theme.colors.secondaryDark};
        }
      `;
      break;
    case 'tertiary':
      styles += `
        background-color: transparent;
        color: ${theme.colors.primary};
        border: 1px solid ${theme.colors.primary};
        &:hover {
          background-color: ${theme.colors.lightGray};
        }
      `;
      break;
    case 'danger':
      styles += `
        background-color: ${theme.colors.danger};
        color: ${theme.colors.white};
        border: none;
        &:hover {
          background-color: ${theme.colors.dangerDark};
        }
      `;
      break;
    default:
      styles += `
        background-color: ${theme.colors.primary};
        color: ${theme.colors.white};
        border: none;
        &:hover {
          background-color: ${theme.colors.primaryDark};
        }
      `;
  }
  
  // Size styles
  switch ($size) {
    case 'small':
      styles += `
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
      `;
      break;
    case 'medium':
      styles += `
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
      `;
      break;
    case 'large':
      styles += `
        padding: 1rem 2rem;
        font-size: 1.125rem;
      `;
      break;
    default:
      styles += `
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
      `;
  }
  
  // Full width style
  if ($fullWidth) {
    styles += `
      width: 100%;
      display: block;
    `;
  }
  
  // Common styles
  styles += `
    border-radius: ${theme.borderRadius};
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    &:focus {
      outline: none;
      box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5);
    }
  `;
  
  return styles;
};

// Use transient props with $ prefix to avoid passing them to DOM
const StyledButton = styled.button<ButtonStyleProps>`
  ${props => getButtonStyles(props.$variant, props.$size, props.$fullWidth)}
`;

// Button component with proper TypeScript typing
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, $variant, $size, $fullWidth, ...props }, ref) => {
    return (
      <StyledButton
        ref={ref}
        $variant={$variant}
        $size={$size}
        $fullWidth={$fullWidth}
        {...props}
      >
        {children}
      </StyledButton>
    );
  }
);

Button.displayName = 'Button';

export default Button;
