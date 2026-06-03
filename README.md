# Lexora — Invoice OCR Processing API
 
> Intelligent backend for automated invoice processing using computer vision, OCR, and AI-powered data extraction.
 
Lexora is a REST API built with **FastAPI** that takes a photo or scan of an invoice, preprocesses the image, extracts text via OCR, and uses a large language model to structure the data into a normalized JSON response — ready for storage, review, and export.
 
---
 
## Key Features
 
- **Image preprocessing pipeline** — resize, grayscale, shadow removal, sharpening, and deskew using OpenCV
- **OCR extraction** — text detection with EasyOCR including spatial row reconstruction from bounding box coordinates
- **AI-powered structuring** — Gemini LLM extracts invoice fields with per-field confidence scores
- **Document storage** — original invoice images uploaded to Cloudinary with URL persisted per invoice
- **Export** — invoices exportable as PDF (ReportLab), XML (UBL 2.1 structure), and CSV
- **Authentication** — JWT-based auth with OAuth2 password flow, bcrypt password hashing
- **Audit logging** — every CREATE, UPDATE, and DELETE operation is recorded with user and entity context
- **Clean architecture** — repository pattern, service interfaces, dependency injection via FastAPI's DI system
---
 
## Tech Stack
 
| Layer | Technology |
|---|---|
| Framework | FastAPI 0.136 + Uvicorn |
| ORM | SQLModel + SQLAlchemy 2.0 |
| Database | PostgreSQL (via psycopg3) |
| OCR | EasyOCR 1.7 (PyTorch-backed) |
| Image Processing | OpenCV 4.13 |
| AI Extraction | Google Gemini (google-genai 2.2) |
| Auth | python-jose (JWT) + passlib (bcrypt) |
| File Storage | Cloudinary |
| PDF Export | ReportLab |
| Validation | Pydantic v2 |
 
---
 
## Architecture
 
```
┌─────────────────────────────────────────────────────┐
│                    FastAPI Routers                   │
│  /auth  /invoices  /users  /parties  /audit-logs    │
└─────────────────┬───────────────────────────────────┘
                  │ Depends()
┌─────────────────▼───────────────────────────────────┐
│                  Service Layer                       │
│  InvoiceService · UserService · PartyService · ...  │
└────────┬───────────────────┬────────────────────────┘
         │                   │
┌────────▼──────┐   ┌────────▼────────────────────────┐
│  Repositories │   │        InvoiceOrchestrator       │
│  (SQLModel)   │   │                                  │
└────────┬──────┘   │  ImagePreprocessor               │
         │          │      → OCRProcessor (EasyOCR)    │
┌────────▼──────┐   │          → LLMExtractor (Gemini) │
│  PostgreSQL   │   └─────────────────────────────────┘
└───────────────┘
```
 
### Key Design Decisions
 
**Orchestrator pattern** — the invoice processing pipeline (preprocess → OCR → LLM) is coordinated by a dedicated `InvoiceOrchestrator` class, keeping the service layer clean and each processing module independently testable.
 
**Interface-driven services** — every service implements an abstract interface (`InvoiceServiceInterface`, `UserServiceInterface`, etc.), decoupling the router from the implementation and making the codebase easy to extend or swap out.
 
**Dependency injection everywhere** — FastAPI's `Depends()` system is used throughout: repositories, services, the orchestrator, JWT service, and current user are all injected, never instantiated inside business logic.
 
**EasyOCR model loaded once at startup** — OCR model initialization is expensive (~5s). The `lifespan` event loads the EasyOCR reader once into `app.state` and reuses it across all requests, avoiding per-request overhead.
 
**Row reconstruction from bounding boxes** — EasyOCR returns individual text blocks with pixel coordinates. A custom `_reconstruct_rows` method groups detections by Y-coordinate proximity and sorts by X to reconstruct the original tabular structure of the invoice before passing it to the LLM.
 
**Per-field confidence scores** — the Gemini prompt instructs the model to return a `confidence` value (0.0–1.0) alongside every extracted field. This is surfaced to the frontend so users know which fields to review carefully before saving.
 
**Cascade deletes** — `Invoice` → `InvoiceItem`, `Document`, and `ExtractedField` all use `cascade: all, delete-orphan` so deleting an invoice cleans up all related records atomically.
 
---
 
## Project Structure
 
```
app/
├── api/
│   ├── deps/           # FastAPI dependency factories
│   └── routes/         # Routers (invoice, user, auth, party, audit)
├── auth/               # JWT service, auth service, dependencies
├── enums/              # AuditAction, AuditEntity, PartyType
├── infrastructure/     # Database engine
├── models/             # SQLModel table definitions
├── modules/
│   ├── image_processing/   # OpenCV preprocessing pipeline
│   ├── ocr_processing/     # EasyOCR + row reconstruction
│   └── llm_extractor/      # Gemini prompt + response parsing
├── orchestator/        # InvoiceOrchestrator
├── repositories/       # Data access layer
├── schemas/
│   ├── requests/       # Pydantic input models
│   └── responses/      # Pydantic output models
├── services/
│   ├── interfaces/     # Abstract base classes
│   └── *.py            # Service implementations
├── utils/              # password_hasher, cloudinary_utils
└── main.py             # App factory, lifespan, middleware
```
 
