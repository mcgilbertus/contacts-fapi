import datetime
from fastapi import HTTPException, status

from domain.model.Contactos import Contacto, ContactoSinId


class ContactosRepo:
    def __init__(self):
        self.contactos = [Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)),
                          Contacto(id=2, nombre='Contacto2', direccion='dir2'),
                          Contacto(id=3, nombre='Contacto3')]

    def buscar_contacto(self, id):
        i, c = next(((i, c) for i, c in enumerate(self.contactos) if c.id == id), (None, None))
        if c is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")
        return c, i

    def get_next_id(self):
        new_id = 1
        for c in self.contactos:
            if c.id >= new_id:
                new_id = c.id + 1
        return new_id

    def get_all(self):
        return self.contactos

    def get_by_id(self, id):
        return self.buscar_contacto(id)

    def agregar(self, data: ContactoSinId):
        c = Contacto(**data.model_dump(exclude_none=True), id=self.get_next_id())
        self.contactos.append(c)
        return c

    def editar(self, id: int, data: ContactoSinId):
        c, i = self.buscar_contacto(id)
        c = c.model_copy(update=data.model_dump(exclude_unset=True))
        self.contactos[i] = c
        return c

    def borrar(self, id):
        c, i = self.buscar_contacto(id)
        self.contactos.remove(c)
