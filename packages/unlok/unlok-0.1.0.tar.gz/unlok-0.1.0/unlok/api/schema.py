from typing import List, Optional, Literal
from unlok.funcs import execute, aexecute
from unlok.rath import LokRath
from rath.scalars import ID
from pydantic import BaseModel, Field
from enum import Enum


class ApplicationClientType(str, Enum):
    """An enumeration."""

    CONFIDENTIAL = "CONFIDENTIAL"
    "Confidential"
    PUBLIC = "PUBLIC"
    "Public"


class ApplicationAuthorizationGrantType(str, Enum):
    """An enumeration."""

    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"
    "Authorization code"
    IMPLICIT = "IMPLICIT"
    "Implicit"
    PASSWORD = "PASSWORD"
    "Resource owner password-based"
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    "Client credentials"
    OPENID_HYBRID = "OPENID_HYBRID"
    "OpenID connect hybrid"


class ApplicationAlgorithm(str, Enum):
    """An enumeration."""

    A_ = "A_"
    "No OIDC support"
    RS256 = "RS256"
    "RSA with SHA-2 256"
    HS256 = "HS256"
    "HMAC with SHA-2 256"


class FaktApplicationKind(str, Enum):
    """An enumeration."""

    WEBSITE = "WEBSITE"
    "Website"
    DESKTOP = "DESKTOP"
    "Dekstop"
    USER = "USER"
    "User"


class GrantType(str, Enum):
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    IMPLICIT = "IMPLICIT"
    PASSWORD = "PASSWORD"
    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"


class PublicFaktType(str, Enum):
    DEKSTOP = "DEKSTOP"
    WEBSITE = "WEBSITE"


class ScopeFragment(BaseModel):
    typename: Optional[Literal["Scope"]] = Field(alias="__typename")
    value: str
    label: str
    description: Optional[str]

    class Config:
        frozen = True


class UserFragmentProfile(BaseModel):
    typename: Optional[Literal["Profile"]] = Field(alias="__typename")
    avatar: Optional[str]

    class Config:
        frozen = True


class UserFragment(BaseModel):
    typename: Optional[Literal["HerreUser"]] = Field(alias="__typename")
    id: ID
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    email: str
    profile: Optional[UserFragmentProfile]

    class Config:
        frozen = True


class Get_scopesQuery(BaseModel):
    scopes: Optional[List[Optional[ScopeFragment]]]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment Scope on Scope {\n  value\n  label\n  description\n}\n\nquery get_scopes {\n  scopes {\n    ...Scope\n  }\n}"

    class Config:
        frozen = True


class Aget_scopeQuery(BaseModel):
    scope: Optional[ScopeFragment]

    class Arguments(BaseModel):
        id: str

    class Meta:
        document = "fragment Scope on Scope {\n  value\n  label\n  description\n}\n\nquery aget_scope($id: String!) {\n  scope(key: $id) {\n    ...Scope\n  }\n}"

    class Config:
        frozen = True


class Search_scopesQuery(BaseModel):
    scopes: Optional[List[Optional[ScopeFragment]]]

    class Arguments(BaseModel):
        search: Optional[str] = None

    class Meta:
        document = "fragment Scope on Scope {\n  value\n  label\n  description\n}\n\nquery search_scopes($search: String) {\n  scopes(search: $search) {\n    ...Scope\n  }\n}"

    class Config:
        frozen = True


class MeQuery(BaseModel):
    me: Optional[UserFragment]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment User on HerreUser {\n  id\n  username\n  email\n  profile {\n    avatar\n  }\n}\n\nquery me {\n  me {\n    ...User\n  }\n}"

    class Config:
        frozen = True


async def aget_scopes(rath: LokRath = None) -> Optional[List[Optional[ScopeFragment]]]:
    """get_scopes



    Arguments:
        rath (lok.rath.LokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ScopeFragment]]]"""
    return (await aexecute(Get_scopesQuery, {}, rath=rath)).scopes


def get_scopes(rath: LokRath = None) -> Optional[List[Optional[ScopeFragment]]]:
    """get_scopes



    Arguments:
        rath (lok.rath.LokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ScopeFragment]]]"""
    return execute(Get_scopesQuery, {}, rath=rath).scopes


async def aaget_scope(id: str, rath: LokRath = None) -> Optional[ScopeFragment]:
    """aget_scope



    Arguments:
        id (str): id
        rath (lok.rath.LokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[ScopeFragment]"""
    return (await aexecute(Aget_scopeQuery, {"id": id}, rath=rath)).scope


def aget_scope(id: str, rath: LokRath = None) -> Optional[ScopeFragment]:
    """aget_scope



    Arguments:
        id (str): id
        rath (lok.rath.LokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[ScopeFragment]"""
    return execute(Aget_scopeQuery, {"id": id}, rath=rath).scope


async def asearch_scopes(
    search: Optional[str] = None, rath: LokRath = None
) -> Optional[List[Optional[ScopeFragment]]]:
    """search_scopes



    Arguments:
        search (Optional[str], optional): search.
        rath (lok.rath.LokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ScopeFragment]]]"""
    return (await aexecute(Search_scopesQuery, {"search": search}, rath=rath)).scopes


def search_scopes(
    search: Optional[str] = None, rath: LokRath = None
) -> Optional[List[Optional[ScopeFragment]]]:
    """search_scopes



    Arguments:
        search (Optional[str], optional): search.
        rath (lok.rath.LokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ScopeFragment]]]"""
    return execute(Search_scopesQuery, {"search": search}, rath=rath).scopes


async def ame(rath: LokRath = None) -> Optional[UserFragment]:
    """me



    Arguments:
        rath (lok.rath.LokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[UserFragment]"""
    return (await aexecute(MeQuery, {}, rath=rath)).me


def me(rath: LokRath = None) -> Optional[UserFragment]:
    """me



    Arguments:
        rath (lok.rath.LokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[UserFragment]"""
    return execute(MeQuery, {}, rath=rath).me
