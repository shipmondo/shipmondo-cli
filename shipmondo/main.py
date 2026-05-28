import typer
import json
import os
import subprocess
import sys
from shipmondo.commands import account
from shipmondo.commands import bookkeeping_integrations
from shipmondo.commands import waybills
from shipmondo.commands import carriers
from shipmondo.commands import products
from shipmondo.commands import package_types
from shipmondo.commands import documents
from shipmondo.commands import items
from shipmondo.commands import shipments
from shipmondo.commands import labels
from shipmondo.commands import payment_gateways
from shipmondo.commands import pickup_requests
from shipmondo.commands import printers
from shipmondo.commands import print_jobs
from shipmondo.commands import quotes
from shipmondo.commands import return_portals
from shipmondo.commands import sales_orders
from shipmondo.commands import pick_lists
from shipmondo.commands import packing_slips
from shipmondo.commands import sales_order_packagings
from shipmondo.commands import fulfillments
from shipmondo.commands import pickup_points
from shipmondo.commands import service_point
from shipmondo.commands import shipping_modules
from shipmondo.commands import shipment_templates
from shipmondo.commands import shipment_drafts
from shipmondo.commands import staff_accounts
from shipmondo.commands import setups
from shipmondo.commands import webhooks
from shipmondo.commands import setup

app = typer.Typer(name='shipmondo', help='Agent-native Discovery-Enabled Shipmondo CLI', no_args_is_help=True)

@app.command("update")
def update_cli():
    """Updates the Shipmondo CLI to the latest version from GitHub."""
    print("🔄 Pulling the latest version from GitHub...")
    try:
        subprocess.run(["pipx", "install", "git+https://github.com/shipmondo/shipmondo-cli.git", "--force"], check=True, capture_output=True, text=True)
        print("✅ Shipmondo CLI successfully updated!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update. Pipx error:\n{e.stderr}", file=sys.stderr)
        raise typer.Exit(1)
    except FileNotFoundError:
        print("❌ 'pipx' command not found. Please ensure pipx is installed.", file=sys.stderr)
        raise typer.Exit(1)

