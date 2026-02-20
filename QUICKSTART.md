# 🚀 Quick Start Guide

Get the BanglaVerse Evaluation Form running in 5 minutes!

## ⚡ Super Quick Start

```bash
# 1. Navigate to project directory
cd /path/to/banglaverser_form

# 2. Create and activate virtual environment (if not already done)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Django (if not already installed)
pip install django

# 4. Migrations are already done, but if you need to run them:
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser
# Enter username, email (optional), and password

# 6. Start the server
python manage.py runserver

# 7. Open your browser and go to:
# - Main form: http://127.0.0.1:8000/
# - Admin panel: http://127.0.0.1:8000/admin/
```

## 📝 Adding Your Data

### Option 1: Using Django Admin (Easiest)

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click "Dialect Data" → "Add Dialect Data"
4. Fill in:
   - **Dialect name**: Choose from dropdown (Chittagonian, Sylheti, etc.)
   - **Original standard text**: The standard Bangla text
   - **AI generated dialect text**: The AI-translated dialectal version
5. Click "Save and add another" to add more (you need 50 per dialect)
6. Repeat for "Plausibility Data"

### Option 2: Using Sample Data Script

1. Edit `load_sample_data.py` with your actual data
2. Run:
   ```bash
   python manage.py shell < load_sample_data.py
   ```

### Option 3: Using Django Shell

```bash
python manage.py shell
```

```python
from evaluation.models import DialectData, PlausibilityData

# Add dialect data
DialectData.objects.create(
    dialect_name='chittagonian',
    original_standard_text='আমি ভাত খাই',
    ai_generated_dialect_text='আঁই ভাত খাঁই'
)

# Add plausibility data
PlausibilityData.objects.create(
    question='বাংলাদেশের রাজধানী কোথায়?',
    correct_answer='ঢাকা',
    wrong_option_1='চট্টগ্রাম',
    wrong_option_2='সিলেট',
    wrong_option_3='রাজশাহী'
)

# Exit shell
exit()
```

## ✅ Testing the Form

1. Make sure you have added data (at least 10 dialect items per dialect and some plausibility items)
2. Go to http://127.0.0.1:8000/
3. Select a dialect from the dropdown
4. Click "Start Evaluation"
5. You should see 10 random dialect pairs and plausibility questions
6. Fill out the ratings
7. Submit the form
8. Check the admin panel to see your submitted evaluations

## 📊 Viewing Submitted Evaluations

1. Go to http://127.0.0.1:8000/admin/
2. Click on "Dialect Evaluations" or "Plausibility Evaluations"
3. You'll see all submitted responses with:
   - Evaluator name/email
   - Ratings
   - Comments
   - Timestamp
   - Session ID (for grouping responses)

## 🔄 Resetting the Database

If you want to start fresh:

```bash
# Delete the database
rm db.sqlite3

# Delete migrations (optional)
rm evaluation/migrations/0001_initial.py

# Recreate everything
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 🐛 Common Issues

### "No such table" error
**Solution**: Run migrations
```bash
python manage.py migrate
```

### "Not enough data for dialect" error
**Solution**: Add at least 10 items for that dialect through admin panel

### Server won't start
**Solution**: Make sure you're in the correct directory where `manage.py` exists

### Can't login to admin
**Solution**: Create a superuser
```bash
python manage.py createsuperuser
```

## 📱 Sharing the Form

### For Local Network Sharing

```bash
# Find your IP address
# On Linux/Mac: ifconfig or ip addr
# On Windows: ipconfig

# Run server on all interfaces
python manage.py runserver 0.0.0.0:8000

# Update settings.py
ALLOWED_HOSTS = ['*']  # Or specify your IP address

# Share this URL with others on your network:
# http://YOUR_IP:8000/
```

### For Internet Sharing

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment options to:
- PythonAnywhere (Free)
- Heroku
- Railway
- Render
- DigitalOcean

## 🎯 Next Steps

1. **Add your data**: At least 50 items per dialect (250 total for 5 dialects)
2. **Test thoroughly**: Try all dialects and check randomization
3. **Customize** (optional):
   - Edit templates in `evaluation/templates/evaluation/`
   - Modify styles in `base.html`
   - Add more dialects in `models.py`
4. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) to make it publicly accessible
5. **Share**: Send the link to your evaluators

## 💡 Pro Tips

- Each evaluation session gets a unique ID, so you can track which responses came from the same person
- The form shows progress bars to help evaluators see how far they've come
- You can export data as CSV from the admin panel
- Add more than 50 items per dialect for even better randomization
- Regular backups: `python manage.py dumpdata > backup.json`

## 🆘 Need Help?

- Check the full [README.md](README.md) for detailed information
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guides
- Review Django documentation: https://docs.djangoproject.com/

---

**You're ready to start evaluating! 🎉**
