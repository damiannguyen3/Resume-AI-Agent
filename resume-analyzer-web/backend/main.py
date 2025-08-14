from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

app = FastAPI(title="Resume SEO Analyzer API", version="1.0.0")

# CORS middleware to allow React frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models (same as your existing code)
class SEORecommendation(BaseModel):
    category: str
    recommendation: str
    priority: str
    implementation: str

class ScoreBreakdown(BaseModel):
    keyword_score: int
    ats_compatibility: int
    industry_terms: int
    skills_optimization: int
    format_structure: int
    explanation: str

class ResumeAnalysis(BaseModel):
    current_role: str
    target_industry: str
    missing_keywords: List[str]
    seo_recommendations: List[SEORecommendation]
    overall_score: int
    score_breakdown: ScoreBreakdown
    summary: str

class ResumeRequest(BaseModel):
    resume_text: str
    user_email: Optional[str] = None

# Initialize LLM and parser
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an expert resume SEO analyst. Analyze the provided resume and provide specific search engine optimization recommendations.

    Focus on:
    1. ATS (Applicant Tracking System) optimization
    2. Industry-specific keywords
    3. Skills and technologies that should be highlighted
    4. Format and structure improvements for better scanning
    5. Missing keywords that recruiters commonly search for

    SCORING SYSTEM (1-10):
    - 1-3: Poor - Major SEO issues, missing critical keywords, poor ATS compatibility
    - 4-5: Below Average - Some keywords present but lacks optimization, formatting issues
    - 6-7: Good - Decent keyword usage, mostly ATS-friendly, room for improvement
    - 8-9: Excellent - Well-optimized, strong keyword presence, ATS-friendly format
    - 10: Perfect - Exceptional SEO optimization, comprehensive keywords, ideal ATS format

    Consider these scoring factors:
    • Keyword density and relevance (25%)
    • ATS compatibility (25%)
    • Industry-specific terminology (20%)
    • Skills section optimization (15%)
    • Format and structure (15%)

    Provide actionable, specific recommendations with priority levels.

    {format_instructions}
    """),
    ("user", "Please analyze this resume for SEO optimization:\n\n{resume_text}"),
]).partial(format_instructions=parser.get_format_instructions())

def analyze_resume_service(resume_text: str) -> ResumeAnalysis:
    """Analyze a resume and provide SEO recommendations"""
    chain = prompt | llm | parser
    
    try:
        analysis = chain.invoke({"resume_text": resume_text})
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

# API Routes
@app.get("/")
async def root():
    return {"message": "Resume SEO Analyzer API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "google_api_configured": bool(os.getenv("GOOGLE_API_KEY"))}

@app.post("/api/analyze", response_model=ResumeAnalysis)
async def analyze_resume_endpoint(request: ResumeRequest):
    """
    Analyze a resume and return SEO recommendations
    """
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")
    
    try:
        result = analyze_resume_service(request.resume_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/sample")
async def analyze_sample_resume():
    """
    Analyze the sample resume for testing
    """
    sample_resume = """
John Smith
Software Developer
Email: john.smith@email.com
Phone: (555) 123-4567

Experience:
- Worked at Tech Company for 2 years
- Built websites using JavaScript
- Fixed bugs and wrote code

Education:
- Computer Science Degree from University

Skills:
- Programming
- Problem solving
"""
    
    try:
        result = analyze_resume_service(sample_resume)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
