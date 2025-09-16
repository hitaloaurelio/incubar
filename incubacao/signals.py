# incubacao/signals.py
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_in)
def logout_other_sessions(sender, request, user, **kwargs):
    current_session_key = request.session.session_key
    all_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    for session in all_sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.id) and session.session_key != current_session_key:
            session.delete()  # encerra sessão antiga
