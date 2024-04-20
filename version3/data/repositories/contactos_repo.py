from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session

from data.entities.modelos_bd import ContactoBd
from domain.Contactos import ContactoSinId
from domain.exceptions.NotFound import NotFoundError


class ContactosRepo:
    def get_all(self, db: Session) -> Sequence[ContactoBd]:
        return db.scalars(select(ContactoBd)).all()

    def get_by_id(self, db: Session, id: int) -> ContactoBd:
        result = db.get(ContactoBd, id)
        if result is None:
            raise NotFoundError(f'Contacto [{id}] no encontrado')
        return result

    def agregar(self, db: Session, datos: ContactoSinId) -> ContactoBd:
        cto = ContactoBd(**datos.model_dump(exclude_none=True))
        db.add(cto)
        db.commit()
        return cto

    def actualizar(self, db: Session, id: int, datos: ContactoSinId) -> ContactoBd:
        cto = self.get_by_id(db, id)
        for k, v in datos.dict(exclude_unset=True).items():
            setattr(cto, k, v)
        db.commit()
        return cto

    def borrar(self, db: Session, id: int) -> ContactoBd:
        cto = self.get_by_id(db, id)
        db.delete(cto)
        db.commit()
        return cto

    def get_all_count(self, db: Session) -> int:
        return db.query(ContactoBd).count()
