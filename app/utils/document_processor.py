import os
import PyPDF2
from docx import Document
import aiofiles
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Utility class for processing different document formats"""
    
    @staticmethod
    async def extract_text_from_file(file_path: str) -> str:
        """Extract text from various file formats"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return await DocumentProcessor._extract_from_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                return await DocumentProcessor._extract_from_docx(file_path)
            elif file_extension == '.txt':
                return await DocumentProcessor._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise
    
    @staticmethod
    async def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error reading PDF file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    async def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error reading DOCX file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    async def _extract_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                return await file.read()
        except Exception as e:
            logger.error(f"Error reading TXT file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def validate_file_size(file_path: str, max_size_mb: int = 10) -> bool:
        """Validate file size"""
        try:
            file_size = os.path.getsize(file_path)
            max_size_bytes = max_size_mb * 1024 * 1024
            return file_size <= max_size_bytes
        except Exception as e:
            logger.error(f"Error checking file size for {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def validate_file_format(filename: str) -> bool:
        """Validate file format"""
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_extension = os.path.splitext(filename)[1].lower()
        return file_extension in allowed_extensions