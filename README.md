# DOORS MCP Server | DOORS MCP 服务器

This is a Model Context Protocol (MCP) server, locally deployed on the user's computer, integrating with IBM DOORS requirements management system. It enables AI agents and other MCP clients to access and query testcase data in DOORS via DXL.  
这是一个 Model Context Protocol (MCP) 服务器，通过在用户电脑中本地部署，实现了与 IBM DOORS 需求管理系统的集成，使 AI 代理和其他 MCP 客户端能够通过DXL访问和查询 DOORS 中的测试用例数据。

## Version Information | 版本信息

Current version: V1.0.3  
当前版本：V1.0.3

## Project Overview | 项目简介

This project creates a Model Context Protocol (MCP) server with the following core features:  
本项目创建了一个 Model Context Protocol (MCP) 服务器，实现以下核心功能：
- Provides MCP interface for external calls  
  提供 MCP 接口供外部调用
- Queries and outputs structured DOORS testcase data  
  实现 DOORS 测试用例数据的查询和结构化输出
- Supports interaction with DOORS client via DXL scripts  
  支持通过 DXL 脚本与 DOORS 客户端交互
- Converts DOORS data to standardized Markdown format and parses it  
  将 DOORS 数据转换为标准化 Markdown 格式并解析
- Provides standardized access for AI agents and other MCP clients via MCP tools  
  通过 MCP 工具函数提供对 AI 代理和其他 MCP 客户端的标准化访问

## Project Features | 项目特性

- Standardized interface: MCP protocol-based, supports multiple client integrations  
  标准化接口：基于MCP协议，支持多种客户端集成
- Secure authentication: Manages sensitive credentials via environment variables  
  安全认证：通过环境变量管理敏感认证信息
- Resource management: Automatically manages creation and cleanup of temp files/directories  
  资源管理：自动管理临时文件和目录的创建与清理
- Error handling: Robust exception handling and detailed error tracking  
  错误处理：完善的异常处理和详细的错误信息追踪
- Logging: Comprehensive logging for debugging and monitoring  
  日志记录：全面的日志记录便于调试和监控
- Type safety: Uses TypedDict for structured data type checking  
  类型安全：使用TypedDict提供结构化数据类型检查
- Timeout control: Supports command execution timeout (100s)  
  超时控制：支持命令执行超时控制（100秒）
- File validation: Supports file existence and size checks  
  文件验证：支持文件存在性和大小检查

## Functional Features | 功能特性

- Supports querying DOORS testcase data (only "Released" Testcase objects)  
  支持查询 DOORS 测试用例数据（仅限Released状态的Testcase对象）
- Supports passing DOORS client path via MCP client  
  支持通过 MCP 客户端传递 DOORS 客户端路径
- Handles DOORS interaction results with temp files/directories  
  使用临时文件和目录处理 DOORS 交互结果
- Good exception handling and resource management  
  具有良好的异常处理和资源管理机制
- Supports DOORS authentication via environment variables  
  支持通过环境变量配置DOORS认证信息
- Detailed logging and error tracking  
  提供详细的日志记录和错误信息追踪
- Supports timeout control and command execution monitoring  
  支持超时控制和命令执行监控

## System Architecture | 系统架构

### Architecture Design | 架构设计

- MCP Interface Layer: Implements MCP protocol with FastMCP, registers tool functions for external calls  
  MCP接口层：使用FastMCP框架实现MCP协议，注册工具函数供外部调用
- Business Logic Layer: Handles DOORS testcase data access and Markdown conversion  
  业务逻辑层：实现DOORS测试用例数据访问逻辑和Markdown格式转换
- Data Access Layer: Interacts with DOORS client via DXL scripts, generates structured Markdown output  
  数据访问层：通过DXL脚本与DOORS客户端交互，生成结构化Markdown输出
- Data Parsing Layer: Parses Markdown files, converts to structured testcase objects  
  数据解析层：解析Markdown格式文件，转换为结构化测试用例对象
- Resource Management Layer: Uses tempfile module for temp file creation and cleanup  
  资源管理层：使用tempfile模块管理临时文件的创建和自动清理
- Config Management Layer: Loads environment variables with python-dotenv (username, password, server address)  
  配置管理层：使用python-dotenv加载环境变量配置（用户名、密码、服务器地址）
- Error Handling Layer: Uses traceback and logging for exception handling and detailed logs  
  错误处理层：使用traceback和logging模块进行异常处理和详细日志记录
- Timeout Control Layer: Uses subprocess for command execution timeout  
  超时控制层：使用subprocess模块实现命令执行超时控制

### Design Patterns | 设计模式

- Factory Pattern: Uses FastMCP() factory method to create MCP server instance  
  工厂模式：使用FastMCP()工厂方法创建MCP服务器实例
