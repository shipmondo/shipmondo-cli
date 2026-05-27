import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage pickup_points")

@app.command("list")
def list_cmd(
    carrier_code: str = typer.Option(None, "--carrier-code", help="Carrier code to be included in the filter."),
    country_code: str = typer.Option(None, "--country-code", help="Country code (ISO Alpha-2) to be included in the filter."),
    zipcode: str = typer.Option(None, "--zipcode", help="Zip code / Postal code."),
    city: str = typer.Option(None, "--city", help="Name of the city. It is recommended to include city with the request to increase the hit accuracy. "),
    address: str = typer.Option(None, "--address", help="Street address (contains street name and house number)"),
    param_id: str = typer.Option(None, "--id", help="The ID of the pickup point. Used to look up a specific service point for a carrier. When used, zip code is no longer required. Some carrier may not support this parameter."),
    quantity: int = typer.Option(None, "--quantity", help="Defines how many pickup points are being returned."),
    collect_points: bool = typer.Option(None, "--collect-points", help="Set as true to get collect points for products like GLS Click&Collect"),
    product_code: str = typer.Option(None, "--product-code", help="Used to, e.g., determine whether to return postfiliale (default) or packstations for DHL Parcel."),
    in_delivery: bool = typer.Option(None, "--in-delivery", help="Filter on whether or not the pickup point supports drop-off of parcels."),
    out_delivery: bool = typer.Option(None, "--out-delivery", help="Filter on whether or not the pickup point supports pickup of parcels."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List pickup points"""
    if help_json:
        print("""{
  "command": "shipmondo pickup_points list",
  "description": "List pickup points",
  "method": "GET",
  "endpoint": "/pickup_points",
  "parameters": {
    "carrier_code": {
      "cli_flag": "--carrier-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Carrier code to be included in the filter."
    },
    "country_code": {
      "cli_flag": "--country-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Country code (ISO Alpha-2) to be included in the filter."
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
      "description": "Name of the city. It is recommended to include city with the request to increase the hit accuracy. "
    },
    "address": {
      "cli_flag": "--address",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Street address (contains street name and house number)"
    },
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "The ID of the pickup point. Used to look up a specific service point for a carrier. When used, zip code is no longer required. Some carrier may not support this parameter."
    },
    "quantity": {
      "cli_flag": "--quantity",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "Defines how many pickup points are being returned."
    },
    "collect_points": {
      "cli_flag": "--collect-points",
      "location": "query",
      "type": "bool",
      "required": false,
      "description": "Set as true to get collect points for products like GLS Click&Collect"
    },
    "product_code": {
      "cli_flag": "--product-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Used to, e.g., determine whether to return postfiliale (default) or packstations for DHL Parcel."
    },
    "in_delivery": {
      "cli_flag": "--in-delivery",
      "location": "query",
      "type": "bool",
      "required": false,
      "description": "Filter on whether or not the pickup point supports drop-off of parcels."
    },
    "out_delivery": {
      "cli_flag": "--out-delivery",
      "location": "query",
      "type": "bool",
      "required": false,
      "description": "Filter on whether or not the pickup point supports pickup of parcels."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if carrier_code is None:
        print(json.dumps({"error": "Missing required Option '--carrier-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    if country_code is None:
        print(json.dumps({"error": "Missing required Option '--country-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    if zipcode is None:
        print(json.dumps({"error": "Missing required Option '--zipcode'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/pickup_points"
    url_params = {}
    if carrier_code is not None:
        url_params["carrier_code"] = carrier_code
    if country_code is not None:
        url_params["country_code"] = country_code
    if zipcode is not None:
        url_params["zipcode"] = zipcode
    if city is not None:
        url_params["city"] = city
    if address is not None:
        url_params["address"] = address
    if param_id is not None:
        url_params["id"] = param_id
    if quantity is not None:
        url_params["quantity"] = quantity
    if collect_points is not None:
        url_params["collect_points"] = collect_points
    if product_code is not None:
        url_params["product_code"] = product_code
    if in_delivery is not None:
        url_params["in_delivery"] = in_delivery
    if out_delivery is not None:
        url_params["out_delivery"] = out_delivery
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

