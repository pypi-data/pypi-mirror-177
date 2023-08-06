class ErrorCodes:
    SMS_SEND_ERROR = 'Sms couldn\'t send!'
    APPLICATION_ID_ERROR = 'You must set application id!'
    AWS_ACCESS_KEY_ERROR = 'You must set aws access key id!'
    AWS_SECRET_KEY_ERROR = 'You must set aws secret access key!'
    DESTINATION_NUMBER_ERROR = 'You must set phone number to send sms!'
    MESSAGE_ERROR = 'You must set message which you want to send as sms!'


class PinPointException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
