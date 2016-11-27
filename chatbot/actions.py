import django

import decimal
from .models import User, Task
from .services import transfer_funds, get_account_info

def format_number(value, format="0.00", rounding="ROUND_HALF_UP"):
    return decimal.Decimal(value).quantize(decimal.Decimal(format), rounding=rounding)

def get_users():
    return User.objects.all()

def get_user(messenger_id):
    try:
        user = User.objects.get(messenger_id=messenger_id)
    except User.DoesNotExist as udne:
        user = User.objects.create(messenger_id=messenger_id)

    return user

def get_agents():
    return User.objects.filter(type='AGENT')

def update_user(messenger_id, data):
    return User.objects.filter(messenger_id=messenger_id).update(**data)

def create_task(messenger_id, description):
    task = Task.objects.create(owner=get_user(messenger_id), description=description)
    update_user(messenger_id, {'state' : 'TASK_IS_CREATED'})

def update_task(reference_number, data):
    return Task.objects.filter(reference_number=reference_number).update(**data)

def get_task(reference_number):
    return Task.objects.get(reference_number=reference_number)

def get_available_tasks():
    return Task.objects.filter(status='AVAILABLE')

def update_task_amount(messenger_id, amount):
    task = Task.objects.filter(owner=get_user(messenger_id)).last()
    update_task(task.reference_number, {'amount' : format_number(amount)})
    update_user(messenger_id, {'state' : 'WAITING_FOR_AGENT'})
    transfer_funds('CUSTOMER', 'APP', amount=format_number(amount))


def set_agent(messenger_id, reference_number):
    task = get_task(reference_number)
    update_task(reference_number, {'agent' : get_user(messenger_id), 'status' : 'ON_PROCESS'})
    update_user(messenger_id, {'recipient_id' : task.owner.messenger_id, 'state' : 'TASK_ON_PROCESS'})
    update_user(task.owner.messenger_id, {'recipient_id' : messenger_id, 'state' : 'TASK_ON_PROCESS'})

def cancel_task(messenger_id):
    task = Task.objects.filter(owner=get_user(messenger_id)).last()
    update_task(task.reference_number, {'status' : 'CANCELLED'})
    update_user(messenger_id, {'state' : 'INITIAL_STATE'})
    transfer_funds('APP', 'CUSTOMER', amount=float(task.amount))

def done_task(messenger_id):
    task = Task.objects.filter(agent=get_user(messenger_id)).last()
    update_user(messenger_id, {'state' : 'INITIAL_STATE'})
    update_user(task.owner.messenger_id, {'state' : 'INITIAL_STATE'})
    update_task(task.reference_number, {'status' : 'DONE'})
    transfer_funds('APP', 'AGENT', amount=float(task.amount))

def decline_task(messenger_id):
    task = Task.objects.filter(agent=get_user(messenger_id)).last()
    update_user(messenger_id, {'state' : 'INITIAL_STATE'})
    update_user(task.owner.messenger_id, {'state' : 'WAITING_FOR_AGENT'})
