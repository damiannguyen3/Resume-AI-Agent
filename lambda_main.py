import json
import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

def lambda_handler(event, context):
    """
    AWS Lambda handler for resume analysis
    """
    try:
        # Handle CORS preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': ''
            }
        
        # Parse the request body
        if event.get('body'):
            body = json.loads(event['body'])
        else:
            body = event
        
        # Handle different endpoints
        path = event.get('path', '').replace('/prod', '')  # Remove stage prefix
        
        if path == '/health':
            return create_response({'status': 'healthy', 'service': 'Resume SEO Analyzer'})
        
        elif path == '/api/analyze/sample':
            return handle_sample_analysis()
        
        elif path == '/api/analyze':
            resume_text = body.get('resume_text', '')
            if not resume_text:
                return create_error_response('Resume text is required', 400)
            
            return handle_resume_analysis(resume_text)
        
        else:
            return create_error_response('Endpoint not found', 404)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_error_response(f'Internal server error: {str(e)}', 500)

def handle_resume_analysis(resume_text: str):
    """Analyze the provided resume text"""
    try:
        # Initialize the OpenAI LLM
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not openai_api_key:
            return create_error_response('OpenAI API key not configured', 500)
        
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            openai_api_key=openai_api_key
        )
        
        # Create the analysis prompt
        prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
            You are an expert resume optimizer and SEO specialist. Analyze the following resume and provide detailed recommendations for search engine optimization and ATS (Applicant Tracking System) compatibility.

            Resume Text:
            {resume_text}

            Please provide a comprehensive analysis with the following sections:

            1. **SEO Keywords Analysis**:
               - List missing industry-relevant keywords
               - Suggest specific keywords to add based on the role/industry
               - Rate current keyword density (1-10)

            2. **ATS Optimization**:
               - Identify potential ATS scanning issues
               - Suggest formatting improvements
               - Recommend section restructuring if needed

            3. **Content Recommendations**:
               - Missing critical sections
               - Weak areas that need strengthening
               - Specific achievements to highlight better

            4. **Technical Improvements**:
               - File format recommendations
               - Formatting suggestions
               - Length and structure optimization

            5. **Industry-Specific Suggestions**:
               - Role-specific keywords to include
               - Industry trends to incorporate
               - Professional buzzwords that add value

            Please format your response as structured JSON with clear sections and actionable recommendations.
            """
        )
        
        # Create the chain
        chain = prompt | llm | StrOutputParser()
        
        # Run the analysis
        analysis_result = chain.invoke({"resume_text": resume_text})
        
        return create_response({
            'analysis': analysis_result,
            'resume_length': len(resume_text),
            'word_count': len(resume_text.split()),
            'timestamp': context.aws_request_id if 'context' in globals() else 'local'
        })
        
    except Exception as e:
        return create_error_response(f'Analysis failed: {str(e)}', 500)

def handle_sample_analysis():
    """Return a sample analysis for testing"""
    sample_analysis = {
        'analysis': '''
        **SEO Keywords Analysis** (Score: 6/10)
        • Missing keywords: "data analysis", "machine learning", "Python programming"
        • Current keyword density is moderate
        • Recommend adding more technical skills

        **ATS Optimization** (Score: 7/10)
        • Good use of standard section headers
        • Consider adding a "Technical Skills" section
        • Use bullet points consistently

        **Content Recommendations**
        • Add quantified achievements (e.g., "increased efficiency by 25%")
        • Include more action verbs
        • Expand on project outcomes

        **Technical Improvements**
        • Use PDF format for better ATS compatibility
        • Ensure consistent formatting
        • Keep resume to 1-2 pages

        **Industry-Specific Suggestions**
        • Add certifications if available
        • Include relevant software proficiencies
        • Mention collaborative project experience
        ''',
        'resume_length': 850,
        'word_count': 127,
        'timestamp': 'sample'
    }
    
    return create_response(sample_analysis)

def create_response(data, status_code=200):
    """Create a standardized API response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }

def create_error_response(message, status_code=400):
    """Create a standardized error response"""
    return create_response({'detail': message}, status_code)
