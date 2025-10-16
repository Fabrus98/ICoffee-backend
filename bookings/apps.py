from django.apps import AppConfig
from .storage import update_session_date

class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'

    update_session_date()