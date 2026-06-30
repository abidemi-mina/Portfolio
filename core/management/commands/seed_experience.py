from django.core.management.base import BaseCommand

from core.models import TechStack


class Command(BaseCommand):
    help = "Seed technology stack"

    TECH_STACK = [
        # ==========================
        # Languages
        # ==========================
        {
            "name": "Python",
            "category": "language",
            "proficiency": 95,
            "icon_class": "devicon-python-plain",
            "order": 1,
            "is_featured": True,
        },
        {
            "name": "JavaScript",
            "category": "language",
            "proficiency": 92,
            "icon_class": "devicon-javascript-plain",
            "order": 2,
            "is_featured": True,
        },
        {
            "name": "Java",
            "category": "language",
            "proficiency": 80,
            "icon_class": "devicon-java-plain",
            "order": 3,
            "is_featured": True,
        },
        {
            "name": "Kotlin",
            "category": "language",
            "proficiency": 80,
            "icon_class": "devicon-kotlin-plain",
            "order": 4,
            "is_featured": True,
        },
        {
            "name": "PHP",
            "category": "language",
            "proficiency": 85,
            "icon_class": "devicon-php-plain",
            "order": 5,
            "is_featured": False,
        },
        {
            "name": "SQL",
            "category": "language",
            "proficiency": 88,
            "icon_class": "fas fa-database",
            "order": 6,
            "is_featured": False,
        },
        {
            "name": "HTML5",
            "category": "language",
            "proficiency": 95,
            "icon_class": "devicon-html5-plain",
            "order": 7,
            "is_featured": False,
        },
        {
            "name": "CSS3",
            "category": "language",
            "proficiency": 92,
            "icon_class": "devicon-css3-plain",
            "order": 8,
            "is_featured": False,
        },

        # ==========================
        # Frameworks
        # ==========================
        {
            "name": "Django",
            "category": "framework",
            "proficiency": 95,
            "icon_class": "devicon-django-plain",
            "order": 1,
            "is_featured": True,
        },
        {
            "name": "FastAPI",
            "category": "framework",
            "proficiency": 90,
            "icon_class": "devicon-fastapi-plain",
            "order": 2,
            "is_featured": True,
        },
        {
            "name": "Jetpack Compose Multiplatform",
            "category": "framework",
            "proficiency": 82,
            "icon_class": "devicon-jetpackcompose-plain",
            "order": 3,
            "is_featured": True,
        },
        {
            "name": "Ktor",
            "category": "framework",
            "proficiency": 80,
            "icon_class": "fas fa-server",
            "order": 4,
            "is_featured": False,
        },
        {
            "name": "Bootstrap",
            "category": "framework",
            "proficiency": 90,
            "icon_class": "devicon-bootstrap-plain",
            "order": 5,
            "is_featured": False,
        },
        {
            "name": "Tailwind CSS",
            "category": "framework",
            "proficiency": 90,
            "icon_class": "devicon-tailwindcss-original",
            "order": 6,
            "is_featured": False,
        },

        # ==========================
        # Databases
        # ==========================
        {
            "name": "PostgreSQL",
            "category": "database",
            "proficiency": 90,
            "icon_class": "devicon-postgresql-plain",
            "order": 1,
            "is_featured": True,
        },
        {
            "name": "MySQL",
            "category": "database",
            "proficiency": 90,
            "icon_class": "devicon-mysql-plain",
            "order": 2,
            "is_featured": True,
        },
        {
            "name": "SQLite",
            "category": "database",
            "proficiency": 85,
            "icon_class": "devicon-sqlite-plain",
            "order": 3,
            "is_featured": False,
        },

        # ==========================
        # AI & Machine Learning
        # ==========================
        {
            "name": "Pandas",
            "category": "ai_ml",
            "proficiency": 92,
            "icon_class": "devicon-pandas-original",
            "order": 1,
            "is_featured": True,
        },
        {
            "name": "NumPy",
            "category": "ai_ml",
            "proficiency": 90,
            "icon_class": "devicon-numpy-original",
            "order": 2,
            "is_featured": False,
        },
        {
            "name": "Scikit-learn",
            "category": "ai_ml",
            "proficiency": 88,
            "icon_class": "fas fa-brain",
            "order": 3,
            "is_featured": True,
        },
        {
            "name": "TensorFlow",
            "category": "ai_ml",
            "proficiency": 82,
            "icon_class": "devicon-tensorflow-original",
            "order": 4,
            "is_featured": True,
        },
        {
            "name": "Matplotlib",
            "category": "ai_ml",
            "proficiency": 85,
            "icon_class": "fas fa-chart-line",
            "order": 5,
            "is_featured": False,
        },
        {
            "name": "Google Gemini API",
            "category": "ai_ml",
            "proficiency": 90,
            "icon_class": "fas fa-robot",
            "order": 6,
            "is_featured": False,
        },
        {
            "name": "LLaMA Research",
            "category": "ai_ml",
            "proficiency": 88,
            "icon_class": "fas fa-microchip",
            "order": 7,
            "is_featured": False,
        },

        # ==========================
        # Automation
        # ==========================
        {
            "name": "n8n",
            "category": "automation",
            "proficiency": 90,
            "icon_class": "fas fa-code-branch",
            "order": 1,
            "is_featured": True,
        },
        {
            "name": "Voiceflow",
            "category": "automation",
            "proficiency": 88,
            "icon_class": "fas fa-comments",
            "order": 2,
            "is_featured": False,
        },

        # ==========================
        # Tools & DevOps
        # ==========================
        {
            "name": "Git",
            "category": "tool",
            "proficiency": 90,
            "icon_class": "devicon-git-plain",
            "order": 1,
            "is_featured": True,
        },
        {
            "name": "GitHub",
            "category": "tool",
            "proficiency": 92,
            "icon_class": "devicon-github-original",
            "order": 2,
            "is_featured": True,
        },
        {
            "name": "Visual Studio Code",
            "category": "tool",
            "proficiency": 95,
            "icon_class": "devicon-vscode-plain",
            "order": 3,
            "is_featured": False,
        },
        {
            "name": "Android Studio",
            "category": "tool",
            "proficiency": 80,
            "icon_class": "devicon-androidstudio-plain",
            "order": 4,
            "is_featured": False,
        },
        {
            "name": "Postman",
            "category": "tool",
            "proficiency": 90,
            "icon_class": "devicon-postman-plain",
            "order": 5,
            "is_featured": False,
        },
        {
            "name": "Blender",
            "category": "tool",
            "proficiency": 70,
            "icon_class": "devicon-blender-original",
            "order": 6,
            "is_featured": False,
        },

        # ==========================
        # Cloud
        # ==========================
        {
            "name": "Amazon Web Services (AWS)",
            "category": "cloud",
            "proficiency": 75,
            "icon_class": "devicon-amazonwebservices-original-wordmark",
            "order": 1,
            "is_featured": True,
        },
    ]

    def handle(self, *args, **kwargs):
        for tech in self.TECH_STACK:
            TechStack.objects.update_or_create(
                name=tech["name"],
                defaults=tech,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Successfully seeded {len(self.TECH_STACK)} technologies."
            )
        )