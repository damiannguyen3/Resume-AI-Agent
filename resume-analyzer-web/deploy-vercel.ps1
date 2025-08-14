# Vercel Deployment Script for Resume Analyzer
# Run this script to deploy your app to Vercel

Write-Host "🚀 Resume SEO Analyzer - Vercel Deployment" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if we're in the right directory
$currentPath = Get-Location
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Please run this script from the resume-analyzer-web directory" -ForegroundColor Red
    Write-Host "cd `"c:\Users\Damian\AI Agent\resume-analyzer-web`"" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found package.json" -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js first." -ForegroundColor Red
    exit 1
}

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Cyan
    git init
    git add .
    git commit -m "Initial commit for Vercel deployment"
}

Write-Host "`n📋 Pre-deployment checklist:" -ForegroundColor Cyan
Write-Host "1. ✅ React app created and tested locally"
Write-Host "2. ✅ API endpoints created in /api folder"
Write-Host "3. ✅ vercel.json configuration file created"
Write-Host "4. Do you have a Google Gemini API key?"
Write-Host "5. Do you have a GitHub account?"
Write-Host "6. Do you have a Vercel account?"

$apiKey = Read-Host "`nDo you have your Google Gemini API key ready? (y/n)"
if ($apiKey -ne "y" -and $apiKey -ne "Y") {
    Write-Host "Please get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
    exit 0
}

$github = Read-Host "Have you pushed your code to GitHub? (y/n)"
if ($github -ne "y" -and $github -ne "Y") {
    Write-Host "Please push your code to GitHub first, then run this script again." -ForegroundColor Yellow
    Write-Host "Commands:" -ForegroundColor Cyan
    Write-Host "git add ." -ForegroundColor Gray
    Write-Host "git commit -m 'Ready for Vercel deployment'" -ForegroundColor Gray
    Write-Host "git push origin main" -ForegroundColor Gray
    exit 0
}

Write-Host "`n🔧 Installing Vercel CLI..." -ForegroundColor Cyan
try {
    $vercelVersion = vercel --version
    Write-Host "✅ Vercel CLI already installed: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

Write-Host "`n🚀 Starting Vercel deployment..." -ForegroundColor Cyan
Write-Host "You'll be prompted to:" -ForegroundColor Yellow
Write-Host "1. Login to Vercel (if not already logged in)"
Write-Host "2. Link to existing project or create new one"
Write-Host "3. Confirm project settings"

Write-Host "`nRunning: vercel" -ForegroundColor Cyan
vercel

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Deployment successful!" -ForegroundColor Green
    Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to your Vercel dashboard: https://vercel.com/dashboard"
    Write-Host "2. Find your project and go to Settings → Environment Variables"
    Write-Host "3. Add environment variable:"
    Write-Host "   Name: GOOGLE_API_KEY"
    Write-Host "   Value: [your Google Gemini API key]"
    Write-Host "4. Redeploy the project after adding the environment variable"
    Write-Host "`n🎉 Your app will be live at the URL shown above!" -ForegroundColor Green
    
    Write-Host "`nWant to deploy to production now? (y/n)" -ForegroundColor Cyan
    $prod = Read-Host
    if ($prod -eq "y" -or $prod -eq "Y") {
        Write-Host "`nDeploying to production..." -ForegroundColor Cyan
        vercel --prod
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n🎊 Production deployment successful!" -ForegroundColor Green
            Write-Host "Your resume analyzer is now live!" -ForegroundColor Green
        }
    }
} else {
    Write-Host "`n❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Check the error messages above and try again." -ForegroundColor Yellow
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
