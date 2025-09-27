# -*- coding: utf-8 -*-
# DOORS MCP server main file
# Implements DOORS testcase data query, DXL script interaction, structured output, exception handling, etc.

import subprocess           # For executing DOORS client commands
import tempfile             # For temporary file and directory management
import traceback            # For exception stack trace
from typing import List, Optional, Dict   # Type annotations
from typing_extensions import TypedDict   # Structured data types
from dotenv import load_dotenv            # Load environment variables
load_dotenv()  # Load DOORS authentication info from .env file
import os
import psutil
import glob

import logging                # Logging
logging.basicConfig(
    filename='mylog.txt',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

from mcp.server.fastmcp import FastMCP    # MCP协议服务器框架
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create MCP server instance, register to MCP Inspector/Claude Desktop tool list
# FastMCP framework implements MCP protocol and tool registration
mcp = FastMCP(name="IBM_DOORS_MCP")

@mcp.tool()
def get_testcases(module_path: str, output_path: str):
    """
    Query testcase objects from the specified DOORS module via CMD and DXL script, return a structured data list, and support custom output file path.

    Args:
        module_path (str): Full path to the DOORS testcase module, e.g. "/Project/TestcaseModule"
        output_path (str): Directory path to save the output file, e.g. "C:\\output_path", automatically generates several output.md documents, usually it is the root directory of the project.

    Environment variables required:
        DOORS_USERNAME, DOORS_PASSWORD, DOORS_SERVERADDR (authentication info), optional DOORS_PATH (DOORS client path, default "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe")

    Returns:
        List[Testcase]: Structured list of testcase objects, each element contains:
            - ID: Unique identifier for the testcase
            - Object_Type: Fixed as "Testcase"
            - Object_Status: Fixed as "Released"
            - TcURL: Testcase URL link
            - Test_Description: Testcase description
            - Test_Steps: Test steps
            - Expected_Results: Expected results

    Example:
        >>> get_testcases("/Project/TestcaseModule", "C:\\output_path")
    """

    # Get DOORS authentication info (prefer parameters, then environment variables)
    # Authentication info is used to log in to DOORS client, must include username, password, server address
    auth_username = os.getenv('DOORS_USERNAME')
    auth_password = os.getenv('DOORS_PASSWORD')
    auth_serveraddr = os.getenv('DOORS_SERVERADDR')
    doors_path = os.getenv('DOORS_PATH')
    # Join output file path and convert to forward slash for DXL compatibility
    out_path = os.path.join(output_path, "output.md")
    out_path = out_path.replace("\\", "/")

    # Validate output_path is a legal, existing directory
    if not os.path.isdir(output_path):
        logger.error(f"Output directory does not exist or is invalid: {output_path}")
        raise FileNotFoundError(f"Output directory does not exist or is invalid: {output_path}")
    elif 'out_path' in locals() and out_path != "\\IBM_DOORS_MCP-MAIN\\output.md":
        logger.info(f"Using MCP client provided output path: {out_path}")
    else:
        logger.info(f"Using default output path: {out_path}")

    # Validate authentication info completeness, raise exception if missing
    if not auth_username or not auth_password or not auth_serveraddr:
        raise ValueError("DOORS username, password, and server address are required")
    
    # Log DOORS client path source (for debugging)
    if 'doors_path' in locals() and doors_path != "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe":
        logger.info(f"Using MCP client provided DOORS path: {doors_path}")
    else:
        logger.info(f"Using default DOORS path: {doors_path}")

    # Validate module_path parameter
    if 'module_path' in locals():
        logger.info(f"Using MCP client provided module path: {module_path}")
    else:
        raise ValueError("Module path is required, e.g. /XXXXX/System/SysT/SysTS")

    # Construct DXL script to read module and output testcase attributes in Markdown format
    # DXL script traverses module objects, filters Released Testcase objects, and outputs as standard Markdown
    dxl_script = f'''// DXL分批导出实现
Module m; m = null
Object o; o = null
int batch_num = 1
int case_count = 0
string out_path = ""
Stream output = null

m = read("{module_path}", false)
if (null m) {{
    print "ERROR: {module_path} not found\n"
    halt
}}

for o in m do {{
    string ObjType = o."Object_Type"
    string ObjStatus = o."Object_Status"
    if (!null ObjType && ObjType == "Testcase" && !null ObjStatus && ObjStatus == "Released") {{
        if (case_count == 0) {{
            out_path = "{module_path}\\output_" batch_num ".md"
            output = write(out_path)
        }}
        output << "++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        output << "## Testcase: " identifier(o) "\n"
        output << "- **URL**: " getURL(o) "\n"
        output << "- **Status**: Released\n"
        output << "- **Description**: " o."Test_Description" "\n"
        output << "- **Steps**:\n" o."Test_Steps" "\n"
        output << "- **Expected Results**:\n" o."Expected_Results" "\n"
        case_count++
        if (case_count == 30) {{
            close(output)
            batch_num++
            case_count = 0
        }}
    }}
}}
if (case_count > 0 && output != null) {{
    output << "__DXL_SUCCESS__"
    close(output)
}}
close(m)
'''

    # Create temporary directory to manage related files
    with tempfile.TemporaryDirectory() as temp_dir:
        dxl_path = os.path.join(temp_dir, "script.dxl")        # Create DXL script file in temp directory
        with open(dxl_path, "w") as dxl_file:
            dxl_file.write(dxl_script)
        if os.path.exists(dxl_path):
            logging.info(f"script.dxl  generated, path: {dxl_path}") 
        if not os.path.exists(dxl_path):
            logging.error(f"script.dxl not generated, path: {dxl_path}")
            raise FileNotFoundError(f"script.dxl not generated, path: {dxl_path}")
        if os.path.getsize(dxl_path) == 0:
            logging.error(f"script.dxl file is empty, path: {dxl_path}")
            raise RuntimeError(f"script.dxl file is empty, path: {dxl_path}")
        try:
            # Build and execute DOORS command
            # Use double quotes for paths to handle spaces
            cmd = f'"{doors_path}" -d {auth_serveraddr} -u {auth_username} -P {auth_password} -dxl "#include <{dxl_path}>"' 
            # cmd = f'"C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe" -d 36677@doors.prehgad.local -u CaoX -P vT38.6F3GV7ytFHx111111111111111 -dxl "#include <C:\\Users\\cao_x2\\AppData\\Local\\Temp\\tmpuwhcg589\\script.dxl>"'
            # 批量删除所有 output*.md 文件，防止误判
            output_md_pattern = os.path.join(output_path, "output_*.md").replace("\\", "/")
            for file in glob.glob(output_md_pattern):
                try:
                    os.remove(file)
                    logger.info(f"Old output_*.md deleted: {file}")
                except Exception as e:
                    logger.warning(f"Failed to delete old output.md: {file}, error: {e}")
            marker = "__DXL_SUCCESS__"  # Marker string for DXL script execution success
            max_wait = int(os.getenv("DOORS_MAX_WAIT", "1200"))  # Maximum wait time in seconds, configurable via env
            poll_interval = 1  # File polling interval (seconds)
            # Asynchronously start DOORS client process to execute DXL script
            
            proc = subprocess.Popen(
                 cmd,
                 cwd=r"C:\\Program Files\\IBM\\Rational\\DOORS\\9.7",
                 shell=True
            )

            logger.info(f"Executing DOORS command: {cmd}")
            start = time.time()
            found = False
            # Loop to check if any output_*.md file is generated and contains marker string
            while time.time() - start < max_wait:
                # Check if any output_*.md file is generated
                output_md_pattern = os.path.join(output_path, "output_*.md").replace("\\", "/")
                for file in glob.glob(output_md_pattern):
                    if os.path.isfile(file):
                        with open(file, "r") as f:
                            content = f.read()
                        # Check if file contains DXL success marker
                        if marker in content:
                            found = True
                            logger.info(f"DXL success marker found in: {file}")
                            break  # Marker detected, exit inner loop
                if found:
                    break  # Exit outer loop if marker found
                time.sleep(poll_interval)  # Not detected, wait and retry
            
            # Timeout: marker not detected, consider execution failed
            if not found:
                error_msg = f"DXL did not output marker string within {max_wait} seconds, command: {cmd}"
                logger.error(error_msg)
                raise TimeoutError(error_msg)
            else: # Marker detected, wait for DOORS process to exit normally
                logger.info(f"DOORS DXL process ended, output_*.md marker detected")
            
            # 分批内容清洗：遍历所有 output_*.md 文件，去除空行并写回
            output_md_pattern = os.path.join(output_path, "output_*.md").replace("\\", "/")
            cleaned_count = 0
            for file in glob.glob(output_md_pattern):
                if os.path.isfile(file):
                    with open(file, "r", encoding="utf-8") as f:
                        content = f.read()
                    cleaned_content = "\n".join([line for line in content.splitlines() if any(c not in " \t\r" for c in line)])
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(cleaned_content)
                    cleaned_count += 1
                    logger.info(f"Cleaned file: {file}")
            logger.info(f"All output_*.md files cleaned, total: {cleaned_count}")
            
            # Find and kill all doors.exe processes
            try:
                killed_pids = []
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] and proc.info['name'].lower() == "doors.exe":
                        pid = proc.info['pid']
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True)
                        killed_pids.append(pid)
                logger.info(f"Killed doors.exe PIDs: {killed_pids}")
            except Exception as e:
                logger.error(f"Failed to kill doors.exe processes: {str(e)}")
            # 原始方式保留（可选）
            # subprocess.run(f"taskkill /F /PID {doors_pid}", shell=True)
        except Exception as e:
            # DXL execution exception handling, log context and raise detailed exception
            logger.error(f"DXL execution exception: {str(e)}")
            error_context = {
                "command": cmd,
                "module_path": module_path,
                "doors_path": doors_path,
                "out_path": out_path,
                "temp_dir": temp_dir,
                "error": str(e)
            }
            raise RuntimeError(f"DXL execution exception: {str(e)}, command: {cmd}, temp directory: {temp_dir}") from e
        finally:
            # Clean up temporary DXL script file
            os.unlink(dxl_path)
    

@mcp.resource("config://version")
def get_version():
    return "1.0.4"

if __name__ == "__main__":
    mcp.run(transport='stdio')
