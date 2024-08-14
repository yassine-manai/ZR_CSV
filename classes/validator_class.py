

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
from globals.global_vars import glob_vals
from config.log_config import logger
from dateutil.parser import parse, ParserError

date_formats = ["%d-%m-%Y", "%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y"]


class Company_validation(BaseModel):
    
    # Mandatory fields
    id: int
    name: str
    xValidUntil: str

    
    # Optional fields
    xValidFrom: Optional[str] = ''
    filialId: Optional[int] = ''
    surname: Optional[str] = ''
    phone1: Optional[str] = ''
    email1: Optional[str] = ''
    street: Optional[str] = ''   
    phone1: Optional[str] = ''
    town: Optional[str] = ''
    postbox: Optional[str] = ''   


    @field_validator('id', 'filialId', mode='before')
    def validate_positive_data(cls, value):
        try:
            value = int(value)  
        except (ValueError, TypeError):
            raise ValueError(f"Compagny Id must be an integer between 1 and 99999, provided {value}")
        
        if value <= 1 or value > 99999:
            raise ValueError(f"Compagny Id must be between 1 and 99999, provided {value}")
        return value

    
    @field_validator('xValidUntil', 'xValidFrom', mode='before')
    def validate_date_format(cls, value, info):
        global glob_vals
        
        non_empty_fields = ['Company_ValidUntil', 'Participant_ValidUntil']

        if info.field_name in non_empty_fields and value == '':
            raise ValueError(f"{info.field_name} cannot be empty")

        if value == '':
            return value

        try:
            date_obj = parse(value, fuzzy=False)

            formatted_date = date_obj.strftime(glob_vals['date_format_val'])
            return formatted_date
        
        except (ParserError, ValueError) as e:
            raise ValueError(f"Date format for '{value}' is not supported or invalid: {str(e)}")


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
    filialId: Optional[int] = 7001
    ptcptType: Optional[int] = 2
    cardclass: Optional[str] = ''
    identificationType: Optional[str] = ''
    validFrom: Optional[str] = ''
    validUntil: Optional[str] = ''
    admission: Optional[str] = ''
    ignorePresence: Optional[str] = ''
    present: Optional[str] = ''
    status: Optional[int] = 0
    ptcptGrpNo: Optional[int] = None    
    displayText: Optional[str] = ''
    memo: Optional[str] = ''   
    delete: Optional[str] = ''
    lpn2: Optional[str] = ''   
    lpn3: Optional[str] = ''


    @field_validator('id', 'filialId', mode='before')
    def validate_positive_data(cls, value):
        try:
            value = int(value)  
        except (ValueError, TypeError):
            raise ValueError(f"Compagny Id must be an integer between 1 and 99999, provided {value}")
        
        if value <= 1 or value > 99999:
            raise ValueError(f"Compagny Id must be between 1 and 99999, provided {value}")
        return value


    @field_validator('xValidUntil', 'xValidFrom', 'validFrom', 'validUntil', mode='before')
    def validate_date_format(cls, value, info):
        if value == '':
            
            return KeyError

        try:
            date_obj = parse(value, fuzzy=False)

            formatted_date = date_obj.strftime(glob_vals['date_format_val'])
            return formatted_date
        
        except (ParserError, ValueError) as e:
            raise ValueError(f"Date format for '{value}' is not supported or invalid: {str(e)}")



    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['id', 'firstName', 'surname', 'cardno', 'lpn1', 'contractid']

        for field in mandatory_fields:
            if not values.get(field):
                raise ValueError(f"The field {field} is mandatory and cannot be empty.")

        return values
    
    
    
    @field_validator('ptcptType', mode='before')
    def validate_ptcpt_type(cls, value: int):
        if value not in [2, 6]:                
                raise ValueError(f"Participant Type must be either 2 or 6, provided is {value}")
        return value
    
    