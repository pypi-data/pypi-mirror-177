import objectrest


class Client:
    def __init__(self, api_key: str):
        self._gtfs_client = objectrest.RequestHandler(
            base_url="https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService",
        )
        self._legacy_client = objectrest.ApiTokenRequestHandler(
            base_url="http://developer.itsmarta.com",
            api_token=api_key,
            api_token_keyword="apiKey",
        )
        self._real_time_rail_client = objectrest.ApiTokenRequestHandler(
            base_url="https://developerservices.itsmarta.com:18096",
            api_token=api_key,
            api_token_keyword="apiKey",
        )
        self._lab_client = objectrest.ApiTokenRequestHandler(
            base_url="http://labs.itsmarta.com",
            api_token=api_key,
            api_token_keyword="api_key",
        )
