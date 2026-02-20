# 🇧🇩 BanglaVerse Evaluation Form

A Django-based web application for evaluating AI-generated Bangla dialect translations and MCQ distractor plausibility.

## 📋 Features

### Query 1: Dialect Translation Evaluation
- **5 Supported Dialects**: Chittagonian, Sylheti, Noakhali, Barishal, Rangpur
- **Randomized Selection**: Displays 10 random pairs from 50 available per dialect
- **Rating System**: Evaluators rate translations on:
  - Accuracy (1-5 scale)
  - Naturalness (1-5 scale)
- **Conditional Display**: Only shows data for the selected dialect

### Query 2: MCQ Distractor Plausibility
- **Human-made Questions**: Original questions and correct answers
- **AI-generated Distractors**: 3 wrong options per question
- **Plausibility Rating**: 1-5 scale for each wrong option
- **Randomized Selection**: Random 10 items displayed

### Additional Features
- **Session Tracking**: Each evaluation session gets a unique ID
- **Email Required**: Email is required for submission and ensures unique responses
- **One Submission Per Email**: Prevents duplicate submissions from the same evaluator
- **URL Email Pre-filling**: Share personalized links with pre-filled emails
- **Progress Indicators**: Visual progress bars for completion
- **Responsive Design**: Modern, mobile-friendly UI
- **One-Click Export**: Download data as JSON with admin download buttons
- **Command Line Export**: Export data via Django management commands

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for version control)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd banglaverser_form
   ```

2. **Create and activate virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run migrations** (already done, but if needed)
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main form: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

---

## 📊 Adding Data

### Method 1: Django Admin Panel (Recommended)

1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Add data:
   - **Dialect Data**: Click "Dialect Data" → "Add Dialect Data"
     - Select dialect name
     - Enter original standard text
     - Enter AI-generated dialect text
     - Save and add more (you need 50 per dialect)
   
   - **Plausibility Data**: Click "Plausibility Data" → "Add Plausibility Data"
     - Enter question
     - Enter correct answer
     - Enter 3 wrong options
     - Save and add more

### Method 2: Django Shell (Bulk Import)

```python
python manage.py shell

from evaluation.models import DialectData, PlausibilityData

# Example: Adding dialect data
DialectData.objects.create(
    dialect_name='chittagonian',
    original_standard_text='আমি ভাত খাই',
    ai_generated_dialect_text='আঁই ভাত খাঁই'
)

# Example: Adding plausibility data
PlausibilityData.objects.create(
    question='বাংলাদেশের রাজধানী কোথায়?',
    correct_answer='ঢাকা',
    wrong_option_1='চট্টগ্রাম',
    wrong_option_2='সিলেট',
    wrong_option_3='রাজশাহী'
)
```

### Method 3: CSV/JSON Import (Advanced)

You can create a management command to bulk import from CSV/JSON files.

---

## 🎯 How It Works

### User Flow

1. **Evaluator Information**: User enters optional name/email and selects a dialect
2. **Data Fetching**: System fetches:
   - 10 random dialect pairs for the selected dialect
   - Random plausibility questions (up to 10)
3. **Evaluation**: User rates each item
4. **Submission**: All responses saved to database with session ID
5. **Thank You Page**: Confirmation and option to submit another evaluation

### Technical Flow

```
User Selects Dialect
    ↓
AJAX Call to /api/get-dialect-data/?dialect=<name>
    ↓
Backend: Random Sample of 10 from 50
    ↓
AJAX Call to /api/get-plausibility-data/
    ↓
Backend: Random Sample of ≤10
    ↓
JavaScript Renders Forms Dynamically
    ↓
User Completes Evaluation
    ↓
POST to /api/submit-evaluation/
    ↓
Save to Database → Redirect to Thank You
```

---

## 📁 Project Structure

```
banglaverser_form/
├── banglaverse_project/          # Django project settings
│   ├── settings.py               # Configuration
│   ├── urls.py                   # Main URL routing
│   └── wsgi.py                   # WSGI configuration
├── evaluation/                   # Main app
│   ├── models.py                 # Database models
│   ├── views.py                  # View logic
│   ├── urls.py                   # App URL routing
│   ├── admin.py                  # Admin configuration
│   ├── templates/                # HTML templates
│   │   └── evaluation/
│   │       ├── base.html         # Base template with styles
│   │       ├── home.html         # Main evaluation form
│   │       ├── thank_you.html    # Thank you page
│   │       └── export.html       # Export instructions
│   └── migrations/               # Database migrations
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management script
└── README.md                     # This file
```

---

## 🗄️ Database Schema

### DialectData
- `id`: Primary key
- `dialect_name`: Choice field (5 dialects)
- `original_standard_text`: TextField
- `ai_generated_dialect_text`: TextField
- `created_at`: DateTime

### PlausibilityData
- `id`: Primary key
- `question`: TextField
- `correct_answer`: TextField
- `wrong_option_1`: TextField
- `wrong_option_2`: TextField
- `wrong_option_3`: TextField
- `created_at`: DateTime

### DialectEvaluation
- `id`: Primary key
- `dialect_data`: ForeignKey to DialectData
- `evaluator_name`: CharField (optional)
- `evaluator_email`: EmailField (optional)
- `accuracy_rating`: IntegerField (1-5)
- `naturalness_rating`: IntegerField (1-5)
- `comments`: TextField (optional)
- `session_id`: CharField
- `created_at`: DateTime

### PlausibilityEvaluation
- `id`: Primary key
- `plausibility_data`: ForeignKey to PlausibilityData
- `evaluator_name`: CharField (optional)
- `evaluator_email`: EmailField (optional)
- `option_1_plausibility`: IntegerField (1-5)
- `option_2_plausibility`: IntegerField (1-5)
- `option_3_plausibility`: IntegerField (1-5)
- `comments`: TextField (optional)
- `session_id`: CharField
- `created_at`: DateTime

---

## 📤 Exporting Data

### Method 1: One-Click Download (Easiest)
1. Login as admin at http://127.0.0.1:8000/admin/
2. Go to http://127.0.0.1:8000/export/
3. Click the download button for the data you want:
   - **Download All Data**: Everything in one JSON file
   - **Download Dialect Data**: All dialect translation pairs
   - **Download Plausibility Data**: All MCQ questions
   - **Download Dialect Evaluations**: All user ratings for dialects
   - **Download Plausibility Evaluations**: All user ratings for MCQs

### Method 2: Django Management Command

```bash
# Export all evaluation data
python manage.py dumpdata evaluation --indent 2 > evaluation_data.json

# Export specific data
python manage.py dumpdata evaluation.DialectEvaluation --indent 2 > dialect_results.json
python manage.py dumpdata evaluation.PlausibilityEvaluation --indent 2 > plausibility_results.json
```

### Method 3: Custom Python Script

```python
import csv
from evaluation.models import DialectEvaluation

# Export dialect evaluations to CSV
with open('dialect_evaluations.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Dialect', 'Original Text', 'AI Text', 'Accuracy', 'Naturalness', 'Comments', 'Evaluator', 'Date'])
    
    for eval in DialectEvaluation.objects.select_related('dialect_data').all():
        writer.writerow([
            eval.id,
            eval.dialect_data.get_dialect_name_display(),
            eval.dialect_data.original_standard_text,
            eval.dialect_data.ai_generated_dialect_text,
            eval.accuracy_rating,
            eval.naturalness_rating,
            eval.comments,
            eval.evaluator_name or 'Anonymous',
            eval.created_at
        ])
```

---

## 👥 Sharing with Evaluators

### Email Pre-filling Feature

You can share personalized links with evaluators that automatically pre-fill their email address:

**URL Format:**
```
http://your-domain.com/?email=evaluator@example.com
```

**Benefits:**
- Email field is auto-filled and locked (read-only)
- Prevents typos in email addresses
- Ensures unique identification
- Each email can only submit once

**Example:**
```bash
# For local testing
http://127.0.0.1:8000/?email=john@example.com

# For production
https://your-app.pythonanywhere.com/?email=researcher@university.edu
```

**Creating Multiple Links:**
If you have a list of evaluators, you can create personalized links:
```python
evaluators = [
    "alice@example.com",
    "bob@example.com",
    "charlie@example.com"
]

base_url = "https://your-app.pythonanywhere.com"
for email in evaluators:
    print(f"{base_url}/?email={email}")
```

**Important Notes:**
- Each email address can only submit ONE evaluation
- Attempting to submit again with the same email will show an error
- The email field becomes read-only when pre-filled from URL
- Evaluators can still manually enter email if they access the base URL

---

## 🌐 Deployment

### For GitHub Pages (Static Site)
This is a Django app and cannot be directly deployed to GitHub Pages. Use the options below instead.

### For Heroku

1. **Install Heroku CLI**

2. **Create `Procfile`**
   ```
   web: gunicorn banglaverse_project.wsgi
   ```

3. **Install gunicorn**
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

4. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### For PythonAnywhere

1. Upload your code
2. Create a new web app with Django
3. Configure WSGI file to point to your project
4. Run migrations
5. Collect static files

### For Railway/Render

Follow their Django deployment guides.

### Important: Production Settings

Before deploying, update `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable

# Add security settings
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

---

## 🔧 Configuration

### Environment Variables (for production)

Create a `.env` file:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### Custom Dialects

Edit `evaluation/models.py`:

```python
DIALECT_CHOICES = [
    ('your_dialect', 'Your Dialect Name'),
    # Add more...
]
```

Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📈 Analytics & Monitoring

You can add simple analytics by:

1. Viewing evaluation stats in Django admin
2. Using Django's built-in query tools:

```python
from evaluation.models import DialectEvaluation

# Average ratings per dialect
from django.db.models import Avg

stats = DialectEvaluation.objects.values('dialect_data__dialect_name').annotate(
    avg_accuracy=Avg('accuracy_rating'),
    avg_naturalness=Avg('naturalness_rating')
)
```

---

## 🐛 Troubleshooting

### Issue: "No such table: evaluation_dialectdata"
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: "CSRF verification failed"
**Solution**: Ensure you're using the correct domain and cookies are enabled

### Issue: "Not enough data for dialect"
**Solution**: Add at least 10 items for each dialect through admin panel

### Issue: Static files not loading
**Solution**: Run collectstatic
```bash
python manage.py collectstatic
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

See LICENSE file for details.

---

## 👥 Contact

For questions or support, please contact the research team.

---

## 🎓 Citation

If you use this tool in your research, please cite:

```
BanglaVerse Evaluation Form
[Your Institution/Team Name]
2026
```

---

## ⚡ Quick Commands Reference

```bash
# Start development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Django shell
python manage.py shell

# Export data
python manage.py dumpdata evaluation --indent 2 > data.json
```

---

**Happy Evaluating! 🎉**
