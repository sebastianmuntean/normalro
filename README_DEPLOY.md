# CMS Deployment Guide for Windows Hosting

## Prerequisites

1. **Python 3.8+** installed on the hosting server
2. **Node.js 16+** for building the React frontend
3. **IIS** with Python support (or Apache/Nginx)
4. **FastCGI** module for IIS

## Deployment Steps

### Option A: Automated Deployment (Recommended)

1. **Run the deployment script:**
   ```batch
   deploy.bat
   ```

2. **Upload the `deploy` folder** contents to your hosting provider's web root directory

### Option B: Manual Deployment

#### 1. Build the React Frontend
```batch
cd frontend
npm install
npm run build
```

#### 2. Prepare the Backend
```batch
cd backend
pip install -r requirements.txt
```

#### 3. Copy Files to Server
- Copy `frontend/build/*` to your web root
- Copy `backend/*` to `backend/` subdirectory on server
- Copy `web.config` to web root

## Server Configuration

### IIS Configuration

1. **Install Python CGI Handler:**
   - Install Python on the server
   - Install `wfastcgi` package: `pip install wfastcgi`
   - Configure FastCGI in IIS Manager

2. **Configure Application Settings:**
   - Set `FLASK_ENV=production`
   - Set `SECRET_KEY` to a secure random string
   - Set `JWT_SECRET_KEY` to a secure random string
   - Set `PYTHONPATH` to your backend directory

3. **URL Rewrite Module:**
   - Install IIS URL Rewrite Module
   - The provided `web.config` handles routing

### Environment Variables

Set these environment variables in your hosting control panel:

```
FLASK_ENV=production
SECRET_KEY=your-super-secure-secret-key-here
JWT_SECRET_KEY=your-super-secure-jwt-key-here
DATABASE_URL=sqlite:///cms.db
```

### Database Setup

1. **Initialize the database:**
   ```python
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

2. **Create admin user:**
   ```python
   python -c "
   from app import app, db, User
   app.app_context().push()
   admin = User(username='admin', email='admin@example.com', is_admin=True)
   admin.set_password('your-admin-password')
   db.session.add(admin)
   db.session.commit()
   print('Admin user created!')
   "
   ```

## File Structure on Server

```
wwwroot/
├── index.html              # React app entry point
├── static/                 # React app assets
├── web.config             # IIS configuration
├── backend/               # Flask backend
│   ├── app.py
│   ├── wsgi.py           # WSGI entry point
│   ├── config.py
│   ├── requirements.txt
│   └── cms.db            # SQLite database
└── instance/             # Instance folder for uploads
```

## Security Considerations

1. **Change default secrets:**
   - Update `SECRET_KEY` in production
   - Update `JWT_SECRET_KEY` in production

2. **Database security:**
   - Consider using PostgreSQL/MySQL for production
   - Regular database backups

3. **HTTPS:**
   - Configure SSL certificate
   - Force HTTPS redirects

## Hosting Provider Specific Notes

### Shared Hosting (cPanel/Plesk)
- Upload files via File Manager or FTP
- Use subdomain or subdirectory if needed
- Configure Python app in hosting control panel

### VPS/Dedicated Server
- Install IIS and configure FastCGI
- Set up proper file permissions
- Configure firewall rules

### Cloud Hosting (Azure/AWS)
- Use App Service for easy Python deployment
- Configure application settings in portal
- Set up database service if needed

## Troubleshooting

### Common Issues

1. **500 Internal Server Error:**
   - Check Python path in web.config
   - Verify all dependencies are installed
   - Check error logs

2. **Database Errors:**
   - Ensure database file has write permissions
   - Initialize database with `db.create_all()`

3. **Static Files Not Loading:**
   - Check static file paths in React build
   - Verify web.config MIME types

4. **API Routes Not Working:**
   - Verify URL rewrite rules in web.config
   - Check FastCGI configuration

### Log Files
- Check IIS logs: `C:\inetpub\logs\LogFiles\`
- Check Windows Event Viewer for Python errors
- Enable Flask debug logging in development

## Support

For hosting-specific configuration, consult your hosting provider's documentation for:
- Python application deployment
- FastCGI configuration
- Database setup
- SSL certificate installation

## Maintenance

### Regular Tasks
1. **Database Backups:** Schedule regular backups of your SQLite/database
2. **Updates:** Keep Python packages updated with `pip update`
3. **Monitoring:** Set up monitoring for uptime and performance
4. **Logs:** Regularly check and rotate log files 