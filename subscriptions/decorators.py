
from .models import Customer
from django.conf import settings
import stripe
from django.shortcuts import redirect

#check if stripe subscription is active else will disable membership option in user's account

def check_sub(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:    
            try:
                
                subscriber = Customer.objects.filter(user= request.user)
                stripe_customer = Customer.objects.get(user=request.user)
                stripe.api_key = settings.STRIPE_SECRET_KEY
                subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
                product = stripe.Product.retrieve(subscription.plan.product)
                if subscription.status == 'canceled' or subscription.status == 'ended':
                    subscriber.delete()
                #if subscription.status == 'active' or subscription.status == 'trialing' or subscription.status == 'Failed':
                else:
                    return view_func(request, *args, **kwargs)
                    
            except Customer.DoesNotExist:
                return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func 


