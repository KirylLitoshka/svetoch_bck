from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base
from slugify import slugify
from datetime import date

Base = declarative_base()


class Subsystem(Base):
    __tablename__ = "subsystems"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    alt_name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    current_date = Column(Date, default=date.today())

    def __init__(self, name, alt_name, *args, **kwargs):
        self.name = name
        self.alt_name = alt_name
        if not kwargs.get("slug", None):
            self.slug = slugify(self.name, allow_unicode=True)
        else:
            self.slug = slugify(kwargs.get("slug"), allow_unicode=True)
        super(Subsystem, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"Subsystem({self.name}, {self.alt_name})"
