from streaminglogs import GenericLog


class ExceptionLog(GenericLog):
    class_name: str = 'ExceptionLog'
    csharp_class_name: str = 'com.lw.common.logging.messages.ExceptionLog, com.lw.common.logging.messages'

    source: str
    stacktrace: str
    inner_message: str

    def __init__(self, origin, source, stacktrace, message, inner_message, ip_address, additional_information, tags):
        super().__init__(self.class_name, origin, message, ip_address, additional_information, tags)
        self.source = source
        self.stacktrace = stacktrace
        self.inner_message = inner_message

    def as_legacy_dict(self):
        return {
            '$type': self.csharp_class_name,
            'Timespan': self.timespan,
            'Origin': self.origin,
            'Source': self.source,
            'Stacktrace': self.stacktrace,
            'Message': self.message,
            'InnerMessage': self.inner_message,
            'IpAddress': self.ip_address,
            'InputType': self.input_type,
            'AdditionalInformation': self.additional_information,
            'Tags': self.tags
        }
