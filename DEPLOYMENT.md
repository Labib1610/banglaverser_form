# 🚀 Deployment Guide for BanglaVerse Evaluation Form

This guide provides step-by-step instructions for deploying your Django evaluation form to various platforms.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Added at least 50 dialect data items per dialect (5 dialects = 250 items minimum)
- [ ] Added plausibility questions (at least 10 recommended)
- [ ] Tested the form locally
- [ ] Created a superuser account
- [ ] Set up proper SECRET_KEY for production
- [ ] Updated ALLOWED_HOSTS in settings

---

## 🌐 Deployment Options

### Option 1: GitHub + PythonAnywhere (Recommended for Beginners)

**Cost**: Free tier available

**Steps**:

1. **Push to GitHub**
   ```bash
   cd /path/to/banglaverser_form
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/banglaverse-form.git
   git push -u origin main
   ```

2. **Sign up for PythonAnywhere**
   - Go to https://www.pythonanywhere.com/
   - Create a free account

3. **Create a new Web App**
   - Click "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10

4. **Clone your repository**
   ```bash
   # In PythonAnywhere console
   cd ~
   git clone https://github.com/yourusername/banglaverse-form.git
   cd banglaverse-form
   ```

5. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure WSGI file**
   - Go to Web tab → WSGI configuration file
   - Replace contents with:
   ```python
   import sys
   import os
   
   path = '/home/yourusername/banglaverse-form'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'banglaverse_project.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

7. **Set up static files**
   - In Web tab, set Static files:
     - URL: `/static/`
     - Directory: `/home/yourusername/banglaverse-form/staticfiles/`

8. **Run migrations and collect static**
   ```bash
   cd ~/banglaverse-form
   source venv/bin/activate
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

9. **Reload web app**
   - Click "Reload" button in Web tab
   - Visit your site: `yourusername.pythonanywhere.com`

---

### Option 2: Heroku (Easy, Professional)

**Cost**: Free tier removed, paid plans start at $5/month

**Steps**:

1. **Install Heroku CLI**
   ```bash
   # On Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Prepare for Heroku**
   
   Create `Procfile`:
   ```bash
   echo "web: gunicorn banglaverse_project.wsgi" > Procfile
   ```
   
   Update `requirements.txt`:
   ```bash
   pip install gunicorn whitenoise
   pip freeze > requirements.txt
   ```
   
   Update `settings.py` - add at the top of MIDDLEWARE:
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
       # ... rest of middleware
   ]
   
   # At the bottom
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   heroku open
   ```

---

### Option 3: Railway (Modern, Easy)

**Cost**: $5/month with generous free trial

**Steps**:

1. **Sign up at Railway**
   - Go to https://railway.app/
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository

3. **Add Environment Variables**
   In Railway dashboard, add:
   ```
   DJANGO_SETTINGS_MODULE=banglaverse_project.settings
   SECRET_KEY=your-random-secret-key
   ALLOWED_HOSTS=your-app.railway.app
   ```

4. **Create `railway.json`**
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn banglaverse_project.wsgi",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

5. **Push and Deploy**
   ```bash
   git add .
   git commit -m "Add Railway config"
   git push
   ```

---

### Option 4: Render (Easy, Free Tier Available)

**Cost**: Free tier available

**Steps**:

1. **Sign up at Render**
   - Go to https://render.com/
   - Sign up

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo

3. **Configure**
   - Name: `banglaverse-form`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn banglaverse_project.wsgi:application`

4. **Add Environment Variables**
   ```
   PYTHON_VERSION=3.10.0
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=your-app.onrender.com
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

---

### Option 5: DigitalOcean App Platform

**Cost**: $5/month

**Steps**:

1. **Sign up for DigitalOcean**
   - Go to https://www.digitalocean.com/

2. **Create App**
   - Go to Apps → Create App
   - Connect GitHub repository

3. **Configure**
   - Detected: Python
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn banglaverse_project.wsgi`

4. **Add Database** (optional)
   - Add PostgreSQL database for production

5. **Environment Variables**
   Add in Settings:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app.ondigitalocean.app
   ```

---

## 🔒 Security Configuration for Production

Update `settings.py` for production:

