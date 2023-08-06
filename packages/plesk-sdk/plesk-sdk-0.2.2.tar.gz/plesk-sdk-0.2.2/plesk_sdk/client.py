import requests
import json
from typing import Dict, List

from .patterns import Singleton


class Client(metaclass=Singleton):

    def __init__(self, plesk_url: str, api_key: str) -> None:
        """
        :param plesk_url: str - Base endpoint of Plesk Service
        :param api_key: str - api_key is required for use Plesk Service.
        :return: None
        """

        self.plesk_url = f"{plesk_url}/api/v2"
        self.API_KEY = api_key
        self.headers = {"Content-Type": "application/json"}

    def request_config(self) -> Dict:
        return {"verify": False, "headers": self.get_headers()}

    def get_headers(self) -> Dict:
        self.headers.update({"X-API-Key": self.API_KEY})

        return self.headers

    def get_response(self, resp: requests.Response) -> Dict:
        if not str(resp.status_code).startswith("2"):
            raise ValueError("API Error: ", resp.content)

        response = resp.json()

        if response.get('code') != 0 and response.get('code'):
            raise ValueError("API Error: ", response["stderr"])

        return response 

    def subscription_off(self, subscription_name: str) -> Dict:
        """
        Suspends a whole subscription.

        :param subscription_name: str - Accepts a domain name
        :return: Dict - {'code': 0, 'stdout': '', 'stderr': ''}
        """

        params = ["--webspace-off", subscription_name]

        resp = requests.post(
            f"{self.plesk_url}/cli/subscription/call",
            data=json.dumps({"params": params}),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def subscription_on(self, subscription_name: str) -> Dict:
        """
        Activates a whole subscription.

        :param subscription_name:  str - Accepts a domain name
        :return: Dict - {'code': 0, 'stdout': '', 'stderr': ''}
        """

        params = ["--webspace-on", subscription_name]

        resp = requests.post(
            f"{self.plesk_url}/cli/subscription/call",
            data=json.dumps({"params": params}),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def kwargs_to_list(self, kwargs: Dict) -> List[str]:
        params = []
        for item in kwargs.items():
            key, value = item
            params.extend([f"-{key}", value])

        return params

    def subscription_create(self, subscription_name: str, **kwargs) -> Dict:
        """
        Creates a subscription.

        :param subscription_name: str - Accepts a domain name
        :param kwargs: Dict - must contain owner, service-plan, login, ip, passwd
        :return: -> Dict - {'code': 0, 'stdout': "SUCCESS: Creation of domain '<subscription_name>' completed.", 'stderr': ''}
        """

        params = ["--create", subscription_name]
        params.extend(self.kwargs_to_list(kwargs=kwargs))

        resp = requests.post(
            url=f"{self.plesk_url}/cli/subscription/call",
            data=json.dumps({"params": params}),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def subscription_remove(self, subscription_name: str) -> Dict:
        """
        Remove a subscription.

        :param subscription_name: str - Accepts a domain name
        :return: -> Dict - {"code": 0, "stdout": "SUCCESS: Removal of '<subscription_name>' completed.", "stderr": "" }
        """

        params = ["--remove", subscription_name]

        resp = requests.post(
            url=f"{self.plesk_url}/cli/subscription/call",
            data=json.dumps({"params": params}),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def create_customer(self, data: Dict) -> Dict:
        """
        Create a new Customer account

        :param data: Dict - must contain name, login, password, email, type, company, status, locale, owner_login, external_id, description
        :return: Dict - {'id': <id:int>, 'guid': <guid:str>}
        """

        resp = requests.post(
            url=f"{self.plesk_url}/clients",
            data=json.dumps(data),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def update_customer(self, customer_id: int, data: Dict) -> Dict:
        """
        Update a Customer account

        :para customer_id: int - unique id of Customer
        :param data: Dict - fields for changes name, login, password, email, company, status, locale, owner_login, external_id, description
        :return: Dict - {'id': <id:int>, 'guid': <guid:str>}
        """
        resp = requests.put(
            url=f"{self.plesk_url}/clients/{customer_id}",
            data=json.dumps(data),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def customer_activate(self, customer_id: int) -> Dict:
        """
        Update a Customer status to active

        :para customer_id: int - unique id of customer
        :return: Dict - {'id': <id:int>, 'guid': <guid:str>}
        """
        resp = requests.put(
            url=f"{self.plesk_url}/clients/{customer_id}",
            data=json.dumps({"status": 0}),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def customer_suspend(self, customer_id: int) -> Dict:
        """
        Update a Customer status to suspend

        :para customer_id: int - unique id of customer
        :return: Dict - {'id': <id:int>, 'guid': <guid:str>}
        """

        resp = requests.put(
            url=f"{self.plesk_url}/clients/{customer_id}",
            data=json.dumps({"status": 1}),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def get_login_link(self, user: str) -> Dict:
        """
        Generate auto-login link

        :param user: str - username to select a profile
        :return: Dict - {"code": 0,
        "stdout": "https://<server-hostname-or-ip>/login?secret=<secret>",
        "stderr": ""}
        """

        params = ["--get-login-link", "-user", user]

        resp = requests.post(
            url=f"{self.plesk_url}/cli/admin/call",
            data=json.dumps({"params": params}),
            **self.request_config(),
        )

        return self.get_response(resp=resp)

    def get_customer_domains(self, customer_id: int) -> List:
        """
        List of customer domains

        :param customer_id: int
        :return: List - [
          {
            "id": int,
            "name": str,
            "ascii_name": str,
            "hosting_type": str,
            "base_domain_id": int,
            "www_root": str,
            "guid": str,
            "created": str,
            "aliases": [
              {
                "name": str,
                "ascii_name": str,
                "web": bool,
                "dns": bool,
                "mail": bool,
                "seo_redirect": bool
              }
            ]
          }
        ]"""

        resp = requests.get(
            url=f"{self.plesk_url}/clients/{customer_id}/domains",
            **self.request_config(),
        )

        return resp.json()

    def get_domain(self, domain_id: int) -> Dict:
        """
        Domain details

        :param domain_id: int
        :return: Dict - {
          "id": int,
          "name": str,
          "ascii_name": str,
          "hosting_type": str,
          "base_domain_id": int,
          "www_root": str,
          "guid": str,
          "created": str,
          "aliases": [
            {
              "name": str,
              "ascii_name": str,
              "web": bool,
              "dns": bool,
              "mail": bool,
              "seo_redirect": bool
            }
          ]
        }
        """

        resp = requests.get(
            url=f"{self.plesk_url}/domains/{domain_id}",
            **self.request_config(),
        )

        return resp.json()
    
