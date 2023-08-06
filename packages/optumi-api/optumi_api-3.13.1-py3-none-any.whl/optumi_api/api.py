##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .LoginServer import login as oauth_login
from .HoldoverTime import HoldoverTime
from requests.exceptions import ConnectionError

import phonenumbers

# Generic Operating System Services
import datetime, json
from typing import Union

# Optumi imports
import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    ServiceException,
    OptumiException,
)


def login(
    connection_token=None, dnsName=optumi.login.PORTAL, port=optumi.login.PORTAL_PORT
):
    if not optumi.login.check_login(dnsName, port, mode="api"):
        if connection_token == None:
            login_status, message = optumi.login.login_rest_server(
                dnsName, port, oauth_login(), mode="api", login_type="oauth"
            )
            if login_status != 1:
                raise NotLoggedInException("Login failed: " + message)
        else:
            login_status, message = optumi.login.login_rest_server(
                dnsName, port, connection_token, mode="api", login_type="token"
            )
            if login_status != 1:
                raise NotLoggedInException("Login failed: " + message)
        ## This is currently necessary in order for the controller to recognize that the user has signed the agreement
        optumi.login.get_new_agreement()


def logout():
    try:
        optumi.login.logout()
    except NotLoggedInException:
        pass


def get_phone_number():
    return json.loads(optumi.core.get_user_information(False).text)["phoneNumber"]


def set_phone_number(phone_number: str):
    if phone_number == "":
        optumi.core.set_user_information("phoneNumber", "")
    else:
        number = phonenumbers.parse(phone_number, "US")
        if not phonenumbers.is_valid_number(number):
            raise OptumiException(
                "The string supplied did not seem to be a valid phone number."
            )
        optumi.core.set_user_information(
            "phoneNumber",
            phonenumbers.format_number(
                number, phonenumbers.PhoneNumberFormat.E164
            ).replace("+", ""),
        )


def get_holdover_time():
    res = optumi.core.get_user_information(False)
    return HoldoverTime(
        int(
            json.loads(optumi.core.get_user_information(False).text)["userHoldoverTime"]
        )
        // 60  # Convert to minutes
    )


def set_holdover_time(holdover_time: Union[int, HoldoverTime]):
    optumi.core.set_user_information(
        "userHoldoverTime",
        str(
            holdover_time.seconds
            if type(holdover_time) is HoldoverTime
            else holdover_time * 60  # Convert to seconds
        ),
    )


def get_connection_token():
    return json.loads(optumi.core.get_connection_token().text)


def redeem_signup_code(signupCode):
    optumi.core.redeem_signup_code(signupCode)
