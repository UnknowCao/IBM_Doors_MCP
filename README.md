# DOORS MCP 服务器  
# DOORS MCP Server

这是一个 Model Context Protocol (MCP) 服务器，通过在用户电脑中本地部署，实现了与 IBM DOORS 需求管理系统的集成，使 AI 代理和其他 MCP 客户端能够通过DXL访问和查询 DOORS 中的测试用例数据。  
This is a Model Context Protocol (MCP) server, locally deployed on the user's computer, integrating with IBM DOORS requirements management system. It enables AI agents and other MCP clients to access and query testcase data in DOORS via DXL.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)  
[![DOORS](https://img.shields.io/badge/DOORS-9.7%2B-orange.svg)](https://www.ibm.com/products/doors)

## 版本信息  
## Version Info

当前版本：V1.0.2  
Current version: V1.0.2

## 项目概述  
## Project Overview

本项目创建了一个 Model Context Protocol (MCP) 服务器，实现以下核心功能：  
This project creates a Model Context Protocol (MCP) server with the following core features:
- 提供 MCP 接口供外部调用  
  Provides MCP interface for external calls
- 实现 DOORS 测试用例数据的查询和结构化输出  
  Queries and outputs structured DOORS testcase data
- 支持通过 DXL 脚本与 DOORS 客户端交互  
  Supports interaction with DOORS client via DXL scripts
- 将 DOORS 数据转换为标准化 Markdown 格式并解析  
  Converts DOORS data to standardized Markdown format and parses it
- 通过 MCP 工具函数提供对 AI 代理和其他 MCP 客户端的标准化访问  
  Provides standardized access for AI agents and other MCP clients via MCP tools

## 项目特点  
## Project Features

- **标准化接口**：基于MCP协议，支持多种客户端集成  
  **Standardized interface**: MCP protocol-based, supports multiple client integrations
- **安全认证**：通过环境变量管理敏感认证信息  
  **Secure authentication**: Manages sensitive credentials via environment variables
- **资源管理**：自动管理临时文件和目录的创建与清理  
  **Resource management**: Automatically manages creation and cleanup of temp files/directories
- **错误处理**：完善的异常处理和详细的错误信息追踪  
  **Error handling**: Robust exception handling and detailed error tracking
- **日志记录**：全面的日志记录便于调试和监控  
  **Logging**: Comprehensive logging for debugging and monitoring
- **类型安全**：使用TypedDict提供结构化数据类型检查  
  **Type safety**: Uses TypedDict for structured data type checking
- **超时控制**：支持命令执行超时控制（100秒）  
  **Timeout control**: Supports command execution timeout (100s)
- **文件验证**：支持文件存在性和大小检查  
  **File validation**: Supports file existence and size checks

## 功能特性  
## Functional Features

- ✅ 支持查询 DOORS 测试用例数据（仅限Released状态的Testcase对象）  
  Supports querying DOORS testcase data (only "Released" Testcase objects)
- ✅ 支持通过 MCP 客户端传递 DOORS 客户端路径  
  Supports passing DOORS client path via MCP client
- ✅ 使用临时文件和目录处理 DOORS 交互结果  
  Handles DOORS interaction results with temp files/directories
- ✅ 具有良好的异常处理和资源管理机制  
  Good exception handling and resource management
- ✅ 支持通过环境变量配置DOORS认证信息  
  Supports DOORS authentication via environment variables
- ✅ 提供详细的日志记录和错误信息追踪  
  Detailed logging and error tracking
- ✅ 支持超时控制和命令执行监控  
  Supports timeout control and command execution monitoring

## 系统架构  
## System Architecture

### 架构设计  
### Architecture Design

- **MCP接口层**：使用FastMCP框架实现MCP协议，注册工具函数供外部调用  
  **MCP Interface Layer**: Implements MCP protocol with FastMCP, registers tool functions for external calls
- **业务逻辑层**：实现DOORS测试用例数据访问逻辑和Markdown格式转换  
  **Business Logic Layer**: Handles DOORS testcase data access and Markdown conversion
- **数据访问层**：通过DXL脚本与DOORS客户端交互，生成结构化Markdown输出  
  **Data Access Layer**: Interacts with DOORS client via DXL scripts, generates structured Markdown output
- **数据解析层**：解析Markdown格式文件，转换为结构化测试用例对象  
  **Data Parsing Layer**: Parses Markdown files, converts to structured testcase objects
- **资源管理层**：使用tempfile模块管理临时文件的创建和自动清理  
  **Resource Management Layer**: Uses tempfile module for temp file creation and cleanup
- **配置管理层**：使用python-dotenv加载环境变量配置（用户名、密码、服务器地址）  
  **Config Management Layer**: Loads environment variables with python-dotenv (username, password, server address)
- **错误处理层**：使用traceback和logging模块进行异常处理和详细日志记录  
  **Error Handling Layer**: Uses traceback and logging for exception handling and detailed logs
- **超时控制层**：使用subprocess模块实现命令执行超时控制  
  **Timeout Control Layer**: Uses subprocess for command execution timeout

### 设计模式  
### Design Patterns

- 工厂模式：使用FastMCP()工厂方法创建MCP服务器实例  
  Factory Pattern: Uses FastMCP() factory method to create MCP server instance
- 装饰器模式：使用@mcp.tool()装饰器注册MCP工具函数  
  Decorator Pattern: Uses @mcp.tool() decorator to register MCP tool functions
- 上下文管理器模式：使用tempfile.TemporaryDirectory()确保临时资源的自动清理  
  Context Manager Pattern: Uses tempfile.TemporaryDirectory() for automatic temp resource cleanup
- 异常处理链模式：通过多层try-except和RuntimeError包装实现错误传播和上下文信息保留  
  Exception Chain Pattern: Multi-layer try-except and RuntimeError wrapping for error propagation and context retention
- 建造者模式：通过DXL脚本构建复杂的DOORS查询命令  
  Builder Pattern: Builds complex DOORS query commands via DXL scripts
- 单例模式：确保MCP服务器实例的唯一性  
  Singleton Pattern: Ensures MCP server instance uniqueness

## 使用说明  
## Usage Instructions

### MCP 服务器配置与启动  
### MCP Server Configuration & Startup

#### 在 VS Code 中配置和启动服务器  
#### Configure and Start Server in VS Code

1. **MCP 服务器配置注意事项**：  
   **MCP Server Configuration Notes:**
   - 确保 `cline_mcp_settings.json` 中的参数与服务器实现匹配  
     Ensure parameters in `cline_mcp_settings.json` match server implementation
   - 特别注意 `parameters` 部分应与工具函数的参数定义一致  
     Pay attention to `parameters` section matching tool function definitions
   - 环境变量设置应与实际 DOORS 环境匹配  
     Environment variables should match actual DOORS environment
   - autoApprove 列表应准确反映注册的 MCP 工具函数名称  
     autoApprove list should accurately reflect registered MCP tool function names
   - 确保DOORS客户端路径在目标机器上正确安装且可访问  
     Ensure DOORS client path is correctly installed and accessible on target machine

2. **配置 MCP 客户端**：  
   **Configure MCP Client:**
   - 在 `cline_mcp_settings.json` 中添加以下配置：  
     Add the following config to `cline_mcp_settings.json`:
   
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
        "C:\\Data\\Users\\cao_x2\\Documents\\Cline\\IBM_Doors_MCP-main\\IBM_DOORS_MCP",
        "run",
        "server.py"
      ]
    }
  }
}
```

6. **配置用户名，密码，服务器地址信息**：  
      **Configure username, password, server address:**
      在项目根目录下创建`.env`文件，并在文件中配置DOORS认证信息，程序会自动从环境变量中获取相关信息：  
      Create a `.env` file in the project root and configure DOORS credentials. The program will automatically read from environment variables:
      ```
      DOORS_USERNAME= Doors account name
      DOORS_PASSWORD= Doors password
      DOORS_SERVERADDR=1234@doors.xxxxx.local
      DOORS_PATH="C:/Program Files/IBM/Rational/DOORS/9.7/bin/doors.exe"
      DOORS_MAX_WAIT=1200
      ```

### MCP 工具函数  
### MCP Tool Functions

#### 查询测试用例  
#### Query Testcases
```python
testcases = get_testcases(
    module_path="/项目/测试用例模块",
    output_path="C:/person"
)
```
- `output_path` 必须为已存在的合法目录，自动生成 `output.md` 文件（如 `C:/person/output.md`），并进行内容清理和校验。  
  `output_path` must be a valid existing directory. `output.md` will be auto-generated (e.g. `C:/person/output.md`), with content cleanup and validation.
- 所有路径参数自动转换为正斜杠格式，确保 DXL 兼容。  
  All path parameters are auto-converted to forward slash format for DXL compatibility.

### 工具函数特点  
### Tool Function Features

- 注册为 MCP 工具，可在 MCP Inspector 或 Claude Desktop 中调用  
  Registered as MCP tool, callable in MCP Inspector or Claude Desktop
- 自动从环境变量获取 DOORS 认证信息（用户名、密码、服务器地址、DOORS_PATH、DOORS_MAX_WAIT）  
  Automatically reads DOORS credentials from environment variables (username, password, server address, DOORS_PATH, DOORS_MAX_WAIT)
- 仅返回状态为 "Released" 的 Testcase 对象  
  Only returns Testcase objects with status "Released"
- 输出文件存在性和大小自动校验，内容自动去除空行  
  Output file existence and size auto-checked, content auto-cleans empty lines
- 错误处理和日志记录更完善，支持详细堆栈跟踪  
  Improved error handling and logging, supports detailed stack trace
- 命令执行超时可通过环境变量配置（默认 1200 秒）  
  Command execution timeout configurable via environment variable (default 1200s)
- 详细日志记录认证信息来源、路径、命令、异常、临时文件状态等  
  Detailed logs for credential source, paths, commands, exceptions, temp file status, etc.

### 参数说明  
### Parameter Description

- `module_path`: DOORS 测试用例模块路径（如 "/项目/测试用例模块"）  
  DOORS testcase module path (e.g. "/Project/TestcaseModule")
- `output_path`: 输出文件保存目录（如 "C:/person"），自动生成 output.md  
  Output file save directory (e.g. "C:/person"), auto-generates output.md
- 环境变量配置（.env）：  
  Environment variable config (.env):
  - `DOORS_USERNAME`、`DOORS_PASSWORD`、`DOORS_SERVERADDR` 必填  
    Required: `DOORS_USERNAME`, `DOORS_PASSWORD`, `DOORS_SERVERADDR`
  - `DOORS_PATH` 可选，默认 "C:/Program Files/IBM/Rational/DOORS/9.7/bin/doors.exe"  
    Optional: `DOORS_PATH`, default "C:/Program Files/IBM/Rational/DOORS/9.7/bin/doors.exe"
  - `DOORS_MAX_WAIT` 可选，命令最大等待秒数, 根据Doors响应速度设定合理时间  
    Optional: `DOORS_MAX_WAIT`, max command wait seconds, set according to Doors response speed

## 安装要求  
## Installation Requirements

- Python 3.11+  
- IBM DOORS 客户端（本地安装并可访问）  
  IBM DOORS client (locally installed and accessible)
- DXL 脚本支持（DOORS自带）  
  DXL script support (built-in DOORS)
- Windows 操作系统（支持DOORS客户端）  
  Windows OS (supports DOORS client)
- python-dotenv（用于环境变量管理）  
  python-dotenv (for environment variable management)

## 依赖项  
## Dependencies

- `python-dotenv>=1.1.1`（用于环境变量管理）  
  python-dotenv>=1.1.1 (for environment variable management)
- `mcp[cli]>=1.12.4`（Model Context Protocol 支持）  
  mcp[cli]>=1.12.4 (Model Context Protocol support)
- `fastmcp>=2.11.2`（MCP 服务器框架）  
  fastmcp>=2.11.2 (MCP server framework)

## 开发工具  
## Development Tools

- **FastMCP 框架**：实现MCP协议和工具注册  
  FastMCP framework: Implements MCP protocol and tool registration
- **TypedDict 数据模型**：定义结构化测试用例对象类型  
  TypedDict data model: Defines structured testcase object types
- **subprocess**：执行DOORS客户端命令和DXL脚本  
  subprocess: Executes DOORS client commands and DXL scripts
- **tempfile**：管理临时文件和目录的创建与清理  
  tempfile: Manages creation and cleanup of temp files/directories
- **traceback**：提供详细的异常堆栈跟踪信息  
  traceback: Provides detailed exception stack trace
- **logging**：记录详细的执行日志和调试信息  
  logging: Records detailed execution logs and debug info
- **python-dotenv**：加载环境变量配置文件  
  python-dotenv: Loads environment variable config files
- **os**：文件系统操作和环境变量管理  
  os: File system operations and environment variable management
- **typing_extensions**：提供额外的类型注解支持  
  typing_extensions: Provides extra type annotation support
- **typing**：提供基础类型注解支持  
  typing: Provides basic type annotation support

## 安全注意事项  
## Security Notes

- 避免在代码中硬编码敏感信息（用户名、密码等）  
  Avoid hardcoding sensitive info (username, password, etc.) in code
- 推荐使用环境变量存储认证信息，确保安全性  
  Use environment variables for credentials to ensure security
- 确保临时文件正确清理，防止敏感信息泄露  
  Ensure temp files are properly cleaned up to prevent info leaks
- 使用日志记录跟踪执行过程，但避免在日志中记录敏感信息  
  Use logs to track execution, but avoid logging sensitive info
- 确保DOORS客户端路径的正确性和安全性  
  Ensure DOORS client path is correct and secure
- 确保DOORS服务器地址的正确性和可访问性  
  Ensure DOORS server address is correct and accessible
- 确保DOORS命令执行的超时控制，防止命令挂起  
  Ensure DOORS command execution timeout to prevent hanging

## 日志记录  
## Logging

系统使用标准日志记录，会输出以下信息：  
System uses standard logging, outputs the following info:
- 认证信息来源（MCP 客户端参数或环境变量）  
  Credential source (MCP client params or environment variables)
- DOORS 路径来源（默认路径或自定义路径）  
  DOORS path source (default or custom)
- 命令执行信息（包括完整的DOORS命令）  
  Command execution info (including full DOORS command)
- 错误和异常信息（包括详细的堆栈跟踪）  
  Error and exception info (including detailed stack trace)
- DXL脚本生成和执行状态  
  DXL script generation and execution status
- 临时文件创建和清理状态  
  Temp file creation and cleanup status
- Markdown文件解析状态  
  Markdown file parsing status
- 文件大小和存在性检查结果  
  File size and existence check results
- 超时控制和执行时间信息  
  Timeout control and execution time info

## 贡献指南  
## Contribution Guide

本项目采用模块化设计，易于扩展和维护。欢迎贡献：  
This project uses modular design, easy to extend and maintain. Contributions welcome:
- 新的 MCP 工具函数  
  New MCP tool functions
- 增强的错误处理和异常恢复机制  
  Enhanced error handling and exception recovery
- 改进的日志记录和调试信息  
  Improved logging and debug info
- 更好的文档和使用示例  
  Better documentation and usage examples
- 完善测试用例和单元测试  
  Improved testcases and unit tests
- 优化资源管理（特别是临时文件处理和清理）  
  Optimized resource management (especially temp file handling and cleanup)
- 改进异常处理和错误报告机制  
  Improved exception handling and error reporting
- 增强配置管理和参数验证  
  Enhanced config management and parameter validation
- 支持更多的DOORS对象类型和属性  
  Support for more DOORS object types and attributes
- 优化Markdown解析性能和准确性  
  Optimized Markdown parsing performance and accuracy
- 支持更多的DOORS属性字段  
  Support for more DOORS attribute fields
- 改进超时控制和性能优化  
  Improved timeout control and performance optimization
