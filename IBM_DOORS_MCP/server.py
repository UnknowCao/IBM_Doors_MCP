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

# 定义需求对象的数据结构，便于类型检查和结构化输出
# class Requirement(TypedDict):
#     id: str              # 需求对象的唯一标识符
#     heading: str         # 需求对象的标题
#     text: str            # 需求对象的正文内容
#     created_on: str      # 创建时间
#     created_by: str      # 创建人
#     modified_on: str     # 最后修改时间
#     modified_by: str     # 最后修改人

# Define the data structure for testcase objects
class Testcase(TypedDict):
    ID: str              # Unique identifier for the testcase
    Object_Type: str     # Testcase title (fixed as "Testcase")
    Test_Description: str  # Testcase description
    Object_Status: str   # Testcase status (fixed as "Released")
    TcURL: str           # Testcase URL link
    Test_Steps: str      # Test steps
    Expected_Results: str  # Expected results

# Create MCP server instance, register to MCP Inspector/Claude Desktop tool list
# FastMCP framework implements MCP protocol and tool registration
mcp = FastMCP(name="IBM_DOORS_MCP")

# Register tool function as MCP tool for external calls
# @mcp.tool()
# def get_requirements(module_path: str, auth: Optional[Dict[str, str]] = None, doors_path: str = "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe") -> List[Requirement]:
#     """
#     通过 DOORS DXL 脚本调用 DOORS 客户端，读取指定模块的需求对象，返回结构化数据列表。

#     参数:
#         module_path (str): DOORS 模块的路径（如 "/项目/需求模块"）
#         auth (Dict[str, str], optional): 认证信息字典，包含用户名和密码，如 {"username": "user", "password": "pass"}
#         doors_path (str): DOORS 客户端的执行路径，默认为 "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe"
    
#     返回:
#         List[Requirement]: 需求对象的结构化列表，每个元素为一个需求的详细信息。
        
#     示例:
#         >>> get_requirements("/项目/需求模块", {"username": "user", "password": "pass", "doors_path": "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe"})
#     """
#     # 获取认证信息（优先使用参数，其次使用环境变量）
#     if auth and isinstance(auth, dict):
#         # 从参数中获取用户名和密码
#         auth_username = auth.get('username')
#         auth_password = auth.get('password')
#         auth_serveraddr = auth.get('serveraddr')
#     else:
#         # 从环境变量获取认证信息
#         auth_username = os.getenv('DOORS_USERNAME')
#         auth_password = os.getenv('DOORS_PASSWORD')
#         auth_serveraddr = os.getenv('DOORS_SERVERADDR')
    
#     # 验证认证信息是否完整
#     if not auth_username or not auth_password or not auth_serveraddr:
#         # 如果没有提供认证信息，则抛出异常
#         raise ValueError("需要提供DOORS用户名,密码和服务器地址")
    
#     # 记录认证信息来源（用于调试）
#     if auth and isinstance(auth, dict):
#         logger.info("使用MCP客户端提供的认证信息")
#     else:
#         logger.info("使用环境变量中的认证信息")
    
#     # 记录DOORS路径来源（用于调试）
#     if 'doors_path' in locals() and doors_path != "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe":
#         logger.info(f"使用MCP客户端提供的DOORS路径: {doors_path}")
#     else:
#         logger.info(f"使用默认的DOORS路径: {doors_path}")
    
#     # 构造 DXL 脚本，读取模块并输出对象属性为 CSV 格式
#     dxl_script = f'''
#     Module m = null
#     object 0 = null
#     int i =0

#     m = read("{module_path}", false)
#     if (null m) {{
#         print "ERROR: Module" module_path "not found\\n"
#         halt
#     }}
#     for o in m do {{
#         string ObjType = o."Object_Type"
#         string ObjStatus = o."Object_Status"
#         if(!null ObjType && ObjType == "Testcase" && !null ObjStatus && ObjStatus == "Released") 
#         {{
#             print identifier(o) ","
#             print getURL(o) ","
#             print o."Test_Description" ","
#             print o."Test_Steps" ","
#             print o."Expected_Results" "\\n"
#         }}
#     }}
# close(m)
# '''
#     # 临时保存 DXL 脚本
#     with tempfile.NamedTemporaryFile("w", delete=False, suffix=".dxl") as dxl_file:
#         dxl_file.write(dxl_script)
#         dxl_path = dxl_file.name

#     # 临时保存 DOORS 输出的 CSV 文件
#     with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv") as out_file:
#         out_path = out_file.name

#     try:
#         # 调用 DOORS 客户端以批处理方式运行 DXL 脚本，输出重定向到 CSV
#         cmd = f'"{doors_path}" -d {auth_serveraddr} -u {auth_username} -P {auth_password} -batch -dxl "{dxl_path}" > "{out_path}"'
#         logger.info(f"正在执行DOORS命令: {cmd}")
#         result = subprocess.run(cmd, shell=True, timeout=60, capture_output=True)
#         if result.returncode != 0:
#             logger.error(f"DOORS DXL执行失败，错误信息: {result.stderr}")
#             raise RuntimeError("DOORS DXL执行失败")
#     except Exception as e:
#         logger.error(f"DXL执行异常: {str(e)}")
#         # 清理临时文件并抛出异常
#         os.unlink(dxl_path)
#         os.unlink(out_path)
#         raise RuntimeError(f"DXL执行异常: {str(e)}")

