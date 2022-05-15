from fastapi import HTTPException
from exponent_server_sdk import (
    PushClient,
    PushMessage,
    PushTicket,
    DeviceNotRegisteredError,
    PushTicketError,
)
from starlette.status import HTTP_418_IM_A_TEAPOT

# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# FIREBASE_CONFIG = os.environ.get("FIREBASE_CONFIG")
# cred = credentials.Certificate("C:/Users/minco/OneDrive/Desktop/vs-code-projects/bpr-backend/firebase_funcs/firebase_service_account.json")


def send_push_message(token, message, data=None):
    # if "ExponentPushToken[" not in token:
    #     token = "ExponentPushToken[" + token + "]"
    response: PushTicket = PushClient().publish(
        PushMessage(to=token, body=message, data=data)
    )

    try:
        print(response)
        return response.is_success

    except DeviceNotRegisteredError:
        # TODO: Invalidate the token as innactive
        return HTTPException(
            status_code=HTTP_418_IM_A_TEAPOT,
            detail="Device with token {token} not registered".format(token=token),
        )

    except PushTicketError as error:
        return {
            "token": token,
            "message": message,
            "data": data,
            "push_response": dict(error.push_response()),
        }

    except ValueError as v_err:
        print(v_err)
