Load Checker API
FastAPI service for load verification and carrier validation, built for HappyRobot's carrier sales operations.
Features

Load details retrieval by reference number
Carrier validation using FMCSA API
Redis caching for improved performance
Rate limiting and API key authentication
Docker containerization

Live Demo

API Endpoint: http://54.165.86.20:8000
API Documentation: http://54.165.86.20:8000/docs

Local Development

Clone and setup:

bashCopygit clone https://github.com/cbrahmam/happyrobot.git
cd happyrobot
cp .env.example .env  # Add your API keys

Run with Docker:

bashCopydocker-compose up -d
API Endpoints
GET /loads/{reference_number}
Retrieve load details by reference number.
GET /carriers/validate
Validate carrier using MC number.
Environment Setup
Required environment variables in .env:

API_KEY: For API authentication
FMCSA_API_KEY: For carrier validation
REDIS_URL: Redis connection string