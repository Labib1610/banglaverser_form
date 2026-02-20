# 📦 Project Summary - BanglaVerse Evaluation Form

## 🎯 What Was Created

A complete Django web application for evaluating AI-generated Bangla dialect translations and MCQ distractor plausibility.

---

## 📂 Complete File Structure

```
banglaverser_form/
│
├── banglaverse_project/              # Django Project Configuration
│   ├── __init__.py
│   ├── settings.py                   # Project settings (updated with 'evaluation' app)
│   ├── urls.py                       # Main URL routing (includes evaluation URLs)
│   ├── asgi.py
│   └── wsgi.py
│
├── evaluation/                       # Main Application
│   ├── __init__.py
│   ├── models.py                     # 4 Database Models
│   │   ├── DialectData              # Stores dialect translation pairs
│   │   ├── PlausibilityData         # Stores MCQ questions with options
│   │   ├── DialectEvaluation        # Stores user ratings for dialects
│   │   └── PlausibilityEvaluation   # Stores user ratings for MCQs
│   │
│   ├── views.py                      # 6 View Functions
│   │   ├── home()                   # Main evaluation form page
│   │   ├── get_dialect_data()       # API: Random 10 dialect items
│   │   ├── get_plausibility_data()  # API: Random plausibility items
│   │   ├── submit_evaluation()      # API: Save evaluation responses
│   │   ├── thank_you()              # Thank you page
│   │   └── export_data()            # Export instructions page
│   │
│   ├── admin.py                      # Admin Panel Configuration
│   │   ├── DialectDataAdmin
│   │   ├── PlausibilityDataAdmin
│   │   ├── DialectEvaluationAdmin
│   │   └── PlausibilityEvaluationAdmin
│   │
│   ├── urls.py                       # App-specific URLs
│   │
│   ├── templates/                    # HTML Templates
│   │   └── evaluation/
│   │       ├── base.html            # Base template with styles
│   │       ├── home.html            # Main evaluation form
│   │       ├── thank_you.html       # Success page
│   │       └── export.html          # Export instructions
│   │
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py          # Initial database schema
│   │
│   ├── apps.py
│   └── tests.py
│
├── db.sqlite3                        # SQLite Database (created after migrations)
│
├── manage.py                         # Django management script
│
├── README.md                         # Comprehensive documentation
├── QUICKSTART.md                     # Quick start guide
├── DEPLOYMENT.md                     # Deployment instructions
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── load_sample_data.py               # Sample data loading script
├── start.sh                          # Linux/Mac startup script
└── start.bat                         # Windows startup script
```

---

## 🏗️ Technical Architecture

### Database Schema (4 Models)

#### 1. DialectData
**Purpose**: Stores the dialect translation pairs  
**Fields**:
- `dialect_name` - Choice field (5 dialects)
- `original_standard_text` - Original Bangla text
- `ai_generated_dialect_text` - AI-generated dialectal version
- `created_at` - Timestamp

**Data Requirement**: 50 items per dialect × 5 dialects = 250 total items

#### 2. PlausibilityData
**Purpose**: Stores MCQ questions with correct and wrong options  
**Fields**:
- `question` - Human-made question
- `correct_answer` - Human-made correct answer
- `wrong_option_1/2/3` - AI-generated wrong options
- `created_at` - Timestamp

**Data Requirement**: At least 10 items (more recommended)

#### 3. DialectEvaluation
**Purpose**: Stores evaluator responses for dialect translations  
**Fields**:
- `dialect_data` - ForeignKey to DialectData
- `evaluator_name/email` - Optional evaluator info
- `accuracy_rating` - 1-5 scale
- `naturalness_rating` - 1-5 scale
- `comments` - Optional text
- `session_id` - Groups responses from same person
- `created_at` - Timestamp

#### 4. PlausibilityEvaluation
**Purpose**: Stores evaluator responses for MCQ options  
**Fields**:
- `plausibility_data` - ForeignKey to PlausibilityData
- `evaluator_name/email` - Optional evaluator info
- `option_1/2/3_plausibility` - 1-5 scale for each wrong option
- `comments` - Optional text
- `session_id` - Groups responses from same person
- `created_at` - Timestamp

---

## 🔄 User Flow & Features

### Complete User Journey

1. **Landing Page**
   - Modern gradient design
   - Evaluator info form (name, email - optional)
   - Dialect selection dropdown (5 choices)
   - "Start Evaluation" button (disabled until dialect selected)

2. **Data Fetching** (Asynchronous)
   - AJAX call to `/api/get-dialect-data/?dialect=<name>`
   - Backend randomly samples 10 from 50 items for selected dialect
   - AJAX call to `/api/get-plausibility-data/`
   - Backend randomly samples up to 10 plausibility items
   - Loading indicator shown during fetch

