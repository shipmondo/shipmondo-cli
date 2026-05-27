# Shipmondo CLI Agent Skill

You are an expert autonomous agent interacting with the Shipmondo API via the `shipmondo` terminal executable. This CLI is strictly designed for machine-to-machine interaction. 

## 1. Environment Setup
Before executing any commands, you must configure authentication in your terminal environment:
```bash
export SHIPMONDO_API_USER="your_user"
export SHIPMONDO_API_KEY="your_key"
```

## 2. Self-Discovery & Introspection (CRITICAL)
You do not need to guess parameters, endpoints, or schemas. The CLI is entirely self-describing. When you are unsure how to perform an action, follow this discovery loop:
1. **List all available commands:** Run `shipmondo commands --json` to get a catalog of every available resource and action.
2. **Inspect a specific command:** Run `shipmondo [RESOURCE] [ACTION] --help-json` to view the exact machine-readable schema for that command. 
   - *Example:* `shipmondo carriers list --help-json`
   - This output will explicitly define all required positional arguments, explicit CLI flags (like `--receiver-country-code`), and the exact JSON payload schema required for the `--data` flag.

## 3. Core Execution Syntax
Run actions using direct shell command execution: `shipmondo [RESOURCE] [ACTION] [OPTIONS]`
* **Always use JSON**: Append the `--json` flag to every command to ensure you receive raw data instead of human-readable text.
* **Query & Path Parameters**: Simple parameters are mapped to explicit kebab-case CLI flags. (e.g., `--page 1`, `--receiver-country-code DK`). Do not pass these inside the JSON payload.
* **Complex Data Payloads**: For `POST`, `PUT`, or `PATCH` requests (like creating a shipment), pass the highly nested JSON payload as a string using the `--data` flag.
  - *Example:* `shipmondo webhooks create --data '{"endpoint": "https://example.com", "key": "secret", "action": "shipment.create"}' --json`

## 4. CRITICAL: Creating Shipments (Domain Rule)
The Shipmondo API uses a modernized `parties` array for assigning roles to a shipment. You must **NEVER** use the deprecated `sender` or `receiver` root objects in your JSON payload. 
* Instead, pass an array of objects under the `parties` key, specifying the `"role"` (e.g., `"sender"`, `"receiver"`, `"pickup_point"`). 
* *Example Payload Segment:* `{"parties": [{"role": "sender", "name": "Sender Inc", "address1": "Main St 1"}, {"role": "receiver", "name": "John Doe", "address1": "Elm St 2"}]}`

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

## 6. Token Efficiency
Shipmondo payloads can be massive. If you only need specific fields (like finding a specific ID or status), pipe the output through `jq` to filter the data before reading it into your context window.
* *Example:* `shipmondo sales_orders list --json | jq '.data[].id'`

## 7. Error Handling & Debugging
* **Validation Errors:** If you miss a required parameter or pass an invalid payload, the CLI will terminate with an exit code of `1` and output a JSON error to standard error (`stderr`). Read this error carefully to self-correct your payload.
* **Network Debugging:** If you suspect an API mismatch, append the `--debug` flag to your command. This will print the raw outgoing HTTP request (URL, Headers, JSON) and the raw incoming HTTP response directly to `stderr` for your inspection.