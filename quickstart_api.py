import requests
import json


# De URL van de API-endpoint voor orders
orders_url = 'https://app.lightr.nl/api/v1/orders'

# De headers met het Authorization token en Content-Type
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer jouwtoken',  # Vervang dit door je eigen token
    'Content-Type': 'application/json'
}

# Functie om de beschikbare fonts op te halen
def get_fonts():
    url = 'https://app.lightr.nl/api/v1/fonts'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Functie om de velden van een specifieke preset op te halen
def get_preset_details(preset_id):
    url = f'https://app.lightr.nl/api/v1/presets/{preset_id}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")



# Functie om een order te plaatsen
def post_order(font_id):
    data = {
        "preset_id": "9a8e675d-fcf1-403f-a17e-153b1591080c",
        "font_id": font_id,
        "quantity": 1,
        "type": "send_multiple"
    }

    response = requests.post(orders_url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Functie om een ontvanger toe te voegen aan de order
def add_receiver_to_order(order_id):
    receivers_url = f'https://app.lightr.nl/api/v1/orders/{order_id}/receivers'
    receiver_data = {
        ## adres gegeven voor in het systeem deze zijn altijd het zelfde
        'name': "Jan Jansen",
        'country_id': '99d4d37a-0956-428c-9eb6-67e9b205cc09',
        'address': " Voorbeelstraat 123",
        'postal_code': "1234AB",
        'city': "Barneveld",
        ## deze zijn verschillende per kaart. Upload je een nieuwe (basis) template dan kan je deze variabelen zelf bepalen
        ### Multiline is wel altijd het zelfde, dit is de tekst voor op het kaartje.
        'text_variables': {
            # adres gegeven die op het kaartje worden geschreven
            'Bedrijf': 'Testcompany',
            'Naam': 'Jan Jansen',
            'Straat': 'Voorbeeldstraat 123',
            'Postcode': '1234 AB Barneveld',
            'Land': 'Nederland',
            ### tekst op het kaartje
            'Multiline': 'Beste Dion, \n\ndit is een test order via de API\n\nNog een regel\n\nmet vriendelijke groet,\n Maas'
            }

    }

    response = requests.post(receivers_url, headers=headers, data=json.dumps(receiver_data))

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


def finalize_order(order_id):
    finalize_url = f'https://app.lightr.nl/api/v1/orders/{order_id}/finalize'
    
    response = requests.post(finalize_url, headers=headers)

    if response.status_code == 204:
        return "order is besteld"
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")





try:
    fonts_response = get_fonts()
    ## ik gebruik hier nu het eerste id, elk font heeft zijn eigen id.
    font_id = fonts_response['data'][0]['id']
    print("--font_id", font_id)
    
    # Haal preset details op (kan eenmalig worden uitgevoerd per type kaart,)
    preset_details = get_preset_details("9a8e675d-fcf1-403f-a17e-153b1591080c")
    print("--Preset Details:", preset_details)

    # Plaats de order met de opgehaalde font_id
    order_response = post_order(font_id)
    print("---Order Response:", order_response)

    # Haal de order ID op uit de response
    order_id = order_response['data']['id']

    # Voeg een ontvanger toe aan de geplaatste order
    ## deze voer je net zo vaak uit als het aantal recievers / ontvangers.
    ### na het uitvoeren van deze call zie je hier je order staan inclusief preview en het aantal kaarten 
    #### https://app.lightr.nl/dashboard/orders 
    receiver_response = add_receiver_to_order(order_id)
    print("---Receiver Response:", receiver_response)

    # activeer de onderstaande regel om je order te verzenden / bestellen.
    #finalization_response = finalize_order(order_id)
    #print("---Finalization Response:", finalization_response)

except Exception as e:
    print("Er is een fout opgetreden:", e)
