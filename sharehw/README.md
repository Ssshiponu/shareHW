# ShareHW - Student Collaboration Platform

ShareHW is a web application designed to facilitate homework and notes sharing among high school students, creating an intuitive, secure, and collaborative learning environment.

## Features

- User authentication and authorization
- Homework management
- Notes sharing with privacy controls
- File upload and download
- Content search and filtering
- Responsive design

## Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- Redis (optional, for caching)
- pip (Python package installer)

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/MohinUddin/sharehw.git
cd sharehw
```

2. Run the setup script:
```bash
./setup.sh
```

This script will:
- Create a virtual environment
- Install dependencies
- Set up the database
- Create necessary directories

3. Configure environment variables:
Copy the `.env.example` file to `.env` and update the values:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the development server:
```bash
./run.sh
```

The application will be available at `http://localhost:5000`

## Manual Setup (if setup.sh fails)

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
```bash
mysql -u root -p < scripts/init_db.sql
```

4. Initialize Flask database:
```bash
export FLASK_APP=app
flask init-db
```

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage report:
```bash
pytest --cov=app tests/
```

## Project Structure

```
sharehw/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   └── content.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── homework.py
│   │   ├── notes.py
│   │   └── admin.py
│   ├── templates/
│   ├── static/
│   └── utils/
│       ├── file_handler.py
│       ├── email_handler.py
│       └── cache.py
├── migrations/
├── tests/
├── uploads/
├── venv/
├── config.py
├── requirements.txt
├── setup.sh
├── run.sh
├── .env
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- **Mohin Uddin Shipon**
  - Student of Dhamrai Govt. College
  - Email: mohinuddinshipon10@example.com
  - GitHub: [MohinUddin](https://github.com/MohinUddin)
