from dataclasses import dataclass

@dataclass
class Data:
    title: str  = "Titulo",
    description: str = "Sin descripcion",
    color: str = "red"
    image: str = None,
    url: str = None,
    thumbnail: str = None
    
    def dict(self):
        return self.__dict__

    

    
    
d = Data(title="AAA")
print(**d)