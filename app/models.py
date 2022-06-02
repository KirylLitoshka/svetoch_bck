from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import UniqueConstraint

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
    __table_args__ = (UniqueConstraint("name", "agreement"),)

    def __init__(self, name, agreement="Отсутствует", legal_address=None, phone=None, *args, **kwargs):
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


class Meter(Base, Model):
    __tablename__ = "meters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint("model", "capacity"),)

    def __init__(self, model, capacity, *args, **kwargs):
        self.model = model
        self.capacity = capacity
        super(Meter, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.__class__}({self.model}, {self.capacity})"
