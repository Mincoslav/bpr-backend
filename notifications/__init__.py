from exponent_server_sdk import (
    PushClient,
    PushMessage,
    PushTicket,
    DeviceNotRegisteredError,
    PushTicketError,
)

# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# FIREBASE_CONFIG = os.environ.get("FIREBASE_CONFIG")
# cred = credentials.Certificate("C:/Users/minco/OneDrive/Desktop/vs-code-projects/bpr-backend/firebase_funcs/firebase_service_account.json")


def send_push_message(token, message, data=None):
    response: PushTicket = PushClient().publish(
        PushMessage(to=token, body=message, data=data)
    )

    try:
        print(response)
        return response.is_success

    except DeviceNotRegisteredError:
        # TODO: Invalidate the token as innactive
        return True

    except PushTicketError as error:
        return {
            "token": token,
            "message": message,
            "data": data,
            "push_response": dict(error.push_response()),
        }
    
    except ValueError as v_err:
        print(v_err)