- Decorator Pattern: Uses @mcp.tool() decorator to register MCP tool functions  
  装饰器模式：使用@mcp.tool()装饰器注册MCP工具函数
- Context Manager Pattern: Uses tempfile.TemporaryDirectory() for automatic temp resource cleanup  
  上下文管理器模式：使用tempfile.TemporaryDirectory()确保临时资源的自动清理
- Exception Chain Pattern: Multi-layer try-except and RuntimeError wrapping for error propagation and context retention  
  异常处理链模式：通过多层try-except和RuntimeError包装实现错误传播和上下文信息保留
- Builder Pattern: Builds complex DOORS query commands via DXL scripts  
  建造者模式：通过DXL脚本构建复杂的DOORS查询命令
- Singleton Pattern: Ensures MCP server instance uniqueness  
  单例模式：确保MCP服务器实例的唯一性

## Usage Instructions | 使用说明

---

## UV Local Deployment Guide | UV 本地部署指南

1. Install Python  
   安装Python
- Download the installer from the official Python website.  
  前往Python官网下载安装包
- For Windows, install the x64 version (e.g., Python 3.13.7).  
  Windows系统安装x64版本（如Python 3.13.7）
- After installation, verify by running `python` in CMD.  
  安装完成后在CMD输入`python`验证

2. Install UV  
   安装UV

```bash
pip install uv
```
- Verify installation by running `uv` in CMD.  
  在CMD输入`uv`验证安装
```bash
uv
```

3. Install IBM_DOORS_MCP  
   安装IBM_DOORS_MCP

- Download or clone the MCP package.  
  下载或克隆MCP安装包
- Unzip to your chosen directory.  
  解压到指定目录
- Run `uv venv` to create a virtual environment.  
  运行`uv venv`创建虚拟环境
```bash
uv venv
```
- Run `uv init` to initialize the Python project.  
  运行`uv init`初始化Python项目
```bash
uv init
```
- Run `uv add --requirements requirements.txt` to install dependencies.  
  运行`uv add --requirements requirements.txt`安装依赖
```bash
uv add --requirements requirements.txt
```
- Run `uv pip sync requirements.txt` to update dependencies.  
  运行`uv pip sync requirements.txt`同步依赖
```bash
uv pip sync requirements.txt
```  

4. Configure MCP Server (Cline)  
   配置MCP服务器（Cline）

- Open the Cline panel in VS Code, configure MCP servers.  
  在VS Code中打开Cline面板，配置MCP服务器
- Edit `cline_mcp_settings.json` and set the correct MCP path.  
  编辑`cline_mcp_settings.json`，设置正确的MCP路径
- Example config:  
  配置示例：
```json
{
  "mcpServers": {
    "doors-mcp-server": {
      "autoApprove": [
        "get_testcases"
      ],
      "disabled": false,
      "timeout": 600,
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "C: //add-your-doors-mcp-server-path",
        "run",
        "server.py"
      ]
    }
  }
}
```

5. Prepare Environment Variables  
   环境变量准备

- Create a `.env` file in the project root:  
  在项目根目录创建`.env`文件：
```
DOORS_USERNAME= Doors account name
DOORS_PASSWORD= Doors password
DOORS_SERVERADDR=1234@doors.xxxxx.local
DOORS_PATH="C:/Program Files/IBM/Rational/DOORS/9.7/bin/doors.exe"
DOORS_MAX_WAIT=1200
```

6. Directory Structure  
   目录结构

- Project root contains `IBM_DOORS_MCP` folder and `.env` file.  
  项目根目录包含`IBM_DOORS_MCP`文件夹和`.env`文件
- `server.py` is inside `IBM_DOORS_MCP`.  
  `server.py`位于`IBM_DOORS_MCP`文件夹内

7. Troubleshooting  
   常见问题与排查

- If `pip install` or `uv add` times out, check your network.  
  pip/uv安装超时请检查网络
- If `uv` is not recognized, reinstall Python to a writable path.  
  uv命令无效请重新安装Python到可写路径
- If `server.py` not found, check MCP path in config.  
  未找到server.py请检查配置路径
- If MCP communication fails, increase timeout or adjust DOORS_MAX_WAIT.  
  MCP通讯失败请加大timeout或调整DOORS_MAX_WAIT
- If DOORS login fails, check `.env` parameters.  
  DOORS登录失败请检查.env参数

---

## MCP Tool Functions | MCP工具函数

### Query Testcases | 查询测试用例

```python
testcases = get_testcases(
    module_path="/Project/TestcaseModule",
    output_path="C:/person"
)
```
- `output_path` must be an existing directory; `output.md` is generated automatically.  
  `output_path`必须为已存在目录，会自动生成`output.md`
