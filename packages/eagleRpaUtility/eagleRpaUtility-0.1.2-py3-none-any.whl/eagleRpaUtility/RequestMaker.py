import json
import requests

from dataclasses import dataclass

@dataclass
class RequestMaker():
    session: requests.Session = requests.Session()
    protocol: str = None
    host: str = None
    port: int = 443 if protocol=="https" else 80
    timeout: int = 7

    def setHostParameter(self, protocol: str, host: str):
        self.protocol = protocol
        self.host = host

    def clearSession(self) -> None:
        self.session.cookies.clear()
        self.session.headers.clear()

    def updateHeaders(self, new_headers: dict) -> None:
        self.session.headers.update(new_headers)

    def updateCookies(self, cookies = dict) -> None:
        self.session.cookies.update(cookies)

    def makeRequest(self, method:str, url:str = None, endpoint:str = None, params:dict = None, data:dict = None, json_data:dict = None) -> dict:
        info = {"error": False}
        if endpoint:
            url=f"{self.protocol}://{self.host}:{str(self.port)}/{endpoint}"
            if not (self.protocol and self.host):
                raise MissingParameter("Must set protocol and host before using endpoint parameter.")
        if not (url or endpoint):
            raise MissingParameter("Must pass url or endpoint.")
        try:
            response = self.session.request(method, url, params=params, data=data, json=json_data,timeout=self.timeout)
            info["status_code"] = response.status_code
            if not response.ok:
                info["error"] = True
                info["error_message"] = "Status code not 200."
            if not response.headers.get("content-type"):
                info["response"] = response.content
            elif "html" in response.headers["content-type"]:
                info["response"] = response.text
            elif "text" in response.headers["content-type"]:
                info["response"] = response.text
            elif "json" in response.headers["content-type"]:
                try:
                    info["response"] = response.json()
                except json.decoder.JSONDecodeError:
                    info["error"] = True
                    info["error_message"] = "Invalid response."
            else:
                info["response"] = response.content
        except requests.exceptions.Timeout:
                info["error"] = True
                info["error_message"] = "Connection timed out, retry."
        except requests.exceptions.ConnectionError:
            info["error"] = True
            info["error_message"] = "Connection error."
        except requests.exceptions.RequestException as e:
            info["error"] = True
            info["error_message"] = f"Request excpetion: {e}"
        return info

class MissingParameter(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message