import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage shipping_modules")

@app.command("carriers")
def carriers_cmd(
    receiver_country_code: str = typer.Option(None, "--receiver-country-code", help="Will limit the results to only contain carriers that are valid for the given country."),
    own_agreement_only: bool = typer.Option(None, "--own-agreement-only", help="Will limit the results to only contain carriers for which your account has an active agreement."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Get carriers"""
    if help_json:
        print("""{
  "command": "shipmondo shipping_modules carriers",
  "description": "Get carriers",
  "method": "GET",
  "endpoint": "/shipping_modules/carriers",
  "parameters": {
    "receiver_country_code": {
      "cli_flag": "--receiver-country-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Will limit the results to only contain carriers that are valid for the given country."
    },
    "own_agreement_only": {
      "cli_flag": "--own-agreement-only",
      "location": "query",
      "type": "bool",
      "required": false,
      "description": "Will limit the results to only contain carriers for which your account has an active agreement."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipping_modules/carriers"
    url_params = {}
    if receiver_country_code is not None:
        url_params["receiver_country_code"] = receiver_country_code
    if own_agreement_only is not None:
        url_params["own_agreement_only"] = own_agreement_only
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

@app.command("products")
def products_cmd(
    carrier_code: str = typer.Option(None, "--carrier-code", help="The carrier code to find products for."),
    own_agreement_only: bool = typer.Option(None, "--own-agreement-only", help="Will limit the results to only contain products for which your account has an active agreement."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Get valid products"""
    if help_json:
        print("""{
  "command": "shipmondo shipping_modules products",
  "description": "Get valid products",
  "method": "GET",
  "endpoint": "/shipping_modules/products",
  "parameters": {
    "carrier_code": {
      "cli_flag": "--carrier-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "The carrier code to find products for."
    },
    "own_agreement_only": {
      "cli_flag": "--own-agreement-only",
      "location": "query",
      "type": "bool",
      "required": false,
      "description": "Will limit the results to only contain products for which your account has an active agreement."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if carrier_code is None:
        print(json.dumps({"error": "Missing required Option '--carrier-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipping_modules/products"
    url_params = {}
    if carrier_code is not None:
        url_params["carrier_code"] = carrier_code
    if own_agreement_only is not None:
        url_params["own_agreement_only"] = own_agreement_only
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

@app.command("shopify_shipping_methods")
def shopify_shipping_methods_cmd(
    param_id: int = typer.Argument(None, help="The ID of the Shopify shipping method."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Get Shopify shipping method"""
    if help_json:
        print("""{
  "command": "shipmondo shipping_modules shopify_shipping_methods",
  "description": "Get Shopify shipping method",
  "method": "GET",
  "endpoint": "/shipping_modules/shopify/shipping_methods/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "The ID of the Shopify shipping method."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipping_modules/shopify/shipping_methods/{param_id}"
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

