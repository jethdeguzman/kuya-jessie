from chatbot.actions import *
import requests

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


def waiting_for_agent(recipient_id, type=None):
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
                                            "payload": "USER_DEFINED_PAYLOAD"
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
        update_user(recipient_id, data={'state': 'START_AGENT'})


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
