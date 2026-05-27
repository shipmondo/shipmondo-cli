import typer
import json
import sys
from shipmondo.client import ShipmondoClient

app = typer.Typer(help="Manage sales_orders")

@app.command("list")
def list_cmd(
    param_id: int = typer.Option(None, "--id", help="ID for the sales order to be included in the filter."),
    order_id: str = typer.Option(None, "--order-id", help="Order ID for the sales order to be included in the filter."),
    reference: str = typer.Option(None, "--reference", help="reference for the order to be included in the filter."),
    bill_to_email: str = typer.Option(None, "--bill-to-email", help="Billing email for the order to be included in the filter."),
    bill_to_mobile: str = typer.Option(None, "--bill-to-mobile", help="Billing mobile for the order to be included in the filter."),
    ship_to_email: str = typer.Option(None, "--ship-to-email", help="Shipping email for the order to be included in the filter."),
    ship_to_mobile: str = typer.Option(None, "--ship-to-mobile", help="Shipping mobile for the order to be included in the filter."),
    archived: bool = typer.Option(None, "--archived", help="Filter for archived or not."),
    created_at_min: str = typer.Option(None, "--created-at-min", help="'From' value of 'created' timestamp for the sales orders to be included in the filter. Examples: * 2018-06-19T11:00:03.305+02:00 * 2018-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00"),
    created_at_max: str = typer.Option(None, "--created-at-max", help="'To' value of 'created' timestamp for the sales orders to be included in the filter. Examples: * 2018-06-29T11:00:03.305+02:00 * 2018-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00"),
    updated_at_min: str = typer.Option(None, "--updated-at-min", help="'From' value of 'updated' timestamp for the sales orders to be included in the filter. Examples: * 2018-06-19T11:00:03.305+02:00 * 2018-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00"),
    updated_at_max: str = typer.Option(None, "--updated-at-max", help="'To' value of 'updated' timestamp for the sales orders to be included in the filter. Examples: * 2018-06-29T11:00:03.305+02:00 * 2018-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00"),
    per_page: int = typer.Option(None, "--per-page", help="For pagination. Defines how many entries are returned per page."),
    page: int = typer.Option(None, "--page", help="For pagination. Defines which page the results are fetched from."),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List all sales orders"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders list",
  "description": "List all sales orders",
  "method": "GET",
  "endpoint": "/sales_orders",
  "parameters": {
    "id": {
      "cli_flag": "--id",
      "location": "query",
      "type": "int",
      "required": false,
      "description": "ID for the sales order to be included in the filter."
    },
    "order_id": {
      "cli_flag": "--order-id",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Order ID for the sales order to be included in the filter."
    },
    "reference": {
      "cli_flag": "--reference",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "reference for the order to be included in the filter."
    },
    "bill_to_email": {
      "cli_flag": "--bill-to-email",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Billing email for the order to be included in the filter."
    },
    "bill_to_mobile": {
      "cli_flag": "--bill-to-mobile",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Billing mobile for the order to be included in the filter."
    },
    "ship_to_email": {
      "cli_flag": "--ship-to-email",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Shipping email for the order to be included in the filter."
    },
    "ship_to_mobile": {
      "cli_flag": "--ship-to-mobile",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Shipping mobile for the order to be included in the filter."
    },
    "archived": {
      "cli_flag": "--archived",
      "location": "query",
      "type": "bool",
      "required": false,
      "description": "Filter for archived or not."
    },
    "created_at_min": {
      "cli_flag": "--created-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' value of 'created' timestamp for the sales orders to be included in the filter. Examples: * 2018-06-19T11:00:03.305+02:00 * 2018-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00"
    },
    "created_at_max": {
      "cli_flag": "--created-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' value of 'created' timestamp for the sales orders to be included in the filter. Examples: * 2018-06-29T11:00:03.305+02:00 * 2018-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00"
    },
    "updated_at_min": {
      "cli_flag": "--updated-at-min",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'From' value of 'updated' timestamp for the sales orders to be included in the filter. Examples: * 2018-06-19T11:00:03.305+02:00 * 2018-06-19 will be transformed into 2017-06-19T00:00:00.000+02:00"
    },
    "updated_at_max": {
      "cli_flag": "--updated-at-max",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "'To' value of 'updated' timestamp for the sales orders to be included in the filter. Examples: * 2018-06-29T11:00:03.305+02:00 * 2018-06-29 will be transformed into 2017-06-29T00:00:00.000+02:00"
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
    endpoint = f"/sales_orders"
    url_params = {}
    if param_id is not None:
        url_params["id"] = param_id
    if order_id is not None:
        url_params["order_id"] = order_id
    if reference is not None:
        url_params["reference"] = reference
    if bill_to_email is not None:
        url_params["bill_to_email"] = bill_to_email
    if bill_to_mobile is not None:
        url_params["bill_to_mobile"] = bill_to_mobile
    if ship_to_email is not None:
        url_params["ship_to_email"] = ship_to_email
    if ship_to_mobile is not None:
        url_params["ship_to_mobile"] = ship_to_mobile
    if archived is not None:
        url_params["archived"] = archived
    if created_at_min is not None:
        url_params["created_at_min"] = created_at_min
    if created_at_max is not None:
        url_params["created_at_max"] = created_at_max
    if updated_at_min is not None:
        url_params["updated_at_min"] = updated_at_min
    if updated_at_max is not None:
        url_params["updated_at_max"] = updated_at_max
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
    """Create a sales order"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders create",
  "description": "Create a sales order",
  "method": "POST",
  "endpoint": "/sales_orders",
  "parameters": {},
  "payload_schema": {
    "required": [
      "order_id",
      "ship_to",
      "bill_to",
      "order_lines",
      "payment_details"
    ],
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "example": "27000",
        "description": "Order ID for the sales order."
      },
      "ordered_at": {
        "type": "string",
        "format": "date-time",
        "example": "2018-10-17T13:25:44.557Z",
        "description": "ISO 8601 datetime the sales order was placed."
      },
      "source_name": {
        "type": "string",
        "example": "Testcompany ApS",
        "description": "Name of the source for the sales order."
      },
      "order_note": {
        "type": "string",
        "example": "Note",
        "description": "A note for the sales order."
      },
      "archived": {
        "type": "boolean",
        "default": false,
        "description": "Defines whether or not the sales order is archived."
      },
      "shipment_template_id": {
        "type": "integer",
        "example": 710,
        "description": "ID of the provided shipment template. Specifies the product and services for the order"
      },
      "return_shipment_template_id": {
        "type": "integer",
        "example": 710,
        "description": "ID of the provided return shipment template. Specifies the return product and services for the sales order."
      },
      "sales_order_packaging_id": {
        "type": "integer",
        "example": 11242,
        "description": "ID of the provided sales order packaging. The packaging specifies the dimensions for the order."
      },
      "bookkeeping_integration_id": {
        "type": "integer",
        "example": 241,
        "description": "ID of the provided bookkeeping integration. Allows the user to create invoices from the order."
      },
      "packing_slip_format": {
        "type": "string",
        "description": "If packing_slip_format is specified, the packing slips will be included in the response.",
        "example": null,
        "enum": [
          "a4_pdf",
          "10x19_pdf"
        ]
      },
      "enable_customs": {
        "type": "boolean",
        "default": false,
        "description": "Defines if order should use customs information from the associated item when creating shipments."
      },
      "use_item_weight": {
        "type": "boolean",
        "default": true,
        "description": "Defines if item weight should be used when creating shipments."
      },
      "assigned_staff_account_id": {
        "type": "integer",
        "default": null,
        "description": "ID of staff account assigned to order",
        "example": 12
      },
      "ship_to": {
        "required": [
          "address1",
          "city",
          "country_code",
          "name",
          "zipcode"
        ],
        "type": "object",
        "description": "Shipping address for the sales order. Used as address when creating shipments.",
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
          }
        }
      },
      "bill_to": {
        "required": [
          "address1",
          "city",
          "country_code",
          "name",
          "zipcode"
        ],
        "type": "object",
        "description": "Billing address for the sales order. Used when creating invoices for associated bookkeeping integration.",
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
          }
        }
      },
      "sender": {
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
      "payment_details": {
        "required": [
          "currency_code",
          "amount_including_vat",
          "vat_amount"
        ],
        "type": "object",
        "properties": {
          "amount_excluding_vat": {
            "type": "string",
            "example": "1600.0",
            "description": "Total price excluding taxes of the sales order."
          },
          "amount_including_vat": {
            "type": "string",
            "example": "2000.0",
            "description": "Total price including taxes of the sales order."
          },
          "authorized_amount": {
            "type": "string",
            "example": "2000.0",
            "description": "The amount authorized by the payment gateway."
          },
          "currency_code": {
            "type": "string",
            "example": "DKK",
            "description": "ISO 4217 currency code of the order total."
          },
          "vat_amount": {
            "type": "string",
            "example": "400.0",
            "description": "Total amount of taxes for the order."
          },
          "vat_percent": {
            "type": "string",
            "example": "0.25",
            "description": "Average tax percentage."
          },
          "payment_method": {
            "type": "string",
            "example": "quickpay",
            "description": "The method by which the order was paid."
          },
          "transaction_id": {
            "type": "string",
            "example": "123456789",
            "description": "Transaction ID of the payment as specified by the associated payment gateway."
          },
          "payment_gateway_id": {
            "type": "string",
            "example": "4012",
            "description": "ID of the provided payment gateway. Used to capture and void payments from Shipmondo."
          }
        }
      },
      "service_point": {
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
          },
          "carrier_code": {
            "type": "string",
            "example": "gls",
            "description": "Carrier code of the pickup point. Defines which carrier the pickup point belongs to."
          }
        }
      },
      "order_lines": {
        "type": "array",
        "description": "The order lines describe all the lines for the sales order, including items, shipping, and more.",
        "items": {
          "required": [
            "line_type",
            "item_name",
            "quantity",
            "currency_code"
          ],
          "type": "object",
          "properties": {
            "line_type": {
              "type": "string",
              "example": "item",
              "description": "Specifies the type of line.",
              "enum": [
                "item",
                "shipping",
                "discount",
                "gift_card",
                "payment_fee"
              ]
            },
            "item_name": {
              "type": "string",
              "example": "T-Shirt",
              "description": "Name of the item"
            },
            "item_sku": {
              "type": "string",
              "example": "TS001-WH",
              "description": "Stock keeping unit (SKU) of the item"
            },
            "item_variant_code": {
              "type": "string",
              "example": "White",
              "description": "Variant code of the item"
            },
            "quantity": {
              "type": "number",
              "example": 2.0,
              "description": "The quantity of the item in the order"
            },
            "unit_price_excluding_vat": {
              "type": "string",
              "example": "800.0",
              "description": "Price excluding taxes of a single item in the order line"
            },
            "discount_amount_excluding_vat": {
              "type": "string",
              "example": "0.0",
              "description": "Total discount of the items in the order line"
            },
            "vat_percent": {
              "type": "string",
              "example": "0.25",
              "description": "Tax percentage for the order line"
            },
            "currency_code": {
              "type": "string",
              "example": "DKK",
              "description": "ISO 4217 currency code"
            },
            "unit_weight": {
              "type": "integer",
              "example": 2000,
              "description": "The weight of a single item in the order line."
            },
            "item_barcode": {
              "type": "string",
              "example": "12345678",
              "description": "Barcode of the item. Used when scanning item for pick."
            },
            "item_bin": {
              "type": "string",
              "example": "AB-001",
              "description": "The bin/location where the item is located in the warehouse."
            },
            "image_url": {
              "type": "string",
              "example": "http://example.com/image",
              "description": "Image URL of the item that appears on the order or when picking. Will only be displayed if the URL is HTTPS."
            },
            "cost_price": {
              "type": "string",
              "example": "50.0",
              "description": "Unit cost price of the item as used for customs."
            },
            "country_code_of_origin": {
              "type": "string",
              "example": "DK",
              "description": "ISO 3166-1 alpha-2 country code of origin."
            },
            "customs_commodity_code": {
              "type": "string",
              "example": "123456",
              "description": "Tariff code for the item. Used when creating shipments that require customs declaration."
            },
            "customs_description": {
              "type": "string",
              "example": "Example contents",
              "description": "Customs description for the item. Used when creating shipments that require customs declaration."
            },
            "custom_product_data": {
              "description": "Custom product data for the order line.",
              "type": "array",
              "items": {
                "type": "string",
                "example": "Example text"
              }
            }
          }
        }
      },
      "carrier_fields": {
        "type": "object",
        "properties": {
          "sort_code": {
            "type": "string",
            "example": "SM123D",
            "description": "The sort code for Instabox."
          },
          "availability_token": {
            "type": "string",
            "example": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx",
            "description": "The availability token for Instabox."
          }
        }
      },
      "tags": {
        "type": "array",
        "description": "Custom tags for the order. Tags can be used to filter and search for orders.",
        "items": {
          "type": "string",
          "example": "tag1"
        }
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders"
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
    param_id: int = typer.Argument(None, help="ID for the sales order to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a sales order"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders get",
  "description": "Retrieve a sales order",
  "method": "GET",
  "endpoint": "/sales_orders/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}"
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
    param_id: int = typer.Argument(None, help="ID for the sales order that needs to be updated"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Update a sales order"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders update",
  "description": "Update a sales order",
  "method": "PUT",
  "endpoint": "/sales_orders/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order that needs to be updated"
    }
  },
  "payload_schema": {
    "type": "object",
    "properties": {
      "shipment_template_id": {
        "type": "integer",
        "example": 710,
        "description": "ID of the provided shipment template. Specifies the product and services for the order."
      },
      "return_shipment_template_id": {
        "type": "integer",
        "example": 710,
        "description": "ID of the provided return shipment template. Specifies the return product and services for the sales order."
      },
      "sales_order_packaging_id": {
        "type": "integer",
        "example": 11242,
        "description": "ID of the provided sales order packaging. The packaging specifies the dimensions for the sales order."
      },
      "order_status": {
        "type": "string",
        "example": "open",
        "description": "The status of the order in Shipmondo. Possible values: open, cancelled, on-hold"
      },
      "enable_customs": {
        "type": "boolean",
        "default": false,
        "description": "Defines if order should use customs information from the associated item when creating shipments."
      },
      "use_item_weight": {
        "type": "boolean",
        "default": true,
        "description": "Defines if item weight should be used when creating shipments."
      },
      "assigned_staff_account_id": {
        "type": "integer",
        "default": null,
        "description": "ID of staff account assigned to order",
        "example": 12
      },
      "ship_to": {
        "required": [
          "address1",
          "city",
          "country_code",
          "name",
          "zipcode"
        ],
        "type": "object",
        "description": "Shipping address for the sales order. Used as address when creating shipments.",
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
          }
        }
      },
      "bill_to": {
        "required": [
          "address1",
          "city",
          "country_code",
          "name",
          "zipcode"
        ],
        "type": "object",
        "description": "Billing address for the sales order. Used when creating invoices for associated bookkeeping integration.",
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
          }
        }
      },
      "sender": {
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
      "service_point": {
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
      "order_lines": {
        "type": "array",
        "description": "Order lines for the order. If an order line ID is provided, it will update the existing line, otherwise a new line will be created. To remove an existing line, set the quantity to 0 when updating. Below are only updatable properties, see POST /sales_orders for create new order_line properties.",
        "items": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer",
              "example": 1234,
              "description": "Unique identifier of the object. Used for identifying the specific line when updating order lines."
            },
            "quantity": {
              "type": "number",
              "example": 2.0,
              "description": "The quantity of the item in the order"
            },
            "unit_price_excluding_vat": {
              "type": "string",
              "example": "800.0",
              "description": "Price excluding taxes of a single item in the order line"
            },
            "vat_percent": {
              "type": "string",
              "example": "0.25",
              "description": "Tax percentage for the order line"
            },
            "unit_weight": {
              "type": "integer",
              "example": 2000,
              "description": "The weight of a single item in the order line."
            },
            "custom_product_data": {
              "description": "Custom product data for the order line.",
              "type": "array",
              "items": {
                "type": "string",
                "example": "Example text"
              }
            }
          }
        }
      },
      "carrier_fields": {
        "type": "object",
        "properties": {
          "sort_code": {
            "type": "string",
            "example": "SM123D",
            "description": "The sort code for Instabox."
          },
          "availability_token": {
            "type": "string",
            "example": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx",
            "description": "The availability token for Instabox."
          }
        }
      }
    }
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}"
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
    param_id: int = typer.Argument(None, help="ID for the sales order that needs to be deleted"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Delete a sales order"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders delete",
  "description": "Delete a sales order",
  "method": "DELETE",
  "endpoint": "/sales_orders/{id}",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order that needs to be deleted"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}"
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

@app.command("put_order_note")
def put_order_note_cmd(
    param_id: int = typer.Argument(None, help="ID for the sales order that note should be updated for"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Update a sales order note"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders put_order_note",
  "description": "Update a sales order note",
  "method": "PUT",
  "endpoint": "/sales_orders/{id}/order_note",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order that note should be updated for"
    }
  },
  "payload_schema": {
    "type": "object",
    "properties": {
      "order_note": {
        "type": "string",
        "example": "Note",
        "description": "A note for the sales order."
      }
    }
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/order_note"
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

@app.command("create_shipment")
def create_shipment_cmd(
    param_id: int = typer.Argument(None, help="ID of the sales order to create a shipment for"),
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
  "command": "shipmondo sales_orders create_shipment",
  "description": "Create a shipment",
  "method": "POST",
  "endpoint": "/sales_orders/{id}/create_shipment",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the sales order to create a shipment for"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/create_shipment"
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

@app.command("capture")
def capture_cmd(
    param_id: int = typer.Argument(None, help="ID for the sales order that needs to be captured"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Capture payment"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders capture",
  "description": "Capture payment",
  "method": "POST",
  "endpoint": "/sales_orders/{id}/capture",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order that needs to be captured"
    }
  },
  "payload_schema": {
    "type": "object",
    "properties": {
      "amount": {
        "type": "string",
        "example": "200.00",
        "description": "Amount to be captured. \nUnless specified, the authorized amount for the transaction associated with the order will be captured."
      }
    }
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/capture"
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

@app.command("refund")
def refund_cmd(
    param_id: int = typer.Argument(None, help="ID of the sales order that you wish to refund"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Refund payment"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders refund",
  "description": "Refund payment",
  "method": "POST",
  "endpoint": "/sales_orders/{id}/refund",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the sales order that you wish to refund"
    }
  },
  "payload_schema": {
    "type": "object",
    "properties": {
      "amount": {
        "type": [
          "string",
          "null"
        ],
        "nullable": true,
        "example": "200.00",
        "description": "Amount to be refunded. \nIf not specified the captured amount for the transaction associated with the order will be refunded."
      }
    }
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/refund"
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

@app.command("void")
def void_cmd(
    param_id: int = typer.Argument(None, help="ID of the sales order that you wish to void"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Void payment"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders void",
  "description": "Void payment",
  "method": "POST",
  "endpoint": "/sales_orders/{id}/void",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID of the sales order that you wish to void"
    }
  },
  "payload_schema": {
    "type": "object",
    "properties": {
      "amount": {
        "type": [
          "string",
          "null"
        ],
        "nullable": true,
        "example": "200.00",
        "description": "Amount to be voided. \nIf not specified the uncaptured amount for the transaction associated with the order will be voided."
      }
    }
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/void"
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

@app.command("barcode")
def barcode_cmd(
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Process a barcode"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders barcode",
  "description": "Process a barcode",
  "method": "POST",
  "endpoint": "/sales_orders/barcode",
  "parameters": {},
  "payload_schema": {
    "type": "object",
    "properties": {
      "barcode": {
        "type": "string",
        "example": "QB000000027000",
        "description": "The barcode is a 14-character string, prefixed with 'QB'. It contains the ID of the sales order, and extended to 14 characters with zeroes."
      }
    }
  }
}""")
        raise typer.Exit()

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/barcode"
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

@app.command("pick_list")
def pick_list_cmd(
    param_id: int = typer.Argument(None, help="ID for the sales order to be included in the filter"),
    param_format: str = typer.Option(None, "--format", help="Format for the pick list. Available: a4_pdf, 10x19_pdf "),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a pick list"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders pick_list",
  "description": "Retrieve a pick list",
  "method": "GET",
  "endpoint": "/sales_orders/{id}/pick_list",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order to be included in the filter"
    },
    "format": {
      "cli_flag": "--format",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Format for the pick list. Available: a4_pdf, 10x19_pdf "
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/pick_list"
    url_params = {}
    if param_format is not None:
        url_params["format"] = param_format
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

@app.command("packing_slips")
def packing_slips_cmd(
    param_id: int = typer.Argument(None, help="ID for the sales order to be included in the filter"),
    param_format: str = typer.Option(None, "--format", help="Format for the packing slip. Available: a4_pdf, 10x19_pdf "),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Retrieve a packing slip"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders packing_slips",
  "description": "Retrieve a packing slip",
  "method": "GET",
  "endpoint": "/sales_orders/{id}/packing_slips",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order to be included in the filter"
    },
    "format": {
      "cli_flag": "--format",
      "location": "query",
      "type": "str",
      "required": false,
      "description": "Format for the packing slip. Available: a4_pdf, 10x19_pdf "
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/packing_slips"
    url_params = {}
    if param_format is not None:
        url_params["format"] = param_format
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

@app.command("fulfillments")
def fulfillments_cmd(
    param_id: int = typer.Argument(None, help="ID for the sales order to be included in the filter"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """List fulfillments"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders fulfillments",
  "description": "List fulfillments",
  "method": "GET",
  "endpoint": "/sales_orders/{id}/fulfillments",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order to be included in the filter"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/fulfillments"
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

@app.command("fulfillments")
def fulfillments_cmd(
    param_id: int = typer.Argument(None, help="ID for the sales order to be included in the filter"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Create a fulfillment"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders fulfillments",
  "description": "Create a fulfillment",
  "method": "POST",
  "endpoint": "/sales_orders/{id}/fulfillments",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order to be included in the filter"
    }
  },
  "payload_schema": {
    "required": [
      "fulfillment_lines",
      "order_line_id",
      "shipped_quantity"
    ],
    "type": "object",
    "properties": {
      "fulfilled_by_third_party": {
        "type": "boolean",
        "default": false,
        "description": "Defines if fulfillment is fulfilled by a third party."
      },
      "order_packaging_id": {
        "type": "integer",
        "example": 16,
        "description": "ID of a desired order_packaging. Specifies which order packaging to use."
      },
      "fulfillment_lines": {
        "type": "array",
        "description": "Lines to be fulfilled for the sales_order.",
        "items": {
          "required": [
            "order_line_id",
            "shipped_quantity"
          ],
          "type": "object",
          "properties": {
            "order_line_id": {
              "type": "integer",
              "example": 45891,
              "description": "The id of the order_line you wish to fulfill. It has to be associated with the sales_order."
            },
            "shipped_quantity": {
              "type": "string",
              "example": "1.0",
              "description": "The quantity of items you wish to ship. Total shipped quantity must not be higher than the quantity of items for the order line."
            }
          }
        }
      }
    }
  }
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/fulfillments"
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

@app.command("mark_as_paid")
def mark_as_paid_cmd(
    param_id: int = typer.Argument(None, help="ID for the sales order that needs to be marked as paid"),
    payload: str = typer.Option(None, "--data", help="JSON payload string"),
    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),
    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),
    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),
    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),
    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")
):
    """Mark as paid"""
    if help_json:
        print("""{
  "command": "shipmondo sales_orders mark_as_paid",
  "description": "Mark as paid",
  "method": "POST",
  "endpoint": "/sales_orders/{id}/mark_as_paid",
  "parameters": {
    "id": {
      "cli_flag": "Positional Argument",
      "location": "path",
      "type": "int",
      "required": true,
      "description": "ID for the sales order that needs to be marked as paid"
    }
  },
  "payload_schema": null
}""")
        raise typer.Exit()

    if param_id is None:
        print(json.dumps({"error": "Missing required Argument 'id'"}), file=sys.stderr)
        raise typer.Exit(1)

    client = ShipmondoClient(debug=debug)
    endpoint = f"/sales_orders/{param_id}/mark_as_paid"
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

