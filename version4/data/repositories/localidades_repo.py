from sqlalchemy import select, Sequence, Row
from sqlalchemy.orm import Session

from domain.exceptions.NotFound import NotFoundError
from domain.model.localidad import Localidad
from domain.model.provincia import Provincia


class LocalidadesRepo:
    """
    Repositorio de localidades, en base de datos
    """

    # region Métodos CRUD
    def get_all(self, db: Session) -> Sequence[Row]:
        """
        Devuelve la lista completa de Localidades
        :return: list[Row]. Lista de los campos de localidad mas el nombre de la provincia
        """
        result = db.execute(select(Localidad.id, Localidad.nombre, Provincia.nombre.label('provincia'))
                            .outerjoin(Provincia, Localidad.provincia_id == Provincia.id)).all()
        return result

    def get_by_id(self, db: Session, id: int) -> Localidad:
        """
        Busca una Localidad por id
        :param id: int. El id a buscar
        :return: Localidad. La Localidad encontrada.
        """
        result = db.get(Localidad, id)
        if result is None:
            raise NotFoundError(f'Localidad [{id}] no encontrada')
        return result

    def agregar(self, db: Session, datos: Localidad) -> Localidad:
        """
        Agrega una nueva Localidad a la lista
        :param data: LocalidadesinId. Datos de la Localidad a agregar. El id se asignará automáticamente
        :return: Localidad. La Localidad agregada, con el id asignado
        """
        db.add(datos)
        db.commit()
        return datos

    def editar(self, db: Session, id: int, datos: dict) -> Localidad:
        """
        Reemplaza los valores de una Localidad existente por los nuevos valores
        :param id: int. Id de la Localidad a editar
        :param data: LocalidadesinId. Datos nuevos de la Localidad. El id no se modifica
        :return: Localidad. La Localidad actualizada
        """
        cto = self.get_by_id(db, id)
        for k, v in datos.items():
            setattr(cto, k, v)
        db.commit()
        return cto

    def borrar(self, db: Session, id: int) -> None:
        """
        Borra una Localidad de la lista
        :param id: int. Id de la Localidad a borrar
        :return: None. Si la Localidad se encuentra en la lista, se elmimina.
        """
        cto = self.get_by_id(db, id)
        db.delete(cto)
        db.commit()

    # endregion

    # region otros metodos
    def get_all_locs_of_prov(self, db: Session, prov_id: int) -> Sequence[Localidad]:
        """
        Devuelve la lista de Localidades de una Provincia
        :param prov_id: int. Id de la Provincia
        :return: list[Localidad]. Lista de Localidades
        """
        return db.scalars(select(Localidad).where(Localidad.provincia_id == prov_id)).all()

    def get_all_count(self, db: Session) -> int:
        """
        Devuelve la cantidad de Localidades en la tabla
        :return: int, cantidad de Localidades
        """
        return db.query(Localidad).count()
    # endregion
