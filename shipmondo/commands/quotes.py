import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage quotes")

@app.command("create")
def create_cmd(
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Create a shipment quote"""
    if help_json:
        print("""{
  "command": "shipmondo quotes create",
  "description": "Create a shipment quote",
  "method": "POST",
  "endpoint": "/quotes",
  "parameters": {},
  "payload_schema": {
    "required": [
      "product_code",
      "sender",
      "receiver",
      "parcels"
    ],
    "type": "object",
    "properties": {
      "product_code": {
        "type": "string",
        "description": "Product code referring to which product should be quoted for.",
        "example": "PDK_MH"
      },
      "service_codes": {
        "description": "Comma-separated string of service codes referring to which services should be quoted for.",
        "type": "string",
        "example": "EMAIL_NT,SMS_NT"
      },
      "sender": {
        "description": "Sender address for which the shipment is quoted.",
        "required": [
          "address1",
          "city",
          "country_code",
          "zipcode"
        ],
        "type": "object",
        "properties": {
          "address1": {
            "type": "string",
            "example": "Hvileh\u00f8jvej 25"
          },
          "address2": {
            "type": "string",
            "example": null,
            "description": "Second address line can be used for floor/room number, building name etc."
          },
          "zipcode": {
            "type": "string",
            "example": "5220"
          },
          "city": {
            "type": "string",
            "example": "Odense S\u00d8"
          },
          "country_code": {
            "type": "string",
            "example": "DK"
          }
        }
      },
      "receiver": {
        "description": "Receiver address for which the shipment is quoted.",
        "required": [
          "address1",
          "city",
          "country_code",
          "zipcode"
        ],
        "type": "object",
        "properties": {
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
        }
      },
      "parcels": {
        "type": "array",
        "items": {
          "type": "object",
          "required": [
            "weight"
          ],
          "properties": {
            "quantity": {
              "type": "integer",
              "description": "Number of parcels of this kind. Maximum quantity depends on the product.",
              "example": 1,
              "default": 1,
              "minimum": 1
            },
            "weight": {
              "type": "integer",
              "description": "Weight in grams per colli.",
              "example": 1000,
              "minimum": 1
            },
            "length": {
              "type": "integer",
              "description": "Length in cm",
              "example": 20,
              "minimum": 1
            },
            "width": {
              "type": "integer",
              "description": "Width in cm",
              "example": 10,
              "minimum": 1
            },
            "height": {
              "type": "integer",
              "description": "Height in cm",
              "example": 6,
              "minimum": 1
            },
            "volume": {
              "type": "number",
              "description": "Volume in cubic metres",
              "example": 0.012,
              "minimum": 0.001
            },
            "running_metre": {
              "type": "number",
              "description": "Running metre in metre",
              "example": 1.25,
              "minimum": 0.001
            },
            "description": {
              "description": "Describes the contents of the parcel.",
              "type": "string",
              "example": "Bike accessories"
            },
            "packaging": {
              "type": "string",
              "description": "Package type for the parcel. Must be a valid package type for the customer.",
              "example": "PL1"
            },
            "stackable": {
              "type": "boolean",
              "description": "Whether the parcel can be stacked.",
              "default": true,
              "example": true
            },
            "dangerous_goods": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "class": {
                    "type": "string",
                    "description": "ADR class of the dangerous goods.",
                    "example": "3"
                  },
                  "un_number": {
                    "type": "string",
                    "description": "UN number of the dangerous goods.",
                    "example": "1202"
                  },
                  "net_weight": {
                    "type": "integer",
                    "description": "Net weight in grams of the dangerous goods. Use either this or net_weight_kg.",
                    "example": 20100
                  },
                  "net_weight_kg": {
                    "type": "number",
                    "description": "Net weight in kilograms of the dangerous goods. Use either this or net_weight.",
                    "example": 20.1
                  },
                  "quantity": {
                    "type": "integer",
                    "description": "Number of pieces of this kind of dangerous goods.",
                    "example": 3
                  },
                  "packaging": {
                    "type": "string",
                    "description": "Packaging the dangerous goods are contained in.",
                    "example": "drums"
                  },
                  "description": {
                    "type": "string",
                    "description": "Description of the dangerous goods.",
                    "example": "DIESEL FUEL, < 62\u00b0C (640K)"
                  },
                  "tunnel_restriction_code": {
                    "type": "string",
                    "description": "Tunnel restriction code that applies to the dangerous goods.",
                    "example": "A"
                  },
                  "packing_group": {
                    "type": "string",
                    "description": "Packing group that applies to the dangerous goods.",
                    "example": "III"
                  },
                  "environmentally_hazardous": {
                    "type": "boolean",
                    "description": "Whether or not the dangerous goods are hazardous to the environment."
                  }
                }
              }
            },
            "declared_value": {
              "description": "Value of the goods in the parcel. Used in terms of insurance for certain carriers.",
              "type": "object",
              "nullable": true,
              "properties": {
                "amount": {
                  "type": "number",
                  "description": "Valued amount.",
                  "example": 1250
                },
                "currency_code": {
                  "type": "string",
                  "description": "Currency code for the currency of the amount.",
                  "example": "DKK"
                }
              }
            }
          }
        }
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/quotes"
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

@app.command("list")
def list_cmd(
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List available quotes for a shipment"""
    if help_json:
        print("""{
  "command": "shipmondo quotes list",
  "description": "List available quotes for a shipment",
  "method": "POST",
  "endpoint": "/quotes/list",
  "parameters": {},
  "payload_schema": {
    "type": "object",
    "required": [
      "sender",
      "receiver",
      "parcels"
    ],
    "properties": {
      "sender": {
        "description": "Sender address for which the shipment is quoted.",
        "required": [
          "address1",
          "city",
          "country_code",
          "zipcode"
        ],
        "type": "object",
        "properties": {
          "address1": {
            "type": "string",
            "example": "Hvileh\u00f8jvej 25"
          },
          "address2": {
            "type": "string",
            "example": null,
            "description": "Second address line can be used for floor/room number, building name etc."
          },
          "zipcode": {
            "type": "string",
            "example": "5220"
          },
          "city": {
            "type": "string",
            "example": "Odense S\u00d8"
          },
          "country_code": {
            "type": "string",
            "example": "DK"
          }
        }
      },
      "receiver": {
        "description": "Receiver address for which the shipment is quoted.",
        "required": [
          "address1",
          "city",
          "country_code",
          "zipcode"
        ],
        "type": "object",
        "properties": {
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
        }
      },
      "parcels": {
        "type": "array",
        "items": {
          "type": "object",
          "required": [
            "weight"
          ],
          "properties": {
            "quantity": {
              "type": "integer",
              "description": "Number of parcels of this kind. Maximum quantity depends on the product.",
              "example": 1,
              "default": 1,
              "minimum": 1
            },
            "weight": {
              "type": "integer",
              "description": "Weight in grams per colli.",
              "example": 1000,
              "minimum": 1
            },
            "length": {
              "type": "integer",
              "description": "Length in cm",
              "example": 20,
              "minimum": 1
            },
            "width": {
              "type": "integer",
              "description": "Width in cm",
              "example": 10,
              "minimum": 1
            },
            "height": {
              "type": "integer",
              "description": "Height in cm",
              "example": 6,
              "minimum": 1
            },
            "volume": {
              "type": "number",
              "description": "Volume in cubic metres",
              "example": 0.012,
              "minimum": 0.001
            },
            "running_metre": {
              "type": "number",
              "description": "Running metre in metre",
              "example": 1.25,
              "minimum": 0.001
            },
            "description": {
              "description": "Describes the contents of the parcel.",
              "type": "string",
              "example": "Bike accessories"
            },
            "packaging": {
              "type": "string",
              "description": "Package type for the parcel. Must be a valid package type for the customer.",
              "example": "PL1"
            },
            "stackable": {
              "type": "boolean",
              "description": "Whether the parcel can be stacked.",
              "default": true,
              "example": true
            },
            "dangerous_goods": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "class": {
                    "type": "string",
                    "description": "ADR class of the dangerous goods.",
                    "example": "3"
                  },
                  "un_number": {
                    "type": "string",
                    "description": "UN number of the dangerous goods.",
                    "example": "1202"
                  },
                  "net_weight": {
                    "type": "integer",
                    "description": "Net weight in grams of the dangerous goods. Use either this or net_weight_kg.",
                    "example": 20100
                  },
                  "net_weight_kg": {
                    "type": "number",
                    "description": "Net weight in kilograms of the dangerous goods. Use either this or net_weight.",
                    "example": 20.1
                  },
                  "quantity": {
                    "type": "integer",
                    "description": "Number of pieces of this kind of dangerous goods.",
                    "example": 3
                  },
                  "packaging": {
                    "type": "string",
                    "description": "Packaging the dangerous goods are contained in.",
                    "example": "drums"
                  },
                  "description": {
                    "type": "string",
                    "description": "Description of the dangerous goods.",
                    "example": "DIESEL FUEL, < 62\u00b0C (640K)"
                  },
                  "tunnel_restriction_code": {
                    "type": "string",
                    "description": "Tunnel restriction code that applies to the dangerous goods.",
                    "example": "A"
                  },
                  "packing_group": {
                    "type": "string",
                    "description": "Packing group that applies to the dangerous goods.",
                    "example": "III"
                  },
                  "environmentally_hazardous": {
                    "type": "boolean",
                    "description": "Whether or not the dangerous goods are hazardous to the environment."
                  }
                }
              }
            },
            "declared_value": {
              "description": "Value of the goods in the parcel. Used in terms of insurance for certain carriers.",
              "type": "object",
              "nullable": true,
              "properties": {
                "amount": {
                  "type": "number",
                  "description": "Valued amount.",
                  "example": 1250
                },
                "currency_code": {
                  "type": "string",
                  "description": "Currency code for the currency of the amount.",
                  "example": "DKK"
                }
              }
            }
          }
        }
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/quotes/list"
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

