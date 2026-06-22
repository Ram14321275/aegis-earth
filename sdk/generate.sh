#!/bin/bash
set -e

echo "Generating Aegis Earth Public SDKs..."

# 1. Dump the OpenAPI schema
cd ../backend
python scripts/dump_openapi.py
cd ../sdk

# 2. Setup output directories
mkdir -p typescript
mkdir -p python

# 3. Generate TypeScript SDK
echo "Generating TypeScript SDK..."
npx @openapitools/openapi-generator-cli generate \
    -i ../backend/openapi.json \
    -g typescript-fetch \
    -o ./typescript \
    --additional-properties=supportsES6=true,typescriptThreePlus=true

# 4. Generate Python SDK
echo "Generating Python SDK..."
npx @openapitools/openapi-generator-cli generate \
    -i ../backend/openapi.json \
    -g python \
    -o ./python \
    --additional-properties=packageName=aegis_earth_sdk

echo "SDK generation complete."
