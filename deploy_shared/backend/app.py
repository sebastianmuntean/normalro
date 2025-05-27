from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    return app

# Create app instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    pages = db.relationship('Page', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.String(20), default='published')  # 'published' or 'draft'
    parent_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)
    parent = db.relationship('Page', remote_side=[id], backref='children')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user or not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    user = User(
        username=data['username'],
        email=data['email'],
        is_admin=data.get('is_admin', False)
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return jsonify({'token': access_token, 'user': {'id': user.id, 'username': user.username, 'email': user.email, 'is_admin': user.is_admin}})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    print('JWT identity:', user_id)
    user = User.query.get(int(user_id))
    print('User from DB:', user)
    if not user:
        print('User not found for id:', user_id)
        return jsonify({'message': 'User not found'}), 404
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    }
    print('Returning user data:', user_data)
    return jsonify(user_data)

@app.route('/api/auth/me', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    })

@app.route('/api/pages', methods=['GET'])
def get_pages():
    # Query parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'created_at_desc')
    status = request.args.get('status', 'published')
    
    # Base query - only published pages by default
    query = Page.query.filter_by(status=status)
    
    # Search functionality
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Page.title.ilike(search_term),
                Page.content.ilike(search_term),
                Page.slug.ilike(search_term)
            )
        )
    
    # Sorting
    if sort == 'created_at_desc':
        query = query.order_by(Page.created_at.desc())
    elif sort == 'created_at_asc':
        query = query.order_by(Page.created_at.asc())
    elif sort == 'title_asc':
        query = query.order_by(Page.title.asc())
    elif sort == 'title_desc':
        query = query.order_by(Page.title.desc())
    elif sort == 'author_asc':
        query = query.join(User).order_by(User.username.asc())
    elif sort == 'author_desc':
        query = query.join(User).order_by(User.username.desc())
    else:
        query = query.order_by(Page.created_at.desc())
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    pages = query.offset((page - 1) * limit).limit(limit).all()
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit
    
    return jsonify({
        'pages': [{
            'id': page.id,
            'title': page.title,
            'content': page.content,
            'slug': page.slug,
            'status': page.status,
            'parent_id': page.parent_id,
            'created_at': page.created_at.isoformat(),
            'updated_at': page.updated_at.isoformat(),
            'author': page.author.username
        } for page in pages],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'totalPages': total_pages,
            'hasNext': page < total_pages,
            'hasPrev': page > 1
        }
    })

@app.route('/api/pages/<slug>', methods=['GET'])
def get_page_by_slug(slug):
    page = Page.query.filter_by(slug=slug, status='published').first()
    if not page:
        return jsonify({'message': 'Page not found'}), 404
    return jsonify({
        'id': page.id,
        'title': page.title,
        'content': page.content,
        'slug': page.slug,
        'status': page.status,
        'parent_id': page.parent_id,
        'created_at': page.created_at.isoformat(),
        'updated_at': page.updated_at.isoformat(),
        'author': page.author.username
    })

@app.route('/api/pages', methods=['POST'])
@jwt_required()
def create_page():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user or not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    if Page.query.filter_by(slug=data['slug']).first():
        return jsonify({'message': 'Slug already exists'}), 400
    page = Page(
        title=data['title'],
        content=data['content'],
        slug=data['slug'],
        status=data.get('status', 'published'),
        parent_id=data.get('parent_id'),
        user_id=user.id
    )
    db.session.add(page)
    db.session.commit()
    return jsonify({'id': page.id}), 201

