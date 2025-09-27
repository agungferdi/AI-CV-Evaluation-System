#!/usr/bin/env python3
"""
Test script to verify the CV Evaluation Backend setup
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from app.models.schemas import EvaluationResult, TaskStatus
        print("✓ Models imported successfully")
        
        from app.services.gemini_service import GeminiService
        print("✓ Gemini service imported successfully")
        
        from app.services.vector_db import VectorDBService
        print("✓ Vector DB service imported successfully")
        
        from app.utils.document_processor import DocumentProcessor
        print("✓ Document processor imported successfully")
        
        from app.api.routes import router
        print("✓ API routes imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

async def test_gemini_api():
    """Test Gemini API connectivity"""
    print("\nTesting Gemini API connectivity...")
    
    try:
        from app.services.gemini_service import GeminiService
        
        # Check if API key is configured
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("✗ GEMINI_API_KEY not found in environment")
            return False
        
        print(f"✓ API key configured (ends with: ...{api_key[-8:]})")
        
        # Test API call
        service = GeminiService()
        response = await service.generate_content_async("Hello, respond with just 'OK'")
        print(f"✓ API call successful: {response.strip()}")
        
        return True
    except Exception as e:
        print(f"✗ Gemini API test failed: {e}")
        return False

async def test_document_processing():
    """Test document processing"""
    print("\nTesting document processing...")
    
    try:
        from app.utils.document_processor import DocumentProcessor
        
        # Test with sample CV
        sample_cv_path = project_root / "sample_cv.txt"
        if sample_cv_path.exists():
            text = await DocumentProcessor.extract_text_from_file(str(sample_cv_path))
            print(f"✓ Text extracted from sample CV ({len(text)} characters)")
        else:
            print("✗ Sample CV file not found")
            return False
        
        # Test file validation
        if DocumentProcessor.validate_file_format("test.pdf"):
            print("✓ File format validation working")
        else:
            print("✗ File format validation failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Document processing test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("CV Evaluation Backend - Setup Verification")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    tests = [
        test_imports,
        test_gemini_api,
        test_document_processing
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All {total} tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Run: uvicorn main:app --reload")
        print("2. Open: http://localhost:8000/docs")
        print("3. Test the API endpoints")
    else:
        print(f"✗ {total - passed} of {total} tests failed.")
        print("Please check the error messages above and fix the issues.")
    
    return passed == total

if __name__ == "__main__":
    # Install python-dotenv if not present
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("Installing python-dotenv...")
        os.system("pip install python-dotenv")
        from dotenv import load_dotenv
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)