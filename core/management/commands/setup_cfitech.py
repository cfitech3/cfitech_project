"""
Commande de configuration initiale CFI-TECH
Usage: python manage.py setup_cfitech
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Configure les données initiales de CFI-TECH (domaines, FAQ, services, config site)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n🚀 Configuration initiale CFI-TECH\n'))

        # Charger les fixtures
        fixtures = [
            ('core', 'initial_data'),
            ('formations', 'domains'),
            ('services', 'services'),
        ]

        for app, fixture in fixtures:
            try:
                call_command('loaddata', fixture, app_label=app, verbosity=0)
                self.stdout.write(self.style.SUCCESS(f'  ✅ {app}/{fixture} chargé'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠️  {app}/{fixture}: {e}'))

        self.stdout.write('\n' + self.style.SUCCESS(
            '✨ Configuration terminée !\n\n'
            'Prochaines étapes :\n'
            '  1. python manage.py createsuperuser\n'
            '  2. python manage.py runserver\n'
            '  3. Admin: http://localhost:8000/cfitech-admin/\n'
            '  4. Configurez le site dans Admin → Configuration du site\n'
        ))
