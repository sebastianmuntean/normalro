from app import app, db, User, Category

def init_db():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
        categories = ['News', 'Technology', 'Business', 'Lifestyle']
        for cat_name in categories:
            if not Category.query.filter_by(name=cat_name).first():
                db.session.add(Category(name=cat_name, description=f'Articles about {cat_name.lower()}'))
        db.session.commit()
        print('Database initialized!')

if __name__ == '__main__':
    init_db() 