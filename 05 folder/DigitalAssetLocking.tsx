import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useDigitalAssetManager } from '../../services/DigitalAssetManager';
import Button from '../ui/Button';

interface DigitalAssetLockingProps {
  userId: string;
  userAge: number;
  isKYCVerified: boolean;
}

const DigitalAssetLocking: React.FC<DigitalAssetLockingProps> = ({ userId, userAge, isKYCVerified }) => {
  const assetManager = useDigitalAssetManager();
  const [userAssets, setUserAssets] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserAssets = async () => {
      try {
        setLoading(true);
        const assets = await assetManager.getUserAssets(userId);
        setUserAssets(assets);
        setError(null);
      } catch (err) {
        setError('Failed to load user assets. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserAssets();
  }, [userId, assetManager]);

  const handleLockAsset = async (assetId: string) => {
    try {
      setLoading(true);
      // Lock until user turns 18
      const yearsToLock = 18 - userAge;
      const daysToLock = yearsToLock * 365;
      
      const result = await assetManager.lockAsset(assetId, userId, daysToLock);
      
      if (result.success) {
        setSuccessMessage(`Asset ${assetId} has been locked until you reach 18 years of age.`);
        
        // Refresh user assets
        const assets = await assetManager.getUserAssets(userId);
        setUserAssets(assets);
      } else {
        setError('Failed to lock asset. Please try again.');
      }
    } catch (err) {
      setError('An error occurred while locking the asset.');
    } finally {
      setLoading(false);
    }
  };

  const handleCompoundAsset = async (assetId: string) => {
    try {
      setLoading(true);
      const result = await assetManager.compoundAsset(assetId, userId, 0.05); // 5% compound rate
      
      if (result.success) {
        setSuccessMessage(`Asset ${assetId} has been compounded successfully. New value: ${result.newValue.toFixed(2)}`);
        
        // Refresh user assets
        const assets = await assetManager.getUserAssets(userId);
        setUserAssets(assets);
      } else {
        setError('Failed to compound asset. Please try again.');
      }
    } catch (err) {
      setError('An error occurred while compounding the asset.');
    } finally {
      setLoading(false);
    }
  };

  const handleUnlockAttempt = async (assetId: string) => {
    try {
      setLoading(true);
      
      if (!isKYCVerified) {
        setError('KYC verification is required to unlock assets.');
        setLoading(false);
        return;
      }
      
      if (userAge < 18) {
        setError('You must be 18 or older to unlock this asset.');
        setLoading(false);
        return;
      }
      
      const result = await assetManager.unlockAsset(assetId, userId, { kycVerified: true, age: userAge });
      
      if (result.success) {
        setSuccessMessage(`Asset ${assetId} has been unlocked successfully.`);
        
        // Refresh user assets
        const assets = await assetManager.getUserAssets(userId);
        setUserAssets(assets);
      } else {
        setError('Failed to unlock asset. Please try again.');
      }
    } catch (err) {
      setError('An error occurred while attempting to unlock the asset.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !userAssets) {
    return <LoadingContainer>Loading assets...</LoadingContainer>;
  }

  if (error && !userAssets) {
    return <ErrorContainer>{error}</ErrorContainer>;
  }

  return (
    <Container>
      <Header>
        <Title>Digital Asset Management</Title>
        {userAge < 18 && (
          <AgeRestrictionBanner>
            You are under 18. Some digital assets will be locked until you reach the legal age of access.
          </AgeRestrictionBanner>
        )}
      </Header>

      {successMessage && (
        <SuccessMessage>
          {successMessage}
          <CloseButton onClick={() => setSuccessMessage(null)}>×</CloseButton>
        </SuccessMessage>
      )}

      {error && (
        <ErrorMessage>
          {error}
          <CloseButton onClick={() => setError(null)}>×</CloseButton>
        </ErrorMessage>
      )}

      <AssetSummary>
        <SummaryItem>
          <SummaryLabel>Total Value:</SummaryLabel>
          <SummaryValue>{userAssets?.totalValue || 0}</SummaryValue>
        </SummaryItem>
        <SummaryItem>
          <SummaryLabel>Locked Value:</SummaryLabel>
          <SummaryValue>{userAssets?.lockedValue || 0}</SummaryValue>
        </SummaryItem>
        <SummaryItem>
          <SummaryLabel>Staked Value:</SummaryLabel>
          <SummaryValue>{userAssets?.stakedValue || 0}</SummaryValue>
        </SummaryItem>
      </AssetSummary>

      <AssetsSection>
        <SectionTitle>Your Assets</SectionTitle>
        
        {userAssets?.assets?.length === 0 ? (
          <NoAssetsMessage>You don't have any digital assets yet.</NoAssetsMessage>
        ) : (
          <AssetsList>
            {userAssets?.assets?.map((asset: any) => (
              <AssetCard key={asset.id} status={asset.status}>
                <AssetHeader>
                  <AssetName>{asset.name}</AssetName>
                  <AssetType>{asset.type}</AssetType>
                </AssetHeader>
                <AssetDescription>{asset.description}</AssetDescription>
                <AssetValue>Value: {asset.value}</AssetValue>
                
                {asset.status === 'LOCKED' && (
                  <AssetLockInfo>
                    <LockIcon>🔒</LockIcon>
                    <LockText>
                      Locked until: {new Date(asset.lockInfo?.lockedUntil).toLocaleDateString()}
                      <br />
                      Reason: {asset.lockInfo?.reason}
                    </LockText>
                  </AssetLockInfo>
                )}
                
                <AssetActions>
                  {asset.status === 'ACTIVE' && userAge < 18 && (
                    <Button $variant="outline" onClick={() => handleLockAsset(asset.id)}>
                      Lock Until 18
                    </Button>
                  )}
                  
                  {asset.status === 'LOCKED' && userAge >= 18 && isKYCVerified && (
                    <Button $variant="primary" onClick={() => handleUnlockAttempt(asset.id)}>
                      Unlock
                    </Button>
                  )}
                  
                  {asset.status === 'LOCKED' && (
                    <Button $variant="outline" onClick={() => handleCompoundAsset(asset.id)}>
                      Compound
                    </Button>
                  )}
                  
                  {asset.status === 'ACTIVE' && (
                    <>
                      <Button $variant="outline" onClick={() => {}}>Transfer</Button>
                      <Button $variant="outline" onClick={() => {}}>Stake</Button>
                    </>
                  )}
                </AssetActions>
              </AssetCard>
            ))}
          </AssetsList>
        )}
      </AssetsSection>

      {userAge < 18 && (
        <InfoSection>
          <InfoTitle>About Age-Restricted Assets</InfoTitle>
          <InfoContent>
            <p>As you are under 18, certain digital assets will be locked until you reach the legal age of access.</p>
            <p>While locked, your assets will continue to:</p>
            <ul>
              <li>Be securely stored in your account</li>
              <li>Compound in value over time</li>
              <li>Be minted and mined automatically</li>
              <li>Accumulate staking rewards</li>
            </ul>
            <p>Once you turn 18 and complete KYC verification, you'll gain full access to all your digital assets.</p>
          </InfoContent>
        </InfoSection>
      )}
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

const AgeRestrictionBanner = styled.div`
  background-color: #fff8e1;
  border-left: 4px solid #ffc107;
  padding: 1rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
`;

const SuccessMessage = styled.div`
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  position: relative;
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

const AssetSummary = styled.div`
  display: flex;
  justify-content: space-between;
  background-color: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
`;

const SummaryItem = styled.div`
  text-align: center;
  flex: 1;
`;

const SummaryLabel = styled.div`
  font-size: 0.875rem;
  color: ${props => props.theme.colors.textLight};
  margin-bottom: 0.5rem;
`;

const SummaryValue = styled.div`
  font-size: 1.5rem;
  font-weight: 600;
  color: ${props => props.theme.colors.text};
`;

const AssetsSection = styled.div`
  margin-bottom: 2rem;
`;

const SectionTitle = styled.h2`
  font-size: 1.5rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 1.5rem;
`;

const NoAssetsMessage = styled.div`
  text-align: center;
  padding: 2rem;
  background-color: #f8fafc;
  border-radius: 8px;
  color: ${props => props.theme.colors.textLight};
`;

const AssetsList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
`;

const AssetCard = styled.div<{ status: string }>`
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border-left: 4px solid ${props => {
    switch (props.status) {
      case 'LOCKED':
        return '#ffc107';
      case 'STAKED':
        return '#3f51b5';
      case 'ACTIVE':
        return '#4caf50';
      default:
        return '#e0e0e0';
    }
  }};
`;

const AssetHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const AssetName = styled.h3`
  font-size: 1.25rem;
  color: ${props => props.theme.colors.text};
  margin: 0;
`;

const AssetType = styled.span`
  font-size: 0.75rem;
  background-color: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  color: ${props => props.theme.colors.textLight};
`;

const AssetDescription = styled.p`
  color: ${props => props.theme.colors.textLight};
  margin-bottom: 1rem;
  font-size: 0.875rem;
`;

const AssetValue = styled.div`
  font-weight: 600;
  margin-bottom: 1rem;
`;

const AssetLockInfo = styled.div`
  display: flex;
  align-items: center;
  background-color: #fff8e1;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
`;

const LockIcon = styled.span`
  font-size: 1.5rem;
  margin-right: 0.75rem;
`;

const LockText = styled.div`
  font-size: 0.875rem;
`;

const AssetActions = styled.div`
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
`;

const InfoSection = styled.div`
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 2rem;
`;

const InfoTitle = styled.h3`
  font-size: 1.25rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 1rem;
`;

const InfoContent = styled.div`
  color: ${props => props.theme.colors.textLight};
  
  p {
    margin-bottom: 1rem;
  }
  
  ul {
    padding-left: 1.5rem;
    margin-bottom: 1rem;
    
    li {
      margin-bottom: 0.5rem;
    }
  }
`;

const LoadingContainer = styled.div`
  text-align: center;
  padding: 2rem;
`;

const ErrorContainer = styled.div`
  background-color: #ffebee;
  color: #d32f2f;
  padding: 1rem;
  border-radius: 4px;
  margin: 2rem auto;
  max-width: 600px;
`;

export default DigitalAssetLocking;
