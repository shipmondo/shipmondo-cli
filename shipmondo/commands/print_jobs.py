import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage print_jobs")

@app.command("create")
def create_cmd(
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Create a print job"""
    if help_json:
        print("""{
  "command": "shipmondo print_jobs create",
  "description": "Create a print job",
  "method": "POST",
  "endpoint": "/print_jobs",
  "parameters": {},
  "payload_schema": {
    "type": "object",
    "required": [
      "document_id",
      "document_type",
      "host_name",
      "printer_name",
      "label_format"
    ],
    "properties": {
      "document_id": {
        "type": "integer",
        "example": 11460,
        "description": "Identifier for the provided document_type."
      },
      "document_type": {
        "type": "string",
        "example": "shipment",
        "description": "Type of document that should be printed.",
        "enum": [
          "shipment",
          "sales_order",
          "fulfillment",
          "proforma",
          "waybill"
        ]
      },
      "host_name": {
        "type": "string",
        "example": "WAREHOUSE-PC-01",
        "description": "The name of the computer/host to print at."
      },
      "printer_name": {
        "type": "string",
        "example": "GK420D",
        "description": "The name of the printer that should be printed on."
      },
      "label_format": {
        "type": "string",
        "example": "10x19_zpl",
        "enum": [
          "a4_pdf",
          "10x19_pdf",
          "10x19_zpl",
          "compact_pdf",
          "compact_zpl"
        ],
        "description": "The given format of the print job. Label_formats: compact_pdf and compact_zpl, is only compatible with document_type: shipment."
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/print_jobs"
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

@app.command("batch")
def batch_cmd(
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Create a print job batch"""
    if help_json:
        print("""{
  "command": "shipmondo print_jobs batch",
  "description": "Create a print job batch",
  "method": "POST",
  "endpoint": "/print_jobs/batch",
  "parameters": {},
  "payload_schema": {
    "type": "object",
    "required": [
      "print_jobs",
      "host_name"
    ],
    "properties": {
      "host_name": {
        "type": "string",
        "example": "WAREHOUSE-PC-01",
        "description": "The name of the computer/host to print at."
      },
      "print_jobs": {
        "type": "array",
        "description": "A list of print jobs to be printed in the specified order.",
        "items": {
          "type": "object",
          "required": [
            "document_id",
            "document_type",
            "printer_name",
            "label_format"
          ],
          "properties": {
            "document_id": {
              "type": "integer",
              "example": 11460,
              "description": "Identifier for the provided document_type."
            },
            "document_type": {
              "type": "string",
              "example": "shipment",
              "description": "Type of document that should be printed.",
              "enum": [
                "shipment",
                "sales_order",
                "fulfillment",
                "proforma",
                "waybill"
              ]
            },
            "printer_name": {
              "type": "string",
              "example": "GK420D",
              "description": "The name of the printer that should be printed on."
            },
            "label_format": {
              "type": "string",
              "example": "10x19_zpl",
              "enum": [
                "a4_pdf",
                "10x19_pdf",
                "10x19_zpl",
                "compact_pdf",
                "compact_zpl"
              ],
              "description": "The given format of the print job. Label_formats: compact_pdf and compact_zpl, is only compatible with document_type: shipment."
            }
          }
        }
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/print_jobs/batch"
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

