import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage webhooks")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID of the webhook object "),
    name: str = typer.Option(None, "--name", help="Name of the webhook "),
    active: bool = typer.Option(None, "--active", help="The current active status of the webhook "),
    created_at_min: str = typer.Option(None, "--created-at-min", help="'From' timestamp for the webhooks to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "),
    created_at_max: str = typer.Option(None, "--created-at-max", help="'To' timestamp for the webhooks to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "),
    updated_at_min: str = typer.Option(None, "--updated-at-min", help="'From' value of 'updated' timestamp for the webhooks to be included in the filter. Examples: * 2018-06-19T11:00:03.305+02:00 * 2018-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "),
    updated_at_max: str = typer.Option(None, "--updated-at-max", help="'To' value of 'updated' timestamp for the webhooks to be included in the filter. Examples: * 2018-06-29T11:00:03.305+02:00 * 2018-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all webhooks"""
    if help_json:
        print("""{
  "command": "shipmondo webhooks list",
  "description": "List all webhooks",
  "method": "GET",
  "endpoint": "/webhooks",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID of the webhook object "
    },
    "name": {
      "cli_flag": "--name",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Name of the webhook "
    },
    "active": {
      "cli_flag": "--active",
      "location": "query",
      "type": "bool",
      "required": false,
      "description": "The current active status of the webhook "
    },
    "created_at_min": {
      "cli_flag": "--created-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' timestamp for the webhooks to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "
    },
    "created_at_max": {
      "cli_flag": "--created-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' timestamp for the webhooks to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "
    },
    "updated_at_min": {
      "cli_flag": "--updated-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' value of 'updated' timestamp for the webhooks to be included in the filter. Examples: * 2018-06-19T11:00:03.305+02:00 * 2018-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "
    },
    "updated_at_max": {
      "cli_flag": "--updated-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' value of 'updated' timestamp for the webhooks to be included in the filter. Examples: * 2018-06-29T11:00:03.305+02:00 * 2018-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "
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
    endpoint = f"/webhooks"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if name is not None:
        url_params["name"] = name
    if active is not None:
        url_params["active"] = active
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
    """Create a webhook"""
    if help_json:
        print("""{
  "command": "shipmondo webhooks create",
  "description": "Create a webhook",
  "method": "POST",
  "endpoint": "/webhooks",
  "parameters": {},
  "payload_schema": {
    "type": "object",
    "required": [
      "name",
      "endpoint",
      "key",
      "action",
      "resource_name"
    ],
    "properties": {
      "name": {
        "type": "string",
        "example": "Example Name",
        "description": "User-specified name of the webhook."
      },
      "endpoint": {
        "type": "string",
        "example": "https://example.com/webhook",
        "description": "Endpoint the webhook sends request to."
      },
      "key": {
        "type": "string",
        "example": "example_key_123",
        "description": "Encryption key that should encrypt and decrypt the webhook message with JWT."
      },
      "action": {
        "type": "string",
        "example": "create",
        "description": "The action that webhook is hooked to.",
        "enum": [
          "create",
          "cancel",
          "status_update",
          "create_fulfillment",
          "create_shipment",
          "payment_captured",
          "payment_voided",
          "delete",
          "latest",
          "delivered"
        ]
      },
      "resource_name": {
        "type": "string",
        "example": "Shipments",
        "description": "The name of the resource that webhook is hooked to.",
        "enum": [
          "Shipments",
          "Orders",
          "Shipment Monitor"
        ]
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/webhooks"
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
    param_id: int = typer.Argument(None, help="ID for the webhook to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a webhook"""
    if help_json:
        print("""{
  "command": "shipmondo webhooks get",
  "description": "Retrieve a webhook",
  "method": "GET",
  "endpoint": "/webhooks/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the webhook to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/webhooks/{param_id}"
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
    param_id: int = typer.Argument(None, help="ID of the webhook that is to be updated"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Update a webhook"""
    if help_json:
        print("""{
  "command": "shipmondo webhooks update",
  "description": "Update a webhook",
  "method": "PUT",
  "endpoint": "/webhooks/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the webhook that is to be updated"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/webhooks/{param_id}"
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

@app.command("delete")
def delete_cmd(
    param_id: int = typer.Argument(None, help="ID of the webhook that is to be deleted"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Delete a webhook"""
    if help_json:
        print("""{
  "command": "shipmondo webhooks delete",
  "description": "Delete a webhook",
  "method": "DELETE",
  "endpoint": "/webhooks/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the webhook that is to be deleted"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/webhooks/{param_id}"
    url_params = {}
    if query:
        url_params.update(json.loads(query))
    data = client.request("DELETE", endpoint, params=url_params)

    if open_pdf:
        from shipmondo.pdf_viewer import extract_and_open_pdfs
        extract_and_open_pdfs(data)

    if json_output:
        typer.echo(json.dumps(data))
    else:
        typer.echo("Success. Run with --json to see data.")

