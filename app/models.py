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
    services = relationship("Service", back_populates="subsystem", cascade="all, delete-orphan")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # def __init__(self, name, alt_name, *args, **kwargs):
    #     self.name = name
    #     self.alt_name = alt_name
    #     super(Subsystem, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"Subsystem({self.name}, {self.alt_name})"


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, primary_key=True)
    alt_name = Column(String, nullable=False)
    component = Column(String, unique=True, nullable=False)
    subsystem_name = Column(String, ForeignKey("subsystems.name"), nullable=False)
    subsystem = relationship("Subsystem", back_populates="services")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, name, alt_name, subsystem_name, *args, **kwargs):
        self.name = name
        self.alt_name = alt_name
        self.subsystem_name = subsystem_name
        if not kwargs.get("component", None):
            self.component = self.subsystem_name.title() + self.name.title()
        else:
            self.component = kwargs.get("component")
        super(Service, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.__class__}({self.name}, {self.alt_name}, {self.component})"
