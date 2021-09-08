from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class DisabilitiesSchema(SQLModel):
    ObjectId: int
    DiscountList: List[str]


class Disabledfacilitie(SQLModel, table=True):
    __tablename__ = 'disabledfacilities'

    DFId: Optional[int] = Field(default=None, primary_key=True)
    DFObjectId: int = Field(default=None, foreign_key="objects.ObjectId")
    DFType: int = Field(default=None, foreign_key="dftypes.DFTId")
    object: "Object" = Relationship(back_populates="dftypes_link")
    dftype: "Dftype" = Relationship(back_populates="objects_link")


class Discount(SQLModel, table=True):
    __tablename__ = 'discounts'

    DSId: Optional[int] = Field(default=None, primary_key=True)
    ObjectId: int = Field(default=None, foreign_key="objects.ObjectId")
    DSType: int = Field(default=None, foreign_key="dstypes.DSTId")

    object: "Object" = Relationship(back_populates="dstypes_link")
    dstype: "Dstype" = Relationship(back_populates="objects_link")


class Dftype(SQLModel, table=True):
    __tablename__ = 'dftypes'

    DFTId: int = Field(default=None, primary_key=True)
    DFTDesc: str

    objects_link: List[Disabledfacilitie] = Relationship(back_populates="dftype")


class Dstype(SQLModel, table=True):
    __tablename__ = 'dstypes'

    DSTId: Optional[int] = Field(default=None, primary_key=True)
    DSTDesc: str

    objects_link: List[Discount] = Relationship(back_populates="dstype")


class BaseObject(SQLModel):
    ObjectId: Optional[int] = Field(default=None, primary_key=True)
    Name: str
    Description: str
    ImagePath: str
    Longitude: float
    Latitude: float


class Object(BaseObject, table=True):
    __tablename__ = 'objects'

    EasyAcces: bool
    FreeEntry: bool
    FreeParking: Optional[bool] = None
    GMapLink: str
    OPMapLink: Optional[str] = None

    dftypes_link: List[Disabledfacilitie] = Relationship(back_populates="object")
    dstypes_link: List[Discount] = Relationship(back_populates="object")
