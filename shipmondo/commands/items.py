import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage items")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID of the item that needs to be considered for filter"),
    sku: str = typer.Option(None, "--sku", help="SKU of the item that needs to be considered for filter"),
    name: str = typer.Option(None, "--name", help="Name of the item that needs to be considered for filter"),
    barcode: str = typer.Option(None, "--barcode", help="The barcode value of the item that needs to be considered for filter"),
    created_at_min: str = typer.Option(None, "--created-at-min", help="'From' timestamp for the items to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "),
    created_at_max: str = typer.Option(None, "--created-at-max", help="'To' timestamp for the items to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "),
    updated_at_min: str = typer.Option(None, "--updated-at-min", help="'From' value of 'updated' timestamp for the items to be included in the filter. Examples: * 2018-06-19T11:00:03.305+02:00 * 2018-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "),
    updated_at_max: str = typer.Option(None, "--updated-at-max", help="'To' value of 'updated' timestamp for the items to be included in the filter. Examples: * 2018-06-29T11:00:03.305+02:00 * 2018-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all items"""
    if help_json:
        print("""{
  "command": "shipmondo items list",
  "description": "List all items",
  "method": "GET",
  "endpoint": "/items",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID of the item that needs to be considered for filter"
    },
    "sku": {
      "cli_flag": "--sku",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "SKU of the item that needs to be considered for filter"
    },
    "name": {
      "cli_flag": "--name",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Name of the item that needs to be considered for filter"
    },
    "barcode": {
      "cli_flag": "--barcode",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "The barcode value of the item that needs to be considered for filter"
    },
    "created_at_min": {
      "cli_flag": "--created-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' timestamp for the items to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "
    },
    "created_at_max": {
      "cli_flag": "--created-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' timestamp for the items to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "
    },
    "updated_at_min": {
      "cli_flag": "--updated-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' value of 'updated' timestamp for the items to be included in the filter. Examples: * 2018-06-19T11:00:03.305+02:00 * 2018-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "
    },
    "updated_at_max": {
      "cli_flag": "--updated-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' value of 'updated' timestamp for the items to be included in the filter. Examples: * 2018-06-29T11:00:03.305+02:00 * 2018-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "
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
    endpoint = f"/items"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if sku is not None:
        url_params["sku"] = sku
    if name is not None:
        url_params["name"] = name
    if barcode is not None:
        url_params["barcode"] = barcode
    if created_at_min is not None:
        url_params["created_at_min"] = created_at_min
    if created_at_max is not None:
        url_params["created_at_max"] = created_at_max
    if updated_at_min is not None:
        url_params["updated_at_min"] = updated_at_min
    if updated_at_max is not None:
        url_params["updated_at_max"] = updated_at_max
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
    """Create an item"""
    if help_json:
        print("""{
  "command": "shipmondo items create",
  "description": "Create an item",
  "method": "POST",
  "endpoint": "/items",
  "parameters": {},
  "payload_schema": {
    "type": "object",
    "required": [
      "sku",
      "name"
    ],
    "properties": {
      "sku": {
        "type": "string",
        "example": "EX-123",
        "description": "SKU (stock keeping unit). Must be unique for every item, including variants."
      },
      "name": {
        "type": "string",
        "example": "T-Shirt",
        "description": "Name of the item."
      },
      "variant_code": {
        "type": "string",
        "example": "Large",
        "description": "Variant code of the item."
      },
      "barcode": {
        "type": "string",
        "example": "1234567891011",
        "description": "Barcode of the item, which is used when scanning item for pick. Will be displayed as a code 128 barcode"
      },
      "bin": {
        "type": "string",
        "example": "123-a",
        "description": "The bin/location where the item is located in the warehouse."
      },
      "weight": {
        "type": "integer",
        "example": 1000,
        "description": "Weight of the item in grams."
      },
      "image_url": {
        "type": "string",
        "example": "https://example.com/image.jpg",
        "description": "Image URL of the item that appears on the order or when picking. Will only be displayed if the URL is HTTPS."
      },
      "country_code_of_origin": {
        "type": "string",
        "example": "DK",
        "description": "ISO 3166-1 alpha-2 country code of origin."
      },
      "currency_code": {
        "type": "string",
        "example": "DKK",
        "description": "ISO 4217 currency code."
      },
      "customs_commodity_code": {
        "type": "string",
        "example": "123456",
        "description": "Global tariff code for the item. Used when creating shipments that require customs declaration."
      },
      "customs_description": {
        "type": "string",
        "example": "Example contents",
        "description": "Customs description for the item. Used when creating shipments that require customs declaration."
      },
      "shop": {
        "type": "string",
        "example": "API",
        "description": "Origin shop of the item."
      },
      "virtual": {
        "type": "boolean",
        "default": false,
        "description": "Describes if the item is a virtual item."
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/items"
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
    param_id: int = typer.Argument(None, help="ID for the item to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve an item"""
    if help_json:
        print("""{
  "command": "shipmondo items get",
  "description": "Retrieve an item",
  "method": "GET",
  "endpoint": "/items/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the item to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/items/{param_id}"
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

@app.command("update")
def update_cmd(
    param_id: int = typer.Argument(None, help="ID for the item that is to be updated"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Update an item"""
    if help_json:
        print("""{
  "command": "shipmondo items update",
  "description": "Update an item",
  "method": "PUT",
  "endpoint": "/items/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the item that is to be updated"
    }
  },
  "payload_schema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "example": "T-Shirt",
        "description": "Name of the item."
      },
      "variant_code": {
        "type": "string",
        "example": "Large",
        "description": "Variant code of the item."
      },
      "barcode": {
        "type": "string",
        "example": "1234567891011",
        "description": "Barcode of the item. Used when scanning item for pick."
      },
      "bin": {
        "type": "string",
        "example": "123-a",
        "description": "The bin/location where the item is located in the warehouse."
      },
      "weight": {
        "type": "integer",
        "example": 1000,
        "description": "Weight of the item in grams."
      },
      "image_url": {
        "type": "string",
        "example": "https://example.com/image.jpg",
        "description": "Image URL of the item that appears on the order or when picking. Will only be displayed if the URL is HTTPS."
      },
      "country_code_of_origin": {
        "type": "string",
        "example": "DK",
        "description": "ISO 3166-1 alpha-2 country code of origin."
      },
      "currency_code": {
        "type": "string",
        "example": "DKK",
        "description": "ISO 4217 currency code."
      },
      "customs_commodity_code": {
        "type": "string",
        "example": "123456",
        "description": "Global tariff code for the item. Used when creating shipments that require customs declaration."
      },
      "customs_description": {
        "type": "string",
        "example": "Example contents",
        "description": "Customs description for the item. Used when creating shipments that require customs declaration."
      },
      "virtual": {
        "type": "boolean",
        "default": false,
        "description": "Describes if the item is a virtual item."
      }
    }
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/items/{param_id}"
    url_params = {}
    if query:
        url_params.update(json.loads(query))
    parsed_data = json.loads(payload) if payload else None
    data = client.request("PUT", endpoint, json=parsed_data, params=url_params)

    if open_pdf:
        from shipmondo.pdf_viewer import extract_and_open_pdfs
        extract_and_open_pdfs(data)

    if json_output:
        typer.echo(json.dumps(data))
    else:
        typer.echo("Success. Run with --json to see data.")

