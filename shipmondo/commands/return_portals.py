import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage return_portals")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID for the return portal."),
    active: bool = typer.Option(None, "--active", help="Filters for whether or not the return portal is active"),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all return portals"""
    if help_json:
        print("""{
  "command": "shipmondo return_portals list",
  "description": "List all return portals",
  "method": "GET",
  "endpoint": "/return_portals",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID for the return portal."
    },
    "active": {
      "cli_flag": "--active",
      "location": "query",
      "type": "bool",
      "required": false,
      "description": "Filters for whether or not the return portal is active"
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
    endpoint = f"/return_portals"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if active is not None:
        url_params["active"] = active
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

@app.command("get")
def get_cmd(
    param_id: int = typer.Argument(None, help="ID for the return portal to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a return portal"""
    if help_json:
        print("""{
  "command": "shipmondo return_portals get",
  "description": "Retrieve a return portal",
  "method": "GET",
  "endpoint": "/return_portals/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the return portal to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/return_portals/{param_id}"
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

@app.command("shipments")
def shipments_cmd(
    param_id: int = typer.Argument(None, help="ID for the return portal to be included in the filter"),
    order_id: str = typer.Option(None, "--order-id", help="Order ID for the shipments to be included in the filter"),
    package_number: str = typer.Option(None, "--package-number", help="Package number for the shipments that need to be considered for filter"),
    carrier_code: str = typer.Option(None, "--carrier-code", help="Carrier code to be included in the filter."),
    receiver_country: str = typer.Option(None, "--receiver-country", help="ISO3166-1 alpha-2 country code to be included in the filter."),
    created_at_min: str = typer.Option(None, "--created-at-min", help="'From' timestamp for the shipments to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "),
    created_at_max: str = typer.Option(None, "--created-at-max", help="'To' timestamp for the shipments to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all shipments for a return portal"""
    if help_json:
        print("""{
  "command": "shipmondo return_portals shipments",
  "description": "List all shipments for a return portal",
  "method": "GET",
  "endpoint": "/return_portals/{id}/shipments",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the return portal to be included in the filter"
    },
    "order_id": {
      "cli_flag": "--order-id",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Order ID for the shipments to be included in the filter"
    },
    "package_number": {
      "cli_flag": "--package-number",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Package number for the shipments that need to be considered for filter"
    },
    "carrier_code": {
      "cli_flag": "--carrier-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Carrier code to be included in the filter."
    },
    "receiver_country": {
      "cli_flag": "--receiver-country",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "ISO3166-1 alpha-2 country code to be included in the filter."
    },
    "created_at_min": {
      "cli_flag": "--created-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' timestamp for the shipments to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "
    },
    "created_at_max": {
      "cli_flag": "--created-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' timestamp for the shipments to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "
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

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/return_portals/{param_id}/shipments"
    url_params = {}
    if order_id is not None:
        url_params["order_id"] = order_id
    if package_number is not None:
        url_params["package_number"] = package_number
    if carrier_code is not None:
        url_params["carrier_code"] = carrier_code
    if receiver_country is not None:
        url_params["receiver_country"] = receiver_country
    if created_at_min is not None:
        url_params["created_at_min"] = created_at_min
    if created_at_max is not None:
        url_params["created_at_max"] = created_at_max
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

