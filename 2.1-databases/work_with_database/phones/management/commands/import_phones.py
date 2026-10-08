import csv
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        csv_path = Path(settings.BASE_DIR) / 'phones.csv'
        with csv_path.open(newline='', encoding='utf-8') as file:
            for phone in csv.DictReader(file, delimiter=';'):
                Phone.objects.update_or_create(
                    id=int(phone['id']),
                    defaults={
                        'name': phone['name'],
                        'image': phone['image'],
                        'price': int(phone['price']),
                        'release_date': date.fromisoformat(phone['release_date']),
                        'lte_exists': phone['lte_exists'].strip().lower() == 'true',
                    },
                )
