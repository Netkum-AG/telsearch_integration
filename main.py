#!/usr/bin/env python3

import sys

from search import Search
from wms_interface import WMSInterface

if __name__ == '__main__':

    telsearch_phonebook = None

    if len(sys.argv[1:]) < 4:
        print(f'TealSearch lookup param error {sys.argv[1:]}')
    else:
        request_text, telsearch_key, wms_hostname, wms_app_token = sys.argv[1:5]

        if len(sys.argv) == 6:
            telsearch_phonebook = sys.argv[-1]

        # init WMS Interface
        wms_interface = WMSInterface(
            wms_hostname=wms_hostname,
            wms_app_token=wms_app_token,
            telsearch_phonebook=telsearch_phonebook
        )

        # check login
        if not wms_interface.check_login():
            print('WMS login error')

        else:

            # lookup
            search = Search(
                request_text=request_text,
                telsearch_key=telsearch_key
            )

            search_result_dict = search.get_entry()

            # if no result return request
            if not search_result_dict:
                print(search.request_text)
            else:
                print(search_result_dict["display_name"])

                # contact creation
                if telsearch_phonebook and search_result_dict:
                    wms_interface.create_contact(search_result_dict)
