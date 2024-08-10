from typing import Optional

from pydantic import Field

from api.v1.models.contacto_modelos import ContactoDetailModel, ContactoUpdateModel


# region Details
class ContactoDetailV2Model(ContactoDetailModel):
    nrodoc: Optional[str] = Field(default=None, description='Número de documento')


# endregion

class ContactoUpdateV2Model(ContactoUpdateModel):
    nrodoc: Optional[str] = Field(default=None, description='Número de documento')


class ContactoCreateV2Model(ContactoUpdateV2Model):
    pass

# endregion
