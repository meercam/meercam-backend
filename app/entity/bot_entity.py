from dataclasses import dataclass

@dataclass
class BotEntity:
    def __init__(self, id, name, scheme, ip, port, username, password):
        self.id = id
        self.name = name
        self.scheme = scheme
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def alert(self, message):
        print(f"{self.name} 봇에게 {message}를 보냄")
        pass