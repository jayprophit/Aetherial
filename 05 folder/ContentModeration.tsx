import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useContentModerationSystem } from '../../services/ContentModerationSystem';
import Button from '../ui/Button';

interface ContentModerationProps {
  userId: string;
  userAge: number;
}

enum ContentType {
  TEXT = 'text',
  IMAGE = 'image',
  VIDEO = 'video',
  AUDIO = 'audio',
  COMMENT = 'comment',
  MESSAGE = 'message',
  POST = 'post',
  PRODUCT = 'product',
  COURSE = 'course'
}

const ContentModeration: React.FC<ContentModerationProps> = ({ userId, userAge }) => {
  const moderationSystem = useContentModerationSystem();
  const [content, setContent] = useState<string>('');
  const [contentType, setContentType] = useState<ContentType>(ContentType.TEXT);
  const [moderationResult, setModerationResult] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string>('');
  const [flagReason, setFlagReason] = useState<string>('');
  const [flaggedContent, setFlaggedContent] = useState<any[]>([]);
  const [appealText, setAppealText] = useState<string>('');

  useEffect(() => {
    // In a real app, we would fetch flagged content from an API
    setFlaggedContent([
      {
        id: 'content-1',
        type: ContentType.TEXT,
        excerpt: 'This content was flagged for potential policy violations...',
        date: new Date().toISOString(),
        status: 'pending'
      },
      {
        id: 'content-2',
        type: ContentType.IMAGE,
        excerpt: 'Image was flagged for review...',
        date: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
        status: 'removed'
      }
    ]);
  }, []);

  const handleModerateContent = async () => {
    if (!content.trim() && contentType !== ContentType.IMAGE) {
      setError('Please enter content to moderate');
      return;
    }

    if (contentType === ContentType.IMAGE && !imageUrl.trim()) {
      setError('Please enter an image URL to moderate');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      let result;
      if (contentType === ContentType.IMAGE) {
        result = await moderationSystem.moderateImage(imageUrl, userAge);
      } else {
        result = await moderationSystem.moderateContent(content, contentType, userAge);
      }
      
      setModerationResult(result);
    } catch (err) {
      setError('Failed to moderate content. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFlagContent = async () => {
    if (!content.trim()) {
      setError('Please enter content to flag');
      return;
    }

    if (!flagReason.trim()) {
      setError('Please select a reason for flagging');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const result = await moderationSystem.flagInappropriateContent(
        'content-' + Date.now(),
        contentType,
        flagReason as any
      );
      
      if (result.success) {
        setContent('');
        setFlagReason('');
        setModerationResult({
          message: result.message,
          flagId: result.flagId
        });
      } else {
        setError('Failed to flag content. Please try again.');
      }
    } catch (err) {
      setError('An error occurred while flagging content.');
    } finally {
      setLoading(false);
    }
  };

  const handleAppealModeration = async (moderationId: string) => {
    if (!appealText.trim()) {
      setError('Please enter a reason for your appeal');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const result = await moderationSystem.appealModeration(moderationId, appealText);
      
      if (result.success) {
        setAppealText('');
        setModerationResult({
          message: result.message,
          appealId: result.appealId,
          status: result.status
        });
      } else {
        setError('Failed to submit appeal. Please try again.');
      }
    } catch (err) {
      setError('An error occurred while submitting appeal.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Header>
        <Title>Content Moderation System</Title>
        <Description>
          Our AI-powered content moderation system helps maintain a safe and appropriate environment for all users.
          {userAge < 13 && (
            <AgeBanner>
              Users under 13 have additional content restrictions for their safety.
            </AgeBanner>
          )}
        </Description>
      </Header>

      {error && (
        <ErrorMessage>
          {error}
          <CloseButton onClick={() => setError(null)}>×</CloseButton>
        </ErrorMessage>
      )}

      <Tabs>
        <Tab active={contentType !== ContentType.IMAGE} onClick={() => setContentType(ContentType.TEXT)}>
          Text Content
        </Tab>
        <Tab active={contentType === ContentType.IMAGE} onClick={() => setContentType(ContentType.IMAGE)}>
          Image Content
        </Tab>
      </Tabs>

      <Section>
        <SectionTitle>Check Content</SectionTitle>
        
        {contentType === ContentType.IMAGE ? (
          <InputGroup>
            <Label>Image URL</Label>
            <Input
              type="text"
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
              placeholder="Enter image URL to check"
            />
          </InputGroup>
        ) : (
          <>
            <InputGroup>
              <Label>Content Type</Label>
              <Select value={contentType} onChange={(e) => setContentType(e.target.value as ContentType)}>
                <option value={ContentType.TEXT}>Text</option>
                <option value={ContentType.COMMENT}>Comment</option>
                <option value={ContentType.MESSAGE}>Message</option>
                <option value={ContentType.POST}>Post</option>
                <option value={ContentType.PRODUCT}>Product Description</option>
                <option value={ContentType.COURSE}>Course Content</option>
              </Select>
            </InputGroup>
            
            <InputGroup>
              <Label>Content</Label>
              <TextArea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Enter content to check"
                rows={5}
              />
            </InputGroup>
          </>
        )}
        
        <ButtonContainer>
          <Button $variant="primary" onClick={handleModerateContent} disabled={loading}>
            {loading ? 'Checking...' : 'Check Content'}
          </Button>
        </ButtonContainer>

        {moderationResult && (
          <ResultCard approved={moderationResult.isApproved}>
            <ResultHeader>
              <ResultTitle>Moderation Result</ResultTitle>
              <ResultStatus approved={moderationResult.isApproved}>
                {moderationResult.isApproved ? 'Approved' : 'Not Approved'}
              </ResultStatus>
            </ResultHeader>
            
            {moderationResult.contentRating && (
              <ResultItem>
                <ResultLabel>Content Rating:</ResultLabel>
                <ResultValue>{moderationResult.contentRating}</ResultValue>
              </ResultItem>
            )}
            
            {moderationResult.moderationAction && (
              <ResultItem>
                <ResultLabel>Action:</ResultLabel>
                <ResultValue>{moderationResult.moderationAction}</ResultValue>
              </ResultItem>
            )}
            
            {moderationResult.reason && (
              <ResultItem>
                <ResultLabel>Reason:</ResultLabel>
                <ResultValue>{moderationResult.reason}</ResultValue>
              </ResultItem>
            )}
            
            {moderationResult.ageRestriction && (
              <ResultItem>
                <ResultLabel>Age Restriction:</ResultLabel>
                <ResultValue>{moderationResult.ageRestriction}+</ResultValue>
              </ResultItem>
            )}
            
            {moderationResult.suggestedEdits && (
              <ResultItem>
                <ResultLabel>Suggested Edits:</ResultLabel>
                <ResultValue>{moderationResult.suggestedEdits}</ResultValue>
              </ResultItem>
            )}
            
            {moderationResult.message && (
              <ResultMessage>{moderationResult.message}</ResultMessage>
            )}
            
            {!moderationResult.isApproved && moderationResult.moderationId && (
              <AppealSection>
                <AppealTitle>Appeal this decision</AppealTitle>
                <TextArea
                  value={appealText}
                  onChange={(e) => setAppealText(e.target.value)}
                  placeholder="Explain why you believe this content should be approved"
                  rows={3}
                />
                <Button 
                  $variant="outline" 
                  onClick={() => handleAppealModeration(moderationResult.moderationId)}
                  disabled={loading || !appealText.trim()}
                >
                  Submit Appeal
                </Button>
              </AppealSection>
            )}
          </ResultCard>
        )}
      </Section>

      <Section>
        <SectionTitle>Flag Inappropriate Content</SectionTitle>
        
        <InputGroup>
          <Label>Content Type</Label>
          <Select value={contentType} onChange={(e) => setContentType(e.target.value as ContentType)}>
            <option value={ContentType.TEXT}>Text</option>
            <option value={ContentType.IMAGE}>Image</option>
            <option value={ContentType.VIDEO}>Video</option>
            <option value={ContentType.COMMENT}>Comment</option>
            <option value={ContentType.MESSAGE}>Message</option>
            <option value={ContentType.POST}>Post</option>
          </Select>
        </InputGroup>
        
        <InputGroup>
          <Label>Content</Label>
          <TextArea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter content to flag"
            rows={5}
          />
        </InputGroup>
        
        <InputGroup>
          <Label>Reason for Flagging</Label>
          <Select value={flagReason} onChange={(e) => setFlagReason(e.target.value)}>
            <option value="">Select a reason</option>
            <option value="adult_content">Adult Content</option>
            <option value="violence">Violence</option>
            <option value="harassment">Harassment</option>
            <option value="hate_speech">Hate Speech</option>
            <option value="misinformation">Misinformation</option>
            <option value="spam">Spam</option>
            <option value="other">Other</option>
          </Select>
        </InputGroup>
        
        <ButtonContainer>
          <Button $variant="warning" onClick={handleFlagContent} disabled={loading}>
            {loading ? 'Flagging...' : 'Flag Content'}
          </Button>
        </ButtonContainer>
      </Section>

      <Section>
        <SectionTitle>Your Flagged Content</SectionTitle>
        
        {flaggedContent.length === 0 ? (
          <EmptyMessage>You haven't flagged any content yet.</EmptyMessage>
        ) : (
          <FlaggedList>
            {flaggedContent.map((item) => (
              <FlaggedItem key={item.id} status={item.status}>
                <FlaggedHeader>
                  <FlaggedType>{item.type}</FlaggedType>
                  <FlaggedStatus status={item.status}>
                    {item.status === 'pending' ? 'Under Review' : 'Removed'}
                  </FlaggedStatus>
                </FlaggedHeader>
                <FlaggedExcerpt>{item.excerpt}</FlaggedExcerpt>
                <FlaggedDate>Flagged on: {new Date(item.date).toLocaleDateString()}</FlaggedDate>
              </FlaggedItem>
            ))}
          </FlaggedList>
        )}
      </Section>

      <InfoSection>
        <InfoTitle>About Our Content Moderation</InfoTitle>
        <InfoContent>
          <p>Our AI-powered content moderation system helps maintain a safe and appropriate environment for all users by:</p>
          <ul>
            <li>Monitoring all users across all functions and features</li>
            <li>Enforcing age-appropriate content restrictions</li>
            <li>Preventing inappropriate behavior (adult content, abuse, violence)</li>
            <li>Implementing temporary or permanent bans for policy violations</li>
          </ul>
          <p>Users under 13 have additional content restrictions for their safety, in compliance with COPPA and other regulations.</p>
        </InfoContent>
      </InfoSection>
    </Container>
  );
};

// Styled components
const Container = styled.div`
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
`;

const Header = styled.div`
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 1rem;
`;

const Description = styled.p`
  color: ${props => props.theme.colors.textLight};
  margin-bottom: 1rem;
`;

const AgeBanner = styled.div`
  background-color: #e8f5e9;
  border-left: 4px solid #4caf50;
  padding: 1rem;
  margin-top: 1rem;
  font-weight: 500;
`;

const ErrorMessage = styled.div`
  background-color: #ffebee;
  color: #d32f2f;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  position: relative;
`;

const CloseButton = styled.button`
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: inherit;
`;

const Tabs = styled.div`
  display: flex;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid ${props => props.theme.colors.secondaryDark};
`;

const Tab = styled.div<{ active: boolean }>`
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: ${props => props.active ? '600' : '400'};
  color: ${props => props.active ? props.theme.colors.primary : props.theme.colors.textLight};
  border-bottom: 2px solid ${props => props.active ? props.theme.colors.primary : 'transparent'};
`;

const Section = styled.div`
  margin-bottom: 2.5rem;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
`;

const SectionTitle = styled.h2`
  font-size: 1.5rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 1.5rem;
`;

const InputGroup = styled.div`
  margin-bottom: 1.5rem;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: ${props => props.theme.colors.text};
`;

const Input = styled.input`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid ${props => props.theme.colors.secondaryDark};
  border-radius: 4px;
  font-size: 1rem;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 2px rgba(74, 108, 247, 0.2);
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid ${props => props.theme.colors.secondaryDark};
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 2px rgba(74, 108, 247, 0.2);
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid ${props => props.theme.colors.secondaryDark};
  border-radius: 4px;
  font-size: 1rem;
  background-color: #ffffff;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 2px rgba(74, 108, 247, 0.2);
  }
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: fl
(Content truncated due to size limit. Use line ranges to read in chunks)