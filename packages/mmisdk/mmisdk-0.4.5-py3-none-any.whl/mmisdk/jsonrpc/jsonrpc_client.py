
from typing import List
from typing import Union

import requests

from mmisdk.common.abstract_client import AbstractClient
from mmisdk.jsonrpc.jsonrpc_create_transaction_metadata import JsonRpcCreateTransactionMetadata
from mmisdk.jsonrpc.jsonrpc_create_transaction_params import JsonRpcCreateTransactionParams
from mmisdk.jsonrpc.jsonrpc_get_transaction_result import JsonRpcGetTransactionResult
from mmisdk.jsonrpc.jsonrpc_request import JsonRpcRequest
from mmisdk.jsonrpc.jsonrpc_response import JsonRpcResponse
from mmisdk.jsonrpc.jsonrpc_transaction_id import JsonRpcTransactionId


class JsonRpcClient(AbstractClient):

    def __init__(self, api_url, token, refresh_token_url):
        self.api_url = api_url
        self.token = token
        self.refresh_token_url = refresh_token_url

    def __create_access_token(self):
        """Internal method that creates an access token, necessary to authenticate other calls against the JSON-RPC custodian's API.

        Returns:
            The access token as a string.
        """
        payload = {"grant_type": "refresh_token",
                   "refresh_token": self.token}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(self.refresh_token_url,  data=payload, headers=headers)
        response_json = response.json()
        if 'access_token' not in response_json:
            raise requests.HTTPError(
                f"Couldn't create the access token, {response_json}")

        access_token = response_json["access_token"]
        return access_token

    def __get_headers(self):
        """Internal method that creates the HTTP header to use for the calls against JSON-RPC custodian's API. It includes an authorization header that uses the access token.

        Returns:
            The HTTP header as a dictionary.
        """
        access_token = self.__create_access_token()
        return {
            "Authorization": 'Bearer ' + access_token
        }

    def get_transaction_by_id(self, tx_id: str) -> JsonRpcGetTransactionResult:
        url = f"{self.api_url}/v1/json-rpc"
        headers = self.__get_headers()
        payload = JsonRpcRequest[List[str]](
            id=1,  # TODO
            method="custodian_getTransactionById",
            params=[tx_id]
        )
        payload_json = payload.dict()

        response = requests.post(url, json=payload_json, headers=headers)
        response_json = response.json()
        response_json_parsed = JsonRpcResponse[JsonRpcGetTransactionResult](**response_json)
        error = response_json_parsed.error
        result = response_json_parsed.result

        if error is not None:
            raise requests.HTTPError(
                f"Couldn't get the transaction. Request failed with code {error.code}: {error.message}")

        if result is None:
            raise requests.HTTPError(
                f"Coudn't find a transaction with passed id {tx_id}")

        return result

    def create_transaction(self, tx_params: JsonRpcCreateTransactionParams, tx_metadata: JsonRpcCreateTransactionMetadata) -> JsonRpcTransactionId:
        url = f"{self.api_url}/v1/json-rpc"
        headers = self.__get_headers()
        payload = JsonRpcRequest[List[Union[JsonRpcCreateTransactionParams, JsonRpcCreateTransactionMetadata]]](
            id=1,  # TODO
            method="custodian_createTransaction",
            params=[tx_params, tx_metadata],
        )

        # Exclude None fields, otherwise the JSON-RPC API raises Validation error
        payload_json = payload.dict(exclude_none=True, by_alias=True)

        response = requests.post(url, json=payload_json, headers=headers)
        response_json = response.json()
        response_json_parsed = JsonRpcResponse[JsonRpcTransactionId](**response_json)
        error = response_json_parsed.error

        if error is not None:
            raise requests.HTTPError(
                f"Couldn't create the transaction. Th request failed: {error}")

        # Parse and validate response
        return response_json["result"]
