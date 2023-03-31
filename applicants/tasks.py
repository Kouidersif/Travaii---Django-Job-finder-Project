from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from datetime import datetime
from main.models import (Jobs, User)

@shared_task(bind=True)
def inform_company(self, job_id, user_id):
    today_date = datetime.now()
    job = Jobs.objects.get(pk=job_id)
    user = User.objects.get(pk=user_id)

    mail_subject = f"It’s here! The first application for {job.position}" 
    from_email='no-reply@travaii.com'
    email_message = 'apply_email/applied_for_your_job.html'
    html_message = render_to_string(email_message, {
                'position':job.position,
                'publisher':job.publisher.full_name,
                'job':job,
                'applicant':user.full_name,
                'time':today_date,
            })
    message = EmailMessage(mail_subject, html_message,from_email, to=[job.publisher.email])
    message.content_subtype = 'html'
    message.send()
    return "Email Has been Sent"
