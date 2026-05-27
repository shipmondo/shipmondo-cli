import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage package_types")

@app.command("list")
def list_cmd(
    product_code: str = typer.Option(None, "--product-code", help="Code for the product to be included in the filter"),
    sender_country_code: str = typer.Option(None, "--sender-country-code", help="Country code of the sender country, format: ISO3133 alpha-2"),
    receiver_country_code: str = typer.Option(None, "--receiver-country-code", help="Country code of the receiver country, format: ISO3133 alpha-2"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all package types"""
    if help_json:
        print("""{
  "command": "shipmondo package_types list",
  "description": "List all package types",
  "method": "GET",
  "endpoint": "/package_types",
  "parameters": {
    "product_code": {
      "cli_flag": "--product-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Code for the product to be included in the filter"
    },
    "sender_country_code": {
      "cli_flag": "--sender-country-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Country code of the sender country, format: ISO3133 alpha-2"
    },
    "receiver_country_code": {
      "cli_flag": "--receiver-country-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Country code of the receiver country, format: ISO3133 alpha-2"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if product_code is None:
        print(json.dumps({"error": "Missing required Option '--product-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    if sender_country_code is None:
        print(json.dumps({"error": "Missing required Option '--sender-country-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    if receiver_country_code is None:
        print(json.dumps({"error": "Missing required Option '--receiver-country-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/package_types"
    url_params = {}
    if product_code is not None:
        url_params["product_code"] = product_code
    if sender_country_code is not None:
        url_params["sender_country_code"] = sender_country_code
    if receiver_country_code is not None:
        url_params["receiver_country_code"] = receiver_country_code
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

