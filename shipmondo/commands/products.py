import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage products")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID for the product to be included in the filter."),
    product_code: str = typer.Option(None, "--product-code", help="Code for the product to be included in the filter."),
    sender_country_code: str = typer.Option(None, "--sender-country-code", help="Country code (ISO Alpha-2) of the sender country to be included in the filter."),
    receiver_country_code: str = typer.Option(None, "--receiver-country-code", help="Country code (ISO Alpha-2) of the receiver country to be included in the filter."),
    carrier_code: str = typer.Option(None, "--carrier-code", help="Carrier code to be included in the filter."),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all products"""
    if help_json:
        print("""{
  "command": "shipmondo products list",
  "description": "List all products",
  "method": "GET",
  "endpoint": "/products",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID for the product to be included in the filter."
    },
    "product_code": {
      "cli_flag": "--product-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Code for the product to be included in the filter."
    },
    "sender_country_code": {
      "cli_flag": "--sender-country-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Country code (ISO Alpha-2) of the sender country to be included in the filter."
    },
    "receiver_country_code": {
      "cli_flag": "--receiver-country-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Country code (ISO Alpha-2) of the receiver country to be included in the filter."
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
    endpoint = f"/products"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if product_code is not None:
        url_params["product_code"] = product_code
    if sender_country_code is not None:
        url_params["sender_country_code"] = sender_country_code
    if receiver_country_code is not None:
        url_params["receiver_country_code"] = receiver_country_code
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

