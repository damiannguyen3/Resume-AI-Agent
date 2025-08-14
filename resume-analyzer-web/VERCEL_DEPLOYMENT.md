# Resume SEO Analyzer - Vercel Deployment Guide

## 🚀 Deploy to Vercel (Easiest Option!)

Vercel is perfect for full-stack React + Python applications and offers excellent free hosting.

## Prerequisites ✅

1. **GitHub Account**: [Sign up here](https://github.com) - FREE
2. **Vercel Account**: [Sign up here](https://vercel.com) - FREE tier available
3. **Google Gemini API Key**: [Get one here](https://makersuite.google.com/app/apikey) - FREE tier available

## Quick Deployment (5 minutes!)

### Option A: One-Click Deploy (Recommended)

1. **Push your code to GitHub**:
```powershell
cd "c:\Users\Damian\AI Agent\resume-analyzer-web"
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your `Resume-AI-Agent` repository
   - Vercel will auto-detect it's a React app

3. **Configure Environment Variables**:
   - In Vercel dashboard, go to Settings → Environment Variables
   - Add: `GOOGLE_API_KEY` = `your_gemini_api_key_here`
   - Click "Deploy"

### Option B: Vercel CLI

```powershell
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
cd "c:\Users\Damian\AI Agent\resume-analyzer-web"
vercel

# Follow the prompts:
# - Link to existing project? N
# - What's your project's name? resume-analyzer
# - In which directory is your code located? ./
# - Want to override the settings? N

# Add environment variables
vercel env add GOOGLE_API_KEY
# Paste your Google Gemini API key when prompted

# Deploy to production
vercel --prod
```

## What Vercel Provides 🎯

- **Frontend**: React app hosted on Vercel's global CDN
- **Backend**: Python API routes as serverless functions
- **Domain**: Custom `.vercel.app` domain (can add custom domain)
- **HTTPS**: Automatic SSL certificate
- **Auto-deployment**: Deploys on every Git push

## API Endpoints (after deployment)

Your app will have these endpoints:
- `https://your-app.vercel.app/api/health` - Health check
- `https://your-app.vercel.app/api/analyze` - Analyze resume
- `https://your-app.vercel.app/api/analyze/sample` - Sample analysis

## Cost Breakdown 💰

### Vercel Free Tier:
- **Bandwidth**: 100GB/month
- **Serverless Functions**: 100GB-Hrs/month
- **Build Time**: 6,000 minutes/month
- **Projects**: Unlimited
- **Custom Domains**: Included

### After Free Tier:
- **Pro Plan**: $20/month per user
- **Hobby usage**: Usually stays FREE

### Google Gemini API:
- **Free tier**: 15 requests/minute, 1,500 requests/day
- **Paid**: $0.001 per 1,000 characters

## Testing Your Deployment 🧪

After deployment, test these URLs:

```bash
# Health check
curl https://your-app.vercel.app/api/health

# Sample analysis
curl -X POST https://your-app.vercel.app/api/analyze/sample

# Full analysis
curl -X POST https://your-app.vercel.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Software Engineer with 5 years experience..."}'
```

## Project Structure for Vercel 📁

```
resume-analyzer-web/
├── api/                    # Serverless functions
│   ├── health.py          # Health endpoint
│   ├── analyze.py         # Main analysis endpoint
│   └── analyze/
│       └── sample.py      # Sample analysis endpoint
├── src/                   # React frontend
├── public/                # Static files
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── package.json          # Node.js dependencies
```

## Environment Variables 🔧

Set these in Vercel dashboard:

| Variable | Value | Description |
|----------|--------|-------------|
| `GOOGLE_API_KEY` | `your_api_key` | Google Gemini API key |

## Custom Domain (Optional) 🌐

1. **In Vercel Dashboard**:
   - Go to Project Settings → Domains
   - Add your custom domain
   - Update DNS records as instructed

2. **Popular Domain Providers**:
   - Namecheap, GoDaddy, Cloudflare

## Troubleshooting 🔧

### Common Issues:

1. **Build Errors**:
   - Check `vercel logs` for detailed error messages
   - Ensure all dependencies are in `package.json` and `requirements.txt`

2. **API Not Working**:
   - Verify environment variables are set
   - Check function logs in Vercel dashboard

3. **CORS Errors**:
   - The API files include CORS headers
   - If issues persist, check browser console

### Useful Commands:

```powershell
# View deployment logs
vercel logs

# View environment variables
vercel env ls

# Remove deployment
vercel remove

# Check deployment status
vercel inspect
```

## Advanced Features 🚀

### Analytics
```powershell
# Add Vercel Analytics (free)
npm install @vercel/analytics
```

### Monitoring
- Built-in performance monitoring
- Real-time function logs
- Usage statistics

### Scaling
- Automatic scaling based on traffic
- Global edge network
- Zero cold starts for React app

## Security Best Practices 🔐

- Environment variables are encrypted
- Automatic HTTPS
- No server to maintain or patch
- API keys never exposed to client

## Deployment Workflow 🔄

1. **Development**: Work locally with `npm start`
2. **Commit**: Push changes to GitHub
3. **Auto-deploy**: Vercel automatically deploys
4. **Preview**: Each PR gets a preview URL
5. **Production**: Merge to main for production deploy

## Support & Documentation 📚

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

Your resume analyzer will be live at `https://your-app.vercel.app` in minutes! 🎉
