from typing import Union

from GCoreAPI.GCore_Base import Base


class Useractions(Base):
    def __init__(self, token: str, project_id: int):
        super().__init__(token, project_id)
        self.api_url = f"{self.BASE_URL}/user_actions"

    def subscribe_to_log(self,
                         auth_header_value: str,
                         auth_header_name: str,
                         url: str
                         ) -> dict:
        responce_url = f"{self.api_url}/subscribe"
        self.reset()
        self.add_application_header()
        self.add_to_json('auth_header_value', auth_header_value)
        self.add_to_json('auth_header_name', auth_header_name)
        self.add_to_json('url', url)

        return self.request(responce_url, request_type='POST', body=True)

    def get_client_subscriptions_list(self) -> dict:
        url = f"{self.api_url}/subscriptions_list"
        return self.request(url, request_type='GET')

    def get_client_subscriptions_list_AMQP(self) -> dict:
        url = f"{self.api_url}/amqp_subscriptions_list"
        return self.request(url, request_type='GET')

    def unsubscribe_to_log(self) -> dict:
        url = f"{self.api_url}/unsubscribe"
        return self.request(url, request_type='POST')

    def subscribe_to_log_over_AMQP(self,
                                   connection_string: str,
                                   exchange: Union[str, None] = None,
                                   receive_child_client_events: bool = False,
                                   routing_key: Union[str, None] = None
                                   ) -> dict:

        responce_url = f"{self.api_url}/subscribe_amqp"
        self.reset()
        self.add_application_header()
        self.add_to_json('connection_string', connection_string)
        if exchange is not None:
            self.add_to_json('exchange', exchange)
        if receive_child_client_events is not None:
            self.add_to_json('receive_child_client_events', receive_child_client_events)
        if routing_key is not None:
            self.add_to_json('routing_key', routing_key)

        return self.request(responce_url, request_type='POST', body=True)

    def unsubscribe_to_log_AMQP(self) -> dict:
        url = f"{self.api_url}/unsubscribe_amqp"
        return self.request(url, request_type='POST')
