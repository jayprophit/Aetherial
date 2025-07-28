import React, { useState } from 'react';
import styled from 'styled-components';
import { Button } from '../components/ui/Button';
import MainLayout from '../components/layout/MainLayout';

interface CourseCardImageProps {
  $image?: string;
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

const CoursesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
`;

const CourseCard = styled.div`
  background-color: white;
  border-radius: ${({ theme }) => theme.borderRadius};
  overflow: hidden;
  box-shadow: ${({ theme }) => theme.shadows.small};
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: ${({ theme }) => theme.shadows.medium};
  }
`;

const CourseCardImage = styled.div<CourseCardImageProps>`
  height: 180px;
  background-color: ${({ theme }) => theme.colors.background};
  background-image: ${props => props.$image ? `url(${props.$image})` : 'none'};
  background-size: cover;
  background-position: center;
  border-radius: ${({ theme }) => theme.borderRadius} ${({ theme }) => theme.borderRadius} 0 0;
`;

const CourseCardContent = styled.div`
  padding: 1.5rem;
`;

const CourseCardTitle = styled.h3`
  font-size: 1.2rem;
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: 0.5rem;
`;

const CourseCardDescription = styled.p`
  font-size: 0.95rem;
  color: ${({ theme }) => theme.colors.textLight};
  margin-bottom: 1rem;
  line-height: 1.6;
`;

const CourseCardMeta = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.textLight};
`;

const AgeRestriction = styled.span`
  background-color: ${({ theme }) => theme.colors.warning};
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
`;

const FilterSection = styled.div`
  margin-bottom: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
`;

const FilterButton = styled.button<{ $active?: boolean }>`
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

const CreateCourseSection = styled.div`
  background-color: ${({ theme }) => theme.colors.backgroundLight};
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: 2rem;
  margin-bottom: 3rem;
`;

const CreateCourseTitle = styled.h2`
  font-size: 1.8rem;
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: 1rem;
`;

const CreateCourseDescription = styled.p`
  font-size: 1.1rem;
  color: ${({ theme }) => theme.colors.textLight};
  margin-bottom: 1.5rem;
  line-height: 1.6;
  max-width: 800px;
`;

const EducationPage = () => {
  const [filter, setFilter] = useState('all');
  const [userAge, setUserAge] = useState(25); // Simulated user age
  
  // Simulated course data
  const courses = [
    {
      id: 1,
      title: 'Introduction to Digital Marketing',
      description: 'Learn the fundamentals of digital marketing, including SEO, social media, and content strategy.',
      image: '/images/digital-marketing.jpg',
      duration: '4 weeks',
      level: 'Beginner',
      ageRestriction: 0
    },
    {
      id: 2,
      title: 'Advanced Blockchain Development',
      description: 'Deep dive into blockchain technology and smart contract development with real-world applications.',
      image: '/images/blockchain.jpg',
      duration: '8 weeks',
      level: 'Advanced',
      ageRestriction: 16
    },
    {
      id: 3,
      title: 'Financial Literacy for Teens',
      description: 'Essential financial concepts and practices tailored for teenagers to build a strong financial foundation.',
      image: '/images/finance.jpg',
      duration: '3 weeks',
      level: 'Beginner',
      ageRestriction: 13
    },
    {
      id: 4,
      title: 'Professional Photography Masterclass',
      description: 'Comprehensive guide to professional photography techniques, equipment, and post-processing.',
      image: '/images/photography.jpg',
      duration: '6 weeks',
      level: 'Intermediate',
      ageRestriction: 0
    },
    {
      id: 5,
      title: 'Cryptocurrency Trading Strategies',
      description: 'Advanced trading techniques and market analysis for cryptocurrency markets.',
      image: '/images/crypto-trading.jpg',
      duration: '5 weeks',
      level: 'Advanced',
      ageRestriction: 18
    },
    {
      id: 6,
      title: 'Game Development for Beginners',
      description: 'Introduction to game development concepts, tools, and basic programming for aspiring game creators.',
      image: '/images/game-dev.jpg',
      duration: '7 weeks',
      level: 'Beginner',
      ageRestriction: 13
    }
  ];
  
  // Filter courses based on selected filter and age restrictions
  const filteredCourses = courses.filter(course => {
    // Filter by category
    if (filter !== 'all' && course.level.toLowerCase() !== filter.toLowerCase()) {
      return false;
    }
    
    // Filter by age restriction
    if (course.ageRestriction > userAge) {
      return false;
    }
    
    return true;
  });
  
  return (
    <MainLayout>
      <Container>
        <Header>
          <Title>E-Learning Platform</Title>
          <Subtitle>
            Discover courses, expand your knowledge, and develop new skills with our age-appropriate learning content.
          </Subtitle>
        </Header>
        
        <FilterSection>
          <FilterButton $active={filter === 'all'} onClick={() => setFilter('all')}>
            All Courses
          </FilterButton>
          <FilterButton $active={filter === 'beginner'} onClick={() => setFilter('beginner')}>
            Beginner
          </FilterButton>
          <FilterButton $active={filter === 'intermediate'} onClick={() => setFilter('intermediate')}>
            Intermediate
          </FilterButton>
          <FilterButton $active={filter === 'advanced'} onClick={() => setFilter('advanced')}>
            Advanced
          </FilterButton>
        </FilterSection>
        
        <CoursesGrid>
          {filteredCourses.map(course => (
            <CourseCard key={course.id}>
              <CourseCardImage $image={course.image} />
              <CourseCardContent>
                <CourseCardTitle>{course.title}</CourseCardTitle>
                <CourseCardMeta>
                  <span>{course.duration}</span>
                  <span>{course.level}</span>
                  {course.ageRestriction > 0 && (
                    <AgeRestriction>{course.ageRestriction}+</AgeRestriction>
                  )}
                </CourseCardMeta>
                <CourseCardDescription>{course.description}</CourseCardDescription>
                <Button $variant="primary">Enroll Now</Button>
              </CourseCardContent>
            </CourseCard>
          ))}
        </CoursesGrid>
        
        <CreateCourseSection>
          <CreateCourseTitle>Create Your Own Course</CreateCourseTitle>
          <CreateCourseDescription>
            Share your expertise with our community by creating and publishing your own courses.
            Our platform provides all the tools you need to create engaging learning experiences.
          </CreateCourseDescription>
          <Button $variant="primary">Start Creating</Button>
        </CreateCourseSection>
      </Container>
    </MainLayout>
  );
};

export default EducationPage;