```python
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

---

## 📊 Database Options

### SQLite (Default - Good for small to medium traffic)
Already configured. No changes needed.

### PostgreSQL (Recommended for production)

1. **Install**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update settings.py**
   ```python
   import dj_database_url
   
   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3',
           conn_max_age=600
       )
   }
   ```

3. **Set DATABASE_URL environment variable**
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

---

## 🔄 GitHub Actions for Auto-Deploy

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          git remote add heroku https://heroku:$HEROKU_API_KEY@git.heroku.com/your-app-name.git
          git push heroku main
```

---

## 📧 Email Configuration (Optional)

To send evaluation notifications via email:

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
```

---

## � Sharing with Evaluators (Email Pre-filling)

After deployment, you can share personalized evaluation links with pre-filled email addresses.

### Creating Personalized Links

**Format:**
```
https://your-deployed-domain.com/?email=evaluator@example.com
```

**Examples:**
```
# PythonAnywhere
https://yourusername.pythonanywhere.com/?email=john.doe@university.edu

# Heroku
https://your-app.herokuapp.com/?email=researcher@institute.org

# Custom domain
https://banglaverse-eval.com/?email=participant@email.com
```

### Bulk Link Generation

Create a Python script to generate links for multiple evaluators:

```python
# generate_links.py
evaluators = [
    {"name": "Dr. Alice", "email": "alice@university.edu"},
    {"name": "Dr. Bob", "email": "bob@research.org"},
    {"name": "Prof. Charlie", "email": "charlie@institute.edu"},
]

base_url = "https://yourusername.pythonanywhere.com"

print("Personalized Evaluation Links:\n")
for person in evaluators:
    link = f"{base_url}/?email={person['email']}"
    print(f"{person['name']}: {link}")
```

### Email Template for Invitations

```
Subject: BanglaVerse Dialect Evaluation - Your Personal Link

Dear [Evaluator Name],

You are invited to participate in the BanglaVerse dialect translation evaluation study.

Your personalized evaluation link:
[YOUR_DEPLOYED_URL]/?email=[EVALUATOR_EMAIL]

This link is unique to you and will pre-fill your email address. You can submit only ONE evaluation.

The evaluation takes approximately 15-20 minutes to complete.

Thank you for your contribution!

Best regards,
Research Team
```

### Important Notes

- **One Submission Per Email**: Each email address can only submit once
- **Email Validation**: The system checks for duplicate submissions
- **Read-Only Email**: Pre-filled emails are locked and cannot be changed
- **Security**: Email addresses are visible in URL (use HTTPS in production)

---

## 🔍 Monitoring and Analytics

### Option 1: Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

### Option 2: Google Analytics

Add to `base.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## 🧪 Testing Before Deployment

```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check --deploy

# Collect static files
python manage.py collectstatic

# Run with production settings
DEBUG=False python manage.py runserver
```

---

## 📱 Custom Domain Setup

### For PythonAnywhere
1. Upgrade to paid account
2. Go to Web tab → Add custom domain
3. Update DNS records

### For Heroku
```bash
heroku domains:add www.yourdomain.com
# Then update DNS with provided values
```

### For Other Platforms
Follow their specific custom domain guides.

---

## 🔄 Continuous Deployment

Once set up, deployment is as simple as:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Most platforms will auto-deploy on push to main branch.

---

## 📞 Support

If you encounter issues:

1. Check platform-specific logs
2. Verify environment variables
3. Ensure all migrations are run
4. Check ALLOWED_HOSTS setting
5. Verify static files are collected

---

## ✅ Post-Deployment Checklist

- [ ] Site is accessible via URL
- [ ] Admin panel works (`/admin/`)
- [ ] Can add data through admin
- [ ] Evaluation form loads correctly
- [ ] Dialect selection works
- [ ] Randomization works
- [ ] Email pre-filling works (test with `?email=test@example.com`)
- [ ] Duplicate email prevention works (try submitting twice)
- [ ] Form submission works
- [ ] Thank you page displays
- [ ] Data is saved to database
- [ ] Export page works (`/export/`)
- [ ] Download buttons generate JSON files
- [ ] SSL/HTTPS is enabled
- [ ] Custom domain configured (if applicable)

## 📊 After Data Collection

Once evaluators have submitted responses:

1. **Login as admin**: `https://your-domain.com/admin/`
2. **Go to export page**: `https://your-domain.com/export/`
3. **Download data**: Click download buttons for JSON exports
4. **Analyze data**: Use Python, pandas, or other tools for analysis

---

**Good luck with your deployment! 🚀**
