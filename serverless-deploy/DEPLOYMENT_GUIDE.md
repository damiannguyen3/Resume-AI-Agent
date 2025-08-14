# Resume SEO Analyzer - AWS Serverless Deployment

## Prerequisites ✅

1. **AWS Account**: [Sign up here](https://aws.amazon.com) - FREE tier available
2. **Google Gemini API Key**: [Get one here](https://makersuite.google.com/app/apikey) - FREE tier available
3. **AWS CLI & SAM CLI**: Install using the commands below

## Step-by-Step Deployment

### 1. Install Required Tools

```powershell
# Install AWS CLI
winget install Amazon.AWSCLI

# Install SAM CLI
winget install Amazon.SAM-CLI

# Verify installations
aws --version
sam --version
```

### 2. Configure AWS Credentials

```powershell
# Configure AWS (you'll need Access Key ID and Secret from AWS Console)
aws configure

# Enter when prompted:
# - AWS Access Key ID: [from AWS Console -> IAM -> Users -> Security credentials]
# - AWS Secret Access Key: [from AWS Console]
# - Default region: us-east-1 (or your preferred region)
# - Default output format: json
```

### 3. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key (keep it safe!)

### 4. Deploy the Backend

```powershell
# Navigate to the serverless deployment folder
cd "c:\Users\Damian\AI Agent\serverless-deploy"

# Build the SAM application
sam build

# Deploy with guided setup (first time only)
sam deploy --guided

# You'll be prompted for:
# - Stack name: resume-analyzer-serverless
# - AWS Region: us-east-1 (or your choice)
# - GoogleApiKey: [paste your Google Gemini API key here]
# - Confirm changes before deploy: Y
# - Allow SAM to create IAM roles: Y
# - Save parameters to samconfig.toml: Y
```

### 5. Update Frontend Configuration

After deployment, you'll get an API Gateway URL. Update your React app:

```powershell
# Create production environment file
cd "c:\Users\Damian\AI Agent\resume-analyzer-web"
```

Create `.env.production` with your API URL:
```
REACT_APP_API_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod
```

### 6. Build and Deploy Frontend

```powershell
# Build the React app for production
npm run build

# Deploy to S3 (replace bucket name with your actual bucket from deployment output)
aws s3 sync build/ s3://resume-analyzer-serverless-website-123456789012 --delete
```

### 7. Get Your Live Website URL

After deployment, you'll get a CloudFront URL like:
`https://d1234567890abc.cloudfront.net`

## Cost Estimate 💰

### AWS Free Tier (12 months):
- **Lambda**: 1M requests/month (FREE)
- **API Gateway**: 1M calls/month (FREE)
- **S3**: 5GB storage (FREE)
- **CloudFront**: 50GB transfer (FREE)

### After Free Tier:
- **Light usage**: ~$5-10/month
- **Moderate usage**: ~$10-20/month

### Google Gemini API:
- **Free tier**: 15 requests/minute, 1,500 requests/day
- **Paid**: $0.001 per 1,000 characters

## Testing Your Deployment

1. **Test the API directly**:
```powershell
# Test health endpoint
curl https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod/health

# Test sample analysis
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod/api/analyze/sample
```

2. **Test the full website**:
   - Open the CloudFront URL in your browser
   - Try the sample resume analysis
   - Upload and analyze your own resume

## Troubleshooting 🔧

**Common Issues:**

1. **API Key errors**: Make sure your Google Gemini API key is correct
2. **CORS errors**: Check that the API Gateway CORS is configured
3. **Build errors**: Ensure all dependencies are installed
4. **Permission errors**: Verify your AWS credentials have proper permissions

**Useful Commands:**

```powershell
# View deployment logs
sam logs -n ResumeAnalyzerFunction --stack-name resume-analyzer-serverless --tail

# Update just the Lambda function
sam deploy

# Delete the entire stack
sam delete --stack-name resume-analyzer-serverless
```

## Security Best Practices 🔐

- Never commit API keys to Git
- Use environment variables for secrets
- Enable CloudTrail for audit logging
- Set up billing alerts in AWS Console
- Regularly rotate API keys

## Scaling & Monitoring 📊

- **CloudWatch**: Monitor Lambda performance and errors
- **X-Ray**: Trace requests for debugging
- **Cost Explorer**: Track AWS spending
- **Budgets**: Set spending alerts

Your resume analyzer will be live at a professional URL and can handle thousands of users! 🚀