@app.command("commands")
def list_all_commands(json_output: bool = typer.Option(True, "--json", help="Force JSON catalog output")):
    """Returns a complete machine-readable list of all available subcommands."""
    print("""{
  "account": [
    {
      "command": "get",
      "description": "Retrieve account infomation",
      "method": "GET",
      "endpoint": "/account/"
    },
    {
      "command": "balance",
      "description": "Retrieve balance",
      "method": "GET",
      "endpoint": "/account/balance"
    },
    {
      "command": "payment_requests",
      "description": "List all payment requests",
      "method": "GET",
      "endpoint": "/account/payment_requests"
    }
  ],
  "bookkeeping_integrations": [
    {
      "command": "list",
      "description": "List all bookkeeping integrations",
      "method": "GET",
      "endpoint": "/bookkeeping_integrations"
    },
    {
      "command": "get",
      "description": "Retrieve a bookkeeping integration",
      "method": "GET",
      "endpoint": "/bookkeeping_integrations/{id}"
    }
  ],
  "waybills": [
    {
      "command": "list",
      "description": "List all bulk waybills",
      "method": "GET",
      "endpoint": "/waybills"
    },
    {
      "command": "create",
      "description": "Create a bulk waybill",
      "method": "POST",
      "endpoint": "/waybills"
    },
    {
      "command": "get",
      "description": "Retrieve a bulk waybill",
      "method": "GET",
      "endpoint": "/waybills/{id}"
    },
    {
      "command": "put_close",
      "description": "Close an open bulk waybill",
      "method": "PUT",
      "endpoint": "/waybills/{id}/close"
    },
    {
      "command": "load_carriers",
      "description": "Creates and adds a new load carrier to the bulk waybill",
      "method": "POST",
      "endpoint": "/waybills/{waybill_id}/load_carriers"
    },
    {
      "command": "load_carriers",
      "description": "List all load carriers",
      "method": "GET",
      "endpoint": "/waybills/{waybill_id}/load_carriers"
    },
    {
      "command": "load_carriers",
      "description": "Retrieve a load carrier",
      "method": "GET",
      "endpoint": "/waybills/{waybill_id}/load_carriers/{id}"
    }
  ],
  "carriers": [
    {
      "command": "list",
      "description": "List available carriers",
      "method": "GET",
      "endpoint": "/carriers"
    }
  ],
  "products": [
    {
      "command": "list",
      "description": "List all products",
      "method": "GET",
      "endpoint": "/products"
    }
  ],
  "package_types": [
    {
      "command": "list",
      "description": "List all package types",
      "method": "GET",
      "endpoint": "/package_types"
    }
  ],
  "documents": [
    {
      "command": "end_of_day",
      "description": "Retrieve an End of Day list",
      "method": "GET",
      "endpoint": "/documents/end_of_day"
    },
    {
      "command": "waybill",
      "description": "Retrieve a waybill",
      "method": "GET",
      "endpoint": "/documents/waybill"
    }
  ],
  "items": [
    {
      "command": "list",
      "description": "List all items",
      "method": "GET",
      "endpoint": "/items"
    },
    {
      "command": "create",
      "description": "Create an item",
      "method": "POST",
      "endpoint": "/items"
    },
    {
      "command": "get",
      "description": "Retrieve an item",
      "method": "GET",
      "endpoint": "/items/{id}"
    },
    {
      "command": "update",
      "description": "Update an item",
      "method": "PUT",
      "endpoint": "/items/{id}"
    }
  ],
  "shipments": [
    {
      "command": "labels",
      "description": "Retrieve labels of a shipment",
      "method": "GET",
      "endpoint": "/shipments/{id}/labels"
    },
    {
      "command": "list",
      "description": "List all shipments",
      "method": "GET",
      "endpoint": "/shipments"
    },
    {
      "command": "create",
      "description": "Create a shipment",
      "method": "POST",
      "endpoint": "/shipments"
    },
    {
      "command": "get",
      "description": "Retrieve a shipment",
      "method": "GET",
      "endpoint": "/shipments/{id}"
    },
    {
      "command": "put_cancel",
      "description": "Cancel a shipment",
      "method": "PUT",
      "endpoint": "/shipments/{id}/cancel"
    },
    {
      "command": "proforma_invoices",
      "description": "Retrieve a proforma invoice",
      "method": "GET",
      "endpoint": "/shipments/{id}/proforma_invoices"
    },
    {
      "command": "waybills",
      "description": "Retrieve waybill for a shipment",
      "method": "GET",
      "endpoint": "/shipments/{id}/waybills"
    },
    {
      "command": "quote",
      "description": "Create a shipment quote",
      "method": "POST",
      "endpoint": "/shipments/quote"
    },
    {
      "command": "qr_code",
      "description": "Fetch QR codes for a shipment",
      "method": "GET",
      "endpoint": "/shipments/{id}/qr_code"
    }
  ],
  "labels": [
    {
      "command": "list",
      "description": "Retrieve labels for multiple shipments",
      "method": "GET",
      "endpoint": "/labels"
    }
  ],
  "payment_gateways": [
    {
      "command": "list",
      "description": "List all payment gateways",
      "method": "GET",
      "endpoint": "/payment_gateways"
    },
    {
      "command": "get",
      "description": "Retrieve a payment gateway",
      "method": "GET",
      "endpoint": "/payment_gateways/{id}"
    }
  ],
  "pickup_requests": [
    {
      "command": "list",
      "description": "List all pickup requests",
      "method": "GET",
      "endpoint": "/pickup_requests"
    },
    {
      "command": "create",
      "description": "Create a pickup request",
      "method": "POST",
      "endpoint": "/pickup_requests"
    },
    {
      "command": "get",
      "description": "Retrieve a pickup request",
      "method": "GET",
      "endpoint": "/pickup_requests/{id}"
    }
  ],
  "printers": [
    {
      "command": "list",
      "description": "List all printers",
      "method": "GET",
      "endpoint": "/printers"
    }
  ],
  "print_jobs": [
    {
      "command": "create",
      "description": "Create a print job",
      "method": "POST",
      "endpoint": "/print_jobs"
    },
    {
      "command": "batch",
      "description": "Create a print job batch",
      "method": "POST",
      "endpoint": "/print_jobs/batch"
    }
  ],
  "quotes": [
    {
      "command": "create",
      "description": "Create a shipment quote",
      "method": "POST",
      "endpoint": "/quotes"
    },
    {
      "command": "list",
      "description": "List available quotes for a shipment",
      "method": "POST",
      "endpoint": "/quotes/list"
    }
  ],
  "return_portals": [
    {
      "command": "list",
      "description": "List all return portals",
      "method": "GET",
      "endpoint": "/return_portals"
    },
    {
      "command": "get",
      "description": "Retrieve a return portal",
      "method": "GET",
      "endpoint": "/return_portals/{id}"
    },
    {
      "command": "shipments",
      "description": "List all shipments for a return portal",
      "method": "GET",
      "endpoint": "/return_portals/{id}/shipments"
    }
  ],
  "sales_orders": [
    {
      "command": "list",
      "description": "List all sales orders",
      "method": "GET",
      "endpoint": "/sales_orders"
    },
    {
      "command": "create",
      "description": "Create a sales order",
      "method": "POST",
      "endpoint": "/sales_orders"
    },
    {
      "command": "get",
      "description": "Retrieve a sales order",
      "method": "GET",
      "endpoint": "/sales_orders/{id}"
    },
    {
      "command": "update",
      "description": "Update a sales order",
      "method": "PUT",
      "endpoint": "/sales_orders/{id}"
    },
    {
      "command": "delete",
      "description": "Delete a sales order",
      "method": "DELETE",
      "endpoint": "/sales_orders/{id}"
    },
    {
      "command": "put_order_note",
      "description": "Update a sales order note",
      "method": "PUT",
      "endpoint": "/sales_orders/{id}/order_note"
    },
    {
      "command": "create_shipment",
      "description": "Create a shipment",
      "method": "POST",
      "endpoint": "/sales_orders/{id}/create_shipment"
    },
    {
      "command": "capture",
      "description": "Capture payment",
      "method": "POST",
      "endpoint": "/sales_orders/{id}/capture"
    },
    {
      "command": "refund",
      "description": "Refund payment",
      "method": "POST",
      "endpoint": "/sales_orders/{id}/refund"
    },
    {
      "command": "void",
      "description": "Void payment",
      "method": "POST",
      "endpoint": "/sales_orders/{id}/void"
    },
    {
      "command": "barcode",
      "description": "Process a barcode",
      "method": "POST",
      "endpoint": "/sales_orders/barcode"
    },
    {
      "command": "pick_list",
      "description": "Retrieve a pick list",
      "method": "GET",
      "endpoint": "/sales_orders/{id}/pick_list"
    },
    {
      "command": "packing_slips",
      "description": "Retrieve a packing slip",
      "method": "GET",
      "endpoint": "/sales_orders/{id}/packing_slips"
    },
    {
      "command": "fulfillments",
      "description": "List fulfillments",
      "method": "GET",
      "endpoint": "/sales_orders/{id}/fulfillments"
    },
    {
      "command": "fulfillments",
      "description": "Create a fulfillment",
      "method": "POST",
      "endpoint": "/sales_orders/{id}/fulfillments"
    },
    {
      "command": "mark_as_paid",
      "description": "Mark as paid",
      "method": "POST",
      "endpoint": "/sales_orders/{id}/mark_as_paid"
    }
  ],
  "pick_lists": [
    {
      "command": "list",
      "description": "Retrieve pick lists",
      "method": "GET",
      "endpoint": "/pick_lists"
    }
  ],
  "packing_slips": [
    {
      "command": "list",
      "description": "Retrieve packing slips",
      "method": "GET",
      "endpoint": "/packing_slips"
    }
  ],
  "sales_order_packagings": [
    {
      "command": "list",
      "description": "List all packagings",
      "method": "GET",
      "endpoint": "/sales_order_packagings"
    },
    {
      "command": "get",
      "description": "Retrieve a packaging",
      "method": "GET",
      "endpoint": "/sales_order_packagings/{id}"
    }
  ],
  "fulfillments": [
    {
      "command": "get",
      "description": "Retrieve a fulfillment",
      "method": "GET",
      "endpoint": "/fulfillments/{id}"
    },
    {
      "command": "create_shipment",
      "description": "Create a shipment for a fulfillment",
      "method": "POST",
      "endpoint": "/fulfillments/{id}/create_shipment"
    }
  ],
  "pickup_points": [
    {
      "command": "list",
      "description": "List pickup points",
      "method": "GET",
      "endpoint": "/pickup_points"
    }
  ],
  "service_point": [
    {
      "command": "service_points",
      "description": "Get service points based on product.",
      "method": "GET",
      "endpoint": "/service_point/service_points"
    },
    {
      "command": "service_point_types",
      "description": "Get valid service point types",
      "method": "GET",
      "endpoint": "/service_point/service_point_types"
    }
  ],
  "shipping_modules": [
    {
      "command": "carriers",
      "description": "Get carriers",
      "method": "GET",
      "endpoint": "/shipping_modules/carriers"
    },
    {
      "command": "products",
      "description": "Get valid products",
      "method": "GET",
      "endpoint": "/shipping_modules/products"
    },
    {
      "command": "shopify_shipping_methods",
      "description": "Get Shopify shipping method",
      "method": "GET",
      "endpoint": "/shipping_modules/shopify/shipping_methods/{id}"
    }
  ],
  "shipment_templates": [
    {
      "command": "list",
      "description": "List all shipment templates",
      "method": "GET",
      "endpoint": "/shipment_templates"
    },
    {
      "command": "get",
      "description": "Retrieve a shipment template",
      "method": "GET",
      "endpoint": "/shipment_templates/{id}"
    }
  ],
  "shipment_drafts": [
    {
      "command": "list",
      "description": "List all shipment drafts",
      "method": "GET",
      "endpoint": "/shipment_drafts"
    },
    {
      "command": "create",
      "description": "Create a shipment draft",
      "method": "POST",
      "endpoint": "/shipment_drafts"
    },
    {
      "command": "get",
      "description": "Retrieve a shipment draft",
      "method": "GET",
      "endpoint": "/shipment_drafts/{id}"
    },
    {
      "command": "update",
      "description": "Update a shipment draft",
      "method": "PUT",
      "endpoint": "/shipment_drafts/{id}"
    },
    {
      "command": "delete",
      "description": "Delete a shipment draft",
      "method": "DELETE",
      "endpoint": "/shipment_drafts/{id}"
    }
  ],
  "staff_accounts": [
    {
      "command": "list",
      "description": "List all staff accounts",
      "method": "GET",
      "endpoint": "/staff_accounts"
    },
    {
      "command": "get",
      "description": "Retrieve a single staff account",
      "method": "GET",
      "endpoint": "/staff_accounts/{id}"
    }
  ],
  "setups": [
    {
      "command": "carriers",
      "description": "Request Carrier setup file",
      "method": "GET",
      "endpoint": "/setups/carriers"
    }
  ],
  "webhooks": [
    {
      "command": "list",
      "description": "List all webhooks",
      "method": "GET",
      "endpoint": "/webhooks"
    },
    {
      "command": "create",
      "description": "Create a webhook",
      "method": "POST",
      "endpoint": "/webhooks"
    },
    {
      "command": "get",
      "description": "Retrieve a webhook",
      "method": "GET",
      "endpoint": "/webhooks/{id}"
    },
    {
      "command": "update",
      "description": "Update a webhook",
      "method": "PUT",
      "endpoint": "/webhooks/{id}"
    },
    {
      "command": "delete",
      "description": "Delete a webhook",
      "method": "DELETE",
      "endpoint": "/webhooks/{id}"
    }
  ]
}""")

