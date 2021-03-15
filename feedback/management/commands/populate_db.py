import random
from datetime import datetime, timedelta

import pytz
from essential_generators import DocumentGenerator
from django.core.management.base import BaseCommand

from feedback.models import Giver, Feedback


class Command(BaseCommand):
    help = 'Populates the database with random generated data.'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='The number of feedback entries that should be generated.')

    def handle(self, *args, **options):
        givers = [
            Giver.objects.get_or_create(name='James'), Giver.objects.get_or_create(name='John'),
            Giver.objects.get_or_create(name='Robert'), Giver.objects.get_or_create(name='Michael'),
            Giver.objects.get_or_create(name='William'), Giver.objects.get_or_create(name='David'),
            Giver.objects.get_or_create(name='Richard'), Giver.objects.get_or_create(name='Joseph'),
        ]
        gen = DocumentGenerator()
        amount = options['amount'] if options['amount'] else 2500
        for i in range(0, amount):
            dt = pytz.utc.localize(datetime.now() - timedelta(days=random.randint(0, 1825)))
            feedback = Feedback.objects.create(
                activity=random.choice(Feedback.ACTIVITIES)[0],
                giver=random.choice(givers)[0],
                complex=True if random.randint(1, 2) == 1 else False,
                complicated=True if random.randint(1, 2) == 1 else False,
                entrustability=random.choice(Feedback.ENTRUSTABILITY_SCORES)[0],
                done_well=gen.sentence(),
                needs_improvement=gen.sentence(),
            )
            feedback.date = dt.date()
            feedback.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))
