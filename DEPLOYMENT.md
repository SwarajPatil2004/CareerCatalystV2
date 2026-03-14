# Deployment Guide

This guide provides instructions for deploying CareerCatalyst to various cloud platforms.

## 🚀 Cloud Platform Instructions

### 1. Render.com (Easiest for Web Apps)
- **Backend (FastAPI)**:
  - Create a new "Web Service".
  - Connect your GitHub repository.
  - Runtime: "Docker".
  - Docker Command: Leave as default (it will use `Dockerfile.prod`).
  - Add Environment Variables: `DATABASE_URL`, `SECRET_KEY`, `REDIS_URL`, `ENVIRONMENT=prod`.
- **Database (PostgreSQL)**:
  - Create a new "PostgreSQL" instance on Render.
  - Copy the internal database URL into your Backend's environment variables.

### 2. Railway.app (Great for full stacks)
- Create a new project from your GitHub repo.
- Railway will detect the `docker-compose.yml` or the Dockerfile.
- Use the "Provision PostgreSQL" and "Provision Redis" buttons to add databases instantly.
- Deployment is automatic on push to `main`.

### 3. DigitalOcean (For full control)
- Create a "Droplet" (Ubuntu 22.04).
- Install Docker and Docker Compose.
- Clone your repo and run:
  ```bash
  docker-compose -f docker-compose.prod.yml up -d
  ```
- Configure your domain A records to point to the Droplet's IP.

## 🔒 Security Best Practices
- Always use HTTPS (the provided Nginx config is ready for SSL).
- Change `SECRET_KEY` to a long, random string.
- Never commit your actual `.env` file to version control.
- Use a dedicated database user with limited privileges for production.

## 🏥 Monitoring & Health
- Monitor the `/health` endpoint for uptime.
- Check logs via `docker-compose logs -f backend`.
- Real-time logs will be in JSON format for easier parsing by log aggregators.
