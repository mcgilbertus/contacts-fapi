from sqlalchemy import select, column
from sqlalchemy.orm import Session

from data.entities.ContactoBd import ContactoBd
from domain.Contacto import ContactoSinId


class ContactosRepository:
    def get_all(self, db: Session):
        return db.query(ContactoBd).all()

    def get_by_id(self, db: Session, id: int):
        return db.execute(select(ContactoBd).where(ContactoBd.id == id)).scalar()

    def agregar(self, db: Session, datos: ContactoSinId):
        cto = ContactoBd(**datos.model_dump(exclude_none=True))
        db.add(cto)
        db.commit()
        return cto

    def buscar_contacto(self, db: Session, id: int):
        cto = db.get(ContactoBd, id)
        return cto

    def actualizar(self, db: Session, id: int, datos: ContactoSinId):
        cto = self.buscar_contacto(db, id)
        if not cto:
            return None
        for k, v in datos.dict(exclude_unset=True).items():
            setattr(cto, k, v)
        db.commit()
        return cto

    def borrar(self, db: Session, id: int):
        cto = self.buscar_contacto(db, id)
        if not cto:
            return None
        db.delete(cto)
        db.commit()
        return cto
