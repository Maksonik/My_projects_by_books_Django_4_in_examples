from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def payment_completed(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешном оплате заказа
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f"My shop - Invoice no. {order_id}"
    message = 'Please, find attached the invoice for your recent purchase'
    email = EmailMessage(subject,
                         message,
                         'maksonik7@gmail.com',
                         [order.email])
    # Сгенерировать PDF
    html = render_to_string('orders/order/pdf.html', {'order' : order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # Прикрепить PDF-файл
    email.attach(f'order_{order_id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # отправить электронное письмо
    email.send()