from flask import Blueprint, jsonify, request, send_file
import random
from datetime import datetime, timedelta
import os

books_bp = Blueprint('books', __name__)

# Comprehensive digital books library
DIGITAL_LIBRARY = {
    "AI & Machine Learning": {
        "icon": "🤖",
        "books": [
            {
                "id": 1,
                "title": "Deep Learning for Emotional AI Systems",
                "authors": ["Dr. Sarah Chen", "Prof. Michael Rodriguez"],
                "publisher": "TechPress Academic",
                "publication_date": "2024-01-15",
                "isbn": "978-0-123456-78-9",
                "pages": 624,
                "language": "English",
                "format": ["PDF", "EPUB", "Interactive"],
                "file_size": "45 MB",
                "price": 89.99,
                "rating": 4.9,
                "reviews": 456,
                "downloads": 12340,
                "description": "Comprehensive guide to developing emotionally intelligent AI systems using advanced neural architectures",
                "cover_image": "https://example.com/book_covers/emotional_ai.jpg",
                "preview_pages": 25,
                "table_of_contents": [
                    "Chapter 1: Introduction to Emotional AI",
                    "Chapter 2: Neural Architecture Fundamentals",
                    "Chapter 3: LSTM Networks for Emotion Processing",
                    "Chapter 4: Transformer Models in Emotional AI",
                    "Chapter 5: Variational Autoencoders for Emotion",
                    "Chapter 6: Multi-Agent Emotional Systems",
                    "Chapter 7: Cognitive Architecture Integration",
                    "Chapter 8: Bayesian Networks for Uncertainty",
                    "Chapter 9: GANs for Emotion Generation",
                    "Chapter 10: Practical Implementation",
                    "Chapter 11: Case Studies and Applications",
                    "Chapter 12: Future Directions"
                ],
                "key_topics": [
                    "LSTM-Transformer-VAE Architecture",
                    "Emotional Intelligence Models",
                    "Multi-Agent Systems",
                    "Cognitive Architectures",
                    "Practical Implementation"
                ],
                "code_examples": True,
                "datasets_included": True,
                "interactive_simulations": True,
                "related_courses": [1],
                "difficulty_level": "Advanced",
                "prerequisites": ["Basic Machine Learning", "Python Programming", "Linear Algebra"],
                "target_audience": ["AI Researchers", "ML Engineers", "Graduate Students"],
                "sample_code": "https://github.com/example/emotional-ai-code",
                "errata": "https://example.com/errata/emotional_ai",
                "reviews_detailed": [
                    {
                        "reviewer": "Dr. John Smith",
                        "affiliation": "MIT AI Lab",
                        "rating": 5,
                        "comment": "Excellent comprehensive coverage of emotional AI. The practical examples are particularly valuable.",
                        "date": "2024-01-20"
                    },
                    {
                        "reviewer": "AI Engineer",
                        "rating": 5,
                        "comment": "Best book on emotional AI I've read. Clear explanations and great code examples.",
                        "date": "2024-01-18"
                    }
                ]
            },
            {
                "id": 2,
                "title": "Quantum Machine Learning: Algorithms and Applications",
                "authors": ["Prof. Alice Quantum", "Dr. Bob Entanglement"],
                "publisher": "Quantum Academic Press",
                "publication_date": "2024-02-01",
                "isbn": "978-0-987654-32-1",
                "pages": 512,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "38 MB",
                "price": 79.99,
                "rating": 4.8,
                "reviews": 234,
                "downloads": 8760,
                "description": "Explore the intersection of quantum computing and machine learning with practical algorithms and real-world applications",
                "cover_image": "https://example.com/book_covers/quantum_ml.jpg",
                "preview_pages": 30,
                "table_of_contents": [
                    "Chapter 1: Quantum Computing Fundamentals",
                    "Chapter 2: Quantum Gates and Circuits",
                    "Chapter 3: Quantum Algorithms Overview",
                    "Chapter 4: QAOA for Optimization",
                    "Chapter 5: Variational Quantum Eigensolver",
                    "Chapter 6: Quantum Support Vector Machines",
                    "Chapter 7: Quantum Neural Networks",
                    "Chapter 8: Quantum GANs",
                    "Chapter 9: Hybrid Classical-Quantum Systems",
                    "Chapter 10: Implementation on Real Hardware"
                ],
                "key_topics": [
                    "QAOA Algorithms",
                    "Variational Quantum Eigensolver",
                    "Quantum Support Vector Machines",
                    "Quantum Neural Networks",
                    "Hardware Implementation"
                ],
                "code_examples": True,
                "quantum_simulators": True,
                "related_courses": [2],
                "difficulty_level": "Advanced",
                "prerequisites": ["Quantum Mechanics", "Linear Algebra", "Machine Learning Basics"],
                "target_audience": ["Quantum Researchers", "ML Engineers", "Physics Students"]
            },
            {
                "id": 3,
                "title": "Multi-Agent Systems: Design and Implementation",
                "authors": ["Dr. Lisa Wang", "Prof. David Chen"],
                "publisher": "Distributed Systems Press",
                "publication_date": "2024-01-10",
                "isbn": "978-0-456789-12-3",
                "pages": 480,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "32 MB",
                "price": 69.99,
                "rating": 4.7,
                "reviews": 189,
                "downloads": 6540,
                "description": "Comprehensive guide to designing and implementing multi-agent systems for distributed AI applications",
                "cover_image": "https://example.com/book_covers/multi_agent.jpg",
                "preview_pages": 20,
                "key_topics": [
                    "Agent Communication Protocols",
                    "Distributed Coordination",
                    "Collective Intelligence",
                    "Swarm Intelligence",
                    "Real-world Applications"
                ],
                "related_courses": [3],
                "difficulty_level": "Intermediate"
            }
        ]
    },
    "Blockchain & Cryptocurrency": {
        "icon": "⛓️",
        "books": [
            {
                "id": 4,
                "title": "DeFi Protocol Development: From Theory to Practice",
                "authors": ["Alex Thompson", "Emma Davis"],
                "publisher": "Blockchain Academic",
                "publication_date": "2024-01-25",
                "isbn": "978-0-789123-45-6",
                "pages": 568,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "42 MB",
                "price": 94.99,
                "rating": 4.9,
                "reviews": 345,
                "downloads": 9870,
                "description": "Complete guide to developing decentralized finance protocols with Solidity and Web3 technologies",
                "cover_image": "https://example.com/book_covers/defi_dev.jpg",
                "preview_pages": 35,
                "table_of_contents": [
                    "Chapter 1: DeFi Fundamentals",
                    "Chapter 2: Smart Contract Development",
                    "Chapter 3: Solidity Advanced Patterns",
                    "Chapter 4: Automated Market Makers",
                    "Chapter 5: Lending and Borrowing Protocols",
                    "Chapter 6: Yield Farming Mechanisms",
                    "Chapter 7: Cross-Chain Protocols",
                    "Chapter 8: Security and Auditing",
                    "Chapter 9: Testing and Deployment",
                    "Chapter 10: Real-world Case Studies"
                ],
                "key_topics": [
                    "Smart Contract Development",
                    "Automated Market Makers",
                    "Lending Protocols",
                    "Yield Farming",
                    "Cross-Chain Integration"
                ],
                "code_examples": True,
                "smart_contract_templates": True,
                "related_courses": [4],
                "difficulty_level": "Advanced",
                "prerequisites": ["Solidity Basics", "Blockchain Fundamentals", "Web3 Development"],
                "target_audience": ["Blockchain Developers", "DeFi Engineers", "Smart Contract Auditors"]
            },
            {
                "id": 5,
                "title": "NFT Marketplace Architecture and Implementation",
                "authors": ["Emma Davis", "Michael Johnson"],
                "publisher": "Web3 Publishing",
                "publication_date": "2024-02-10",
                "isbn": "978-0-321654-98-7",
                "pages": 392,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "28 MB",
                "price": 59.99,
                "rating": 4.6,
                "reviews": 156,
                "downloads": 4320,
                "description": "Build comprehensive NFT marketplaces with minting, trading, and IPFS integration",
                "cover_image": "https://example.com/book_covers/nft_marketplace.jpg",
                "preview_pages": 25,
                "key_topics": [
                    "NFT Standards (ERC-721, ERC-1155)",
                    "IPFS Integration",
                    "Marketplace Smart Contracts",
                    "Frontend Development",
                    "Wallet Integration"
                ],
                "related_courses": [5],
                "difficulty_level": "Intermediate"
            }
        ]
    },
    "Robotics & IoT": {
        "icon": "🤖",
        "books": [
            {
                "id": 6,
                "title": "Text2Robot: Natural Language Robotics Control",
                "authors": ["Dr. James Park", "Prof. Sarah Kim"],
                "publisher": "Robotics Press",
                "publication_date": "2024-01-30",
                "isbn": "978-0-654321-87-0",
                "pages": 456,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "35 MB",
                "price": 74.99,
                "rating": 4.8,
                "reviews": 123,
                "downloads": 3450,
                "description": "Develop natural language interfaces for robotic control systems using advanced NLP and robotics integration",
                "cover_image": "https://example.com/book_covers/text2robot.jpg",
                "preview_pages": 20,
                "key_topics": [
                    "Natural Language Processing for Robotics",
                    "ROS Integration",
                    "Command Parsing and Execution",
                    "Computer Vision Integration",
                    "Real-world Applications"
                ],
                "related_courses": [6],
                "difficulty_level": "Advanced"
            },
            {
                "id": 7,
                "title": "IoT Fleet Management: Scalable Device Orchestration",
                "authors": ["Maria Gonzalez", "Dr. Robert Lee"],
                "publisher": "IoT Academic Press",
                "publication_date": "2024-02-05",
                "isbn": "978-0-147258-36-9",
                "pages": 384,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "29 MB",
                "price": 64.99,
                "rating": 4.7,
                "reviews": 98,
                "downloads": 2890,
                "description": "Comprehensive guide to managing large-scale IoT deployments with real-time monitoring and control",
                "cover_image": "https://example.com/book_covers/iot_fleet.jpg",
                "preview_pages": 18,
                "key_topics": [
                    "Device Management Protocols",
                    "MQTT and Communication",
                    "Cloud Integration",
                    "Real-time Monitoring",
                    "Security and Scalability"
                ],
                "related_courses": [7],
                "difficulty_level": "Intermediate"
            }
        ]
    },
    "Healthcare Technology": {
        "icon": "🏥",
        "books": [
            {
                "id": 8,
                "title": "AI in Medical Diagnosis: Computer Vision Applications",
                "authors": ["Dr. Robert Kim", "Dr. Jennifer Lee"],
                "publisher": "Medical AI Press",
                "publication_date": "2024-01-20",
                "isbn": "978-0-258147-69-3",
                "pages": 512,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "48 MB",
                "price": 89.99,
                "rating": 4.9,
                "reviews": 234,
                "downloads": 5670,
                "description": "Advanced AI techniques for medical image analysis and automated diagnosis systems",
                "cover_image": "https://example.com/book_covers/medical_ai.jpg",
                "preview_pages": 30,
                "key_topics": [
                    "Medical Image Processing",
                    "Deep Learning for Diagnosis",
                    "DICOM Integration",
                    "Regulatory Compliance",
                    "Clinical Validation"
                ],
                "related_courses": [8],
                "difficulty_level": "Advanced"
            }
        ]
    },
    "Business & Entrepreneurship": {
        "icon": "💼",
        "books": [
            {
                "id": 9,
                "title": "Digital Transformation: Technology Strategy for Modern Business",
                "authors": ["David Wilson", "Susan Brown"],
                "publisher": "Business Tech Press",
                "publication_date": "2024-01-12",
                "isbn": "978-0-369852-14-7",
                "pages": 368,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "25 MB",
                "price": 54.99,
                "rating": 4.6,
                "reviews": 167,
                "downloads": 4230,
                "description": "Strategic guide to implementing digital transformation initiatives in modern enterprises",
                "cover_image": "https://example.com/book_covers/digital_transform.jpg",
                "preview_pages": 22,
                "key_topics": [
                    "Digital Strategy Development",
                    "Technology Integration",
                    "Change Management",
                    "ROI Measurement",
                    "Case Studies"
                ],
                "related_courses": [10, 11],
                "difficulty_level": "Intermediate"
            }
        ]
    },
    "Cybersecurity": {
        "icon": "🔒",
        "books": [
            {
                "id": 10,
                "title": "Advanced Threat Detection: AI-Powered Cybersecurity",
                "authors": ["Mark Johnson", "Dr. Lisa Chen"],
                "publisher": "Security Academic Press",
                "publication_date": "2024-02-15",
                "isbn": "978-0-741852-96-3",
                "pages": 496,
                "language": "English",
                "format": ["PDF", "EPUB"],
                "file_size": "41 MB",
                "price": 84.99,
                "rating": 4.9,
                "reviews": 189,
                "downloads": 6780,
                "description": "Implement advanced threat detection systems using artificial intelligence and machine learning",
                "cover_image": "https://example.com/book_covers/threat_detection.jpg",
                "preview_pages": 28,
                "key_topics": [
                    "AI-Powered Threat Detection",
                    "Machine Learning for Security",
                    "Network Security Analytics",
                    "Incident Response Automation",
                    "Zero-Day Detection"
                ],
                "related_courses": [12],
                "difficulty_level": "Advanced"
            }
        ]
    }
}

