import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage setups")

@app.command("carriers")
def carriers_cmd(
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Request Carrier setup file"""
    if help_json:
        print("""{
  "command": "shipmondo setups carriers",
  "description": "Request Carrier setup file",
  "method": "GET",
  "endpoint": "/setups/carriers",
  "parameters": {},
  "payload_schema": null
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/setups/carriers"
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

