# 🎯 AI-Powered CV Evaluation System

> **A sophisticated backend service that evaluates candidate CVs and project reports using Google's Gemini API with intelligent scoring and professional PDF report generation.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Gemini AI](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Table of Contents
- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#️-system-architecture)
- [🚀 Getting Started](#-getting-started)
- [📱 Using the System](#-using-the-system)
- [📊 Understanding the Results](#-understanding-the-results)
- [🔧 API Reference](#-api-reference)
- [📄 PDF Report Generation](#-pdf-report-generation)
- [🎨 FastAPI Interactive Documentation](#-fastapi-interactive-documentation)
- [💡 Technical Implementation](#-technical-implementation)
- [🔬 Testing & Validation](#-testing--validation)

## 🎯 Overview

This project implements a **complete AI-driven recruitment evaluation system** that:

1. **Accepts candidate files** (CV + Project Report) in multiple formats (PDF, DOCX, TXT)
2. **Analyzes content** using Google Gemini 2.0 Flash AI with advanced prompt engineering
3. **Provides detailed scoring** across multiple evaluation criteria (1-5 scale)
4. **Generates professional PDF reports** with comprehensive feedback
5. **Delivers results in under 1 second** with lightning-fast AI processing

**Perfect for:** HR departments, recruitment agencies, technical hiring managers, and educational institutions conducting candidate assessments.

## ✨ Key Features

### 🤖 AI-Powered Intelligence
- **Google Gemini 2.0 Flash Integration**: Latest LLM for advanced text processing
- **4-Step Evaluation Pipeline**: Structured analysis with prompt chaining
- **Retrieval-Augmented Generation (RAG)**: Context-aware evaluations using vector database
- **Intelligent Scoring**: Standardized 1-5 scale evaluation across multiple criteria

### 📄 Document Processing
- **Multi-Format Support**: PDF, DOCX, and TXT file processing
- **Smart Text Extraction**: Handles various document layouts and formatting
- **File Validation**: Size limits, format checking, and error handling

### ⚡ Performance & Reliability
- **Lightning-Fast Processing**: Evaluations complete in under 1 second
- **Async Processing**: Non-blocking evaluation with background tasks
- **Real-time Status**: Instant progress tracking and completion notifications
- **Error Resilience**: Retry logic, failure simulation, and graceful degradation
- **Professional Reports**: Automated PDF generation with detailed analysis

### 🌐 User Experience
- **Interactive API Documentation**: Built-in Swagger UI for easy testing
- **One-Click Evaluation**: Upload files and start evaluation in single request
- **RESTful Design**: Clean, intuitive API endpoints
- **CORS Enabled**: Ready for frontend integration

## 🏗️ System Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  File Upload│───▶│   FastAPI    │───▶│  Background │
│   (Multi)   │    │   Server     │    │   Tasks     │
└─────────────┘    └──────────────┘    └─────────────┘
                           │                      │
                           ▼                      ▼
                   ┌──────────────┐    ┌─────────────┐
                   │   Database   │    │   Gemini    │
                   │  (SQLite)    │    │     AI      │
                   └──────────────┘    └─────────────┘
                           │                      │
                           ▼                      ▼
                   ┌──────────────┐    ┌─────────────┐
                   │    Vector    │    │     PDF     │
                   │   Database   │    │  Generator  │
                   │    (RAG)     │    │             │
                   └──────────────┘    └─────────────┘
```

### Core Components:
- **FastAPI Server**: High-performance async web framework
- **Gemini AI Service**: Google's latest LLM for intelligent evaluation
- **Vector Database**: RAG implementation for context-aware scoring
- **PDF Service**: Professional report generation with ReportLab
- **Document Processor**: Multi-format text extraction utilities

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))
- Git

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/agungferdi/AI-CV-Evaluation-System.git
cd AI-CV-Evaluation-System
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key:
GEMINI_API_KEY=your_actual_api_key_here
```

5. **Test Your Setup**
```bash
python test_setup.py
```
You should see all tests pass ✅

6. **Start the Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

🎉 **Your server is now running at:** http://localhost:8000

## 📱 Using the System

### Step 1: Access the Interactive Documentation

Navigate to **http://localhost:8000/docs** in your browser. You'll see the **FastAPI Interactive Documentation** (also called **Swagger UI**). This is an automatically generated web interface that lets you test all API endpoints directly from your browser - no coding required!

![FastAPI Interactive Documentation](images/input%20data%20evaluate%20direct.png)

**What is FastAPI Interactive Documentation?**
- **Swagger UI**: A web-based interface that automatically documents your API
- **Try it out**: Click any endpoint to test it directly in the browser
- **Real-time testing**: Upload files, send requests, and see responses instantly
- **No Postman needed**: Everything works directly in the web browser

### Step 2: Upload Files and Start Evaluation (One-Click Method)

**🎯 Recommended: Use the User-Friendly Endpoint**

1. Find **`POST /api/v1/evaluate-direct`** (marked as "**Evaluate Files Direct**")
2. Click **"Try it out"**
3. Upload your files:
   - **cv_file**: Your CV/resume (PDF, DOCX, or TXT)
   - **project_report**: Your project documentation (PDF, DOCX, or TXT)
   - **job_description**: The position you're applying for (optional)
4. Click **"Execute"**

![Evaluation Results](images/results%20evaluate%20direct.png)

**Response:** You'll immediately get a task ID:
```json
{
  "id": "a9d2b772-7b7c-4cd3-a9f0-ba4c7a0aef83",
  "status": "queued"
}
```

### Step 3: Check Your Results

1. Find **`GET /api/v1/result/{task_id}`**
2. Click **"Try it out"**
3. Paste your task ID from Step 2
4. Click **"Execute"**
5. **Results are available almost instantly!** (Processing typically takes less than 1 second)

![Get Results by ID](images/get%20result%20by%20id.png)

### Step 4: View All Your Evaluations

Use **`GET /api/v1/tasks`** to see all your evaluation history with results.

### Step 5: Generate PDF Report

1. Find **`GET /api/v1/export-pdf/{task_id}`**
2. Enter your completed task ID
3. Click **"Execute"**
4. **Download** your professional PDF evaluation report!

![PDF Export Route](images/try%20route%20convert%20to%20pdf.png)

### 📋 Sample PDF Report Pages

Here's what your generated PDF evaluation report looks like:

**Page 1: Executive Summary & CV Evaluation**
![PDF Report Page 1](images/result_1_pdf.png)

**Page 2: Project Evaluation Details**
![PDF Report Page 2](images/result_2_pdf.png)

**Page 3: Recommendations & Final Assessment**
![PDF Report Page 3](images/result_3_pdf.png)

## 📊 Understanding the Results

When your evaluation completes, you'll receive a comprehensive analysis:

```json
{
  "cv_structure": {
    "personal_info": { ... },
    "skills": ["Python", "FastAPI", "Machine Learning"],
    "experience": [ ... ],
    "education": [ ... ]
  },
  "cv_match": {
    "overall_score": 85,
    "match_rate": "High Match",
    "strengths": ["Strong technical skills", "Relevant experience"],
    "improvement_areas": ["Could highlight leadership experience"],
    "detailed_analysis": { ... }
  },
  "project_evaluation": {
    "technical_complexity": 8,
    "innovation_score": 7,
    "implementation_quality": 9,
    "relevance_to_position": 8
  },
  "recommendations": {
    "cv_suggestions": [ ... ],
    "project_improvements": [ ... ],
    "interview_preparation": [ ... ]
  }
}
```

**Score Interpretation:**
- **90-100**: Exceptional match
- **80-89**: High match  
- **70-79**: Good match
- **60-69**: Moderate match
- **Below 60**: Needs improvement

## 🏗️ Architecture & Design Choices

### Technology Stack

- **FastAPI**: High-performance async web framework with automatic OpenAPI docs
- **Google Gemini 2.0 Flash**: Latest LLM for advanced text processing and evaluation
- **SQLAlchemy**: Async ORM for database operations with SQLite
- **Tenacity**: Retry library for resilient AI API calls
- **ReportLab**: Professional PDF generation
- **PyMuPDF & python-docx**: Document processing libraries

### Key Design Decisions

1. **Async-First Architecture**: All operations are asynchronous for better performance
2. **Background Task Processing**: Ultra-fast evaluations don't block the API
3. **Multi-Format Support**: Handles PDF, DOCX, and TXT files seamlessly
4. **Retry Logic**: Resilient AI API calls with exponential backoff
5. **Interactive Documentation**: FastAPI auto-generates browsable API docs
6. **Professional Reports**: Clean PDF exports for sharing results

## 🔧 API Reference

### Core Endpoints

#### 1. **POST** `/api/v1/evaluate-direct` - One-Click Evaluation
**Purpose**: Upload files and start evaluation in one step (user-friendly)

**Parameters**:
- `cv_file`: Your CV/resume file (PDF/DOCX/TXT)
- `project_report`: Your project documentation (PDF/DOCX/TXT) 
- `job_description`: Target position (optional text)

**Response**:
```json
{
  "id": "task-uuid",
  "status": "queued",
  "message": "Evaluation started successfully"
}
```

#### 2. **GET** `/api/v1/result/{task_id}` - Check Results
**Purpose**: Retrieve evaluation results by task ID

**Response** (when completed):
```json
{
  "id": "task-uuid",
  "status": "completed",
  "result": {
    "cv_structure": { ... },
    "cv_match": { ... },
    "project_evaluation": { ... },
    "recommendations": { ... }
  }
}
```

#### 3. **GET** `/api/v1/export-pdf/{task_id}` - Download PDF Report
**Purpose**: Generate and download professional PDF evaluation report

**Response**: PDF file download

#### 4. **GET** `/api/v1/tasks` - View All Evaluations
**Purpose**: List all your evaluation history

### Advanced Endpoints

#### **POST** `/api/v1/upload` - File Upload Only
Upload files first, then evaluate separately (for advanced workflows)

#### **POST** `/api/v1/evaluate` - Evaluate Uploaded Files
Start evaluation for previously uploaded files

## 📄 PDF Report Features

Your generated PDF reports include:

- **Executive Summary**: Overall match score and key findings
- **CV Analysis**: Detailed breakdown of qualifications vs requirements
- **Project Evaluation**: Technical assessment and innovation metrics
- **Recommendations**: Specific improvement suggestions
- **Professional Formatting**: Clean, shareable design

## 🧪 Testing Your Setup

Run the included test script to verify everything works:

```bash
python test_setup.py
```

**What it tests:**
- ✅ Python environment
- ✅ Required packages
- ✅ Gemini API connection
- ✅ Database initialization
- ✅ File processing capabilities

## 🔍 Troubleshooting

### Common Issues

**1. "Gemini API key not found"**
```bash
# Make sure your .env file has:
GEMINI_API_KEY=your_actual_key_here
```

**2. "ModuleNotFoundError"**
```bash
# Reinstall dependencies:
pip install -r requirements.txt
```

**3. "Database locked" error**
```bash
# Delete the database file and restart:
rm evaluation.db
uvicorn main:app --reload
```

**4. "Port already in use"**
```bash
# Use a different port:
uvicorn main:app --reload --port 8080
```

**5. File upload fails**
- Check file size (max 10MB)
- Ensure supported format (PDF, DOCX, TXT)
- Try with sample files first

### Getting Help

1. Check the logs in your terminal
2. Test with the sample files (`sample_cv.txt`, `sample_project_report.txt`)
3. Verify your Gemini API key is working
4. Try the basic test script: `python test_setup.py`

## 🤝 Contributing

This project was built as part of a backend development assignment. Feel free to:

- Report bugs or suggest improvements
- Add new evaluation criteria
- Enhance the PDF report formatting
- Add support for more file formats

## 📜 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using FastAPI and Google Gemini AI**

*Ready to evaluate CVs like a pro? Start the server and visit http://localhost:8000/docs!*

### Key Design Decisions

1. **Async-First Architecture**: All operations are async to handle concurrent evaluations
2. **Pipeline Pattern**: Modular 4-step evaluation pipeline for maintainability
3. **Background Processing**: Lightning-fast AI evaluations with instant responses
4. **Vector RAG**: Context retrieval improves evaluation accuracy and consistency
5. **Structured Prompting**: JSON-based prompts ensure reliable, parseable responses
6. **Error Resilience**: Comprehensive retry logic with exponential backoff

### Evaluation Pipeline (4 Steps)

```
Step 1: CV Structure Extraction
├── Extract skills, experience, projects, education
└── Convert unstructured text to structured data

Step 2: Context Retrieval  
├── Query vector DB for relevant job requirements
└── Retrieve scoring rubrics for CV evaluation

Step 3: CV Evaluation & Scoring
├── Compare extracted data with job requirements
├── Generate match rate (0.0-1.0)
└── Provide detailed feedback with scores (1-5)

Step 4: Project Report Evaluation
├── Retrieve project scoring rubric from vector DB
├── Initial evaluation with Gemini
├── Refinement pass for consistency
└── Generate final scores and feedback
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd cv-evaluation-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
# Update .env file with your API key
echo "GEMINI_API_KEY=AIzaSyBMR02W3-zJGpSr7rU7Rh_KThcbDKYfXiQ" > .env
```

5. **Run the application**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. **Access the API**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📖 Usage Examples

### 1. Upload Files

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "cv_file=@sample_cv.pdf" \
  -F "project_report=@project_report.pdf"
```

**Response:**
```json
{
  "message": "Files uploaded successfully",
  "files": {
    "cv_file": "sample_cv.pdf",
    "project_report": "project_report.pdf"
  },
  "file_paths": {
    "cv_file_path": "uploads/uuid_cv_sample_cv.pdf",
    "project_report_path": "uploads/uuid_project_project_report.pdf"
  }
}
```

### 2. Start Evaluation

```bash
curl -X POST "http://localhost:8000/api/v1/evaluate" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "cv_file_path=uploads/uuid_cv_sample_cv.pdf&project_report_path=uploads/uuid_project_project_report.pdf&job_description=Senior Backend Developer position requiring Python, APIs, and cloud experience"
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "queued"
}
```

### 3. Check Results

```bash
curl -X GET "http://localhost:8000/api/v1/result/123e4567-e89b-12d3-a456-426614174000"
```

**Response (Processing):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:30Z"
}
```

**Response (Completed):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "result": {
    "cv_match_rate": 0.82,
    "cv_feedback": "Strong backend experience with Python and cloud platforms. Limited AI/ML integration experience but shows good architectural understanding.",
    "project_score": 7.5,
    "project_feedback": "Well-implemented solution with good error handling. Code quality is solid with clear documentation. Could benefit from more comprehensive testing.",
    "overall_summary": "Strong candidate with relevant backend experience. Project demonstrates solid engineering skills. Would be a good fit for the role with some AI/ML learning.",
    "cv_evaluation_details": {
      "technical_skills_match": 4,
      "experience_level": 4,
      "relevant_achievements": 3,
      "cultural_fit": 4,
      "overall_score": 4
    },
    "project_evaluation_details": {
      "correctness": 4,
      "code_quality": 4,
      "resilience": 3,
      "documentation": 4,
      "creativity": 3,
      "overall_score": 4
    }
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:32:15Z"
}
```

## 🧪 Testing the API

### Using FastAPI Interactive Docs

1. Navigate to http://localhost:8000/docs
2. Use the interactive interface to test all endpoints
3. Upload sample files and run evaluations

### Sample Test Files

**Option 1: Use Your Own Files (Recommended)**
- Upload your existing CV (PDF, DOCX, or TXT format)
- Upload any project report or portfolio document
- The system works with real documents and provides more meaningful results!

**Option 2: Create Sample Files**
If you don't have files ready, create these test files in the project directory:

**sample_cv.txt**
```
John Doe
Senior Software Engineer

EXPERIENCE:
- 5 years of backend development with Python and Django
- Built REST APIs serving 1M+ requests daily
- Experience with AWS, Docker, and PostgreSQL
- Led team of 4 developers on microservices migration

SKILLS:
- Python, Django, FastAPI
- PostgreSQL, Redis, MongoDB  
- AWS, Docker, Kubernetes
- REST APIs, GraphQL

PROJECTS:
- E-commerce platform handling $10M+ annual revenue
- Real-time analytics dashboard for 50K+ users
- Microservices architecture migration project

EDUCATION:
- BS Computer Science, University of Technology (2018)
```

**sample_project.txt**
```
CV Evaluation System Project Report

OVERVIEW:
Built an AI-powered CV evaluation system using FastAPI and OpenAI GPT-4.

IMPLEMENTATION:
- FastAPI backend with async processing
- OpenAI integration for text analysis
- PostgreSQL for data persistence
- Redis for caching and task queues
- Docker containerization

KEY FEATURES:
- File upload (PDF, DOCX support)
- Async evaluation pipeline
- RESTful API design
- Error handling and retries
- Comprehensive logging

CODE QUALITY:
- Modular architecture with service layer
- Unit tests with 85% coverage
- Type hints throughout codebase
- Comprehensive documentation

CHALLENGES & SOLUTIONS:
- API rate limiting: Implemented exponential backoff
- Large file processing: Added streaming upload
- Error resilience: Added retry mechanisms
```

💡 **Pro Tip**: The AI evaluation works best with real documents! Try uploading your actual CV and a project you've worked on for the most accurate and useful feedback.

## 🔧 Configuration

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (with defaults)
DATABASE_URL=sqlite+aiosqlite:///./evaluation.db
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes
VECTOR_DB_PATH=./chroma_db
```

### Customizing Evaluation Parameters

The system uses predefined scoring rubrics stored in ChromaDB. You can modify these by:

1. Accessing the vector database service
2. Adding custom job descriptions and scoring criteria
3. The system will automatically use relevant context for evaluations

## 🚦 Error Handling & Resilience

### Built-in Resilience Features

1. **Retry Logic**: Automatic retries with exponential backoff for AI API calls
2. **Failure Simulation**: 5% random failure rate for testing resilience
3. **Graceful Degradation**: Fallback responses when AI calls fail
4. **Input Validation**: Comprehensive file format and size validation
5. **Database Transactions**: Atomic operations with rollback on failure

### Common Error Scenarios

- **File Upload Errors**: Invalid format, size limits, corrupted files
- **AI API Failures**: Rate limiting, timeouts, service unavailable
- **Processing Errors**: Malformed text, extraction failures
- **Database Errors**: Connection issues, constraint violations

## 📊 Scoring System

### CV Evaluation Criteria (1-5 scale)

- **Technical Skills Match**: Alignment with job requirements
- **Experience Level**: Years and complexity of relevant experience  
- **Relevant Achievements**: Impact and scale of accomplishments
- **Cultural Fit**: Communication, learning attitude, teamwork

### Project Evaluation Criteria (1-5 scale)

- **Correctness**: Meeting requirements and functionality
- **Code Quality**: Clean, modular, testable code
- **Resilience**: Error handling, fault tolerance
- **Documentation**: Clear instructions and explanations
- **Creativity**: Additional features and innovations

### Overall Scoring

- **CV Match Rate**: 0.0-1.0 (percentage match with job requirements)
- **Project Score**: 1-10 (aggregated from detailed criteria)
- **Overall Summary**: Narrative evaluation with hiring recommendation

## 🔄 Development & Deployment

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if implemented)
pytest tests/
```

### Production Deployment

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♀️ Support

For questions, issues, or contributions:

1. Check the interactive API docs at `/docs`
2. Review this README for common use cases
3. Open an issue for bugs or feature requests
4. Check logs for debugging information

## 🔮 Future Enhancements

- [ ] Authentication and user management
- [ ] Batch processing for multiple CVs
- [ ] Custom evaluation templates
- [ ] Dashboard for evaluation analytics
- [ ] Integration with HR systems
- [ ] Multi-language support
- [ ] Advanced document parsing (images, tables)
- [ ] Real-time evaluation status via WebSockets