import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage carriers")

@app.command("list")
def list_cmd(
    sender_country_code: str = typer.Option(None, "--sender-country-code", help="Sender country code to be included in the filter."),
    receiver_country_code: str = typer.Option(None, "--receiver-country-code", help="Receiver country code to be included in the filter."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List available carriers"""
    if help_json:
        print("""{
  "command": "shipmondo carriers list",
  "description": "List available carriers",
  "method": "GET",
  "endpoint": "/carriers",
  "parameters": {
    "sender_country_code": {
      "cli_flag": "--sender-country-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Sender country code to be included in the filter."
    },
    "receiver_country_code": {
      "cli_flag": "--receiver-country-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Receiver country code to be included in the filter."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if receiver_country_code is None:
        print(json.dumps({"error": "Missing required Option '--receiver-country-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/carriers"
    url_params = {}
    if sender_country_code is not None:
        url_params["sender_country_code"] = sender_country_code
    if receiver_country_code is not None:
        url_params["receiver_country_code"] = receiver_country_code
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

