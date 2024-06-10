from xml.etree import ElementTree

import requests


class Search:
    API_ENDPOINT = 'https://search.ch/tel/api/'

    def __init__(self, request_text: str, telsearch_key: str):

        self.request_text = request_text
        self.telsearch_key = telsearch_key

        if not self.request_text[0] in ('+', '0'):
            self.request_text = f'+{self.request_text}'

    def get_entry(self):
        resp = requests.get(
            url=self.API_ENDPOINT,
            params={
                'was': self.request_text,
                'key': self.telsearch_key
            }
        )

        if resp.status_code != 200:
            return

        xml_root = ElementTree.fromstring(resp.text)

        # for each node
        for child in xml_root:

            # we return the first entry
            if child.tag.endswith('entry'):

                lookup_entry_dict = {}
                fields_to_save = (
                    'Organisation',
                    'name',
                    'firstname',
                    'street',
                    'streetno',
                    'zip',
                    'city',
                    'canton',
                    'country',
                    'phone',
                    'occupation'
                )
                extras_to_save = ('email', 'website')
                ignored_websites = ('facebook', 'linkedin', 'instagram', 'twitter')

                # get data of entry
                for field in child:
                    if field.text != '':
                        field_name = field.tag.split('}')[-1]

                        if field_name in fields_to_save:
                            lookup_entry_dict[field_name] = field.text

                        elif field.attrib.get('type') in extras_to_save:
                            if field.attrib['type'] in extras_to_save:
                                if not any([company_name in field.text for company_name in ignored_websites]):
                                    lookup_entry_dict[field.attrib['type']] = field.text.replace('*', '')

                if 'firstname' in lookup_entry_dict.keys():
                    lookup_entry_dict['display_name'] = f'{lookup_entry_dict["firstname"]} {lookup_entry_dict["name"]}'
                else:
                    lookup_entry_dict['display_name'] = lookup_entry_dict["name"]

                return lookup_entry_dict
