from chatbot.actions import *
import requests
import json

PAGE_ACCESS_TOKEN = 'EAAZAVsVdErmoBAMxVEMZBoxZCBhikbWfZBe1d4AJGJWmwsGOZA1uoZAprUCyU4kaZAP5YVG0tVefuKwLvP8ToCZB59h1XrY2d0oiVSSDXku7mHuQkBgL5ZBCck57OUuOE55zUswP1nIhVQIH40OZC21sDpyLhosIdKLmzzIvHrUKggJQZDZD'
HEADERS = {'Content-Type':'application/json'}
URL = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(PAGE_ACCESS_TOKEN)


def initial_state(recipient_id, type=None):
    return {"recipient": {
                    "id": str(recipient_id)
                },
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "What do you want to do next?",
                            "buttons": [
                                            {
                                                "type": "postback",
                                                "title": "Create New Task",
                                                "payload": "CREATE_NEW_TASK"
                                            },
                                            {
                                                "type": "postback",
                                                "title": "Be an Agent",
                                                "payload": "BE_AN_AGENT"
                                            }
                            ]
                        }
                    }
                }
            }


def start_agent(recipient_id, type=None):
    return {"recipient": {
                "id": str(recipient_id)
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "What do you want to do next?",
                        "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "View Available Tasks",
                                            "payload": "USER_DEFINED_PAYLOAD"
                                        },
                                        {
                                            "type": "postback",
                                            "title": "Logout",
                                            "payload": "USER_DEFINED_PAYLOAD"
                                        }
                            ]
                        }
                    }
                }
            }


def get_user_profile_preferences(recipient_id):
    url = 'https://graph.facebook.com/v2.6/{0}?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token={1}'.format(recipient_id, PAGE_ACCESS_TOKEN)
    response = requests.get(url=url)
    return response.json()


def last_available_task(recipient_id, task):
    user_profile = get_user_profile_preferences(task.owner.messenger_id)

    return {"recipient":{
            "id": str(recipient_id)
        },
        "message":{
            "attachment":{
                        "type":"template",
                        "payload":{
                            "template_type":"generic",
                            "elements":[
                                        {
                                            "title": task.description,
                                            "item_url":"",
                                            "image_url": user_profile.get('profile_pic'),
                                            "subtitle": user_profile.get('first_name') + ' ' + user_profile.get('last_name'),
                                            "buttons":[
                                                        {
                                                            "type": "postback",
                                                            "title": "Accept for P{}".format(task.amount),
                                                            "payload": "TASK_ON_PROCESS"
                                                        }
                                            ]
                                        }
                            ]
                        }
            }
        }
        }


def agents_chat_blast():
    agents = get_agents()

    for agent in agents:
        recipient_id = agent.messenger_id
        task = get_available_tasks().last()
        data = last_available_task(recipient_id, task)
        response = requests.post(url=URL, data=json.dumps(data), headers=HEADERS)
        print(response.json())


def waiting_for_agent(recipient_id, type=None):
    agents_chat_blast()
    return {"recipient": {
            "id": str(recipient_id)
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "Please wait while we connect you to our agents.",
                        "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "Cancel Task",
                                            "payload": "CANCEL_TASK"
                                        }
                            ]
                        }
                    }
                }
            }


def task_selected(recipient_id, type=None):
    return {"recipient": {
            "id": str(recipient_id)
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "What do you want to do next?",
                        "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "Decline",
                                            "payload": "USER_DEFINED_PAYLOAD"
                                        },
                                        {
                                            "type": "postback",
                                            "title": "Done Task",
                                            "payload": "USER_DEFINED_PAYLOAD"
                                        }
                            ]
                        }
                    }
                }
            }


def task_on_process(recipient_id, type=None):
    if str(type).upper() == 'CUSTOMER':
        return {"recipient": {
                "id": str(recipient_id)
                },
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "What do you want to do next?",
                            "buttons": [
                                            {
                                                "type": "postback",
                                                "title": "Decline",
                                                "payload": "DECLINE"
                                            }
                                ]
                            }
                        }
                    }
                }
 
    elif str(type).upper() == 'AGENT':
        return {"recipient": {
                "id": str(recipient_id)
                },
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "What do you want to do next?",
                            "buttons": [
                                            {
                                                "type": "postback",
                                                "title": "Decline",
                                                "payload": "DECLINE"
                                            },
                                            {
                                                "type": "postback",
                                                "title": "Done Task",
                                                "payload": "DECLINE"
                                            }
                                ]
                            }
                        }
                    }
                }
    
    else:
        return initial_state(recipient_id)


def invalid_command(recipient_id, type=None):
        return {"recipient": {
                "id": str(recipient_id)
                },
                "message": {
                        "text": "Oops, I didn't get that. Type 'help' to show available options."
                    }
                }


def create_new_task(recipient_id, type=None):
    return {"recipient": {
            "id": str(recipient_id)
            },
            "message": {
                    "text": "Please describe your task."
                }
            }

def initial_state_request(recipient_id, text):
    if text.upper() == 'CREATE_NEW_TASK':
        update_user(recipient_id, data={'state': 'CREATE_NEW_TASK'})
    elif text.upper() == 'BE_AN_AGENT':
        update_user(recipient_id, data={'type': 'AGENT', 'state': 'START_AGENT'})


def create_new_task_request(recipient_id, text):
    create_task(recipient_id, text)


def task_is_created(recipient_id, type=None):
    return {"recipient": {
            "id": str(recipient_id)
            },
            "message": {
                    "text": "How much are you willing to pay for it?"
                }
            }

def task_is_created_request(recipient_id, text):
    update_task_amount(recipient_id, float(text))


def waiting_for_agent_request(recipient_id, text):
    if text.upper() == 'CANCEL_TASK':
        cancel_task(recipient_id)
