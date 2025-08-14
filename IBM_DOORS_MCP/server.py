import subprocess
import tempfile
import traceback
from typing import List, Optional, Dict
from typing_extensions import TypedDict
from dotenv import load_dotenv
load_dotenv()  # 加载环境变量文件 .env
import logging
import os
from mcp.server.fastmcp import FastMCP

# 配置日志记录
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

# 定义测试用例对象的数据结构
class Testcase(TypedDict):
    ID: str              # 测试用例的唯一标识符
    Object_Type: str     # 测试用例标题
    Test_Description: str  # 测试用例内容
    Object_Status: str   # 测试用例状态
    TcURL: str           # 测试用例的URL链接
    Test_Steps: str      # 测试步骤
    Expected_Results: str  # 预期结果

# 创建 MCP 服务器实例，名称会显示在 MCP Inspector/Claude Desktop 工具列表中
mcp = FastMCP(name="IBM_DOORS_MCP")

# 注册工具函数为 MCP 工具，供外部调用
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

# 新增：查询测试用例的工具函数
@mcp.tool()
def get_testcases(module_path: str) -> List[Testcase]:
    """
通过CMD调用Doors程序和DXL脚本，读取指定模块的测试用例对象，返回结构化数据列表。

参数:
    module_path (str): DOORS 测试用例模块的路径（如 "/项目/测试用例模块"）
    环境变量需包含 DOORS_USERNAME、DOORS_PASSWORD、DOORS_SERVERADDR（认证信息），可选 DOORS_PATH（DOORS 客户端路径，默认 "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe"）

返回:
    List[Testcase]: 测试用例对象的结构化列表，每个元素包含：
        - ID: 测试用例唯一标识符
        - Object_Type: 固定为 "Testcase"
        - Object_Status: 固定为 "Released"
        - TcURL: 测试用例的URL链接
        - Test_Description: 测试用例内容
        - Test_Steps: 测试步骤
        - Expected_Results: 预期结果

示例:
    >>> get_testcases("/项目/测试用例模块")
"""

    # 获取认证信息（优先使用参数，其次使用环境变量）
        # 从环境变量获取认证信息
    auth_username = os.getenv('DOORS_USERNAME')
    auth_password = os.getenv('DOORS_PASSWORD')
    auth_serveraddr = os.getenv('DOORS_SERVERADDR')
    doors_path = os.getenv('DOORS_PATH', "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe")

    # 验证认证信息是否完整
    if not auth_username or not auth_password or not auth_serveraddr:
        # 如果没有提供认证信息，则抛出异常
        raise ValueError("需要提供DOORS用户名,密码和服务器地址")
    
    # 记录DOORS路径来源（用于调试）
    if 'doors_path' in locals() and doors_path != "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe":
        logger.info(f"使用MCP客户端提供的DOORS路径: {doors_path}")
    else:
        logger.info(f"使用默认的DOORS路径: {doors_path}")

    if 'module_path' in locals():
        logger.info(f"使用MCP客户端提供的模块路径: {module_path}")
    else:
        raise ValueError("需要提供模块路径，如/XXXXX/System/SysT/SysTS")

    # 构造 DXL 脚本，读取模块并输出测试用例属性为 Markdown 格式
    dxl_script = f'''Module m;m = null
Object o; o = null
int i = 0

m = read("{module_path}", false)
if (null m) {{
	print "ERROR: {module_path} not found\\n"
    halt
}}

Stream output = write("output.md")
for o in m do {{
    string ObjType = o."Object_Type"
    string ObjStatus = o."Object_Status"
    if(!null ObjType && ObjType == "Testcase" && !null ObjStatus && ObjStatus == "Released") 
    {{
        output << "- TcID: " identifier(o) "\n"
        output << "- URL: " getURL(o) "\n"
        output << "- Test_Description: " o."Test_Description" "\n"
        output << "- Test_Steps: " o."Test_Steps" "\n"
        output << "- Expected_Results: " o."Expected_Results" "\n\n"
    }}
}}
close(output)
close(m)
    '''
    # 创建临时目录管理相关文件
    with tempfile.TemporaryDirectory() as temp_dir:
        dxl_path = os.path.join(temp_dir, "script.dxl")        # 在临时目录中创建 DXL 脚本文件
        with open(dxl_path, "w", encoding="utf-8") as dxl_file:
            dxl_file.write(dxl_script)
        if not os.path.exists(dxl_path):
            logging.error(f"script.dxl未生成，路径: {dxl_path}")
            raise FileNotFoundError(f"script.dxl未生成，路径: {dxl_path}")
        if os.path.getsize(dxl_path) == 0:
            logging.error(f"script.dxl文件为空，路径: {dxl_path}")
            raise RuntimeError(f"script.dxl文件为空，路径: {dxl_path}")
        
        # 设置output.md文件路径
        out_path = os.path.join(temp_dir, "output.md")
        
        try:
            # 构建并执行 DOORS 命令
            # 使用双引号包裹路径，处理路径中的空格
            cmd = f'"{doors_path}" -d {auth_serveraddr} -u {auth_username} -P {auth_password} -dxl "#include <{dxl_path}>"'
            logger.info(f"正在执行DOORS命令: {cmd}")
            # 执行命令并捕获输出
            # shell=True 允许使用字符串命令，适用于Windows环境
            # timeout=60 防止命令挂起
            # capture_output=True 捕获标准错误输出用于调试
            result = subprocess.run(cmd, shell=True, timeout=100, capture_output=True)
            # 检查命令执行状态
            if result.returncode != 0:
                # 记录详细的错误信息
                stderr = result.stderr.decode("utf-8", errors="ignore") if result.stderr else None
                logger.error(f"DOORS DXL执行失败，错误信息: {result.stderr}")
                error_context = {
                    "command": cmd,
                    "exit_code": result.returncode,
                    "stderr": stderr,
                    "module_path": module_path,
                    "doors_path": doors_path,
                    "temp_dir": temp_dir
                }
                # 创建详细的错误信息
                error_msg = f"DOORS DXL执行失败: 退出代码 {result.returncode}, 命令: {cmd}"
                if stderr:
                    error_msg += f", 错误详情: {stderr}"
                raise RuntimeError(error_msg)
        except Exception as e:
            # 记录异常信息
            logger.error(f"DXL执行异常: {str(e)}")
            error_context = {
                "command": cmd,
                "module_path": module_path,
                "doors_path": doors_path,
                "temp_dir": temp_dir,
                "error": str(e)
            }
            # 抛出带详细上下文信息的异常
            raise RuntimeError(f"DXL执行异常: {str(e)}, 命令: {cmd}, 临时目录: {temp_dir}") from e
        
        # 检查output.md文件是否存在且不为空
        if not os.path.exists(out_path):
            logging.error(f"output.md未生成，路径: {out_path}")
            raise FileNotFoundError(f"output.md未生成，路径: {out_path}")
        if os.path.getsize(out_path) == 0:
            logging.error(f"output.md文件内容为空，路径: {out_path}")
            raise RuntimeError(f"output.md文件内容为空，路径: {out_path}")
        
        # 解析 Markdown 文件，转换为结构化 Testcase 列表
        testcases: List[Testcase] = []
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                content = f.read()
            # 按测试用例分组解析Markdown内容
            test_case_blocks = content.strip().split("\n\n")
            
            for block in test_case_blocks:
                if not block.strip():
                    continue
                    
                lines = block.strip().split("\n")
                testcase_data = {}
                
                for line in lines:
                    if line.startswith("- TcID: "):
                        testcase_data["ID"] = line.replace("- TcID: ", "").strip()
                    elif line.startswith("- URL: "):
                        testcase_data["TcURL"] = line.replace("- URL: ", "").strip()
                    elif line.startswith("- Test_Description: "):
                        testcase_data["Test_Description"] = line.replace("- Test_Description: ", "").strip()
                    elif line.startswith("- Test_Steps: "):
                        testcase_data["Test_Steps"] = line.replace("- Test_Steps: ", "").strip()
                    elif line.startswith("- Expected_Results: "):
                        testcase_data["Expected_Results"] = line.replace("- Expected_Results: ", "").strip()
                
                # 确保所有必需字段都存在
                if all(key in testcase_data for key in ["ID", "TcURL", "Test_Description", "Test_Steps", "Expected_Results"]):
                    testcases.append({
                        "ID": testcase_data["ID"],
                        "Object_Type": "Testcase",  # 添加缺失的字段
                        "Object_Status": "Released",  # 添加缺失的字段
                        "TcURL": testcase_data["TcURL"],
                        "Test_Description": testcase_data["Test_Description"],
                        "Test_Steps": testcase_data["Test_Steps"],
                        "Expected_Results": testcase_data["Expected_Results"]
                    })
        except Exception as e:
            logger.error(f"MD解析异常: {str(e)}")
            error_context = {
                "module_path": module_path,
                "file_path": out_path,
                "error": str(e),
                "file_content": open(out_path, "r", encoding="utf-8").read() if os.path.exists(out_path) else None,
                "traceback": traceback.format_exc()
            }
            raise RuntimeError(f"MD解析异常: {str(e)}, 文件路径: {out_path}, 文件内容: {error_context['file_content']}, 堆栈跟踪: {error_context['traceback']}") from e
    return testcases

@mcp.resource("config://version")
def get_version():
    return "1.0.1"
# MCP 服务器入口，支持命令行/Inspector/Claude Desktop 启动
if __name__ == "__main__":
    mcp.run(transport='stdio')
