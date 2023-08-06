import os
import atexit
import requests

from logging import INFO
from datetime import datetime
from socket import gethostname, gethostbyname

class CentralizedLogger:
    SERVER_HOST = "https://log.rpa.eagleprojects.it"
    DEAFULT_START = "start"
    DEAFULT_STOP = "stop"

    def __init__(self, buffer_lenght:int =3):
        self.session = requests.Session()
        self.utente = os.getlogin()
        self.hostname = gethostname()
        self.ip = str(gethostbyname(self.hostname))
        self.domain = os.environ["userdomain"]
        self.eagle_domain = self.domain == "EAGLE"
        self.id_run = None
        self.max_buffer_lenght = buffer_lenght
        self.upload_buffer = []
        self.user_info = {
            "user": self.utente,
            "ip": self.ip,
            "hostname": self.hostname,
            "domain": self.domain
        }

    def setupRun(self, automation:str =None, client:str =None, developer:str =None) -> None:
        if not (automation and client and developer):
            raise InstanceError()
        self.automation_info = {
            "name": automation,
            "client": client,
            "developer": developer
        }
        atexit.register(self.flushBuffer)
        self.addRun()

    def uploadInfo(self, endpoint:str, payload:dict) -> bool:
        try:
            request = self.session.post(f"{self.SERVER_HOST}/{endpoint}", json=payload, timeout=3, verify=False)
            if request.ok:
                payload = request.json()
                self.id_run = payload["data"]["id"] if endpoint == "addRun" else self.id_run
                return True
            else:
                raise ResponseNot200(endpoint)
        except requests.exceptions.ConnectionError:
            raise ServerConnectionError()
        except requests.exceptions.Timeout:
            raise ServerConnectionError()
        except Exception as e:
            raise UnknownError(e)
        finally:
            atexit.unregister(self.flushBuffer)

    def addRun(self) -> bool:
        payload = {
            "user_info": self.user_info,
            "automation_info": self.automation_info,
            "timestamp": datetime.now().isoformat()
        }
        return self.uploadInfo("addRun", payload)

    def addLog(self, message:str, level:int = INFO) -> None:
        payload = {
            "id_run": self.id_run,
            "message": message,
            "level": level,
            "timestamp": datetime.now().isoformat()
        }
        self.upload_buffer.append(payload)
        if len(self.upload_buffer) >= self.max_buffer_lenght or message == self.DEAFULT_STOP:
            self.flushBuffer()

    def flushBuffer(self) -> None:
        self.uploadInfo("addLogList", self.upload_buffer)
        self.upload_buffer = []

class InstanceError(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return f"Must pass automation, client and developer name."

class ResponseNot200(Exception):
    def __init__(self, route, *args):
        super().__init__(args)
        self.route = route

    def __str__(self):
        return f"Response status for route {self.route} not 200."

class ServerConnectionError(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Server connection error."

class UnknownError(Exception):
    def __init__(self, e, *args):
        super().__init__(args)
        self.e = e

    def __str__(self):
        return f"Unknown error. Excpetion: {type(self.e).__name__}"