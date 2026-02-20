#!/bin/bash

# BanglaVerse Evaluation Form - Startup Script

echo "🇧🇩 Starting BanglaVerse Evaluation Form..."
echo ""

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found!"
    echo "Please run this script from the banglaverser_form directory."
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment not activated!"
    echo "Consider activating it with: source venv/bin/activate"
    echo ""
fi

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django not found!"
    echo "Installing Django..."
    pip install django
fi

# Check if migrations are needed
if [ ! -f "db.sqlite3" ]; then
    echo "📊 Database not found. Running migrations..."
    python manage.py migrate
    echo ""
    echo "👤 Creating superuser account..."
    python manage.py createsuperuser
fi

echo ""
echo "✅ Starting development server..."
echo ""
echo "📍 Access the application at:"
echo "   - Main form: http://127.0.0.1:8000/"
echo "   - Admin panel: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
