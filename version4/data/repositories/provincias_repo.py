from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session

from domain.exceptions.NotFound import NotFoundError
from domain.model.localidad import Localidad
from domain.model.provincia import Provincia


class ProvinciasRepo:
    """
    Repositorio de provincias, en base de datos
    """

    # region Métodos CRUD
    def get_all(self, db: Session) -> Sequence[Provincia]:
        """
        Devuelve la lista completa de Provincias
        :return: list[Provincia]. Lista de Provincias
        """
        return db.scalars(select(Provincia)).all()

    def get_by_id(self, db: Session, id: int) -> Provincia:
        """
        Busca un Provincia por id
        :param id: int. El id a buscar
        :return: Provincia. La Provincia encontrada.
        """
        result = db.get(Provincia, id)
        if result is None:
            raise NotFoundError(f'Provincia [{id}] no encontrada')
        return result

    def agregar(self, db: Session, datos: Provincia) -> Provincia:
        """
        Agrega una nueva Provincia a la lista
        :param data: ProvinciaSinId. Datos de la Provincia a agregar. El id se asignará automáticamente
        :return: Provincia. La Provincia agregada, con el id asignado
        """
        db.add(datos)
        db.commit()
        return datos

    def editar(self, db: Session, id: int, datos: dict) -> Provincia:
        """
        Reemplaza los valores de una Provincia existente por los nuevos valores
        :param id: int. Id de la Provincia a editar
        :param data: ProvinciaSinId. Datos nuevos de la Provincia. El id no se modifica
        :return: Provincia. La Provincia actualizada
        """
        cto = self.get_by_id(db, id)
        for k, v in datos.items():
            setattr(cto, k, v)
        db.commit()
        return cto

    def borrar(self, db: Session, id: int) -> None:
        """
        Borra una Provincia de la lista
        :param id: int. Id de la Provincia a borrar
        :return: None. Si la Provincia se encuentra en la lista, se elmimina.
        """
        cto = self.get_by_id(db, id)
        db.delete(cto)
        db.commit()

    # endregion

    # region otros metodos
    def get_all_count(self, db: Session) -> int:
        """
        Devuelve la cantidad de Provincias en la tabla
        :return: int, cantidad de Provincias
        """
        return db.query(Provincia).count()
    # endregion
