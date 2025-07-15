# 🔍 Resume SEO Analyzer

An AI-powered tool that analyzes resumes and provides specific SEO optimization recommendations to improve ATS (Applicant Tracking System) compatibility and recruiter visibility.

## ✨ Features

- **Smart Resume Analysis**: Uses Google's Gemini AI to analyze resume content
- **SEO Scoring**: Detailed scoring breakdown (1-10) across 5 key areas
- **ATS Optimization**: Recommendations for Applicant Tracking System compatibility
- **Keyword Analysis**: Identifies missing industry-specific keywords
- **Priority Recommendations**: Categorized suggestions with implementation guides

## 📊 Scoring Categories

1. **Keywords** (25%) - Job-specific and industry terminology
2. **ATS Compatibility** (25%) - Format and structure optimization
3. **Industry Terms** (20%) - Sector-specific vocabulary
4. **Skills Optimization** (15%) - Technical and soft skills highlighting
5. **Format & Structure** (15%) - Layout and readability

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google AI API key (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd resume-seo-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

4. **Get your Google AI API key**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

### Usage

```bash
python main.py
```

Choose from three options:
1. **Analyze sample resume** - Test with built-in example
2. **Upload resume file** - Analyze your own `.txt` file
3. **Paste resume text** - Copy and paste resume content

## 📋 Example Output

```
📋 Current Role: Software Developer
🎯 Target Industry: Technology
⭐ Overall SEO Score: 6/10

📊 Score Breakdown:
   🔤 Keywords: 5/10
   🤖 ATS Compatibility: 7/10
   🏭 Industry Terms: 4/10
   💪 Skills Optimization: 6/10
   📄 Format & Structure: 8/10

💡 SEO Recommendations (5 total):

1. 🔴 Keywords [High Priority]
   💡 Add specific programming languages and frameworks
   🛠️ Include: React, Node.js, Python, AWS, Docker
```

## 🛠️ Technologies Used

- **LangChain** - AI framework and prompt engineering
- **Google Gemini AI** - Natural language processing
- **Pydantic** - Data validation and structured output
- **Python-dotenv** - Environment variable management

## 📁 Project Structure

```
resume-seo-analyzer/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔒 Security

- **Never commit API keys** - Use `.env` file (included in `.gitignore`)
- **Free tier available** - Google AI offers generous free usage
- **No data storage** - Resumes are processed locally and not stored

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:
1. Check that your API key is correctly set in `.env`
2. Ensure all dependencies are installed
3. Verify your resume is in `.txt` format
4. Open an issue on GitHub for additional help

## 🔮 Future Features

- [ ] PDF and DOCX file support
- [ ] Industry-specific optimization templates
- [ ] Batch resume processing
- [ ] Resume comparison tool
- [ ] Export optimization reports

---

**Made with ❤️ to help job seekers optimize their resumes for better visibility**
