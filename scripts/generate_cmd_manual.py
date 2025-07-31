import subprocess
import datetime
import json

def execute_commands(cmd):
    try:
        cmd = cmd + " -h"
        print(f"Executing {cmd}")
        result = subprocess.run(
            cmd if isinstance(cmd, list) else cmd.split(),
            capture_output=True,
            text=True,
            check=True,
            # shell=True,
            timeout=5  # 30 second timeout
        )
        
        print(f"STATUS for {cmd}: SUCCESS")
        print(f"RC: {result.returncode}")
        print(f"Out: {result.stdout}")
        
        if result.stderr:
            print(f"STDERR for {cmd}: {result.stderr}")
            return {"rc": result.returncode, "out": result.stderr if result.stdout == '' else result.stdout}

        return {"rc": result.returncode, "out": result.stdout}
        
    except subprocess.CalledProcessError as e:
        print(f"STATUS for {cmd}: FAILED")
        print(f"RC: {e.returncode}")
        print(f"STDERR: {e.stderr}")
        print(f"STDOUT: {e.stdout}")
        return {"rc": e.returncode, "out": e.stderr if e.stdout == '' else e.stdout}
        
    except subprocess.TimeoutExpired:
        print(f"STATUS for {cmd}: TIMEOUT")
        return {"rc": "nok", "out": "TIMEOUT"}

def store_cmd_manual(commands, output_file="command_output.json"):
    """Execute a list of commands and save output to file."""
    cmd_out = {}
    for cmd in commands:
        cmd_out[cmd] = execute_commands(cmd)

    with open(output_file, 'w') as f:
        json.dump(cmd_out, f, indent=2)

# Usage example
commands = [
    "dslist",
    "mfbr",
    "mfcat",
    "mfcopy",
    "mfdelete",
    "mfdsutil",
    "mfed",
    "mfless",
    "mfrename",
    "mfrestore.sh",
    "copy_from_mfds",
    "copy_to_mfds",
    "mfspool",
    "sub",
    "mfcancel",
    "mfscp",
    "bindrep",
    "xesim",
    "uedit",
    "scanError",
    "diffError.sh",
    "espa",
    "dj",
    "dt",
    "xtrans",
    "xtrace",
    "xspool",
    "fp",
    "my_release_changes",
    "cfm",
    "taildrst"
]

store_cmd_manual(commands)