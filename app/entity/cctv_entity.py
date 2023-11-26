from dataclasses import dataclass

@dataclass
class CCTVEntity:
    def __init__(self, id, name, scheme, ip, port, username, password):
        self.id = id
        self.name = name
        self.scheme = scheme
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def get_connection_string(self):
        if self.scheme == 'file':
             return self.ip
        
        if self.username is None:
            return f"{self.scheme}://{self.ip}:{self.port}"
        return f"{self.scheme}://{self.username}:{self.password}@{self.ip}:{self.port}"
    
    