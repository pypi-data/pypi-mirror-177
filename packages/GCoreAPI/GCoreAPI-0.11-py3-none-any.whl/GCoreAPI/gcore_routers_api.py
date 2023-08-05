from typing import Union, List, Dict

from GCoreAPI.GCore_Base import Base


class Routers(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/routers"

    def get_router(self, router_id: str, region_id: int) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}'
        self.reset()

        return self.request(url, request_type='GET', params=True)

    def list_routers(self, region_id: int) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}'
        self.reset()

        return self.request(url, request_type='GET', params=True)

    def create_router(self, region_id: int,
                      name: str,
                      routes: List[Dict] = None,
                      interfaces: List = None,
                      external_gateway_info: Dict = None) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}'
        self.reset()
        self.add_application_header()

        self.add_to_json('name', name)
        if routes is not None:
            self.add_to_json('routes', routes)
        if interfaces is not None:
            self.add_to_json('interfaces', interfaces)
        if external_gateway_info is not None:
            self.add_to_json('external_gateway_info', external_gateway_info)

        return self.request(url, request_type='POST', body=True)

    def delete_router(self, region_id: int, router_id: str = None) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}'
        self.reset()

        return self.request(url, request_type='DELETE', body=True)

    def update_router(self, region_id: int,
                      router_id: str = None,
                      name: str = None,
                      routes: List[Dict] = None,
                      external_gateway_info: Dict = None) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}'
        self.reset()
        self.add_application_header()

        if routes is not None:
            self.add_to_json('routes', routes)
        if name is not None:
            self.add_to_json('name', name)
        if external_gateway_info is not None:
            self.add_to_json('external_gateway_info', external_gateway_info)

        return self.request(url, request_type='PATCH', body=True)

    def attach_subnet(self, region_id: int, router_id: str, subnet_id: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}/attach'
        self.reset()
        self.add_application_header()

        self.add_to_json('subnet_id', subnet_id)

        return self.request(url, request_type='POST', body=True)

    def detach_subnet(self, region_id: int, router_id: str, subnet_id: str) -> dict:
        url = f'{self.api_url}/{self.project_id}/{region_id}/{router_id}/detach'
        self.reset()
        self.add_application_header()

        self.add_to_json('subnet_id', subnet_id)

        return self.request(url, request_type='POST', body=True)

    def get_router_id_by_name(self, region_id: int, router_name: str) -> str:
        list_routers = self.list_routers(region_id=region_id)

        for router in list_routers['results']:
            if router['name'] == router_name:
                return router['id']

    def get_router_name_by_id(self, region_id: int, router_id: str) -> str:
        list_routers = self.list_routers(region_id=region_id)

        for router in list_routers['results']:
            if router['id'] == region_id:
                return router['name']








