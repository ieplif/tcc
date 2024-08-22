from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class Patient:
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    full_name: Mapped[str]
    age: Mapped[int]
    place_of_birth: Mapped[str]
    marital_status: Mapped[str]
    gender: Mapped[str]
    profession: Mapped[str]
    residential_address: Mapped[str]
    commercial_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


@table_registry.mapped_as_dataclass
class ClinicalHistory:
    __tablename__ = 'clinical_histories'

    history_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    main_complaint: Mapped[str]
    disease_history: Mapped[str]
    lifestyle_habits: Mapped[str]
    previous_treatments: Mapped[str]
    personal_family_history: Mapped[str]
    other_information: Mapped[str] = None
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


@table_registry.mapped_as_dataclass
class ClinicalExamination:
    __tablename__ = 'clinical_examinations'

    exam_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    exam_details: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
