# AWS Serverless Deployment Script for Resume Analyzer
# Run this script to deploy your app to AWS

Write-Host "🚀 Resume SEO Analyzer - AWS Deployment Script" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if AWS CLI is installed
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI installed: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "winget install Amazon.AWSCLI" -ForegroundColor Yellow
    exit 1
}

# Check if SAM CLI is installed
try {
    $samVersion = sam --version
    Write-Host "✅ SAM CLI installed: $samVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ SAM CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "winget install Amazon.SAM-CLI" -ForegroundColor Yellow
    exit 1
}

# Check AWS credentials
try {
    $identity = aws sts get-caller-identity 2>$null
    if ($identity) {
        Write-Host "✅ AWS credentials configured" -ForegroundColor Green
    } else {
        throw "No credentials"
    }
} catch {
    Write-Host "❌ AWS credentials not configured. Please run:" -ForegroundColor Red
    Write-Host "aws configure" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n📋 Pre-deployment checklist:" -ForegroundColor Cyan
Write-Host "1. Do you have a Google Gemini API key? (Get one at: https://makersuite.google.com/app/apikey)"
Write-Host "2. Have you tested your app locally?"
Write-Host "3. Are you ready to deploy to AWS?"

$continue = Read-Host "`nContinue with deployment? (y/n)"
if ($continue -ne "y" -and $continue -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Navigate to serverless deploy directory
Set-Location "c:\Users\Damian\AI Agent\serverless-deploy"

Write-Host "`n🔨 Building SAM application..." -ForegroundColor Cyan
sam build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build successful!" -ForegroundColor Green

Write-Host "`n🚀 Starting deployment..." -ForegroundColor Cyan
Write-Host "You'll be prompted for configuration. Use these suggestions:" -ForegroundColor Yellow
Write-Host "- Stack name: resume-analyzer-serverless"
Write-Host "- AWS Region: us-east-1 (or your preferred region)"
Write-Host "- GoogleApiKey: [paste your Google Gemini API key]"
Write-Host "- Confirm changes: Y"
Write-Host "- Allow SAM to create roles: Y"
Write-Host "- Save parameters: Y"

sam deploy --guided

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Backend deployed successfully!" -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Note down the API Gateway URL from the output above"
Write-Host "2. Update your React app's .env.production file with the API URL"
Write-Host "3. Build and deploy the frontend:"
Write-Host "   cd `"c:\Users\Damian\AI Agent\resume-analyzer-web`""
Write-Host "   npm run build"
Write-Host "   aws s3 sync build/ s3://[your-bucket-name] --delete"
Write-Host "`n🎉 Your resume analyzer will be live shortly!" -ForegroundColor Green

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
