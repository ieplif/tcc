from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class PatientSchema(BaseModel):
    full_name: str
    age: int
    place_of_birth: str
    marital_status: str
    gender: str
    profession: str
    residential_address: str
    commercial_address: str


class PatientPublic(PatientSchema):
    id: int


class PatientList(BaseModel):
    patients: List[PatientPublic]


class PatientFilter(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    place_of_birth: Optional[str] = None
    marital_status: Optional[str] = None
    gender: Optional[str] = None
    profession: Optional[str] = None
    residential_address: Optional[str] = None
    commercial_address: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    place_of_birth: Optional[str] = None
    marital_status: Optional[str] = None
    gender: Optional[str] = None
    profession: Optional[str] = None
    residential_address: Optional[str] = None
    commercial_address: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class ClinicalHistorySchema(BaseModel):
    patient_id: int
    main_complaint: str
    disease_history: str
    lifestyle_habits: str
    previous_treatments: str
    personal_family_history: str
    other_information: Optional[str] = None


class ClinicalHistoryPublic(ClinicalHistorySchema):
    history_id: int


class ClinicalHistoryList(BaseModel):
    clinical_histories: List[ClinicalHistoryPublic]


class ClinicalHistoryFilter(BaseModel):
    patient_id: Optional[int] = None
    main_complaint: Optional[str] = None
    disease_history: Optional[str] = None
    lifestyle_habits: Optional[str] = None
    previous_treatments: Optional[str] = None
    personal_family_history: Optional[str] = None
    other_information: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class ClinicalHistoryUpdate(BaseModel):
    patient_id: Optional[int] = None
    main_complaint: Optional[str] = None
    disease_history: Optional[str] = None
    lifestyle_habits: Optional[str] = None
    previous_treatments: Optional[str] = None
    personal_family_history: Optional[str] = None
    other_information: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
