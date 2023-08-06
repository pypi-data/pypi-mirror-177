from streaminglogs import GenericLog


class ActivityLog(GenericLog):
    class_name: str = 'ActivityLog'
    csharp_class_name: str = 'com.lw.common.logging.messages.ActivityLog, com.lw.common.logging.messages'

    def __init__(self, origin, message, ip_address, additional_information, tags):
        super().__init__(self.class_name, origin, message, ip_address, additional_information, tags)

    def as_legacy_dict(self):
        return {
            '$type': self.csharp_class_name,
            'Timespan': self.timespan,
            'Origin': self.origin,
            'Message': self.message,
            'IpAddress': self.ip_address,
            'InputType': self.input_type,
            'AdditionalInformation': self.additional_information,
            'Tags': self.tags
        }
