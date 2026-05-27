import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage packing_slips")

@app.command("list")
def list_cmd(
    ids: str = typer.Option(None, "--ids", help="A list of sales order IDs that you want to fetch packing slips for. Examples 10075,10076,10077 "),
    output_format: str = typer.Option(None, "--output-format", help="Format for the packing slips. Available: a4_pdf, 10x19_pdf "),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve packing slips"""
    if help_json:
        print("""{
  "command": "shipmondo packing_slips list",
  "description": "Retrieve packing slips",
  "method": "GET",
  "endpoint": "/packing_slips",
  "parameters": {
    "ids": {
      "cli_flag": "--ids",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "A list of sales order IDs that you want to fetch packing slips for. Examples 10075,10076,10077 "
    },
    "output_format": {
      "cli_flag": "--output-format",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Format for the packing slips. Available: a4_pdf, 10x19_pdf "
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if ids is None:
        print(json.dumps({"error": "Missing required Option '--ids'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/packing_slips"
    url_params = {}
    if ids is not None:
        url_params["ids"] = ids
    if output_format is not None:
        url_params["output_format"] = output_format
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

