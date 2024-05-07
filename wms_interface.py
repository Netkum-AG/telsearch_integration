import requests


class WMSInterface:

    def __init__(self, wms_hostname, wms_app_token, telsearch_phonebook):
        self.wms_hostname = wms_hostname
        self.wms_app_token = wms_app_token
        self.telsearch_phonebook = telsearch_phonebook

    def check_login(self):
        return requests.get(
            url=f'{self.wms_hostname}/api/v1/PBX/version/',
            headers={
                'Authorization': f'Bearer {self.wms_app_token}'
            }
        ).status_code == 200


    def get_create_phonebook_id(self):
        resp = requests.get(
            url=f'{self.wms_hostname}/api/v1/Phonebooks/',
            headers={
                'Authorization': f'Bearer {self.wms_app_token}'
            }
        )

        phonebook_id = None
        for wms_phonebook in resp.json()['result']['records']:
            if wms_phonebook['name'] == self.telsearch_phonebook:
                phonebook_id = wms_phonebook['id']

        if not phonebook_id:
            resp = requests.post(
                url=f'{self.wms_hostname}/api/v1/Phonebooks/',
                headers={
                    'Authorization': f'Bearer {self.wms_app_token}'
                },
                data={
                    'data[name]': self.telsearch_phonebook,
                    'data[type]': 2  # Global
                }
            )
            phonebook_id = resp.json()['result']['id']
        return phonebook_id

    def create_contact(self, contact_dict: dict):

        phonebook_id = self.get_create_phonebook_id(),
        if phonebook_id:
            requests.post(
                url=f'{self.wms_hostname}/api/v1/Contacts/',
                headers={
                    'Authorization': f'Bearer {self.wms_app_token}'
                },
                data={
                    'data[name]': contact_dict['display_name'],
                    'data[phonebook_id]': self.get_create_phonebook_id(),
                    'data[phone]': contact_dict.get('phone', ''),
                    'data[email]': contact_dict.get('email', ''),
                    'data[note]': contact_dict.get('website', ''),
                    'data[address]': f"{contact_dict.get('street', '')} {contact_dict.get('streetno', '')}",
                    'data[postal_code]': f"{contact_dict.get('zip', '')}",
                    'data[city]': f"{contact_dict.get('city', '')}",
                    'data[province]': f"{contact_dict.get('canton', '')}",
                    'data[country]': f"{contact_dict.get('country', '')}",
                    'data[organization]': f"{contact_dict.get('occupation', '')}",
                }
            )
