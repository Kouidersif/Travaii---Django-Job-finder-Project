from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.csrf import csrf_exempt # new
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .decorators import check_sub
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from .models import Customer
import stripe
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse  # updated
from .models import *
from main.models import User
from django.contrib import messages
import time
import logging
from company.decorators import notLogged
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
import random
proration_date = int(time.time())



stripe.api_key= settings.STRIPE_SECRET_KEY



def add_Card(request):
    customer = stripe.Customer.create(
        email=request.user.email,
    )
    intent = stripe.SetupIntent.create(
            customer=customer.id,
            payment_method_types=["card"],
            )
    print(intent.id)
    return render(request, 'join.html',{'client_secret':intent.client_secret} )



def TestClock(request):
    creatobj = stripe.test_helpers.TestClock.create(frozen_time=1670192338, name="Annual renewal")
    customer_create= stripe.Customer.create(
                    email=request.user.email,
                    test_clock= creatobj.id,
                    payment_method="pm_card_visa",
                    invoice_settings={"default_payment_method": "pm_card_visa"},
                    )
    sub = stripe.Subscription.create(
                customer=customer_create.id,
                items=[{"price": "price_1Lz0nvKORmC2RvgX0uRVY5kz"}],
                )
    subscription = stripe.Subscription.retrieve(sub.id)
    product = stripe.Product.retrieve(subscription.plan.product)
    
    f = Customer.objects.create(
        user= request.user,
        stripeid= customer_create.id,
        stripe_subscription_id= sub.id,
        membership = True,
        cancel_at_period_end= False, 
        selected_membership = product.name
        )
    print(customer_create)
    print(creatobj)
    return HttpResponse('tested')



def Advance_time(request):
    stripe.test_helpers.TestClock.advance('clock_1MAv8XKORmC2RvgXdL7Oy4um', frozen_time=1733316283)
    return HttpResponse('tested check sub')




@login_required
def ShowTotal_before_update(request):
    try:
        if request.user.customer.membership:
            stripe_customer = Customer.objects.get(user=request.user)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
            product = stripe.Product.retrieve(subscription.plan.product)
            customer_data= stripe.Customer.retrieve(stripe_customer.stripeid)
            
            if request.method == 'GET' and 'membership' in request.GET:
                small_Business= ProName.objects.filter(name='Small business')
                Mid_market_plan = ProName.objects.filter(name='Mid-market enterprises')
                large_enterprise_plan = ProName.objects.filter(name='Large enterprise')
            #small business companies
                for s in small_Business:
                    if request.GET['membership'] == 'smallbusinessmonth':
                        selected_member = 'Small business'
                        pri_year_id= s.price_month_id_code
                        pri_digi= int(s.price_per_month)
                        membership = 'smallbusiness'
                        membership_id = pri_year_id
                        final_dollar = pri_digi
                        get_request_sub_id = '?membership=smallbusinessmonth'
                        
                    elif request.GET['membership'] == 'smallbusinessyear':
                        selected_member = 'Small business'
                        pri_year_id= s.price_year_id_code
                        pri_digi= int(s.price_per_year)
                        membership = 'smallbusiness'
                        membership_id = pri_year_id
                        final_dollar = pri_digi
                        get_request_sub_id = '?membership=smallbusinessyear'
                
                        #Mid Market companies
                for t in Mid_market_plan:
                    if request.GET['membership'] == 'midmarketplanyear' :
                        selected_member = 'Mid-market enterprises'
                        pri_year_id= t.price_year_id_code
                        pri_digi= int(t.price_per_year)
                        membership = 'midmarketplanyear'
                        membership_id = pri_year_id
                        final_dollar = pri_digi
                        get_request_sub_id = '?membership=midmarketplanyear'
                    elif request.GET['membership'] == 'midmarketplanmonth' :
                        selected_member = 'Mid-market enterprises'
                        pri_month_id= t.price_month_id_code
                        pri_digi= int(t.price_per_month)
                        membership = 'midmarketplanyear'
                        membership_id = pri_month_id
                        final_dollar = pri_digi
                        get_request_sub_id = '?membership=midmarketplanmonth'
                #Larg Companies
                for p in large_enterprise_plan:
                    if request.GET['membership'] == 'Largeenterprisemonth':
                        selected_member = 'Large enterprise'
                        pri_month_id= p.price_month_id_code
                        pri_digi= int(p.price_per_month)
                        membership = 'Largeenterprisemonth'
                        membership_id = pri_month_id
                        final_dollar = pri_digi
                        get_request_sub_id = '?membership=Largeenterprisemonth'
                    elif request.GET['membership'] == 'Largeenterpriseyear':
                        selected_member = 'Large enterprise'
                        pri_year_id= p.price_year_id_code
                        pri_digi= int(p.price_per_year)
                        membership = 'Largeenterpriseyear'
                        membership_id = pri_year_id
                        final_dollar = pri_digi
                        get_request_sub_id = '?membership=Largeenterpriseyear'
        items= [{ 'id': subscription['items']['data'][0].id,
                'price': membership_id, # Switch to new price
                }]
        proration_date = int(time.time())
        invoice = stripe.Invoice.upcoming(
                customer=stripe_customer.stripeid,
                subscription=stripe_customer.stripe_subscription_id,
                subscription_items=items,
                subscription_proration_date=proration_date,
                )
        payment_method = stripe.Customer.list_payment_methods(
                customer=stripe_customer.stripeid,
                type="card",
                )
        last4digits = payment_method['data']
        invoice_unused_time= invoice['lines']['data'][0]
        invoice_remaining_time=invoice['lines']['data'][1]
        total =abs(invoice_remaining_time.amount) + (invoice_unused_time.amount)
        if total < 0:
            
            credit_to_account = abs(total/100)
            total = 0
        else:
            credit_to_account = ''
            total = abs(invoice_remaining_time.amount) + (invoice_unused_time.amount)
        today_date= datetime.date.today()
        
        context={'invoice':invoice, 'invoice_unused_time':invoice_unused_time, 'last4digits':last4digits,'customer_data':customer_data,
            'invoice_remaining_time':invoice_remaining_time, 'total':total, 'credit_to_account':credit_to_account, 'get_request_sub_id':get_request_sub_id, 'today_date':today_date}
        return render(request, 'preview.html', context)
            
    except Customer.DoesNotExist:
        return redirect('subscription')
    

##########
@login_required
def Update_subscription(request):
    try:
        if request.user.customer.membership:
            stripe_customer = Customer.objects.get(user=request.user)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
            product = stripe.Product.retrieve(subscription.plan.product)
            if request.method == 'GET' and 'membership' in request.GET:
                small_Business= ProName.objects.filter(name='Small business')
                Mid_market_plan = ProName.objects.filter(name='Mid-market enterprises')
                large_enterprise_plan = ProName.objects.filter(name='Large enterprise')
            #small business companies
                for s in small_Business:
                    if request.GET['membership'] == 'smallbusinessmonth':
                        selected_member = 'Small business'
                        pri_year_id= s.price_month_id_code
                        pri_digi= int(s.price_per_month)
                        membership = 'smallbusiness'
                        membership_id = pri_year_id
                        final_dollar = pri_digi
                    elif request.GET['membership'] == 'smallbusinessyear':
                        selected_member = 'Small business'
                        pri_year_id= s.price_year_id_code
                        pri_digi= int(s.price_per_year)
                        membership = 'smallbusiness'
                        membership_id = pri_year_id
                        final_dollar = pri_digi
                
                        #Mid Market companies
                for t in Mid_market_plan:
                    if request.GET['membership'] == 'midmarketplanyear' :
                        selected_member = 'Mid-market enterprises'
                        pri_year_id= t.price_year_id_code
                        pri_digi= int(t.price_per_year)
                        membership = 'midmarketplanyear'
                        membership_id = pri_year_id
                        final_dollar = pri_digi
                    elif request.GET['membership'] == 'midmarketplanmonth' :
                        selected_member = 'Mid-market enterprises'
                        pri_month_id= t.price_month_id_code
                        pri_digi= int(t.price_per_month)
                        membership = 'midmarketplanyear'
                        membership_id = pri_month_id
                        final_dollar = pri_digi
                #Larg Companies
                for p in large_enterprise_plan:
                    if request.GET['membership'] == 'Largeenterprisemonth':
                        selected_member = 'Large enterprise'
                        pri_month_id= p.price_month_id_code
                        pri_digi= int(p.price_per_month)
                        membership = 'Largeenterprisemonth'
                        membership_id = pri_month_id
                        final_dollar = pri_digi
                    elif request.GET['membership'] == 'Largeenterpriseyear':
                        selected_member = 'Large enterprise'
                        pri_year_id= p.price_year_id_code
                        pri_digi= int(p.price_per_year)
                        membership = 'Largeenterpriseyear'
                        membership_id = pri_year_id
                        final_dollar = pri_digi
                        
            proration_date = int(time.time()),
            stripe.Subscription.modify(
            subscription.id,
            cancel_at_period_end=False,
            proration_behavior='always_invoice',
            items=[{
                'id': subscription['items']['data'][0].id,
                'price': membership_id,
            }],
            )
            
            subscriber = Customer.objects.filter(user= request.user)
            subscriber.update(
                selected_membership = selected_member
            )
            subscriber.update(
                cancel_at_period_end= False,
            )

            
            
            #i have to change the template because it does not need a session id it will do it auto 
            ### WORRKEDDDD!!!!!!!!!!!!!
            
        #print(session)
            
        return redirect('success')
    except Customer.DoesNotExist:
        return redirect('subscription')


###choose PLAN
    


def subscribe(request):
    if request.user.is_authenticated:
        try:
            stripe_customer = Customer.objects.get(user=request.user)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
            product = stripe.Product.retrieve(subscription.plan.product)
            if subscription.status == 'past_due':
                return render(request, 'declined.html')
            else:
                check_interval = subscription['items']['data'][0]['price']
                #print(check_interval.recurring.interval)
                print(subscription.status)
                current_plan = product.name
                small_Business= ProName.objects.filter(name='Small business')
                Mid_market_plan = ProName.objects.filter(name='Mid-market enterprises')
                large_enterprise_plan = ProName.objects.filter(name='Large enterprise')
                context={
                    'small_Business':small_Business, 'Mid_market_plan':Mid_market_plan, 'large_enterprise_plan':large_enterprise_plan, 'check_interval':check_interval,
                    'product':product, 'subscription':subscription, 'current_plan':current_plan
                }
                return render(request, 'choose.html', context)
        except Customer.DoesNotExist:
            small_Business= ProName.objects.filter(name='Small business')
            Mid_market_plan = ProName.objects.filter(name='Mid-market enterprises')
            large_enterprise_plan = ProName.objects.filter(name='Large enterprise' )
            context={
                'small_Business':small_Business, 'Mid_market_plan':Mid_market_plan, 'large_enterprise_plan':large_enterprise_plan
            }
            return render(request, 'choose.html', context)

    else:
        small_Business= ProName.objects.filter(name='Small business')
        Mid_market_plan = ProName.objects.filter(name='Mid-market enterprises')
        large_enterprise_plan = ProName.objects.filter(name='Large enterprise' )
        context={
            'small_Business':small_Business, 'Mid_market_plan':Mid_market_plan, 'large_enterprise_plan':large_enterprise_plan
        }
        return render(request, 'choose.html', context)
    
    

##START SUBSCRIPTION 

@login_required
@notLogged
def checkout(request):
    try:
        pass
    except Customer.DoesNotExist:
        pass
    if request.method == 'POST':
        pass
    if request.method == 'GET' and 'membership' in request.GET:
        small_Business= ProName.objects.filter(name='Small business')
        Mid_market_plan = ProName.objects.filter(name='Mid-market enterprises')
        large_enterprise_plan = ProName.objects.filter(name='Large enterprise')
        #small business companies
        for s in small_Business:
            if request.GET['membership'] == 'smallbusinessmonth':
                selected= 'Small business'
                pri_year_id= s.price_month_id_code
                pri_digi= int(s.price_per_month)
                membership = 'smallbusiness'
                membership_id = pri_year_id
                final_dollar = pri_digi
            elif request.GET['membership'] == 'smallbusinessyear':
                selected= 'Small business'
                
                pri_year_id= s.price_year_id_code
                pri_digi= int(s.price_per_year)
                membership = 'smallbusiness'
                membership_id = pri_year_id
                final_dollar = pri_digi
        
                #Mid Market companies
        for t in Mid_market_plan:
            if request.GET['membership'] == 'midmarketplanyear' :
                selected= 'Mid-market enterprises'
                pri_year_id= t.price_year_id_code
                pri_digi= int(t.price_per_year)
                membership = 'midmarketplanyear'
                membership_id = pri_year_id
                final_dollar = pri_digi
            elif request.GET['membership'] == 'midmarketplanmonth' :
                selected= 'Mid-market enterprises'
                pri_month_id= t.price_month_id_code
                pri_digi= int(t.price_per_month)
                membership = 'midmarketplanyear'
                membership_id = pri_month_id
                final_dollar = pri_digi
        #Larg Companies
        for p in large_enterprise_plan:
            if request.GET['membership'] == 'Largeenterprisemonth':
                selected= 'Large enterprise'
                pri_month_id= p.price_month_id_code
                pri_digi= int(p.price_per_month)
                membership = 'Largeenterprisemonth'
                membership_id = pri_month_id
                final_dollar = pri_digi
            elif request.GET['membership'] == 'Largeenterpriseyear':
                selected= 'Large enterprise'
                pri_year_id= p.price_year_id_code
                pri_digi= int(p.price_per_year)
                membership = 'Largeenterpriseyear'
                membership_id = pri_year_id
                final_dollar = pri_digi
            # Create Strip Checkout
        
    session = stripe.checkout.Session.create(
        client_reference_id=request.user.id if request.user.is_authenticated else None,
        payment_method_types=['card'],
        customer_email = request.user.email,
        line_items=[{
            'price': membership_id,
            'quantity': 1,
        }],
        mode='subscription',
        allow_promotion_codes=True,
        success_url='https://travaii.com/subscription/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://travaii.com/subscription/cancel',
    )
    #print(session)
    print('session completed')
    return render(request, 'checkout.html', {'final_dollar': final_dollar, 'session_id': session.id})

####RREACTIVATE SUBSCRIPTIOON







@check_sub
def yearly(request):
    stripe_customer = Customer.objects.get(user=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
    return render(request, 'choose_year.html')


@login_required
@notLogged
def customer_portal(request):
    stripe_customer = Customer.objects.get(user=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
    # Authenticate your user.
    session = stripe.billing_portal.Session.create(
    customer=stripe_customer.stripeid,
    return_url='https://travaii.com/',
    )
    return redirect(session.url)










####DIAMOND 

###Success Page


@login_required
@notLogged
def success(request):
    return render(request, 'success.html')

@login_required
@notLogged
def cancel(request):
    return render(request, 'cancel.html')



#WEBHOOK 
import datetime

def Confirm_message(request, user, to_email):
    mail_subject = 'Your subscription has been activated!'
    templ = render_to_string('success_subscription.html', {
        'name':user.full_name,
        'plan':request.user.customer.selected_membership,

    })
    success_email = EmailMessage(
                mail_subject, templ, 
                to=[to_email],
            )
    success_email.send()

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')
        user = User.objects.get(id=client_reference_id)
        subscription = stripe.Subscription.retrieve(stripe_subscription_id)
        product = stripe.Product.retrieve(subscription.plan.product)
        numbers = '0987654321124801424129801240984120981432324241250832509523095230974209814'
        user_unique_id = str(user.id)
        length= 15
        order_id = "".join(random.sample(numbers, length))
        order_id_user_id= user_unique_id + order_id
        date_today = datetime.date.today()
        Customer.objects.create(
        user= user,
        stripeid= stripe_customer_id,
        stripe_subscription_id= stripe_subscription_id,
        membership = True,
        cancel_at_period_end= False, 
        selected_membership = product.name,
        track_id = order_id_user_id
        )
        
        
        subject = 'Welcome to Travaii Premium'
        html_message = render_to_string('success_subscription.html', {
         'name':user.full_name,
            'plan':product.name,
            'today':date_today,
            'order_id':order_id_user_id
                })
        
        from_email='no-reply@travaii.com'
        to_email = user.email
        send_mail(subject, '', from_email, [to_email], html_message=html_message)
        list_payment_meth= stripe.Customer.list_payment_methods(
                        stripe_customer_id,
                        type="card",
                        )
        make_payment_default = stripe.Customer.modify(
                            stripe_customer_id,
                            invoice_settings ={
                            'default_payment_method':list_payment_meth['data'][0].id,
                            }
                            )
        
    # Use the event type to find out what happened
    if event and event['type'] == 'payment_intent.payment_failed':

        # Get the object affected
        payment_intent = event['data']['object']

        # Use stored information to get an error object
        e = payment_intent['last_payment_error']

        # Use its type to choose a response
        if e['type'] == 'card_error':
            logging.error("A payment error occurred: {}".format(e['message']))
        elif e['type'] == 'invalid_request':
            logging.error("An invalid request occurred.")
        else:
            logging.error("Another problem occurred, maybe unrelated to Stripe")

    return HttpResponse(status=200)





    
