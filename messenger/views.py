import requests
import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .states import *
from chatbot.actions import *

REQUEST_HANDLER = {
    'INITIAL_STATE': initial_state_request,
    'CREATE_NEW_TASK': create_new_task_request,
    'TASK_IS_CREATED': task_is_created_request,
    'WAITING_FOR_AGENT': waiting_for_agent_request,
}

RESPONSE_HANDLER = {
    'INITIAL_STATE': initial_state,
    'START_AGENT': start_agent,
    'CREATE_NEW_TASK': create_new_task,
    'TASK_IS_CREATED': task_is_created,
    'WAITING_FOR_AGENT': waiting_for_agent,
    'TASK_SELECTED': task_selected,
    'INVALID_COMMAND': invalid_command,
    'TASK_ON_PROCESS': task_on_process
}

VERIFY_TOKEN = 'kuyajessie'
PAGE_ACCESS_TOKEN = 'EAAIv6P1MQB0BAGP5ZBDmvjqNhQvuZBzLnGvLtEvXFIMZAy1ZAnO93IS0NpZBIwaZCZASMCo7zeOmcMRW0O6jFR6Hj9dokm73YBGr3diYSMeyeAzeJgEQHbSTpDbhFRrMKzswLKT8W8Hv4ogijwNAKkGfqWUu4K3dtYx1ipJfVVXUvIKyqmKZA73J'
HEADERS = {'Content-Type':'application/json'}
URL = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(PAGE_ACCESS_TOKEN)

def send_menu(recipient_id, state, type=None):
    try:
        data = RESPONSE_HANDLER[state](recipient_id, type)
        response = requests.post(url=URL, data=json.dumps(data), headers=HEADERS)
    except KeyError as e:
        return Response(status=status.HTTP_200_OK)

    print('==========')
    print(response.json())


class Callback(APIView):
    """
    This will be the callback url of the chatbot Kuya Jessie.
    """
    def get(self, request):
        hub_challenge = request.GET.get('hub.challenge')
        hub_verify_token = request.GET.get('hub.verify_token')

        if VERIFY_TOKEN == hub_verify_token:
            return Response(int(hub_challenge))
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        try:
            messaging = request.data['entry'][0]['messaging'][0]
            message = messaging['message']
            text = message['text']
            sender_id = messaging['sender']['id']
        except KeyError as e:
            print('========')
            print('Received a postback request.')
            postback = messaging.get('postback')
            if postback is not None:
                text = postback['payload']
                sender_id = messaging['sender']['id']
            else:
                return Response(status=status.HTTP_200_OK)

        user = get_user(sender_id)
        user_state = user.state
        user_type = user.type

        print('===========')
        print(user.state)
        print(user.type)
        print(text)

        if text.upper() == 'HELP':
            send_menu(sender_id, state=user_state, type=user_type)
            return Response(status=status.HTTP_200_OK)

        REQUEST_HANDLER[user_state](sender_id, text)
        user = get_user(sender_id)
        send_menu(sender_id, state=user.state, type=user.type)

        return Response(status=status.HTTP_200_OK)
