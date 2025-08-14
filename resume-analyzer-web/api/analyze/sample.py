from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # Sample analysis data
        sample_data = {
            'analysis': {
                'target_industry': 'Technology',
                'missing_keywords': ['Python', 'Machine Learning', 'React', 'Node.js'],
                'seo_recommendations': [
                    {
                        'category': 'Keywords',
                        'recommendation': 'Add more technical keywords like "Full-stack development", "API integration"',
                        'priority': 'High',
                        'implementation': 'Include these terms in your experience section and skills list'
                    },
                    {
                        'category': 'ATS Optimization',
                        'recommendation': 'Use bullet points and standard section headers',
                        'priority': 'High',
                        'implementation': 'Format with clear sections: Experience, Education, Skills, Projects'
                    },
                    {
                        'category': 'Quantified Achievements',
                        'recommendation': 'Add metrics and numbers to your accomplishments',
                        'priority': 'Medium',
                        'implementation': 'Include percentages, dollar amounts, time saved, etc.'
                    }
                ],
                'overall_score': 7,
                'score_breakdown': {
                    'keyword_score': 6,
                    'ats_compatibility': 8,
                    'content_quality': 7,
                    'format_score': 7
                },
                'summary': 'Strong technical background but could benefit from more industry keywords and quantified achievements. Consider highlighting specific technologies and project outcomes.'
            },
            'resume_length': 1200,
            'word_count': 180,
            'timestamp': 'sample-vercel'
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(sample_data)
        self.wfile.write(response.encode())

    def do_GET(self):
        # Redirect GET to POST for sample endpoint
        self.do_POST()
