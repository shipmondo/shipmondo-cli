import json
import os
import re
import sys
from collections import defaultdict

def resolve_schema(schema_obj, spec, seen_refs=None):
    """Recursively resolves OpenAPI $ref pointers into raw dictionaries."""
    if seen_refs is None:
        seen_refs = set()
        
    if isinstance(schema_obj, dict):
        if "$ref" in schema_obj:
            ref = schema_obj["$ref"]
            if ref in seen_refs:
                return {"$ref": "[Circular Reference]"}
            seen_refs.add(ref)
            
            parts = ref.split("/")
            curr = spec
            for p in parts[1:]:
                curr = curr.get(p, {})
            return resolve_schema(curr, spec, seen_refs)
        
        return {k: resolve_schema(v, spec, seen_refs.copy()) for k, v in schema_obj.items()}
        
    elif isinstance(schema_obj, list):
        return [resolve_schema(i, spec, seen_refs.copy()) for i in schema_obj]
        
    return schema_obj

def clean_param_name(name):
    """Converts API parameters (e.g. receiver_country_code or custom-header) into safe python variables."""
    safe_name = name.replace("-", "_").replace(".", "_")
    if safe_name in ["id", "type", "format", "filter"]:
        return f"param_{safe_name}"
    return safe_name

def map_type(openapi_type):
    """Maps OpenAPI types to Python type strings."""
    mapping = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "number": "float"
    }
    return mapping.get(openapi_type, "str")