@app.command("openapi")
def print_openapi_spec(json_output: bool = typer.Option(True, "--json", help="Dump raw openapi spec")):
    """Exposes the raw foundational OpenAPI schema to the client agent context."""
    if os.path.exists("openapi.json"):
        with open("openapi.json", "r") as openapi_file:
            print(json.dumps(json.load(openapi_file)))
    else:
        print('{"error": "openapi.json layout file missing from compilation path"}')

app.add_typer(account.app, name="account")
app.add_typer(bookkeeping_integrations.app, name="bookkeeping_integrations")
app.add_typer(waybills.app, name="waybills")
app.add_typer(carriers.app, name="carriers")
app.add_typer(products.app, name="products")
app.add_typer(package_types.app, name="package_types")
app.add_typer(documents.app, name="documents")
app.add_typer(items.app, name="items")
app.add_typer(shipments.app, name="shipments")
app.add_typer(labels.app, name="labels")
app.add_typer(payment_gateways.app, name="payment_gateways")
app.add_typer(pickup_requests.app, name="pickup_requests")
app.add_typer(printers.app, name="printers")
app.add_typer(print_jobs.app, name="print_jobs")
app.add_typer(quotes.app, name="quotes")
app.add_typer(return_portals.app, name="return_portals")
app.add_typer(sales_orders.app, name="sales_orders")
app.add_typer(pick_lists.app, name="pick_lists")
app.add_typer(packing_slips.app, name="packing_slips")
app.add_typer(sales_order_packagings.app, name="sales_order_packagings")
app.add_typer(fulfillments.app, name="fulfillments")
app.add_typer(pickup_points.app, name="pickup_points")
app.add_typer(service_point.app, name="service_point")
app.add_typer(shipping_modules.app, name="shipping_modules")
app.add_typer(shipment_templates.app, name="shipment_templates")
app.add_typer(shipment_drafts.app, name="shipment_drafts")
app.add_typer(staff_accounts.app, name="staff_accounts")
app.add_typer(setups.app, name="setups")
app.add_typer(webhooks.app, name="webhooks")
app.add_typer(setup.app, name="setup")

if __name__ == '__main__':
    app()
