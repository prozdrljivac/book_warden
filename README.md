# Book Warden

## Description

Small book inventory app with two goals:

1. Learning about Repository Pattern
2. Trying out FastAPI

## Documents

[API Information and Setup Guide](/api/README.md)

## Practice Tasks - Python & Software Engineering

### Task 1: Add Service Layer (Architecture Pattern)
**Goal:** Learn layered architecture and separation of concerns
- [ ] Create `services/book_service.py` 
- [ ] Move business logic from routes to service layer
- [ ] Implement dependency injection for service in routes
- [ ] Add transaction management and error handling

### Task 2: Implement Connection Pool Pattern
**Goal:** Learn resource management and performance optimization  
- [ ] Replace individual DB connections with connection pool
- [ ] Create database context manager
- [ ] Add connection timeout and retry logic
- [ ] Measure performance improvement

### Task 3: Add Custom Exception Handling
**Goal:** Practice error handling and HTTP status codes
- [ ] Create `exceptions.py` with custom exception classes
- [ ] Add FastAPI exception handlers
- [ ] Implement proper HTTP status code mapping
- [ ] Add error response DTOs

### Task 4: Implement Factory Pattern for DTOs
**Goal:** Reduce code duplication using design patterns
- [ ] Remove duplicate DTO classes (GetBookResponseDto/ListBookResponseDto)
- [ ] Create DTO factory with builder methods
- [ ] Add validation logic in factory

### Task 5: Add Query Builder Pattern
**Goal:** Practice builder pattern and SQL safety
- [ ] Create `QueryBuilder` class for dynamic SQL construction
- [ ] Replace string concatenation in `update_book` method
- [ ] Add support for filtering and sorting
- [ ] Implement proper SQL injection protection

### Task 6: Implement Caching with LRU Algorithm
**Goal:** Learn caching strategies and algorithms
- [ ] Add LRU cache for book retrieval
- [ ] Implement cache invalidation on updates/deletes
- [ ] Add cache statistics endpoint
- [ ] Compare performance with/without cache

### Task 7: Add Search Functionality with Trie Data Structure
**Goal:** Practice advanced data structures
- [ ] Implement Trie for book title/author search
- [ ] Add search endpoint with autocomplete
- [ ] Compare Trie vs database LIKE queries performance
- [ ] Add fuzzy search capability

### Task 8: Implement Repository Interface (Strategy Pattern)
**Goal:** Learn abstraction and testability
- [ ] Create `IBookRepository` abstract base class
- [ ] Implement `SQLiteBookRepository` and `InMemoryBookRepository`
- [ ] Add repository factory for switching implementations
- [ ] Write unit tests using in-memory repository

### Task 9: Add Validation Pipeline (Chain of Responsibility)
**Goal:** Practice behavioral design patterns
- [ ] Create validation chain for book data
- [ ] Add validators: title length, author format, description sanitization
- [ ] Implement custom validation rules
- [ ] Add validation error aggregation

### Task 10: Database Migration System
**Goal:** Learn database versioning and schema management
- [ ] Create migration framework from scratch
- [ ] Add version tracking table
- [ ] Implement up/down migration methods
- [ ] Add CLI commands for migration management

**Completion Goal:** Transform from 55/100 to 85+/100 professional-grade application.