3. **Dialect Evaluation Section**
   - Displays 10 random dialect pairs
   - For each pair:
     - Original standard text (highlighted)
     - AI-generated dialect translation (highlighted)
     - Accuracy rating (1-5 radio buttons with custom styling)
     - Naturalness rating (1-5 radio buttons with custom styling)
     - Optional comments textarea
   - Visual progress bar updates as ratings are selected

4. **Plausibility Evaluation Section**
   - Displays random MCQ items
   - For each MCQ:
     - Question (highlighted)
     - Correct answer (green highlight)
     - 3 wrong options (red highlight)
     - Plausibility rating for each wrong option (1-5 scale)
     - Optional comments textarea
   - Visual progress bar updates as ratings are selected

5. **Validation & Submission**
   - JavaScript validates all required fields
   - Shows error alert if any ratings missing
   - Submits via POST to `/api/submit-evaluation/`
   - Data includes session ID for grouping
   - Disable button prevents double submission

6. **Thank You Page**
   - Success message
   - Option to submit another evaluation
   - Returns to fresh form if clicked

---

## 🎨 Frontend Features

### Design Elements
- **Gradient Background**: Purple/blue gradient for modern look
- **Card-based Layout**: White container with shadow
- **Custom Radio Buttons**: Styled as clickable boxes
- **Progress Bars**: Visual feedback on completion
- **Responsive Design**: Works on mobile, tablet, desktop
- **Color Coding**: 
  - Blue/purple for dialects
  - Green for correct answers
  - Red for wrong options

### JavaScript Functionality
- **Dynamic Rendering**: Forms generated from API data
- **Real-time Progress**: Updates as user selects ratings
- **Form Validation**: Checks all required fields
- **AJAX Requests**: No page reloads
- **Session Tracking**: UUID generation for grouping
- **Error Handling**: User-friendly error messages

---

## 🔧 Backend Features

### Views & APIs

#### 1. `home(request)`
**Type**: Template view  
**URL**: `/`  
**Purpose**: Renders main evaluation form  
**Returns**: HTML page with dialect choices

#### 2. `get_dialect_data(request)`
**Type**: JSON API  
**URL**: `/api/get-dialect-data/?dialect=<name>`  
**Method**: GET  
**Logic**: 
- Filters DialectData by selected dialect
- Randomly samples 10 items
- Returns JSON with id, original_text, ai_text
**Error Handling**: Returns 400 if not enough data

#### 3. `get_plausibility_data(request)`
**Type**: JSON API  
**URL**: `/api/get-plausibility-data/`  
**Method**: GET  
**Logic**:
- Fetches all PlausibilityData
- Randomly samples up to 10 items
- Returns JSON with all fields
**Error Handling**: Returns 400 if no data

#### 4. `submit_evaluation(request)`
**Type**: JSON API  
**URL**: `/api/submit-evaluation/`  
**Method**: POST  
**Logic**:
- Receives JSON with evaluator info and ratings
- Creates DialectEvaluation records for each dialect item
- Creates PlausibilityEvaluation records for each MCQ
- All records tagged with same session_id
**Returns**: Success message with session_id
**Error Handling**: Returns 400 with error message

#### 5. `thank_you(request)`
**Type**: Template view  
**URL**: `/thank-you/`  
**Purpose**: Shows success message

#### 6. `export_data(request)`
**Type**: Template view  
**URL**: `/export/`  
**Purpose**: Shows export instructions (admin only)

---

## 🛡️ Admin Panel Features

### DialectData Admin
- List view with dialect name, text previews, timestamp
- Filter by dialect and date
- Search by text content
- Custom preview methods (50 char limit)

### PlausibilityData Admin
- List view with question and answer previews
- Search functionality
- Custom preview methods

### DialectEvaluation Admin
- Shows all evaluation responses
- Filters by date and ratings
- Search by evaluator info
- Read-only created_at field

### PlausibilityEvaluation Admin
- Shows all MCQ evaluation responses
- Filters by date
- Search by evaluator info
- Displays all 3 option ratings

---

## 📊 Key Features Implemented

### ✅ Query 1 Requirements
- [x] 5 dialect types supported
- [x] 50 data pairs per dialect capacity
- [x] Conditional display (only selected dialect shown)
- [x] Random 10 selection from 50
- [x] Randomization happens on each request

### ✅ Query 2 Requirements
- [x] Human-made questions and correct answers
- [x] 3 AI-generated wrong options per question
- [x] Plausibility rating system (1-5 scale)
- [x] Random selection of questions
- [x] Combined in same form

