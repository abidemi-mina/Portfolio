# Portfolio Platform — Architecture Document

## Design Decisions

### 1. Django 5 + SQLite (dev) / PostgreSQL (prod)
SQLite for zero-friction local development; production uses PostgreSQL via `DATABASES` config switch. The switch requires only environment variable changes — no code changes.

### 2. Service Layer Pattern (SRP + DIP)
Every app has a `services.py` module that owns all business logic and database queries. Views are thin HTTP adapters that delegate to services. This means:
- Views never contain queries
- Services are independently testable
- Logic is reusable across views, management commands, and API endpoints

### 3. Abstract Base Models (OCP + LSP)
Three abstract models form the inheritance chain:
- `TimeStampedModel` — created_at, updated_at (every model)
- `SluggedModel(TimeStampedModel)` — title, slug with auto-generation
- `PublishableModel(SluggedModel)` — is_published, meta_title, meta_description

Adding a new content type means inheriting from the right level. No model duplication.

### 4. Singleton SiteConfig
`SiteConfig.objects.get_or_create(pk=1)` with `pk = 1` enforcement on save. Gives admin-editable control over every piece of dynamic content (hero copy, social links, availability badge) without touching code.

### 5. Context Processor for Global Data
`core.context_processors.site_context` injects `site_config` into every template. No view needs to pass it manually.

### 6. SEO Middleware
`core.middleware.SEOMiddleware` attaches `request.canonical_url` to every request for use in Open Graph and canonical link tags. Keeps SEO logic DRY.

### 7. Whitenoise for Static Files
Eliminates the need for a separate static file server in development and simple production deployments. CompressedManifestStaticFilesStorage adds cache-busting hashes.

## App Responsibilities

| App | Responsibility |
|-----|---------------|
| core | SiteConfig, TechStack, homepage service, base models, sitemaps |
| projects | Project, Technology, ProjectHighlight, CRUD, search, filter |
| experience | Work/education timeline entries |
| certifications | Credential cards |
| blog | Post, Tag, Markdown rendering, view counter |
| contact | ContactMessage, AJAX form, email notification |

## Database Model Summary

```
TimeStampedModel (abstract)
├── SiteConfig          (singleton)
├── TechStack           (grouped by category)
├── Experience          (timeline items)
├── Certification       (credential cards)
├── ContactMessage      (inbound messages)
└── SluggedModel (abstract)
    └── PublishableModel (abstract)
        ├── Project     → ManyToMany Technology
        │               → OneToMany ProjectHighlight
        └── Post        → ManyToMany Tag
```

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values

# Database setup
python manage.py migrate
python manage.py seed_portfolio

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Production Checklist
- Set `DEBUG=False`
- Set `SECRET_KEY` to 50+ char random string
- Configure PostgreSQL in `DATABASES`
- Set `ALLOWED_HOSTS` to your domain
- Set `SITE_URL` for canonical URLs
- Configure SMTP for contact form emails
- Run `python manage.py collectstatic`
- Add `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`
- Serve with Gunicorn + Nginx
