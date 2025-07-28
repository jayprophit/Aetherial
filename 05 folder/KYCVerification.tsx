import React, { useState } from 'react';
import styled from 'styled-components';
import Button from '../ui/Button';

interface KYCVerificationProps {
  onVerificationComplete: (verified: boolean) => void;
  userId: string;
}

enum VerificationStep {
  INITIAL = 'initial',
  ID_UPLOAD = 'id_upload',
  SELFIE = 'selfie',
  ADDRESS_PROOF = 'address_proof',
  PROCESSING = 'processing',
  COMPLETE = 'complete',
  FAILED = 'failed'
}

const KYCVerification: React.FC<KYCVerificationProps> = ({ onVerificationComplete, userId }) => {
  const [currentStep, setCurrentStep] = useState<VerificationStep>(VerificationStep.INITIAL);
  const [idDocument, setIdDocument] = useState<File | null>(null);
  const [selfieImage, setSelfieImage] = useState<File | null>(null);
  const [addressProof, setAddressProof] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [userAge, setUserAge] = useState<number | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>, fileType: 'id' | 'selfie' | 'address') => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      
      // Check file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError('File size exceeds 5MB limit');
        return;
      }
      
      // Check file type
      const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
      if (!validTypes.includes(file.type)) {
        setError('Invalid file type. Please upload JPG, PNG or PDF');
        return;
      }
      
      setError(null);
      
      switch (fileType) {
        case 'id':
          setIdDocument(file);
          break;
        case 'selfie':
          setSelfieImage(file);
          break;
        case 'address':
          setAddressProof(file);
          break;
      }
    }
  };

  const proceedToNextStep = () => {
    switch (currentStep) {
      case VerificationStep.INITIAL:
        setCurrentStep(VerificationStep.ID_UPLOAD);
        break;
      case VerificationStep.ID_UPLOAD:
        if (idDocument) {
          setCurrentStep(VerificationStep.SELFIE);
        } else {
          setError('Please upload your ID document');
        }
        break;
      case VerificationStep.SELFIE:
        if (selfieImage) {
          setCurrentStep(VerificationStep.ADDRESS_PROOF);
        } else {
          setError('Please upload your selfie');
        }
        break;
      case VerificationStep.ADDRESS_PROOF:
        if (addressProof) {
          submitVerification();
        } else {
          setError('Please upload proof of address');
        }
        break;
    }
  };

  const submitVerification = async () => {
    setIsProcessing(true);
    setCurrentStep(VerificationStep.PROCESSING);
    
    try {
      // In a real implementation, this would call a backend API
      // For demo purposes, we'll simulate the verification process
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Simulate successful verification
      setCurrentStep(VerificationStep.COMPLETE);
      
      // Set a mock age for the user (over 18)
      const mockAge = 25;
      setUserAge(mockAge);
      
      onVerificationComplete(true);
    } catch (err) {
      setCurrentStep(VerificationStep.FAILED);
      setError('Verification failed. Please try again.');
      onVerificationComplete(false);
    } finally {
      setIsProcessing(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case VerificationStep.INITIAL:
        return (
          <>
            <StepTitle>KYC Verification</StepTitle>
            <StepDescription>
              To access full platform features, we need to verify your identity. This process requires:
              <RequirementsList>
                <li>A valid government-issued ID (passport, driver's license, or ID card)</li>
                <li>A selfie photo of yourself</li>
                <li>Proof of address (utility bill, bank statement, etc.)</li>
              </RequirementsList>
              <ImportantNote>
                Users under 18 will have limited access to certain features, and digital assets will be locked until legal age of access.
              </ImportantNote>
            </StepDescription>
            <Button $variant="primary" onClick={proceedToNextStep}>Start Verification</Button>
          </>
        );
      
      case VerificationStep.ID_UPLOAD:
        return (
          <>
            <StepTitle>Upload ID Document</StepTitle>
            <StepDescription>
              Please upload a clear photo or scan of your government-issued ID.
              <br />
              Accepted formats: JPG, PNG, PDF (max 5MB)
            </StepDescription>
            <FileUploadContainer>
              <FileInput
                type="file"
                accept=".jpg,.jpeg,.png,.pdf"
                onChange={(e) => handleFileUpload(e, 'id')}
              />
              {idDocument && (
                <FileName>Selected: {idDocument.name}</FileName>
              )}
            </FileUploadContainer>
            <ButtonContainer>
              <Button $variant="outline" onClick={() => setCurrentStep(VerificationStep.INITIAL)}>Back</Button>
              <Button $variant="primary" onClick={proceedToNextStep}>Next</Button>
            </ButtonContainer>
          </>
        );
      
      case VerificationStep.SELFIE:
        return (
          <>
            <StepTitle>Upload Selfie</StepTitle>
            <StepDescription>
              Please upload a clear selfie photo of yourself holding your ID document.
              <br />
              Accepted formats: JPG, PNG (max 5MB)
            </StepDescription>
            <FileUploadContainer>
              <FileInput
                type="file"
                accept=".jpg,.jpeg,.png"
                onChange={(e) => handleFileUpload(e, 'selfie')}
              />
              {selfieImage && (
                <FileName>Selected: {selfieImage.name}</FileName>
              )}
            </FileUploadContainer>
            <ButtonContainer>
              <Button $variant="outline" onClick={() => setCurrentStep(VerificationStep.ID_UPLOAD)}>Back</Button>
              <Button $variant="primary" onClick={proceedToNextStep}>Next</Button>
            </ButtonContainer>
          </>
        );
      
      case VerificationStep.ADDRESS_PROOF:
        return (
          <>
            <StepTitle>Upload Proof of Address</StepTitle>
            <StepDescription>
              Please upload a document showing your current address (utility bill, bank statement, etc.).
              <br />
              Document must be less than 3 months old.
              <br />
              Accepted formats: JPG, PNG, PDF (max 5MB)
            </StepDescription>
            <FileUploadContainer>
              <FileInput
                type="file"
                accept=".jpg,.jpeg,.png,.pdf"
                onChange={(e) => handleFileUpload(e, 'address')}
              />
              {addressProof && (
                <FileName>Selected: {addressProof.name}</FileName>
              )}
            </FileUploadContainer>
            <ButtonContainer>
              <Button $variant="outline" onClick={() => setCurrentStep(VerificationStep.SELFIE)}>Back</Button>
              <Button $variant="primary" onClick={proceedToNextStep}>Submit</Button>
            </ButtonContainer>
          </>
        );
      
      case VerificationStep.PROCESSING:
        return (
          <>
            <StepTitle>Processing Verification</StepTitle>
            <StepDescription>
              Please wait while we verify your information. This may take a few moments.
            </StepDescription>
            <LoadingIndicator />
          </>
        );
      
      case VerificationStep.COMPLETE:
        return (
          <>
            <StepTitle>Verification Complete</StepTitle>
            <StepDescription>
              Your identity has been successfully verified. You now have full access to all platform features.
              {userAge !== null && userAge < 18 && (
                <ImportantNote>
                  As you are under 18, certain features will be restricted and digital assets will be locked until you reach the legal age of access.
                </ImportantNote>
              )}
            </StepDescription>
            <Button $variant="primary" onClick={() => window.location.reload()}>Continue to Platform</Button>
          </>
        );
      
      case VerificationStep.FAILED:
        return (
          <>
            <StepTitle>Verification Failed</StepTitle>
            <StepDescription>
              We were unable to verify your identity. Please check your documents and try again.
            </StepDescription>
            <Button $variant="primary" onClick={() => setCurrentStep(VerificationStep.INITIAL)}>Try Again</Button>
          </>
        );
    }
  };

  return (
    <KYCContainer>
      <ProgressIndicator>
        <ProgressStep active={currentStep === VerificationStep.INITIAL} completed={currentStep !== VerificationStep.INITIAL}>1</ProgressStep>
        <ProgressLine completed={currentStep !== VerificationStep.INITIAL} />
        <ProgressStep active={currentStep === VerificationStep.ID_UPLOAD} completed={currentStep !== VerificationStep.INITIAL && currentStep !== VerificationStep.ID_UPLOAD}>2</ProgressStep>
        <ProgressLine completed={currentStep !== VerificationStep.INITIAL && currentStep !== VerificationStep.ID_UPLOAD} />
        <ProgressStep active={currentStep === VerificationStep.SELFIE} completed={currentStep !== VerificationStep.INITIAL && currentStep !== VerificationStep.ID_UPLOAD && currentStep !== VerificationStep.SELFIE}>3</ProgressStep>
        <ProgressLine completed={currentStep !== VerificationStep.INITIAL && currentStep !== VerificationStep.ID_UPLOAD && currentStep !== VerificationStep.SELFIE} />
        <ProgressStep active={currentStep === VerificationStep.ADDRESS_PROOF} completed={currentStep === VerificationStep.PROCESSING || currentStep === VerificationStep.COMPLETE}>4</ProgressStep>
      </ProgressIndicator>
      
      <ContentContainer>
        {error && <ErrorMessage>{error}</ErrorMessage>}
        {renderStepContent()}
      </ContentContainer>
    </KYCContainer>
  );
};

// Styled components
const KYCContainer = styled.div`
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const ProgressIndicator = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
`;

const ProgressStep = styled.div<{ active: boolean; completed: boolean }>`
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${props => props.active ? props.theme.colors.primary : props.completed ? props.theme.colors.success : props.theme.colors.secondaryDark};
  color: #ffffff;
  font-weight: bold;
`;

const ProgressLine = styled.div<{ completed: boolean }>`
  flex: 1;
  height: 2px;
  background-color: ${props => props.completed ? props.theme.colors.success : props.theme.colors.secondaryDark};
  margin: 0 10px;
`;

const ContentContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const StepTitle = styled.h2`
  font-size: 1.5rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 0.5rem;
`;

const StepDescription = styled.p`
  color: ${props => props.theme.colors.textLight};
  margin-bottom: 1.5rem;
`;

const RequirementsList = styled.ul`
  margin: 1rem 0;
  padding-left: 1.5rem;
  
  li {
    margin-bottom: 0.5rem;
  }
`;

const ImportantNote = styled.div`
  background-color: #fff8e1;
  border-left: 4px solid #ffc107;
  padding: 1rem;
  margin: 1rem 0;
  font-weight: 500;
`;

const FileUploadContainer = styled.div`
  margin-bottom: 1.5rem;
`;

const FileInput = styled.input`
  width: 100%;
  padding: 0.5rem;
  border: 1px dashed ${props => props.theme.colors.primary};
  border-radius: 4px;
`;

const FileName = styled.div`
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: ${props => props.theme.colors.textLight};
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 1rem;
`;

const ErrorMessage = styled.div`
  background-color: #ffebee;
  color: #d32f2f;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
`;

const LoadingIndicator = styled.div`
  width: 40px;
  height: 40px;
  margin: 1rem auto;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: ${props => props.theme.colors.primary};
  border-radius: 50%;
  animation: spin 1s linear infinite;
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

export default KYCVerification;