- All path parameters are converted to forward slash format for DXL compatibility.  
  所有路径参数自动转换为正斜杠格式，确保DXL兼容
- Only "Released" Testcase objects are returned, with fields: ID, Object_Type, Object_Status, TcURL, Test_Description, Test_Steps, Expected_Results.  
  仅返回状态为"Released"的Testcase对象，字段包括ID、Object_Type、Object_Status、TcURL、Test_Description、Test_Steps、Expected_Results
- Detailed error handling and logging are supported.  
  支持详细异常处理和日志记录
- doors.exe processes are managed and cleaned up automatically.  
  doors.exe进程自动管理和清理
- Command timeout is configurable via `DOORS_MAX_WAIT` (default 1200s).  
  命令超时可通过`DOORS_MAX_WAIT`配置（默认1200秒）
- Output file existence, size, and marker are checked.  
  输出文件存在性、大小和marker自动校验
- Dependencies: psutil, logging, traceback, tempfile, os, dotenv, typing_extensions.  
  依赖项包括psutil、logging、traceback、tempfile、os、dotenv、typing_extensions

### 参数说明

- `module_path`: DOORS测试用例模块路径（如"/项目/测试用例模块"）
- `output_path`: 输出文件保存目录（如"C:/person"），自动生成output.md
- 环境变量配置（.env）：
  - `DOORS_USERNAME`、`DOORS_PASSWORD`、`DOORS_SERVERADDR` 必填
  - `DOORS_PATH` 可选，默认"C:/Program Files/IBM/Rational/DOORS/9.7/bin/doors.exe"
  - `DOORS_MAX_WAIT` 可选，命令最大等待秒数, 根据Doors响应速度设定合理时间

## Installation Requirements | 安装要求

- Python 3.11+  
  Python 3.11及以上
- IBM DOORS client (locally installed and accessible)  
  IBM DOORS客户端（本地安装并可访问）
- DXL script support (bundled with DOORS)  
  DXL脚本支持（DOORS自带）
- Windows OS (supports DOORS client)  
  Windows操作系统（支持DOORS客户端）
- python-dotenv (for environment variable management)  
  python-dotenv（用于环境变量管理）

## Dependencies | 依赖项

- python-dotenv>=1.1.1
- mcp[cli]>=1.12.4
- fastmcp>=2.11.2
- psutil>=7.0.0

## Development Tools | 开发工具

- FastMCP framework  
- TypedDict data model  
- subprocess  
- tempfile  
- traceback  
- logging  
- python-dotenv  
- os  
- typing_extensions  
- typing  


## Security Notes | 安全注意事项

- Avoid hardcoding sensitive info (username, password, etc.)  
  避免硬编码敏感信息（用户名、密码等）
- Use environment variables for credentials  
  推荐使用环境变量存储认证信息
- Ensure temp files are cleaned up  
  确保临时文件正确清理
- Avoid logging sensitive info  
  日志中避免记录敏感信息
- Verify DOORS client path and server address  
  确保DOORS客户端路径和服务器地址正确
- Control command timeout to prevent hanging  
  控制命令超时，防止挂起

## Logging | 日志记录

- Logs include:  
  日志内容包括：
  - Credential source (MCP client or env)  
    认证信息来源（MCP客户端参数或环境变量）
  - DOORS path source  
    DOORS路径来源
  - Command execution info  
    命令执行信息
  - Errors and stack traces  
    错误和堆栈信息
  - DXL script status  
    DXL脚本状态
  - Temp file creation/cleanup  
    临时文件创建和清理状态
  - Markdown parsing status  
    Markdown解析状态
  - File size/existence checks  
    文件大小和存在性检查结果
  - Timeout and execution time  
    超时控制和执行时间信息

## Contribution Guide | 贡献指南

- Modular design, easy to extend and maintain  
  模块化设计，易于扩展和维护
- Contributions welcome:  
  欢迎贡献：
  - New MCP tool functions  
    新的MCP工具函数
  - Enhanced error handling  
    增强的错误处理
  - Improved logging  
    改进的日志记录
  - Better docs and usage examples  
    更好的文档和使用示例
  - More tests and unit tests  
    完善测试用例和单元测试
  - Resource management optimization  
    优化资源管理
  - Exception handling/reporting improvements  
    改进异常处理和错误报告机制
  - Config management and parameter validation  
    增强配置管理和参数验证
  - Support for more DOORS object types/fields  
    支持更多DOORS对象类型和属性
  - Markdown parsing performance/accuracy  
    优化Markdown解析性能和准确性
  - Timeout control and performance optimization  
    改进超时控制和性能优化

---
