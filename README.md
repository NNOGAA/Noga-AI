# Noga AI - Unified API

API untuk analisis nutrisi makanan menggunakan OCR + Google Gemini AI. Service ini menggabungkan OCR ingredients, nutrition facts, AI summary, dan validation dalam satu API.

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Copy dan edit .env file
cp .env.example .env

# Install dependencies
pip install -r requirements.txt
```

### 2. Jalankan Server

```bash
# Development
python main.py

# Production
uvicorn main:app --host 0.0.0.0 --port 8080
```

> **Note:** Database table akan otomatis dibuat saat pertama kali server dijalankan.

### 3. Akses API Docs

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## 🐳 Docker

```bash
docker build -t noga-ai .
docker run -p 8080:8080 --env-file .env noga-ai
```

> **Note:** Docker dan deployment otomatis setup database via `init_db.py` saat startup.

## 📡 API Endpoints

| Endpoint              | Method | Deskripsi                                   |
| --------------------- | ------ | ------------------------------------------- |
| `/ocr-ingredients`    | POST   | Extract ingredients dari foto label makanan |
| `/ocr-nutrition-info` | POST   | Extract nutrition facts dari foto label     |
| `/summary_foods`      | POST   | Generate AI summary & health analysis       |
| `/validate-fix-typo`  | POST   | Validasi dan perbaiki typo otomatis         |

## 📝 Contoh Request

### Extract Ingredients

```json
POST /ocr-ingredients
{
  "session_id": "user123",
  "composition": "https://example.com/image.jpg"
}
```

### Extract Nutrition Info

```json
POST /ocr-nutrition-info
{
  "session_id": "user123",
  "nutrition_info": "https://example.com/nutrition.jpg"
}
```

### Generate Summary

```json
POST /summary_foods
{
  "ingredients": [
    {"nama": "Sugar", "status": "bad", "detail": "High in empty calories"}
  ],
  "nutrition_info": [
    {"nama": "Calories", "nilai": 250, "type": "kilocalorie", "status": "neutral"}
  ]
}
```

## ⚙️ Environment Variables

```env
DB_HOST=your_mysql_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
GOOGLE_API_KEY=your_gemini_api_key
PORT=8080
```

## 🏗️ Tech Stack

- **FastAPI** - Web framework
- **Google Gemini AI** (2.0-flash) - OCR & AI processing
- **MySQL** - Database untuk menyimpan hasil OCR
- **Uvicorn** - ASGI server

## 📦 Struktur Proyek

```
Noga-AI/
├── main.py              # FastAPI app & routing
├── handlers/            # Business logic per endpoint
├── functions/           # OCR & AI utilities
├── schemas/             # Pydantic models
├── db/                  # Database connection
└── models/              # Health classification data
```
