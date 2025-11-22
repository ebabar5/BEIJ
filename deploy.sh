#!/bin/bash

# BEIJ Backend Deployment Script
# This script builds and deploys the BEIJ e-commerce backend

set -e  # Exit on any error

echo "🚀 Starting BEIJ Backend Deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build the backend image
echo "🔨 Building backend Docker image..."
docker-compose build backend

# Start the services
echo "🏃 Starting services..."
docker-compose up -d backend

# Wait for backend to be healthy
echo "⏳ Waiting for backend to be ready..."
timeout=60
counter=0

while [ $counter -lt $timeout ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy and ready!"
        break
    fi
    echo "⏳ Waiting for backend... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

if [ $counter -ge $timeout ]; then
    echo "❌ Backend failed to start within $timeout seconds"
    docker-compose logs backend
    exit 1
fi

# Show running containers
echo "📊 Running containers:"
docker-compose ps

# Show logs
echo "📝 Recent logs:"
docker-compose logs --tail=20 backend

echo "🎉 Deployment complete!"
echo "📍 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
