import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Head from 'next/head';
import Link from 'next/link';

// Styled components
const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

const Header = styled.header`
  background-color: ${props => props.theme.colors.primary};
  color: white;
  padding: 20px 0;
  margin-bottom: 40px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const HeaderContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.div`
  font-size: 24px;
  font-weight: bold;
`;

const NavLinks = styled.ul`
  display: flex;
  list-style: none;
  
  @media (max-width: 768px) {
    display: none;
  }
`;

const NavItem = styled.li`
  margin-left: 20px;
`;

const NavLink = styled.a`
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s;
  
  &:hover {
    opacity: 0.8;
  }
`;

const Title = styled.h1`
  font-size: 32px;
  margin-bottom: 20px;
  color: ${props => props.theme.colors.text};
`;

const Subtitle = styled.p`
  font-size: 18px;
  margin-bottom: 40px;
  color: ${props => props.theme.colors.textLight};
`;

const KYCContainer = styled.div`
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 40px;
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: ${props => props.theme.colors.text};
`;

const Input = styled.input`
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 16px;
  outline: none;
  
  &:focus {
    border-color: ${props => props.theme.colors.primary};
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 16px;
  outline: none;
  background-color: white;
  
  &:focus {
    border-color: ${props => props.theme.colors.primary};
  }
`;

const Button = styled.button`
  padding: 12px 24px;
  background-color: ${props => props.$variant === 'primary' ? props.theme.colors.primary : props.theme.colors.secondary};
  color: ${props => props.$variant === 'primary' ? 'white' : props.theme.colors.text};
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: ${props => props.$variant === 'primary' ? props.theme.colors.primaryDark : '#e2e8f0'};
  }
`;

const InfoBox = styled.div`
  background-color: ${props => props.$type === 'warning' ? '#fff8e1' : '#e3f2fd'};
  border-left: 4px solid ${props => props.$type === 'warning' ? '#ffb74d' : '#64b5f6'};
  padding: 15px 20px;
  margin-bottom: 20px;
  border-radius: 4px;
`;

const InfoTitle = styled.h4`
  margin: 0 0 10px;
  color: ${props => props.$type === 'warning' ? '#f57c00' : '#1976d2'};
`;

const InfoText = styled.p`
  margin: 0;
  color: ${props => props.theme.colors.text};
`;

const TabContainer = styled.div`
  margin-bottom: 30px;
`;

const TabButtons = styled.div`
  display: flex;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 20px;
`;

const TabButton = styled.button`
  padding: 12px 24px;
  background-color: ${props => props.$active ? props.theme.colors.primary : 'transparent'};
  color: ${props => props.$active ? 'white' : props.theme.colors.text};
  border: none;
  border-bottom: ${props => props.$active ? `3px solid ${props.theme.colors.primaryDark}` : '3px solid transparent'};
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    background-color: ${props => props.$active ? props.theme.colors.primary : '#f1f5f9'};
  }
`;

const TabContent = styled.div`
  display: ${props => props.$active ? 'block' : 'none'};
`;

const FeatureList = styled.div`
  margin-top: 60px;
`;

const FeatureTitle = styled.h2`
  font-size: 24px;
  margin-bottom: 20px;
  color: ${props => props.theme.colors.text};
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const FeatureCard = styled.div`
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  }
`;

const FeatureIcon = styled.div`
  width: 60px;
  height: 60px;
  background-color: ${props => props.theme.colors.primary};
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  color: white;
  font-size: 24px;
`;

const FeatureCardTitle = styled.h3`
  font-size: 20px;
  margin-bottom: 15px;
  color: ${props => props.theme.colors.text};
`;

const FeatureText = styled.p`
  color: ${props => props.theme.colors.textLight};
`;

