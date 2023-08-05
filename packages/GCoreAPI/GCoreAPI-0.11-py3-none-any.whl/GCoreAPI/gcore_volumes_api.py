from typing import Dict, List

from GCoreAPI.GCore_Base import Base


class Volumes(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/volumes"

    def list_volumes(self, project_id: int,
                     region_id: int,
                     instance_id: str = None,
                     cluster_id: str = None,
                     limit: int = None,
                     offset: int = None,
                     bootable: bool = None,
                     has_attachments: bool = None,
                     id_part: str = None,
                     name_part: str = None,
                     metadata_kv: str = None,
                     metadata_k: str = None
                     ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}"
        self.reset()

        if instance_id is not None:
            self.add_query_param('instance_id', instance_id)
        if cluster_id is not None:
            self.add_query_param('cluster_id', cluster_id)
        if limit is not None:
            self.add_query_param('limit', limit)
        if offset is not None:
            self.add_query_param('offset', offset)
        if bootable is not None:
            self.add_query_param('bootable', bootable)
        if has_attachments is not None:
            self.add_query_param('has_attachments', has_attachments)
        if id_part is not None:
            self.add_query_param('id_part', id_part)
        if name_part is not None:
            self.add_query_param('name_part', name_part)
        if metadata_kv is not None:
            self.add_query_param('metadata_kv', metadata_kv)
        if metadata_k is not None:
            self.add_query_param('metadata_k', metadata_k)

        return self.request(url, request_type='GET', params=True)

    def create_volume(self, project_id: int,
                      region_id: int,
                      name: str,
                      source: str = 'image',
                      size: int = None,
                      attachment_tag: str = None,
                      type_name: str = None,
                      instance_id_to_attach_to: str = None,
                      metadata: Dict = None,
                      image_id: str = None,
                      lifecycle_policy_ids: List[int] = None,
                      snapshot_id: str = None,
                      ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)
        self.add_to_json('source', source)

        if source == 'image':
            if size is not None:
                self.add_to_json('size', size)
            else:
                print(f'If source is image - size is required')
            if image_id is not None:
                self.add_to_json('image_id', image_id)
            else:
                print(f'If source is image - image_id is required')

        elif source == 'snapshot':
            if snapshot_id is not None:
                self.add_to_json('snapshot_id', snapshot_id)
            else:
                print(f'If source is snapshot - snapshot_id is required')

        elif source == 'new_volume':
            if size is not None:
                self.add_to_json('size', size)
            else:
                print(f'If source is new_volume - size is required')

        if attachment_tag is not None:
            self.add_to_json('attachment_tag', attachment_tag)
        if type_name is not None:
            self.add_to_json('type_name', type_name)
        if instance_id_to_attach_to is not None:
            self.add_to_json('instance_id_to_attach_to', instance_id_to_attach_to)
        if metadata is not None:
            self.add_to_json('metadata', metadata)
        if lifecycle_policy_ids is not None:
            self.add_to_json('lifecycle_policy_ids', lifecycle_policy_ids)

        return self.request(url, request_type='POST', body=True)

    def delete_volume(self, project_id: int,
                      region_id: int,
                      pk: str,
                      snapshots: str = None
                      ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}"
        self.reset()
        if snapshots is not None:
            self.add_query_param('snapshots', snapshots)

        return self.request(url, request_type='DELETE', params=True)

    def get_volume(self, project_id: int,
                   region_id: int,
                   pk: str,
                   ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}"
        self.reset()

        return self.request(url, request_type='GET')

    def change_volume_name(self, project_id: int,
                           region_id: int,
                           pk: str,
                           name: str
                           ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}"
        self.reset()
        self.add_application_header()
        self.add_to_json('name', name)

        return self.request(url, request_type='PATCH', body=True)

    def attach_volume(self, project_id: int,
                      region_id: int,
                      pk: str,
                      instance_id: str,
                      attachment_tag: str = None
                      ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/attach"
        self.reset()
        self.add_application_header()
        self.add_to_json('instance_id', instance_id)

        if attachment_tag is not None:
            self.add_to_json('attachment_tag', attachment_tag)

        return self.request(url, request_type='POST', body=True)

    def detach_volume(self, project_id: int,
                      region_id: int,
                      pk: str,
                      instance_id: str,
                      ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/detach"
        self.reset()
        self.add_application_header()
        self.add_to_json('instance_id', instance_id)

        return self.request(url, request_type='POST', body=True)

    def change_volume_type(self, project_id: int,
                           region_id: int,
                           pk: str,
                           volume_type: str,
                           ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/retype"
        self.reset()
        self.add_application_header()
        self.add_to_json('volume_type', volume_type)

        return self.request(url, request_type='POST', body=True)

    def revert_volume_to_last_snapshot(self, project_id: int,
                                       region_id: int,
                                       pk: str,
                                       ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/revert"
        self.reset()
        return self.request(url, request_type='POST')

    def extend_volume(self, project_id: int,
                      region_id: int,
                      pk: str,
                      size: int
                      ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/revert"
        self.reset()
        self.add_application_header()
        self.add_to_json('size', size)
        return self.request(url, request_type='POST', body=True)

    def list_volume_metadata(self, project_id: int,
                             region_id: int,
                             pk: str,
                             ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/metadata"
        self.reset()

        return self.request(url, request_type='GET')

    def create_update_volume_metadata(self, project_id: int,
                                      region_id: int,
                                      pk: str,
                                      key: str = None
                                      ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/metadata"
        self.reset()
        self.add_application_header()
        if key is not None:
            self.add_to_json('key', key)
            return self.request(url, request_type='POST', body=True)

        return self.request(url, request_type='POST')

    def replace_volume_metadata(self, project_id: int,
                                region_id: int,
                                pk: str,
                                key: str = None
                                ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/metadata"
        self.reset()
        self.add_application_header()

        if key is not None:
            self.add_to_json('key', key)
            return self.request(url, request_type='PUT', body=True)

        return self.request(url, request_type='PUT')

    def delete_volume_metadata(self, project_id: int,
                               region_id: int,
                               pk: str,
                               key: str = None
                               ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/metadata_item"
        self.reset()

        if key is not None:
            self.add_query_param('key', key)
            return self.request(url, request_type='DELETE', params=True)

        return self.request(url, request_type='DELETE')

    def get_volume_metadata_by_key(self, project_id: int,
                                   region_id: int,
                                   pk: str,
                                   key: str = None
                                   ) -> dict:
        url = f"{self.api_url}/{project_id}/{region_id}/{pk}/metadata_item"
        self.reset()

        if key is not None:
            self.add_query_param('key', key)
            return self.request(url, request_type='GET', params=True)

        return self.request(url, request_type='GET')
