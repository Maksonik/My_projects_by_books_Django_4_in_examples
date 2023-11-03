from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешном создании заказа
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name}, \n\n You have successfully placed an order. Your order ID is {order.id}'
    mail_sent = send_mail(subject,
                          message,
                          'maksonik7@gmail.com',
                          [order.email])
    return mail_sent