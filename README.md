# AI Resume Analyzer

An intelligent resume analysis application that uses AI to evaluate and provide feedback on resumes. This project combines a Python FastAPI backend with a modern React frontend to deliver a seamless user experience.

## Features

- 📄 **Resume Upload & Parsing** - Upload resumes in multiple formats and extract key information
- 🤖 **AI-Powered Analysis** - Intelligent analysis using machine learning models
- 📊 **Detailed Feedback** - Get comprehensive feedback on resume structure and content
- 💾 **Database Storage** - Store and manage analyzed resumes
- 🎨 **Modern UI** - Clean, responsive frontend built with React and Vite
- ⚡ **Fast API Backend** - High-performance Python backend with FastAPI

## Project Structure

```
AI-Resume-Analyzer/
├── backend/
│   ├── ai_analyzer.py       # AI analysis logic
│   ├── analyzer.py          # Main analyzer module
│   ├── database.py          # Database operations
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Data models
│   ├── parser.py            # Resume parser
│   └── uploads/             # Uploaded resume files
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── main.jsx         # Application entry point
│   │   ├── index.css        # Global styles
│   │   └── assets/          # Static assets
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.js       # Vite configuration
│   └── index.html           # HTML template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Prerequisites

- **Python 3.8+** - For backend
- **Node.js 16+** - For frontend
- **npm or yarn** - Package manager for frontend
- **Conda (optional)** - For Python environment management

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a Python virtual environment (or use conda):
```bash
# Using conda
conda create -n resume-analyzer python=3.10
conda activate resume-analyzer

# Or using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with necessary environment variables:
```bash
# backend/.env
API_KEY=your_api_key_here
DATABASE_URL=your_database_url
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend

```bash
cd backend
conda activate resume-analyzer  # If using conda
python main.py
```

The API will be available at `http://localhost:8000`

### Start the Frontend

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

## Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **Python** - Core language

### Frontend
- **React** - UI library
- **Vite** - Build tool and dev server
- **CSS** - Styling

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Last Updated:** June 2, 2026
