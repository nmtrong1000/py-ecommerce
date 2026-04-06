# Py-Ecommerce

## Clean architecture

# Clean Architecture: 4-Layer Inward Flow

```
  INFRASTRUCTURE  ─────────────────────────────────────────────────
  Role:    DB / External Tools / Implementations
  ─────────────────────────────────────────────────────────────────
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃     Repository Impl      ┃ ━━━━▶ ┃          Model           ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛       ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                ┃                                   ┃
                ┃                                   ┃
                ▼                                   ▼
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                  Dependency Injection (DI)                  ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                ┃
                ┃
                ▼
  PRESENTATION  ───────────────────────────────────────────────────
  Role:    Entry points / UI / Delivery
  ─────────────────────────────────────────────────────────────────
                ┃
                ┃
                ▼
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓       ┌──────────────────────────┐
    ┃       Controller         ┃ ━━━━▶ │       Normalizer         │
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛       └──────────────────────────┘
                ┃
                ┃
                ▼
  APPLICATION  ────────────────────────────────────────────────────
  Role:    Orchestration / Use Cases / DTOs
  ─────────────────────────────────────────────────────────────────
                ┃
                ┃
                ▼
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓       ┌──────────────────────────┐
    ┃  Service Orchestrators   ┃ ━━━━▶ │          DTO             │
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛       └──────────────────────────┘
                ┃
                ┃
                ▼
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓       ┌──────────────────────────┐
    ┃       Use Case           ┃ ━━━━▶ │        Mapper            │
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛       └──────────────────────────┘
                ┃
                ┃
                ▼
  DOMAIN  ─────────────────────────────────────────────────────────
  Role:    Business Logic / Entities / Interfaces
  ─────────────────────────────────────────────────────────────────
                ┃
                ┃
                ▼
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃        Repository        ┃ ━━━━▶ ┃         Entity           ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛       ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Directory structure

```
.
├── alembic                         <---- Database migration environment
│   └── versions                    <---- Schema change history scripts
├── app                             <---- Main application source code
│   ├── application                 <---- Business orchestration layer
│   │   ├── dtos                    <---- Data Transfer Objects for I/O
│   │   ├── services                <---- Application-specific workflows
│   │   └── usecases                <---- Individual business actions
│   ├── domain                      <---- Core enterprise logic & rules
│   │   ├── entities                <---- Pure business objects
│   │   └── repositories            <---- Abstract data access interfaces
│   ├── infrastructure              <---- Technical & external tool logic
│   │   ├── config                  <---- App settings & env variables
│   │   ├── di                      <---- Dependency Injection wiring
│   │   └── persistence             <---- Data storage implementation
│   │       ├── mappers             <---- DB-to-Entity transformation
│   │       ├── models              <---- Database-specific ORM schemas
│   │       └── repositories        <---- Concrete database logic
│   ├── presentation                <---- User interface/Entry points
│   │   └── controllers             <---- API route handlers
│   └── shared                      <---- Global utilities & constants
├── devops                          <---- Deployment & CI/CD assets
│   ├── compose                     <---- Docker Compose configurations
│   └── docker                      <---- Container build files
├── docs                            <---- Technical documentation
└── tests                           <---- Automated test suites
    ├── integration                 <---- Tests for external contracts
    └── unit                        <---- Isolated logic verification
        └── mockup                  <---- Fakes/Mocks for testing
```

## Technical stacks

- Python v3.13
- FastAPI v0.135.1
- Postgres
- Redis v7.3.0
- SQLAlchemy v2.0.48
- Alembic v1.18.4
- Pydantic v2.12.5
- Pytest v9.0.2
