#!/bin/bash

echo "Setting up ShareHW development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create uploads directory if it doesn't exist
if [ ! -d "uploads" ]; then
    echo "Creating uploads directory..."
    mkdir uploads
fi

# Initialize database
echo "Setting up database..."
if command -v mysql &> /dev/null; then
    echo "MySQL is installed"
    # Check if database exists
    if mysql -u root -e "use sharehw_db" 2>/dev/null; then
        echo "Database already exists"
    else
        echo "Creating database..."
        mysql -u root < scripts/init_db.sql
    fi
else
    echo "MySQL is not installed. Please install MySQL and run the database setup script manually."
fi

# Initialize Flask database
echo "Initializing Flask database..."
export FLASK_APP=app
flask init-db

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
