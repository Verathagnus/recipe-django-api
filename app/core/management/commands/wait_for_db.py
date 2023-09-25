"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        timeout = options.get('timeout', 60)  # Default timeout is 30 seconds.
        start_time = time.time()

        db_up = False
        while db_up is False and time.time() - start_time < timeout:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(self.style.ERROR("Database unavailable, \
                    waiting for 1 second..."))
                time.sleep(1)

        if db_up is False:
            raise TimeoutError('Database timed out.')

        self.stdout.write(self.style.SUCCESS('Database available!'))
