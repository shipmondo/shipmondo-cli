import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage waybills")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID for the bulk waybill to be included in the filter"),
    reference: str = typer.Option(None, "--reference", help="Reference for the bulk waybill that need to be considered for filter"),
    carrier_code: str = typer.Option(None, "--carrier-code", help="Carrier code to be included in the filter  Examples: bring "),
    status: str = typer.Option(None, "--status", help="Status to be included in the filter"),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all bulk waybills"""
    if help_json:
        print("""{
  "command": "shipmondo waybills list",
  "description": "List all bulk waybills",
  "method": "GET",
  "endpoint": "/waybills",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID for the bulk waybill to be included in the filter"
    },
    "reference": {
      "cli_flag": "--reference",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Reference for the bulk waybill that need to be considered for filter"
    },
    "carrier_code": {
      "cli_flag": "--carrier-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Carrier code to be included in the filter  Examples: bring "
    },
    "status": {
      "cli_flag": "--status",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Status to be included in the filter"
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
    endpoint = f"/waybills"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if reference is not None:
        url_params["reference"] = reference
    if carrier_code is not None:
        url_params["carrier_code"] = carrier_code
    if status is not None:
        url_params["status"] = status
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
    """Create a bulk waybill"""
    if help_json:
        print("""{
  "command": "shipmondo waybills create",
  "description": "Create a bulk waybill",
  "method": "POST",
  "endpoint": "/waybills",
  "parameters": {},
  "payload_schema": {
    "required": [
      "carrier_code",
      "packages",
      "receiver",
      "sender"
    ],
    "type": "object",
    "properties": {
      "carrier_code": {
        "type": "string",
        "enum": [
          "bring",
          "pdk"
        ],
        "example": "bring"
      },
      "customer_number": {
        "type": "string",
        "description": "Used if you have more than one agreement for the selected carrier. If not given, it defaults to the first agreement found."
      },
      "status": {
        "type": "string",
        "enum": [
          "open",
          "closed"
        ],
        "default": "closed"
      },
      "label_format": {
        "type": "string",
        "enum": [
          "10x19_pdf",
          "a4_pdf"
        ],
        "description": "Format of routing labels. Defaults to default label format of the user. Note that this is only used if status is set to \"closed\""
      },
      "sender": {
        "required": [
          "address1",
          "city",
          "country_code",
          "name",
          "zipcode"
        ],
        "type": "object",
        "properties": {
          "name": {
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
          }
        },
        "description": "Required"
      },
      "receiver": {
        "required": [
          "address1",
          "city",
          "country_code",
          "name",
          "zipcode"
        ],
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "example": "Lene Hansen"
          },
          "address1": {
            "type": "string",
            "example": "Skibhusvej 52"
          },
          "address2": {
            "type": "string",
            "description": "Second address line can be used for floor/room number, building name etc.",
            "example": null
          },
          "zipcode": {
            "type": "string",
            "example": "5000"
          },
          "city": {
            "type": "string",
            "example": "Odense C"
          },
          "country_code": {
            "type": "string",
            "example": "DK"
          }
        },
        "description": "Required"
      },
      "loading": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "example": "Lene Hansen"
          },
          "address1": {
            "type": "string",
            "example": "Skibhusvej 52"
          },
          "address2": {
            "type": "string",
            "description": "Second address line can be used for floor/room number, building name etc.",
            "example": null
          },
          "zipcode": {
            "type": "string",
            "example": "5000"
          },
          "city": {
            "type": "string",
            "example": "Odense C"
          },
          "country_code": {
            "type": "string",
            "example": "DK"
          },
          "date": {
            "type": "string",
            "format": "date-time",
            "example": "2019-01-30T13:54:29.000Z"
          }
        },
        "description": "Optional, except date if carrier is Bring. If no fields are included sender is copied"
      },
      "delivery": {
        "type": "object",
        "properties": {
          "name": {
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
          }
        },
        "description": "Optional. If all fields are not included receiver is copied to\nthese fields"
      },
      "packages": {
        "type": "array",
        "description": "Required if status is set to \"closed\"",
        "items": {
          "type": "object",
          "properties": {
            "product_code": {
              "description": "Product code of the parcels that the pallet contains. If pallets contain multiple products, the codes must be comma-separated, e.g., \"PDK_M,PDK_BP\".",
              "type": "string",
              "enum": [
                "BRI_PPB",
                "BRI_BPB",
                "PDK_BP",
                "PDK_M",
                "PDK_TB",
                "PDK_PL"
              ],
              "example": "BRI_PPB"
            },
            "package_type": {
              "description": "Type of pallet. Determines whether it is a pallet for individual parcel shipments or the shipment is the pallet itself.",
              "type": "string",
              "enum": [
                "PARCEL",
                "PALLET"
              ],
              "example": "PARCEL"
            },
            "amount": {
              "type": "integer",
              "example": 3,
              "description": "PARCEL: The amount of parcels in the pallet. PALLET: x amount of pallets. This is be split into x routing labels."
            },
            "weight": {
              "type": "integer",
              "description": "Total weight of the pallet/parcels in grams",
              "example": 1000
            }
          }
        }
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/waybills"
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
    param_id: int = typer.Argument(None, help="ID for the bulk waybill to be included in the filter"),
    label_format: str = typer.Option(None, "--label-format", help="Format of routing labels. Defaults to default label format of the user."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a bulk waybill"""
    if help_json:
        print("""{
  "command": "shipmondo waybills get",
  "description": "Retrieve a bulk waybill",
  "method": "GET",
  "endpoint": "/waybills/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the bulk waybill to be included in the filter"
    },
    "label_format": {
      "cli_flag": "--label-format",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Format of routing labels. Defaults to default label format of the user."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/waybills/{param_id}"
    url_params = {}
    if label_format is not None:
        url_params["label_format"] = label_format
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

@app.command("put_close")
def put_close_cmd(
    param_id: int = typer.Argument(None, help="ID for the bulk waybill to be included in the filter"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Close an open bulk waybill"""
    if help_json:
        print("""{
  "command": "shipmondo waybills put_close",
  "description": "Close an open bulk waybill",
  "method": "PUT",
  "endpoint": "/waybills/{id}/close",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the bulk waybill to be included in the filter"
    }
  },
  "payload_schema": {
    "required": [],
    "type": "object",
    "properties": {
      "label_format": {
        "type": "string",
        "enum": [
          "10x19_pdf",
          "a4_pdf"
        ],
        "description": "Format of routing labels. Defaults to default label format of the user."
      },
      "packages": {
        "description": "Required unless the waybill uses load carriers.",
        "required": [
          "product_code",
          "package_type",
          "amount",
          "weight"
        ],
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "product_code": {
              "description": "Product code of the parcels that the pallet contains. If pallets contain multiple products, the codes must be comma-separated, e.g., \"PDK_M,PDK_BP\".",
              "type": "string",
              "enum": [
                "BRI_PPB",
                "BRI_BPB",
                "PDK_BP",
                "PDK_M",
                "PDK_TB",
                "PDK_PL"
              ],
              "example": "BRI_PPB"
            },
            "package_type": {
              "description": "Type of pallet. Determines whether it is a pallet for individual parcel shipments or the shipment is the pallet itself.",
              "type": "string",
              "enum": [
                "PARCEL",
                "PALLET"
              ],
              "example": "PARCEL"
            },
            "amount": {
              "type": "integer",
              "example": 3,
              "description": "PARCEL: The amount of parcels in the pallet. PALLET: x amount of pallets. This is be split into x routing labels."
            },
            "weight": {
              "type": "integer",
              "description": "Total weight of the pallet/parcels in grams",
              "example": 1000
            }
          }
        }
      }
    }
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/waybills/{param_id}/close"
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

@app.command("load_carriers")
def load_carriers_cmd(
    waybill_id: int = typer.Argument(None, help="ID of the bulk waybill to add a load carrier to."),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Creates and adds a new load carrier to the bulk waybill"""
    if help_json:
        print("""{
  "command": "shipmondo waybills load_carriers",
  "description": "Creates and adds a new load carrier to the bulk waybill",
  "method": "POST",
  "endpoint": "/waybills/{waybill_id}/load_carriers",
  "parameters": {
    "waybill_id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the bulk waybill to add a load carrier to."
    }
  },
  "payload_schema": {
    "required": [
      "package_type"
    ],
    "type": "object",
    "properties": {
      "package_type": {
        "type": "string",
        "enum": [
          "PALLET",
          "H_PALLET",
          "Q_PALLET",
          "S_PALLET",
          "PARCEL",
          "CAGE",
          "BOX",
          "ENVELOPE"
        ],
        "example": "PALLET",
        "description": "Type of load carrier. Not all values are valid for all carriers."
      }
    }
  }
}""")
        raise typer.Exit()

    if waybill_id is None:
        print(json.dumps({"error": "Missing required Argument 'waybill_id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/waybills/{waybill_id}/load_carriers"
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

@app.command("load_carriers")
def load_carriers_cmd(
    waybill_id: int = typer.Argument(None, help="ID of the bulk waybill to fetch all load carriers for."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all load carriers"""
    if help_json:
        print("""{
  "command": "shipmondo waybills load_carriers",
  "description": "List all load carriers",
  "method": "GET",
  "endpoint": "/waybills/{waybill_id}/load_carriers",
  "parameters": {
    "waybill_id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the bulk waybill to fetch all load carriers for."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if waybill_id is None:
        print(json.dumps({"error": "Missing required Argument 'waybill_id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/waybills/{waybill_id}/load_carriers"
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

@app.command("load_carriers")
def load_carriers_cmd(
    waybill_id: int = typer.Argument(None, help="ID of the bulk waybill to find a specific load carrier for."),
    param_id: int = typer.Argument(None, help="ID of the load carrier to be retrieved."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a load carrier"""
    if help_json:
        print("""{
  "command": "shipmondo waybills load_carriers",
  "description": "Retrieve a load carrier",
  "method": "GET",
  "endpoint": "/waybills/{waybill_id}/load_carriers/{id}",
  "parameters": {
    "waybill_id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the bulk waybill to find a specific load carrier for."
    },
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the load carrier to be retrieved."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if waybill_id is None:
        print(json.dumps({"error": "Missing required Argument 'waybill_id'"}), file=sys.stderr)
        raise typer.Exit(1)

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/waybills/{waybill_id}/load_carriers/{param_id}"
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