@app.route('/api/pages/<int:page_id>', methods=['PUT'])
@jwt_required()
def edit_page(page_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user or not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    page = Page.query.get(page_id)
    if not page:
        return jsonify({'message': 'Page not found'}), 404
    data = request.get_json()
    if 'title' in data:
        page.title = data['title']
    if 'content' in data:
        page.content = data['content']
    if 'slug' in data and data['slug'] != page.slug:
        if Page.query.filter_by(slug=data['slug']).first():
            return jsonify({'message': 'Slug already exists'}), 400
        page.slug = data['slug']
    if 'status' in data:
        page.status = data['status']
    if 'parent_id' in data:
        page.parent_id = data['parent_id']
    db.session.commit()
    return jsonify({'id': page.id})

@app.route('/api/pages/<int:page_id>', methods=['DELETE'])
@jwt_required()
def delete_page(page_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user or not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    page = Page.query.get(page_id)
    if not page:
        return jsonify({'message': 'Page not found'}), 404
    db.session.delete(page)
    db.session.commit()
    return '', 204

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email, 'is_admin': u.is_admin}
        for u in users
    ])

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return '', 204

@app.route('/api/admin/pages', methods=['GET'])
@admin_required
def list_pages():
    # Query parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'created_at_desc')
    status = request.args.get('status', 'all')
    
    # Base query - all pages for admin
    query = Page.query
    
    # Status filter
    if status != 'all':
        query = query.filter_by(status=status)
    
    # Search functionality
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Page.title.ilike(search_term),
                Page.content.ilike(search_term),
                Page.slug.ilike(search_term)
            )
        )
    
    # Sorting
    if sort == 'created_at_desc':
        query = query.order_by(Page.created_at.desc())
    elif sort == 'created_at_asc':
        query = query.order_by(Page.created_at.asc())
    elif sort == 'title_asc':
        query = query.order_by(Page.title.asc())
    elif sort == 'title_desc':
        query = query.order_by(Page.title.desc())
    elif sort == 'author_asc':
        query = query.join(User).order_by(User.username.asc())
    elif sort == 'author_desc':
        query = query.join(User).order_by(User.username.desc())
    else:
        query = query.order_by(Page.created_at.desc())
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    pages = query.offset((page - 1) * limit).limit(limit).all()
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit
    
    return jsonify({
        'pages': [{
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'content': p.content,
            'author': p.author.username,
            'status': p.status,
            'published': p.status == 'published'
        } for p in pages],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'totalPages': total_pages,
            'hasNext': page < total_pages,
            'hasPrev': page > 1
        }
    })

@app.route('/api/admin/pages/<int:page_id>', methods=['DELETE'])
@admin_required
def delete_page_admin(page_id):
    page = Page.query.get(page_id)
    if not page:
        return jsonify({'message': 'Page not found'}), 404
    db.session.delete(page)
    db.session.commit()
    return '', 204

@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@admin_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'is_admin': user.is_admin})

@app.route('/api/admin/pages', methods=['POST'])
@admin_required
def create_page_admin():
    data = request.get_json()
    page = Page(
        title=data['title'],
        content=data['content'],
        slug=data['slug'],
        status=data.get('status', 'published'),
        user_id=data['user_id']
    )
    db.session.add(page)
    db.session.commit()
    return jsonify({'id': page.id}), 201

@app.route('/api/admin/pages/<int:page_id>', methods=['PUT'])
@admin_required
def edit_page_admin(page_id):
    page = Page.query.get(page_id)
    if not page:
        return jsonify({'message': 'Page not found'}), 404
    data = request.get_json()
    page.title = data.get('title', page.title)
    page.content = data.get('content', page.content)
    page.slug = data.get('slug', page.slug)
    page.status = data.get('status', page.status)
    db.session.commit()
    return jsonify({'id': page.id})

@app.route('/api/init-admin', methods=['GET', 'POST'])
def init_admin():
    """Initialize admin user for shared hosting deployment"""
    try:
        # Check if any admin already exists
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            return jsonify({
                'status': 'success',
                'message': f'Admin user already exists: {existing_admin.username}',
                'admin_exists': True
            })
        
        # Create default admin user
        admin = User(
            username='admin',
            email='admin@normal.ro',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Admin user created successfully!',
            'username': 'admin',
            'password': 'admin123',
            'warning': 'IMPORTANT: Please change the password immediately after login!',
            'login_url': '/admin'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to create admin user: {str(e)}'
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000) 