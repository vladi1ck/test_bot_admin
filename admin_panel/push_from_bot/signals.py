from django.db.models.signals import post_save
from django.dispatch import receiver

import push_from_bot.tasks
from push_from_bot.models import Push


# @receiver(signal=post_save, sender=Push)
# def send_push(instance,  **kwargs):
#     print('HERE')
#     push_from_bot.tasks.send_broadcast_message.delay(instance.id)
#     instance.sent = True