#     requirements: List[Requirement] = []
#     try:
#         # 解析 CSV 文件，转换为结构化 Requirement 列表
#         with open(out_path, "r", encoding="utf-8") as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 # 跳过错误行或格式不完整行
#                 if len(row) < 7 or row[0].startswith("ERROR"):
#                     continue
#                 requirements.append({
#                     "id": row[0],
#                     "heading": row[1],
#                     "text": row[2],
#                     "created_on": row[3],
#                     "created_by": row[4],
#                     "modified_on": row[5],
#                     "modified_by": row[6]
#                 })
#     finally:
#         # 清理临时文件
#         os.unlink(dxl_path)
#         os.unlink(out_path)

#     return requirements


# Added: Tool function for querying testcases
@mcp.tool()
def get_testcases(module_path: str, output_path: str) -> List[Testcase]:
    """
    Query testcase objects from the specified DOORS module via CMD and DXL script, return a structured data list, and support custom output file path.

    Args:
        module_path (str): Full path to the DOORS testcase module, e.g. "/Project/TestcaseModule"
        output_path (str): Directory path to save the output file, e.g. "C:\\output_path", automatically generates output.md

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
    dxl_script = f'''Module m;m = null
Object o;o = null
int i = 0

m = read("{module_path}", false)
if (null m) {{
    print "ERROR: {module_path} not found\\n"
    halt
}}

Stream output = write("{out_path}")
for o in m do {{
    string ObjType = o."Object_Type"
    string ObjStatus = o."Object_Status"
    if(!null ObjType && ObjType == "Testcase" && !null ObjStatus && ObjStatus == "Released") 
    {{
        output <<  "++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"     
        output << "## Testcase: " identifier(o) "\n"
        output << "- **URL**: " getURL(o) "\n"
        output << "- **Status**: Released\n"
        output << "- **Description**: " o."Test_Description" "\n"
        output << "- **Steps**:\n" o."Test_Steps" "\n"
        output << "- **Expected Results**:\n" o."Expected_Results" "\n"
    }}
}}
output << "__DXL_SUCCESS__"
close(output) 
close(m)
'''

    # Create temporary directory to manage related files
    with tempfile.TemporaryDirectory() as temp_dir:
        dxl_path = os.path.join(temp_dir, "script.dxl")        # Create DXL script file in temp directory
        with open(dxl_path, "w", encoding="utf-8") as dxl_file:
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
            # Check and remove old output.md to prevent false positive
            if os.path.isfile(out_path):
                try:
                    os.remove(out_path)
                    logger.info(f"Old output.md deleted: {out_path}")
                except Exception as e:
                    logger.warning(f"Failed to delete old output.md: {e}")
            marker = "__DXL_SUCCESS__"  # Marker string for DXL script execution success
            max_wait = int(os.getenv("DOORS_MAX_WAIT", "1200"))  # Maximum wait time in seconds, configurable via env
            poll_interval = 1  # File polling interval (seconds)
            # Asynchronously start DOORS client process to execute DXL script
            #args = [doors_path, '-d ', auth_serveraddr, '-u ', auth_username, '-P ', auth_password, '-dxl ', f'#include <{dxl_path}>']
            # os.system('C:/Program Files/IBM/Rational/DOORS/9.7/bin/doors.exe')
            # cmd1 = subprocess.Popen(
            #     [r'{doors_path}'],
                # env=env,
                # cwd=r'C:\Program Files\IBM\Rational\DOORS\bin',
                # stdout=subprocess.PIPE,
                # stdin=subprocess.PIPE,
                # stderr=subprocess.PIPE, 
                # creationflags=subprocess.CREATE_NEW_CONSOLE,
                # close_fds=True
            # )
            # cmd1.stdin.write(cmd.encode('utf-8') + b'\n')
            # cmd1.stdin.flush()
            # cmd1.wait()
            # cmd1.stdin.close()
            # #cmd1.stdout.close()
            # cmd1.stderr.close()
            
            proc = subprocess.Popen(
                 cmd,
                 cwd=r"C:\\Program Files\\IBM\\Rational\\DOORS\\9.7",
                 shell=True
            )
            doors_pid = proc.pid

            # process = subprocess.Popen([
            #     r'C:\Program Files\IBM\Rational\DOORS\9.7\bin\doors.exe',
            #     '-nosplash',  # 禁用启动画面
            #     '-console',   # 启用控制台输出
            #     '-debug'      # 启用调试模式
            # ], env=env, cwd=r'C:\Program Files\IBM\Rational\DOORS\9.7\bin')
            # process = subprocess.Popen([
            #     'cmd', '/c', 'doors.exe'
            # ], cwd=r'C:\Program Files\IBM\Rational\DOORS\9.7\bin'
            # )

            logger.info(f"Executing DOORS command: {cmd}")
            start = time.time()
            found = False
            # Loop to check if output.md is generated and contains marker string
            while time.time() - start < max_wait:
                # Check if file is generated
                if os.path.isfile(out_path):
                    with open(out_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Check if file contains DXL success marker
                    if marker in content:
                        found = True
                        break  # Marker detected, exit loop
                time.sleep(poll_interval)  # Not detected, wait and retry
            # Timeout: marker not detected, consider execution failed
            if not found:
                error_msg = f"DXL did not output marker string within {max_wait} seconds, command: {cmd}"
                logger.error(error_msg)
                raise TimeoutError(error_msg)
            else: # Marker detected, wait for DOORS process to exit normally
                logger.info(f"DOORS DXL process ended, output.md marker detected")
            subprocess.run(f"taskkill /F /PID {doors_pid}", shell=True)
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
    # Check if output.md file exists and is not empty
    # Raise exception if file does not exist or is empty
    if not os.path.isfile(out_path):
        logging.error(f"File does not exist: {out_path}")
        raise FileNotFoundError(f"File does not exist: {out_path}")
    elif os.path.getsize(out_path) == 0:
        logging.error(f"File is empty: {out_path}")
        raise RuntimeError(f"File is empty: {out_path}")
        # Open and read output.md file content
    
    with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()
    # Remove all blank lines
    cleaned_content = "\n".join([line for line in content.splitlines() if any(c not in " \t\r" for c in line)])
    # Write back to original file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

    # Parse Markdown file, convert to structured Testcase list
    # Parse Markdown content by testcase group, extract fields
    # Initialize testcase list
    testcases: List[Testcase] = []
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            content2 = f.read()
        # 按分隔符分割，得到多个测试用例块
        test_case_blocks = content2.strip().split("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for block in test_case_blocks:
            lines = [line for line in block.strip().split("\n") if line.strip() and line.strip() != "__DXL_SUCCESS__"]
            if not lines:
                continue
            testcase_data = {}
            for line in lines:
                if line.startswith("## Testcase: "):
                    testcase_data["ID"] = line.replace("## Testcase: ", "").strip()
                elif line.startswith("- **URL**: "):
                    testcase_data["TcURL"] = line.replace("- **URL**: ", "").strip()
                elif line.startswith("- **Status**:"):
                    testcase_data["Object_Status"] = line.replace("- **Status**: ", "").strip()
                elif line.startswith("- **Description**:"):
                    testcase_data["Test_Description"] = line.replace("- **Description**: ", "").strip()
                elif line.startswith("- **Steps**:"):
                    testcase_data["Test_Steps"] = ""
                elif "Test_Steps" in testcase_data and not line.startswith("- **Expected Results**:"):
                    # 收集步骤内容直到遇到 Expected Results
                    testcase_data["Test_Steps"] += (line.strip() + "\n")
                elif line.startswith("- **Expected Results**:"):
                    testcase_data["Expected_Results"] = ""
                elif "Expected_Results" in testcase_data:
                    # 收集期望结果内容直到遇到下一个字段或结束
                    testcase_data["Expected_Results"] += (line.strip() + "\n")
            # 清理步骤和期望结果的多余换行
            if "Test_Steps" in testcase_data:
                testcase_data["Test_Steps"] = testcase_data["Test_Steps"].strip()
            if "Expected_Results" in testcase_data:
                testcase_data["Expected_Results"] = testcase_data["Expected_Results"].strip()
            # 固定 Object_Type
            testcase_data["Object_Type"] = "Testcase"
            # 检查所有字段
            if all(key in testcase_data for key in ["ID", "TcURL", "Test_Description", "Test_Steps", "Expected_Results"]):
                testcases.append({
                    "ID": testcase_data["ID"],
                    "Object_Type": "Testcase",
                    "Object_Status": testcase_data.get("Object_Status", "Released"),
                    "TcURL": testcase_data["TcURL"],
                    "Test_Description": testcase_data["Test_Description"],
                    "Test_Steps": testcase_data["Test_Steps"],
                    "Expected_Results": testcase_data["Expected_Results"]
                })
    except Exception as e:
        logger.error(f"MD parsing exception: {str(e)}")
        error_context = {
            "module_path": module_path,
            "file_path": out_path,
            "error": str(e),
            "file_content": open(out_path, "r", encoding="utf-8").read() if os.path.exists(out_path) else None,
            "traceback": traceback.format_exc()
        }
        raise RuntimeError(f"MD parsing exception: {str(e)}, file path: {out_path}, file content: {error_context['file_content']}, traceback: {error_context['traceback']}") from e
    return testcases

@mcp.resource("config://version")
def get_version():
    return "1.0.2"


if __name__ == "__main__":
    mcp.run(transport='stdio')
