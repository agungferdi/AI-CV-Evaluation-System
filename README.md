# CV Evaluation Backend

A sophisticated AI-powered backend service that evaluates candidate CVs and project reports using Google's Gemini API. This system implements a complete evaluation pipeline with prompt chaining, retrieval-augmented generation (RAG), and async processing.

## 🚀 Features

- **AI-Driven Evaluation Pipeline**: 4-step evaluation process using Gemini 2.0 Flash
- **Document Processing**: Support for PDF, DOCX, and TXT file formats
- **Retrieval-Augmented Generation (RAG)**: ChromaDB for context-aware evaluations
- **Async Processing**: Non-blocking evaluation with background tasks
- **Resilient Architecture**: Retry logic, error handling, and failure simulation
- **Comprehensive Scoring**: Standardized evaluation parameters for both CV and projects
- **RESTful API**: Clean API design with automatic documentation

## 📋 API Endpoints

### Core Endpoints

1. **POST /api/v1/upload** - Upload CV and project report files
2. **POST /api/v1/evaluate** - Create evaluation task (returns immediately with task ID)  
3. **GET /api/v1/result/{id}** - Retrieve evaluation results (supports polling for completion)

### Additional Endpoints

4. **GET /api/v1/tasks** - List all evaluation tasks
5. **DELETE /api/v1/task/{id}** - Delete task and associated files
6. **GET /** - API root information
7. **GET /health** - Health check endpoint

## 🏗️ Architecture & Design Choices

### Technology Stack

- **FastAPI**: High-performance async web framework with automatic OpenAPI docs
- **Google Gemini 2.0 Flash**: Latest LLM for advanced text processing and evaluation
- **ChromaDB**: Vector database for RAG implementation
- **SQLAlchemy**: Async ORM for database operations
- **Tenacity**: Retry library for resilient AI API calls
- **PyMuPDF & python-docx**: Document processing libraries

### Key Design Decisions

1. **Async-First Architecture**: All operations are async to handle concurrent evaluations
2. **Pipeline Pattern**: Modular 4-step evaluation pipeline for maintainability
3. **Background Processing**: Long-running AI evaluations don't block API responses
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

Create test files in the project directory:

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