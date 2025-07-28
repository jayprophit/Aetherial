import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import MainLayout from '../components/layout/MainLayout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';

// Styled components
const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageHeader = styled.div`
  margin-bottom: 2rem;
`;

const PageTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
`;

const PageDescription = styled.p`
  font-size: 1.125rem;
  color: #64748B;
`;

const AIAssistantContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 70vh;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
`;

const ChatHeader = styled.div`
  display: flex;
  align-items: center;
  padding: 1rem;
  background-color: #4A6CF7;
  color: white;
`;

const AIAvatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.25rem;
`;

const ChatTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
`;

const MessagesContainer = styled.div`
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: #F8FAFC;
`;

const MessageBubble = styled.div<{ $isUser: boolean }>`
  max-width: 70%;
  padding: 1rem;
  border-radius: 1rem;
  margin-bottom: 1rem;
  align-self: ${props => props.$isUser ? 'flex-end' : 'flex-start'};
  background-color: ${props => props.$isUser ? '#4A6CF7' : 'white'};
  color: ${props => props.$isUser ? 'white' : '#1E293B'};
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  margin-left: ${props => props.$isUser ? 'auto' : '0'};
  margin-right: ${props => props.$isUser ? '0' : 'auto'};
`;

const ChatInputContainer = styled.div`
  display: flex;
  padding: 1rem;
  background-color: white;
  border-top: 1px solid #E5E7EB;
`;

const ChatInput = styled.input`
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #E5E7EB;
  border-radius: 0.375rem;
  margin-right: 0.5rem;
  font-size: 1rem;
  
  &:focus {
    outline: none;
    border-color: #4A6CF7;
    box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.2);
  }
`;

const AIFeaturesSection = styled.div`
  margin-top: 3rem;
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
`;

const FeatureCard = styled(Card)`
  height: 100%;
`;

const FeatureIcon = styled.div`
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #4A6CF7;
`;

const FeatureTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
`;

const FeatureDescription = styled.p`
  color: #64748B;
`;

// Sample messages
const INITIAL_MESSAGES = [
  { id: 1, content: "Hello! I'm your AI assistant. How can I help you today?", isUser: false },
];

// AI features
const AI_FEATURES = [
  {
    icon: '💬',
    title: 'Multi-Model Conversation',
    description: 'Engage in natural conversations with our advanced AI that combines multiple specialized models for the best responses.',
  },
  {
    icon: '🛒',
    title: 'E-commerce Assistance',
    description: 'Get help with finding products, setting up your shop, and optimizing your product listings.',
  },
  {
    icon: '📚',
    title: 'Learning Support',
    description: 'Receive personalized learning recommendations and assistance with course content creation.',
  },
  {
    icon: '📝',
    title: 'Content Creation',
    description: 'Generate high-quality content for blogs, social media, and product descriptions.',
  },
  {
    icon: '📊',
    title: 'Business Intelligence',
    description: 'Access AI-powered insights and recommendations for your business operations.',
  },
  {
    icon: '🔍',
    title: 'Research Assistant',
    description: 'Get help with research, fact-checking, and information gathering on any topic.',
  },
];

// AIAssistantPage component
const AIAssistantPage: React.FC = () => {
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [inputValue, setInputValue] = useState('');
  const [isClient, setIsClient] = useState(false);

  // Fix for hydration issues
  useEffect(() => {
    setIsClient(true);
  }, []);

  const handleSendMessage = () => {
    if (inputValue.trim() === '') return;
    
    // Add user message
    const userMessage = {
      id: messages.length + 1,
      content: inputValue,
      isUser: true,
    };
    
    setMessages([...messages, userMessage]);
    setInputValue('');
    
    // Simulate AI response after a short delay
    setTimeout(() => {
      const aiResponses = [
        "I'd be happy to help with that! Could you provide more details?",
        "That's an interesting question. Here's what I found...",
        "Based on your request, I recommend the following options...",
        "I can definitely assist with that. Let me guide you through the process.",
        "I've analyzed your question and here's my recommendation...",
      ];
      
      const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)];
      
      const aiMessage = {
        id: messages.length + 2,
        content: randomResponse,
        isUser: false,
      };
      
      setMessages(prevMessages => [...prevMessages, aiMessage]);
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  if (!isClient) {
    return null;
  }

  return (
    <MainLayout>
      <PageContainer>
        <PageHeader>
          <PageTitle>AI Assistant</PageTitle>
          <PageDescription>
            Interact with our advanced multi-model AI assistant for help with any platform feature.
          </PageDescription>
        </PageHeader>
        
        <AIAssistantContainer>
          <ChatHeader>
            <AIAvatar>🤖</AIAvatar>
            <ChatTitle>Unified Platform AI</ChatTitle>
          </ChatHeader>
          
          <MessagesContainer>
            {messages.map(message => (
              <MessageBubble key={message.id} $isUser={message.isUser}>
                {message.content}
              </MessageBubble>
            ))}
          </MessagesContainer>
          
          <ChatInputContainer>
            <ChatInput
              type="text"
              placeholder="Type your message here..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <Button variant="primary" onClick={handleSendMessage}>Send</Button>
          </ChatInputContainer>
        </AIAssistantContainer>
        
        <AIFeaturesSection>
          <SectionTitle>AI Capabilities</SectionTitle>
          <FeaturesGrid>
            {AI_FEATURES.map((feature, index) => (
              <FeatureCard key={index} $elevated $rounded>
                <FeatureIcon>{feature.icon}</FeatureIcon>
                <FeatureTitle>{feature.title}</FeatureTitle>
                <FeatureDescription>{feature.description}</FeatureDescription>
              </FeatureCard>
            ))}
          </FeaturesGrid>
        </AIFeaturesSection>
      </PageContainer>
    </MainLayout>
  );
};

// Shared components
const SectionTitle = styled.h2`
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1rem;
`;

export default AIAssistantPage;
