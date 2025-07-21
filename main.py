from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()

class SEORecommendation(BaseModel):
  category: str  # e.g., "Keywords", "Skills", "Industry Terms"
  recommendation: str
  priority: str  # "High", "Medium", "Low"
  implementation: str  # How to implement this

class ScoreBreakdown(BaseModel):
    keyword_score: int  # /10
    ats_compatibility: int  # /10
    industry_terms: int  # /10
    skills_optimization: int  # /10
    format_structure: int  # /10
    explanation: str

class ResumeAnalysis(BaseModel):
  current_role: str
  target_industry: str
  missing_keywords: list[str]
  seo_recommendations: list[SEORecommendation]
  overall_score: int  # 1-10
  score_breakdown: ScoreBreakdown
  summary: str

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system", 
      """
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
      """,
    ),
    ("user", "Please analyze this resume for SEO optimization:\n\n{resume_text}"),
  ]
).partial(format_instructions=parser.get_format_instructions())

def analyze_resume(resume_text: str):
    """Analyze a resume and provide SEO recommendations"""
    chain = prompt | llm | parser
    
    try:
        analysis = chain.invoke({"resume_text": resume_text})
        return analysis
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        return None

def read_resume_file(file_path: str) -> str:
    """Read resume from various file formats"""
    try:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        elif file_path.endswith('.pdf'):
            # You can add PDF reading with PyPDF2 or similar
            print("PDF reading not implemented yet. Please convert to .txt file.")
            return None
        elif file_path.endswith('.docx'):
            # You can add DOCX reading with python-docx
            print("DOCX reading not implemented yet. Please convert to .txt file.")
            return None
        else:
            print("Unsupported file format. Please use .txt files.")
            return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Sample resume for testing
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

# Interactive resume analysis
def main():
    print("🔍 Resume SEO Analyzer")
    print("=" * 40)
    
    choice = input("\nChoose an option:\n1. Analyze sample resume\n2. Upload your own resume (.txt file)\n3. Paste resume text\n\nEnter choice (1-3): ")
    
    resume_text = None
    
    if choice == "1":
        # Use sample resume
        resume_text = sample_resume
        print("\nUsing sample resume...")
        
    elif choice == "2":
        file_path = input("Enter the path to your resume file (.txt): ")
        resume_text = read_resume_file(file_path)
        
    elif choice == "3":
        print("\nPaste your resume text (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        resume_text = "\n".join(lines)
        
    else:
        print("Invalid choice!")
        return
    
    if resume_text:
        print("\n🔄 Analyzing resume...")
        result = analyze_resume(resume_text)
        
        if result:
            print("\n✅ Analysis Complete!")
            print("=" * 50)
            print(f"📋 Current Role: {result.current_role}")
            print(f"🎯 Target Industry: {result.target_industry}")
            print(f"⭐ Overall SEO Score: {result.overall_score}/10")
            
            # Display detailed score breakdown
            print(f"\n📊 Score Breakdown:")
            print(f"   🔤 Keywords: {result.score_breakdown.keyword_score}/10")
            print(f"   🤖 ATS Compatibility: {result.score_breakdown.ats_compatibility}/10")
            print(f"   🏭 Industry Terms: {result.score_breakdown.industry_terms}/10")
            print(f"   💪 Skills Optimization: {result.score_breakdown.skills_optimization}/10")
            print(f"   📄 Format & Structure: {result.score_breakdown.format_structure}/10")
            print(f"   💡 Explanation: {result.score_breakdown.explanation}")
            
            print(f"\n📝 Summary: {result.summary}")
            
            if result.missing_keywords:
                print(f"\n🔍 Missing Keywords: {', '.join(result.missing_keywords)}")
            
            print(f"\n💡 SEO Recommendations ({len(result.seo_recommendations)} total):")
            print("=" * 50)
            
            for i, rec in enumerate(result.seo_recommendations, 1):
                priority_emoji = "🔴" if rec.priority == "High" else "🟡" if rec.priority == "Medium" else "🟢"
                print(f"\n{i}. {priority_emoji} {rec.category} [{rec.priority} Priority]")
                print(f"   💡 {rec.recommendation}")
                print(f"   🛠️  How to implement: {rec.implementation}")
        else:
            print("❌ Failed to analyze resume")
    else:
        print("❌ No resume text provided")

if __name__ == "__main__":
    main()

