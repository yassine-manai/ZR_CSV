from app.gui.main_window import CSVLoaderApp
from classes.validator_class import Company_validation, Consumer_validation
from functions.dict_xml import consumer_to_xml, contract_to_xml

def main():
    app = CSVLoaderApp()
    app.mainloop()
    
    
    
    

def data_consumer(c_id: int) -> dict:
    return {
        "id": 25,
        "contractid": c_id,
        "xValidFrom": '1900-01-01',
        "xValidUntil": '2025-01-01',
        "filialId": 7077,
        
        "firstName":'Participant_Firstname',
        "surname": 'Participant_Surname',
        "ptcptType": 6,
        "cardno": "E542",
        "cardclass": 'Participant_Cardclass',
        "identificationType": 'Participant_IdentificationType',
        "validFrom": '2020-01-01',
        "validUntil": '2025-01-01',
        "admission": "",
        "ignorePresence": '0',
        "present": 'false',
        "status": '0',
        "ptcptGrpNo": 6,
        
        "displayText": '-1',
        "limit": '9999900',
        "memo": "Note1",
        "status": 10,
        "delete": '0',
        "ignorePresence":'0',
        "lpn1": 'NOLPN',
        "lpn2": 'NOLPN',
        "lpn3": 'NOLPN',
    }


data_contract = {
        "id": 45,
        "name": "MG",
        "xValidFrom": "12/10/2054",
        "xValidUntil": "2021-12-31",
        "surname": "Groupe Me",
        "phone1": "76111111",
        "email1": "Monoprix@mail.tn",
        "street": "Lac 1",
        "town": "Tunis",
        "postbox": "666",
}

""" xml_output = contract_to_xml(data_contract)
validated_contract = Company_validation(data_contract)

print(validated_contract)
 """



contract_id = 2
""" consumer_data = data_consumer(contract_id)
consumer = consumer_to_xml(consumer_data)
 """

#print(consumer)


if __name__ == "__main__":
    #GET METHOD
    #get_company_details(49)
    #check_participant(2,231)
    
    #POST METHOD
    #create_company(contract)
    #create_participant(2,3,consumer)
    #main()
    
    print("--------------------------------")


    data_contract = {
        "id": 45,
        "name": "MG",
        "xValidFrom": "12/10/2054",
        "xValidUntil": "2021-12-31",
        "surname": "Groupe Me",
        "phone1": "76111111",
        "email1": "Monoprix@mail.tn",
        "street": "Lac 1",
        "town": "Tunis",
        "postbox": "666",
}
    
    validated_contract = Company_validation(**data_contract)    
    xml_output = contract_to_xml(validated_contract.dict())
        
    #print(f"Validated Contract {validated_contract} \n")
    #print(f"XML Contract {xml_output}")


    consumer_data = data_consumer(contract_id)
    validated_consumer = Consumer_validation(**consumer_data)    
    consumer = contract_to_xml(validated_consumer.dict())
        
    print(f"Validated Contract {validated_consumer} \n")
    print(f"XML Consumer {consumer}")


