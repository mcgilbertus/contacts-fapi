from data.entities.modelos_bd import ContactoBd
from domain.Contactos import ContactoSinId
from domain.exceptions.NotFound import NotFoundError
from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session


class ContactosRepo:
    """
    Repositorio de contactos, en base de datos
    """

    # region Métodos CRUD
    def get_all(self, db: Session) -> Sequence[ContactoBd]:
        """
        Devuelve la lista completa de contactos
        :return: list[Contacto]. Lista de contactos
        """
        return db.scalars(select(ContactoBd)).all()

    def get_by_id(self, db: Session, id: int) -> ContactoBd:
        """
        Busca un contacto por id
        :param id: int. El id a buscar
        :return: Contacto. El contacto encontrado.
                 Si no se encuentra, el método buscar_contacto lanzará una excepción NotFoundError
        """
        result = db.get(ContactoBd, id)
        if result is None:
            raise NotFoundError(f'Contacto [{id}] no encontrado')
        return result

    def agregar(self, db: Session, datos: ContactoSinId) -> ContactoBd:
        """
        Agrega un nuevo contacto a la lista
        :param data: ContactoSinId. Datos del contacto a agregar. El id se asignará automáticamente
          usando el método get_next_id
        :return: Contacto. El contacto agregado, con el id asignado
        """
        cto = ContactoBd(**datos.model_dump(exclude_none=True))
        db.add(cto)
        db.commit()
        return cto

    def editar(self, db: Session, id: int, datos: ContactoSinId) -> ContactoBd:
        """
        Reemplaza los valores de un contacto existente por los nuevos valores
        :param id: int. Id del contacto a editar
        :param data: ContactoSinId. Datos nuevos del contacto. El id no se modifica
        :return: Contacto. El contacto actualizado
        """
        cto = self.get_by_id(db, id)
        for k, v in datos.dict(exclude_unset=True).items():
            setattr(cto, k, v)
        db.commit()
        return cto

    def borrar(self, db: Session, id: int) -> ContactoBd:
        """
        Borra un contacto de la lista
        :param id: int. Id del contacto a borrar
        :return: None. Si el contacto se encuentra en la lista, se elmimina.
          Si no se encuentra, el método buscar_contacto lanzará una excepción HTTP con código 404
        """
        cto = self.get_by_id(db, id)
        db.delete(cto)
        db.commit()
        return cto

    # endregion

    # region otros metodos
    def get_all_count(self, db: Session) -> int:
        """
        Devuelve la cantidad de contactos en la tabla
        :return: int, cantidad de contactos
        """
        return db.query(ContactoBd).count()
    # endregion
