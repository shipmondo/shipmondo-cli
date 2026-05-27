import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage service_point")

@app.command("service_points")
def service_points_cmd(
    product_code: str = typer.Option(None, "--product-code", help="Product code to find service points for."),
    country_code: str = typer.Option(None, "--country-code", help="Country code to find service points within."),
    zipcode: str = typer.Option(None, "--zipcode", help="Zip code / Postal code."),
    city: str = typer.Option(None, "--city", help="Name of the city. It is recommended to include city in the request to increase accuracy."),
    address: str = typer.Option(None, "--address", help="Street address (street name and house number). It is recommended to include the address in the request to increase accuracy.    If this parameter is not present or the address cannot be validated, the results will be based on the zipcode coordinates alone."),
    quantity: int = typer.Option(None, "--quantity", help="Defines the maximum amount of pickup points that will be returned."),
    service_point_types: str = typer.Option(None, "--service-point-types", help="Service point types. If not provided, will default to use all valid service point types for the given product."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Get service points based on product."""
    if help_json:
        print("""{
  "command": "shipmondo service_point service_points",
  "description": "Get service points based on product.",
  "method": "GET",
  "endpoint": "/service_point/service_points",
  "parameters": {
    "product_code": {
      "cli_flag": "--product-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Product code to find service points for."
    },
    "country_code": {
      "cli_flag": "--country-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Country code to find service points within."
    },
    "zipcode": {
      "cli_flag": "--zipcode",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Zip code / Postal code."
    },
    "city": {
      "cli_flag": "--city",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Name of the city. It is recommended to include city in the request to increase accuracy."
    },
    "address": {
      "cli_flag": "--address",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Street address (street name and house number). It is recommended to include the address in the request to increase accuracy.    If this parameter is not present or the address cannot be validated, the results will be based on the zipcode coordinates alone."
    },
    "quantity": {
      "cli_flag": "--quantity",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "Defines the maximum amount of pickup points that will be returned."
    },
    "service_point_types": {
      "cli_flag": "--service-point-types",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Service point types. If not provided, will default to use all valid service point types for the given product."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if product_code is None:
        print(json.dumps({"error": "Missing required Option '--product-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    if country_code is None:
        print(json.dumps({"error": "Missing required Option '--country-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    if zipcode is None:
        print(json.dumps({"error": "Missing required Option '--zipcode'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/service_point/service_points"
    url_params = {}
    if product_code is not None:
        url_params["product_code"] = product_code
    if country_code is not None:
        url_params["country_code"] = country_code
    if zipcode is not None:
        url_params["zipcode"] = zipcode
    if city is not None:
        url_params["city"] = city
    if address is not None:
        url_params["address"] = address
    if quantity is not None:
        url_params["quantity"] = quantity
    if service_point_types is not None:
        url_params["service_point_types"] = service_point_types
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

@app.command("service_point_types")
def service_point_types_cmd(
    product_code: str = typer.Option(None, "--product-code", help="The product code to find service point types for."),
    country_code: str = typer.Option(None, "--country-code", help="The country code to find service point types for."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Get valid service point types"""
    if help_json:
        print("""{
  "command": "shipmondo service_point service_point_types",
  "description": "Get valid service point types",
  "method": "GET",
  "endpoint": "/service_point/service_point_types",
  "parameters": {
    "product_code": {
      "cli_flag": "--product-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "The product code to find service point types for."
    },
    "country_code": {
      "cli_flag": "--country-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "The country code to find service point types for."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if product_code is None:
        print(json.dumps({"error": "Missing required Option '--product-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/service_point/service_point_types"
    url_params = {}
    if product_code is not None:
        url_params["product_code"] = product_code
    if country_code is not None:
        url_params["country_code"] = country_code
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

