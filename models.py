from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Fluid(Base):
    __tablename__ = "fluids"

    id = Column(Integer, primary_key=True, index=True)
    fluid_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    status = Column(String, default="Active")
    revision = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    fluid_id = Column(String, ForeignKey("fluids.fluid_id"))
    status = Column(String, default="Active")
    revision = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
