# Book Warden API

A FastAPI-based book management system demonstrating clean architecture patterns and comprehensive testing strategies.

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Installation

1. Clone the repository and navigate to the API directory:
```bash
git clone <repository-url>
cd book_warden/api
```

2. Install dependencies:
```bash
make install
```

3. Create environment file:
```bash
cp .env.example .env
```
Edit `.env` with your configuration values if needed.

### Running the Application

Start the development server:
```bash
make dev
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

### Available Commands

```bash
make dev      # Start development server
make test     # Run all tests
make lint     # Run code linting
make install  # Install dependencies
make clean    # Clean cache files
```

## API Endpoints

### Books

- `GET /api/v1/books` - List all books
- `POST /api/v1/books` - Create a new book
- `GET /api/v1/books/{id}` - Get a specific book
- `PUT /api/v1/books/{id}` - Update a book
- `DELETE /api/v1/books/{id}` - Delete a book

## Testing

Run the complete test suite:
```bash
make test
```

The project includes 51+ tests covering:
- API integration tests
- Repository layer tests
- Service layer tests
- Validation tests

## Project Structure

```
api/
├── apps/
│   ├── books/          # Book domain logic
│   │   ├── models.py   # Data models
│   │   ├── dtos.py     # Data transfer objects
│   │   ├── repositories.py  # Data access layer
│   │   ├── services.py # Business logic layer
│   │   └── routes.py   # API endpoints
│   ├── exceptions.py   # Custom exceptions
│   └── validators.py   # Input validation
├── config/
│   ├── settings.py     # Application configuration
│   └── logging.py      # Logging configuration
├── db/
│   └── setup.py        # Database initialization
├── tests/              # Test suite
├── main.py             # FastAPI application
└── Makefile            # Development commands
```

## Architecture

The application follows clean architecture principles:

- **Repository Pattern**: Abstracts data access logic
- **Service Layer**: Contains business logic
- **Dependency Injection**: Uses FastAPI's dependency system
- **Exception Handling**: Custom business rule exceptions
- **Validation**: Pydantic models for request/response validation

