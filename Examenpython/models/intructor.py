from mongoengine import * 
from models.sena import NombreSena

class NombreIntructor(Document):
    nombrecompleto =StringField(max_length=80,required=True)
    correoelectronico =StringField(max_length=80,required=True)
    centro = ReferenceField(NombreSena, required=True)
    
    def _repr__(self):
        return self.nombrecompleto