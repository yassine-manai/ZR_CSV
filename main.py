import tkinter as tk
from api.api_media import create_company, create_participant, get_company_details
from app.gui.main_window import CSVLoaderApp
from app.logic.check_current_data import check_participant
from classes.data_class import CompanyContract
from functions.dict_xml import consumer_to_xml, contract_to_xml
    
def main():
    app = CSVLoaderApp()
    app.mainloop()
    
    

def data_consumer(c_id: str) -> dict:
    return {
        "consumer": {
            "contractid": c_id,
            "name": "",
            "xValidFrom": "2019-01-01+01:00",
            "xValidUntil": "2025-12-31",
            "filialId": "1001"
        },
        "person": {
            "firstName": "yassnne",
            "surname": "Rossi"
        },
        "identification": {
            "ptcptType": "6",
            "cardno": "4475",
            "cardclass": "0",
            "identificationType": "51",
            "validFrom": "2021-01-01+01:00",
            "validUntil": "2025-01-01+01:00",
            "usageProfile": {
                "id": "1",
                "name": "Global Access",
                "description": ""
            },
            "admission": "",
            "ignorePresence": "0",
            "present": "false",
            "status": "0",
            "ptcptGrpNo": "-1",
            "chrgOvdrftAcct": "0"
        },
        "displayText": "-1",
        "limit": "9999900",
        "memo": "Note1",
        "status": "0",
        "delete": "0",
        "ignorePresence": "0",
        "lpn1": "LPN1A",
        "lpn2": "LPN2",
        "lpn3": "LPN3"
    }


data_contract = {
    "contract": {
        "name": "MG",
        "xValidFrom": "2021-01-01",
        "xValidUntil": "2021-12-31"
    },
    "person": {
        "surname": "Groupe Me",
        "phone1": "76111111",
        "email1": "Monoprix@mail.tn"
    },
    "stdAddr": {
        "street": "Lac 1",
        "town": "Tunis",
        "postbox": "666"
    }
}

contract = contract_to_xml(data_contract)
#print(contract)

contract_id = "2"

consumer_data = data_consumer(contract_id)

consumer = consumer_to_xml(consumer_data)


#print(consumer)


if __name__ == "__main__":
    #GET METHOD
    #get_company_details(49)
    #check_participant(2,231)
    
    #POST METHOD
    #create_company(contract)
    #create_participant(2,3,consumer)
    main()





