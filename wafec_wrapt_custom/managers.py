import requests
import json
import logging

LOG = logging.getLogger(__name__)


class DataEvent(object):
    def __init__(self, source, event_name, value, data_type, is_callable):
        self.source = str(source)
        self.event_name = str(event_name)
        self.value = str(value)
        self.data_type = str(data_type)
        self.is_callable = is_callable


class DataManagerAdapter(object):
    def notify(self, data_event):
        pass


class DataManager(object):
    def __init__(self, api_uri):
        self._api_uri = api_uri

    def notify(self, data_event):
        try:
            data = {
                'source': data_event.source,
                'event_name': data_event.event_name,
                'value': data_event.value,
                'is_callable': data_event.is_callable,
                'data_type': data_event.data_type
            }
            headers = {
                'Content-Type': 'application/json'
            }
            requests.post(self._api_uri, data=json.dumps(data), headers=headers)
        except Exception as exc:
            LOG.exception(str(exc))
