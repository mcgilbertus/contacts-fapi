"""
Indica que no se encontró un recurso solicitado.
"""
class NotFoundError(Exception):

    def __init__(self, message):
        super().__init__(message)
        # eventualmente, podemos crear otras excepciones para distintos codigos de estado
        self._status_code = 404

    @property
    def status_code(self):
        # Codigo de estado (solo lectura)
        return self._status_code
