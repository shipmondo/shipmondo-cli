import typer
from pathlib import Path

app = typer.Typer(help="CLI AI agent integration and setup")

skill_content = """---
name: shipmondo
description: Interact with the Shipmondo API to manage shipments, drafts, carriers, and orders via the shipmondo Python CLI.
---

# Shipmondo CLI Agent Skill

You are an expert at interacting with the Shipmondo API via the `shipmondo` Python CLI.
...

## Environment Setup
Before executing any commands, you must configure authentication in your terminal environment:
```bash
export SHIPMONDO_API_USER="your_user"
export SHIPMONDO_API_KEY="your_key"
```

## Self-Discovery & Introspection (CRITICAL)
You do not need to guess parameters, endpoints, or schemas. The CLI is entirely self-describing. When you are unsure how to perform an action, follow this discovery loop:
1. **List all available commands:** Run `shipmondo commands --json` to get a catalog of every available resource and action.
2. **Inspect a specific command:** Run `shipmondo [RESOURCE] [ACTION] --help-json` to view the exact machine-readable schema for that command. 
   - *Example:* `shipmondo carriers list --help-json`
   - This output will explicitly define all required positional arguments, explicit CLI flags (like `--receiver-country-code`), and the exact JSON payload schema required for the `--data` flag.

## Core Execution Syntax
Run actions using direct shell command execution: `shipmondo [RESOURCE] [ACTION] [OPTIONS]`
* **Always use JSON**: Append the `--json` flag to every command to ensure you receive raw data instead of human-readable text.
* **Query & Path Parameters**: Simple parameters are mapped to explicit kebab-case CLI flags. (e.g., `--page 1`, `--receiver-country-code DK`). Do not pass these inside the JSON payload.
* **Complex Data Payloads**: For `POST`, `PUT`, or `PATCH` requests (like creating a shipment), pass the highly nested JSON payload as a string using the `--data` flag.
  - *Example:* `shipmondo webhooks create --data '{"endpoint": "https://example.com", "key": "secret", "action": "shipment.create"}' --json`

## 4. CRITICAL: Creating Shipments (Domain Rule)
The Shipmondo API uses a modernized `parties` array for assigning various parties to a  shipment. You must **NEVER** use the deprecated `sender` or `receiver` root objects in your JSON payload. 
* Instead, pass an array of objects under the `parties` key, specifying the `"type"` (e.g., `"sender"`, `"receiver"`, `"pickup_point"`). 
* *Example Payload Segment:* `{"parties": [{"type": "sender", "name": "Sender Inc", "address1": "Main St 1"}, {"type": "receiver", "name": "John Doe", "address1": "Elm St 2"}]}`

## 5. Pagination and Reading Lists
When you run a standard collection `list` command, the CLI automatically wraps the API response in a paginated structure:
```json
{
  "data": [ ... ],
  "meta": { 
    "current_page": 1, 
    "per_page": 20, 
    "total_count": 150, 
    "total_pages": 8 
  }
}
```
* **Use Pagination Flags:** Control your context window by using the `--page` and `--per-page` flags. Never exceed `--per-page 50`.
* **Traversing:** Check `meta.total_pages` to determine if you need to execute the command again with a higher `--page` number.

## Token Efficiency
Shipmondo payloads can be massive. If you only need specific fields (like finding a specific ID or status), pipe the output through `jq` to filter the data before reading it into your context window.
* *Example:* `shipmondo sales_orders list --json | jq '.data[].id'`

## Error Handling & Debugging
* **Validation Errors:** If you miss a required parameter or pass an invalid payload, the CLI will terminate with an exit code of `1` and output a JSON error to standard error (`stderr`). Read this error carefully to self-correct your payload.
* **Network Debugging:** If you suspect an API mismatch, append the `--debug` flag to your command. This will print the raw outgoing HTTP request (URL, Headers, JSON) and the raw incoming HTTP response directly to `stderr` for your inspection.

## Carrier & Product Discovery Flow

When assisting a user with a booking, you must determine the correct `product_code` (and optional services). 
* **Hierarchy:** A Carrier has many Products. A Product has many Services.
* **Booking Rule:** You only need to submit the `product_code` (the API automatically infers the carrier). Adding services might require extra payload fields; if you miss any, the API will return a descriptive error. Follow the API's error instructions to correct the payload.

### Discovery Protocol
Before drafting a shipment payload, check if the user already knows their `product_code`. 
* **IF YES:** Proceed directly to the booking phase.
* **IF NO:** Execute the following discovery steps.

**Step 1: Identify the Routing**
Ask the user for the sender and receiver country codes if they haven't provided them. 

**Step 2: Fetch Available Carriers**
Run the carrier list command using the routing parameters:
`shipmondo carriers list --sender-country-code <sender_country_code> --receiver-country-code <receiver_country_code>`
Present the available carriers to the user and ask which one they prefer.

**Step 3: Fetch Carrier Products (WARNING: VERBOSE OUTPUT)**  
Once you have the `carrier_code` from Step 2, fetch the products. 
*CRITICAL:* The products endpoint returns massive amounts of JSON. You must pipe the output through `jq` to extract only the `code` and `name` to prevent context window overflow.
Example:
`shipmondo products list --carrier-code gls | jq '[.[] | {code: .code, name: .name}]'`

Present this filtered list to the user to make their final selection before building the shipment payload.

## Resource Mapping & Guardrails

To prevent semantic confusion, map user-facing business terminology to the precise CLI resource domains below.

### Drafts vs. Orders vs. Templates
Users may use overlapping terms when discussing shipments, orders, or templates. You must route their requests to the correct subsystem:

* **Shipment Drafts:** When a user asks for "drafts" or "shipment drafts", interact strictly with the `shipmondo shipment_drafts` namespace.
* **Sales Orders:** When a user asks about "orders", "sales orders", or "customer orders", interact strictly with the `shipmondo sales_orders` namespace.
* **Shipment Templates (CRITICAL GUARDRAIL):** The `shipmondo shipment_templates` namespace is reserved for high-level administration of shipping presets. Messing with templates can heavily disrupt automated fulfillment logic. **You must NEVER create, modify, or delete shipment templates.** If a user requests a template modification, politely explain that they must manage templates manually through the Shipmondo Web Dashboard for safety reasons.

### File & Label Presentation
When a user asks to "see", "view" or "open" a shipping label, commercial invoice, or tracking document, do not just return the raw text or base64 JSON payload. 

* Use the global `--open-pdf` flag on the fetching command. 
* This tells the CLI engine to automatically intercept the base64 string, write it to a local temporary file, and trigger the system's native PDF viewer for the human user immediately.
* If this approach fails, try to manually decode the base64 string and write it to a file, then open it with a system command.

Example:
`shipmondo labels get 12345 --open-pdf`

## Service Points
When a shipment requires delivery to a service point (drop point/parcel shop), it must be defined correctly within the parties array.
* **The Correct Type:** You MUST use `"type": "service_point"`. 

**Correct Example:**
```json
{
  "parties": [
    {
      "type": "service_point",
      "service_point_id": "9743"
    }
  ]
}

```

## Service Point vs. Pickup (CRITICAL DISTINCTION)
You must understand the strict difference between a **Service Point** and a **Pickup** in the Shipmondo ecosystem. Do not confuse or combine these terms.

* **Service Point (Drop Point / Parcel Shop):** 
  * This is a location (drop point/parcel shop) where the *receiver* goes to collect their parcel, or where the *sender* goes to drop it off.
  * **Implementation:** This is defined inside the `parties` array using `"type": "service_point"`.

* **Pickup (Carrier Collection):** 
  * This is when the *carrier* is requested to drive to the *sender's address* to collect the parcels directly.

### The `quotes create` Exception
While the majority of Shipmondo booking endpoints (like shipment drafts and sales orders) require you to pass addresses via the `parties` array, the **Quotes** endpoint is a strict exception.

* When executing `shipmondo quotes create`, you **MUST NOT** use the `parties` array.
* You must use the traditional `sender` and `receiver` objects directly at the root level of the payload.

**Correct Quotes Example:**

```json
{
  "sender": {
    "country_code": "DK",
    "zipcode": "5000"
  },
  "receiver": {
    "country_code": "DK",
    "zipcode": "8000"
  }
}"""