# Research papers and technical documents
RESEARCH_PAPERS = [
    {
        "id": 101,
        "title": "Quantum-Enhanced Emotional AI: A Novel Approach to Affective Computing",
        "authors": ["Dr. Sarah Chen", "Prof. Michael Rodriguez", "Dr. Alice Quantum"],
        "journal": "Journal of Advanced AI Research",
        "publication_date": "2024-01-15",
        "doi": "10.1000/jair.2024.001",
        "pages": 24,
        "abstract": "This paper presents a novel approach to emotional AI using quantum-enhanced neural networks...",
        "keywords": ["Quantum Computing", "Emotional AI", "Neural Networks", "Affective Computing"],
        "citations": 45,
        "downloads": 1234,
        "file_size": "2.8 MB",
        "format": "PDF",
        "open_access": True,
        "related_books": [1, 2]
    },
    {
        "id": 102,
        "title": "Scalable Multi-Agent Systems for Distributed Blockchain Networks",
        "authors": ["Dr. Lisa Wang", "Alex Thompson"],
        "journal": "Distributed Systems Quarterly",
        "publication_date": "2024-01-20",
        "doi": "10.1000/dsq.2024.002",
        "pages": 18,
        "abstract": "We propose a scalable architecture for multi-agent systems operating on distributed blockchain networks...",
        "keywords": ["Multi-Agent Systems", "Blockchain", "Distributed Systems", "Scalability"],
        "citations": 23,
        "downloads": 876,
        "file_size": "1.9 MB",
        "format": "PDF",
        "open_access": True,
        "related_books": [3, 4]
    }
]

