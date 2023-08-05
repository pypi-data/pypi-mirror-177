from GCoreAPI.GCore_Base import Base


class Networks(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/networks"
        self.available_networks_api_url = f"{self.BASE_URL}/availablenetworks"

    def list_networks(self, region_id: int,
                      order_by: str = None,
                      metadata_kv: str = None,
                      metadata_v: str = None,
                      ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        if order_by is not None:
            self.add_query_param('order_by', order_by)

        if metadata_kv is not None:
            self.add_query_param('metadata_kv', metadata_kv)
        if metadata_v is not None:
            self.add_query_param('metadata_v', metadata_v)

        return self.request(url, request_type='GET', params=True)

    def create_network(self, region_id: int,
                       name: str,
                       metadata: dict = None,
                       create_router: bool = True,
                       network_type: str = 'vxlan'
                       ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)
        self.add_to_json('create_router', create_router)
        self.add_to_json('type', network_type)

        if metadata is not None:
            self.add_to_json('metadata', metadata)

        return self.request(url, request_type='POST', body=True)

    def delete_network(self, region_id: int,
                       network_id: str,
                       ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}"
        self.reset()
        return self.request(url, request_type='DELETE')

    def get_network(self, region_id: int,
                    network_id: str,
                    ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}"
        self.reset()
        return self.request(url, request_type='GET')

    def change_network_name(self, region_id: int,
                            network_id: str,
                            name: str
                            ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)
        return self.request(url, request_type='PATCH', body=True)

    def list_networks_with_subnets_details(self, region_id: int,
                                           network_id: str = None,
                                           network_type: str = None,
                                           order_by: str = None,
                                           shared: bool = None,
                                           metadata_kv: str = None,
                                           metadata_k: str = None,
                                           ) -> dict:

        url = f"{self.available_networks_api_url}/{self.project_id}/{region_id}"
        self.reset()
        if network_id is not None:
            self.add_query_param('network_id', network_id)
        if network_type is not None:
            self.add_query_param('network_type', network_type)
        if order_by is not None:
            self.add_query_param('order_by', order_by)
        if shared is not None:
            self.add_query_param('shared', shared)
        if metadata_kv is not None:
            self.add_query_param('metadata_kv', metadata_kv)
        if metadata_k is not None:
            self.add_query_param('metadata_k', metadata_k)

        return self.request(url, request_type='GET', params=True)

    def list_instances_ports_by_network_id(self, region_id: int,
                                           network_id: str
                                           ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}/ports"
        self.reset()

        return self.request(url, request_type='GET')

    def list_network_metadata(self, region_id: int,
                              network_id: str
                              ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}/metadata"
        self.reset()

        return self.request(url, request_type='GET')

    def create_update_network_metadata(self, region_id: int,
                                       network_id: str,
                                       key: str = None,
                                       ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}/metadata"
        self.reset()
        self.add_application_header()
        if key is not None:
            self.add_to_json('key', key)

        return self.request(url, request_type='POST', body=True)

    def replace_network_metadata(self, region_id: int,
                                 network_id: str,
                                 key: str = None,
                                 ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}/metadata"
        self.reset()
        self.add_application_header()
        if key is not None:
            self.add_to_json('key', key)

        return self.request(url, request_type='PUT', body=True)

    def delete_network_metadata_item(self, region_id: int,
                                     network_id: str,
                                     key: str = None,
                                     ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}/metadata_item"
        self.reset()
        if key is not None:
            self.add_query_param('key', key)

        return self.request(url, request_type='DELETE', params=True)

    def get_network_metadata_item(self, region_id: int,
                                  network_id: str,
                                  key: str = None,
                                  ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{network_id}/metadata_item"
        self.reset()
        if key is not None:
            self.add_query_param('key', key)

        return self.request(url, request_type='GET', params=True)
