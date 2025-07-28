import React, { useState } from 'react';
import styled from 'styled-components';
import { Button } from '../components/ui/Button';
import MainLayout from '../components/layout/MainLayout';

interface JobCardImageProps {
  $image?: string;
}

interface FilterButtonProps {
  $active?: boolean;
}

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

const Header = styled.header`
  margin-bottom: 2rem;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: 1rem;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  color: ${({ theme }) => theme.colors.textLight};
  max-width: 800px;
  margin: 0 auto;
`;

const FilterSection = styled.div`
  margin-bottom: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
`;

const FilterButton = styled.button<FilterButtonProps>`
  padding: 0.5rem 1rem;
  background-color: ${props => props.$active ? props.theme.colors.primary : 'white'};
  color: ${props => props.$active ? 'white' : props.theme.colors.text};
  border: 1px solid ${props => props.$active ? props.theme.colors.primary : props.theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background-color: ${props => props.$active ? props.theme.colors.primary : props.theme.colors.backgroundLight};
  }
`;

const JobsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: 3rem;
`;

const JobCard = styled.div`
  background-color: white;
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: 1.5rem;
  box-shadow: ${({ theme }) => theme.shadows.small};
  display: flex;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const JobCardImage = styled.div<JobCardImageProps>`
  width: 80px;
  height: 80px;
  background-color: ${({ theme }) => theme.colors.background};
  background-image: ${props => props.$image ? `url(${props.$image})` : 'none'};
  background-size: cover;
  background-position: center;
  border-radius: ${({ theme }) => theme.borderRadius};
  margin-right: 1.5rem;
  
  @media (max-width: 768px) {
    margin-bottom: 1rem;
  }
`;

const JobCardContent = styled.div`
  flex: 1;
`;

const JobCardHeader = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const JobCardTitle = styled.h3`
  font-size: 1.2rem;
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: 0.5rem;
`;

const JobCardCompany = styled.div`
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.textLight};
  margin-bottom: 0.5rem;
`;

const JobCardSalary = styled.div`
  font-size: 1.1rem;
  font-weight: bold;
  color: ${({ theme }) => theme.colors.primary};
  
  @media (max-width: 768px) {
    margin-bottom: 0.5rem;
  }
`;

const JobCardDescription = styled.p`
  font-size: 0.95rem;
  color: ${({ theme }) => theme.colors.textLight};
  margin-bottom: 1rem;
  line-height: 1.6;
`;

const JobCardMeta = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.textLight};
`;

const JobCardTag = styled.span`
  background-color: ${({ theme }) => theme.colors.backgroundLight};
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
`;

const JobCardFooter = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
`;

const JobCardLocation = styled.div`
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.textLight};
`;

const PostJobSection = styled.div`
  background-color: ${({ theme }) => theme.colors.backgroundLight};
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: 2rem;
  margin-bottom: 3rem;
`;

const PostJobTitle = styled.h2`
  font-size: 1.8rem;
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: 1rem;
`;

const PostJobDescription = styled.p`
  font-size: 1.1rem;
  color: ${({ theme }) => theme.colors.textLight};
  margin-bottom: 1.5rem;
  line-height: 1.6;
  max-width: 800px;
`;

const BusinessPlansSection = styled.div`
  margin-bottom: 3rem;
`;

const BusinessPlansTitle = styled.h2`
  font-size: 1.8rem;
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: 1rem;
  text-align: center;
`;

const BusinessPlansDescription = styled.p`
  font-size: 1.1rem;
  color: ${({ theme }) => theme.colors.textLight};
  margin-bottom: 2rem;
  line-height: 1.6;
  max-width: 800px;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
`;

const BusinessPlansGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
`;

const PlanCard = styled.div`
  background-color: white;
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: 2rem;
  box-shadow: ${({ theme }) => theme.shadows.small};
  display: flex;
  flex-direction: column;
  
  &:hover {
    box-shadow: ${({ theme }) => theme.shadows.medium};
  }
`;

const PlanTitle = styled.h3`
  font-size: 1.5rem;
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: 0.5rem;
  text-align: center;
`;

const PlanPrice = styled.div`
  font-size: 2rem;
  font-weight: bold;
  color: ${({ theme }) => theme.colors.primary};
  margin-bottom: 1.5rem;
  text-align: center;
`;

const PlanFeatures = styled.ul`
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
  flex: 1;
`;

const PlanFeatureItem = styled.li`
  padding: 0.5rem 0;
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.text};
  display: flex;
  align-items: center;
  
  &:before {
    content: "✓";
    color: ${({ theme }) => theme.colors.success};
    margin-right: 0.5rem;
    font-weight: bold;
  }
