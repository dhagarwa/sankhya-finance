#!/bin/bash

# Sankhya Finance - Google Cloud Run Deployment Script

set -e

# Configuration
PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
SERVICE_NAME="sankhya-finance-api"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying Sankhya Finance API to Google Cloud Run"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo "======================================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Authenticate with gcloud (if needed)
echo "🔐 Checking gcloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔑 Please authenticate with gcloud:"
    gcloud auth login
fi

# Set the project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Configure Docker for gcloud
echo "🐳 Configuring Docker for gcloud..."
gcloud auth configure-docker

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME .

# Push the image to Google Container Registry
echo "📤 Pushing image to Google Container Registry..."
docker push $IMAGE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars ENV=production \
    --timeout 300

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")

echo ""
echo "🎉 Deployment completed successfully!"
echo "======================================================"
echo "Service URL: $SERVICE_URL"
echo "Health Check: $SERVICE_URL/health"
echo "API Documentation: $SERVICE_URL/docs"
echo ""
echo "To test the API:"
echo "curl -X POST '$SERVICE_URL/analyze' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"query\": \"What is Apple's current stock price?\"}'"
echo ""
echo "🔧 To update environment variables:"
echo "gcloud run services update $SERVICE_NAME --region $REGION --set-env-vars OPENAI_API_KEY=your_key_here"
echo ""
echo "📊 To view logs:"
echo "gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME' --limit 50 --format json" 