def generate_cli():
    if not os.path.exists("openapi.json"):
        print("Error: openapi.json not found in the root directory.")
        return

    with open("openapi.json", "r", encoding="utf-8") as f:
        spec = json.load(f)

    catalog = defaultdict(list)
    resources = defaultdict(list)
    
    for path, methods in spec.get("paths", {}).items():
        parts = [p for p in path.split("/") if p]
        if not parts:
            continue
        resource_name = parts[0]
        resources[resource_name].append((path, methods))

    os.makedirs("shipmondo/commands", exist_ok=True)
    generated_modules = []

    for resource, endpoints in resources.items():
        module_name = resource.replace("-", "_")
        generated_modules.append(module_name)
        file_path = f"shipmondo/commands/{module_name}.py"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("import typer\n")
            f.write("import json\n")
            f.write("import sys\n")
            f.write("from shipmondo.client import ShipmondoClient\n\n")
            f.write(f'app = typer.Typer(help="Manage {resource}")\n\n')

            for path, methods in endpoints:
                for method, details in methods.items():
                    if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                        continue

                    parts = [p for p in path.split("/") if p]
                    
                    if len(parts) == 1:
                        if method == "get":
                            cmd_name = "get" if resource == "account" else "list"
                        elif method == "post":
                            cmd_name = "create"
                        else:
                            cmd_name = method
                    else:
                        sub_action_parts = [p.replace("-", "_") for p in parts[1:] if "{" not in p]
                        if sub_action_parts:
                            cmd_name = "_".join(sub_action_parts)
                            if method in ["post", "put", "patch", "delete"] and method != "post":
                                cmd_name = f"{method}_{cmd_name}"
                        else:
                            if method == "get":
                                cmd_name = "get"
                            elif method in ["put", "patch"]:
                                cmd_name = "update"
                            elif method == "delete":
                                cmd_name = "delete"
                            else:
                                cmd_name = method

                    safe_func_name = f"{cmd_name}_cmd"
                    description = details.get("summary", f"{method.upper()} {path}").replace('"', "'")
                    
                    catalog[module_name].append({
                        "command": cmd_name,
                        "description": description,
                        "method": method.upper(),
                        "endpoint": path
                    })

                    params = details.get("parameters", [])
                    
                    metadata = {
                        "command": f"shipmondo {module_name} {cmd_name}",
                        "description": description,
                        "method": method.upper(),
                        "endpoint": path,
                        "parameters": {},
                        "payload_schema": None
                    }

                    sig_lines = []
                    required_params = [] # Tracks parameters for inner validation block

                    for p in params:
                        p_name = p.get("name")
                        p_in = p.get("in")
                        p_req = p.get("required", False)
                        p_desc = p.get("description", "").replace('"', "'").replace("\n", " ")
                        p_type = map_type(p.get("schema", {}).get("type", "string"))
                        
                        python_var = clean_param_name(p_name)
                        cli_flag = f"--{p_name.replace('_', '-')}"
                        
                        metadata["parameters"][p_name] = {
                            "cli_flag": cli_flag if p_in == "query" else "Positional Argument",
                            "location": p_in,
                            "type": p_type,
                            "required": p_req,
                            "description": p_desc
                        }
                        
                        if p_in == "path":
                            sig_lines.append(f'    {python_var}: {p_type} = typer.Argument(None, help="{p_desc}"),\n')
                            if p_req:
                                required_params.append((python_var, f"Argument '{p_name}'"))
                        else:
                            sig_lines.append(f'    {python_var}: {p_type} = typer.Option(None, "{cli_flag}", help="{p_desc}"),\n')
                            if p_req:
                                required_params.append((python_var, f"Option '{cli_flag}'"))

                    req_body = details.get("requestBody", {})
                    if req_body:
                        schema = req_body.get("content", {}).get("application/json", {}).get("schema")
                        if schema:
                            resolved_payload = resolve_schema(schema, spec)
                            metadata["payload_schema"] = resolved_payload
                    
                    if method in ["post", "put", "patch"]:
                        sig_lines.append('    payload: str = typer.Option(None, "--data", help="JSON payload string"),\n')

                    sig_lines.append('    query: str = typer.Option(None, "--query", help="JSON string fallback for raw custom GET parameters"),\n')
                    sig_lines.append('    json_output: bool = typer.Option(True, "--json/--text", help="Force JSON output"),\n')
                    sig_lines.append('    debug: bool = typer.Option(False, "--debug", help="Print raw API requests and responses to stderr"),\n')
                    sig_lines.append('    open_pdf: bool = typer.Option(False, "--open-pdf", help="Find, decode, and open base64 PDFs in response"),\n')
                    sig_lines.append('    help_json: bool = typer.Option(False, "--help-json", help="Output machine-readable schema for this command as JSON")\n')

                    f.write(f'@app.command("{cmd_name}")\n')
                    f.write(f'def {safe_func_name}(\n')
                    for line in sig_lines:
                        f.write(line)
                    f.write('):\n')
                    f.write(f'    """{description}"""\n')
                    
                    # --- Intercept: Help JSON Command Response ---
                    metadata_json_str = json.dumps(metadata, indent=2).replace('"""', '\\"\\"\\"')
                    f.write(f'    if help_json:\n')
                    f.write(f'        print("""{metadata_json_str}""")\n')
                    f.write(f'        raise typer.Exit()\n\n')
                    
                    # --- Post-Help Validation: Handle Required Fields natively ---
                    for var_name, user_friendly_name in required_params:
                        f.write(f'    if {var_name} is None:\n')
                        f.write(f'        print(json.dumps({{"error": "Missing required {user_friendly_name}"}}), file=sys.stderr)\n')
                        f.write(f'        raise typer.Exit(1)\n\n')
                    
                    f.write('    client = ShipmondoClient(debug=debug)\n')
                    
                    endpoint_build = path
                    for p in params:
                        if p.get("in") == "path":
                            p_original = p.get("name")
                            p_clean = clean_param_name(p_original)
                            endpoint_build = endpoint_build.replace(f"{{{p_original}}}", f"{{{p_clean}}}")
                    
                    f.write(f'    endpoint = f"{endpoint_build}"\n')
                    
                    f.write('    url_params = {}\n')
                    for p in params:
                        if p.get("in") == "query":
                            p_original = p.get("name")
                            p_clean = clean_param_name(p_original)
                            f.write(f'    if {p_clean} is not None:\n')
                            f.write(f'        url_params["{p_original}"] = {p_clean}\n')
                            
                    f.write('    if query:\n')
                    f.write('        url_params.update(json.loads(query))\n')
                    
                    if method in ["post", "put", "patch"]:
                        f.write('    parsed_data = json.loads(payload) if payload else None\n')
                        f.write(f'    data = client.request("{method.upper()}", endpoint, json=parsed_data, params=url_params)\n\n')
                    else:
                        f.write(f'    data = client.request("{method.upper()}", endpoint, params=url_params)\n\n')
                        
                    # --- Intercept: PDF Extraction ---
                    f.write('    if open_pdf:\n')
                    f.write('        from shipmondo.pdf_viewer import extract_and_open_pdfs\n')
                    f.write('        extract_and_open_pdfs(data)\n\n')
                    
                    f.write('    if json_output:\n')
                    f.write('        typer.echo(json.dumps(data))\n')
                    f.write('    else:\n')
                    f.write('        typer.echo("Success. Run with --json to see data.")\n\n')

    # ==================================================
    # Generate shipmondo/commands/setup.py dynamically
    # ==================================================
    skill_markdown = ""
    if os.path.exists("SKILL.md"):
        with open("SKILL.md", "r", encoding="utf-8") as sf:
            skill_markdown = sf.read().replace('"""', '\\"\\"\\"')

    setup_code = f'''import typer
from pathlib import Path

app = typer.Typer(help="CLI AI agent integration and setup")

skill_content = """{skill_markdown}"""

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
        
    typer.echo(f"✅ Shipmondo skill successfully installed to: {{skill_file}}")
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
        
    typer.echo(f"✅ Shipmondo skill successfully installed to: {{skill_file}}")
    typer.echo("GitHub Copilot will automatically load these instructions when relevant.")

@app.command("cursor")
def setup_cursor():
    """Install the Shipmondo Agent Skill into Cursor IDE."""
    target_dir = Path.cwd() / ".cursor" / "skills" / "shipmondo"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = target_dir / "SKILL.md"
    skill_file.write_text(skill_content.strip())
    
    typer.echo(f"✅ Shipmondo skill successfully installed to: {{skill_file}}")
    typer.echo("Cursor's agent will dynamically load these instructions when relevant.")
        
@app.command("windsurf")
def setup_windsurf():
    """Install the Shipmondo Agent Skill into Windsurf IDE."""
    target_dir = Path.cwd() / ".windsurf" / "skills" / "shipmondo"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = target_dir / "SKILL.md"
    skill_file.write_text(skill_content.strip())
    
    typer.echo(f"✅ Shipmondo skill successfully installed to: {{skill_file}}")
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
    
    typer.echo(f"✅ Exported standard Agent Skill folder to: {{target_dir}}/")
    typer.echo("This folder is now ready to be dropped into any Agent Skills-compatible workflow.")
'''
    with open("shipmondo/commands/setup.py", "w", encoding="utf-8") as f:
        f.write(setup_code)
        
    if "setup" not in generated_modules:
        generated_modules.append("setup")

    with open("shipmondo/main.py", "w", encoding="utf-8") as f:
        f.write("import typer\n")
        f.write("import json\n")
        f.write("import os\n")
        f.write("import subprocess\n")
        f.write("import sys\n")
        for mod in generated_modules:
            f.write(f"from shipmondo.commands import {mod}\n")
            
        f.write("\napp = typer.Typer(name='shipmondo', help='Agent-native Discovery-Enabled Shipmondo CLI', no_args_is_help=True)\n\n")
        
        # New Update Command
        f.write('@app.command("update")\n')
        f.write('def update_cli():\n')
        f.write('    """Updates the Shipmondo CLI to the latest version from GitHub."""\n')
        f.write('    print("🔄 Pulling the latest version from GitHub...")\n')
        f.write('    try:\n')
        f.write('        subprocess.run([sys.executable, "-m", "pipx", "install", "git+https://github.com/shipmondo/shipmondo-cli.git", "--force"], check=True, capture_output=True, text=True)\n')
        f.write('        print("✅ Shipmondo CLI successfully updated!")\n')
        f.write('    except subprocess.CalledProcessError as e:\n')
        f.write('        print(f"❌ Failed to update. Pipx error:\\n{e.stderr}", file=sys.stderr)\n')
        f.write('        raise typer.Exit(1)\n')
        f.write('    except FileNotFoundError:\n')
        f.write('        print("❌ \'pipx\' command not found. Please ensure pipx is installed.", file=sys.stderr)\n')
        f.write('        raise typer.Exit(1)\n\n')

        catalog_json_str = json.dumps(dict(catalog), indent=2).replace('"""', '\\"\\"\\"')
        
        f.write('@app.command("commands")\n')
        f.write('def list_all_commands(json_output: bool = typer.Option(True, "--json", help="Force JSON catalog output")):\n')
        f.write('    """Returns a complete machine-readable list of all available subcommands."""\n')
        f.write(f'    print("""{catalog_json_str}""")\n\n')

        f.write('@app.command("openapi")\n')
        f.write('def print_openapi_spec(json_output: bool = typer.Option(True, "--json", help="Dump raw openapi spec")):\n')
        f.write('    """Exposes the raw foundational OpenAPI schema to the client agent context."""\n')
        f.write('    if os.path.exists("openapi.json"):\n')
        f.write('        with open("openapi.json", "r") as openapi_file:\n')
        f.write('            print(json.dumps(json.load(openapi_file)))\n')
        f.write('    else:\n')
        f.write('        print(\'{"error": "openapi.json layout file missing from compilation path"}\')\n\n')

        for mod in generated_modules:
            f.write(f'app.add_typer({mod}.app, name="{mod}")\n')
            
        f.write("\nif __name__ == '__main__':\n")
        f.write("    app()\n")

    print(f"✅ Rebuilt self-describing Discovery CLI framework successfully!")

if __name__ == "__main__":
    generate_cli()