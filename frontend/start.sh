#!/bin/bash
# Frontend startup script for macOS/Linux

echo "Installing dependencies..."
npm install

echo ""
echo "Starting development server..."
npm run dev