@app.command("claude")
def setup_claude(
    global_install: bool = typer.Option(True, "--global/--local", help="Install globally or for this directory only")
):
    """Install the Shipmondo Agent Skill into Claude Code."""
    if global_install:
        target_dir = Path.home() / ".claude" / "skills" / "shipmondo"
    else:
        target_dir = Path.cwd() / ".claude" / "skills" / "shipmondo"
        
    target_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = target_dir / "SKILL.md"
    skill_file.write_text(skill_content.strip())
        
    typer.echo(f"✅ Shipmondo skill successfully installed to: {skill_file}")
    typer.echo("Claude Code will automatically load these instructions when invoked.")

@app.command("copilot")
def setup_copilot(
    global_install: bool = typer.Option(True, "--global/--local", help="Install globally or for this directory only")
):
    """Install the Shipmondo Agent Skill into GitHub Copilot (VS Code)."""
    if global_install:
        target_dir = Path.home() / ".copilot" / "skills" / "shipmondo"
    else:
        target_dir = Path.cwd() / ".github" / "skills" / "shipmondo"
        
    target_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = target_dir / "SKILL.md"
    skill_file.write_text(skill_content.strip())
        
    typer.echo(f"✅ Shipmondo skill successfully installed to: {skill_file}")
    typer.echo("GitHub Copilot will automatically load these instructions when relevant.")

@app.command("cursor")
def setup_cursor():
    """Install the Shipmondo Agent Skill into Cursor IDE."""
    target_dir = Path.cwd() / ".cursor" / "skills" / "shipmondo"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = target_dir / "SKILL.md"
    skill_file.write_text(skill_content.strip())
    
    typer.echo(f"✅ Shipmondo skill successfully installed to: {skill_file}")
    typer.echo("Cursor's agent will dynamically load these instructions when relevant.")
        
@app.command("windsurf")
def setup_windsurf():
    """Install the Shipmondo Agent Skill into Windsurf IDE."""
    target_dir = Path.cwd() / ".windsurf" / "skills" / "shipmondo"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = target_dir / "SKILL.md"
    skill_file.write_text(skill_content.strip())
    
    typer.echo(f"✅ Shipmondo skill successfully installed to: {skill_file}")
    typer.echo("Windsurf's Cascade agent will dynamically load these instructions when relevant.")

@app.command("export")
def setup_export():
    """Export the standard-compliant Agent Skill subfolder (./shipmondo)."""
    target_dir = Path.cwd() / "shipmondo"
    target_file = target_dir / "SKILL.md"
    
    if target_file.exists():
        typer.echo("ℹ️ The shipmondo/SKILL.md file already exists in this directory.", err=True)
        raise typer.Exit(0)
        
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(skill_content.strip())
    
    typer.echo(f"✅ Exported standard Agent Skill folder to: {target_dir}/")
    typer.echo("This folder is now ready to be dropped into any Agent Skills-compatible workflow.")
