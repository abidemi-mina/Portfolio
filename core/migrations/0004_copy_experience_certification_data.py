"""
Historical data migration — no-op on fresh installs.
This migration existed to copy data from the now-removed experience and
certifications apps into core. On a fresh install there is nothing to copy,
so it runs clean. The seed_portfolio command handles populating data instead.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_experience_certification_to_core'),
    ]

    operations = []
