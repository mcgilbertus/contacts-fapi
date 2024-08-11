from typing import Optional

from pydantic import Field

from api.v1.models.contacto_modelos import ContactoDetailModel, ContactoUpdateModel

#### api/v2/models/contacto_modelos_v2.py

class ContactoDetailV2Model(ContactoDetailModel):
    nrodoc: Optional[str] = Field(default=None, description='Número de documento')


class ContactoUpdateV2Model(ContactoUpdateModel):
    nrodoc: Optional[str] = Field(default=None, description='Número de documento')


class ContactoCreateV2Model(ContactoUpdateV2Model):
    pass

