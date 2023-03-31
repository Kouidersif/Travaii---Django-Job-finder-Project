from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from datetime import datetime, timedelta
import stripe
from main.models import User
import time 
from subscriptions.models import Customer





@shared_task(bind=True)
def Create_membership(self, user_id):
    """
    Activate subscription for user and send Email to inform
    """

    user = User.objects.get(id=user_id)
    customer = stripe.Customer.create(
            email = user.email,
            name = user.full_name,
            )
    

    end_date = datetime.today() + timedelta(days=30)
    unix_time = int(time.mktime(end_date.timetuple()))
    subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[{"price": 'price_1M2IF6KORmC2RvgXMZWFL7uI'}],
    trial_end=unix_time,
    )

    Customer.objects.create(
        user = user,
        stripeid = customer.id,
        stripe_subscription_id = subscription.id,
        membership = True,
        selected_membership = 'Large enterprise',
    )
    mail_subject = 'Free Trial Subscription Activated - Travaii'
    html_message = 'Hello!<br><br>'
    html_message += f'Hi {user.full_name} <br> We are excited to inform you that you have received a free trial subscription to our platform. During this trial period, you can start sharing job openings for free.<br><br>'
    html_message += 'Thank you for choosing us!<br><br>'
    html_message += 'Best regards,<br>The Travaii Team'
    from_email= 'support@travaii.com'
    message = EmailMessage(mail_subject, html_message,from_email, to=[user.email])
    message.content_subtype = 'html' # this is required because there is no plain text email version
    message.send()

    
    return "Subscription has been created and email was sent "