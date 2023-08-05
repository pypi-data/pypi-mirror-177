from typing import Union, List, Dict

from GCoreAPI.GCore_Base import Base


class Regions(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/regions"

    def get_region(self, region_id: int, show_volume_types: bool = None) -> dict:
        url = f'{self.api_url}/{region_id}'
        self.reset()
        self.add_application_header()

        if show_volume_types is not None:
            self.add_to_json('show_volume_types', show_volume_types)

        return self.request(url, request_type='GET', body=True)

    def list_region(self, show_volume_types: bool = None) -> dict:
        url = f'{self.api_url}'
        self.reset()
        self.add_application_header()

        if show_volume_types is not None:
            self.add_to_json('show_volume_types', show_volume_types)

        return self.request(url, request_type='GET', body=True)

    def get_city_id_by_name(self, region_name: str) -> int:
        list_regions = self.list_region()
        for region in list_regions['results']:
            if region['display_name'].lower() == region_name.strip().lower():
                return int(region['id'])

    def get_city_name_by_id(self, region_id: int) -> str:
        list_regions = self.list_region()
        for region in list_regions['results']:
            if int(region['id']) == region_id:
                return str(region['display_name'])

    def get_cities(self, country: str = None) -> List:
        cities = []
        list_regions = self.list_region()
        for region in list_regions['results']:
            if region['country'].lower() == country.lower():
                cities.append(region['display_name'])
        return cities

    def get_countries(self) -> List:
        countries = []
        list_regions = self.list_region()
        for region in list_regions['results']:
            countries.append(region['country'])

        return countries


