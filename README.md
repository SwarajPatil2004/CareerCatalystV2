# CareerCatalyst

A production-grade web platform for career development, featuring student profile management, TPO (Training and Placement Officer) operations, Skill Intelligence for resume analysis, and structured Career Roadmaps.

## Features

- **Auth**: JWT-based authentication with role-based access control (Student, TPO).
- **Student Portal**: Manage profile, skills, experiences, projects, and track career progress.
- **TPO Portal**: Manage placement drives, track student activity, and monitor "students at risk".
- **Skill Intelligence**: Automated analysis of resume bullets for action verbs, metrics, and quality.
- **Career Roadmaps**: Detailed learning paths with phases, tasks, and XP tracking.

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Pydantic.
- **Frontend**: React, TypeScript, Tailwind CSS, Lucide Icons.
- **Infrastructure**: Docker, Nginx.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- (Optional for manual setup) Python 3.11+, Node.js 18+

### Running with Docker (Recommended)

1. Clone the repository.
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Start the application:
   ```bash
   docker-compose up --build
   ```
4. Access the platforms:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:8000](http://localhost:8000)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Manual Setup

#### Backend

1. Navigate to the root directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## User Roles & Setup

- **Student**: Register via the frontend portal. Default role is `student`.
- **TPO**: To create a TPO account, register a user and then manually update their role in the database to `tpo`.
  ```sql
  UPDATE users SET role = 'tpo' WHERE email = 'tpo@example.com';
  ```

## Database Migrations

Currently, the project uses SQLAlchemy's `create_all()` or automated table creation on startup. For production-grade migrations, consider adding Alembic.

---

Built with ❤️ by the CareerCatalyst Team.
