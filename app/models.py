from email.policy import default
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import date

Base = declarative_base()


class Subsystem(Base):
    __tablename__ = "subsystems"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    alt_name = Column(String, unique=True, nullable=False)
    current_date = Column(Date, default=date.today())

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, name, alt_name, *args, **kwargs):
        self.name = name
        self.alt_name = alt_name
        super(Subsystem, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"Subsystem({self.name}, {self.alt_name})"


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, primary_key=True)
    alt_name = Column(String, nullable=False)
    subsystem_id = Column(Integer, ForeignKey(
        "subsystems.id", ondelete="CASCADE"))
    component = Column(String, unique=True, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, name, alt_name, subsystem_id, *args, **kwargs):
        self.name = name
        self.alt_name = alt_name
        self.subsystem_id = subsystem_id
        if not kwargs.get("component", None):
            self.component = self.name.title()
        else:
            self.component = kwargs.get("component").title()
        super(Service, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.__class__}({self.name}, {self.alt_name}, {self.component})"


class Renter(Base):
    __tablename__ = "renters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    agreement = Column(String, nullable=True)
    legal_address = Column(String, nullable=True)
    mail_address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    subsystem_id = Column(Integer, ForeignKey(
        "subsystems.id", ondelete="CASCADE"))

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, name, agreement, legal_address, phone, subsystem_id, *args, **kwargs):
        self.name = name
        self.agreement = agreement
        self.legal_address = legal_address
        self.phone = phone
        self.subsystem_id = subsystem_id
        if not kwargs.get("mail_address", None):
            self.mail_address = self.legal_address
        else:
            self.mail_address = kwargs.get("mail_address")

    def __repr__(self) -> str:
        return f"{self.__class__}({self.name}, {self.legal_address}, {self.phone}, {self.subsystem_id})"
