import datetime

from domain.exceptions.NotFound import NotFoundError
from domain.model.contactos import Contacto, ContactoSinId


class ContactosRepo:
    """
    Repositorio de contactos -en memoria, en esta versión
    """

    def __init__(self):
        """
        Inicializa el repositorio con algunos contactos de prueba
        """
        self.contactos = [Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)),
                          Contacto(id=2, nombre='Contacto2', direccion='dir2'),
                          Contacto(id=3, nombre='Contacto3')]

    # region Métodos suplementarios
    def buscar_contacto(self, id: int) -> (Contacto, int):
        """
        Busca un contacto por id
        :param id: int. Id del contacto a buscar
        :return: Contacto, int. Contacto encontrado y su posición (índice) en la lista
                 Si no se encuentra, lanza una excepción HTTP con código 404
        """
        i, c = next(((i, c) for i, c in enumerate(self.contactos) if c.id == id), (None, None))
        if c is None:
            raise NotFoundError("Contacto no encontrado")
        return c, i

    def get_next_id(self) -> int:
        """
        Devuelve un nuevo id para un contacto, sumando uno al mayor id existente en la lista
        :return: int. Nuevo id
        """
        new_id = 1
        for c in self.contactos:
            if c.id >= new_id:
                new_id = c.id + 1
        return new_id

    # endregion

    # region Métodos CRUD
    def get_all(self) -> list[Contacto]:
        """
        Devuelve la lista completa de contactos
        :return: list[Contacto]. Lista de contactos
        """
        return self.contactos

    def get_by_id(self, id: int) -> Contacto:
        """
        Busca un contacto por id
        :param id: int. El id a buscar
        :return: Contacto. El contacto encontrado.
                 Si no se encuentra, el método buscar_contacto lanzará una excepción NotFoundError
        """
        return self.buscar_contacto(id)[0]

    def agregar(self, data: ContactoSinId) -> Contacto:
        """
        Agrega un nuevo contacto a la lista
        :param data: ContactoSinId. Datos del contacto a agregar. El id se asignará automáticamente
          usando el método get_next_id
        :return: Contacto. El contacto agregado, con el id asignado
        """
        c = Contacto(**data.model_dump(exclude_none=True), id=self.get_next_id())
        self.contactos.append(c)
        return c

    def editar(self, id: int, data: ContactoSinId) -> Contacto:
        """
        Reemplaza los valores de un contacto existente por los nuevos valores
        :param id: int. Id del contacto a editar
        :param data: ContactoSinId. Datos nuevos del contacto. El id no se modifica
        :return: Contacto. El contacto actualizado
        """
        c, i = self.buscar_contacto(id)
        c = c.model_copy(update=data.model_dump(exclude_unset=True))
        self.contactos[i] = c
        return c

    def borrar(self, id: int) -> None:
        """
        Borra un contacto de la lista
        :param id: int. Id del contacto a borrar
        :return: None. Si el contacto se encuentra en la lista, se elmimina.
          Si no se encuentra, el método buscar_contacto lanzará una excepción HTTP con código 404
        """
        c, i = self.buscar_contacto(id)
        self.contactos.remove(c)
    # endregion
