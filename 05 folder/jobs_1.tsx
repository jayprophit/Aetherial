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

const JobsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: 3rem;
`;

const JobCard = styled(Card)`
  transition: transform 0.2s ease-in-out;
  
  &:hover {
    transform: translateY(-3px);
  }
`;

const JobHeader = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
`;

const CompanyLogo = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 8px;
  background-color: #F1F5F9;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.5rem;
  color: #4A6CF7;
`;

const JobInfo = styled.div`
  flex: 1;
`;

const JobTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
`;

const CompanyName = styled.div`
  font-size: 1rem;
  color: #64748B;
`;

const JobMeta = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
`;

const JobMetaItem = styled.div`
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #64748B;
  
  &::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #4A6CF7;
    margin-right: 0.5rem;
  }
`;

const JobDescription = styled.p`
  color: #334155;
  margin-bottom: 1.5rem;
`;

const JobSkills = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
`;

const SkillTag = styled.div`
  font-size: 0.75rem;
  color: #4A6CF7;
  background-color: #EFF6FF;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
`;

const JobFooter = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const JobSalary = styled.div`
  font-weight: 600;
  color: #4A6CF7;
`;

const FiltersContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #F8FAFC;
  border-radius: 0.5rem;
`;

const FilterGroup = styled.div`
  display: flex;
  flex-direction: column;
  min-width: 200px;
`;

const FilterLabel = styled.label`
  font-weight: 600;
  margin-bottom: 0.5rem;
`;

const FilterSelect = styled.select`
  padding: 0.5rem;
  border: 1px solid #E5E7EB;
  border-radius: 0.375rem;
  
  &:focus {
    outline: none;
    border-color: #4A6CF7;
    box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.2);
  }
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 2rem;
  
  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
`;

const AIMatchingSection = styled.div`
  position: sticky;
  top: 2rem;
  padding: 1.5rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  margin-bottom: 2rem;
`;

const AIMatchingTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  
  &::before {
    content: '🤖';
    margin-right: 0.5rem;
  }
`;

const MatchedJobCard = styled(Card)`
  margin-bottom: 1rem;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const MatchedJobTitle = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
`;

const MatchedJobCompany = styled.div`
  font-size: 0.875rem;
  color: #64748B;
  margin-bottom: 0.5rem;
`;

const MatchScore = styled.div`
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #4A6CF7;
  font-weight: 600;
  margin-bottom: 0.5rem;
`;

const ProgressBar = styled.div<{ $progress: number }>`
  width: 100%;
  height: 6px;
  background-color: #E2E8F0;
  border-radius: 3px;
  margin-bottom: 0.5rem;
  overflow: hidden;
  
  &::after {
    content: '';
    display: block;
    width: ${props => props.$progress}%;
    height: 100%;
    background-color: #4A6CF7;
    border-radius: 3px;
  }
`;

// Sample jobs data
const JOBS = [
  {
    id: 1,
    title: 'Senior Frontend Developer',
    company: 'TechCorp',
    companyLogo: '💻',
    location: 'San Francisco, CA',
    type: 'Full-time',
    remote: true,
    salary: '$120,000 - $150,000',
    description: 'We are looking for an experienced Frontend Developer to join our team. You will be responsible for building user interfaces, implementing features, and ensuring the best user experience.',
    skills: ['React', 'TypeScript', 'CSS', 'Redux', 'Next.js'],
    postedAt: '2 days ago',
  },
  {
    id: 2,
    title: 'Data Scientist',
    company: 'AnalyticsPro',
    companyLogo: '📊',
    location: 'New York, NY',
    type: 'Full-time',
    remote: true,
    salary: '$130,000 - $160,000',
    description: 'Join our data science team to analyze complex datasets, build predictive models, and extract actionable insights to drive business decisions.',
    skills: ['Python', 'Machine Learning', 'SQL', 'Data Visualization', 'Statistics'],
    postedAt: '1 day ago',
  },
  {
    id: 3,
    title: 'DevOps Engineer',
    company: 'CloudSystems',
    companyLogo: '☁️',
    location: 'Austin, TX',
    type: 'Full-time',
    remote: false,
    salary: '$110,000 - $140,000',
    description: 'We are seeking a DevOps Engineer to help us build and maintain our cloud infrastructure, implement CI/CD pipelines, and ensure system reliability and security.',
    skills: ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'CI/CD'],
    postedAt: '3 days ago',
  },
  {
    id: 4,
    title: 'UX/UI Designer',
    company: 'DesignHub',
    companyLogo: '🎨',
    location: 'Remote',
    type: 'Contract',
    remote: true,
    salary: '$80 - $100 per hour',
    description: 'Looking for a talented UX/UI Designer to create beautiful, intuitive interfaces for our products. You will work closely with product managers and developers to deliver exceptional user experiences.',
    skills: ['Figma', 'Adobe XD', 'User Research', 'Prototyping', 'Interaction Design'],
    postedAt: '5 days ago',
  },
  {
    id: 5,
    title: 'Backend Developer',
    company: 'ServerSide',
    companyLogo: '🔧',
    location: 'Seattle, WA',
    type: 'Full-time',
    remote: false,
    salary: '$115,000 - $145,000',
    description: 'Join our backend team to design and implement APIs, optimize database performance, and build scalable services that power our applications.',
    skills: ['Node.js', 'Express', 'MongoDB', 'PostgreSQL', 'API Design'],
    postedAt: '1 week ago',
  },
];