@books_bp.route('/overview', methods=['GET'])
def get_library_overview():
    total_books = sum(len(cat["books"]) for cat in DIGITAL_LIBRARY.values())
    total_downloads = sum(book["downloads"] for cat in DIGITAL_LIBRARY.values() for book in cat["books"])
    avg_rating = sum(book["rating"] for cat in DIGITAL_LIBRARY.values() for book in cat["books"]) / total_books
    
    return jsonify({
        "total_books": total_books,
        "total_downloads": total_downloads,
        "average_rating": round(avg_rating, 1),
        "categories": len(DIGITAL_LIBRARY),
        "research_papers": len(RESEARCH_PAPERS),
        "languages": ["English", "Spanish", "French", "German", "Chinese"],
        "formats": ["PDF", "EPUB", "Interactive"],
        "new_releases_this_month": 8,
        "bestsellers": 12
    })

@books_bp.route('/categories', methods=['GET'])
def get_book_categories():
    categories = []
    for name, data in DIGITAL_LIBRARY.items():
        categories.append({
            "name": name,
            "icon": data["icon"],
            "book_count": len(data["books"]),
            "total_downloads": sum(book["downloads"] for book in data["books"]),
            "avg_rating": round(sum(book["rating"] for book in data["books"]) / len(data["books"]), 1),
            "avg_price": round(sum(book["price"] for book in data["books"]) / len(data["books"]), 2)
        })
    return jsonify(categories)

