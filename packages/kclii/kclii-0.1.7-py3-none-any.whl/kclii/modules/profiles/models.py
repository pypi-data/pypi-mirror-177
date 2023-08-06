from sqlalchemy import Column, String, Integer, Sequence, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from kclii.database.database import Base


class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(Integer, Sequence("profile_id_seq"), primary_key=True)
    name = Column(String, nullable=False)
    environment_variables = relationship(
        "EnvironmentVariablesModel",
        back_populates="profile",
        cascade="all, delete, delete-orphan",
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EnvironmentVariablesModel(Base):
    __tablename__ = "environment_variables"

    id = Column(Integer, Sequence("profile_id_seq"), primary_key=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("ProfileModel", back_populates="environment_variables")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
