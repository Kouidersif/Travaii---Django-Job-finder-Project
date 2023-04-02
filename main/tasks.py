from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime
from main.models import (User)

@shared_task(bind=True)
def Notify_user_account_deleted(self, user_id):
    today_date = datetime.now()
    user = User.objects.get(pk=user_id)

    mail_subject = 'Travaii Team: Account has been deleted'
    templ = render_to_string('account_deleted.html', {
        'name':user.full_name,
    })
    success_email = EmailMessage(
                mail_subject, templ, 
                to=[user.email],
            )
    success_email.send()
    return "User has been notified about account deletion"