@books_bp.route('/category/<category_name>', methods=['GET'])
def get_books_by_category(category_name):
    if category_name in DIGITAL_LIBRARY:
        return jsonify(DIGITAL_LIBRARY[category_name]["books"])
    return jsonify({"error": "Category not found"}), 404

@books_bp.route('/book/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    for category in DIGITAL_LIBRARY.values():
        for book in category["books"]:
            if book["id"] == book_id:
                # Add reading statistics and additional details
                book_details = book.copy()
                book_details.update({
                    "reading_time": f"{random.randint(8, 20)} hours",
                    "reading_level": "Graduate/Professional",
                    "similar_books": [
                        {"id": 2, "title": "Quantum Machine Learning", "rating": 4.8},
                        {"id": 3, "title": "Multi-Agent Systems", "rating": 4.7}
                    ],
                    "reader_statistics": {
                        "completion_rate": f"{random.randint(75, 95)}%",
                        "average_reading_time": f"{random.randint(10, 25)} days",
                        "bookmark_frequency": f"{random.randint(15, 40)} bookmarks/reader"
                    },
                    "citation_info": {
                        "apa_format": f"{book['authors'][0]} ({book['publication_date'][:4]}). {book['title']}. {book['publisher']}.",
                        "bibtex": f"@book{{{book['title'].replace(' ', '').lower()}{book['publication_date'][:4]},\n  title={{{book['title']}}},\n  author={{{' and '.join(book['authors'])}}},\n  year={{{book['publication_date'][:4]}}},\n  publisher={{{book['publisher']}}}\n}}"
                    },
                    "accessibility": {
                        "screen_reader_compatible": True,
                        "text_to_speech": True,
                        "adjustable_font_size": True,
                        "high_contrast_mode": True
                    }
                })
                return jsonify(book_details)
    return jsonify({"error": "Book not found"}), 404

@books_bp.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    author = request.args.get('author', '')
    min_rating = float(request.args.get('min_rating', 0))
    max_price = float(request.args.get('max_price', 999999))
    format_filter = request.args.get('format', '')
    sort_by = request.args.get('sort', 'relevance')
    
    results = []
    for cat_name, cat_data in DIGITAL_LIBRARY.items():
        if category and category != cat_name:
            continue
            
        for book in cat_data["books"]:
            # Filter by search criteria
            if (query in book["title"].lower() or 
                query in book["description"].lower() or
                any(query in topic.lower() for topic in book.get("key_topics", []))):
                
                if (author == '' or any(author.lower() in auth.lower() for auth in book["authors"])) and \
                   (book["rating"] >= min_rating) and \
                   (book["price"] <= max_price) and \
                   (format_filter == '' or format_filter in book["format"]):
                    
                    book_result = book.copy()
                    book_result["category"] = cat_name
                    results.append(book_result)
    
    # Sort results
    if sort_by == 'price_low':
        results.sort(key=lambda x: x["price"])
    elif sort_by == 'price_high':
        results.sort(key=lambda x: x["price"], reverse=True)
    elif sort_by == 'rating':
        results.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == 'newest':
        results.sort(key=lambda x: x["publication_date"], reverse=True)
    elif sort_by == 'popular':
        results.sort(key=lambda x: x["downloads"], reverse=True)
    
    return jsonify({
        "results": results,
        "total": len(results),
        "query": query,
        "filters": {
            "category": category,
            "author": author,
            "min_rating": min_rating,
            "max_price": max_price,
            "format": format_filter,
            "sort_by": sort_by
        }
    })

@books_bp.route('/bestsellers', methods=['GET'])
def get_bestsellers():
    # Get books with highest download counts
    bestsellers = []
    for cat_name, cat_data in DIGITAL_LIBRARY.items():
        for book in cat_data["books"]:
            book_bestseller = book.copy()
            book_bestseller["category"] = cat_name
            bestsellers.append(book_bestseller)
    
    # Sort by downloads
    bestsellers.sort(key=lambda x: x["downloads"], reverse=True)
    return jsonify(bestsellers[:10])  # Top 10 bestsellers

@books_bp.route('/new-releases', methods=['GET'])
def get_new_releases():
    # Get recently published books
    new_releases = []
    for cat_name, cat_data in DIGITAL_LIBRARY.items():
        for book in cat_data["books"]:
            book_release = book.copy()
            book_release["category"] = cat_name
            new_releases.append(book_release)
    
    # Sort by publication date
    new_releases.sort(key=lambda x: x["publication_date"], reverse=True)
    return jsonify(new_releases[:8])  # Latest 8 releases

@books_bp.route('/featured', methods=['GET'])
def get_featured_books():
    # Get high-rated books with good download counts
    featured = []
    for cat_name, cat_data in DIGITAL_LIBRARY.items():
        for book in cat_data["books"]:
            if book["rating"] >= 4.7 and book["downloads"] >= 5000:
                book_featured = book.copy()
                book_featured["category"] = cat_name
                featured.append(book_featured)
    
    # Sort by rating and downloads
    featured.sort(key=lambda x: (x["rating"], x["downloads"]), reverse=True)
    return jsonify(featured[:6])  # Top 6 featured books

@books_bp.route('/author/<author_name>', methods=['GET'])
def get_books_by_author(author_name):
    author_books = []
    author_info = None
    
    for cat_name, cat_data in DIGITAL_LIBRARY.items():
        for book in cat_data["books"]:
            if any(author_name.lower() in author.lower() for author in book["authors"]):
                book_info = book.copy()
                book_info["category"] = cat_name
                author_books.append(book_info)
    
    if author_books:
        # Create author profile
        author_info = {
            "name": author_name,
            "total_books": len(author_books),
            "total_downloads": sum(book["downloads"] for book in author_books),
            "avg_rating": round(sum(book["rating"] for book in author_books) / len(author_books), 1),
            "specializations": list(set(book["category"] for book in author_books)),
            "bio": f"Expert author specializing in {', '.join(set(book['category'] for book in author_books))}",
            "education": "PhD in Computer Science",
            "affiliations": ["University Research Lab", "Tech Industry"]
        }
        
        return jsonify({
            "author": author_info,
            "books": author_books
        })
    
    return jsonify({"error": "Author not found"}), 404

@books_bp.route('/research-papers', methods=['GET'])
def get_research_papers():
    return jsonify(RESEARCH_PAPERS)

@books_bp.route('/research-paper/<int:paper_id>', methods=['GET'])
def get_research_paper_details(paper_id):
    for paper in RESEARCH_PAPERS:
        if paper["id"] == paper_id:
            return jsonify(paper)
    return jsonify({"error": "Research paper not found"}), 404

@books_bp.route('/download/<int:book_id>', methods=['POST'])
def download_book(book_id):
    data = request.get_json()
    user_id = data.get('user_id')
    format_type = data.get('format', 'PDF')
    
    # Simulate download process
    download_info = {
        "download_id": random.randint(100000, 999999),
        "book_id": book_id,
        "user_id": user_id,
        "format": format_type,
        "download_date": datetime.now().isoformat(),
        "download_url": f"https://example.com/downloads/{book_id}_{format_type.lower()}.{format_type.lower()}",
        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
        "file_size": f"{random.randint(20, 50)} MB"
    }
    
    return jsonify({
        "success": True,
        "download": download_info,
        "message": f"Book download ready in {format_type} format!"
    })

@books_bp.route('/purchase', methods=['POST'])
def purchase_book():
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    payment_method = data.get('payment_method')
    
    # Simulate purchase process
    purchase = {
        "purchase_id": random.randint(100000, 999999),
        "book_id": book_id,
        "user_id": user_id,
        "payment_method": payment_method,
        "purchase_date": datetime.now().isoformat(),
        "status": "completed",
        "receipt_url": f"https://example.com/receipts/{random.randint(100000, 999999)}.pdf"
    }
    
    return jsonify({
        "success": True,
        "purchase": purchase,
        "message": "Book purchased successfully! Download links have been sent to your email."
    })

@books_bp.route('/reading-list/<int:user_id>', methods=['GET'])
def get_reading_list(user_id):
    # Simulate user's reading list
    reading_list = []
    all_books = []
    
    # Collect all books
    for cat_name, cat_data in DIGITAL_LIBRARY.items():
        for book in cat_data["books"]:
            book_item = book.copy()
            book_item["category"] = cat_name
            all_books.append(book_item)
    
    # Get random books for reading list
    reading_list = random.sample(all_books, min(5, len(all_books)))
    
    for book in reading_list:
        book["reading_progress"] = random.randint(0, 100)
        book["last_read"] = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        book["bookmarks"] = random.randint(0, 15)
        book["notes"] = random.randint(0, 25)
    
    return jsonify({
        "user_id": user_id,
        "reading_list": reading_list,
        "total_books": len(reading_list),
        "reading_streak": random.randint(5, 45),
        "total_reading_time": f"{random.randint(50, 200)} hours"
    })

@books_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_book_recommendations(user_id):
    # Simulate personalized book recommendations
    recommendations = []
    all_books = []
    
    # Collect all books
    for cat_name, cat_data in DIGITAL_LIBRARY.items():
        for book in cat_data["books"]:
            book_rec = book.copy()
            book_rec["category"] = cat_name
            all_books.append(book_rec)
    
    # Get random recommendations (in real app, this would be ML-based)
    recommendations = random.sample(all_books, min(6, len(all_books)))
    
    return jsonify({
        "user_id": user_id,
        "recommendations": recommendations,
        "reason": "Based on your reading history and interests"
    })

