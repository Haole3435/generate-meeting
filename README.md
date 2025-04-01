# Meeting Minutes Generator (generate-meeting)

An application that automatically generates meeting minutes from audio files or text, using AI to analyze and summarize content.

## System Architecture

### 1. Frontend (Streamlit)
- Simple and intuitive user interface
- Support for audio and text file uploads
- Display results and enable Word file downloads

### 2. Backend (FastAPI)
- Handle frontend requests
- Manage file uploads and downloads
- Coordinate data processing flow

### 3. Core Processing
- **Audio Processing**: Convert audio files to WAV format
- **Transcription**: Use OpenAI Whisper to convert speech to text
- **Text Analysis**: Use GPT-4 to analyze and summarize text
  - Generate abstract summary
  - Extract key points
  - Identify action items
  - Analyze sentiment

### 4. Output Generation
- Create well-structured Word documents
- Include all analysis sections
- Professional and readable formatting

## System Requirements

- Python 3.10 or higher
- FFmpeg (for audio processing)
- OpenAI API key
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Local Installation

1. Clone repository:
```bash
git clone <repository-url>
cd generate-meeting
```

2. Create and activate virtual environment:
```bash
conda create -n generate-meeting python=3.10
conda activate generate-meeting
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
- Windows: Download and install from [FFmpeg website](https://ffmpeg.org/download.html)
- Linux: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

5. Create `.env` file in root directory:
```env
OPENAI_API_KEY=your_api_key_here
```

### Option 2: Docker Installation

1. Build Docker images:
```bash
# Build backend image
docker build -t generate-meeting-backend -f docker/backend.Dockerfile .

# Build frontend image
docker build -t generate-meeting-frontend -f docker/frontend.Dockerfile .
```

2. Create a Docker network:
```bash
docker network create generate-meeting-network
```

3. Run the containers:
```bash
# Run backend container
docker run -d \
  --name generate-meeting-backend \
  --network generate-meeting-network \
  -p 8000:8000 \
  -v $(pwd)/outputs:/app/outputs \
  --env-file .env \
  generate-meeting-backend

# Run frontend container
docker run -d \
  --name generate-meeting-frontend \
  --network generate-meeting-network \
  -p 8501:8501 \
  -e BACKEND_URL=http://generate-meeting-backend:8000 \
  generate-meeting-frontend
```

4. Or use Docker Compose (recommended):
```bash
docker-compose up -d
```

## Directory Structure

```
generate-meeting/
├── app/
│   ├── backend/
│   │   └── main.py
│   ├── core/
│   │   ├── chains.py
│   │   ├── models.py
│   │   └── processing.py
│   ├── frontend/
│   │   └── main.py
│   └── schemas/
│       └── model.py
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── docker-compose.yml
├── outputs/
├── requirements.txt
└── .env
```

## Running the Application

### Option 1: Local Development

1. Start backend server:
```bash
cd app/backend
uvicorn main:app --reload
```

2. Start frontend:
```bash
cd app/frontend
streamlit run main.py
```

3. Access the application:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

### Option 2: Docker Deployment

1. Access the application:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

2. View container logs:
```bash
# View backend logs
docker logs generate-meeting-backend

# View frontend logs
docker logs generate-meeting-frontend
```

3. Stop the containers:
```bash
# Using Docker Compose
docker-compose down

# Or manually
docker stop generate-meeting-frontend generate-meeting-backend
docker rm generate-meeting-frontend generate-meeting-backend
```

## Usage

1. Open browser and navigate to http://localhost:8501
2. Select input type (Audio or Text)
3. Upload file or enter text
4. Click "Generate Minutes"
5. Wait for processing to complete
6. Download the Word file containing the minutes

## Features

- Speech-to-text conversion
- Automatic summarization
- Key points extraction
- Action items identification
- Sentiment analysis
- Professional Word document export

## Important Notes

- Ensure sufficient disk space for file processing
- Audio files should be of good quality for accurate results
- Stable internet connection required for OpenAI API usage
- When using Docker, ensure proper volume mounting for persistent storage
- Docker containers require proper network configuration for inter-service communication

