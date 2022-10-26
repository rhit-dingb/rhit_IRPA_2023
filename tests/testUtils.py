def createEntityObjHelper(entityValue, entityLabel="none",  entityRole=None):
        res = {"entity": entityLabel, "value": entityValue}
        if (entityRole):
            res["role"] = entityRole

        return res


def createFakeTracker(intent, entities):

    tracker = {
        "latest_message": {
            "intent": {
                "name": intent
            },
            "entities": entities,
            "text": None,
            "message_id": None,
            "metadata": {}
        },
        "sender_id": "someone",
        "slots": {
        "AA_CONTINUE_FORM": None,
        "PERSON": None,
        "account_type": None,
        "amount-of-money": None,
        "amount_transferred":None,
        "credit_card": None,
        "currency": None,
        "end_time": None,
        "end_time_formatted": None,
        "grain": None,
        "handoff_to": None,
        "next_form_name": None,
        "number": None,
        "payment_amount_type": None,
        "previous_form_name": None,
        "repeated_validation_failures": None,
        "requested_slot": None,
        "search_type": None,
        "start_time": None,
        "start_time_formatted": None,
        "time": None,
        "time_formatted": None,
        "vendor_name": None,
        "zz_confirm_form": None
        },
        "latest_event_time": 1607396994.449022,
        "followup_action": None,
        "paused": False,
        "events": [
            {
            "event": "action",
            "timestamp": 1607396994.448949,
            "name": "action_session_start",
            "policy": None,
            "confidence": 1.0
            },
            {
            "event": "session_started",
            "timestamp": 1607396994.44901
            },
            {
            "event": "action",
            "timestamp": 1607396994.449022,
            "name": "action_listen",
            "policy": None,
            "confidence": None
            }
        ],
        "latest_input_channel": None,
        "active_loop": {},
        "latest_action": {
            "action_name": "action_listen"
        },
        "latest_action_name": "action_listen"

    }

    return tracker