import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage shipment_drafts")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID for the draft shipment to be included in the filter"),
    created_at_min: str = typer.Option(None, "--created-at-min", help="'From' timestamp for the Shipment drafts to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "),
    created_at_max: str = typer.Option(None, "--created-at-max", help="'To' timestamp for the Shipment drafts to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all shipment drafts"""
    if help_json:
        print("""{
  "command": "shipmondo shipment_drafts list",
  "description": "List all shipment drafts",
  "method": "GET",
  "endpoint": "/shipment_drafts",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID for the draft shipment to be included in the filter"
    },
    "created_at_min": {
      "cli_flag": "--created-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' timestamp for the Shipment drafts to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "
    },
    "created_at_max": {
      "cli_flag": "--created-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' timestamp for the Shipment drafts to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "
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
    endpoint = f"/shipment_drafts"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if created_at_min is not None:
        url_params["created_at_min"] = created_at_min
    if created_at_max is not None:
        url_params["created_at_max"] = created_at_max
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
    """Create a shipment draft"""
    if help_json:
        print("""{
  "command": "shipmondo shipment_drafts create",
  "description": "Create a shipment draft",
  "method": "POST",
  "endpoint": "/shipment_drafts",
  "parameters": {},
  "payload_schema": {
    "allOf": [
      {
        "allOf": [
          {
            "type": "object",
            "properties": {
              "own_agreement": {
                "type": "boolean",
                "description": "Whether the shipment is created using an own agreement with the carrier.",
                "nullable": true
              },
              "customer_number": {
                "type": "string",
                "description": "Customer number used for own agreements with the carrier.",
                "example": "56212",
                "nullable": true
              },
              "carrier_code": {
                "type": "string",
                "description": "Carrier code for the shipment draft.",
                "example": "gls",
                "nullable": true
              },
              "product_code": {
                "type": "string",
                "description": "Product code for the shipment draft.",
                "example": "GLSDK_SD"
              },
              "service_codes": {
                "type": "array",
                "description": "Array of service codes applied to the shipment.",
                "items": {
                  "type": "string",
                  "example": "SMS_NT"
                },
                "example": [
                  "SMS_NT",
                  "EMAIL_NT"
                ]
              },
              "terms_of_trade": {
                "type": "string",
                "description": "Incoterms for the shipment.",
                "example": "DDP",
                "nullable": true
              },
              "reference": {
                "type": "string",
                "description": "Reference for the shipment. Shown on labels and in tracking information.",
                "example": "Order #1234",
                "nullable": true
              },
              "additional_reference": {
                "type": "string",
                "description": "Additional reference for the shipment. Shown on labels and in tracking information.",
                "example": "Customer #5678",
                "nullable": true
              },
              "contents": {
                "type": "string",
                "description": "Description of the contents of the shipment.",
                "example": "Books and clothing",
                "nullable": true
              },
              "origin_shipment_id": {
                "type": "integer",
                "description": "ID of the original shipment if this shipment is a return shipment.",
                "example": 12515120,
                "nullable": true
              },
              "parties": {
                "type": "array",
                "description": "Array of parties associated with the shipment.",
                "items": {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "enum": [
                        "sender",
                        "receiver",
                        "pickup",
                        "importer",
                        "freight_payer",
                        "service_point",
                        "return"
                      ],
                      "description": "Type of party. Parties with `sender` and `receiver` are required for all shipments.",
                      "example": "sender"
                    },
                    "name": {
                      "type": "string",
                      "description": "Name of the party. For companies, this should be the company name.",
                      "example": "Min Virksomhed ApS"
                    },
                    "attention": {
                      "type": "string",
                      "description": "Attention field can be used for the name of a specific person at the address.",
                      "example": "Lene Hansen"
                    },
                    "address1": {
                      "type": "string",
                      "description": "First address line. This should be the street name and number.",
                      "example": "Hvileh\u00f8jvej 25"
                    },
                    "address2": {
                      "type": "string",
                      "description": "Second address line can be used for floor/room number, building name etc.",
                      "example": null
                    },
                    "postal_code": {
                      "type": "string",
                      "description": "Postal code of the address.",
                      "example": "5220"
                    },
                    "city": {
                      "type": "string",
                      "description": "City of the address.",
                      "example": "Odense S\u00d8"
                    },
                    "country_code": {
                      "type": "string",
                      "description": "Country code of the address in ISO3166 alpha-2 format.",
                      "example": "DK"
                    },
                    "email": {
                      "type": "string",
                      "description": "E-mail address of the party.",
                      "example": "info@minvirksomhed.dk"
                    },
                    "phone": {
                      "type": "string",
                      "description": "Phone number of the party.",
                      "example": "+4570400407"
                    },
                    "attributes": {
                      "type": "array",
                      "description": "Attributes for the party. Used for additional information about the party.",
                      "items": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string",
                            "description": "Name of the attribute.",
                            "example": "vat_no"
                          },
                          "value": {
                            "type": "string",
                            "description": "Value of the attribute.",
                            "example": "DK36399066"
                          }
                        },
                        "required": [
                          "name",
                          "value"
                        ]
                      }
                    }
                  },
                  "required": [
                    "type"
                  ]
                }
              },
              "pickup_details": {
                "type": "object",
                "properties": {
                  "date": {
                    "type": "string",
                    "format": "date",
                    "example": "2021-10-13",
                    "description": "Scheduled date."
                  },
                  "from": {
                    "type": "string",
                    "format": "time",
                    "example": "08:00:00",
                    "description": "Scheduled earliest time. Format HH:MM:SS."
                  },
                  "to": {
                    "type": "string",
                    "format": "time",
                    "example": "16:00:00",
                    "description": "Scheduled latest time. Format HH:MM:SS."
                  },
                  "instruction": {
                    "type": "string",
                    "example": "Goods are placed at gate 21",
                    "description": "Instruction to the carrier. Only applicable for products which supports instructions."
                  }
                }
              },
              "delivery_details": {
                "type": "object",
                "properties": {
                  "date": {
                    "type": "string",
                    "format": "date",
                    "example": "2021-10-13",
                    "description": "Scheduled date."
                  },
                  "from": {
                    "type": "string",
                    "format": "time",
                    "example": "08:00:00",
                    "description": "Scheduled earliest time. Format HH:MM:SS."
                  },
                  "to": {
                    "type": "string",
                    "format": "time",
                    "example": "16:00:00",
                    "description": "Scheduled latest time. Format HH:MM:SS."
                  },
                  "instruction": {
                    "type": "string",
                    "example": "Goods are placed at gate 21",
                    "description": "Instruction to the carrier. Only applicable for products which supports instructions."
                  }
                }
              },
              "parcels": {
                "type": "array",
                "items": {
                  "allOf": [
                    {
                      "type": "object",
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
                        "loading_meter": {
                          "type": "number",
                          "description": "Loading meter in meters",
                          "example": 1.25,
                          "minimum": 0.001
                        },
                        "description": {
                          "description": "Describes the contents of the parcel.",
                          "type": "string",
                          "example": "Bike accessories"
                        },
                        "package_type": {
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
                        "internal_reference": {
                          "type": "string",
                          "description": "A reference for internal use to track parcels, not sent to the carrier.",
                          "example": "parcel-1",
                          "nullable": true
                        },
                        "dangerous_goods": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "hazard_class": {
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
                  ]
                },
                "minItems": 1
              },
              "pallet_exchange": {
                "type": "object",
                "properties": {
                  "pallets1": {
                    "type": "integer",
                    "description": "The number of full pallets to exchange",
                    "example": 0
                  },
                  "pallets2": {
                    "type": "integer",
                    "description": "The number of half pallets to exchange",
                    "example": 0
                  },
                  "pallets4": {
                    "type": "integer",
                    "description": "The number of quarter pallets to exchange",
                    "example": 0
                  }
                }
              },
              "customs": {
                "type": "object",
                "properties": {
                  "attributes": {
                    "type": "array",
                    "description": "List of dynamic attributes for the customs information.",
                    "items": {
                      "type": "object",
                      "properties": {
                        "name": {
                          "type": "string",
                          "description": "Name of the attribute.",
                          "example": "vat_no"
                        },
                        "value": {
                          "type": "string",
                          "description": "Value of the attribute.",
                          "example": "DK36399066"
                        }
                      },
                      "required": [
                        "name",
                        "value"
                      ]
                    }
                  },
                  "export_reason": {
                    "type": "string",
                    "description": "Reason for exporting the goods.",
                    "default": "other",
                    "example": "other",
                    "enum": [
                      "sale_of_goods",
                      "gift",
                      "documents",
                      "commercial_samples",
                      "returned_goods",
                      "other"
                    ],
                    "nullable": true
                  },
                  "freight_cost": {
                    "type": "number",
                    "nullable": true,
                    "description": "Cost of freight."
                  },
                  "insurance_cost": {
                    "type": "number",
                    "nullable": true,
                    "description": "Cost of insurance."
                  },
                  "currency_code": {
                    "type": "string",
                    "nullable": true,
                    "description": "Currency code used for customs values."
                  },
                  "goods": {
                    "type": "array",
                    "description": "List of commodities included in the customs declaration.",
                    "items": {
                      "type": "object",
                      "properties": {
                        "quantity": {
                          "type": "integer",
                          "description": "Quantity of the good in the shipment.",
                          "example": 2
                        },
                        "country_code": {
                          "type": "string",
                          "description": "Country code of origin of the good.",
                          "example": "DK"
                        },
                        "description": {
                          "type": "string",
                          "description": "Description of the good.",
                          "example": "Cotton t-shirt"
                        },
                        "commodity_code": {
                          "type": "string",
                          "description": "Commodity code (tariff/HS code) of the good.",
                          "example": "6109100010"
                        },
                        "unit_value": {
                          "type": "number",
                          "description": "Value of the good per unit.",
                          "example": 122.5
                        },
                        "unit_weight": {
                          "type": "integer",
                          "description": "Weight in grams of the good per unit.",
                          "example": 110
                        },
                        "attributes": {
                          "type": "array",
                          "minItems": 0,
                          "description": "Attributes for the commodity good. Used for additional information.",
                          "items": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string",
                                "description": "Name of the attribute.",
                                "example": "vat_no"
                              },
                              "value": {
                                "type": "string",
                                "description": "Value of the attribute.",
                                "example": "DK36399066"
                              }
                            },
                            "required": [
                              "name",
                              "value"
                            ]
                          }
                        }
                      }
                    }
                  }
                }
              },
              "cod": {
                "description": "Used for COD (cash on delivery) shipments, when booking with service code COD",
                "type": "object",
                "properties": {
                  "amount": {
                    "type": "number",
                    "description": "The amount to be collected.",
                    "example": 326
                  },
                  "currency_code": {
                    "type": "string",
                    "description": "Currency code of the amount.",
                    "example": "NOK"
                  },
                  "account_number": {
                    "type": "string",
                    "description": "The account number which should receive the amount that has been collected.",
                    "example": "123456789"
                  }
                }
              },
              "carrier_insurance": {
                "description": "Object for indicating carrier insurance on the shipment. Only usable for specific carriers and when an insurance service code is provided.",
                "type": "object",
                "properties": {
                  "amount": {
                    "type": "number",
                    "description": "Amount in the given currency that should be insured for the shipment.",
                    "example": 1000,
                    "nullable": true
                  },
                  "currency_code": {
                    "type": "string",
                    "description": "Indicates the currency code for the insured value.",
                    "example": "DKK",
                    "nullable": true
                  }
                }
              },
              "attributes": {
                "type": "array",
                "description": "List of dynamic attributes for the shipment draft.",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "description": "Name of the attribute.",
                      "example": "vat_no"
                    },
                    "value": {
                      "type": "string",
                      "description": "Value of the attribute.",
                      "example": "DK36399066"
                    }
                  },
                  "required": [
                    "name",
                    "value"
                  ]
                }
              }
            }
          },
          {
            "type": "object",
            "properties": {
              "service_point_id": {
                "type": "string",
                "description": "ID of the service point the shipment should be sent to. Note that the full service point can also be provided in the `parties` array with `type` set to `service_point`.",
                "example": "96271"
              }
            }
          }
        ]
      },
      {
        "type": "object",
        "required": [
          "product_code",
          "parties"
        ]
      }
    ]
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipment_drafts"
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
    param_id: int = typer.Argument(None, help="ID for the shipment draft to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a shipment draft"""
    if help_json:
        print("""{
  "command": "shipmondo shipment_drafts get",
  "description": "Retrieve a shipment draft",
  "method": "GET",
  "endpoint": "/shipment_drafts/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment draft to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipment_drafts/{param_id}"
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
    param_id: int = typer.Argument(None, help="ID for the draft shipment that need to be updated"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Update a shipment draft"""
    if help_json:
        print("""{
  "command": "shipmondo shipment_drafts update",
  "description": "Update a shipment draft",
  "method": "PUT",
  "endpoint": "/shipment_drafts/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the draft shipment that need to be updated"
    }
  },
  "payload_schema": {
    "allOf": [
      {
        "type": "object",
        "properties": {
          "own_agreement": {
            "type": "boolean",
            "description": "Whether the shipment is created using an own agreement with the carrier.",
            "nullable": true
          },
          "customer_number": {
            "type": "string",
            "description": "Customer number used for own agreements with the carrier.",
            "example": "56212",
            "nullable": true
          },
          "carrier_code": {
            "type": "string",
            "description": "Carrier code for the shipment draft.",
            "example": "gls",
            "nullable": true
          },
          "product_code": {
            "type": "string",
            "description": "Product code for the shipment draft.",
            "example": "GLSDK_SD"
          },
          "service_codes": {
            "type": "array",
            "description": "Array of service codes applied to the shipment.",
            "items": {
              "type": "string",
              "example": "SMS_NT"
            },
            "example": [
              "SMS_NT",
              "EMAIL_NT"
            ]
          },
          "terms_of_trade": {
            "type": "string",
            "description": "Incoterms for the shipment.",
            "example": "DDP",
            "nullable": true
          },
          "reference": {
            "type": "string",
            "description": "Reference for the shipment. Shown on labels and in tracking information.",
            "example": "Order #1234",
            "nullable": true
          },
          "additional_reference": {
            "type": "string",
            "description": "Additional reference for the shipment. Shown on labels and in tracking information.",
            "example": "Customer #5678",
            "nullable": true
          },
          "contents": {
            "type": "string",
            "description": "Description of the contents of the shipment.",
            "example": "Books and clothing",
            "nullable": true
          },
          "origin_shipment_id": {
            "type": "integer",
            "description": "ID of the original shipment if this shipment is a return shipment.",
            "example": 12515120,
            "nullable": true
          },
          "parties": {
            "type": "array",
            "description": "Array of parties associated with the shipment.",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "sender",
                    "receiver",
                    "pickup",
                    "importer",
                    "freight_payer",
                    "service_point",
                    "return"
                  ],
                  "description": "Type of party. Parties with `sender` and `receiver` are required for all shipments.",
                  "example": "sender"
                },
                "name": {
                  "type": "string",
                  "description": "Name of the party. For companies, this should be the company name.",
                  "example": "Min Virksomhed ApS"
                },
                "attention": {
                  "type": "string",
                  "description": "Attention field can be used for the name of a specific person at the address.",
                  "example": "Lene Hansen"
                },
                "address1": {
                  "type": "string",
                  "description": "First address line. This should be the street name and number.",
                  "example": "Hvileh\u00f8jvej 25"
                },
                "address2": {
                  "type": "string",
                  "description": "Second address line can be used for floor/room number, building name etc.",
                  "example": null
                },
                "postal_code": {
                  "type": "string",
                  "description": "Postal code of the address.",
                  "example": "5220"
                },
                "city": {
                  "type": "string",
                  "description": "City of the address.",
                  "example": "Odense S\u00d8"
                },
                "country_code": {
                  "type": "string",
                  "description": "Country code of the address in ISO3166 alpha-2 format.",
                  "example": "DK"
                },
                "email": {
                  "type": "string",
                  "description": "E-mail address of the party.",
                  "example": "info@minvirksomhed.dk"
                },
                "phone": {
                  "type": "string",
                  "description": "Phone number of the party.",
                  "example": "+4570400407"
                },
                "attributes": {
                  "type": "array",
                  "description": "Attributes for the party. Used for additional information about the party.",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "description": "Name of the attribute.",
                        "example": "vat_no"
                      },
                      "value": {
                        "type": "string",
                        "description": "Value of the attribute.",
                        "example": "DK36399066"
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ]
                  }
                }
              },
              "required": [
                "type"
              ]
            }
          },
          "pickup_details": {
            "type": "object",
            "properties": {
              "date": {
                "type": "string",
                "format": "date",
                "example": "2021-10-13",
                "description": "Scheduled date."
              },
              "from": {
                "type": "string",
                "format": "time",
                "example": "08:00:00",
                "description": "Scheduled earliest time. Format HH:MM:SS."
              },
              "to": {
                "type": "string",
                "format": "time",
                "example": "16:00:00",
                "description": "Scheduled latest time. Format HH:MM:SS."
              },
              "instruction": {
                "type": "string",
                "example": "Goods are placed at gate 21",
                "description": "Instruction to the carrier. Only applicable for products which supports instructions."
              }
            }
          },
          "delivery_details": {
            "type": "object",
            "properties": {
              "date": {
                "type": "string",
                "format": "date",
                "example": "2021-10-13",
                "description": "Scheduled date."
              },
              "from": {
                "type": "string",
                "format": "time",
                "example": "08:00:00",
                "description": "Scheduled earliest time. Format HH:MM:SS."
              },
              "to": {
                "type": "string",
                "format": "time",
                "example": "16:00:00",
                "description": "Scheduled latest time. Format HH:MM:SS."
              },
              "instruction": {
                "type": "string",
                "example": "Goods are placed at gate 21",
                "description": "Instruction to the carrier. Only applicable for products which supports instructions."
              }
            }
          },
          "parcels": {
            "type": "array",
            "items": {
              "allOf": [
                {
                  "type": "object",
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
                    "loading_meter": {
                      "type": "number",
                      "description": "Loading meter in meters",
                      "example": 1.25,
                      "minimum": 0.001
                    },
                    "description": {
                      "description": "Describes the contents of the parcel.",
                      "type": "string",
                      "example": "Bike accessories"
                    },
                    "package_type": {
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
                    "internal_reference": {
                      "type": "string",
                      "description": "A reference for internal use to track parcels, not sent to the carrier.",
                      "example": "parcel-1",
                      "nullable": true
                    },
                    "dangerous_goods": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "hazard_class": {
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
              ]
            },
            "minItems": 1
          },
          "pallet_exchange": {
            "type": "object",
            "properties": {
              "pallets1": {
                "type": "integer",
                "description": "The number of full pallets to exchange",
                "example": 0
              },
              "pallets2": {
                "type": "integer",
                "description": "The number of half pallets to exchange",
                "example": 0
              },
              "pallets4": {
                "type": "integer",
                "description": "The number of quarter pallets to exchange",
                "example": 0
              }
            }
          },
          "customs": {
            "type": "object",
            "properties": {
              "attributes": {
                "type": "array",
                "description": "List of dynamic attributes for the customs information.",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "description": "Name of the attribute.",
                      "example": "vat_no"
                    },
                    "value": {
                      "type": "string",
                      "description": "Value of the attribute.",
                      "example": "DK36399066"
                    }
                  },
                  "required": [
                    "name",
                    "value"
                  ]
                }
              },
              "export_reason": {
                "type": "string",
                "description": "Reason for exporting the goods.",
                "default": "other",
                "example": "other",
                "enum": [
                  "sale_of_goods",
                  "gift",
                  "documents",
                  "commercial_samples",
                  "returned_goods",
                  "other"
                ],
                "nullable": true
              },
              "freight_cost": {
                "type": "number",
                "nullable": true,
                "description": "Cost of freight."
              },
              "insurance_cost": {
                "type": "number",
                "nullable": true,
                "description": "Cost of insurance."
              },
              "currency_code": {
                "type": "string",
                "nullable": true,
                "description": "Currency code used for customs values."
              },
              "goods": {
                "type": "array",
                "description": "List of commodities included in the customs declaration.",
                "items": {
                  "type": "object",
                  "properties": {
                    "quantity": {
                      "type": "integer",
                      "description": "Quantity of the good in the shipment.",
                      "example": 2
                    },
                    "country_code": {
                      "type": "string",
                      "description": "Country code of origin of the good.",
                      "example": "DK"
                    },
                    "description": {
                      "type": "string",
                      "description": "Description of the good.",
                      "example": "Cotton t-shirt"
                    },
                    "commodity_code": {
                      "type": "string",
                      "description": "Commodity code (tariff/HS code) of the good.",
                      "example": "6109100010"
                    },
                    "unit_value": {
                      "type": "number",
                      "description": "Value of the good per unit.",
                      "example": 122.5
                    },
                    "unit_weight": {
                      "type": "integer",
                      "description": "Weight in grams of the good per unit.",
                      "example": 110
                    },
                    "attributes": {
                      "type": "array",
                      "minItems": 0,
                      "description": "Attributes for the commodity good. Used for additional information.",
                      "items": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string",
                            "description": "Name of the attribute.",
                            "example": "vat_no"
                          },
                          "value": {
                            "type": "string",
                            "description": "Value of the attribute.",
                            "example": "DK36399066"
                          }
                        },
                        "required": [
                          "name",
                          "value"
                        ]
                      }
                    }
                  }
                }
              }
            }
          },
          "cod": {
            "description": "Used for COD (cash on delivery) shipments, when booking with service code COD",
            "type": "object",
            "properties": {
              "amount": {
                "type": "number",
                "description": "The amount to be collected.",
                "example": 326
              },
              "currency_code": {
                "type": "string",
                "description": "Currency code of the amount.",
                "example": "NOK"
              },
              "account_number": {
                "type": "string",
                "description": "The account number which should receive the amount that has been collected.",
                "example": "123456789"
              }
            }
          },
          "carrier_insurance": {
            "description": "Object for indicating carrier insurance on the shipment. Only usable for specific carriers and when an insurance service code is provided.",
            "type": "object",
            "properties": {
              "amount": {
                "type": "number",
                "description": "Amount in the given currency that should be insured for the shipment.",
                "example": 1000,
                "nullable": true
              },
              "currency_code": {
                "type": "string",
                "description": "Indicates the currency code for the insured value.",
                "example": "DKK",
                "nullable": true
              }
            }
          },
          "attributes": {
            "type": "array",
            "description": "List of dynamic attributes for the shipment draft.",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "description": "Name of the attribute.",
                  "example": "vat_no"
                },
                "value": {
                  "type": "string",
                  "description": "Value of the attribute.",
                  "example": "DK36399066"
                }
              },
              "required": [
                "name",
                "value"
              ]
            }
          }
        }
      },
      {
        "type": "object",
        "properties": {
          "service_point_id": {
            "type": "string",
            "description": "ID of the service point the shipment should be sent to. Note that the full service point can also be provided in the `parties` array with `type` set to `service_point`.",
            "example": "96271"
          }
        }
      }
    ]
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipment_drafts/{param_id}"
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
    param_id: int = typer.Argument(None, help="ID for the shipment draft that need to be archived"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Delete a shipment draft"""
    if help_json:
        print("""{
  "command": "shipmondo shipment_drafts delete",
  "description": "Delete a shipment draft",
  "method": "DELETE",
  "endpoint": "/shipment_drafts/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment draft that need to be archived"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipment_drafts/{param_id}"
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

