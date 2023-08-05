from typing import Union, List

from GCoreAPI.GCore_Base import Base


class Loadbalancers(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/loadbalancers"
        self.lbpools_api_url = f"{self.BASE_URL}/lbpools"
        self.lblisteners_api_url = f"{self.BASE_URL}/lblisteners"
        self.lbflavors_api_url = f"{self.BASE_URL}/lbflavors"

    def list_loadbalancers(self, region_id: int,
                           show_stats: bool = None,
                           assigned_floating: bool = None,
                           metadata_kv: str = None,
                           metadata_v: str = None,
                           ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        if show_stats is not None:
            self.add_query_param('show_stats', show_stats)
        if assigned_floating is not None:
            self.add_query_param('assigned_floating', assigned_floating)
        if metadata_kv is not None:
            self.add_query_param('metadata_kv', metadata_kv)
        if metadata_v is not None:
            self.add_query_param('metadata_v', metadata_v)

        return self.request(url, request_type='GET', params=True)

    def create_loadbalancer(self, region_id: int,
                            name: str,
                            flavor: Union[str, None] = None,
                            vip_port_id: str = None,
                            metadata: Union[dict, None] = None,
                            listeners: Union[dict, None] = None,
                            tag: Union[list, None] = None,
                            vip_subnet_id: str = None,
                            floating_ip: dict = None,
                            ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)

        if flavor is not None:
            self.add_to_json('flavor', flavor)
        if vip_port_id is not None:
            self.add_to_json('vip_port_id', vip_port_id)
        if metadata is not None:
            self.add_to_json('metadata', metadata)
        if listeners is not None:
            self.add_to_json('listeners', listeners)
        if tag is not None:
            self.add_to_json('tag', tag)
        if vip_subnet_id is not None:
            self.add_to_json('vip_subnet_id', vip_subnet_id)
        if floating_ip is not None:
            self.add_to_json('floating_ip', floating_ip)

        return self.request(url, request_type='POST', body=True)

    def check_quota_for_loadbalancer_creation(self, region_id: int,
                                              name: str,
                                              vip_port_id: str = None,
                                              flavor: Union[str, None] = None,
                                              metadata: Union[dict, None] = None,
                                              listeners: Union[dict, None] = None,
                                              tag: Union[list, None] = None,
                                              vip_subnet_id: str = None,
                                              floating_ip: dict = None,
                                              ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/check_limits"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)

        if flavor is not None:
            self.add_to_json('flavor', flavor)
        if vip_port_id is not None:
            self.add_to_json('vip_port_id', vip_port_id)
        if metadata is not None:
            self.add_to_json('metadata', metadata)
        if listeners is not None:
            self.add_to_json('listeners', listeners)
        if tag is not None:
            self.add_to_json('tag', tag)
        if vip_subnet_id is not None:
            self.add_to_json('vip_subnet_id', vip_subnet_id)
        if floating_ip is not None:
            self.add_to_json('floating_ip', floating_ip)

        return self.request(url, request_type='POST', body=True)

    def delete_loadbalancer(self, region_id: int,
                            loadbalancer_id: str,
                            ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}"
        self.reset()
        return self.request(url, request_type='DELETE')

    def get_loadbalancer(self, region_id: int,
                         loadbalancer_id: str,
                         show_stats: bool = None
                         ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}"
        self.reset()
        if show_stats is not None:
            self.add_query_param('show_stats', show_stats)

        return self.request(url, request_type='GET', params=True)

    def rename_loadbalancer(self, region_id: int,
                            loadbalancer_id: str,
                            name: str
                            ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)

        return self.request(url, request_type='PATCH', body=True)

    def get_custom_security_group_for_loadbalancers(self, region_id: int,
                                                    loadbalancer_id: str,
                                                    ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}/securitygroup"
        self.reset()

        return self.request(url, request_type='GET')

    def create_custom_security_group_for_loadbalancers(self, region_id: int,
                                                       loadbalancer_id: str,
                                                       ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}/securitygroup"
        self.reset()

        return self.request(url, request_type='POST')

    def get_loadbalancers_metrics(self, region_id: int,
                                  loadbalancer_id: str,
                                  time_interval: int,
                                  time_unit: str
                                  ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}/metrics"
        self.reset()
        self.add_application_header()
        self.add_to_json('time_interval', time_interval)
        self.add_to_json('time_unit', time_unit)
        return self.request(url, request_type='POST', body=True)

    def list_loadbalancers_pools(self, region_id: int,
                                 loadbalancer_id: str = None,
                                 listener_id: str = None,
                                 details: bool = None
                                 ) -> dict:

        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}"
        self.reset()
        if loadbalancer_id is not None:
            self.add_query_param('loadbalancer_id', loadbalancer_id)
        if listener_id is not None:
            self.add_query_param('listener_id', listener_id)
        if details is not None:
            self.add_query_param('details', details)

        return self.request(url, request_type='GET', params=True)

    def create_loadbalancer_pool(self, region_id: int,
                                 name: str,
                                 protocol: str,
                                 lb_algorithm: str,
                                 listener_id: str = None,
                                 members: List[dict] = None,
                                 timeout_member_connect: Union[int, None] = None,
                                 timeout_member_data: Union[int, None] = None,
                                 session_persistence: Union[dict, None] = None,
                                 timeout_client_data: Union[int, None] = None,
                                 healthmonitor: dict = None,
                                 loadbalancer_id: str = None,

                                 ) -> dict:

        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)
        self.add_to_json('protocol', protocol)
        self.add_to_json('lb_algorithm', lb_algorithm)

        if listener_id is not None:
            self.add_to_json('listener_id', listener_id)
        if members is not None:
            self.add_to_json('members', members)
        if timeout_member_connect is not None:
            self.add_to_json('timeout_member_connect', timeout_member_connect)
        if timeout_member_data is not None:
            self.add_to_json('timeout_member_data', timeout_member_data)
        if session_persistence is not None:
            self.add_to_json('session_persistence', session_persistence)
        if timeout_client_data is not None:
            self.add_to_json('timeout_client_data', timeout_client_data)
        if healthmonitor is not None:
            self.add_to_json('healthmonitor', healthmonitor)
        if loadbalancer_id is not None:
            self.add_to_json('loadbalancer_id', loadbalancer_id)

        return self.request(url, request_type='POST', body=True)

    def delete_loadbalancer_pool(self, region_id: int,
                                 pool_id: str,
                                 ) -> dict:
        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}/{pool_id}"
        self.reset()
        return self.request(url, request_type='DELETE')

    def get_loadbalancer_pool(self, region_id: int,
                              pool_id: str,
                              ) -> dict:
        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}/{pool_id}"
        self.reset()
        return self.request(url, request_type='GET')

    def patch_loadbalancer_pool(self, region_id: int,
                                pool_id: str,
                                name: str = None,
                                members: List[dict] = None,
                                timeout_member_connect: Union[int, None] = None,
                                timeout_member_data: Union[int, None] = None,
                                session_persistence: Union[dict, None] = None,
                                timeout_client_data: Union[int, None] = None,
                                healthmonitor: dict = None,
                                loadbalancer_id: str = None,

                                ) -> dict:
        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}/{pool_id}"
        self.reset()
        self.add_application_header()

        if name is not None:
            self.add_to_json('name', name)
        if members is not None:
            self.add_to_json('members', members)
        if timeout_member_connect is not None:
            self.add_to_json('timeout_member_connect', timeout_member_connect)
        if timeout_member_data is not None:
            self.add_to_json('timeout_member_data', timeout_member_data)
        if session_persistence is not None:
            self.add_to_json('session_persistence', session_persistence)
        if timeout_client_data is not None:
            self.add_to_json('timeout_client_data', timeout_client_data)
        if healthmonitor is not None:
            self.add_to_json('healthmonitor', healthmonitor)
        if loadbalancer_id is not None:
            self.add_to_json('loadbalancer_id', loadbalancer_id)

        return self.request(url, request_type='PATCH', body=True)

    def create_loadbalancer_pool_member(self, region_id: int,
                                        pool_id: str,
                                        address: str,
                                        protocol_port: int,
                                        weight: int = None,
                                        instance_id: Union[str, None] = None,
                                        admin_state_up: Union[bool, None] = None,
                                        loadbalancer_id: Union[str, None] = None,
                                        subnet_id: Union[str, None] = None,
                                        ) -> dict:
        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}/{pool_id}/member"
        self.reset()
        self.add_application_header()
        self.add_to_json('address', address)
        self.add_to_json('protocol_port', protocol_port)
        if weight is not None:
            self.add_to_json('weight', weight)
        if instance_id is not None:
            self.add_to_json('instance_id', instance_id)
        if admin_state_up is not None:
            self.add_to_json('admin_state_up', admin_state_up)
        if loadbalancer_id is not None:
            self.add_to_json('loadbalancer_id', loadbalancer_id)
        if subnet_id is not None:
            self.add_to_json('subnet_id', subnet_id)

        return self.request(url, request_type='POST', body=True)

    def delete_loadbalancer_health_monitor(self, region_id: int,
                                           pool_id: str,
                                           ) -> dict:
        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}/{pool_id}/healthmonitor"
        self.reset()
        return self.request(url, request_type='DELETE')

    def create_loadbalancer_health_monitor(self, region_id: int,
                                           pool_id: str,
                                           max_retries: int,
                                           monitor_type: str,
                                           delay: int,
                                           timeout: int,
                                           http_method: Union[str, None] = None,
                                           url_path: str = '/',
                                           max_retries_down: int = None,
                                           expected_codes: Union[str, None] = None,
                                           ) -> dict:
        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}/{pool_id}/healthmonitor"
        self.reset()
        self.add_application_header()
        self.add_to_json('max_retries', max_retries)
        self.add_to_json('type', monitor_type)
        self.add_to_json('delay', delay)
        self.add_to_json('timeout', timeout)
        self.add_to_json('url_pat', url_path)

        if http_method is not None:
            self.add_to_json('http_method', http_method)
        if max_retries_down is not None:
            self.add_to_json('max_retries_down', max_retries_down)
        if expected_codes is not None:
            self.add_to_json('expected_codes', expected_codes)

        return self.request(url, request_type='POST', body=True)

    def delete_loadbalancer_pool_member(self, region_id: int,
                                        pool_id: str,
                                        member_id: int,
                                        ) -> dict:
        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}/{pool_id}/member/{member_id}"
        self.reset()

        return self.request(url, request_type='DELETE')

    def list_loadbalancer_listeners(self, region_id: int,
                                    loadbalancer_id: str = None,
                                    show_stats: bool = None
                                    ) -> dict:
        url = f"{self.lbpools_api_url}/{self.project_id}/{region_id}/"
        self.reset()
        if loadbalancer_id is not None:
            self.add_query_param('loadbalancer_id', loadbalancer_id)
        if show_stats is not None:
            self.add_query_param('show_stats', show_stats)

        return self.request(url, request_type='GET', params=True)

    def create_loadbalancer_listener(self, region_id: int,
                                     name: str,
                                     protocol_port: int,
                                     protocol: str,
                                     loadbalancer_id: str,
                                     sni_secret_id: List[str] = None,
                                     secret_id: str = None,
                                     insert_x_forwarded: bool = None
                                     ) -> dict:
        url = f"{self.lblisteners_api_url}/{self.project_id}/{region_id}/"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)
        self.add_to_json('protocol_port', protocol_port)
        self.add_to_json('protocol', protocol)
        self.add_to_json('loadbalancer_id', loadbalancer_id)
        if sni_secret_id is not None:
            self.add_to_json('sni_secret_id', sni_secret_id)
        if secret_id is not None:
            self.add_to_json('secret_id', secret_id)
        if insert_x_forwarded is not None:
            self.add_to_json('insert_x_forwarded', insert_x_forwarded)

        return self.request(url, request_type='POST', body=True)

    def delete_loadbalancer_listener(self, region_id: int,
                                     listener_id: str
                                     ) -> dict:
        url = f"{self.lblisteners_api_url}/{self.project_id}/{region_id}/{listener_id}"
        self.reset()

        return self.request(url, request_type='DELETE')

    def get_listener(self, region_id: int,
                     listener_id: str,
                     show_stats: bool = None
                     ) -> dict:
        url = f"{self.lblisteners_api_url}/{self.project_id}/{region_id}/{listener_id}"
        self.reset()
        if show_stats is not None:
            self.add_query_param('show_stats', show_stats)

        return self.request(url, request_type='GET', params=True)

    def edit_listener_name(self, region_id: int,
                           listener_id: str,
                           name: str
                           ) -> dict:
        url = f"{self.lblisteners_api_url}/{self.project_id}/{region_id}/{listener_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)

        return self.request(url, request_type='PATCH', body=True)

    def update_listener(self, region_id: int,
                        listener_id: str,
                        sni_secret_id: List[str] = None,
                        name: str = None,
                        secret_id: str = None,

                        ) -> dict:
        url = f"{self.lblisteners_api_url}/{self.project_id}/{region_id}/{listener_id}".replace('v1', 'v2')
        self.reset()
        self.add_application_header()
        if sni_secret_id is not None:
            self.add_to_json('sni_secret_id', sni_secret_id)
        if name is not None:
            self.add_to_json('name', name)
        if secret_id is not None:
            self.add_to_json('secret_id', secret_id)

        return self.request(url, request_type='PATCH', body=True)

    def list_loadbalancer_flavors(self, region_id: int,
                                  include_prices: bool = None,
                                  ) -> dict:
        url = f"{self.lbflavors_api_url}/{self.project_id}/{region_id}"
        self.reset()
        if include_prices is not None:
            self.add_query_param('include_prices', include_prices)

        return self.request(url, request_type='GET', params=True)

    def list_loadbalancer_metadata(self, region_id: int,
                                   loadbalancer_id: str = None,
                                   ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}/metadata"
        self.reset()

        return self.request(url, request_type='GET')

    def create_update_loadbalancer_metadata(self, region_id: int,
                                            loadbalancer_id: str = None,
                                            key: str = None
                                            ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}/metadata"
        self.reset()
        self.add_application_header()
        if key is not None:
            self.add_to_json('key', key)

        return self.request(url, request_type='POST', body=True)

    def replace_loadbalancer_metadata(self, region_id: int,
                                      loadbalancer_id: str = None,
                                      key: str = None
                                      ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}/metadata"
        self.reset()
        self.add_application_header()
        if key is not None:
            self.add_to_json('key', key)

        return self.request(url, request_type='PUT', body=True)

    def delete_loadbalancer_metadata(self, region_id: int,
                                     loadbalancer_id: str = None,
                                     key: str = None
                                     ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}/metadata_item"
        self.reset()
        if key is not None:
            self.add_query_param('key', key)

        return self.request(url, request_type='DELETE', params=True)

    def get_loadbalancer_metadata_item_by_key(self, region_id: int,
                                              loadbalancer_id: str = None,
                                              key: str = None
                                              ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{loadbalancer_id}/metadata_item"
        self.reset()
        if key is not None:
            self.add_query_param('key', key)

        return self.request(url, request_type='GET', params=True)