// AI matched jobs
const AI_MATCHED_JOBS = [
  {
    id: 101,
    title: 'Senior React Developer',
    company: 'InnovateX',
    matchScore: 95,
  },
  {
    id: 102,
    title: 'Frontend Team Lead',
    company: 'WebSolutions',
    matchScore: 92,
  },
  {
    id: 103,
    title: 'Full Stack Engineer',
    company: 'TechStart',
    matchScore: 88,
  },
];

// JobsPage component
const JobsPage: React.FC = () => {
  const [typeFilter, setTypeFilter] = useState('All');
  const [locationFilter, setLocationFilter] = useState('All');
  const [remoteFilter, setRemoteFilter] = useState('All');
  const [isClient, setIsClient] = useState(false);

  // Fix for hydration issues
  useEffect(() => {
    setIsClient(true);
  }, []);

  const filteredJobs = JOBS.filter(job => {
    const typeMatch = typeFilter === 'All' || job.type === typeFilter;
    const locationMatch = locationFilter === 'All' || job.location.includes(locationFilter);
    const remoteMatch = remoteFilter === 'All' || 
                        (remoteFilter === 'Remote' && job.remote) || 
                        (remoteFilter === 'On-site' && !job.remote);
    
    return typeMatch && locationMatch && remoteMatch;
  });

  const locationOptions = ['All', 'San Francisco', 'New York', 'Austin', 'Seattle', 'Remote'];
  const typeOptions = ['All', 'Full-time', 'Part-time', 'Contract', 'Internship'];
  const remoteOptions = ['All', 'Remote', 'On-site'];

  if (!isClient) {
    return null;
  }

  return (
    <MainLayout>
      <PageContainer>
        <PageHeader>
          <PageTitle>Job Marketplace</PageTitle>
          <PageDescription>
            Find your next opportunity or hire talent from our diverse pool of professionals.
          </PageDescription>
        </PageHeader>
        
        <FiltersContainer>
          <FilterGroup>
            <FilterLabel htmlFor="type">Job Type</FilterLabel>
            <FilterSelect 
              id="type" 
              value={typeFilter} 
              onChange={(e) => setTypeFilter(e.target.value)}
            >
              {typeOptions.map(option => (
                <option key={option} value={option}>{option}</option>
              ))}
            </FilterSelect>
          </FilterGroup>
          
          <FilterGroup>
            <FilterLabel htmlFor="location">Location</FilterLabel>
            <FilterSelect 
              id="location" 
              value={locationFilter} 
              onChange={(e) => setLocationFilter(e.target.value)}
            >
              {locationOptions.map(option => (
                <option key={option} value={option}>{option}</option>
              ))}
            </FilterSelect>
          </FilterGroup>
          
          <FilterGroup>
            <FilterLabel htmlFor="remote">Remote/On-site</FilterLabel>
            <FilterSelect 
              id="remote" 
              value={remoteFilter} 
              onChange={(e) => setRemoteFilter(e.target.value)}
            >
              {remoteOptions.map(option => (
                <option key={option} value={option}>{option}</option>
              ))}
            </FilterSelect>
          </FilterGroup>
        </FiltersContainer>
        
        <ContentGrid>
          <div>
            <JobsGrid>
              {filteredJobs.map(job => (
                <JobCard key={job.id} $elevated $rounded>
                  <JobHeader>
                    <CompanyLogo>{job.companyLogo}</CompanyLogo>
                    <JobInfo>
                      <JobTitle>{job.title}</JobTitle>
                      <CompanyName>{job.company}</CompanyName>
                    </JobInfo>
                  </JobHeader>
                  
                  <JobMeta>
                    <JobMetaItem>{job.location}</JobMetaItem>
                    <JobMetaItem>{job.type}</JobMetaItem>
                    <JobMetaItem>{job.remote ? 'Remote' : 'On-site'}</JobMetaItem>
                    <JobMetaItem>Posted {job.postedAt}</JobMetaItem>
                  </JobMeta>
                  
                  <JobDescription>{job.description}</JobDescription>
                  
                  <JobSkills>
                    {job.skills.map((skill, index) => (
                      <SkillTag key={index}>{skill}</SkillTag>
                    ))}
                  </JobSkills>
                  
                  <JobFooter>
                    <JobSalary>{job.salary}</JobSalary>
                    <Button variant="primary">Apply Now</Button>
                  </JobFooter>
                </JobCard>
              ))}
            </JobsGrid>
          </div>
          
          <div>
            <AIMatchingSection>
              <AIMatchingTitle>AI Job Matching</AIMatchingTitle>
              <p style={{ marginBottom: '1.5rem' }}>
                Based on your profile and preferences, our AI has found these highly relevant job matches for you.
              </p>
              
              {AI_MATCHED_JOBS.map(job => (
                <MatchedJobCard key={job.id} $bordered $rounded>
                  <MatchedJobTitle>{job.title}</MatchedJobTitle>
                  <MatchedJobCompany>{job.company}</MatchedJobCompany>
                  <MatchScore>{job.matchScore}% Match</MatchScore>
                  <ProgressBar $progress={job.matchScore} />
                  <Button variant="secondary" size="small">View Job</Button>
                </MatchedJobCard>
              ))}
              
              <div style={{ marginTop: '1.5rem' }}>
                <Button variant="primary" $fullWidth>Update Your Profile</Button>
              </div>
            </AIMatchingSection>
          </div>
        </ContentGrid>
      </PageContainer>
    </MainLayout>
  );
};

export default JobsPage;
