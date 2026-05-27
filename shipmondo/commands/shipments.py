import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage shipments")

@app.command("labels")
def labels_cmd(
    param_id: int = typer.Argument(None, help="ID for the shipment to be included in the filter"),
    label_format: str = typer.Option(None, "--label-format", help="Which format the labels should be.  *10x19* is 10 cm x 19 cm  *compact* format returns the smallest label possible."),
    scale_by: str = typer.Option(None, "--scale-by", help="Scale down the labels by either width or height. Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl"),
    scale_size: float = typer.Option(None, "--scale-size", help="Desired scaled length in cm of dimension in 'scale_by'.If the length is higher or wider than the original labels, the labels will not be scaled.   Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve labels of a shipment"""
    if help_json:
        print("""{
  "command": "shipmondo shipments labels",
  "description": "Retrieve labels of a shipment",
  "method": "GET",
  "endpoint": "/shipments/{id}/labels",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment to be included in the filter"
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
      "description": "Scale down the labels by either width or height. Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl"
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

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipments/{param_id}/labels"
    url_params = {}
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

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID for the shipment to be included in the filter"),
    order_id: str = typer.Option(None, "--order-id", help="Order ID for the shipments to be included in the filter"),
    package_number: str = typer.Option(None, "--package-number", help="Shipment or package number for the shipments to be included in the filter"),
    carrier_code: str = typer.Option(None, "--carrier-code", help="Carrier code to be included in the filter."),
    sender_country: str = typer.Option(None, "--sender-country", help="Country code (ISO Alpha-2) to be included in the filter."),
    receiver_country: str = typer.Option(None, "--receiver-country", help="Country code (ISO Alpha-2) to be included in the filter."),
    waybill_reference: str = typer.Option(None, "--waybill-reference", help="Reference of the bulk waybill that the shipment is included in, to be included in the filter."),
    created_at_min: str = typer.Option(None, "--created-at-min", help="'From' timestamp for the shipments to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "),
    created_at_max: str = typer.Option(None, "--created-at-max", help="'To' timestamp for the shipments to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all shipments"""
    if help_json:
        print("""{
  "command": "shipmondo shipments list",
  "description": "List all shipments",
  "method": "GET",
  "endpoint": "/shipments",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID for the shipment to be included in the filter"
    },
    "order_id": {
      "cli_flag": "--order-id",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Order ID for the shipments to be included in the filter"
    },
    "package_number": {
      "cli_flag": "--package-number",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Shipment or package number for the shipments to be included in the filter"
    },
    "carrier_code": {
      "cli_flag": "--carrier-code",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Carrier code to be included in the filter."
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
    "waybill_reference": {
      "cli_flag": "--waybill-reference",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Reference of the bulk waybill that the shipment is included in, to be included in the filter."
    },
    "created_at_min": {
      "cli_flag": "--created-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' timestamp for the shipments to be included in the filter. Examples: * 2017-06-19T11:00:03.305+02:00 * 2017-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00 "
    },
    "created_at_max": {
      "cli_flag": "--created-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' timestamp for the shipments to be included in the filter. Examples: * 2017-06-29T11:00:03.305+02:00 * 2017-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00 "
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
    endpoint = f"/shipments"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if order_id is not None:
        url_params["order_id"] = order_id
    if package_number is not None:
        url_params["package_number"] = package_number
    if carrier_code is not None:
        url_params["carrier_code"] = carrier_code
    if sender_country is not None:
        url_params["sender_country"] = sender_country
    if receiver_country is not None:
        url_params["receiver_country"] = receiver_country
    if waybill_reference is not None:
        url_params["waybill_reference"] = waybill_reference
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
    """Create a shipment"""
    if help_json:
        print("""{
  "command": "shipmondo shipments create",
  "description": "Create a shipment",
  "method": "POST",
  "endpoint": "/shipments",
  "parameters": {},
  "payload_schema": {
    "required": [
      "own_agreement",
      "parcels",
      "product_code",
      "service_codes"
    ],
    "type": "object",
    "properties": {
      "test_mode": {
        "type": "boolean",
        "description": "This option is deprecated and will be removed soon. Please use the [Sandbox](https://shipmondo.dev/docs/sandbox) instead.",
        "deprecated": true,
        "example": true
      },
      "own_agreement": {
        "type": "boolean",
        "default": false,
        "description": "Whether or not the shipment should be booked via your own agreement or Shipmondo's agreement."
      },
      "customer_number": {
        "type": "string",
        "description": "Customer number for the agreement you wish to use. Mostly used if multiple agreements for the same carrier are set up on the account. Defaults to the agreement that was created first."
      },
      "label_format": {
        "type": "string",
        "description": "If label_format is specified, the shipping labels will be included in the response. Defaults to what is setup for the user.",
        "enum": [
          "a4_pdf",
          "10x19_pdf",
          "10x19_png",
          "10x19_zpl",
          "compact_png",
          "compact_pdf",
          "compact_zpl"
        ],
        "example": null
      },
      "product_code": {
        "type": "string",
        "description": "Product code of the product of the shipment.",
        "example": "GLSDK_SD"
      },
      "service_codes": {
        "description": "Comma-separated string of codes of services that are booked with the shipment.",
        "type": "string",
        "example": "EMAIL_NT,SMS_NT"
      },
      "services": {
        "description": "Use service_codes instead.",
        "type": "string",
        "deprecated": true
      },
      "reference": {
        "type": "string",
        "description": "Reference can be printed on the label and transmitted to carriers, when possible.",
        "example": "Order 10001"
      },
      "additional_reference": {
        "type": "string",
        "description": "An secondary reference. When possible, it will be transmitted to the carrier and printed on the label",
        "example": "Invoice 10001"
      },
      "automatic_select_service_point": {
        "type": "boolean",
        "description": "Whether or not the system should automatically select the service point closest to the receiver, when required.",
        "default": false
      },
      "contents": {
        "description": "General description of the contents of the shipment.",
        "type": "string",
        "example": "Goods"
      },
      "term_of_trade": {
        "type": "string",
        "description": "Incoterm for the shipments, e.g., DDP when customs should be paid by the sender.",
        "example": "DAP",
        "default": "DAP"
      },
      "origin_shipment_id": {
        "description": "ID of the origin shipment that the shipment is a return for.",
        "type": "string",
        "example": "1000001235"
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
      "sender": {
        "allOf": [
          {
            "required": [
              "address1",
              "city",
              "country_code",
              "name",
              "zipcode"
            ],
            "type": "object",
            "description": "Sender address for the object",
            "properties": {
              "name": {
                "type": "string",
                "example": "Min Virksomhed ApS",
                "description": "Name of the sender. Can be either a company name or the name of a private person."
              },
              "attention": {
                "type": "string",
                "example": "Lene Hansen",
                "description": "Attention of the sender. If the sender is a company, it is the contact person."
              },
              "address1": {
                "type": "string",
                "example": "Strandvejen 6B",
                "description": "Address of the sender, including address number."
              },
              "address2": {
                "type": "string",
                "description": "Second address line of the sender. Can be used for floor/room number, building name etc.",
                "example": null
              },
              "zipcode": {
                "type": "string",
                "example": "5240",
                "description": "Zip code of the address."
              },
              "city": {
                "type": "string",
                "example": "Odense N\u00d8",
                "description": "Name of the city that the zip code refers to."
              },
              "country_code": {
                "type": "string",
                "example": "DK",
                "description": "ISO 3166-1 alpha-2 country code of the sender."
              },
              "vat_id": {
                "type": "string",
                "example": "GB018384932372",
                "description": "Special VAT identification number; for example, GB EORI for Great Britain or VOEC for Norway."
              },
              "email": {
                "type": "string",
                "example": "info@minvirksomhed.dk",
                "description": "Email address of the sender"
              },
              "mobile": {
                "type": "string",
                "example": "70400407",
                "description": "Mobile number of the sender"
              },
              "telephone": {
                "type": "string",
                "example": "70400407",
                "description": "Landline phone number of the sender"
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `sender` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "receiver": {
        "allOf": [
          {
            "required": [
              "address1",
              "city",
              "country_code",
              "name",
              "zipcode"
            ],
            "type": "object",
            "description": "Receiver address for the object",
            "properties": {
              "name": {
                "type": "string",
                "example": "Lene Hansen",
                "description": "Name of the receiver. Can be either a company name or the name of a private person."
              },
              "attention": {
                "type": "string",
                "example": null,
                "description": "Attention of the receiver. If the receiver is a company, it is the contact person."
              },
              "address1": {
                "type": "string",
                "example": "Skibhusvej 52",
                "description": "Address of the receiver, including address number."
              },
              "address2": {
                "type": "string",
                "description": "Second address line of the receiver. Can be used for, e.g.,apartment number.",
                "example": null
              },
              "zipcode": {
                "type": "string",
                "example": "5000",
                "description": "Zip code of the address."
              },
              "city": {
                "type": "string",
                "example": "Odense C",
                "description": "Name of the city that the zip code refers to."
              },
              "country_code": {
                "type": "string",
                "example": "DK",
                "description": "ISO 3166-1 alpha-2 country code of the receiver address."
              },
              "vat_id": {
                "type": "string",
                "example": "GB018384932372",
                "description": "Special VAT identification number; for example, GB EORI for Great Britain."
              },
              "email": {
                "type": "string",
                "example": "lene@email.dk",
                "description": "Email address of the receiver"
              },
              "mobile": {
                "type": "string",
                "example": "12345678",
                "description": "Mobile number of the receiver"
              },
              "telephone": {
                "type": "string",
                "example": "12345678",
                "description": "Landline phone number of the receiver"
              },
              "instruction": {
                "type": "string",
                "example": "Place on the front porch.",
                "description": "Delivery instruction to the carrier. Only applicable for products which support receiver instructions."
              },
              "date": {
                "type": "string",
                "format": "date",
                "example": "2021-10-14",
                "description": "Requested delivery date."
              },
              "from_time": {
                "type": "string",
                "format": "time",
                "example": "08:00",
                "description": "Requested earliest delivery time."
              },
              "to_time": {
                "type": "string",
                "format": "time",
                "example": "16:00",
                "description": "Requested latest delivery time."
              },
              "member_id": {
                "type": "string",
                "example": "1234567890",
                "description": "Carrier member ID. Some products support/require this; e.g., DHL Parcel shipments to Packstations (DHL PostNumber)."
              },
              "access_code": {
                "type": "string",
                "example": "1234",
                "description": "Gate/door code for the carrier to access the receiver's address."
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `receiver` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "pick_up": {
        "allOf": [
          {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "example": "Min Virksomhed A/S"
              },
              "attention": {
                "type": "string",
                "example": null
              },
              "address1": {
                "type": "string",
                "example": "Hvileh\u00f8jvej 25"
              },
              "address2": {
                "type": "string",
                "description": "Second address line. Can be used for floor/room number, building name etc.",
                "example": null
              },
              "country_code": {
                "type": "string",
                "example": "DK"
              },
              "zipcode": {
                "type": "string",
                "example": "5220"
              },
              "city": {
                "type": "string",
                "example": "Odense S\u00d8"
              },
              "telephone": {
                "type": "string",
                "example": "80808080"
              },
              "instruction": {
                "type": "string",
                "example": "Goods are placed at gate 21",
                "description": "Pickup instruction to the carrier. Only applicable for products which supports pickup instructions."
              },
              "date": {
                "type": "string",
                "format": "date",
                "example": "2021-10-13",
                "description": "Requested pickup date."
              },
              "from_time": {
                "type": "string",
                "format": "time",
                "example": "08:00",
                "description": "Requested earliest pickup time."
              },
              "to_time": {
                "type": "string",
                "format": "time",
                "example": "16:00",
                "description": "Requested latest pickup time."
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `pickup` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "bill_to": {
        "allOf": [
          {
            "type": "object",
            "description": "Customs billing information if it is other than sender/receiver.",
            "properties": {
              "name": {
                "type": "string",
                "example": "Min Virksomhed A/S"
              },
              "attention": {
                "type": "string",
                "example": null
              },
              "address1": {
                "type": "string",
                "example": "Hvileh\u00f8jvej 25"
              },
              "address2": {
                "type": "string",
                "description": "Second address line can be used for floor/room number, building name etc.",
                "example": null
              },
              "zipcode": {
                "type": "string",
                "example": "5220"
              },
              "city": {
                "type": "string",
                "example": "Odense S\u00d8"
              },
              "vat_id": {
                "description": "VAT no. of the customs billing party.",
                "type": "string",
                "example": "DK12345678"
              },
              "country_code": {
                "type": "string",
                "example": "DK"
              },
              "telephone": {
                "type": "string",
                "example": "80808080"
              },
              "mobile": {
                "type": "string",
                "example": "80808080"
              },
              "email": {
                "type": "string",
                "example": "jim@minvirksomhed.dk"
              },
              "customer_number": {
                "type": "string",
                "example": "12345678",
                "description": "Separate carrier customer number to bill if applicable with the given carrier."
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `importer` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "service_point": {
        "allOf": [
          {
            "type": "object",
            "description": "Service point address. Used for shop delivery carrier products.",
            "properties": {
              "id": {
                "type": "string",
                "example": "95558",
                "description": "Identifier of the service point."
              },
              "name": {
                "type": "string",
                "example": "P\u00e5skel\u00f8kkens K\u00f8bmand",
                "description": "Name of the service point."
              },
              "address1": {
                "type": "string",
                "example": "Paaskel\u00f8kkevej 11",
                "description": "Address of the service point."
              },
              "address2": {
                "type": "string",
                "description": "Second address line can be used for floor/room number, building name etc.",
                "example": null
              },
              "zipcode": {
                "type": "string",
                "example": "5000",
                "description": "Zip code of the service point."
              },
              "city": {
                "type": "string",
                "example": "Odense C",
                "description": "City of the provided zipcode."
              },
              "country_code": {
                "type": "string",
                "example": "DK",
                "description": "ISO 3166-1 alpha-2 country code of the service point."
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `service_point` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "return_to": {
        "allOf": [
          {
            "type": "object",
            "description": "Return address if different from the sender address. This is only available for specific products.",
            "properties": {
              "name": {
                "type": "string",
                "example": "Min Virksomhed A/S"
              },
              "attention": {
                "type": "string",
                "example": null
              },
              "address1": {
                "type": "string",
                "example": "Hvileh\u00f8jvej 25"
              },
              "address2": {
                "type": "string",
                "description": "Second address line can be used for floor/room number, building name etc.",
                "example": null
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
              },
              "telephone": {
                "type": "string",
                "example": "80808080"
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `return` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "service_point_id": {
        "type": "string",
        "description": "ID of the service point the shipment should be sent to. Note that the full service point can also be provided in the `parties` array with `type` set to `service_point`.",
        "example": "96271"
      },
      "pickup_details": {
        "type": "object",
        "description": "Details for pickup.",
        "properties": {
          "date": {
            "type": "string",
            "format": "date",
            "example": "2021-10-13",
            "description": "Requested pickup date."
          },
          "from": {
            "type": "string",
            "format": "time",
            "example": "08:00:00",
            "description": "Requested earliest pickup time. Format HH:MM:SS."
          },
          "to": {
            "type": "string",
            "format": "time",
            "example": "16:00:00",
            "description": "Requested latest pickup time. Format HH:MM:SS."
          },
          "instruction": {
            "type": "string",
            "example": "Goods are placed at gate 21",
            "description": "Pickup instruction to the carrier. Only applicable for products which supports pickup instructions."
          }
        }
      },
      "delivery_details": {
        "type": "object",
        "description": "Details for delivery.",
        "properties": {
          "date": {
            "type": "string",
            "format": "date",
            "example": "2021-10-14",
            "description": "Requested delivery date. format: YYYY-MM-DD."
          },
          "from": {
            "type": "string",
            "format": "time",
            "example": "08:00:00",
            "description": "Requested earliest delivery time. Format HH:MM:SS."
          },
          "to": {
            "type": "string",
            "format": "time",
            "example": "16:00:00",
            "description": "Requested latest delivery time. Format HH:MM:SS."
          },
          "instruction": {
            "type": "string",
            "example": "Place on the front porch.",
            "description": "Delivery instruction to the carrier. Only applicable for products which support delivery instructions."
          }
        }
      },
      "label_overlay": {
        "type": "object",
        "description": "Extra section so that shipment label includes a custom barcode and texts. The size of the label will be in 10 x 21 cm instead of 10 x 19 cm.",
        "properties": {
          "barcode": {
            "type": "string",
            "example": "1234567890123"
          },
          "left_text": {
            "type": "string",
            "example": "ABC"
          },
          "right_text": {
            "type": "string",
            "example": "DEF"
          }
        },
        "nullable": true
      },
      "label_scale": {
        "type": "object",
        "description": "Scale for the label. Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl\n\n Note: Use this feature at your own risk. Shipmondo can\u2019t guarantee the scaled labels are usable. Always get the label approved by the carrier before using this feature in production.",
        "required": [
          "scale_by",
          "size"
        ],
        "properties": {
          "scale_by": {
            "description": "Scale down the labels by either width or height.",
            "type": "string",
            "enum": [
              "height",
              "width"
            ]
          },
          "size": {
            "description": "Desired scaled length in cm of dimension in \"scale_by\".If the length is higher or wider than the original labels, the labels will not be scaled.",
            "type": "number",
            "example": 15.6
          }
        }
      },
      "parcels": {
        "type": "array",
        "items": {
          "allOf": [
            {
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
            },
            {
              "type": "object",
              "properties": {
                "internal_reference": {
                  "type": "string",
                  "description": "A reference for internal use to track parcels, not sent to the carrier.",
                  "example": "parcel-1",
                  "nullable": true
                }
              }
            }
          ]
        },
        "minItems": 1
      },
      "print": {
        "type": "boolean",
        "description": "Print the label via the print client. Shipment labels can be sent out to the print queue automatically. Printer and format are specified in the print_at element.",
        "default": false
      },
      "print_at": {
        "type": "object",
        "properties": {
          "host_name": {
            "type": "string",
            "description": "Name of the PC / host where the print client is installed.",
            "example": "WAREHOUSE-PC"
          },
          "printer_name": {
            "type": "string",
            "description": "Name of the printer that is registered within the print client.",
            "example": "Zebra Zdesigner GK420D"
          },
          "label_format": {
            "type": "string",
            "description": "The label format that the printer can accept.",
            "enum": [
              "a4_pdf",
              "10x19_pdf",
              "10x19_png",
              "10x19_zpl"
            ],
            "example": "10x19_zpl"
          }
        }
      },
      "send_label": {
        "type": "object",
        "description": "Send out the label as PDF via email after booking.",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the recipient of the label.",
            "example": "Jim"
          },
          "email": {
            "type": "string",
            "description": "Email address of the recipient of the label, which the label should be sent to.",
            "example": "jim@minvirksomhed.dk"
          },
          "label_format": {
            "type": "string",
            "description": "The label format that should be attached to the email.",
            "enum": [
              "a4_pdf",
              "10x19_pdf",
              "compact_pdf"
            ],
            "example": "a4_pdf"
          }
        }
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
        "description": "Custom details used to generate proforma invoice or sent directly to the carrier. This object is only used for shipments where customs declaration is required.",
        "properties": {
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
            ]
          },
          "currency_code": {
            "type": "string",
            "description": "Currency code for declared prices.",
            "example": "DKK"
          },
          "freight_cost": {
            "type": "number",
            "description": "Cost of freight/shipping in the declared currency.",
            "example": 100.5
          },
          "insurance_cost": {
            "type": "number",
            "description": "Cost of insurance in the declared currency.",
            "example": 50.0
          },
          "term_of_trade": {
            "type": "string",
            "description": "Legacy field. Use `term_of_trade` in the root of the request instead.",
            "example": "DAP",
            "default": "DAP",
            "deprecated": true
          },
          "billed_to_custom_invoice_text": {
            "type": "string",
            "description": "Legacy field. Use `importer` party with attribute `name` = `invoice_note`. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details.\n\nA custom text for the shipment importer. Will not be transmitted to carriers, but will appear on proforma/commercial invoice under \"Importer\" if filled.",
            "example": "Key code: ABC123",
            "deprecated": true
          },
          "sender_custom_invoice_text": {
            "type": "string",
            "description": "Legacy field. Use `sender` party with attribute `name` = `invoice_note`. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details.\n\nA custom text for the shipment sender. Will not be transmitted to carriers, but will appear on proforma/commercial invoice under \"Sender\" if filled.",
            "example": "Key code: ABC123",
            "deprecated": true
          },
          "receiver_custom_invoice_text": {
            "type": "string",
            "description": "Legacy field. Use `receiver` party with attribute `name` = `invoice_note`. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details.\n\nA custom text for the shipment receiver. Will not be transmitted to carriers, but will appear on proforma/commercial invoice under \"Delivery to\" if filled.",
            "example": "Key code: ABC123",
            "deprecated": true
          },
          "goods": {
            "type": "array",
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
                "content": {
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
      "replace_http_status_code": {
        "type": "boolean",
        "description": "If replace_http_status_code is set to true, request will have HTTP status 200. The real HTTP status will be included in the response header as X-HTTP-Status-Code. This is to prevent runtime errors in some frameworks and make it possible to read the error messages.",
        "default": false
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
      "dfm": {
        "description": "Special object for extra information when shipping with Danske Fragtm\u00e6nd. Otherwise it can be ignored.",
        "type": "object",
        "nullable": true,
        "properties": {
          "insurance_type": {
            "type": "string",
            "description": "Type of insurance to be booked.",
            "example": "A",
            "enum": [
              "A",
              "B",
              "C",
              "D"
            ],
            "nullable": true
          },
          "insurance_amount": {
            "type": "number",
            "description": "Amount in DKK that should be insured for the shipment.",
            "example": 1000,
            "nullable": true
          },
          "dot_type": {
            "type": "string",
            "description": "Type of DOT used for the shipment.",
            "example": "DO1",
            "enum": [
              "DO1",
              "DO2",
              "DO3",
              "DO4"
            ],
            "nullable": true
          },
          "dot_time": {
            "type": "string",
            "format": "time",
            "description": "Requested time of DOT delivery. Only valid for DO2, DO3 and DO4. Format: HH:MM",
            "example": "15:00",
            "nullable": true
          },
          "pallets1": {
            "type": "integer",
            "description": "Legacy field. Use `pallet_exchange` instead.",
            "example": 1,
            "nullable": true,
            "deprecated": true
          },
          "pallets2": {
            "type": "integer",
            "description": "Legacy field. Use `pallet_exchange` instead.",
            "example": 1,
            "nullable": true,
            "deprecated": true
          },
          "pallets4": {
            "type": "integer",
            "description": "Legacy field. Use `pallet_exchange` instead.",
            "example": 1,
            "nullable": true,
            "deprecated": true
          },
          "limited_quantity_weight": {
            "type": "integer",
            "description": "Legacy field. Use `parcels.dangerous_goods` instead.",
            "example": 1000,
            "nullable": true,
            "deprecated": true
          },
          "has_dangerous_goods": {
            "type": "boolean",
            "description": "Legacy field. Use `parcels.dangerous_goods` instead.",
            "example": true,
            "nullable": true,
            "deprecated": true
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
      "add_barcode_to_label": {
        "type": "boolean",
        "description": "Add a Code 128 barcode with the shipment ID on the label. Only applicable for product_codes UNI_AL & UNI_ALP.",
        "nullable": true
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipments"
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
    param_id: int = typer.Argument(None, help="ID for the shipment to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a shipment"""
    if help_json:
        print("""{
  "command": "shipmondo shipments get",
  "description": "Retrieve a shipment",
  "method": "GET",
  "endpoint": "/shipments/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipments/{param_id}"
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

@app.command("put_cancel")
def put_cancel_cmd(
    param_id: int = typer.Argument(None, help="ID for the shipment to be included in the filter"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Cancel a shipment"""
    if help_json:
        print("""{
  "command": "shipmondo shipments put_cancel",
  "description": "Cancel a shipment",
  "method": "PUT",
  "endpoint": "/shipments/{id}/cancel",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipments/{param_id}/cancel"
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

@app.command("proforma_invoices")
def proforma_invoices_cmd(
    param_id: int = typer.Argument(None, help="ID for the shipment to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a proforma invoice"""
    if help_json:
        print("""{
  "command": "shipmondo shipments proforma_invoices",
  "description": "Retrieve a proforma invoice",
  "method": "GET",
  "endpoint": "/shipments/{id}/proforma_invoices",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipments/{param_id}/proforma_invoices"
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

@app.command("waybills")
def waybills_cmd(
    param_id: int = typer.Argument(None, help="ID for the shipment to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve waybill for a shipment"""
    if help_json:
        print("""{
  "command": "shipmondo shipments waybills",
  "description": "Retrieve waybill for a shipment",
  "method": "GET",
  "endpoint": "/shipments/{id}/waybills",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipments/{param_id}/waybills"
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

@app.command("quote")
def quote_cmd(
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
  "command": "shipmondo shipments quote",
  "description": "Create a shipment quote",
  "method": "POST",
  "endpoint": "/shipments/quote",
  "parameters": {},
  "payload_schema": {
    "required": [
      "own_agreement",
      "parcels",
      "product_code",
      "service_codes"
    ],
    "type": "object",
    "properties": {
      "test_mode": {
        "type": "boolean",
        "description": "This option is deprecated and will be removed soon. Please use the [Sandbox](https://shipmondo.dev/docs/sandbox) instead.",
        "deprecated": true,
        "example": true
      },
      "own_agreement": {
        "type": "boolean",
        "default": false,
        "description": "Whether or not the shipment should be booked via your own agreement or Shipmondo's agreement."
      },
      "customer_number": {
        "type": "string",
        "description": "Customer number for the agreement you wish to use. Mostly used if multiple agreements for the same carrier are set up on the account. Defaults to the agreement that was created first."
      },
      "label_format": {
        "type": "string",
        "description": "If label_format is specified, the shipping labels will be included in the response. Defaults to what is setup for the user.",
        "enum": [
          "a4_pdf",
          "10x19_pdf",
          "10x19_png",
          "10x19_zpl",
          "compact_png",
          "compact_pdf",
          "compact_zpl"
        ],
        "example": null
      },
      "product_code": {
        "type": "string",
        "description": "Product code of the product of the shipment.",
        "example": "GLSDK_SD"
      },
      "service_codes": {
        "description": "Comma-separated string of codes of services that are booked with the shipment.",
        "type": "string",
        "example": "EMAIL_NT,SMS_NT"
      },
      "services": {
        "description": "Use service_codes instead.",
        "type": "string",
        "deprecated": true
      },
      "reference": {
        "type": "string",
        "description": "Reference can be printed on the label and transmitted to carriers, when possible.",
        "example": "Order 10001"
      },
      "additional_reference": {
        "type": "string",
        "description": "An secondary reference. When possible, it will be transmitted to the carrier and printed on the label",
        "example": "Invoice 10001"
      },
      "automatic_select_service_point": {
        "type": "boolean",
        "description": "Whether or not the system should automatically select the service point closest to the receiver, when required.",
        "default": false
      },
      "contents": {
        "description": "General description of the contents of the shipment.",
        "type": "string",
        "example": "Goods"
      },
      "term_of_trade": {
        "type": "string",
        "description": "Incoterm for the shipments, e.g., DDP when customs should be paid by the sender.",
        "example": "DAP",
        "default": "DAP"
      },
      "origin_shipment_id": {
        "description": "ID of the origin shipment that the shipment is a return for.",
        "type": "string",
        "example": "1000001235"
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
      "sender": {
        "allOf": [
          {
            "required": [
              "address1",
              "city",
              "country_code",
              "name",
              "zipcode"
            ],
            "type": "object",
            "description": "Sender address for the object",
            "properties": {
              "name": {
                "type": "string",
                "example": "Min Virksomhed ApS",
                "description": "Name of the sender. Can be either a company name or the name of a private person."
              },
              "attention": {
                "type": "string",
                "example": "Lene Hansen",
                "description": "Attention of the sender. If the sender is a company, it is the contact person."
              },
              "address1": {
                "type": "string",
                "example": "Strandvejen 6B",
                "description": "Address of the sender, including address number."
              },
              "address2": {
                "type": "string",
                "description": "Second address line of the sender. Can be used for floor/room number, building name etc.",
                "example": null
              },
              "zipcode": {
                "type": "string",
                "example": "5240",
                "description": "Zip code of the address."
              },
              "city": {
                "type": "string",
                "example": "Odense N\u00d8",
                "description": "Name of the city that the zip code refers to."
              },
              "country_code": {
                "type": "string",
                "example": "DK",
                "description": "ISO 3166-1 alpha-2 country code of the sender."
              },
              "vat_id": {
                "type": "string",
                "example": "GB018384932372",
                "description": "Special VAT identification number; for example, GB EORI for Great Britain or VOEC for Norway."
              },
              "email": {
                "type": "string",
                "example": "info@minvirksomhed.dk",
                "description": "Email address of the sender"
              },
              "mobile": {
                "type": "string",
                "example": "70400407",
                "description": "Mobile number of the sender"
              },
              "telephone": {
                "type": "string",
                "example": "70400407",
                "description": "Landline phone number of the sender"
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `sender` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "receiver": {
        "allOf": [
          {
            "required": [
              "address1",
              "city",
              "country_code",
              "name",
              "zipcode"
            ],
            "type": "object",
            "description": "Receiver address for the object",
            "properties": {
              "name": {
                "type": "string",
                "example": "Lene Hansen",
                "description": "Name of the receiver. Can be either a company name or the name of a private person."
              },
              "attention": {
                "type": "string",
                "example": null,
                "description": "Attention of the receiver. If the receiver is a company, it is the contact person."
              },
              "address1": {
                "type": "string",
                "example": "Skibhusvej 52",
                "description": "Address of the receiver, including address number."
              },
              "address2": {
                "type": "string",
                "description": "Second address line of the receiver. Can be used for, e.g.,apartment number.",
                "example": null
              },
              "zipcode": {
                "type": "string",
                "example": "5000",
                "description": "Zip code of the address."
              },
              "city": {
                "type": "string",
                "example": "Odense C",
                "description": "Name of the city that the zip code refers to."
              },
              "country_code": {
                "type": "string",
                "example": "DK",
                "description": "ISO 3166-1 alpha-2 country code of the receiver address."
              },
              "vat_id": {
                "type": "string",
                "example": "GB018384932372",
                "description": "Special VAT identification number; for example, GB EORI for Great Britain."
              },
              "email": {
                "type": "string",
                "example": "lene@email.dk",
                "description": "Email address of the receiver"
              },
              "mobile": {
                "type": "string",
                "example": "12345678",
                "description": "Mobile number of the receiver"
              },
              "telephone": {
                "type": "string",
                "example": "12345678",
                "description": "Landline phone number of the receiver"
              },
              "instruction": {
                "type": "string",
                "example": "Place on the front porch.",
                "description": "Delivery instruction to the carrier. Only applicable for products which support receiver instructions."
              },
              "date": {
                "type": "string",
                "format": "date",
                "example": "2021-10-14",
                "description": "Requested delivery date."
              },
              "from_time": {
                "type": "string",
                "format": "time",
                "example": "08:00",
                "description": "Requested earliest delivery time."
              },
              "to_time": {
                "type": "string",
                "format": "time",
                "example": "16:00",
                "description": "Requested latest delivery time."
              },
              "member_id": {
                "type": "string",
                "example": "1234567890",
                "description": "Carrier member ID. Some products support/require this; e.g., DHL Parcel shipments to Packstations (DHL PostNumber)."
              },
              "access_code": {
                "type": "string",
                "example": "1234",
                "description": "Gate/door code for the carrier to access the receiver's address."
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `receiver` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "pick_up": {
        "allOf": [
          {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "example": "Min Virksomhed A/S"
              },
              "attention": {
                "type": "string",
                "example": null
              },
              "address1": {
                "type": "string",
                "example": "Hvileh\u00f8jvej 25"
              },
              "address2": {
                "type": "string",
                "description": "Second address line. Can be used for floor/room number, building name etc.",
                "example": null
              },
              "country_code": {
                "type": "string",
                "example": "DK"
              },
              "zipcode": {
                "type": "string",
                "example": "5220"
              },
              "city": {
                "type": "string",
                "example": "Odense S\u00d8"
              },
              "telephone": {
                "type": "string",
                "example": "80808080"
              },
              "instruction": {
                "type": "string",
                "example": "Goods are placed at gate 21",
                "description": "Pickup instruction to the carrier. Only applicable for products which supports pickup instructions."
              },
              "date": {
                "type": "string",
                "format": "date",
                "example": "2021-10-13",
                "description": "Requested pickup date."
              },
              "from_time": {
                "type": "string",
                "format": "time",
                "example": "08:00",
                "description": "Requested earliest pickup time."
              },
              "to_time": {
                "type": "string",
                "format": "time",
                "example": "16:00",
                "description": "Requested latest pickup time."
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `pickup` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "bill_to": {
        "allOf": [
          {
            "type": "object",
            "description": "Customs billing information if it is other than sender/receiver.",
            "properties": {
              "name": {
                "type": "string",
                "example": "Min Virksomhed A/S"
              },
              "attention": {
                "type": "string",
                "example": null
              },
              "address1": {
                "type": "string",
                "example": "Hvileh\u00f8jvej 25"
              },
              "address2": {
                "type": "string",
                "description": "Second address line can be used for floor/room number, building name etc.",
                "example": null
              },
              "zipcode": {
                "type": "string",
                "example": "5220"
              },
              "city": {
                "type": "string",
                "example": "Odense S\u00d8"
              },
              "vat_id": {
                "description": "VAT no. of the customs billing party.",
                "type": "string",
                "example": "DK12345678"
              },
              "country_code": {
                "type": "string",
                "example": "DK"
              },
              "telephone": {
                "type": "string",
                "example": "80808080"
              },
              "mobile": {
                "type": "string",
                "example": "80808080"
              },
              "email": {
                "type": "string",
                "example": "jim@minvirksomhed.dk"
              },
              "customer_number": {
                "type": "string",
                "example": "12345678",
                "description": "Separate carrier customer number to bill if applicable with the given carrier."
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `importer` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "service_point": {
        "allOf": [
          {
            "type": "object",
            "description": "Service point address. Used for shop delivery carrier products.",
            "properties": {
              "id": {
                "type": "string",
                "example": "95558",
                "description": "Identifier of the service point."
              },
              "name": {
                "type": "string",
                "example": "P\u00e5skel\u00f8kkens K\u00f8bmand",
                "description": "Name of the service point."
              },
              "address1": {
                "type": "string",
                "example": "Paaskel\u00f8kkevej 11",
                "description": "Address of the service point."
              },
              "address2": {
                "type": "string",
                "description": "Second address line can be used for floor/room number, building name etc.",
                "example": null
              },
              "zipcode": {
                "type": "string",
                "example": "5000",
                "description": "Zip code of the service point."
              },
              "city": {
                "type": "string",
                "example": "Odense C",
                "description": "City of the provided zipcode."
              },
              "country_code": {
                "type": "string",
                "example": "DK",
                "description": "ISO 3166-1 alpha-2 country code of the service point."
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `service_point` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "return_to": {
        "allOf": [
          {
            "type": "object",
            "description": "Return address if different from the sender address. This is only available for specific products.",
            "properties": {
              "name": {
                "type": "string",
                "example": "Min Virksomhed A/S"
              },
              "attention": {
                "type": "string",
                "example": null
              },
              "address1": {
                "type": "string",
                "example": "Hvileh\u00f8jvej 25"
              },
              "address2": {
                "type": "string",
                "description": "Second address line can be used for floor/room number, building name etc.",
                "example": null
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
              },
              "telephone": {
                "type": "string",
                "example": "80808080"
              }
            }
          },
          {
            "deprecated": true,
            "description": "Legacy object. Use `parties` array with `type` set to `return` instead. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details."
          }
        ]
      },
      "service_point_id": {
        "type": "string",
        "description": "ID of the service point the shipment should be sent to. Note that the full service point can also be provided in the `parties` array with `type` set to `service_point`.",
        "example": "96271"
      },
      "pickup_details": {
        "type": "object",
        "description": "Details for pickup.",
        "properties": {
          "date": {
            "type": "string",
            "format": "date",
            "example": "2021-10-13",
            "description": "Requested pickup date."
          },
          "from": {
            "type": "string",
            "format": "time",
            "example": "08:00:00",
            "description": "Requested earliest pickup time. Format HH:MM:SS."
          },
          "to": {
            "type": "string",
            "format": "time",
            "example": "16:00:00",
            "description": "Requested latest pickup time. Format HH:MM:SS."
          },
          "instruction": {
            "type": "string",
            "example": "Goods are placed at gate 21",
            "description": "Pickup instruction to the carrier. Only applicable for products which supports pickup instructions."
          }
        }
      },
      "delivery_details": {
        "type": "object",
        "description": "Details for delivery.",
        "properties": {
          "date": {
            "type": "string",
            "format": "date",
            "example": "2021-10-14",
            "description": "Requested delivery date. format: YYYY-MM-DD."
          },
          "from": {
            "type": "string",
            "format": "time",
            "example": "08:00:00",
            "description": "Requested earliest delivery time. Format HH:MM:SS."
          },
          "to": {
            "type": "string",
            "format": "time",
            "example": "16:00:00",
            "description": "Requested latest delivery time. Format HH:MM:SS."
          },
          "instruction": {
            "type": "string",
            "example": "Place on the front porch.",
            "description": "Delivery instruction to the carrier. Only applicable for products which support delivery instructions."
          }
        }
      },
      "label_overlay": {
        "type": "object",
        "description": "Extra section so that shipment label includes a custom barcode and texts. The size of the label will be in 10 x 21 cm instead of 10 x 19 cm.",
        "properties": {
          "barcode": {
            "type": "string",
            "example": "1234567890123"
          },
          "left_text": {
            "type": "string",
            "example": "ABC"
          },
          "right_text": {
            "type": "string",
            "example": "DEF"
          }
        },
        "nullable": true
      },
      "label_scale": {
        "type": "object",
        "description": "Scale for the label. Only applicable when label_format: a4_pdf, 10x19_pdf, 10x19_zpl, compact_pdf, compact_zpl\n\n Note: Use this feature at your own risk. Shipmondo can\u2019t guarantee the scaled labels are usable. Always get the label approved by the carrier before using this feature in production.",
        "required": [
          "scale_by",
          "size"
        ],
        "properties": {
          "scale_by": {
            "description": "Scale down the labels by either width or height.",
            "type": "string",
            "enum": [
              "height",
              "width"
            ]
          },
          "size": {
            "description": "Desired scaled length in cm of dimension in \"scale_by\".If the length is higher or wider than the original labels, the labels will not be scaled.",
            "type": "number",
            "example": 15.6
          }
        }
      },
      "parcels": {
        "type": "array",
        "items": {
          "allOf": [
            {
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
            },
            {
              "type": "object",
              "properties": {
                "internal_reference": {
                  "type": "string",
                  "description": "A reference for internal use to track parcels, not sent to the carrier.",
                  "example": "parcel-1",
                  "nullable": true
                }
              }
            }
          ]
        },
        "minItems": 1
      },
      "print": {
        "type": "boolean",
        "description": "Print the label via the print client. Shipment labels can be sent out to the print queue automatically. Printer and format are specified in the print_at element.",
        "default": false
      },
      "print_at": {
        "type": "object",
        "properties": {
          "host_name": {
            "type": "string",
            "description": "Name of the PC / host where the print client is installed.",
            "example": "WAREHOUSE-PC"
          },
          "printer_name": {
            "type": "string",
            "description": "Name of the printer that is registered within the print client.",
            "example": "Zebra Zdesigner GK420D"
          },
          "label_format": {
            "type": "string",
            "description": "The label format that the printer can accept.",
            "enum": [
              "a4_pdf",
              "10x19_pdf",
              "10x19_png",
              "10x19_zpl"
            ],
            "example": "10x19_zpl"
          }
        }
      },
      "send_label": {
        "type": "object",
        "description": "Send out the label as PDF via email after booking.",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the recipient of the label.",
            "example": "Jim"
          },
          "email": {
            "type": "string",
            "description": "Email address of the recipient of the label, which the label should be sent to.",
            "example": "jim@minvirksomhed.dk"
          },
          "label_format": {
            "type": "string",
            "description": "The label format that should be attached to the email.",
            "enum": [
              "a4_pdf",
              "10x19_pdf",
              "compact_pdf"
            ],
            "example": "a4_pdf"
          }
        }
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
        "description": "Custom details used to generate proforma invoice or sent directly to the carrier. This object is only used for shipments where customs declaration is required.",
        "properties": {
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
            ]
          },
          "currency_code": {
            "type": "string",
            "description": "Currency code for declared prices.",
            "example": "DKK"
          },
          "freight_cost": {
            "type": "number",
            "description": "Cost of freight/shipping in the declared currency.",
            "example": 100.5
          },
          "insurance_cost": {
            "type": "number",
            "description": "Cost of insurance in the declared currency.",
            "example": 50.0
          },
          "term_of_trade": {
            "type": "string",
            "description": "Legacy field. Use `term_of_trade` in the root of the request instead.",
            "example": "DAP",
            "default": "DAP",
            "deprecated": true
          },
          "billed_to_custom_invoice_text": {
            "type": "string",
            "description": "Legacy field. Use `importer` party with attribute `name` = `invoice_note`. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details.\n\nA custom text for the shipment importer. Will not be transmitted to carriers, but will appear on proforma/commercial invoice under \"Importer\" if filled.",
            "example": "Key code: ABC123",
            "deprecated": true
          },
          "sender_custom_invoice_text": {
            "type": "string",
            "description": "Legacy field. Use `sender` party with attribute `name` = `invoice_note`. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details.\n\nA custom text for the shipment sender. Will not be transmitted to carriers, but will appear on proforma/commercial invoice under \"Sender\" if filled.",
            "example": "Key code: ABC123",
            "deprecated": true
          },
          "receiver_custom_invoice_text": {
            "type": "string",
            "description": "Legacy field. Use `receiver` party with attribute `name` = `invoice_note`. See [migration guide](https://shipmondo.dev/docs/api/parties-migration) for details.\n\nA custom text for the shipment receiver. Will not be transmitted to carriers, but will appear on proforma/commercial invoice under \"Delivery to\" if filled.",
            "example": "Key code: ABC123",
            "deprecated": true
          },
          "goods": {
            "type": "array",
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
                "content": {
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
      "replace_http_status_code": {
        "type": "boolean",
        "description": "If replace_http_status_code is set to true, request will have HTTP status 200. The real HTTP status will be included in the response header as X-HTTP-Status-Code. This is to prevent runtime errors in some frameworks and make it possible to read the error messages.",
        "default": false
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
      "dfm": {
        "description": "Special object for extra information when shipping with Danske Fragtm\u00e6nd. Otherwise it can be ignored.",
        "type": "object",
        "nullable": true,
        "properties": {
          "insurance_type": {
            "type": "string",
            "description": "Type of insurance to be booked.",
            "example": "A",
            "enum": [
              "A",
              "B",
              "C",
              "D"
            ],
            "nullable": true
          },
          "insurance_amount": {
            "type": "number",
            "description": "Amount in DKK that should be insured for the shipment.",
            "example": 1000,
            "nullable": true
          },
          "dot_type": {
            "type": "string",
            "description": "Type of DOT used for the shipment.",
            "example": "DO1",
            "enum": [
              "DO1",
              "DO2",
              "DO3",
              "DO4"
            ],
            "nullable": true
          },
          "dot_time": {
            "type": "string",
            "format": "time",
            "description": "Requested time of DOT delivery. Only valid for DO2, DO3 and DO4. Format: HH:MM",
            "example": "15:00",
            "nullable": true
          },
          "pallets1": {
            "type": "integer",
            "description": "Legacy field. Use `pallet_exchange` instead.",
            "example": 1,
            "nullable": true,
            "deprecated": true
          },
          "pallets2": {
            "type": "integer",
            "description": "Legacy field. Use `pallet_exchange` instead.",
            "example": 1,
            "nullable": true,
            "deprecated": true
          },
          "pallets4": {
            "type": "integer",
            "description": "Legacy field. Use `pallet_exchange` instead.",
            "example": 1,
            "nullable": true,
            "deprecated": true
          },
          "limited_quantity_weight": {
            "type": "integer",
            "description": "Legacy field. Use `parcels.dangerous_goods` instead.",
            "example": 1000,
            "nullable": true,
            "deprecated": true
          },
          "has_dangerous_goods": {
            "type": "boolean",
            "description": "Legacy field. Use `parcels.dangerous_goods` instead.",
            "example": true,
            "nullable": true,
            "deprecated": true
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
      "add_barcode_to_label": {
        "type": "boolean",
        "description": "Add a Code 128 barcode with the shipment ID on the label. Only applicable for product_codes UNI_AL & UNI_ALP.",
        "nullable": true
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipments/quote"
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

@app.command("qr_code")
def qr_code_cmd(
    param_id: int = typer.Argument(None, help="ID for the shipment to fetch QR codes for"),
    file_format: str = typer.Option(None, "--file-format", help="The file format the QR Code will be returned as."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Fetch QR codes for a shipment"""
    if help_json:
        print("""{
  "command": "shipmondo shipments qr_code",
  "description": "Fetch QR codes for a shipment",
  "method": "GET",
  "endpoint": "/shipments/{id}/qr_code",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the shipment to fetch QR codes for"
    },
    "file_format": {
      "cli_flag": "--file-format",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "The file format the QR Code will be returned as."
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/shipments/{param_id}/qr_code"
    url_params = {}
    if file_format is not None:
        url_params["file_format"] = file_format
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

