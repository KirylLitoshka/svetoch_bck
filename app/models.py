from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Model:
    def __init__(self, *args, **kwargs):
        self.__table__ = None

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Renter(Base, Model):
    __tablename__ = "renters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    agreement = Column(String, nullable=True)
    legal_address = Column(String, nullable=True)
    mail_address = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    def __init__(self, name, agreement, legal_address, phone, *args, **kwargs):
        self.name = name
        self.agreement = agreement
        self.legal_address = legal_address
        self.phone = phone
        if not kwargs.get("mail_address", None):
            self.mail_address = self.legal_address
        else:
            self.mail_address = kwargs.get("mail_address")
        super(Renter, self).__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__}({self.name}, {self.legal_address}, {self.phone}, {self.subsystem_id})"
