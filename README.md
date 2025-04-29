# Django Project Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, production-ready Django project template for scalable web applications.

---

## 🚀 Features

- 🧩 **Modular App Structure**: All Django apps live in `apps/` for easy scalability and separation of concerns.
- ⚙️ **Environment-based Settings**: Clean, modular settings for development and production (`conf/settings/`).
- 🐳 **Docker & Docker Compose**: Full support for local and production environments with Docker.
- 🗄️ **PostgreSQL & Redis**: Production-grade database and cache/backing store.
- ☁️ **S3/MinIO Storage**: Optional S3-compatible storage for media files.
- 🦾 **REST API**: Built-in Django REST Framework, JWT authentication, filtering, and error handling.
- 🧑‍💻 **Admin UI**: Jazzmin for a beautiful Django admin interface.
- 🧪 **Testing & Linting**: Pytest, Flake8, and Debug Toolbar for robust development.
- 📦 **Makefile**: Common commands for migrations, pip, and secret key generation.
- 📊 **Monitoring**: Integrated Prometheus and Grafana dashboards for metrics and alerting.
- 🔐 **Security**: Django Axes for brute-force protection, CORS, and secure settings.
- 📦 **CI/CD Ready**: Example GitHub Actions workflow for build and deployment.
- 🤖 **Telegram Notifications**: Deployment script can notify via Telegram on success/failure.
- 🌐 **Traefik Reverse Proxy**: Traefik is used for smart routing, HTTPS, and service discovery in Docker.

## 🛠️ Tech Stack & Integrations

- **Django 5.2**
- **Django REST Framework**
- **PostgreSQL**
- **Redis**
- **Docker & Docker Compose**
- **Prometheus & Grafana**
- **MinIO (S3-compatible storage)**
- **Celery (with Redis broker)**
- **drf-yasg (Swagger/OpenAPI docs)**
- **django-debug-toolbar**
- **pytest, flake8, pyflakes**
- **Traefik**
- **GitHub Actions**

## 📁 Project Structure

```
apps/           # All Django apps
conf/           # Project config (settings, urls, wsgi, asgi, swagger)
deployment/     # Docker, Nginx, Prometheus, Grafana, Traefik, CI/CD scripts
  ├── dev/      # Development Docker Compose, monitoring, Grafana, Prometheus
  ├── prod/     # Production Docker Compose, monitoring, Grafana, Prometheus
  ├── docker-compose.shared.yml # Shared Traefik & MinIO config
  ├── nginx.conf
  ├── entrypoint.sh
  ├── Dockerfile
  └── deploy.sh
requirements/   # base.txt, dev.txt, prod.txt for pip dependencies
Makefile        # Common dev commands
example.env     # Example environment variables
```

### 🗂️ Deployment Structure

- **deployment/dev/**: Local/dev Docker Compose, Prometheus, Grafana configs
- **deployment/prod/**: Production Docker Compose, Prometheus, Grafana configs
- **deployment/docker-compose.shared.yml**: Shared services (Traefik, MinIO)
- **deployment/nginx.conf**: Nginx config for static/media
- **deployment/entrypoint.sh**: Entrypoint for Django/Gunicorn container
- **deployment/Dockerfile**: Multi-stage Docker build for Django
- **deployment/deploy.sh**: Bash script for CI/CD and Telegram notifications

### 🌐 Traefik
- Traefik acts as a reverse proxy and load balancer for all services.
- Handles HTTPS (Let's Encrypt), routing, and service discovery.
- Configured in `deployment/docker-compose.shared.yml` and referenced in both dev/prod setups.

## ⚡ Getting Started

### Prerequisites
- Python 3.8+
- Docker & Docker Compose

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/ganiyevuz/django-project-template.git
   cd django-project-template
   ```
2. Copy the example environment file:
   ```bash
   cp example.env .env
   ```
3. Build and start the development environment:
   ```bash
   cd deployment/dev
   docker-compose up --build
   ```

### Running Locally (without Docker)
1. Install dependencies:
   ```bash
   pip install -r requirements/base.txt -r requirements/dev.txt
   ```
2. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Production
- Use `requirements/prod.txt` for production dependencies.
- Gunicorn is used as the WSGI server (see `deployment/entrypoint.sh`).
- Use `deployment/prod/docker-compose.yml` for production deployment.
- Traefik and MinIO are managed via `deployment/docker-compose.shared.yml`.

## 📊 Monitoring & Observability
- Prometheus scrapes metrics from Django, Traefik, Redis, Node Exporter, and more.
- Grafana dashboards for real-time monitoring.
- Alerts and notifications can be configured.

## 🔒 Security
- Django Axes for brute-force protection
- CORS and CSRF settings
- Environment-based secrets

## 🤝 Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements.

## 📄 License
MIT
