from typing import List

from pydantic import BaseModel


class EnvironmentVariablesIn(BaseModel):
    key: str
    value: str

    class Config:
        orm_mode = True


class EnvironmentVariables(BaseModel):
    key: str
    value: str

    class Config:
        orm_mode = True


class ProfileCoreIn(BaseModel):
    name: str
    environment_variables: List[EnvironmentVariables] = []

    class Config:
        orm_mode = True


class Profile(BaseModel):
    name: str
    environment_variables: List[EnvironmentVariables] = []

    class Config:
        orm_mode = True
