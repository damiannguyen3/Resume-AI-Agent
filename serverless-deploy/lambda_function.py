import json
import os
from typing import Optional
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Pydantic models (same as your backend)
class SEORecommendation(BaseModel):
    category: str
    recommendation: str
    priority: str
    implementation: str

class ScoreBreakdown(BaseModel):
    keyword_score: int
    ats_compatibility: int
    content_quality: int
    format_score: int

class ResumeAnalysis(BaseModel):
    target_industry: str
    missing_keywords: list[str]
    seo_recommendations: list[SEORecommendation]
    overall_score: int
    score_breakdown: ScoreBreakdown
    summary: str

def lambda_handler(event, context):
    """
    AWS Lambda handler for resume analysis
    """
    try:
        # Handle CORS preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return create_cors_response('', 200)
        
        # Parse the request
        path = event.get('path', '').replace('/Prod', '').replace('/prod', '')
        method = event.get('httpMethod', 'GET')
        
        print(f"Request: {method} {path}")
        
        # Route requests
        if path == '/health':
            return create_cors_response({'status': 'healthy', 'service': 'Resume SEO Analyzer'})
        
        elif path == '/api/analyze/sample':
            return handle_sample_analysis()
        
        elif path == '/api/analyze' and method == 'POST':
            if event.get('body'):
                body = json.loads(event['body'])
            else:
                body = event
            
            resume_text = body.get('resume_text', '')
            if not resume_text:
                return create_cors_response({'detail': 'Resume text is required'}, 400)
            
            return handle_resume_analysis(resume_text)
        
        else:
            return create_cors_response({'detail': 'Endpoint not found'}, 404)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_cors_response({'detail': f'Internal server error: {str(e)}'}, 500)

def handle_resume_analysis(resume_text: str):
    """Analyze the provided resume text using Google Gemini"""
    try:
        # Initialize the Gemini LLM
        gemini_api_key = os.environ.get('GOOGLE_API_KEY')
        if not gemini_api_key:
            return create_cors_response({'detail': 'Google API key not configured'}, 500)
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=gemini_api_key
        )
        
        # Set up the parser
        parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)
        
        # Create the analysis prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
You are an expert resume SEO analyst. Analyze the provided resume and provide specific search engine optimization recommendations.

Focus on:
1. ATS (Applicant Tracking System) optimization
2. Industry-specific keywords
3. Skills and technologies that should be highlighted
4. Format and structure improvements
5. Content enhancement suggestions

{format_instructions}
"""),
            ("human", "Analyze this resume:\n\n{resume_text}")
        ])
        
        # Format the prompt with instructions
        formatted_prompt = prompt.format_messages(
            format_instructions=parser.get_format_instructions(),
            resume_text=resume_text
        )
        
        # Run the analysis
        response = llm.invoke(formatted_prompt)
        analysis_result = parser.parse(response.content)
        
        return create_cors_response({
            'analysis': analysis_result.dict(),
            'resume_length': len(resume_text),
            'word_count': len(resume_text.split()),
            'timestamp': context.aws_request_id if 'context' in globals() else 'lambda'
        })
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return create_cors_response({'detail': f'Analysis failed: {str(e)}'}, 500)

def handle_sample_analysis():
    """Return a sample analysis for testing"""
    sample_analysis = {
        'analysis': {
            'target_industry': 'Technology',
            'missing_keywords': ['Python', 'Machine Learning', 'AWS', 'Docker'],
            'seo_recommendations': [
                {
                    'category': 'Keywords',
                    'recommendation': 'Add "Python programming" and "data analysis" keywords',
                    'priority': 'High',
                    'implementation': 'Include these terms in your skills section and project descriptions'
                },
                {
                    'category': 'ATS Optimization',
                    'recommendation': 'Use standard section headers like "Work Experience" and "Education"',
                    'priority': 'High',
                    'implementation': 'Replace creative headers with ATS-friendly standard ones'
                },
                {
                    'category': 'Technical Skills',
                    'recommendation': 'Create a dedicated technical skills section',
                    'priority': 'Medium',
                    'implementation': 'List programming languages, frameworks, and tools separately'
                }
            ],
            'overall_score': 7,
            'score_breakdown': {
                'keyword_score': 6,
                'ats_compatibility': 8,
                'content_quality': 7,
                'format_score': 7
            },
            'summary': 'Good foundation but needs more industry-specific keywords and technical skills highlighted. Consider adding quantified achievements and ensuring ATS compatibility.'
        },
        'resume_length': 850,
        'word_count': 127,
        'timestamp': 'sample'
    }
    
    return create_cors_response(sample_analysis)

def create_cors_response(data, status_code=200):
    """Create a response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data) if isinstance(data, (dict, list)) else data
    }
