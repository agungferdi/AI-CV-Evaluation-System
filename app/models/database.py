from sqlalchemy import Column, String, DateTime, Text, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class EvaluationTask(Base):
    __tablename__ = "evaluation_tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="queued")
    cv_file_path = Column(String, nullable=False)
    project_report_path = Column(String, nullable=False)
    job_description = Column(Text)
    result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "cv_file_path": self.cv_file_path,
            "project_report_path": self.project_report_path,
            "job_description": self.job_description,
            "result": self.result,
            "error_message": self.error_message,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }