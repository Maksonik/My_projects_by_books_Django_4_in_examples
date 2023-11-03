import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    print('payload')
    print(payload)
    print('_'*50)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    print('sig_header')
    print(sig_header)
    print('_' * 50)
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
        print('event')
        print(event)
        print('_' * 50)

    except ValueError as e:
        #Недопустимая полезная нагрузка
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        #недопустимая подпись
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # пометить заказ как оплаченный
            order.paid = True
            # сохранить ИД платежа Stripe
            order.stripe_id = session.payment_intent
            order.save()
            # запустить ассихронное задание
            payment_completed.delay(order.id)

    return HttpResponse(status=200)