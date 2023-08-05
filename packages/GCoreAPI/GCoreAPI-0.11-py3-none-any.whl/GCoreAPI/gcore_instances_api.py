from typing import Union, List, Dict

from GCoreAPI.GCore_Base import Base


class Instances(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/instances"

    def list_instances(self, region_id: int,
                       include_baremetal: bool = None,
                       include_k8s: bool = True,
                       exclude_secgroup: str = None,
                       available_floating: str = None,
                       name: str = None,
                       flavor_id: str = None,
                       limit: int = None,
                       offset: int = None,
                       status: str = None,
                       changes_since: str = None,
                       changes_before: str = None,
                       ip: str = None,
                       uuid: str = None,
                       metadata_kv: str = None,
                       metadata_v: str = None,
                       order_by: str = None
                       ) -> dict:

        self.reset()
        url = f"{self.api_url}/{self.project_id}/{region_id}"
        if include_baremetal is not None:
            self.add_query_param('include_baremetal', include_baremetal)
        if include_k8s is not None:
            self.add_query_param('include_k8s', include_k8s)
        if exclude_secgroup is not None:
            self.add_query_param('exclude_secgroup', exclude_secgroup)
        if available_floating is not None:
            self.add_query_param('available_floating', available_floating)
        if name is not None:
            self.add_query_param('name', name)
        if flavor_id is not None:
            self.add_query_param('flavor_id', flavor_id)
        if limit is not None:
            self.add_query_param('limit', limit)
        if offset is not None:
            self.add_query_param('offset', offset)
        if status is not None:
            self.add_query_param('status', status)
        if changes_since is not None:
            self.add_query_param('changes-since', changes_since)
        if changes_before is not None:
            self.add_query_param('changes-before', changes_since)
        if ip is not None:
            self.add_query_param('ip', ip)
        if uuid is not None:
            self.add_query_param('uuid', uuid)
        if metadata_kv is not None:
            self.add_query_param('metadata_kv', metadata_kv)
        if metadata_v is not None:
            self.add_query_param('metadata_v', metadata_v)
        if order_by is not None:
            self.add_query_param('order_by', order_by)

        return self.request(url, request_type='GET', params=True)

    def create_instance(self, region_id: int,
                        interfaces: List[dict],
                        flavor: str,
                        volumes: List[dict],
                        password: str = None,
                        security_groups: List[int] = None,
                        configuration: Union[dict, None] = None,
                        names: List[str] = None,
                        keypair_name: Union[str, None] = None,
                        username: str = None,
                        metadata: dict = None,
                        allow_app_ports: bool = None,
                        name_templates: List[str] = None,
                        servergroup_id: str = None,
                        user_data: str = None
                        ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}".replace('v1', 'v2')
        self.reset()
        self.add_application_header()
        self.add_to_json('interfaces', interfaces)
        self.add_to_json('flavor', flavor)
        self.add_to_json('volumes', volumes)

        if password is not None:
            self.add_to_json('password', password)
        if security_groups is not None:
            self.add_to_json('security_groups', security_groups)
        if configuration is not None:
            self.add_to_json('configuration', configuration)
        if names is not None:
            self.add_to_json('names', names)
        if keypair_name is not None:
            self.add_to_json('keypair_name', keypair_name)
        if username is not None:
            self.add_to_json('username', username)
        if metadata is not None:
            self.add_to_json('metadata', metadata)
        if allow_app_ports is not None:
            self.add_to_json('allow_app_ports', allow_app_ports)
        if name_templates is not None:
            self.add_to_json('name_templates', name_templates)
        if servergroup_id is not None:
            self.add_to_json('servergroup_id', servergroup_id)
        if user_data is not None:
            self.add_to_json('user_data', user_data)

        return self.request(url, request_type='POST', body=True)

    def check_quota_for_instance_creation(self, region_id: int,
                                          name_templates: Union[List[str], None] = None,
                                          names: List[str] = None,
                                          flavor: str = None,
                                          volumes: List[dict] = None,
                                          interfaces: List[dict] = None,
                                          ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/check_limits".replace('v1', 'v2')
        self.reset()
        self.add_application_header()

        if name_templates is not None:
            self.add_to_json('name_templates', name_templates)
        if names is not None:
            self.add_to_json('names', names)
        if flavor is not None:
            self.add_to_json('flavor', flavor)
        if volumes is not None:
            self.add_to_json('volumes', volumes)
        if interfaces is not None:
            self.add_to_json('interfaces', interfaces)

        return self.request(url, request_type='POST', body=True)

    def get_flavors_for_instance(self, region_id: int,
                                 volumes: List[dict],
                                 include_prices: bool = None,
                                 ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/available_flavors"
        self.reset()
        self.add_application_header()
        self.add_to_json('volumes', volumes)
        if include_prices is not None:
            self.add_query_param('include_prices', include_prices)

        return self.request(url, request_type='POST', params=True, body=True)

    def get_instance_naming(self, region_id: int) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/available_names"
        self.reset()
        return self.request(url, request_type='GET', body=True)

    def delete_instance(self, region_id: int,
                        instance_id: int,
                        volumes: str = None,
                        delete_floating: bool = None,
                        floatings: str = None,
                        reserved_fixed_ips: str = None) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}"
        self.reset()
        if volumes is not None:
            self.add_query_param('volumes', volumes)
        if delete_floating is not None:
            self.add_query_param('delete_floating', delete_floating)
        if floatings is not None:
            self.add_query_param('floatings', floatings)
        if reserved_fixed_ips is not None:
            self.add_query_param('reserved_fixed_ips', reserved_fixed_ips)

        return self.request(url, request_type='DELETE', params=True)

    def get_instance(self, region_id: int,
                     instance_id: int,
                     language: str = None,
                     ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}"
        self.reset()
        if language is not None:
            self.add_cookie('language', language)

        return self.request(url, request_type='GET', params=True, cookies=True)

    def rename_instance(self, region_id: int,
                        instance_id: int,
                        name: str,
                        ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)

        return self.request(url, request_type='PATCH', params=True, body=True)

    def list_network_ports(self, region_id: int,
                           instance_id: int,
                           ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/ports"
        self.reset()

        return self.request(url, request_type='GET')

    def start_instance(self, region_id: int,
                       instance_id: int,
                       activate_profile: bool = None
                       ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/start"
        self.reset()
        self.add_application_header()
        if activate_profile is not None:
            self.add_to_json('activate_profile', activate_profile)

        return self.request(url, request_type='POST', body=True)

    def stop_instance(self, region_id: int,
                      instance_id: int,
                      ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/stop"
        self.reset()

        return self.request(url, request_type='POST')

    def power_cycle(self, region_id: int,
                    instance_id: int,
                    ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/powercycle"
        self.reset()

        return self.request(url, request_type='POST')

    def reboot(self, region_id: int,
               instance_id: int,
               ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/reboot"
        self.reset()

        return self.request(url, request_type='POST')

    def suspend(self, region_id: int,
                instance_id: int,
                ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/suspend"
        self.reset()

        return self.request(url, request_type='POST')

    def resume(self, region_id: int,
               instance_id: int,
               ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/resume"
        self.reset()

        return self.request(url, request_type='POST')

    def change_flavor(self, region_id: int,
                      instance_id: int,
                      flavor_id: str,
                      ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/changeflavor"
        self.reset()
        self.add_application_header()
        self.add_to_json('flavor_id', flavor_id)
        return self.request(url, request_type='POST', body=True)

    def get_flavors_to_resize_into(self, region_id: int,
                                   instance_id: int,
                                   include_prices: bool = None,
                                   ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/available_flavors"
        self.reset()
        if include_prices is not None:
            self.add_query_param('include_prices', include_prices)
        return self.request(url, request_type='GET')

    def get_instance_metrics(self, region_id: int,
                             instance_id: int,
                             time_interval: int,
                             time_unit: str
                             ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/metrics"
        self.reset()
        self.add_application_header()
        self.add_to_json('time_interval', time_interval)
        self.add_to_json('time_unit', time_unit)
        return self.request(url, request_type='POST', body=True)

    def filter_instances_by_security_group(self, region_id: int,
                                           secgroup_id: str,
                                           ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{secgroup_id}/instances"
        self.reset()
        return self.request(url, request_type='GET')

    def get_instance_security_group(self, region_id: int,
                                    instance_id: str,
                                    ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/securitygroups"
        self.reset()
        return self.request(url, request_type='GET')

    def assign_security_group(self, region_id: int,
                              instance_id: str,
                              name: str = None,
                              ports_security_group_names: List[dict] = None
                              ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/addsecuritygroups"
        self.reset()
        self.add_application_header()

        if name is not None:
            self.add_to_json('name', name)
        if ports_security_group_names is not None:
            self.add_to_json('ports_security_group_names', ports_security_group_names)

        return self.request(url, request_type='POST', body=True)

    def unassign_security_group(self, region_id: int,
                                instance_id: str,
                                name: str = None,
                                ports_security_group_names: List[dict] = None
                                ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/delsecuritygroups"
        self.reset()
        self.add_application_header()

        if name is not None:
            self.add_to_json('name', name)
        if ports_security_group_names is not None:
            self.add_to_json('ports_security_group_names', ports_security_group_names)

        return self.request(url, request_type='POST', body=True)

    def get_instance_console_url(self, region_id: int,
                                 instance_id: int,
                                 ) -> dict:

        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/get_console"
        self.reset()

        return self.request(url, request_type='GET')

    def attach_interface(self, region_id: int,
                         instance_id: str,
                         security_groups: List[dict] = None,
                         interface_type: str = 'external',
                         subnet_id: str = None,
                         network_id: str = None,
                         port_id: str = None
                         ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/attach_interface"
        self.reset()
        self.add_application_header()

        if interface_type == 'subnet':
            if subnet_id is not None:
                self.add_to_json('subnet_id', subnet_id)
            else:
                print(f"If type is subnet - subnet_id is required")

        elif interface_type == 'any_subnet':
            if network_id is not None:
                self.add_to_json('network_id', network_id)
            else:
                print(f"If type is subnet - network_id is required")

        elif interface_type == 'reversed_fixed_ip':
            if port_id is not None:
                self.add_to_json('port_id', port_id)
            else:
                print(f"If type is reversed_fixed_ip - port_id is required")

        if security_groups is not None:
            self.add_to_json('security_groups', security_groups)

        self.add_to_json('type', interface_type)

        return self.request(url, request_type='POST', body=True)

    def detach_interface(self, region_id: int,
                         instance_id: str,
                         port_id: str,
                         ip_address: str
                         ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/detach_interface"
        self.reset()
        self.add_application_header()

        self.add_to_json('port_id', port_id)
        self.add_to_json('ip_address', ip_address)

        return self.request(url, request_type='POST', body=True)

    def list_network_instances(self, region_id: int,
                               instance_id: str,
                               ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/interfaces"
        self.reset()

        return self.request(url, request_type='GET')

    def list_instance_metadata(self, region_id: int,
                               instance_id: str,
                               ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/metadata"
        self.reset()

        return self.request(url, request_type='GET')

    def create_or_update_metadata(self, region_id: int,
                                  instance_id: str,
                                  key: str = None,
                                  ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/metadata"
        self.reset()
        self.add_application_header()
        if key is not None:
            self.add_to_json('key', key)

        return self.request(url, request_type='GET', body=True)

    def replace_metadata(self, region_id: int,
                         instance_id: str,
                         key: str = None,
                         ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/metadata"
        self.reset()
        self.add_application_header()
        if key is not None:
            self.add_to_json('key', key)

        return self.request(url, request_type='PUT', body=True)

    def delete_instance_metadata_item(self, region_id: int,
                                      instance_id: str,
                                      key: str,
                                      ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/metadata/{key}"
        self.reset()

        return self.request(url, request_type='DELETE')

    def get_instance_metadata_item(self, region_id: int,
                                   instance_id: str,
                                   key: str,
                                   ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/metadata/{key}"
        self.reset()

        return self.request(url, request_type='GET')

    def delete_instance_metadata_item_by_key(self, region_id: int,
                                             instance_id: str,
                                             key: str = None,
                                             ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/metadata_item"
        self.reset()
        if key is not None:
            self.add_query_param('key', key)

        return self.request(url, request_type='DELETE', params=True)

    def get_instance_metadata_item_by_key(self, region_id: int,
                                          instance_id: str,
                                          key: str = None,
                                          ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/metadata_item"
        self.reset()
        if key is not None:
            self.add_query_param('key', key)

        return self.request(url, request_type='GET', params=True)

    def put_instance_into_server_group(self, region_id: int,
                                       instance_id: str,
                                       servergroup_id: str,
                                       ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/put_into_servergroup"
        self.reset()
        self.add_application_header()
        self.add_to_json('servergroup_id', servergroup_id)

        return self.request(url, request_type='PUT', body=True)

    def remove_instance_into_server_group(self, region_id: int,
                                          instance_id: str,
                                          ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/remove_from_servergroup"
        self.reset()

        return self.request(url, request_type='PUT')

    def get_amount_available_baremetal_nodes_without_reservation(self, region_id: int,
                                                                 client_id: int
                                                                 ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}".replace('instances', 'bmcapacity').replace('v1', 'v2')
        self.reset()
        if client_id is not None:
            self.add_query_param('client_id', client_id)

        return self.request(url, request_type='GET')

    def list_baremetal_instances(self, region_id: int,
                                 type_ddos_profile: str = None,
                                 with_ddos: bool = None,
                                 profile_name: str = None,
                                 only_with_fixed_external_ip: bool = None,
                                 name: str = None,
                                 flavor_id: str = None,
                                 limit: int = None,
                                 offset: int = None,
                                 status: str = None,
                                 changes_since: str = None,
                                 changes_before: str = None,
                                 ip: str = None,
                                 uuid: str = None,
                                 metadata_kv: str = None,
                                 metadata_v: str = None,
                                 order_by: str = None
                                 ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}".replace('instances', 'bminstances')
        self.reset()
        if type_ddos_profile is not None:
            self.add_query_param('type_ddos_profile', type_ddos_profile)
        if with_ddos is not None:
            self.add_query_param('with_ddos', with_ddos)
        if profile_name is not None:
            self.add_query_param('profile_name', profile_name)
        if only_with_fixed_external_ip is not None:
            self.add_query_param('only_with_fixed_external_ip', only_with_fixed_external_ip)
        if name is not None:
            self.add_query_param('name', name)
        if flavor_id is not None:
            self.add_query_param('flavor_id', flavor_id)
        if limit is not None:
            self.add_query_param('limit', limit)
        if offset is not None:
            self.add_query_param('offset', offset)
        if status is not None:
            self.add_query_param('status', status)
        if changes_since is not None:
            self.add_query_param('changes-since', changes_since)
        if changes_before is not None:
            self.add_query_param('changes-before', changes_since)
        if ip is not None:
            self.add_query_param('ip', ip)
        if uuid is not None:
            self.add_query_param('uuid', uuid)
        if metadata_kv is not None:
            self.add_query_param('metadata_kv', metadata_kv)
        if metadata_v is not None:
            self.add_query_param('metadata_v', metadata_v)
        if order_by is not None:
            self.add_query_param('order_by', order_by)

        return self.request(url, request_type='GET', params=True)

    def create_baremetal_server(self, region_id: int,
                                interfaces: List,
                                flavor: str,
                                app_config: Union[Dict, None] = None,
                                password: str = None,
                                ddos_profile: Union[Dict, None] = None,
                                names: List[str] = None,

                                keypair_name: Union[str, None] = None,
                                apptemplate_id: str = None,
                                username: int = None,
                                metadata: Dict = None,
                                name_templates: List[str] = None,
                                image_id: str = None,
                                user_data: str = None,
                                ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}".replace('instances', 'bminstances')
        self.reset()
        self.add_application_header()
        self.add_to_json('interfaces', interfaces)
        self.add_to_json('flavor', flavor)

        if app_config is not None:
            self.add_to_json('app_config', app_config)
        if password is not None:
            self.add_to_json('password', password)
        if ddos_profile is not None:
            self.add_to_json('ddos_profile', ddos_profile)
        if names is not None:
            self.add_to_json('names', names)
        if keypair_name is not None:
            self.add_to_json('keypair_name', keypair_name)
        if apptemplate_id is not None:
            self.add_to_json('apptemplate_id', apptemplate_id)
        if username is not None:
            self.add_to_json('username', username)
        if metadata is not None:
            self.add_to_json('metadata', metadata)
        if name_templates is not None:
            self.add_to_json('name_templates', name_templates)
        if image_id is not None:
            self.add_to_json('image_id', image_id)
        if user_data is not None:
            self.add_to_json('user_data', user_data)

        return self.request(url, request_type='POST', body=True)

    def get_flavors_for_baremetal_instance(self, region_id: int,
                                           image_id: str,
                                           include_prices: bool = None
                                           ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/available_flavors".replace('instances', 'bminstances')
        self.reset()
        self.add_application_header()

        self.add_to_json('image_id', image_id)
        if include_prices is not None:
            self.add_query_param('include_prices', include_prices)

        return self.request(url, request_type='POST', body=True, params=True)

    def rebuild_baremetal_instance(self, region_id: int,
                                   instance_id: str,
                                   image_id: str = None
                                   ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/{instance_id}/rebuild".replace('instances', 'bminstances')
        self.reset()
        if image_id is not None:
            self.add_application_header()
            self.add_to_json('image_id', image_id)
            return self.request(url, request_type='POST', body=True)
        return self.request(url, request_type='POST')

    def check_quota_for_baremetal_server_creation(self, region_id: int,
                                                  flavor: str = None,
                                                  interfaces: List[dict] = None,
                                                  ) -> dict:
        url = f"{self.api_url}/{self.project_id}/{region_id}/check_limits".replace('instances', 'bminstances')
        self.reset()
        self.add_application_header()
        if flavor is not None:
            self.add_to_json('flavor', flavor)
        if interfaces is not None:
            self.add_to_json('interfaces', interfaces)

        return self.request(url, request_type='POST', body=True)

    def search_for_instance_in_all_clients_reseller(self, name: str = None,
                                                    instance_id: str = None,
                                                    ) -> dict:
        url = f"{self.api_url}/search"
        self.reset()
        if name is not None:
            self.add_query_param('name', name)
        if instance_id is not None:
            self.add_query_param('id', instance_id)

        return self.request(url, request_type='GET', params=True)
