# Python imports
import json
import requests

# Django imports
from django.conf import settings


class PlivoAPI(object):
    """
    API interface for Plivo
    """

    def __init__(self):
        self.SMS_TYPE = "sms"
        self.BASE_URL = "https://api.plivo.com/v1"
        self.AUTH_ID = settings.PLIVO_AUTH_ID
        self.AUTH_TOKEN = settings.PLIVO_AUTH_TOKEN
        self.SRC_NUMBER = settings.PLIVO_SOURCE_NUMBER

    def api_endpoints(self):
        """
        Returns Plivo API endpoints
        """
        send_sms_url = "/".join([self.BASE_URL, 'Account/%s/Message/' % self.AUTH_ID])
        end_points = {'send_sms': send_sms_url}
        return end_points

    def api_url(self, url_key):
        """
        Returns Plivo API url
        """
        dic = self.api_endpoints()
        return dic.get(url_key)

    def make_post_request(self, url, data):
        """
        HTTP POST requestand returns response
        """
        auth = (self.AUTH_ID, self.AUTH_TOKEN)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=data, auth=auth, headers=headers)

    def send_sms(self, sms_text, des_number):
        """
        Send SMS

        sms_text: length 160 characters, longer sms will be split.
        """
        data = {'src': self.SRC_NUMBER, 'dst': des_number,
                'text': sms_text, 'type': self.SMS_TYPE}
        response = self.make_post_request(self.api_url('send_sms'), json.dumps(data))
