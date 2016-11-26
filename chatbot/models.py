from __future__ import unicode_literals

import datetime
import random
import time
from decimal import Decimal
from django.db import models
from hashids import Hashids

USER_TYPE  = (
    ('CUSTOMER', 'Customer'),
    ('AGENT', 'Agent'),
)

USER_STATE = (
    ('INITIAL_STATE', 'Initial state'),
    ('CREATE_NEW_TASK', 'Create new task'),
    ('START_AGENT', 'Start agent'),
    ('TASK_IS_CREATED', 'Task is created'),
    ('UDPATED_TASK_AMOUNT', 'Updated task amount'),
    ('WAITING_FOR_AGENT', 'Waiting for agent'),
    ('TASK_SELECTED', 'Task selected'),
    ('TASK_ON_PROCESS', 'Task on process')
)

TASK_STATUS = (
    ('AVAILABLE', 'Available'),
    ('ON_PROCESS', 'On process'),
    ('CANCELLED', 'Cancelled'),
    ('DONE', 'Done')
)

REFERENCE_NUMBER_CHARACTERS = '234567ABCDEFGHJKLMNPQRSTUVWXYZ'

def generate_reference_number():
    now = datetime.datetime.utcnow()
    salt = long(random.getrandbits(32))

    hashids = Hashids(alphabet=REFERENCE_NUMBER_CHARACTERS, min_length=8, salt=str(salt))
    random_string = hashids.encode(long(time.mktime(now.timetuple())) + now.microsecond)

    return random_string

class User(models.Model):
    messenger_id = models.CharField(max_length=255, null=False, blank=False, unique=True)
    type = models.CharField(max_length=255, choices=USER_TYPE, default='CUSTOMER')
    state =  models.CharField(max_length=255, choices=USER_STATE, default='INITIAL_STATE')
    recipient_id =  models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.messenger_id

class Task(models.Model):
    reference_number = models.CharField(max_length=255, null=False, blank=False, unique=True, default=generate_reference_number)
    owner = models.ForeignKey(User, null=True, blank=False, related_name="created_tasks")
    agent = models.ForeignKey(User, null=True, blank=False, related_name="assigned_tasks")
    description = models.TextField(null=False, blank=False, default='')
    status = models.CharField(max_length=255, choices=TASK_STATUS, default='AVAILABLE')
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    date_created = models.DateTimeField(null=False, blank=True, default=datetime.datetime.now)
    date_updated = models.DateTimeField(null=False, blank=True, default=datetime.datetime.now)

    def __unicode__(self):
        return self.reference_number

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.date_updated = datetime.datetime.now()

        super(Task, self).save(*args, **kwargs)
