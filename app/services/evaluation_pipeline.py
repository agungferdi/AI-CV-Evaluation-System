import asyncio
import logging
from typing import Dict, Any
from app.services.gemini_service import GeminiService
from app.services.vector_db import get_vector_db
from app.utils.document_processor import DocumentProcessor
from app.models.schemas import EvaluationResult, TaskStatus
from app.models.database import EvaluationTask
from app.services.database import async_session_maker
from sqlalchemy import select, update
import random

logger = logging.getLogger(__name__)

class EvaluationPipeline:
    """Main evaluation pipeline orchestrating the 4-step AI evaluation process"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
        self.document_processor = DocumentProcessor()
    
    async def run_evaluation(self, task_id: str) -> None:
        """Run the complete evaluation pipeline"""
        async with async_session_maker() as session:
            try:
                # Update task status to processing
                await session.execute(
                    update(EvaluationTask)
                    .where(EvaluationTask.id == task_id)
                    .values(status=TaskStatus.PROCESSING)
                )
                await session.commit()
                
                # Get task details
                result = await session.execute(
                    select(EvaluationTask).where(EvaluationTask.id == task_id)
                )
                task = result.scalar_one_or_none()
                
                if not task:
                    raise ValueError(f"Task {task_id} not found")
                
                # Simulate some processing time and potential failures
                await self._simulate_processing_delay()
                
                # Run the 4-step evaluation pipeline
                evaluation_result = await self._execute_pipeline(task)
                
                # Update task with results
                await session.execute(
                    update(EvaluationTask)
                    .where(EvaluationTask.id == task_id)
                    .values(
                        status=TaskStatus.COMPLETED,
                        result=evaluation_result.dict()
                    )
                )
                await session.commit()
                
                logger.info(f"Evaluation completed successfully for task {task_id}")
                
            except Exception as e:
                logger.error(f"Evaluation failed for task {task_id}: {str(e)}")
                # Update task with error
                await session.execute(
                    update(EvaluationTask)
                    .where(EvaluationTask.id == task_id)
                    .values(
                        status=TaskStatus.FAILED,
                        error_message=str(e)
                    )
                )
                await session.commit()
                raise
    
    async def _execute_pipeline(self, task: EvaluationTask) -> EvaluationResult:
        """Execute the 4-step evaluation pipeline"""
        
        # Extract text from uploaded files
        cv_text = await self.document_processor.extract_text_from_file(task.cv_file_path)
        project_text = await self.document_processor.extract_text_from_file(task.project_report_path)
        
        # Get vector database service
        vector_db = await get_vector_db()
        
        # Step 1: Extract structured info from CV
        logger.info("Step 1: Extracting structured information from CV")
        cv_data = await self.gemini_service.extract_cv_structure(cv_text)
        
        # Step 2: Retrieve relevant job context for CV evaluation
        logger.info("Step 2: Retrieving job context for CV evaluation")
        job_context = await vector_db.retrieve_context(
            query=f"backend developer requirements {' '.join(cv_data.skills[:5])}",
            context_type="job_description",
            n_results=2
        )
        
        cv_context = await vector_db.retrieve_context(
            query="CV evaluation scoring technical skills experience",
            context_type="scoring_rubric",
            n_results=1
        )
        
        combined_cv_context = "\n\n".join([doc["content"] for doc in job_context + cv_context])
        
        # Step 3: Evaluate CV match and generate feedback
        logger.info("Step 3: Evaluating CV match with job requirements")
        cv_match_rate, cv_feedback, cv_evaluation = await self.gemini_service.evaluate_cv_match(
            cv_data, task.job_description or "Backend Developer Position", combined_cv_context
        )
        
        # Step 4: Retrieve project evaluation context and evaluate project
        logger.info("Step 4: Evaluating project report")
        project_context = await vector_db.retrieve_context(
            query="project evaluation rubric code quality correctness resilience documentation",
            context_type="scoring_rubric",
            n_results=2
        )
        
        project_rubric = "\n\n".join([doc["content"] for doc in project_context])
        
        project_score, project_feedback, project_evaluation = await self.gemini_service.evaluate_project_report(
            project_text, project_rubric
        )
        
        # Generate overall summary
        logger.info("Generating overall evaluation summary")
        overall_summary = await self.gemini_service.generate_overall_summary(
            cv_feedback, project_feedback, cv_match_rate, project_score
        )
        
        # Create evaluation result
        return EvaluationResult(
            cv_match_rate=cv_match_rate,
            cv_feedback=cv_feedback,
            project_score=project_score,
            project_feedback=project_feedback,
            overall_summary=overall_summary,
            cv_evaluation_details=cv_evaluation,
            project_evaluation_details=project_evaluation
        )
    
    async def _simulate_processing_delay(self):
        """Simulate processing time and potential failures for demonstration"""
        # Random delay between 2-8 seconds
        delay = random.uniform(2, 8)
        await asyncio.sleep(delay)
        
        # Simulate random failures (5% chance)
        if random.random() < 0.05:
            failure_types = [
                "Gemini API rate limit exceeded",
                "Network timeout during AI processing",
                "Temporary service unavailable"
            ]
            raise Exception(random.choice(failure_types))
        
        # Simulate partial delays for different steps
        if random.random() < 0.3:
            await asyncio.sleep(random.uniform(1, 3))

# Global instance
evaluation_pipeline = EvaluationPipeline()

async def get_evaluation_pipeline() -> EvaluationPipeline:
    """Get evaluation pipeline instance"""
    return evaluation_pipeline