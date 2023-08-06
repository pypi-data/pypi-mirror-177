from datetime import datetime


class GenericLog(object):
    timespan: datetime
    input_type: str
    origin: str
    message: str
    ip_address: str
    additional_information: str
    tags: [str]

    def __init__(self, input_type, origin, message, ip_address, additional_information, tags):
        self.input_type = input_type
        self.timespan = datetime.now()
        self.origin = origin
        self.message = message
        self.ip_address = ip_address
        self.additional_information = additional_information
        self.tags = tags
