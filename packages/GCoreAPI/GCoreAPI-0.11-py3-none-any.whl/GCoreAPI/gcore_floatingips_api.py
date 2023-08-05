from typing import Union, List, Dict

from GCoreAPI.GCore_Base import Base


class FloatingIPs(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/floatingips"

    def list_ip(self, region_id: int) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        return self.request(url, request_type='GET', body=True)

    def create_ip(self, region_id: int,
                  metadata: dict = None,
                  port_id: str = None,
                  fixed_ip_address: str = None) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        self.add_application_header()

        if metadata is not None:
            self.add_to_json('metadata', metadata)
        if port_id is not None:
            self.add_to_json('port_id', port_id)
        if fixed_ip_address is not None:
            self.add_to_json('fixed_ip_address', fixed_ip_address)

        return self.request(url, request_type='POST', body=True)

    def delete_ip(self, region_id: int, pk: str) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{pk}"
        self.reset()

        return self.request(url, request_type='DELETE', params=True)

    def get_ip(self, region_id: int, pk: str) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{pk}"
        self.reset()

        return self.request(url, request_type='GET', params=True)

    def assign_ip_to_lb(self, region_id: int,
                        pk: str,
                        port_id: str,
                        metadata: dict = None,
                        fixed_ip_address: str = None) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{pk}/assign"
        self.reset()
        self.add_application_header()

        self.add_to_json('fixed_ip_address', fixed_ip_address)

        if metadata is not None:
            self.add_to_json('metadata', metadata)
        if fixed_ip_address is not None:
            self.add_to_json('fixed_ip_address', fixed_ip_address)

        return self.request(url, request_type='POST', body=True)

    def unassign_ip(self, region_id: int, pk: str) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{pk}/unassign"
        self.reset()

        return self.request(url, request_type='POST', params=True)

    def get_available_ip(self, region_id: int) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()

        return self.request(url, request_type='GET', body=True)

    def list_network_metadata(self, region_id: int, pk: str) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata"
        self.reset()

        return self.request(url, request_type='GET', body=True)

    def update_ip_metadata(self, region_id: int, pk: str, key: dict) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata"
        self.reset()
        self.add_application_header()

        for elem in key.keys():
            if len(elem) > 255 or len(key[elem]) > 1024:
                print(f"Too long key name '{elem}'!")
                return {"Result": "False", "Reason": f"Too long key name '{elem}'!"}

        self.body = key

        return self.request(url, request_type='POST', body=True)

    def replace_ip_metadata(self, region_id: int, pk: str, key: dict) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata"
        self.reset()
        self.add_application_header()

        for elem in key.keys():
            if len(elem) > 255 or len(key[elem]) > 1024:
                print(f"Too long key name '{elem}'!")
                return {"Result": "False", "Reason": f"Too long key name '{elem}'!"}

        self.body = key

        return self.request(url, request_type='PUT', body=True)

    def delete_ip_metadata(self, region_id: int, pk: str, key: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata_item?key={key}'
        self.reset()

        return self.request(url, request_type='DELETE', body=True)

    def get_ip_metadata(self, region_id: int, pk: str, key: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{pk}/metadata_item?key={key}'
        self.reset()

        return self.request(url, request_type='GET', body=True)







