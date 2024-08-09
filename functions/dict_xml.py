def contract_to_xml(data):
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<cm:contractDetail xmlns:cm="http://gsph.sub.com/cust/types">\n'
    
    # Contract section
    if 'contract' in data:
        xml_content += '<cm:contract>\n'
        for key in ['id', 'name', 'xValidFrom', 'xValidUntil']:
            if key in data['contract']:
                xml_content += f'<cm:{key}>{data["contract"][key]}</cm:{key}>\n'
        xml_content += '</cm:contract>\n'
    
    # Person section
    if 'person' in data:
        xml_content += '<cm:person>\n'
        for key in ['surname', 'phone1', 'email1']:
            if key in data['person']:
                xml_content += f'<cm:{key}>{data["person"][key]}</cm:{key}>\n'
        xml_content += '</cm:person>\n'
    
    # StdAddr section
    if 'stdAddr' in data:
        xml_content += '<cm:stdAddr>\n'
        for key in ['street', 'town', 'postbox']:
            if key in data['stdAddr']:
                xml_content += f'<cm:{key}>{data["stdAddr"][key]}</cm:{key}>\n'
        xml_content += '</cm:stdAddr>\n'
    
    xml_content += '</cm:contractDetail>'
    return xml_content



def consumer_to_xml(data):
    xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'
    xml_content += '<cm:consumerDetail xmlns:cm="http://gsph.sub.com/cust/types">\n'
    
    # Consumer section
    if 'consumer' in data:
        xml_content += '<cm:consumer>\n'
        for key in ['contractid', 'name', 'xValidFrom', 'xValidUntil', 'filialId']:
            if key in data['consumer']:
                xml_content += f'<cm:{key}>{data["consumer"][key]}</cm:{key}>\n'
        xml_content += '</cm:consumer>\n'
    
    # Person section
    if 'person' in data:
        xml_content += '<cm:person>\n'
        for key in ['firstName', 'surname']:
            if key in data['person']:
                xml_content += f'<cm:{key}>{data["person"][key]}</cm:{key}>\n'
        xml_content += '</cm:person>\n'
    
    # Identification section
    if 'identification' in data:
        xml_content += '<cm:identification>\n'
        for key in ['ptcptType', 'cardno', 'cardclass', 'identificationType', 'validFrom', 'validUntil']:
            if key in data['identification']:
                xml_content += f'<cm:{key}>{data["identification"][key]}</cm:{key}>\n'
        
        if 'usageProfile' in data['identification']:
            xml_content += '<cm:usageProfile href="/usageProfile/1">\n'
            for key in ['id', 'name', 'description']:
                if key in data['identification']['usageProfile']:
                    xml_content += f'<cm:{key}>{data["identification"]["usageProfile"][key]}</cm:{key}>\n'
            xml_content += '</cm:usageProfile>\n'
        
        for key in ['admission', 'ignorePresence', 'present', 'status', 'ptcptGrpNo', 'chrgOvdrftAcct']:
            if key in data['identification']:
                xml_content += f'<cm:{key}>{data["identification"][key]}</cm:{key}>\n'
        
        xml_content += '</cm:identification>\n'
    
    # Additional fields
    for key in ['displayText', 'limit', 'memo', 'status', 'delete', 'ignorePresence', 'lpn1', 'lpn2', 'lpn3']:
        if key in data:
            xml_content += f'<cm:{key}>{data[key]}</cm:{key}>\n'
    
    xml_content += '</cm:consumerDetail>'
    return xml_content

""" # Example usage:
data_consumer = {
    "consumer": {
        "contractid": "2",
        "name": "",
        "xValidFrom": "2021-01-01+01:00",
        "xValidUntil": "2025-01-01+01:00",
        "filialId": "1001"
    },
    "person": {
        "firstName": "yassnne",
        "surname": "Rossi"
    },
    "identification": {
        "ptcptType": "2",
        "cardno": "11455",
        "cardclass": "0",
        "identificationType": "51",
        "validFrom": "2020-01-01+01:00",
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


# Example usage:
data_contract = {
    "contract": {
        "id": "11",
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

xml_output = contract_to_xml(data_contract)
print(xml_output)

print("\n")

xml_output = consumer_to_xml(data_consumer)
print(xml_output) 

"""