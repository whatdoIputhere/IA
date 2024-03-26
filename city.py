class City:
    def __init__(self, name, location):
        self.name = name
        self.connections = []
        self.latitude = location[0]
        self.longitude = location[1]
        
    def __str__(self):
        return f'{self.name} ({self.latitude},{self.longitude}) -> {self.connections}'
    
    def getName(self):
        return self.name

    def getConnections(self):
        return self.connections
    
    def printConnections(self):
        print(f"{self.name} has {len(self.connections)} connections.")
        for connection in self.connections:
            print(f"{connection['name']} ({connection['distance']})", end=", ")
        print("\n")

    def getNumberOfConnections(self):
        return len(self.connections)
    
    def addConnection(self, connection):
        #print(f"Adding connection {connection} to {self.name}")
        self.connections.append(connection)
