from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
import uuid
import aiofiles
from typing import Dict, Any
import logging

from app.models.schemas import (
    FileUploadResponse, EvaluationRequest, TaskResponse, 
    TaskResultResponse, TaskStatus
)
from app.models.database import EvaluationTask
from app.services.database import get_db
from app.services.evaluation_pipeline import get_evaluation_pipeline
from app.utils.document_processor import DocumentProcessor

logger = logging.getLogger(__name__)
router = APIRouter()

# Configuration
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    """Save uploaded file to destination"""
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    async with aiofiles.open(destination, 'wb') as f:
        content = await upload_file.read()
        await f.write(content)
    
    return destination

@router.post("/upload", response_model=FileUploadResponse)
async def upload_files(
    cv_file: UploadFile = File(..., description="CV file (PDF, DOCX, or TXT)"),
    project_report: UploadFile = File(..., description="Project report file (PDF, DOCX, or TXT)")
):
    """
    Upload CV and project report files
    
    - **cv_file**: CV file in PDF, DOCX, or TXT format
    - **project_report**: Project report file in PDF, DOCX, or TXT format
    """
    try:
        # Validate file formats
        if not DocumentProcessor.validate_file_format(cv_file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid CV file format. Supported: PDF, DOCX, TXT"
            )
        
        if not DocumentProcessor.validate_file_format(project_report.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid project report file format. Supported: PDF, DOCX, TXT"
            )
        
        # Check file sizes
        cv_content = await cv_file.read()
        project_content = await project_report.read()
        
        if len(cv_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="CV file too large (max 10MB)")
        if len(project_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Project report file too large (max 10MB)")
        
        # Reset file positions
        await cv_file.seek(0)
        await project_report.seek(0)
        
        # Generate unique filenames
        session_id = str(uuid.uuid4())
        cv_filename = f"{session_id}_cv_{cv_file.filename}"
        project_filename = f"{session_id}_project_{project_report.filename}"
        
        # Save files
        cv_path = os.path.join(UPLOAD_DIR, cv_filename)
        project_path = os.path.join(UPLOAD_DIR, project_filename)
        
        cv_saved_path = await save_upload_file(cv_file, cv_path)
        project_saved_path = await save_upload_file(project_report, project_path)
        
        logger.info(f"Files uploaded successfully: CV={cv_saved_path}, Project={project_saved_path}")
        
        return FileUploadResponse(
            message="Files uploaded successfully",
            files={
                "cv_file": cv_file.filename,
                "project_report": project_report.filename
            },
            file_paths={
                "cv_file_path": cv_saved_path,
                "project_report_path": project_saved_path
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.post("/evaluate-direct", response_model=TaskResponse)
async def evaluate_files_direct(
    cv_file: UploadFile = File(..., description="CV file (PDF, DOCX, or TXT)"),
    project_report: UploadFile = File(..., description="Project report file (PDF, DOCX, or TXT)"),
    job_description: str = Form(default="Backend Developer position", description="Job description for evaluation"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload files AND start evaluation in one step - User Friendly!
    
    - **cv_file**: CV file in PDF, DOCX, or TXT format
    - **project_report**: Project report file in PDF, DOCX, or TXT format
    - **job_description**: Job description to evaluate against (optional)
    """
    try:
        # Validate file formats
        if not DocumentProcessor.validate_file_format(cv_file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid CV file format. Supported: PDF, DOCX, TXT"
            )
        
        if not DocumentProcessor.validate_file_format(project_report.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid project report file format. Supported: PDF, DOCX, TXT"
            )
        
        # Check file sizes
        cv_content = await cv_file.read()
        project_content = await project_report.read()
        
        if len(cv_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="CV file too large (max 10MB)")
        if len(project_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Project report file too large (max 10MB)")
        
        # Reset file positions
        await cv_file.seek(0)
        await project_report.seek(0)
        
        # Generate unique filenames
        session_id = str(uuid.uuid4())
        cv_filename = f"{session_id}_cv_{cv_file.filename}"
        project_filename = f"{session_id}_project_{project_report.filename}"
        
        # Save files
        cv_path = os.path.join(UPLOAD_DIR, cv_filename)
        project_path = os.path.join(UPLOAD_DIR, project_filename)
        
        cv_saved_path = await save_upload_file(cv_file, cv_path)
        project_saved_path = await save_upload_file(project_report, project_path)
        
        logger.info(f"Files uploaded successfully: CV={cv_saved_path}, Project={project_saved_path}")
        
        # Create evaluation task immediately
        task = EvaluationTask(
            cv_file_path=cv_saved_path,
            project_report_path=project_saved_path,
            job_description=job_description,
            status=TaskStatus.QUEUED
        )
        
        db.add(task)
        await db.commit()
        await db.refresh(task)
        
        # Start background evaluation immediately
        pipeline = await get_evaluation_pipeline()
        background_tasks.add_task(pipeline.run_evaluation, task.id)
        
        logger.info(f"Files uploaded and evaluation started: {task.id}")
        
        return TaskResponse(id=task.id, status=TaskStatus.QUEUED)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Direct evaluation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload and evaluate files: {str(e)}")

@router.post("/evaluate", response_model=TaskResponse)
async def create_evaluation_task(
    cv_file_path: str = Form(..., description="Path to the uploaded CV file"),
    project_report_path: str = Form(..., description="Path to the uploaded project report file"),
    job_description: str = Form(default="Backend Developer position", description="Job description for evaluation"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db)
):
    """
    \"\"\"\n    [ADVANCED] Create evaluation task from existing file paths\n    \n    Note: Use /evaluate-direct instead for easier file upload + evaluation in one step!\n    \n    - **cv_file_path**: Path to the uploaded CV file\n    - **project_report_path**: Path to the uploaded project report file  \n    - **job_description**: Job description to evaluate against (optional)\n    \"\"\"
    """
    try:
        # Validate file paths exist
        if not os.path.exists(cv_file_path):
            raise HTTPException(status_code=404, detail="CV file not found")
        if not os.path.exists(project_report_path):
            raise HTTPException(status_code=404, detail="Project report file not found")
        
        # Create evaluation task
        task = EvaluationTask(
            cv_file_path=cv_file_path,
            project_report_path=project_report_path,
            job_description=job_description,
            status=TaskStatus.QUEUED
        )
        
        db.add(task)
        await db.commit()
        await db.refresh(task)
        
        # Start background evaluation
        pipeline = await get_evaluation_pipeline()
        background_tasks.add_task(pipeline.run_evaluation, task.id)
        
        logger.info(f"Evaluation task created: {task.id}")
        
        return TaskResponse(id=task.id, status=TaskStatus.QUEUED)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Evaluation task creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create evaluation task: {str(e)}")

@router.get("/result/{task_id}", response_model=TaskResultResponse)
async def get_evaluation_result(
    task_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get evaluation result by task ID
    
    - **task_id**: The ID of the evaluation task
    """
    try:
        # Get task from database
        result = await db.execute(
            select(EvaluationTask).where(EvaluationTask.id == task_id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Build response based on task status
        response_data = {
            "id": task.id,
            "status": task.status,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
        
        if task.status == TaskStatus.COMPLETED and task.result:
            response_data["result"] = task.result
        elif task.status == TaskStatus.FAILED and task.error_message:
            response_data["error"] = task.error_message
        
        return TaskResultResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get result error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get evaluation result: {str(e)}")

@router.get("/tasks")
async def list_tasks(
    include_results: bool = False,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List all evaluation tasks with pagination and optional results"""
    try:
        result = await db.execute(
            select(EvaluationTask)
            .offset(offset)
            .limit(limit)
            .order_by(EvaluationTask.created_at.desc())
        )
        tasks = result.scalars().all()
        
        task_list = []
        for task in tasks:
            task_data = {
                "id": task.id,
                "status": task.status,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "cv_file": task.cv_file_path.split('/')[-1] if task.cv_file_path else None,
                "project_file": task.project_report_path.split('/')[-1] if task.project_report_path else None,
                "job_description": task.job_description
            }
            
            # Include results if requested and available
            if include_results and task.status == TaskStatus.COMPLETED and task.result:
                task_data["result"] = task.result
            elif include_results and task.status == TaskStatus.FAILED and task.error_message:
                task_data["error"] = task.error_message
                
            task_list.append(task_data)
        
        return {
            "tasks": task_list,
            "total": len(tasks)
        }
        
    except Exception as e:
        logger.error(f"List tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list tasks: {str(e)}")

@router.delete("/task/{task_id}")
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete an evaluation task and its associated files"""
    try:
        # Get task from database
        result = await db.execute(
            select(EvaluationTask).where(EvaluationTask.id == task_id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Delete associated files
        try:
            if os.path.exists(task.cv_file_path):
                os.remove(task.cv_file_path)
            if os.path.exists(task.project_report_path):
                os.remove(task.project_report_path)
        except Exception as e:
            logger.warning(f"Failed to delete files for task {task_id}: {e}")
        
        # Delete task from database
        await db.delete(task)
        await db.commit()
        
        return {"message": f"Task {task_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete task error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")