### ✅ Additional Features
- [x] Session tracking with UUID
- [x] Optional evaluator information
- [x] Progress indicators
- [x] Comments for each evaluation
- [x] Admin panel for data management
- [x] Data export capability
- [x] Responsive design
- [x] Error handling
- [x] Success confirmation

---

## 📝 Documentation Created

1. **README.md** (Comprehensive)
   - Features overview
   - Installation guide
   - Data addition methods
   - How it works
   - Database schema
   - Export instructions
   - Deployment preview
   - Configuration options
   - Analytics guide
   - Troubleshooting
   - Command reference

2. **QUICKSTART.md** (Fast Setup)
   - 5-minute setup guide
   - Quick data addition
   - Testing steps
   - Common issues
   - Pro tips

3. **DEPLOYMENT.md** (Production)
   - 5 deployment platform guides
   - Security configuration
   - Database options
   - GitHub Actions setup
   - Email configuration
   - Monitoring setup
   - Custom domain setup
   - Post-deployment checklist

4. **load_sample_data.py** (Helper Script)
   - Sample data structure
   - Easy modification template
   - Ready to use examples

5. **start.sh / start.bat** (Quick Start Scripts)
   - Automated environment checks
   - Database setup
   - Server startup
   - User-friendly messages

---

## 🚀 How to Use

### For Researchers/Admins:

1. **Setup**:
   ```bash
   cd banglaverser_form
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install django
   python manage.py createsuperuser
   ```

2. **Add Data**:
   - Via admin panel: `http://127.0.0.1:8000/admin/`
   - Via shell: Edit `load_sample_data.py` and run
   - Minimum: 10 items per dialect, 10 plausibility questions

3. **Run**:
   ```bash
   ./start.sh  # or start.bat on Windows
   # OR
   python manage.py runserver
   ```

4. **Share**:
   - For local network: `python manage.py runserver 0.0.0.0:8000`
   - For internet: Follow DEPLOYMENT.md

5. **Export Data**:
   - Via admin panel → select items → export action
   - Via command: `python manage.py dumpdata evaluation > data.json`
   - Via Django shell: Custom Python scripts

### For Evaluators:

1. Open the shared link
2. Enter name/email (optional)
3. Select dialect
4. Click "Start Evaluation"
5. Rate all items (progress bars help)
6. Submit
7. See thank you page

---

## 🔮 Customization Options

### Add More Dialects
Edit `evaluation/models.py`:
```python
DIALECT_CHOICES = [
    ('new_dialect', 'New Dialect Name'),
    # ...
]
```
Run: `python manage.py makemigrations && python manage.py migrate`

### Change Rating Scale
Edit models.py to change from 1-5 to any range

### Modify UI
Edit templates in `evaluation/templates/evaluation/`

### Add More Fields
Add to models, run migrations, update templates

---

## 📈 Data Analysis

After collecting evaluations:

```python
from evaluation.models import DialectEvaluation
from django.db.models import Avg

# Average ratings per dialect
stats = DialectEvaluation.objects.values(
    'dialect_data__dialect_name'
).annotate(
    avg_accuracy=Avg('accuracy_rating'),
    avg_naturalness=Avg('naturalness_rating'),
    count=Count('id')
)

# Export to pandas
import pandas as pd
data = list(DialectEvaluation.objects.all().values())
df = pd.DataFrame(data)
df.to_csv('evaluations.csv', index=False)
```

---

## ✨ Best Practices Implemented

1. **Security**:
   - CSRF protection
   - SQL injection prevention (Django ORM)
   - XSS protection (template escaping)

2. **Code Quality**:
   - Separation of concerns (MVC pattern)
   - DRY principle
   - Clear naming conventions
   - Comprehensive comments

3. **User Experience**:
   - Loading indicators
   - Progress feedback
   - Error messages
   - Success confirmation
   - Responsive design

4. **Data Integrity**:
   - Foreign key relationships
   - Session tracking
   - Timestamps
   - Validation

---

## 🎓 Technologies Used

- **Backend**: Django 6.0.2
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (development), PostgreSQL-ready
- **Styling**: Custom CSS with gradients
- **AJAX**: Fetch API
- **Admin**: Django Admin (customized)

---

## 📄 License

See LICENSE file in repository.

---

## 🙏 Next Steps

1. Add your 250 dialect data items (50 per dialect)
2. Add your plausibility questions
3. Test thoroughly
4. Deploy to production
5. Share with evaluators
6. Collect responses
7. Analyze data
8. Publish research! 🎉

---

**Created**: February 2026  
**Status**: Production-ready  
**Version**: 1.0.0

