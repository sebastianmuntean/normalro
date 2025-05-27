from faker import Faker
import random
from app import app, db, Page, User
from datetime import datetime, timedelta
import re

fake = Faker()

# Sample image URLs for articles
SAMPLE_IMAGES = [
    "https://picsum.photos/400/300?random=1",
    "https://picsum.photos/400/300?random=2", 
    "https://picsum.photos/400/300?random=3",
    "https://picsum.photos/400/300?random=4",
    "https://picsum.photos/400/300?random=5",
    "https://picsum.photos/400/300?random=6",
    "https://picsum.photos/400/300?random=7",
    "https://picsum.photos/400/300?random=8",
    "https://picsum.photos/400/300?random=9",
    "https://picsum.photos/400/300?random=10"
]

def create_slug(title):
    """Create a URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]  # Limit length

def generate_html_content():
    """Generate realistic HTML content for articles"""
    paragraphs = []
    
    # Add 3-6 paragraphs
    for _ in range(random.randint(3, 6)):
        paragraphs.append(f"<p>{fake.paragraph(nb_sentences=random.randint(3, 8))}</p>")
    
    # Sometimes add an image
    if random.choice([True, False]):
        img_url = random.choice(SAMPLE_IMAGES)
        img_html = f'<p><img src="{img_url}" alt="Article image" style="max-width: 100%; height: auto;"></p>'
        # Insert image randomly in content
        insert_pos = random.randint(1, len(paragraphs))
        paragraphs.insert(insert_pos, img_html)
    
    # Sometimes add a quote
    if random.choice([True, False]):
        quote = f'<blockquote><p><em>"{fake.sentence()}"</em></p></blockquote>'
        paragraphs.append(quote)
    
    # Sometimes add a list
    if random.choice([True, False]):
        list_items = [f"<li>{fake.sentence()}</li>" for _ in range(random.randint(2, 5))]
        list_html = f"<ul>{''.join(list_items)}</ul>"
        paragraphs.append(list_html)
    
    return ''.join(paragraphs)

def generate_articles():
    """Generate 100 random articles"""
    
    with app.app_context():
        # Get existing admin user or create one
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
        
        print(f"Generating articles with user: {admin_user.username}")
        
        # Generate 100 articles
        for i in range(100):
            title = fake.catch_phrase()
            
            # Make some titles more news-like
            if random.choice([True, False]):
                title = fake.sentence(nb_words=random.randint(4, 8)).replace('.', '')
            
            slug = create_slug(title)
            
            # Make slug unique by adding number if exists
            existing = Page.query.filter_by(slug=slug).first()
            if existing:
                slug = f"{slug}-{i+1}"
            
            content = generate_html_content()
            
            # Random status (mostly published)
            status = random.choices(['published', 'draft'], weights=[85, 15])[0]
            
            # Random date in the last 30 days
            created_date = fake.date_time_between(start_date='-30d', end_date='now')
            
            article = Page(
                title=title,
                content=content,
                slug=slug,
                status=status,
                user_id=admin_user.id,
                created_at=created_date,
                updated_at=created_date
            )
            
            db.session.add(article)
            
            if (i + 1) % 10 == 0:
                print(f"Generated {i + 1} articles...")
        
        db.session.commit()
        print(f"Successfully generated 100 articles!")
        
        # Print stats
        total_pages = Page.query.count()
        published_pages = Page.query.filter_by(status='published').count()
        draft_pages = Page.query.filter_by(status='draft').count()
        
        print(f"\nDatabase stats:")
        print(f"Total pages: {total_pages}")
        print(f"Published: {published_pages}")
        print(f"Drafts: {draft_pages}")

if __name__ == '__main__':
    generate_articles() 