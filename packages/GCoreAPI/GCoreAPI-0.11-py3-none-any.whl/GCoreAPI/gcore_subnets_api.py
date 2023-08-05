from typing import Union, List, Dict

from GCoreAPI.GCore_Base import Base


class Subnets(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/subnets"

    def list_subnets(self, region_id: int,
                     network_id: str = None,
                     metadata_kv: str = None,
                     metadata_v: str = None,
                     ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        if network_id is not None:
            self.add_query_param('network_id', network_id)

        if metadata_kv is not None:
            self.add_query_param('metadata_kv', metadata_kv)
        if metadata_v is not None:
            self.add_query_param('metadata_v', metadata_v)

        return self.request(url, request_type='GET', params=True)

    def create_subnet(self, region_id: int,
                      cidr: str,
                      name: str,
                      network_id: str,
                      host_routes: List[dict] = None,
                      connect_to_network_router: bool = True,
                      enable_dhcp: bool = True,
                      gateway_ip: Union[str, None] = None,
                      dns_nameservers: List[str] = None,
                      metadata: Dict = None,
                      ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('cidr', cidr)
        self.add_to_json('name', name)
        self.add_to_json('network_id', network_id)

        if host_routes is not None:
            self.add_to_json('host_routes', host_routes)
        if connect_to_network_router is not None:
            self.add_to_json('connect_to_network_router', connect_to_network_router)
        if enable_dhcp is not None:
            self.add_to_json('enable_dhcp', enable_dhcp)
        if gateway_ip is not None:
            self.add_to_json('gateway_ip', gateway_ip)
        if dns_nameservers is not None:
            self.add_to_json('dns_nameservers', dns_nameservers)
        if metadata is not None:
            self.add_to_json('metadata', metadata)

        return self.request(url, request_type='POST', body=True)

    def delete_subnet(self, region_id: int,
                      subnet_id: str
                      ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{subnet_id}"
        self.reset()

        return self.request(url, request_type='DELETE')

    def get_subnet(self, region_id: int,
                   subnet_id: str
                   ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{subnet_id}"
        self.reset()

        return self.request(url, request_type='GET')

    def change_subnet_properties(self, region_id: int,
                                 subnet_id: str,
                                 host_routes: List[dict] = None,
                                 name: str = None,
                                 gateway_ip: Union[str, None] = None,
                                 enable_dhcp: bool = None,
                                 dns_nameservers: List[str] = None,
                                 ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{subnet_id}"
        self.reset()
        self.add_application_header()
        if host_routes is not None:
            self.add_to_json('host_routes', host_routes)
        if name is not None:
            self.add_to_json('name', name)
        if gateway_ip is not None:
            self.add_to_json('gateway_ip', gateway_ip)
        if enable_dhcp is not None:
            self.add_to_json('enable_dhcp', enable_dhcp)
        if dns_nameservers is not None:
            self.add_to_json('dns_nameservers', dns_nameservers)

        return self.request(url, request_type='PATCH', body=True)

    def list_subnet_metadata(self, region_id: int,
                             subnet_id: str,
                             ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{subnet_id}/metadata"
        self.reset()

        return self.request(url, request_type='GET')

    def create_update_subnet_metadata(self, region_id: int,
                                      subnet_id: str,
                                      key: str = None
                                      ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{subnet_id}/metadata"
        self.reset()

        if key is not None:
            self.add_application_header()
            self.add_to_json('key', key)
            return self.request(url, request_type='POST', body=True)

        return self.request(url, request_type='POST')

    def replace_subnet_metadata(self, region_id: int,
                                subnet_id: str,
                                key: str = None
                                ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{subnet_id}/metadata"
        self.reset()

        if key is not None:
            self.add_application_header()
            self.add_to_json('key', key)
            return self.request(url, request_type='PUT', body=True)

        return self.request(url, request_type='PUT')

    def delete_subnet_metadata_by_key(self, region_id: int,
                                      subnet_id: str,
                                      key: str = None
                                      ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{subnet_id}/metadata_item"
        self.reset()

        if key is not None:
            self.add_query_param('key', key)
            return self.request(url, request_type='DEL', params=True)

        return self.request(url, request_type='DEL')

    def get_subnet_metadata_by_key(self, region_id: int,
                                   subnet_id: str,
                                   key: str = None
                                   ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{subnet_id}/metadata_item"
        self.reset()

        if key is not None:
            self.add_query_param('key', key)
            return self.request(url, request_type='GET', params=True)

        return self.request(url, request_type='GET')
