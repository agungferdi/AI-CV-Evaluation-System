import os
import asyncio
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class VectorDBService:
    """Simple in-memory vector database service for storing evaluation context"""
    
    def __init__(self):
        self.documents = {}
        self.initialized = False
    
    async def initialize(self):
        """Initialize vector database with default data"""
        try:
            if not self.initialized:
                await self._populate_initial_data()
                self.initialized = True
                logger.info("In-memory vector database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize vector database: {e}")
            raise
    
    async def _populate_initial_data(self):
        """Populate vector database with initial job descriptions and scoring rubrics"""
        
        default_data = [
            {
                "id": "job_desc_backend",
                "content": """
                Backend Developer Position Requirements:
                
                Technical Skills Required:
                - Proficiency in Python, Java, or Node.js
                - Experience with REST API development and design
                - Knowledge of databases (SQL and NoSQL)
                - Cloud platforms experience (AWS, GCP, Azure)
                - Understanding of microservices architecture
                - Version control with Git
                - Experience with Docker and containerization
                - API documentation and testing
                
                Experience Requirements:
                - 3+ years of backend development experience
                - Experience with high-traffic applications
                - Knowledge of system design principles
                - Experience with CI/CD pipelines
                - Understanding of security best practices
                
                Preferred Skills:
                - AI/ML integration experience
                - Experience with LLM APIs
                - Knowledge of vector databases
                - Experience with async programming
                - DevOps and infrastructure knowledge
                
                Cultural Fit:
                - Strong problem-solving skills
                - Good communication abilities
                - Team collaboration experience
                - Continuous learning mindset
                - Attention to detail
                """,
                "type": "job_description",
                "category": "backend_developer"
            },
            {
                "id": "scoring_rubric_cv",
                "content": """
                CV Evaluation Scoring Rubric:
                
                Technical Skills Match (1-5):
                5 - Exceptional: All required skills + advanced expertise
                4 - Strong: Most required skills + some advanced areas
                3 - Good: Core required skills present
                2 - Adequate: Some required skills, gaps present
                1 - Insufficient: Major skill gaps
                
                Experience Level (1-5):
                5 - Senior level with complex project leadership
                4 - Mid-senior with significant contributions
                3 - Mid-level with relevant experience
                2 - Junior with some relevant experience
                1 - Entry level or limited experience
                
                Relevant Achievements (1-5):
                5 - Outstanding achievements with measurable impact
                4 - Strong achievements in relevant areas
                3 - Good achievements demonstrating competence
                2 - Some achievements, limited impact shown
                1 - Few or no relevant achievements
                
                Cultural Fit (1-5):
                5 - Excellent communication, leadership, learning attitude
                4 - Strong collaboration and communication skills
                3 - Good team player with communication skills
                2 - Adequate interpersonal skills
                1 - Limited evidence of soft skills
                """,
                "type": "scoring_rubric",
                "category": "cv_evaluation"
            },
            {
                "id": "scoring_rubric_project",
                "content": """
                Project Deliverable Evaluation Rubric:
                
                Correctness (1-5):
                5 - Fully meets all requirements with excellent implementation
                4 - Meets most requirements with good implementation
                3 - Meets core requirements adequately
                2 - Partially meets requirements
                1 - Fails to meet basic requirements
                
                Code Quality (1-5):
                5 - Exceptional: Clean, modular, well-documented, testable
                4 - Good: Well-structured with good practices
                3 - Adequate: Readable with some structure
                2 - Poor: Limited structure, hard to follow
                1 - Very poor: Messy, unorganized code
                
                Resilience (1-5):
                5 - Comprehensive error handling, retries, fault tolerance
                4 - Good error handling with some resilience features
                3 - Basic error handling present
                2 - Limited error handling
                1 - Poor or no error handling
                
                Documentation (1-5):
                5 - Excellent: Complete README, API docs, design explanations
                4 - Good: Clear README with setup and usage instructions
                3 - Adequate: Basic documentation present
                2 - Limited: Minimal documentation
                1 - Poor: Little to no documentation
                
                Creativity/Bonus (1-5):
                5 - Exceptional additional features and innovations
                4 - Good additional features or improvements
                3 - Some creative elements or enhancements
                2 - Minor additional features
                1 - No additional features beyond requirements
                """,
                "type": "scoring_rubric",
                "category": "project_evaluation"
            }
        ]
        
        # Store documents in memory
        for data in default_data:
            self.documents[data["id"]] = data
        
        logger.info(f"Populated vector database with {len(default_data)} default documents")
    
    async def retrieve_context(self, query: str, context_type: str = None, n_results: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant context based on query (simple keyword matching)"""
        try:
            retrieved_docs = []
            
            # Simple keyword-based retrieval
            query_words = query.lower().split()
            
            for doc_id, doc_data in self.documents.items():
                # Filter by type if specified
                if context_type and doc_data["type"] != context_type:
                    continue
                
                # Simple scoring based on keyword matches
                content_lower = doc_data["content"].lower()
                score = sum(1 for word in query_words if word in content_lower)
                
                if score > 0:
                    retrieved_docs.append({
                        "content": doc_data["content"],
                        "metadata": {
                            "type": doc_data["type"],
                            "category": doc_data["category"]
                        },
                        "score": score
                    })
            
            # Sort by score and limit results
            retrieved_docs.sort(key=lambda x: x["score"], reverse=True)
            retrieved_docs = retrieved_docs[:n_results]
            
            logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query[:50]}...")
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    async def add_document(self, content: str, doc_id: str, doc_type: str, category: str):
        """Add a new document to the vector database"""
        try:
            self.documents[doc_id] = {
                "id": doc_id,
                "content": content,
                "type": doc_type,
                "category": category
            }
            logger.info(f"Added document {doc_id} to vector database")
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise

# Global instance
vector_db_service = VectorDBService()

async def initialize_vector_db():
    """Initialize the vector database service"""
    await vector_db_service.initialize()

async def get_vector_db() -> VectorDBService:
    """Get vector database service instance"""
    return vector_db_service