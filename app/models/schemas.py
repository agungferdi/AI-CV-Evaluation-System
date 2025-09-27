from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileUploadResponse(BaseModel):
    message: str
    files: Dict[str, str]
    file_paths: Dict[str, str]

class EvaluationRequest(BaseModel):
    cv_file_path: str
    project_report_path: str
    job_description: Optional[str] = Field(default="Backend Developer position")

class TaskResponse(BaseModel):
    id: str
    status: TaskStatus

class CVEvaluation(BaseModel):
    technical_skills_match: float = Field(ge=1, le=5)
    experience_level: float = Field(ge=1, le=5)
    relevant_achievements: float = Field(ge=1, le=5)
    cultural_fit: float = Field(ge=1, le=5)
    overall_score: float = Field(ge=1, le=5)

class ProjectEvaluation(BaseModel):
    correctness: float = Field(ge=1, le=5)
    code_quality: float = Field(ge=1, le=5)
    resilience: float = Field(ge=1, le=5)
    documentation: float = Field(ge=1, le=5)
    creativity: float = Field(ge=1, le=5)
    overall_score: float = Field(ge=1, le=5)

class EvaluationResult(BaseModel):
    cv_match_rate: float = Field(ge=0, le=1)
    cv_feedback: str
    project_score: float = Field(ge=1, le=10)
    project_feedback: str
    overall_summary: str
    cv_evaluation_details: Optional[CVEvaluation] = None
    project_evaluation_details: Optional[ProjectEvaluation] = None

class TaskResultResponse(BaseModel):
    id: str
    status: TaskStatus
    result: Optional[EvaluationResult] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ExtractedCVData(BaseModel):
    """Structured data extracted from CV"""
    skills: List[str]
    experiences: List[str]
    projects: List[str]
    education: List[str]
    years_of_experience: Optional[int] = None
    achievements: List[str]