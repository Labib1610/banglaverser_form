# ✅ Getting Started Checklist

Use this checklist to get your BanglaVerse evaluation form up and running.

## 📋 Initial Setup

- [ ] Navigate to project directory: `cd banglaverser_form`
- [ ] Activate virtual environment (if using): `source venv/bin/activate`
- [ ] Verify Django is installed: `python -c "import django; print(django.get_version())"`
- [ ] Database is created (migrations already run) ✓
- [ ] Create superuser: `python manage.py createsuperuser`

## 📝 Add Your Data

### Dialect Data (Required: 50 per dialect)
- [ ] **Chittagonian** - Add 50 translation pairs
- [ ] **Sylheti** - Add 50 translation pairs
- [ ] **Noakhali** - Add 50 translation pairs
- [ ] **Barishal** - Add 50 translation pairs
- [ ] **Rangpur** - Add 50 translation pairs

**Total needed**: 250 dialect translation pairs

### Plausibility Data (Required: At least 10)
- [ ] Add at least 10 MCQ questions with:
  - Human-made question
  - Correct answer
  - 3 AI-generated wrong options

**How to add**:
1. Start server: `python manage.py runserver`
2. Go to: http://127.0.0.1:8000/admin/
3. Login with superuser credentials
4. Click "Dialect Data" → "Add Dialect Data"
5. Click "Plausibility Data" → "Add Plausibility Data"

## 🧪 Testing

- [ ] Start server: `python manage.py runserver` or `./start.sh`
- [ ] Open: http://127.0.0.1:8000/
- [ ] Select a dialect from dropdown
- [ ] Click "Start Evaluation"
- [ ] Verify 10 random items appear
- [ ] Fill out all ratings
- [ ] Submit form
- [ ] Verify thank you page appears
- [ ] Check admin panel for submitted evaluations

## 🌐 Deployment (Optional)

- [ ] Choose deployment platform (PythonAnywhere, Heroku, Railway, Render)
- [ ] Follow steps in DEPLOYMENT.md
- [ ] Set environment variables:
  - `SECRET_KEY`
  - `DEBUG=False`
  - `ALLOWED_HOSTS`
- [ ] Run migrations on production
- [ ] Create production superuser
- [ ] Upload your data
- [ ] Test deployed site

## 📤 Sharing with Evaluators

- [ ] Get deployment URL or set up local network access
- [ ] Test the URL yourself first
- [ ] Share link with evaluators
- [ ] Provide brief instructions:
  1. Open link
  2. Select dialect
  3. Rate translations
  4. Submit

## 📊 Data Collection & Export

- [ ] Monitor submissions in admin panel
- [ ] Export data when collection is complete:
  - Via admin panel, or
  - `python manage.py dumpdata evaluation > results.json`
- [ ] Analyze results using Python/pandas/Excel

## 🔒 Security (For Production)

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Regular backups

## 📚 Documentation Reference

- **Quick Setup**: QUICKSTART.md
- **Full Guide**: README.md
- **Deployment**: DEPLOYMENT.md
- **Project Details**: PROJECT_SUMMARY.md

## 🆘 Common Issues

**"Not enough data for dialect"**
→ Add at least 10 items for that dialect (50 recommended)

**Can't login to admin**
→ Create superuser: `python manage.py createsuperuser`

**Server won't start**
→ Check you're in correct directory with `manage.py`

**Database errors**
→ Run migrations: `python manage.py migrate`

---

## 🎯 Quick Start Commands

```bash
# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
# or
./start.sh  # Linux/Mac
start.bat   # Windows

# Check for issues
python manage.py check

# Django shell (for bulk data loading)
python manage.py shell < load_sample_data.py

# Export data
python manage.py dumpdata evaluation > data.json
```

---

**Ready to start?** ✨

1. Create superuser
2. Start server
3. Add data via admin
4. Test the form
5. Deploy or share locally
6. Collect evaluations!

**Good luck with your research! 🚀**
