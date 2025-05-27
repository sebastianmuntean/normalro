# 🌐 Shared Hosting Deployment Guide (No SSH Access)

## ✅ **Quick Summary**

Your **shared hosting deployment package** has been created in the `deploy_shared` folder. You don't need SSH/terminal access - just file uploads and control panel access!

## 🚀 **Deployment Steps**

### **1. Upload Files**
- Upload the **entire contents** of the `deploy_shared` folder to your web root directory
- Common web root folders: `public_html`, `www`, `htdocs`, or similar

### **2. Set Environment Variables**
In your hosting control panel, find:
- **"Environment Variables"** (cPanel)
- **"PHP/Python Configuration"** 
- **"App Settings"** or similar

Set these variables:
```
SECRET_KEY = your-secure-random-key-here-change-this-immediately
JWT_SECRET_KEY = your-jwt-secure-key-here-also-change-this
FLASK_ENV = production
```

### **3. Enable Python (if needed)**
Some hosts require:
- Enable **Python CGI execution**
- Set **Python version to 3.x**
- Enable **CGI/FastCGI** support

### **4. Initialize Admin User**
Visit: `https://your-domain.com/api/init-admin`

This will create:
- **Username:** `admin`
- **Password:** `admin123`
- **⚠️ IMPORTANT:** Change password immediately!

### **5. Test Your Site**
- **Frontend:** `https://your-domain.com`
- **API Test:** `https://your-domain.com/api/pages`
- **Admin Panel:** `https://your-domain.com/admin`

## 🔧 **Troubleshooting**

### **404 Errors on API Routes**
1. Check if `.htaccess` uploaded correctly
2. Ensure your host supports **URL rewriting** (mod_rewrite)
3. Update the PYTHONPATH in `.htaccess` if needed

### **Python Path Issues**
Edit `.htaccess` line:
```apache
SetEnv PYTHONPATH "/home/your-username/public_html/backend"
```
Change to your actual server path.

### **Database Not Created**
The app creates SQLite database automatically, but if issues occur:
1. Check file permissions on server
2. Ensure Python has write access to backend folder

### **CORS Issues**
The `.htaccess` includes CORS headers, but some hosts may need additional configuration.

## 📁 **File Structure on Server**
```
your-domain.com/
├── .htaccess                 # URL rewriting & environment
├── index.html               # React app entry point
├── static/                  # React build assets
├── backend/
│   ├── wsgi_shared.py       # Shared hosting Python entry
│   ├── app.py              # Flask application
│   ├── config.py           # Environment configuration
│   └── requirements.txt    # Python dependencies
└── manifest.json, etc.     # React app files
```

## 🔑 **Security Notes**
- **Change default passwords immediately!**
- **Use strong, unique SECRET_KEY and JWT_SECRET_KEY**
- **Don't use default 'admin123' password in production**

## 🆘 **Need Help?**
If you encounter issues:
1. Check your hosting provider's documentation for Python CGI setup
2. Contact support for help with environment variables
3. Verify your hosting plan supports Python applications

---

**Deployment package created with `deploy_shared_hosting.bat`** 