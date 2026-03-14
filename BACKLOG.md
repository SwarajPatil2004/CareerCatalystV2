# CareerCatalyst Project Backlog

This document tracks future features, technical debt, and architectural improvements planned for CareerCatalyst.

## 🚀 Future Domains & Features

### [Interview Domain]
- [ ] AI-powered mock interview simulator.
- [ ] Speech-to-text integration for real-time feedback.
- [ ] Behavioral question database with STAR method guides.
- [ ] Performance analytics and improvement suggestions.

### [Resume Domain]
- [ ] PDF parsing for existing resumes.
- [ ] AI resume tailor (adjusting resume for specific JDs).
- [ ] Multiple resume version management.
- [ ] Export to professional templates (PostScript/PDF).

### [Analytics Domain]
- [ ] Institution-wide placement statistics.
- [ ] Student skill gap analysis.
- [ ] Trend prediction for hiring seasons.

### [Student Enhancements]
- [ ] Peer-to-peer grading system for projects/coding tasks.
- [ ] Specialized skill badges and certificates.
- [ ] Social features (following mentors, sharing milestones).

## 🛠️ Technical Improvements

### [Infrastructure]
- [ ] **Alembic Migrations**: Transition from `create_all()` to robust versioned migrations.
- [ ] **Monitoring**: Integrate Prometheus/Grafana or Sentry for error tracking.
- [ ] **Caching**: Implement Redis-based caching for frequent API calls (roadmaps, profiles).
- [ ] **Background Jobs**: Set up Celery/Arq for async resume analysis and email notifications.

### [Testing]
- [ ] **Backend**: Increase unit test coverage (target: 80%+).
- [ ] **Frontend**: Implement E2E testing with Playwright or Cypress.
- [ ] **Security**: Automated OWASP ZAP scanning in CI.

### [Frontend]
- [ ] Dark/Light mode toggle.
- [ ] Advanced dashboard visualizations (D3.js or Chart.js).
- [ ] Real-time notifications via WebSockets.

## 📈 TPO Features
- [ ] Mass email/notification system for placement drives.
- [ ] Automated shortlisting based on criteria and skill scores.
- [ ] Feedback portal for companies to rate student performance.
