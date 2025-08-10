# 🎭 Sentiment Analyzer (Mistral)

A modern AI-powered sentiment analysis application that uses the **Mistral language model** via Ollama to classify text sentiment as Positive, Negative, or Neutral.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-FF7000?style=flat)

## ✨ Features

- **🚀 Fast Analysis**: Real-time sentiment classification using Mistral AI
- **🎨 Modern UI**: Beautiful Streamlit frontend with custom styling
- **🔧 Robust Backend**: FastAPI backend with error handling and health checks
- **📊 Detailed Results**: Processing time, confidence scores, and analysis details
- **💡 Sample Texts**: Built-in examples to test different sentiment types
- **🔍 System Monitoring**: Health check dashboard for system status

## 📁 Project Files

```
sentiment-analyzer-mistral/
│
├── backend/
│   └── main.py              # FastAPI backend server
│
├── frontend/
│   └── app.py              # Streamlit frontend application
│
├── requirements.txt         # Python dependencies
├── test_setup.py           # Setup verification script
├── start_app.py            # Cross-platform startup script
├── start_app.bat           # Windows batch file (Windows only)
├── README.md               # Documentation
└── .gitignore             # Git ignore rules
```
## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Git (for version control)

### Installation & Setup

1. **Create project directory and files**
   ```bash
   mkdir sentiment-analyzer-mistral
   cd sentiment-analyzer-mistral
   mkdir backend frontend
   ```

2. **Create all the project files** (copy the code from the artifacts above):
   - `backend/main.py` (FastAPI Backend)
   - `frontend/app.py` (Streamlit Frontend) 
   - `requirements.txt`
   - `test_setup.py` (Test script)
   - `start_app.py` (Startup script)

3. **Set up Python environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

4. **Set up Ollama and Mistral**
   ```bash
   # Make sure Ollama is running
   ollama serve
   
   # Pull the Mistral model
   ollama pull mistral
   ```

5. **Test your setup**
   ```bash
   python test_setup.py
   ```

6. **Run the application**
   
   **Option A: Windows Batch File (Windows Only)**
   ```cmd
   start_app.bat
   ```
   
   **Option B: Python Startup Script (Cross-Platform)**
   ```bash
   python start_app.py
   ```
   
   **Option C: Manual startup (Two terminals)**
   ```bash
   # Terminal 1 - Backend
   uvicorn backend.main:app --reload
   
   # Terminal 2 - Frontend  
   streamlit run frontend/app.py
   ```

7. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000/docs

## 🎯 Usage

1. **Enter Text**: Type or paste your text in the input area
2. **Analyze**: Click the "Analyze Sentiment" button
3. **View Results**: Get instant sentiment classification with detailed analysis
4. **Try Samples**: Use built-in sample texts to test different sentiment types

### Example Inputs

- **Positive**: "I absolutely love this new product! It works perfectly."
- **Negative**: "This service is terrible and I'm very disappointed."
- **Neutral**: "The meeting is scheduled for 2 PM tomorrow in room B."

## 🔧 API Endpoints

### POST `/analyze/`
Analyze the sentiment of provided text.

**Request Body:**
```json
{
  "text": "Your text here"
}
```

**Response:**
```json
{
  "sentiment": "Positive",
  "text": "Your text here",
  "raw_response": "Positive"
}
```

### GET `/health/`
Check system health and Ollama connection status.

**Response:**
```json
{
  "api_status": "healthy",
  "ollama_status": "connected",
  "mistral_available": true
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"Cannot connect to Ollama service"**
   - Ensure Ollama is running: `ollama serve`
   - Check if Mistral model is available: `ollama list`
   - Pull the model if missing: `ollama pull mistral`

2. **"Cannot connect to backend API"**
   - Verify the FastAPI server is running on port 8000
   - Check firewall settings
   - Try: `curl http://localhost:8000/health/`

3. **Streamlit connection errors**
   - Ensure backend is running first
   - Check if port 8501 is available
   - Try refreshing the browser page

### Performance Tips

- For faster responses, keep Ollama running in the background
- The first analysis may take longer as the model loads
- Consider using a GPU for better performance with larger texts

## 🛠️ Development

### Project Structure

- `backend/main.py`: FastAPI application with sentiment analysis endpoints
- `frontend/app.py`: Streamlit web interface with custom styling
- `requirements.txt`: Python package dependencies

### Running in Development Mode

```bash
# Backend with auto-reload
uvicorn backend.main:app --reload

# Frontend with auto-reload (automatic)
streamlit run frontend/app.py
```

### Adding Features

1. **Custom Models**: Modify the model name in `backend/main.py`
2. **Additional Analysis**: Add new endpoints for different NLP tasks
3. **UI Improvements**: Customize CSS in `frontend/app.py`

## 📦 Deployment

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000 8501

# You'll need to run Ollama separately
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501"]
```

### Cloud Deployment

For cloud deployment, you'll need to:
1. Set up Ollama on a server with sufficient resources
2. Configure proper networking and security
3. Use environment variables for configuration
4. Consider using container orchestration (Kubernetes, Docker Swarm)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Mistral AI](https://mistral.ai/) for the language model
- [Ollama](https://ollama.ai/) for local model hosting
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Streamlit](https://streamlit.io/) for the frontend framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Open an issue on GitHub
3. Review the API documentation at http://localhost:8000/docs

## 📁 Screenshots

![Description](<img width="946" height="913" alt="476355966-258aa885-51a9-4778-833e-9635329950a3" src="https://github.com/user-attachments/assets/de893ade-66b2-4468-9f0b-583819200962" />)
![Description](https://private-user-images.githubusercontent.com/33010011/476355964-69f00ee5-01f3-4b23-8807-ecb22aa53575.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ4MzEzMjUsIm5iZiI6MTc1NDgzMTAyNSwicGF0aCI6Ii8zMzAxMDAxMS80NzYzNTU5NjQtNjlmMDBlZTUtMDFmMy00YjIzLTg4MDctZWNiMjJhYTUzNTc1LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEwVDEzMDM0NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTMxNjc3MzI0NGMzMzRlZmZiMTE4MTU1MWU3MDY0MTIzODUxOTc2NzY4YmFjMGJhYzQwMmU3ZjZlNTliYTE5ZDQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.FrAuV37QDbfSg9o1vBbt372UUnhK0yqV_08PNvwoc-4)
![Description](https://private-user-images.githubusercontent.com/33010011/476355966-258aa885-51a9-4778-833e-9635329950a3.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ4MzEzMjUsIm5iZiI6MTc1NDgzMTAyNSwicGF0aCI6Ii8zMzAxMDAxMS80NzYzNTU5NjYtMjU4YWE4ODUtNTFhOS00Nzc4LTgzM2UtOTYzNTMyOTk1MGEzLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEwVDEzMDM0NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTA1NTJhZjE5ZjMxOWNkMWZkMzljZWMxZDViMGU2MjNiMWViOWNhZjY5M2I1ZjI1N2EwYjgwYWNmYTYzN2RiMWEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.LLoXiBaeuLbeuKvAfWj6tBtHxtZ93Hov1K_lN1lkm3k)
---


**Happy Analyzing! 🎭✨**

