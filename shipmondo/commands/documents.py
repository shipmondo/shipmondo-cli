import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage documents")

@app.command("end_of_day")
def end_of_day_cmd(
    carrier_code: str = typer.Option(None, "--carrier-code", help="Carrier code of the carrier you want to retrieve the list for."),
    from_time: str = typer.Option(None, "--from-time", help="'From' timestamp for the end of day list. Examples: * 2018-06-19T11:00:00.305+02:00 * 2018-06-19 will be transformed into 2018-06-19T00:00:00.000+02:00 "),
    to_time: str = typer.Option(None, "--to-time", help="'To' timestamp for the end of day list. Examples: * 2018-06-20T11:00:00.305+02:00 * 2018-06-20 will be transformed into 2018-06-20T00:00:00.000+02:00 "),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve an End of Day list"""
    if help_json:
        print("""{
  "command": "shipmondo documents end_of_day",
  "description": "Retrieve an End of Day list",
  "method": "GET",
  "endpoint": "/documents/end_of_day",
  "parameters": {
    "carrier_code": {
      "cli_flag": "--carrier-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Carrier code of the carrier you want to retrieve the list for."
    },
    "from_time": {
      "cli_flag": "--from-time",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "'From' timestamp for the end of day list. Examples: * 2018-06-19T11:00:00.305+02:00 * 2018-06-19 will be transformed into 2018-06-19T00:00:00.000+02:00 "
    },
    "to_time": {
      "cli_flag": "--to-time",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "'To' timestamp for the end of day list. Examples: * 2018-06-20T11:00:00.305+02:00 * 2018-06-20 will be transformed into 2018-06-20T00:00:00.000+02:00 "
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if carrier_code is None:
        print(json.dumps({"error": "Missing required Option '--carrier-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    if from_time is None:
        print(json.dumps({"error": "Missing required Option '--from-time'"}), file=sys.stderr)
        raise typer.Exit(1)

    if to_time is None:
        print(json.dumps({"error": "Missing required Option '--to-time'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/documents/end_of_day"
    url_params = {}
    if carrier_code is not None:
        url_params["carrier_code"] = carrier_code
    if from_time is not None:
        url_params["from_time"] = from_time
    if to_time is not None:
        url_params["to_time"] = to_time
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

@app.command("waybill")
def waybill_cmd(
    carrier_code: str = typer.Option(None, "--carrier-code", help="Carrier code to be included in the filter"),
    bag_quantity: int = typer.Option(None, "--bag-quantity", help="Quantity of bags to be declared <br> <strong>Note:</strong> <ul> <li>Required for Deutsche Post, but is only used if an open order is being closed</li>"),
    container_quantity: int = typer.Option(None, "--container-quantity", help="Quantity of bags to be declared <br> <strong>Note:</strong> <ul> <li>If used with Deutsche Post it is just added to bag_quantity</li></ul>"),
    from_time: str = typer.Option(None, "--from-time", help="'From' timestamp for the waybill document. Examples: * 2018-06-19T11:00:00.305+02:00 * 2018-06-19 will be transformed into 2018-06-19T00:00:00.000+02:00 "),
    to_time: str = typer.Option(None, "--to-time", help="'To' timestamp for the waybill document. Examples: * 2018-06-20T11:00:00.305+02:00 * 2018-06-20 will be transformed into 2018-06-20T00:00:00.000+02:00 "),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a waybill"""
    if help_json:
        print("""{
  "command": "shipmondo documents waybill",
  "description": "Retrieve a waybill",
  "method": "GET",
  "endpoint": "/documents/waybill",
  "parameters": {
    "carrier_code": {
      "cli_flag": "--carrier-code",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "Carrier code to be included in the filter"
    },
    "bag_quantity": {
      "cli_flag": "--bag-quantity",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "Quantity of bags to be declared <br> <strong>Note:</strong> <ul> <li>Required for Deutsche Post, but is only used if an open order is being closed</li>"
    },
    "container_quantity": {
      "cli_flag": "--container-quantity",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "Quantity of bags to be declared <br> <strong>Note:</strong> <ul> <li>If used with Deutsche Post it is just added to bag_quantity</li></ul>"
    },
    "from_time": {
      "cli_flag": "--from-time",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "'From' timestamp for the waybill document. Examples: * 2018-06-19T11:00:00.305+02:00 * 2018-06-19 will be transformed into 2018-06-19T00:00:00.000+02:00 "
    },
    "to_time": {
      "cli_flag": "--to-time",
      "location": "query",
      "type": "str",
      "required": true,
      "description": "'To' timestamp for the waybill document. Examples: * 2018-06-20T11:00:00.305+02:00 * 2018-06-20 will be transformed into 2018-06-20T00:00:00.000+02:00 "
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if carrier_code is None:
        print(json.dumps({"error": "Missing required Option '--carrier-code'"}), file=sys.stderr)
        raise typer.Exit(1)

    if from_time is None:
        print(json.dumps({"error": "Missing required Option '--from-time'"}), file=sys.stderr)
        raise typer.Exit(1)

    if to_time is None:
        print(json.dumps({"error": "Missing required Option '--to-time'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/documents/waybill"
    url_params = {}
    if carrier_code is not None:
        url_params["carrier_code"] = carrier_code
    if bag_quantity is not None:
        url_params["bag_quantity"] = bag_quantity
    if container_quantity is not None:
        url_params["container_quantity"] = container_quantity
    if from_time is not None:
        url_params["from_time"] = from_time
    if to_time is not None:
        url_params["to_time"] = to_time
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

