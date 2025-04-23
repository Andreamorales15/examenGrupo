from mongoengine import Document, StringField, DateField, ReferenceField
from models.intructor import NombreIntructor

class Guia(Document):
    nombreguia = StringField(max_length=100, required=True)
    descripcion = StringField(required=True)
    programaformacion = StringField(max_length=100, required=True)
    documento = StringField(required=True)
    fecha = DateField(required=True)
    instructor = ReferenceField(NombreIntructor, required=True)

    
    def __repr__(self):
        return f"<Guia {self.nombreguia}>"