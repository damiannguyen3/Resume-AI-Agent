from http.server import BaseHTTPRequestHandler
import json
import os
from typing import Optional
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Pydantic models
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

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({'status': 'healthy', 'service': 'Resume SEO Analyzer'})
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            if self.path == '/api/analyze/sample':
                response_data = self.handle_sample_analysis()
            elif self.path == '/api/analyze':
                body = json.loads(post_data.decode('utf-8'))
                resume_text = body.get('resume_text', '')
                
                if not resume_text:
                    self.send_error_response('Resume text is required', 400)
                    return
                
                response_data = self.handle_resume_analysis(resume_text)
            else:
                self.send_error_response('Endpoint not found', 404)
                return
            
            self.send_json_response(response_data)
            
        except Exception as e:
            self.send_error_response(f'Internal server error: {str(e)}', 500)

    def handle_resume_analysis(self, resume_text: str):
        """Analyze the provided resume text using Google Gemini"""
        try:
            # Initialize the Gemini LLM
            gemini_api_key = os.environ.get('GOOGLE_API_KEY')
            if not gemini_api_key:
                raise Exception('Google API key not configured')
            
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
            
            return {
                'analysis': analysis_result.dict(),
                'resume_length': len(resume_text),
                'word_count': len(resume_text.split()),
                'timestamp': 'vercel'
            }
            
        except Exception as e:
            raise Exception(f'Analysis failed: {str(e)}')

    def handle_sample_analysis(self):
        """Return a sample analysis for testing"""
        return {
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

    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data)
        self.wfile.write(response.encode())

    def send_error_response(self, message, status_code=400):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps({'detail': message})
        self.wfile.write(response.encode())
