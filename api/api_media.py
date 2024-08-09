from typing import Tuple
from functions.check_error import handle_api_error
from functions.request_api import make_request
from config.log_config import logger

url_api = "https://193.95.82.173:8709/CustomerMediaWebService"

# Company Section

@handle_api_error
def get_company_details(company_id: int) -> Tuple[int, dict]:
    return make_request("GET", f"{url_api}/contracts/{company_id}/detail")

@handle_api_error
def create_company(data: str) -> Tuple[int, dict]:
    logger.debug(f"Creating company with data: {data}")
    return make_request("POST", f"{url_api}/contracts", data=data)

# Participant Part
@handle_api_error
def create_participant(company_id: int, template_id: int, data: str) -> Tuple[int, dict]:
    logger.debug(f"Creating participant for company ID {company_id} with template ID {template_id}")
    return make_request("POST", f"{url_api}/contracts/{company_id}/consumers?templateId={template_id}", data=data)

@handle_api_error
def get_participant(company_id: int, participant_id: int) -> Tuple[int, dict]:
    return make_request("GET", f"{url_api}/consumers/{company_id},{participant_id}")