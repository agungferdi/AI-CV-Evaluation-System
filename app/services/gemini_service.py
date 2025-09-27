import google.generativeai as genai
import json
import os
import asyncio
from typing import Dict, Any, Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
from app.models.schemas import ExtractedCVData, CVEvaluation, ProjectEvaluation

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Gemini API with retry logic and prompt chaining"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,))
    )
    async def generate_content_async(self, prompt: str, temperature: float = 0.1) -> str:
        """Generate content with retry logic"""
        try:
            # Simulate async behavior since genai doesn't have native async support
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=2048,
                    )
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {str(e)}")
            raise
    
    async def extract_cv_structure(self, cv_text: str) -> ExtractedCVData:
        """Step 1: Extract structured information from CV"""
        prompt = f"""
        Analyze the following CV text and extract structured information in JSON format.
        Return ONLY the JSON, no additional text or formatting.
        
        Expected JSON structure:
        {{
            "skills": ["skill1", "skill2", ...],
            "experiences": ["experience1", "experience2", ...],
            "projects": ["project1", "project2", ...],
            "education": ["education1", "education2", ...],
            "years_of_experience": number_or_null,
            "achievements": ["achievement1", "achievement2", ...]
        }}
        
        CV Text:
        {cv_text}
        """
        
        try:
            response = await self.generate_content_async(prompt)
            # Clean response and parse JSON
            json_text = response.strip()
            if json_text.startswith('```json'):
                json_text = json_text[7:-3]
            elif json_text.startswith('```'):
                json_text = json_text[3:-3]
            
            data = json.loads(json_text)
            return ExtractedCVData(**data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from CV extraction: {e}")
            # Return default structure if parsing fails
            return ExtractedCVData(
                skills=[], experiences=[], projects=[], 
                education=[], achievements=[], years_of_experience=None
            )
    
    async def evaluate_cv_match(self, cv_data: ExtractedCVData, job_description: str, 
                               retrieved_context: str) -> tuple[float, str, CVEvaluation]:
        """Step 2 & 3: Compare CV with job requirements and generate match rate"""
        prompt = f"""
        You are an expert HR evaluator. Analyze how well this candidate matches the job requirements.
        
        Job Description:
        {job_description}
        
        Additional Context:
        {retrieved_context}
        
        Candidate Data:
        - Skills: {', '.join(cv_data.skills)}
        - Experience: {cv_data.years_of_experience} years
        - Experiences: {'; '.join(cv_data.experiences)}
        - Projects: {'; '.join(cv_data.projects)}
        - Education: {'; '.join(cv_data.education)}
        - Achievements: {'; '.join(cv_data.achievements)}
        
        Provide evaluation in JSON format:
        {{
            "match_rate": 0.0-1.0,
            "feedback": "detailed feedback string",
            "detailed_scores": {{
                "technical_skills_match": 1-5,
                "experience_level": 1-5,
                "relevant_achievements": 1-5,
                "cultural_fit": 1-5,
                "overall_score": 1-5
            }}
        }}
        """
        
        try:
            response = await self.generate_content_async(prompt)
            json_text = response.strip()
            if json_text.startswith('```json'):
                json_text = json_text[7:-3]
            elif json_text.startswith('```'):
                json_text = json_text[3:-3]
            
            data = json.loads(json_text)
            cv_evaluation = CVEvaluation(**data['detailed_scores'])
            return data['match_rate'], data['feedback'], cv_evaluation
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse CV evaluation: {e}")
            return 0.5, "Unable to evaluate CV properly", CVEvaluation(
                technical_skills_match=3, experience_level=3, relevant_achievements=3,
                cultural_fit=3, overall_score=3
            )
    
    async def evaluate_project_report(self, project_text: str, scoring_rubric: str) -> tuple[float, str, ProjectEvaluation]:
        """Step 4: Evaluate project report with refinement"""
        
        # First evaluation
        initial_prompt = f"""
        Evaluate this project report based on the scoring rubric.
        
        Scoring Rubric:
        {scoring_rubric}
        
        Project Report:
        {project_text}
        
        Provide initial evaluation in JSON format:
        {{
            "score": 1.0-10.0,
            "feedback": "detailed feedback",
            "detailed_scores": {{
                "correctness": 1-5,
                "code_quality": 1-5,
                "resilience": 1-5,
                "documentation": 1-5,
                "creativity": 1-5,
                "overall_score": 1-5
            }}
        }}
        """
        
        try:
            initial_response = await self.generate_content_async(initial_prompt, temperature=0.2)
            json_text = initial_response.strip()
            if json_text.startswith('```json'):
                json_text = json_text[7:-3]
            elif json_text.startswith('```'):
                json_text = json_text[3:-3]
            
            initial_data = json.loads(json_text)
            
            # Second evaluation for refinement
            refinement_prompt = f"""
            Review and refine this project evaluation. Consider if the scoring is fair and consistent.
            
            Initial Evaluation:
            {json.dumps(initial_data, indent=2)}
            
            Project Report (for reference):
            {project_text[:1000]}...
            
            Provide refined evaluation in the same JSON format, but ensure consistency and fairness.
            """
            
            refined_response = await self.generate_content_async(refinement_prompt, temperature=0.1)
            json_text = refined_response.strip()
            if json_text.startswith('```json'):
                json_text = json_text[7:-3]
            elif json_text.startswith('```'):
                json_text = json_text[3:-3]
            
            refined_data = json.loads(json_text)
            project_evaluation = ProjectEvaluation(**refined_data['detailed_scores'])
            
            return refined_data['score'], refined_data['feedback'], project_evaluation
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse project evaluation: {e}")
            return 5.0, "Unable to evaluate project properly", ProjectEvaluation(
                correctness=3, code_quality=3, resilience=3,
                documentation=3, creativity=3, overall_score=3
            )
    
    async def generate_overall_summary(self, cv_feedback: str, project_feedback: str, 
                                     cv_match_rate: float, project_score: float) -> str:
        """Generate overall candidate summary"""
        prompt = f"""
        Generate a concise overall summary for this candidate evaluation:
        
        CV Match Rate: {cv_match_rate:.2f}
        CV Feedback: {cv_feedback}
        
        Project Score: {project_score}/10
        Project Feedback: {project_feedback}
        
        Provide a 2-3 sentence overall summary that highlights key strengths, areas for improvement,
        and hiring recommendation.
        """
        
        try:
            return await self.generate_content_async(prompt, temperature=0.3)
        except Exception as e:
            logger.error(f"Failed to generate overall summary: {e}")
            return "Unable to generate comprehensive summary due to evaluation errors."