import json


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def lambda_handler(event, context):
    response = {"dialogAction": {
        "type": "Close",
        "message": {
            "contentType": "PlainText",
            "content": "Message to convey to the user."
        }
    }
    }

    return dispatch(event)


def elict(slots, slot, mess):
    return {"dialogAction": {
        'type': 'ElicitSlot',
        'intentName': "DiningSuggestionsIntent",
        'slots': slots,
        'slotToElicit': slot,
        "message": {
            "contentType": "PlainText",
            "content": mess
        }
    }
    }


def dispatch(event):
    slots = get_slots(event)

    if slots['Location'] is not None:
        slots['Location'] = slots['Location'].lower()
        slots['Location'] = slots['Location'].capitalize()
        if slots['Location'] not in ['Downtown', 'Midtown', 'Uptown', 'Harlem']:
            return elict(slots, "Location",
                         "Could you please try again? Please select the region from Downtown, Midtown, Uptown or Harlem.")

    if slots['PhoneNumber'] is not None:
        if not slots['PhoneNumber'].isdigit():
            return elict(slots, "PhoneNumber",
                         "Could you please try again? Please provide a 10-digit phone number.")
        elif len(slots['PhoneNumber']) != 10:
            return elict(slots, "PhoneNumber",
                         "Could you please try again? Please provide a 10-digit phone number.")

    # if slots['Cuisine'] is not None:
    #     cuisine_og = slots['Cuisine']
    #     slots['Cuisine'] = slots['Cuisine'].lower()
    #     slots['Cuisine'] = slots['Cuisine'].capitalize()
    #     if slots['Cuisine'] not in ['American', 'French', 'Italian', 'Mexican', 'Thai', 'Indian', 'Chinese', 'Japanese',
    #                                 'Vietnamese', 'Caribbean', 'African', 'Greek', 'Korean', 'British', 'German']:
    #         return elict(slots, "Cuisine",
    #                      f"Sorry, I don't support {cuisine_og} cuisine at this moment. Could you please try something else?")

    output_session_attributes = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}
    return delegate(output_session_attributes, slots)