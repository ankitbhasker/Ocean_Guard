#!/bin/bash

echo "⚛️ Starting Ocean Hazard Platform Frontend..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "Installing dependencies..."
yarn install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
fi

# Start the frontend development server
echo "Starting React development server..."
yarn start
