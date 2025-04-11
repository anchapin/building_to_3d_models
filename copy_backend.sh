#!/bin/bash

# Create deployment directory
DEPLOY_DIR="./deployment"
mkdir -p $DEPLOY_DIR/api

# Copy backend modules to deployment directory
cp -r backend/image_processing $DEPLOY_DIR/api/
cp -r backend/reconstruction $DEPLOY_DIR/api/
cp -r backend/gbxml $DEPLOY_DIR/api/

echo "Backend modules copied to deployment directory"
