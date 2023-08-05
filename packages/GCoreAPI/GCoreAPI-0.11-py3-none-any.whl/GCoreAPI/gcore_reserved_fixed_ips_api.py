from typing import List

from GCoreAPI.GCore_Base import Base


class ReservedFixedIPs(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/reserved_fixed_ips"

    def list_reserved_fixed_ips(self, region_id: int,
                                external_only: bool = None,
                                internal_only: bool = None,
                                available_only: bool = None,
                                vip_only: bool = None,
                                device_id: str = None,
                                limit: int = None,
                                offset: int = None
                                ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()

        if external_only is not None:
            self.add_query_param('external_only', external_only)
        if internal_only is not None:
            self.add_query_param('internal_only', internal_only)
        if available_only is not None:
            self.add_query_param('available_only', available_only)
        if vip_only is not None:
            self.add_query_param('vip_only', vip_only)
        if device_id is not None:
            self.add_query_param('device_id', device_id)
        if limit is not None:
            self.add_query_param('limit', limit)
        if offset is not None:
            self.add_query_param('offset', offset)

        return self.request(url, request_type='GET', params=True)

    def create_reserved_fixed_ips(self, region_id: int,
                                  is_vip: bool = None,
                                  reversed_fixed_ip_type: str = 'external',
                                  subnet_id: str = None,
                                  network_id: str = None,
                                  ip_address: str = None
                                  ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        self.add_application_header()

        if reversed_fixed_ip_type == 'subnet':
            if subnet_id is not None:
                self.add_to_json('subnet_id', subnet_id)
            else:
                print(f"If type is subnet - subnet_id is required")

        elif reversed_fixed_ip_type == 'any_subnet':
            if network_id is not None:
                self.add_to_json('network_id', network_id)
            else:
                print(f"If type is any_subnet - network_id is required")

        elif reversed_fixed_ip_type == 'ip_address':
            if network_id is not None:
                self.add_to_json('network_id', network_id)
            else:
                print(f"If type is ip_address - network_id is required")

            if ip_address is not None:
                self.add_to_json('ip_address', ip_address)
            else:
                print(f"If type is ip_address - ip_address is required")

        if is_vip is not None:
            self.add_to_json('is_vip', is_vip)
        if reversed_fixed_ip_type is not None:
            self.add_to_json('type', reversed_fixed_ip_type)

        return self.request(url, request_type='POST', body=True)

    def delete_reserved_fixed_ips(self, region_id: int,
                                  port_id: str
                                  ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{port_id}"
        self.reset()

        return self.request(url, request_type='DELETE')

    def get_reserved_fixed_ips(self, region_id: int,
                               port_id: str
                               ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{port_id}"
        self.reset()

        return self.request(url, request_type='GET')

    def switch_vip_status_of_reversed_fixed_ip(self, region_id: int,
                                               port_id: int,
                                               is_vip: bool) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{port_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('is_vip', is_vip)

        return self.request(url, request_type='PATCH', body=True)

    def list_instance_ports_that_share_vip(self, region_id: int,
                                           port_id: int,
                                           ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{port_id}/connected_devices"
        self.reset()
        return self.request(url, request_type='GET')

    def add_ports_that_share_vip(self, region_id: int,
                                 port_id: int,
                                 port_ids: List[str] = None
                                 ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{port_id}/connected_devices"
        self.reset()
        self.add_application_header()
        self.add_to_json('port_ids', port_ids)
        return self.request(url, request_type='PATCH', body=True)

    def replace_ports_that_share_vip(self, region_id: int,
                                     port_id: int,
                                     port_ids: List[str] = None
                                     ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{port_id}/connected_devices"
        self.reset()
        self.add_application_header()
        self.add_to_json('port_ids', port_ids)
        return self.request(url, request_type='PUT', body=True)

    def list_instances_ports_available_for_vip_connecting(self, region_id: int,
                                                          port_id: int,
                                                          ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{port_id}/available_devices"
        self.reset()
        return self.request(url, request_type='GET')