// Main component
export default function KYCVerification() {
  const [activeTab, setActiveTab] = useState('personal');
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    dateOfBirth: '',
    email: '',
    phone: '',
    country: '',
    idType: 'passport',
    idNumber: '',
    address: '',
    city: '',
    postalCode: '',
    agreeTerms: false
  });
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [ageVerified, setAgeVerified] = useState(false);
  
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
    
    // Check age if date of birth is entered
    if (name === 'dateOfBirth' && value) {
      const birthDate = new Date(value);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      
      setAgeVerified(age >= 18);
    }
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real application, this would send the data to the server for verification
    setFormSubmitted(true);
  };

  return (
    <>
      <Head>
        <title>KYC Verification | Unified Platform</title>
        <meta name="description" content="Complete your KYC verification to access all features of the unified platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header>
        <HeaderContainer>
          <Link href="/" passHref>
            <Logo as="a" style={{ textDecoration: 'none', color: 'white' }}>Unified Platform</Logo>
          </Link>
          <NavLinks>
            <NavItem>
              <Link href="/" passHref>
                <NavLink>Home</NavLink>
              </Link>
            </NavItem>
            <NavItem>
              <Link href="/social" passHref>
                <NavLink>Social</NavLink>
              </Link>
            </NavItem>
            <NavItem>
              <Link href="/ecommerce" passHref>
                <NavLink>E-Commerce</NavLink>
              </Link>
            </NavItem>
            <NavItem>
              <Link href="/learning" passHref>
                <NavLink>Learning</NavLink>
              </Link>
            </NavItem>
            <NavItem>
              <Link href="/jobs" passHref>
                <NavLink>Jobs</NavLink>
              </Link>
            </NavItem>
          </NavLinks>
        </HeaderContainer>
      </Header>

      <Container>
        <Title>KYC Verification</Title>
        <Subtitle>
          Complete your verification to access all features of the unified platform. 
          This process ensures compliance with regulations and protects all users.
        </Subtitle>
        
        {formSubmitted ? (
          <KYCContainer>
            <Title style={{ fontSize: '24px' }}>Verification Submitted</Title>
            <InfoBox $type="info">
              <InfoTitle $type="info">Verification In Progress</InfoTitle>
              <InfoText>
                Thank you for submitting your verification information. Our team will review your submission
                and update your account status within 24-48 hours. You'll receive an email notification once
                the verification is complete.
              </InfoText>
            </InfoBox>
            
            <FeatureTitle>What's Next?</FeatureTitle>
            <FeatureGrid>
              <FeatureCard>
                <FeatureIcon>✅</FeatureIcon>
                <FeatureCardTitle>Full Platform Access</FeatureCardTitle>
                <FeatureText>
                  Once verified, you'll have access to all platform features including advanced trading, 
                  higher transaction limits, and premium content.
                </FeatureText>
              </FeatureCard>
              
              <FeatureCard>
                <FeatureIcon>💰</FeatureIcon>
                <FeatureCardTitle>Digital Asset Management</FeatureCardTitle>
                <FeatureText>
                  Manage your digital assets with staking, minting, and mining capabilities based on your age verification.
                </FeatureText>
              </FeatureCard>
              
              <FeatureCard>
                <FeatureIcon>🔒</FeatureIcon>
                <FeatureCardTitle>Enhanced Security</FeatureCardTitle>
                <FeatureText>
                  Your verified account has additional security features to protect your assets and personal information.
                </FeatureText>
              </FeatureCard>
            </FeatureGrid>
          </KYCContainer>
        ) : (
          <KYCContainer>
            <InfoBox $type="warning">
              <InfoTitle $type="warning">Important Information</InfoTitle>
              <InfoText>
                Users under 18 will have limited access to certain features. Digital assets (reward points) for users under 18
                will be locked, compounded, minted, mined, and staked until the legal age of access, requiring KYC verification
                for these features.
              </InfoText>
            </InfoBox>
            
            <TabContainer>
              <TabButtons>
                <TabButton 
                  $active={activeTab === 'personal'} 
                  onClick={() => setActiveTab('personal')}
                >
                  Personal Information
                </TabButton>
                <TabButton 
                  $active={activeTab === 'identity'} 
                  onClick={() => setActiveTab('identity')}
                >
                  Identity Verification
                </TabButton>
                <TabButton 
                  $active={activeTab === 'address'} 
                  onClick={() => setActiveTab('address')}
                >
                  Address Verification
                </TabButton>
              </TabButtons>
              
              <form onSubmit={handleSubmit}>
                <TabContent $active={activeTab === 'personal'}>
                  <FormGroup>
                    <Label htmlFor="firstName">First Name</Label>
                    <Input 
                      type="text" 
                      id="firstName" 
                      name="firstName" 
                      value={formData.firstName}
                      onChange={handleInputChange}
                      required 
                    />
                  </FormGroup>
                  
                  <FormGroup>
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input 
                      type="text" 
                      id="lastName" 
                      name="lastName" 
                      value={formData.lastName}
                      onChange={handleInputChange}
                      required 
                    />
                  </FormGroup>
                  
                  <FormGroup>
                    <Label htmlFor="dateOfBirth">Date of Birth</Label>
                    <Input 
                      type="date" 
                      id="dateOfBirth" 
                      name="dateOfBirth" 
                      value={formData.dateOfBirth}
                      onChange={handleInputChange}
                      required 
                    />
                    {formData.dateOfBirth && !ageVerified && (
                      <InfoBox $type="warning" style={{ marginTop: '10px' }}>
                        <InfoText>
                          Users under 18 will have limited access to certain features. Digital assets will be locked until legal age.
                        </InfoText>
                      </InfoBox>
                    )}
                  </FormGroup>
                  
                  <FormGroup>
                    <Label htmlFor="email">Email Address</Label>
                    <Input 
                      type="email" 
                      id="email" 
                      name="email" 
                      value={formData.email}
                      onChange={handleInputChange}
                      required 
                    />
                  </FormGroup>
                  
                  <FormGroup>
                    <Label htmlFor="phone">Phone Number</Label>
                    <Input 
                      type="tel" 
                      id="phone" 
                      name="phone" 
                      value={formData.phone}
                      onChange={handleInputChange}
                      required 
                    />
                  </FormGroup>
                  
                  <Button type="button" $variant="primary" onClick={() => setActiveTab('identity')}>
                    Next: Identity Verification
                  </Button>
                </TabContent>
                
                <TabContent $active={activeTab === 'identity'}>
                  <FormGroup>
                    <Label htmlFor="country">Country of Residence</Label>
                    <Select 
                      id="country" 
                      name="country" 
                      value={formData.country}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select Country</option>
                      <option value="us">United States</option>
                      <option value="ca">Canada</option>
                      <option value="uk">United Kingdom</option>
                      <option value="au">Australia</option>
                      <option value="other">Other</option>
                    </Select>
                  </FormGroup>
                  
                  <FormGroup>
                    <Label htmlFor="idType">ID Type</Label>
                    <Select 
                      id="idType" 
                      name="idType" 
                      value={formData.idType}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="passport">Passport</option>
                      <option value="driverLicense">Driver's License</option>
                      <option value="nationalId">National ID Card</option>
                    </Select>
                  </FormGroup>
                  
                  <FormGroup>
                    <Label htmlFor="idNumber">ID Number</Label>
                    <Input 
                      type="text" 
                      id="idNumber" 
                      name="idNumber" 
                      value={formData.idNumber}
                      onChange={
(Content truncated due to size limit. Use line ranges to read in chunks)