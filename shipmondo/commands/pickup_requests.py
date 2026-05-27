import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage pickup_requests")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID for the pickup request to be included in the filter"),
    carrier_code: str = typer.Option(None, "--carrier-code", help="Carrier code to be included in the filter."),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all pickup requests"""
    if help_json:
        print("""{
  "command": "shipmondo pickup_requests list",
  "description": "List all pickup requests",
  "method": "GET",
  "endpoint": "/pickup_requests",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID for the pickup request to be included in the filter"
    },
    "carrier_code": {
      "cli_flag": "--carrier-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Carrier code to be included in the filter."
    },
    "per_page": {
      "cli_flag": "--per-page",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "For pagination. Defines how many entries are returned per page."
    },
    "page": {
      "cli_flag": "--page",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "For pagination. Defines which page the results are fetched from."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/pickup_requests"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if carrier_code is not None:
        url_params["carrier_code"] = carrier_code
    if per_page is not None:
        url_params["per_page"] = per_page
    if page is not None:
        url_params["page"] = page
    if query:
        url_params.update(json.loads(query))
    data = client.request("GET", endpoint, params=url_params)

    if open_pdf:
        from shipmondo.pdf_viewer import extract_and_open_pdfs
        extract_and_open_pdfs(data)

    if json_output:
        typer.echo(json.dumps(data))
    else:
        typer.echo("Success. Run with --json to see data.")

@app.command("create")
def create_cmd(
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Create a pickup request"""
    if help_json:
        print("""{
  "command": "shipmondo pickup_requests create",
  "description": "Create a pickup request",
  "method": "POST",
  "endpoint": "/pickup_requests",
  "parameters": {},
  "payload_schema": {
    "required": [
      "carrier_code",
      "closed_by",
      "package_location",
      "pickup_address",
      "ready_by",
      "shipment_ids"
    ],
    "type": "object",
    "properties": {
      "carrier_code": {
        "description": "Carrier code for the carrier the pickup should be requested for.",
        "type": "string",
        "example": "ups",
        "enum": [
          "fed_ex",
          "ups",
          "dhl_express",
          "geodis",
          "dhl_freight_se",
          "post_nord",
          "bring"
        ]
      },
      "pickup_address": {
        "required": [
          "address1",
          "city",
          "company_name",
          "contact_name",
          "contact_phone",
          "country_code",
          "zipcode"
        ],
        "type": "object",
        "properties": {
          "company_name": {
            "type": "string",
            "example": "Min Virksomhed ApS"
          },
          "address1": {
            "type": "string",
            "example": "Strandvejen 6B"
          },
          "address2": {
            "type": "string",
            "description": "Second address line can be used for floor/room number, building name etc.",
            "example": null
          },
          "zipcode": {
            "type": "string",
            "example": "5240"
          },
          "city": {
            "type": "string",
            "example": "Odense N\u00d8"
          },
          "country_code": {
            "type": "string",
            "example": "DK"
          },
          "contact_name": {
            "description": "Name of the person that the carrier should contact about the pickup.",
            "type": "string",
            "example": "Hans Hansen"
          },
          "contact_phone": {
            "description": "Phone number of the person that the carrier should contact about the pickup.",
            "type": "string",
            "example": "70400407"
          }
        },
        "description": "Address where the shipments should be picked up from."
      },
      "package_location": {
        "description": "Where on the address the packages should be picked up.",
        "type": "string",
        "example": "At the front door"
      },
      "ready_by": {
        "description": "When shipments are ready for pickup. Pickup date is taken from the date given here.",
        "type": "string",
        "format": "date-time",
        "example": "2019-02-14T08:00:00.000Z"
      },
      "closed_by": {
        "description": "When shipments should be picked up by. The date part is ignored.",
        "type": "string",
        "format": "date-time",
        "example": "2019-02-14T15:00:00.000Z"
      },
      "shipment_ids": {
        "description": "IDs of the shipments you wish to be picked up.",
        "type": "array",
        "items": {
          "type": "integer",
          "example": 12515122
        }
      },
      "is_residential": {
        "description": "Only used for UPS. Whether the pickup address is residential or not.",
        "type": "boolean",
        "default": false
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/pickup_requests"
    url_params = {}
    if query:
        url_params.update(json.loads(query))
    parsed_data = json.loads(payload) if payload else None
    data = client.request("POST", endpoint, json=parsed_data, params=url_params)

    if open_pdf:
        from shipmondo.pdf_viewer import extract_and_open_pdfs
        extract_and_open_pdfs(data)

    if json_output:
        typer.echo(json.dumps(data))
    else:
        typer.echo("Success. Run with --json to see data.")

@app.command("get")
def get_cmd(
    param_id: int = typer.Argument(None, help="ID for the pickup request to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a pickup request"""
    if help_json:
        print("""{
  "command": "shipmondo pickup_requests get",
  "description": "Retrieve a pickup request",
  "method": "GET",
  "endpoint": "/pickup_requests/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the pickup request to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/pickup_requests/{param_id}"
    url_params = {}
    if query:
        url_params.update(json.loads(query))
    data = client.request("GET", endpoint, params=url_params)

    if open_pdf:
        from shipmondo.pdf_viewer import extract_and_open_pdfs
        extract_and_open_pdfs(data)

    if json_output:
        typer.echo(json.dumps(data))
    else:
        typer.echo("Success. Run with --json to see data.")

