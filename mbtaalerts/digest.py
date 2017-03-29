class AlertGrouping:
    def __init__(self, alert_obj, event_list):
        self.alert_obj = alert_obj
        self.event_list = event_list

    def __init__(self, event_list):
        self.event_list = event_list

class AlertObj:
    def __init__(self, alert_obj):
        self.alert_obj = alert_obj

class event:
    def __init__(self, json):
        self.event = json