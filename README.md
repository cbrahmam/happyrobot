<<<<<<< HEAD
<<<<<<< HEAD
=======
To copy code blocks in GitHub or similar interfaces, you can click the copy button (📋 icon) that appears in the top-right corner of each code block. But let me give you the text in an easily copyable format:

```markdown
>>>>>>> b26ec9e (Initial commit - clean repository)
=======
>>>>>>> f64b855 (dd)
# Load Checker API

FastAPI service for load verification and carrier validation, built for HappyRobot's carrier sales operations.

## Features
* Load details retrieval by reference number
* Carrier validation using FMCSA API
* Redis caching for improved performance
* Rate limiting and API key authentication
* Docker containerization

## Live Demo
<<<<<<< HEAD
* API Endpoint: http://54.165.86.20:80
* API Documentation: http://54.165.86.20:80/docs
=======
* API Endpoint: http://54.165.86.20:8000
* API Documentation: http://54.165.86.20:8000/docs
>>>>>>> b26ec9e (Initial commit - clean repository)

## Local Development

1. Clone and setup:
```bash
git clone https://github.com/cbrahmam/happyrobot.git
cd happyrobot
<<<<<<< HEAD
cp .env  # Add your API keys
=======
cp .env.example .env  # Add your API keys
>>>>>>> b26ec9e (Initial commit - clean repository)
```

2. Run with Docker:
```bash
docker-compose up -d
```

## API Endpoints

### GET /loads/{reference_number}
Retrieve load details by reference number.

### GET /carriers/validate
Validate carrier using MC number.

## Environment Setup
Required environment variables in `.env`:
* API_KEY: For API authentication
* FMCSA_API_KEY: For carrier validation
* REDIS_URL: Redis connection string
<<<<<<< HEAD
=======
```
>>>>>>> b26ec9e (Initial commit - clean repository)
