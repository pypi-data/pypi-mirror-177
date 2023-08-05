from typing import Union, List, Dict

from GCoreAPI.GCore_Base import Base


class Flavors(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}"

    def list_flavors(self, region_id: int,
                     include_prices: bool = None,
                     disabled: bool = None,
                     exclude_windows: bool = None) -> dict:
        self.reset()
        url = f"{self.api_url}/flavors/{self.project_id}/{region_id}"

        if include_prices is not None:
            self.add_query_param('include_prices', include_prices)
        if disabled is not None:
            self.add_query_param('disabled', disabled)
        if exclude_windows is not None:
            self.add_query_param('exclude_windows', exclude_windows)

        return self.request(url, request_type='GET', params=True)

    def list_flavors_k8(self, region_id: int,
                        exclude_sgx: bool = None,
                        exclude_gpu: bool = None,
                        include_prices: bool = None) -> dict:
        self.reset()
        url = f"{self.api_url}/k8s/{self.project_id}/{region_id}/flavors"

        if exclude_sgx is not None:
            self.add_query_param('exclude_sgx', exclude_sgx)
        if exclude_gpu is not None:
            self.add_query_param('exclude_gpu', exclude_gpu)
        if include_prices is not None:
            self.add_query_param('include_prices', include_prices)

        return self.request(url, request_type='GET', params=True)

    def list_flavors_baremetal(self, region_id: int,
                               include_prices: bool = None,
                               disabled: bool = None,
                               exclude_windows: bool = None) -> dict:
        self.reset()
        url = f"{self.api_url}/bmflavors/{self.project_id}/{region_id}"

        if include_prices is not None:
            self.add_query_param('include_prices', include_prices)
        if disabled is not None:
            self.add_query_param('disabled', disabled)
        if exclude_windows is not None:
            self.add_query_param('exclude_windows', exclude_windows)

        return self.request(url, request_type='GET', params=True)

    def list_flavors_baremetal_default(self, region_id: int,
                                       include_prices: bool = None,
                                       disabled: bool = None,
                                       exclude_windows: bool = None) -> dict:
        self.reset()
        url = f"{self.api_url}/bmflavors/{region_id}"

        if include_prices is not None:
            self.add_query_param('include_prices', include_prices)
        if disabled is not None:
            self.add_query_param('disabled', disabled)
        if exclude_windows is not None:
            self.add_query_param('exclude_windows', exclude_windows)

        return self.request(url, request_type='GET', params=True)

    def list_flavors_baremetal_available(self, region_id: int,
                                         windows_os: bool = None,
                                         disabled: bool = None,
                                         client_id: int = None) -> dict:
        self.reset()
        url = f"{self.api_url}/bm_reservation_flavors/{region_id}"

        if windows_os is not None:
            self.add_query_param('windows_os', windows_os)
        if disabled is not None:
            self.add_query_param('disabled', disabled)
        if client_id is not None:
            self.add_query_param('client_id', client_id)

        return self.request(url, request_type='GET', params=True)




