"""
Management command to seed the portfolio with Mina's real data.
Run: python manage.py seed_portfolio
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import SiteConfig, TechStack, Experience, Certification
from projects.models import Project, Technology, ProjectHighlight, Category
import datetime


class Command(BaseCommand):
    help = 'Seeds the portfolio database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding portfolio data...')
        self._seed_config()
        self._seed_tech_stack()
        self._seed_categories()
        self._seed_projects()
        self._seed_experience()
        self._seed_certifications()
        self.stdout.write(self.style.SUCCESS('Portfolio seeded successfully!'))

    def _seed_config(self):
        SiteConfig.objects.update_or_create(pk=1, defaults={
            'site_name': 'Dev Mina',
            'tagline': 'Software Engineer & AI Systems Developer',
            'hero_headline': 'I build software that makes businesses smarter.',
            'hero_subheadline': (
                'Backend systems, AI-powered applications, and automation workflows '
                'engineered to solve real problems at scale.'
            ),
            'about_text': (
                'I am Adebowale Abidemi Aminat — a Software Engineer and AI Systems Developer '
                'with experience building backend systems, AI-powered applications, workflow '
                'automation solutions, and enterprise software. My work focuses on turning complex '
                'business requirements into scalable, maintainable, and impactful software products.'
            ),
            'github_url': 'https://github.com/devmina',
            'linkedin_url': 'https://linkedin.com/in/devmina',
            'email': 'hello@devmina.com',
            'is_available': True,
        })
        self.stdout.write('  Config seeded')

    def _seed_tech_stack(self):
        techs = [
            ('Python', 'language', 95, True),
            ('Kotlin', 'language', 80, True),
            ('JavaScript', 'language', 75, False),
            ('Java', 'language', 70, False),
            ('PHP', 'language', 65, False),
            ('SQL', 'language', 85, True),
            ('Django', 'framework', 90, True),
            ('FastAPI', 'framework', 88, True),
            ('Ktor', 'framework', 78, False),
            ('Jetpack Compose Multiplatform', 'framework', 75, False),
            ('PostgreSQL', 'database', 88, True),
            ('MySQL', 'database', 80, False),
            ('Redis', 'database', 75, False),
            ('Gemini API', 'ai_ml', 90, True),
            ('LLM Integration', 'ai_ml', 88, True),
            ('Machine Learning', 'ai_ml', 82, True),
            ('Deep Learning', 'ai_ml', 75, False),
            ('Prompt Engineering', 'ai_ml', 92, True),
            ('n8n', 'automation', 85, True),
            ('Voiceflow', 'automation', 78, False),
            ('Git & GitHub', 'tool', 90, True),
            ('Docker', 'tool', 78, False),
            ('Postman', 'tool', 85, False),
            ('AWS', 'cloud', 75, True),
        ]
        for i, (name, cat, prof, featured) in enumerate(techs):
            TechStack.objects.get_or_create(name=name, defaults={
                'category': cat, 'proficiency': prof, 'is_featured': featured, 'order': i,
            })
        self.stdout.write('  Tech stack seeded')

    def _seed_categories(self):
        cats = [
            ('AI-Powered Application', 'ai', 'Intelligent systems that leverage AI, ML, and LLMs.'),
            ('Backend System',         'backend', 'Scalable APIs, databases, and server-side applications.'),
            ('Workflow Automation',    'automation', 'Automated business processes that reduce manual effort.'),
            ('Business Intelligence',  'bi', 'Data platforms that turn raw information into decisions.'),
            ('Enterprise Software',    'enterprise', 'Systems supporting business operations and workflows.'),
            ('Mobile Application',     'mobile', 'Cross-platform mobile applications.'),
            ('Research & Innovation',  'research', 'Academic and experimental engineering work.'),
        ]
        for name, slug, desc in cats:
            Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
        self.stdout.write('  Categories seeded')

    def _seed_projects(self):
        projects_data = [
            {
                'title': 'GrowthPath',
                'subtitle': 'AI-Powered Lead Generation & Qualification System',
                'description': 'An intelligent lead generation and qualification platform that automates prospect discovery, scoring, and routing using AI-powered workflows.',
                'long_description': '## Overview\n\nGrowthPath automates the most time-consuming parts of a B2B sales pipeline — lead discovery, qualification, and routing — using orchestrated AI workflows.\n\n## Key Features\n\n- AI-powered prospect analysis and scoring\n- Workflow orchestration with n8n\n- Conversational qualification via Voiceflow\n- Sales pipeline optimization and reporting\n\n## Architecture\n\nBuilt on FastAPI with PostgreSQL for persistence and n8n as the workflow orchestration layer. LLM integration handles intelligent prospect analysis.',
                'categories': ['ai', 'automation'],
                'status': 'production',
                'is_featured': True,
                'order': 1,
                'techs': ['FastAPI', 'PostgreSQL', 'n8n', 'Voiceflow', 'Python'],
                'highlights': ['Lead qualification automation', 'Workflow orchestration', 'AI-powered prospect analysis', 'Sales pipeline optimization'],
                'metric_label': 'Qualification accuracy',
                'metric_value': '94%',
            },
            {
                'title': 'Customer Insight AI',
                'subtitle': 'Generative AI Business Intelligence Platform',
                'description': 'An AI-powered system that transforms large volumes of customer feedback into structured business insights, sentiment analysis, and actionable recommendations.',
                'long_description': '## Overview\n\nCustomer Insight AI processes unstructured customer feedback at scale and outputs actionable intelligence — structured reports, sentiment trends, and strategic recommendations.\n\n## Key Features\n\n- Sentiment analysis across feedback channels\n- Automated business intelligence reporting\n- Trend identification and anomaly detection\n- Executive-ready summary generation',
                'categories': ['ai', 'bi'],
                'status': 'production',
                'is_featured': True,
                'order': 2,
                'techs': ['Python', 'Gemini API'],
                'highlights': ['Sentiment analysis', 'Customer intelligence', 'Business recommendations', 'Automated reporting'],
                'metric_label': 'Feedback processed',
                'metric_value': '10k+/day',
            },
            {
                'title': 'AI Fraud Detection System',
                'subtitle': 'ML-Powered Financial Transaction Risk Engine',
                'description': 'A machine learning-powered platform designed to identify fraudulent financial transactions in real time while minimizing false positives.',
                'long_description': '## Overview\n\nA production-grade fraud detection system using ensemble machine learning models to analyze transaction patterns, identify anomalies, and generate risk scores.\n\n## Key Features\n\n- Real-time transaction risk scoring\n- Anomaly detection with deep learning\n- Configurable threshold management\n- Full transaction audit logging',
                'categories': ['ai', 'backend'],
                'status': 'production',
                'is_featured': True,
                'order': 3,
                'techs': ['Python', 'Machine Learning', 'Deep Learning'],
                'highlights': ['Fraud detection', 'Risk scoring', 'Anomaly detection', 'Transaction monitoring'],
                'metric_label': 'Detection precision',
                'metric_value': '97.3%',
            },
            {
                'title': 'USSD Transaction Monitoring Platform',
                'subtitle': 'Fintech Observability & Recovery Middleware',
                'description': 'A monitoring and observability solution for tracking failed USSD transactions and improving financial transaction visibility in mobile banking infrastructure.',
                'long_description': '## Overview\n\nBuilt to solve a critical gap in USSD payment infrastructure: hung and failed transactions that are invisible to operators. This platform provides full observability, automated recovery, and audit logging.\n\n## Key Features\n\n- Six-stage transaction state machine\n- Three-phase recovery engine (Retry → Reversal → Escalation)\n- HUNG vs FAILED transaction distinction\n- Real-time monitoring dashboard\n\n## Research\n\nThis system is the subject of an academic paper co-authored with Prof. Opani Meshack Aweh (ABUAD), currently under review for publication in an international fintech journal.',
                'categories': ['backend', 'research'],
                'status': 'research',
                'is_featured': True,
                'order': 4,
                'techs': ['Python', 'FastAPI', 'PostgreSQL', 'Redis'],
                'highlights': ['Transaction tracking', 'Failure diagnostics', 'Audit logging', 'Reconciliation support'],
                'metric_label': 'Transaction recovery rate',
                'metric_value': '98.1%',
            },
            {
                'title': 'Customer Insight Pro',
                'subtitle': 'Cross-Platform Customer Analytics Application',
                'description': 'A cross-platform customer analytics application built to help organizations better understand customer behavior across multiple touchpoints.',
                'categories': ['mobile', 'bi'],
                'status': 'production',
                'is_featured': True,
                'order': 5,
                'techs': ['Kotlin', 'Jetpack Compose Multiplatform'],
                'highlights': ['Cross-platform (Android & iOS)', 'Customer behavior analytics', 'Real-time data visualization'],
            },
            {
                'title': 'DailySyn',
                'subtitle': 'AI-Powered Productivity & Schedule Optimization',
                'description': 'An AI-powered productivity assistant that dynamically adjusts schedules based on changing responsibilities and priorities.',
                'categories': ['ai', 'automation'],
                'status': 'production',
                'is_featured': False,
                'order': 6,
                'techs': ['AWS', 'Prompt Engineering'],
                'highlights': ['Dynamic schedule adjustment', 'Priority-aware task management', 'AI-driven productivity optimization'],
            },
            {
                'title': 'Hostel Management System',
                'subtitle': 'Complete Accommodation Allocation & Booking Platform',
                'description': 'A complete accommodation allocation and booking platform for managing hostels, room assignments, reservations, and occupancy tracking.',
                'categories': ['enterprise', 'backend'],
                'status': 'production',
                'is_featured': False,
                'order': 7,
                'techs': ['PHP', 'SQL'],
                'highlights': ['Room allocation engine', 'Reservation management', 'Occupancy reporting', 'Admin dashboard'],
            },
        ]

        # Ensure techs exist
        all_tech_names = set()
        for p in projects_data:
            all_tech_names.update(p.get('techs', []))
        for name in all_tech_names:
            Technology.objects.get_or_create(name=name, defaults={'slug': slugify(name)})

        for pd in projects_data:
            proj, _ = Project.objects.update_or_create(
                slug=slugify(pd['title']),
                defaults={
                    'title': pd['title'],
                    'subtitle': pd.get('subtitle', ''),
                    'description': pd['description'],
                    'long_description': pd.get('long_description', ''),
                    'status': pd['status'],
                    'is_featured': pd['is_featured'],
                    'is_published': True,
                    'order': pd['order'],
                    'metric_label': pd.get('metric_label', ''),
                    'metric_value': pd.get('metric_value', ''),
                }
            )
            # Assign multiple categories
            proj.categories.clear()
            for cat_slug in pd.get('categories', []):
                cat = Category.objects.filter(slug=cat_slug).first()
                if cat:
                    proj.categories.add(cat)
            # Assign technologies
            for tech_name in pd.get('techs', []):
                tech = Technology.objects.get(name=tech_name)
                proj.technologies.add(tech)
            proj.highlights.all().delete()
            for i, h in enumerate(pd.get('highlights', [])):
                ProjectHighlight.objects.create(project=proj, text=h, order=i)

        self.stdout.write('  Projects seeded')

    def _seed_experience(self):
        # Clear any previously-seeded placeholder rows so re-running this
        # command always reflects exactly the 12 entries below.
        Experience.objects.all().delete()

        experiences = [
            {
                'type': 'work',
                'role': 'Software Engineer',
                'organization': 'Software Academy',
                'location': 'Nigeria',
                'start_date': datetime.date(2022, 1, 1),
                'end_date': datetime.date(2024, 5, 31),
                'is_current': False,
                'order': 1,
                'description': (
                    'Worked as a Software Engineer at Software Academy, where I designed, developed, '
                    'and maintained full-stack web applications for educational institutions, '
                    'organizations, and businesses. My responsibilities covered the complete software '
                    'development lifecycle, including requirements gathering, system architecture, '
                    'frontend development, backend implementation, database design, testing, deployment, '
                    'and maintenance.\n\n'
                    'I collaborated with other developers to build scalable, secure, and user-friendly '
                    'applications while applying software engineering best practices. During my time at '
                    'Software Academy, I contributed to the development of several production-ready '
                    'systems, including the Software Academy website, the PAMINAS church platform, and '
                    'other organizational web applications. This role strengthened my expertise in '
                    'backend engineering, database management, API development, and building maintainable '
                    'software solutions.'
                ),
            },
            {
                'type': 'work',
                'role': 'Python Developer Intern',
                'organization': 'NXTECH',
                'location': 'Nigeria',
                'start_date': datetime.date(2023, 7, 1),
                'end_date': datetime.date(2023, 9, 30),
                'is_current': False,
                'order': 2,
                'description': (
                    'Completed a Python development internship focused on practical software engineering '
                    'and backend development. Applied object-oriented programming principles to build '
                    'maintainable software while working with databases, debugging techniques, and backend '
                    'application development.\n\n'
                    'The internship provided valuable hands-on experience in solving real-world programming '
                    'problems, improving code quality, and adopting industry-standard software development '
                    'practices that became the foundation for my later work in enterprise software and '
                    'artificial intelligence.'
                ),
            },
            {
                'type': 'work',
                'role': 'Software Engineer Intern',
                'organization': 'Alabian Solutions Limited',
                'location': 'Lagos, Nigeria',
                'start_date': datetime.date(2024, 6, 1),
                'end_date': datetime.date(2024, 9, 30),
                'is_current': False,
                'order': 3,
                'description': (
                    'Worked in an enterprise software engineering environment, contributing to both '
                    'software development and applied artificial intelligence research. Conducted extensive '
                    "research on Meta's LLaMA models, evaluating their capabilities, comparing them with "
                    'other large language models, and exploring practical methods for integrating AI into '
                    'enterprise software.\n\n'
                    'Beyond AI research, I contributed to financial software testing, technical '
                    'documentation, process analysis, and the design of enterprise solutions such as a '
                    'Hostel and Hall Management System. This experience expanded my knowledge of Java, SQL, '
                    'enterprise software architecture, and AI-assisted software engineering.'
                ),
            },
            {
                'type': 'work',
                'role': 'Freelance Full-Stack Software Developer',
                'organization': 'Self-Employed',
                'location': 'Remote',
                'start_date': datetime.date(2024, 1, 1),
                'end_date': None,
                'is_current': True,
                'order': 4,
                'description': (
                    'Provide end-to-end software development services for businesses, organizations, and '
                    'startups by designing and building scalable web applications, enterprise software, '
                    'workflow automation systems, and AI-powered solutions. I manage projects from initial '
                    'concept and system architecture through development, deployment, and ongoing '
                    'maintenance.\n\n'
                    'My freelance portfolio includes e-commerce platforms, enterprise applications, '
                    'artificial intelligence solutions, machine learning systems, workflow automation, '
                    'business intelligence tools, and custom backend systems developed to solve real-world '
                    'business challenges while maintaining high standards of software quality and '
                    'performance.'
                ),
            },
            {
                'type': 'education',
                'role': 'B.Sc. Computer Science (First Class Honours)',
                'organization': 'Afe Babalola University',
                'location': 'Ado-Ekiti, Nigeria',
                'start_date': datetime.date(2021, 10, 1),
                'end_date': datetime.date(2025, 9, 30),
                'is_current': False,
                'order': 5,
                'description': (
                    'Graduated with First Class Honours in Computer Science, building a strong academic '
                    'foundation in software engineering, artificial intelligence, database systems, '
                    'networking, algorithms, and software architecture. Throughout my studies, I combined '
                    'classroom learning with practical software engineering by developing production-ready '
                    'applications, conducting AI research, participating in internships, and serving in '
                    'technical leadership positions.'
                ),
            },
            {
                'type': 'education',
                'role': 'AI & Machine Learning Trainee',
                'organization': 'TechCrush AI & Machine Learning Bootcamp',
                'location': 'Remote',
                'start_date': datetime.date(2026, 3, 1),
                'end_date': datetime.date(2026, 6, 30),
                'is_current': False,
                'order': 6,
                'description': (
                    'Completed a comprehensive 15-week AI and Machine Learning bootcamp covering the '
                    'complete machine learning lifecycle, including data preprocessing, exploratory data '
                    'analysis, feature engineering, supervised learning, deep learning, model evaluation, '
                    'and production workflows. Built practical machine learning solutions such as Diabetes '
                    'Prediction and Credit Card Fraud Detection systems while gaining experience in '
                    'developing production-ready AI applications.'
                ),
            },
            {
                'type': 'education',
                'role': 'AI Engineering Trainee',
                'organization': 'TS Academy',
                'location': 'Remote',
                'start_date': datetime.date(2026, 1, 1),
                'end_date': datetime.date(2026, 3, 31),
                'is_current': False,
                'order': 7,
                'description': (
                    'Participated in practical AI engineering training focused on designing, building, and '
                    'deploying intelligent software systems. Strengthened skills in modern AI development '
                    'practices, software engineering, and integrating AI technologies into scalable '
                    'applications.'
                ),
            },
            {
                'type': 'education',
                'role': 'AWS AI & Machine Learning Learner',
                'organization': 'Amazon Web Services (AWS)',
                'location': 'Remote',
                'start_date': datetime.date(2026, 1, 1),
                'end_date': None,
                'is_current': True,
                'order': 8,
                'description': (
                    'Currently expanding my expertise in cloud-native artificial intelligence and machine '
                    'learning through AWS training. The program focuses on cloud infrastructure, scalable '
                    'AI services, deployment strategies, and building production-ready intelligent '
                    'applications using the AWS ecosystem.'
                ),
            },
            {
                'type': 'education',
                'role': 'Artificial Intelligence Learner',
                'organization': 'Huawei ICT Academy',
                'location': 'Afe Babalola University',
                'start_date': datetime.date(2026, 1, 1),
                'end_date': None,
                'is_current': True,
                'order': 9,
                'description': (
                    "Currently participating in Huawei ICT Academy's Artificial Intelligence learning "
                    'programme, developing practical knowledge in AI concepts, machine learning, and '
                    'intelligent application development through structured learning, hands-on '
                    'laboratories, and collaborative technical activities.'
                ),
            },
            {
                'type': 'volunteer',
                'role': 'Software Director',
                'organization': 'Nigerian Association of Computing Students (NACOS), Afe Babalola University Chapter',
                'location': 'Ado-Ekiti, Nigeria',
                'start_date': datetime.date(2024, 10, 1),
                'end_date': datetime.date(2025, 9, 30),
                'is_current': False,
                'order': 10,
                'description': (
                    'Served as the Software Director of NACOS, providing technical leadership for '
                    'software-related initiatives within the association. Planned and coordinated '
                    'technical workshops, encouraged project-based learning, mentored student developers, '
                    'and promoted practical software engineering beyond the classroom. Worked closely with '
                    "fellow executives to create opportunities that enhanced members' programming skills, "
                    'collaboration, and exposure to modern software development practices.'
                ),
            },
            {
                'type': 'volunteer',
                'role': 'SkillHub Director',
                'organization': 'Nigerian Association of Computing Students (NACOS), Afe Babalola University Chapter',
                'location': 'Ado-Ekiti, Nigeria',
                'start_date': datetime.date(2025, 10, 1),
                'end_date': None,
                'is_current': True,
                'order': 11,
                'description': (
                    'Serve as the SkillHub Director, leading NACOS SkillHub, the association\u2019s flagship '
                    'technical development initiative. Responsible for planning, coordinating, and '
                    'overseeing the execution of the program while working with facilitators, mentors, and '
                    'student leaders to deliver industry-relevant technical training.\n\n'
                    'Under my leadership, SkillHub provides practical learning experiences across software '
                    'engineering, artificial intelligence, cybersecurity, UI/UX design, cloud computing, '
                    'data science, and other emerging technology fields. I oversee program strategy, '
                    'facilitate collaboration between technical teams, and ensure participants gain '
                    'hands-on experience by building real-world projects that prepare them for internships '
                    'and professional careers.'
                ),
            },
            {
                'type': 'volunteer',
                'role': 'Student Coordinator',
                'organization': 'Huawei ICT Academy',
                'location': 'Afe Babalola University, Ado-Ekiti',
                'start_date': datetime.date(2026, 6, 1),
                'end_date': None,
                'is_current': True,
                'order': 12,
                'description': (
                    'Serve as the Student Coordinator for the Huawei ICT Academy at Afe Babalola University, '
                    'acting as the primary liaison between students, academy administrators, and '
                    'instructors. Coordinate student onboarding, organize academy activities, communicate '
                    'important updates, and provide guidance to participants throughout their learning '
                    'journey.\n\n'
                    'In addition to administrative coordination, I support the growth of the academy by '
                    'helping students navigate the Huawei ecosystem, facilitating engagement within the '
                    'learning community, promoting academy initiatives, and contributing to the successful '
                    'delivery of AI and ICT training programs. This role has strengthened my leadership, '
                    'communication, community management, and organizational skills while supporting the '
                    'development of future technology professionals.'
                ),
            },
        ]
        for e in experiences:
            Experience.objects.update_or_create(
                role=e['role'], organization=e['organization'],
                defaults={**e, 'is_published': True}
            )
        self.stdout.write('  Experience seeded')

    def _seed_certifications(self):
        certs = [
            ('Huawei AI Certification', 'Huawei', datetime.date(2023, 6, 1)),
            ('Huawei Cloud Certification', 'Huawei', datetime.date(2023, 9, 1)),
            ('AWS Cloud Practitioner', 'Amazon Web Services', datetime.date(2024, 1, 1)),
        ]
        for i, (name, issuer, date) in enumerate(certs):
            Certification.objects.get_or_create(name=name, defaults={
                'issuer': issuer, 'issue_date': date, 'is_featured': True, 'order': i,
            })
        self.stdout.write('  Certifications seeded')
