import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage staff_accounts")

@app.command("list")
def list_cmd(
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all staff accounts"""
    if help_json:
        print("""{
  "command": "shipmondo staff_accounts list",
  "description": "List all staff accounts",
  "method": "GET",
  "endpoint": "/staff_accounts",
  "parameters": {},
  "payload_schema": null
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/staff_accounts"
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

@app.command("get")
def get_cmd(
    param_id: int = typer.Argument(None, help="ID for the staff_account to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a single staff account"""
    if help_json:
        print("""{
  "command": "shipmondo staff_accounts get",
  "description": "Retrieve a single staff account",
  "method": "GET",
  "endpoint": "/staff_accounts/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the staff_account to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/staff_accounts/{param_id}"
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

