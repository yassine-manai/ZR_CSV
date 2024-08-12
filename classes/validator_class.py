

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator


class Company_validation(BaseModel):

    # Mandatory fields
    id: int
    name: str
    xValidUntil: str

    
    # Optional fields
    xValidFrom: Optional[str] = ''
    filialId: Optional[str] = ''
    surname: Optional[str] = ''
    phone1: Optional[str] = ''
    email1: Optional[str] = ''
    street: Optional[str] = ''   
    phone1: Optional[str] = ''
    town: Optional[str] = ''
    postbox: Optional[str] = ''   


    @field_validator('id', 'filialId', mode='before')
    def validate_positive_data(cls, value):
        if value <= 1:
            raise ValueError("Value must be greater than 1")
        return value     

    
    @field_validator('xValidUntil', 'xValidFrom', mode='before')
    def validate_date_format(cls, value, info):
        non_empty_fields = ['Company_ValidUntil', 'Participant_ValidUntil']

        if info.field_name in non_empty_fields and value == '':
            raise ValueError(f"{info.field_name} cannot be empty")

        if value == '':
            return value

        date_formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d"]

        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(value, fmt)
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue

        raise ValueError(f"Date format for '{value}' is not supported")

    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['id', 'name', 'xValidUntil']

        for field in mandatory_fields:
            if not values.get(field):
                raise ValueError(f"The field {field} is mandatory and cannot be empty.")

        return values
    



class Consumer_validation(BaseModel):

    # Mandatory fields
    id: int
    firstName: str
    surname: str
    cardno: str
    lpn1: str
    contractid: int
    
    # Optional fields
    xValidFrom: Optional[str] = ''
    xValidUntil: Optional[str] = ''
    filialId: Optional[int] = ''
    ptcptType: Optional[int] = ''
    cardclass: Optional[str] = ''
    identificationType: Optional[str] = ''
    validFrom: Optional[str] = ''
    validUntil: Optional[str] = ''
    admission: Optional[str] = ''
    ignorePresence: Optional[str] = ''
    present: Optional[str] = ''
    status: Optional[int] = ''
    ptcptGrpNo: Optional[int] = ''    
    displayText: Optional[str] = ''
    memo: Optional[str] = ''   
    delete: Optional[str] = ''
    lpn2: Optional[str] = ''   
    lpn3: Optional[str] = ''


    @field_validator('id', 'filialId', 'ptcptType', 'status', 'ptcptGrpNo', mode='before')
    def validate_positive_int(cls, value):
        if value is not None and value <= 1:
            raise ValueError("Value must be greater than 1")
        return value

    @field_validator('xValidUntil', 'xValidFrom', 'validFrom', 'validUntil', mode='before')
    def validate_date_format(cls, value, info):
        if value == '':
            return value

        date_formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d"]

        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(value, fmt)
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue

        raise ValueError(f"Date format for '{value}' is not supported")

    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['id', 'firstName', 'surname', 'cardno', 'lpn1', 'contractid']

        for field in mandatory_fields:
            if not values.get(field):
                raise ValueError(f"The field {field} is mandatory and cannot be empty.")

        return values
    
