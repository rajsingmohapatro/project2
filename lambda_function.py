### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def return_outcome(intent_request):
    """
    Based on initial investment it will return the %gain along with message
    """

    #first_name = get_slots(intent_request)["firstName"]
    #age = get_slots(intent_request)["age"]
    investment_amount =int(get_slots(intent_request)["initial_amount"])
    #risk_level = get_slots(intent_request)["riskLvl"]
    source = intent_request["invocationSource"]
    long_term_percentage_gain = 10

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        ### YOUR DATA VALIDATION CODE STARTS HERE ###
        #if age is not None:
         #   if int(age) < 21 or int(age) > 65:
          #      return build_validation_result(
           #         False,
            #        "age",
             #       "Your age should be between 21 to 65 to use this service, "
              #  )
        if investment_amount is not None:
            if int(investment_amount) < 5000:
                return build_validation_result(
                    False,
                    "investment_amount",
                    "No you are not going anywhere poor fella "
                    "please come back to me if you plan to invest more than 10000.",
                )

        ### YOUR DATA VALIDATION CODE ENDS HERE ###

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE STARTS HERE ###
    
    amount_gained = investment_amount * (10/100)
    
    initial_recommendation = 'no option'
    if amount_gained < 0:
        initial_recommendation = """Oh dear Hounds of Hodl, seems like you wont be getting very far at all, you made a loss of {} ...Hmm you might want to consider swimming there.""".format(amount_gained)
    elif amount_gained > 0 and amount_gained < 10000:
        initial_recommendation = """You’ve just scratched in a profit Hounds of Hodl, you made {}, seems like you’ll be enjoying the fresh air of the open seas, in a dingy with oars""".format(amount_gained)
    elif amount_gained >= 10000 and amount_gained > 100000:
        initial_recommendation = """Well done Hounds of Hodl, you generated a profit of {} , you’ll might get to the Carribean if you don’t mind the cramped living quarters and a shared bedroom """.format(amount_gained)
    elif amount_gained >= 100000 and amount_gained < 500000:
        initial_recommendation = """Well done Hounds of Hodl, you generated a profit of {} , not sure about luxury, but you will all get to the Carribean """.format(amount_gained)
    elif amount_gained >= 500000 :
        initial_recommendation = """Well done Hounds of Hodl, you are indeed the real wolves of wall street, you generated a grand profit of {} , it looks like you will be travelling to the Caribean in true style on your very own private 80ft cruiser. Shall I make you a drink to celebrate?""".format(amount_gained)
    else :
        initial_recommendation ="sorry can't tell"
    #return initial_recommendation


    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE ENDS HERE ###

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": initial_recommendation
        },
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "return_outcome":
        return return_outcome(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
