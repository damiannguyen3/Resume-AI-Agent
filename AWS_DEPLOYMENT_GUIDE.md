# Resume SEO Analyzer - AWS Serverless Deployment

## Prerequisites

1. **AWS Account**: Sign up at [aws.amazon.com](https://aws.amazon.com) (free tier available)
2. **AWS CLI**: Install and configure with your credentials
3. **SAM CLI**: Install AWS SAM CLI for serverless deployment
4. **OpenAI API Key**: Get one from [platform.openai.com](https://platform.openai.com)

## Cost Estimate

### Free Tier (First 12 months):
- **Lambda**: 1M requests/month (FREE)
- **API Gateway**: 1M calls/month (FREE)
- **S3**: 5GB storage + 20K requests (FREE)
- **CloudFront**: 50GB transfer + 2M requests (FREE)

### After Free Tier:
- **Typical monthly cost**: $5-15 for moderate usage
- **High traffic**: Could scale to $20-50/month

## Deployment Steps

### Step 1: Install AWS CLI and SAM CLI

```powershell
# Install AWS CLI
winget install Amazon.AWSCLI

# Install SAM CLI
winget install Amazon.SAM-CLI

# Or download from:
# https://aws.amazon.com/cli/
# https://aws.amazon.com/serverless/sam/
```

### Step 2: Configure AWS Credentials

```powershell
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter default region (e.g., us-east-1)
# Enter default output format (json)
```

### Step 3: Deploy the Backend

```powershell
# Navigate to the project directory
cd "c:\Users\Damian\AI Agent"

# Build the SAM application
sam build

# Deploy with guided setup (first time)
sam deploy --guided

# You'll be prompted for:
# - Stack name: resume-analyzer
# - AWS Region: us-east-1 (or your preferred region)
# - OpenAI API Key: your_openai_api_key_here
# - Confirm changes: Y
# - Allow SAM to create IAM roles: Y
```

### Step 4: Update Frontend API URL

After deployment, SAM will output an API Gateway URL. Update your React app:

1. Create a `.env.production` file in your React app:
```
REACT_APP_API_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod
```

2. Build the React app:
```powershell
cd "c:\Users\Damian\AI Agent\resume-analyzer-web"
npm run build
```

### Step 5: Deploy Frontend to S3

```powershell
# Upload the built React app to S3
aws s3 sync build/ s3://resume-analyzer-website --delete

# Enable website hosting
aws s3 website s3://resume-analyzer-website --index-document index.html --error-document index.html
```

### Step 6: Get Your Website URL

```powershell
# Get the CloudFront URL (your final website URL)
aws cloudformation describe-stacks --stack-name resume-analyzer --query 'Stacks[0].Outputs'
```

## Alternative: One-Click Deploy

If you prefer a simpler approach, you can also use:

### Option A: Vercel (Recommended for simplicity)
- Connect your GitHub repo to Vercel
- Add OpenAI API key in environment variables
- Deploy with one click
- Cost: Free for hobby projects

### Option B: Netlify + Railway
- Frontend on Netlify (free)
- Backend on Railway (free tier available)
- Easy GitHub integration

### Option C: AWS Amplify
- Full-stack deployment in one service
- GitHub integration
- Free tier available

## Monitoring and Costs

Once deployed, monitor your usage in the AWS Console:
- **CloudWatch**: View logs and metrics
- **Cost Explorer**: Track spending
- **AWS Budgets**: Set up cost alerts

## Security Notes

- Never commit API keys to Git
- Use environment variables for secrets
- Enable CloudTrail for audit logging
- Set up billing alerts

Your website will be live at a URL like: `https://d1234567890.cloudfront.net`

## Troubleshooting

Common issues and solutions:

1. **CORS errors**: Check API Gateway CORS settings
2. **404 errors**: Ensure CloudFront error pages redirect to index.html
3. **API timeouts**: Check Lambda timeout settings (max 15 minutes)
4. **High costs**: Monitor CloudWatch logs and set billing alerts
