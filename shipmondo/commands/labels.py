import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage labels")

@app.command("list")
def list_cmd(
    ids: str = typer.Option(None, "--ids", help="Comma-separated list of shipment IDs which labels should be retrieved for. Limited to 25 shipment IDs per request."),
    label_format: str = typer.Option(None, "--label-format", help="Which format the labels should be.  *10x19* is 10 cm x 19 cm  *compact* format returns the smallest label possible."),
    scale_by: str = typer.Option(None, "--scale-by", help="Scale down the labels by either width or height. Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl."),
    scale_size: float = typer.Option(None, "--scale-size", help="Desired scaled length in cm of dimension in 'scale_by'.If the length is higher or wider than the original labels, the labels will not be scaled.   Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve labels for multiple shipments"""
    if help_json:
        print("""{
  "command": "shipmondo labels list",
  "description": "Retrieve labels for multiple shipments",
  "method": "GET",
  "endpoint": "/labels",
  "parameters": {
    "ids": {
      "cli_flag": "--ids",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Comma-separated list of shipment IDs which labels should be retrieved for. Limited to 25 shipment IDs per request."
    },
    "label_format": {
      "cli_flag": "--label-format",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Which format the labels should be.  *10x19* is 10 cm x 19 cm  *compact* format returns the smallest label possible."
    },
    "scale_by": {
      "cli_flag": "--scale-by",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Scale down the labels by either width or height. Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl."
    },
    "scale_size": {
      "cli_flag": "--scale-size",
      "location": "query",
      "type": "float",
      "required": false,
      "description": "Desired scaled length in cm of dimension in 'scale_by'.If the length is higher or wider than the original labels, the labels will not be scaled.   Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if ids is None:
        print(json.dumps({"error": "Missing required Option '--ids'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/labels"
    url_params = {}
    if ids is not None:
        url_params["ids"] = ids
    if label_format is not None:
        url_params["label_format"] = label_format
    if scale_by is not None:
        url_params["scale_by"] = scale_by
    if scale_size is not None:
        url_params["scale_size"] = scale_size
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

