class City:
    def __init__(self, name):
        self.name = name
        self.connections = []
        #location = [latitude, longitude]
        
    def __str__(self):
        return f'{self.name} -> {self.connections}'
    
    def getName(self):
        return self.name

    def getConnections(self):
        return self.connections
    
    def addConnection(self, connection):
        #print(f"Adding connection {connection} to {self.name}")
        self.connections.append(connection)
