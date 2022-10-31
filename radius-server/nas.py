class nas():
    def __init__(self,nas_ip,nas_name,password):
        self._nas_ip = nas_ip
        self._nas_name = nas_name
        self._password = password

    def getNasIP(self):
        return self._nas_ip

    def getNasName(self):
        return self._nas_name

    def getNasPassword(self):
        return self._password
