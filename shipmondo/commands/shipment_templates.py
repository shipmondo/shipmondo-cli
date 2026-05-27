import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage shipment_templates")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID for the shipment template to be included in the filter"),
    sender_country: str = typer.Option(None, "--sender-country", help="Country code (ISO Alpha-2) to be included in the filter."),
    receiver_country: str = typer.Option(None, "--receiver-country", help="Country code (ISO Alpha-2) to be included in the filter."),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all shipment templates"""
    if help_json:
        print("""{
  "command": "shipmondo shipment_templates list",
  "description": "List all shipment templates",
  "method": "GET",
  "endpoint": "/shipment_templates",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID for the shipment template to be included in the filter"
    },
    "sender_country": {
      "cli_flag": "--sender-country",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Country code (ISO Alpha-2) to be included in the filter."
    },
    "receiver_country": {
      "cli_flag": "--receiver-country",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Country code (ISO Alpha-2) to be included in the filter."
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
    endpoint = f"/shipment_templates"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if sender_country is not None:
        url_params["sender_country"] = sender_country
    if receiver_country is not None:
        url_params["receiver_country"] = receiver_country
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
    param_id: int = typer.Argument(None, help="ID for the shipment template to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a shipment template"""
    if help_json:
        print("""{
  "command": "shipmondo shipment_templates get",
  "description": "Retrieve a shipment template",
  "method": "GET",
  "endpoint": "/shipment_templates/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment template to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipment_templates/{param_id}"
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