---
 
## API Endpoints
 
### Auth (public)
| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user, returns JWT |
| POST | `/auth/login` | Login with email/password, returns JWT |
 
### Invoices (authenticated)
| Method | Path | Description |
|---|---|---|
| POST | `/invoices/process` | Upload invoice image → preprocess → OCR → LLM extraction |
| POST | `/invoices/save` | Save structured invoice data to database |
| GET | `/invoices/` | List authenticated user's invoices |
| GET | `/invoices/{id}` | Get invoice by ID |
| PATCH | `/invoices/{id}` | Update invoice fields and items |
| PATCH | `/invoices/{id}/status` | Transition invoice status |
| DELETE | `/invoices/{id}` | Delete invoice and all related data |
| GET | `/invoices/by-date` | Filter by issue date range |
| GET | `/invoices/provider/{id}` | Filter by provider |
| GET | `/invoices/category/{cat}` | Filter by category |
| GET | `/invoices/status/{status}` | Filter by status |
| GET | `/invoices/{id}/export/pdf` | Export as PDF |
| GET | `/invoices/{id}/export/xml` | Export as XML (UBL 2.1 structure) |
| GET | `/invoices/{id}/export/csv` | Export as CSV |
 
### Users (authenticated)
| Method | Path | Description |
|---|---|---|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update profile |
| DELETE | `/users/me` | Delete account |
 
### Parties, Audit Logs (authenticated)
Full CRUD for providers/clients and read-only audit log access with filters.
 
---
 
## Getting Started
 
### Prerequisites
 
- Python 3.11+
- PostgreSQL instance
- Tesseract OCR installed (not required — EasyOCR is used instead)
- Cloudinary account
- Google AI Studio API key (Gemini)
### 1. Clone and install
 
```bash
git clone https://github.com/your-username/lexora-backend.git
cd lexora-backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```
 
> **Note:** EasyOCR will download its model weights (~100MB) on first run. Ensure you have internet access.
 
### 2. Configure environment variables
 
Create a `.env` file in the project root:
 
```env
# Database
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=lexora
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
 
# Auth
SECRET_KEY=your_secret_key_here        # generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=30
 
# Gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash
 
# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
```
 
### 3. Set up the database
 
Create the database in PostgreSQL, then run the application once to let SQLModel create all tables automatically on startup:
 
```bash
# Tables are created automatically via SQLModel metadata on first run
uvicorn app.main:app --reload
```
 
### 4. Run the application
 
```bash
uvicorn app.main:app --reload
```
 
The API will be available at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Landing:** `http://localhost:8000/`
---
 
## Invoice Processing Flow
 
```
1. POST /invoices/process (multipart image upload)
        │
        ├── Upload original image → Cloudinary
        │
        └── ImagePreprocessor
              resize → grayscale → denoise → shadow removal → sharpen → deskew
                    │
                    └── OCRProcessor (EasyOCR)
                          detect text blocks → reconstruct rows by Y-coordinate
                                │
                                └── LLMExtractor (Gemini)
                                      structured JSON with per-field confidence scores
                                            │
                                            └── Response to client
 
2. User reviews and corrects extracted data in frontend
 
3. POST /invoices/save
        saves Invoice + Items + ExtractedFields + Document to PostgreSQL
```
 
---
 
## Skills Demonstrated
 
- **FastAPI** — async endpoints, dependency injection, lifespan events, OAuth2, response models, router-level middleware
- **Computer Vision** — OpenCV image preprocessing: adaptive thresholding, morphological operations, Hough line transform for deskew, shadow normalization
- **OCR** — EasyOCR integration, bounding box processing, spatial text reconstruction
- **LLM Integration** — structured prompt engineering, JSON extraction, confidence scoring, error handling for external API failures
- **Clean Architecture** — repository pattern, service interfaces, separation of concerns across 6+ layers
- **Security** — JWT authentication, bcrypt password hashing, per-resource ownership validation, router-level auth guards
- **PostgreSQL** — relational modeling, foreign keys, cascade deletes, eager loading with `selectinload`
- **Pydantic v2** — request/response validation, `ConfigDict`, schema separation between input and output models
- **Third-party integrations** — Cloudinary (file storage), Google Gemini (AI), ReportLab (PDF), UBL XML
---
 
## Future Improvements
 
- Database migrations with Alembic
- Asynchronous invoice processing with background tasks (FastAPI `BackgroundTasks` or Celery)
- GPU support for EasyOCR to reduce processing time from ~15s to ~2s
- Document perspective correction for photos taken at an angle
- Role-based access control (admin vs regular user)
- Rate limiting on the `/process` endpoint
---

## Frontend

Lexora Frontend → [Click here](https://github.com/Lord-Jospe/lexora-frontend)
