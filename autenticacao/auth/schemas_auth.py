from datetime import datetime

from pydantic import BaseModel, EmailStr, constr

# Pydantic models têm poucos métodos públicos por natureza;
# desabilitamos esta checagem para evitar falso-positivo do pylint.
# pylint: disable=too-few-public-methods


class UserCreate(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    senha: constr(min_length=8, max_length=72)

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    senha: constr(min_length=8, max_length=72)

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_cadastro: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ChangePasswordRequest(BaseModel):
    current_password: constr(min_length=8, max_length=72)
    new_password: constr(min_length=8, max_length=72)

    class Config:
        from_attributes = True
