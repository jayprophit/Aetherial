// Mobile Navigation Toggle
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('nav');

menuToggle.addEventListener('click', () => {
    nav.classList.toggle('active');
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!nav.contains(e.target) && !menuToggle.contains(e.target) && nav.classList.contains('active')) {
        nav.classList.remove('active');
    }
});

// Project Filtering
const filterBtns = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        filterBtns.forEach(btn => btn.classList.remove('active'));
        
        // Add active class to clicked button
        btn.classList.add('active');
        
        // Get filter value
        const filterValue = btn.getAttribute('data-filter');
        
        // Filter projects
        projectCards.forEach(card => {
            if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
                card.style.display = 'block';
                // Add animation for appearing cards
                setTimeout(() => {
                    card.classList.add('animate-in');
                }, 50);
            } else {
                card.classList.remove('animate-in');
                setTimeout(() => {
                    card.style.display = 'none';
                }, 300);
            }
        });
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            // Close mobile menu if open
            if (nav.classList.contains('active')) {
                nav.classList.remove('active');
            }
            
            // Calculate header height for offset
            const headerHeight = document.querySelector('header').offsetHeight;
            
            // Scroll to target with offset
            window.scrollTo({
                top: targetElement.offsetTop - headerHeight,
                behavior: 'smooth'
            });
        }
    });
});

// Form submission handling with validation and feedback
const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const subject = document.getElementById('subject').value;
        const message = document.getElementById('message').value;
        
        // Reset previous error messages
        document.querySelectorAll('.error-message').forEach(el => el.remove());
        document.querySelectorAll('.form-group').forEach(el => el.classList.remove('error'));
        
        // Validate form
        let isValid = true;
        
        if (!name) {
            showError('name', 'Please enter your name');
            isValid = false;
        }
        
        if (!email) {
            showError('email', 'Please enter your email');
            isValid = false;
        } else if (!isValidEmail(email)) {
            showError('email', 'Please enter a valid email address');
            isValid = false;
        }
        
        if (!subject) {
            showError('subject', 'Please enter a subject');
            isValid = false;
        }
        
        if (!message) {
            showError('message', 'Please enter your message');
            isValid = false;
        }
        
        if (isValid) {
            // Show success message
            const formGroups = document.querySelectorAll('.form-group');
            const submitBtn = document.querySelector('button[type="submit"]');
            
            // Hide form fields
            formGroups.forEach(group => {
                group.style.opacity = '0';
                setTimeout(() => {
                    group.style.display = 'none';
                }, 300);
            });
            
            // Hide submit button
            submitBtn.style.opacity = '0';
            setTimeout(() => {
                submitBtn.style.display = 'none';
                
                // Show success message
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    <h3>Message Sent Successfully!</h3>
                    <p>Thank you for your message, ${name}. I'll get back to you soon.</p>
                    <button class="btn primary-btn" id="sendAnotherBtn">Send Another Message</button>
                `;
                
                contactForm.appendChild(successMessage);
                
                // Add event listener to "Send Another Message" button
                document.getElementById('sendAnotherBtn').addEventListener('click', () => {
                    // Remove success message
                    successMessage.remove();
                    
                    // Show form fields and button again
                    formGroups.forEach(group => {
                        group.style.display = 'block';
                        setTimeout(() => {
                            group.style.opacity = '1';
                        }, 10);
                    });
                    
                    submitBtn.style.display = 'block';
                    setTimeout(() => {
                        submitBtn.style.opacity = '1';
                    }, 10);
                    
                    // Reset form
                    contactForm.reset();
                });
            }, 300);
        }
    });
}

// Helper function to show error message
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const formGroup = field.parentElement;
    
    formGroup.classList.add('error');
    
    const errorMessage = document.createElement('div');
    errorMessage.className = 'error-message';
    errorMessage.textContent = message;
    
    formGroup.appendChild(errorMessage);
}

// Helper function to validate email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Add active class to navigation links based on scroll position
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('nav ul li a');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        const headerHeight = document.querySelector('header').offsetHeight;
        
        if (window.pageYOffset >= sectionTop - headerHeight - 10) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Add scroll class to header for styling on scroll
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Animate skill bars on scroll
const animateSkills = () => {
    const skills = document.querySelectorAll('.skill-level');
    skills.forEach(skill => {
        skill.style.width = skill.style.width || '0%';
        const targetWidth = skill.getAttribute('style').split('width:')[1].trim().split('%')[0];
        skill.style.width = '0%';
        setTimeout(() => {
            skill.style.width = targetWidth + '%';
            skill.style.transition = 'width 1s ease-in-out';
        }, 200);
    });
};

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.2
};

// Create observer for About section
const aboutObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateSkills();
            aboutObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe About section
const aboutSection = document.querySelector('#about');
if (aboutSection) {
    aboutObserver.observe(aboutSection);
}

// Create observer for project cards
const projectObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
            projectObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe each project card
projectCards.forEach(card => {
    projectObserver.observe(card);
});

// Dark mode toggle
const createDarkModeToggle = () => {
    const header = document.querySelector('header .container');
    
    // Create dark mode toggle button
    const darkModeToggle = document.createElement('div');
    darkModeToggle.className = 'dark-mode-toggle';
    darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    
    // Add dark mode toggle to header
    header.appendChild(darkModeToggle);
    
    // Check for saved user preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // Add event listener to dark mode toggle
    darkModeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        
        if (document.body.classList.contains('dark-mode')) {
            darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            localStorage.setItem('theme', 'dark');
        } else {
            darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            localStorage.setItem('theme', 'light');
        }
    });
};

// Initialize dark mode toggle
createDarkModeToggle();

// Add typing animation to hero section
const createTypingAnimation = () => {
    const heroTitle = document.querySelector('.hero-content h1');
    const originalText = heroTitle.innerHTML;
    const nameSpan = heroTitle.querySelector('span');
    const nameText = nameSpan.textContent;
    
    // Replace original text with animation container
    heroTitle.innerHTML = `Hello, I'm <span class="typing-container"><span class="typing-text highlight"></span><span class="cursor">|</span></span>`;
    
    const typingText = heroTitle.querySelector('.typing-text');
    const cursor = heroTitle.querySelector('.cursor');
    
    // Start typing animation
    let i = 0;
    const typingInterval = setInterval(() => {
        if (i < nameText.length) {
            typingText.textContent += nameText.charAt(i);
            i++;
        } else {
            clearInterval(typingInterval);
            
            // Add blinking cursor animation
            setInterval(() => {
                cursor.style.opacity = cursor.style.opacity === '0' ? '1' : '0';
            }, 500);
        }
    }, 150);
};

// Initialize typing animation
window.addEventListener('load', createTypingAnimation);

// Add image hover effect for project cards
const projectImages = document.querySelectorAll('.project-image');
projectImages.forEach(image => {
    image.addEventListener('mouseenter', () => {
        image.classList.add('hover');
    });
    
    image.addEventListener('mouseleave', () => {
        image.classList.remove('hover');
    });
});

// Initialize AOS (Animate on Scroll) like animations
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                scrollObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    animateElements.forEach(element => {
        scrollObserver.observe(element);
    });
    
    // Add animation classes to elements
    document.querySelectorAll('.section-header').forEach(header => {
        header.classList.add('animate-on-scroll');
    });
    
    document.querySelectorAll('.about-content > div').forEach(div => {
        div.classList.add('animate-on-scroll');
    });
    
    document.querySelectorAll('.contact-content > div').forEach(div => {
        div.classList.add('animate-on-scroll');
    });
});
