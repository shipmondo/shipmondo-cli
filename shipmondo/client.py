import os
import requests
import sys
import json

BASE_URL = "https://app.shipmondo.com/api/public/v3"

class ShipmondoClient:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.api_user = os.getenv("SHIPMONDO_API_USER")
        self.api_key = os.getenv("SHIPMONDO_API_KEY")

        if not self.api_user or not self.api_key:
            print('{"error": "Missing authentication. Set SHIPMONDO_API_USER and SHIPMONDO_API_KEY."}', file=sys.stderr)
            sys.exit(1)
            
        self.session = requests.Session()
        self.session.auth = (self.api_user, self.api_key)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "shipmondo-cli"
        })

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{BASE_URL}{endpoint}"
        
        if self.debug:
            print("\n====== DEBUG: OUTGOING REQUEST ======", file=sys.stderr)
            print(f"{method.upper()} {url}", file=sys.stderr)
            print(f"Headers: {json.dumps(dict(self.session.headers))}", file=sys.stderr)
            if kwargs.get("params"):
                print(f"Query Params: {json.dumps(kwargs['params'])}", file=sys.stderr)
            if kwargs.get("json"):
                print(f"JSON Payload: {json.dumps(kwargs['json'], indent=2)}", file=sys.stderr)
            print("=====================================\n", file=sys.stderr)

        try:
            response = self.session.request(method, url, **kwargs)
            
            if self.debug:
                print("====== DEBUG: INCOMING RESPONSE ======", file=sys.stderr)
                print(f"Status Code: {response.status_code}", file=sys.stderr)
                print(f"Headers: {json.dumps(dict(response.headers), indent=2)}", file=sys.stderr)
                try:
                    print(f"Body: {json.dumps(response.json(), indent=2)}", file=sys.stderr)
                except ValueError:
                    print(f"Body: {response.text}", file=sys.stderr)
                print("======================================\n", file=sys.stderr)

            response.raise_for_status()
            return response.json() if response.text else {}
            
        except requests.exceptions.RequestException as e:
            api_error = str(e)
            status_code = None
            
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
                
                if self.debug and not (200 <= status_code < 300):
                    print("====== DEBUG: ERROR RESPONSE ======", file=sys.stderr)
                    print(f"Status Code: {status_code}", file=sys.stderr)
                    print(f"Body: {e.response.text}", file=sys.stderr)
                    print("===================================\n", file=sys.stderr)

                try:
                    json_data = e.response.json()
                    if isinstance(json_data, dict):
                        api_error = json_data.get("error", e.response.text or f"HTTP Error {status_code}")
                    else:
                        api_error = e.response.text or f"HTTP Error {status_code}"
                except ValueError:
                    api_error = e.response.text or f"HTTP Error {status_code}"
            
            error_payload = {
                "error": "API Request Failed",
                "status_code": status_code,
                "details": api_error
            }
            print(json.dumps(error_payload), file=sys.stderr)
            sys.exit(1)