`;

const JobsPage = () => {
  const [filter, setFilter] = useState('all');
  
  // Simulated job data
  const jobs = [
    {
      id: 1,
      title: 'Senior Frontend Developer',
      company: 'TechCorp',
      logo: '/images/techcorp-logo.jpg',
      location: 'San Francisco, CA (Remote)',
      salary: '$120,000 - $150,000',
      description: 'We are looking for an experienced Frontend Developer to join our team and help build innovative web applications.',
      tags: ['React', 'TypeScript', 'Next.js'],
      postedDate: '2 days ago',
      type: 'Full-time'
    },
    {
      id: 2,
      title: 'Product Manager',
      company: 'InnovateCo',
      logo: '/images/innovateco-logo.jpg',
      location: 'New York, NY',
      salary: '$110,000 - $140,000',
      description: 'Join our product team to lead the development of cutting-edge digital products from conception to launch.',
      tags: ['Product Management', 'Agile', 'UX'],
      postedDate: '1 week ago',
      type: 'Full-time'
    },
    {
      id: 3,
      title: 'Digital Marketing Specialist',
      company: 'GrowthMedia',
      logo: '/images/growthmedia-logo.jpg',
      location: 'Chicago, IL (Hybrid)',
      salary: '$70,000 - $90,000',
      description: 'Help our clients grow their online presence through strategic digital marketing campaigns.',
      tags: ['SEO', 'Social Media', 'Content Marketing'],
      postedDate: '3 days ago',
      type: 'Full-time'
    },
    {
      id: 4,
      title: 'UX/UI Designer',
      company: 'DesignHub',
      logo: '/images/designhub-logo.jpg',
      location: 'Austin, TX (Remote)',
      salary: '$90,000 - $120,000',
      description: 'Create beautiful and intuitive user experiences for web and mobile applications.',
      tags: ['Figma', 'UI Design', 'User Research'],
      postedDate: '5 days ago',
      type: 'Contract'
    },
    {
      id: 5,
      title: 'Data Scientist',
      company: 'AnalyticsPro',
      logo: '/images/analyticspro-logo.jpg',
      location: 'Boston, MA',
      salary: '$130,000 - $160,000',
      description: 'Apply machine learning and statistical analysis to solve complex business problems.',
      tags: ['Python', 'Machine Learning', 'SQL'],
      postedDate: '1 day ago',
      type: 'Full-time'
    }
  ];
  
  // Filter jobs based on selected filter
  const filteredJobs = filter === 'all' ? jobs : jobs.filter(job => job.type.toLowerCase() === filter.toLowerCase());
  
  // Business plan data
  const businessPlans = [
    {
      title: 'Basic',
      price: '$49/month',
      features: [
        'Post up to 5 job listings',
        'Company profile page',
        'Basic applicant tracking',
        'Email notifications',
        '30-day job postings'
      ]
    },
    {
      title: 'Professional',
      price: '$99/month',
      features: [
        'Post up to 15 job listings',
        'Enhanced company profile',
        'Advanced applicant tracking',
        'Featured job listings',
        'Applicant screening tools',
        '60-day job postings',
        'Basic analytics'
      ]
    },
    {
      title: 'Enterprise',
      price: '$249/month',
      features: [
        'Unlimited job listings',
        'Premium company profile',
        'Complete ATS integration',
        'Featured company placement',
        'Advanced screening & assessments',
        '90-day job postings',
        'Comprehensive analytics',
        'Dedicated account manager'
      ]
    }
  ];
  
  return (
    <MainLayout>
      <Container>
        <Header>
          <Title>Job Marketplace</Title>
          <Subtitle>
            Find your next opportunity or hire top talent with our BuddyBoss-style job marketplace.
          </Subtitle>
        </Header>
        
        <FilterSection>
          <FilterButton $active={filter === 'all'} onClick={() => setFilter('all')}>
            All Jobs
          </FilterButton>
          <FilterButton $active={filter === 'full-time'} onClick={() => setFilter('full-time')}>
            Full-time
          </FilterButton>
          <FilterButton $active={filter === 'part-time'} onClick={() => setFilter('part-time')}>
            Part-time
          </FilterButton>
          <FilterButton $active={filter === 'contract'} onClick={() => setFilter('contract')}>
            Contract
          </FilterButton>
          <FilterButton $active={filter === 'internship'} onClick={() => setFilter('internship')}>
            Internship
          </FilterButton>
        </FilterSection>
        
        <JobsGrid>
          {filteredJobs.map(job => (
            <JobCard key={job.id}>
              <JobCardImage $image={job.logo} />
              <JobCardContent>
                <JobCardHeader>
                  <div>
                    <JobCardTitle>{job.title}</JobCardTitle>
                    <JobCardCompany>{job.company}</JobCardCompany>
                  </div>
                  <JobCardSalary>{job.salary}</JobCardSalary>
                </JobCardHeader>
                <JobCardDescription>{job.description}</JobCardDescription>
                <JobCardMeta>
                  {job.tags.map((tag, index) => (
                    <JobCardTag key={index}>{tag}</JobCardTag>
                  ))}
                </JobCardMeta>
                <JobCardFooter>
                  <JobCardLocation>
                    📍 {job.location} • {job.type} • Posted {job.postedDate}
                  </JobCardLocation>
                  <Button $variant="primary" size="small">Apply Now</Button>
                </JobCardFooter>
              </JobCardContent>
            </JobCard>
          ))}
        </JobsGrid>
        
        <PostJobSection>
          <PostJobTitle>Are You Hiring?</PostJobTitle>
          <PostJobDescription>
            Post your job listings and reach thousands of qualified candidates. 
            Our platform provides powerful tools for recruitment and applicant management.
          </PostJobDescription>
          <Button $variant="primary">Post a Job</Button>
        </PostJobSection>
        
        <BusinessPlansSection>
          <BusinessPlansTitle>Business Plans</BusinessPlansTitle>
          <BusinessPlansDescription>
            Choose the right plan for your recruitment needs. All plans include access to our 
            AI-powered matching system and applicant tracking tools.
          </BusinessPlansDescription>
          
          <BusinessPlansGrid>
            {businessPlans.map((plan, index) => (
              <PlanCard key={index}>
                <PlanTitle>{plan.title}</PlanTitle>
                <PlanPrice>{plan.price}</PlanPrice>
                <PlanFeatures>
                  {plan.features.map((feature, featureIndex) => (
                    <PlanFeatureItem key={featureIndex}>{feature}</PlanFeatureItem>
                  ))}
                </PlanFeatures>
                <Button $variant="primary">Select Plan</Button>
              </PlanCard>
            ))}
          </BusinessPlansGrid>
        </BusinessPlansSection>
      </Container>
    </MainLayout>
  );
};

export default JobsPage;
