# DOORS MCP 服务器

这是一个 Model Context Protocol (MCP) 服务器，通过在用户电脑中本地部署，实现了与 IBM DOORS 需求管理系统的集成，使 AI 代理和其他 MCP 客户端能够通过DXL访问和查询 DOORS 中的测试用例数据。

This is a Model Context Protocol (MCP) server, locally deployed on the user's computer, integrating with IBM DOORS requirements management system. It enables AI agents and other MCP clients to access and query testcase data in DOORS via DXL.


## 版本信息 Version information

当前版本：V1.0.3
Current version: V1.0.3

## Project overview

本项目创建了一个 Model Context Protocol (MCP) 服务器，实现以下核心功能：
- 提供 MCP 接口供外部调用
- 实现 DOORS 测试用例数据的查询和结构化输出
- 支持通过 DXL 脚本与 DOORS 客户端交互
- 将 DOORS 数据转换为标准化 Markdown 格式并解析
- 通过 MCP 工具函数提供对 AI 代理和其他 MCP 客户端的标准化访问

This project creates a Model Context Protocol (MCP) server with the following core features:
- Provides MCP interface for external calls
- Queries and outputs structured DOORS testcase data
- Supports interaction with DOORS client via DXL scripts
- Converts DOORS data to standardized Markdown format and parses it
- Provides standardized access for AI agents and other MCP clients via MCP tools


## Project Features

- **标准化接口**：基于MCP协议，支持多种客户端集成
- **安全认证**：通过环境变量管理敏感认证信息
- **资源管理**：自动管理临时文件和目录的创建与清理
- **错误处理**：完善的异常处理和详细的错误信息追踪
- **日志记录**：全面的日志记录便于调试和监控
- **类型安全**：使用TypedDict提供结构化数据类型检查
- **超时控制**：支持命令执行超时控制（100秒）
- **文件验证**：支持文件存在性和大小检查

- **Standardized interface**: MCP protocol-based, supports multiple client integrations
- **Secure authentication**: Manages sensitive credentials via environment variables
- **Resource management**: Automatically manages creation and cleanup of temp files/directories
- **Error handling**: Robust exception handling and detailed error tracking
- **Logging**: Comprehensive logging for debugging and monitoring
- **Type safety**: Uses TypedDict for structured data type checking
- **Timeout control**: Supports command execution timeout (100s)
- **File validation**: Supports file existence and size checks

## Functional Features

- ✅ 支持查询 DOORS 测试用例数据（仅限Released状态的Testcase对象）
- ✅ 支持通过 MCP 客户端传递 DOORS 客户端路径
- ✅ 使用临时文件和目录处理 DOORS 交互结果
- ✅ 具有良好的异常处理和资源管理机制
- ✅ 支持通过环境变量配置DOORS认证信息
- ✅ 提供详细的日志记录和错误信息追踪
- ✅ 支持超时控制和命令执行监控

- ✅ Supports querying DOORS testcase data (only "Released" Testcase objects)
- ✅ Supports passing DOORS client path via MCP client
- ✅ Handles DOORS interaction results with temp files/directories
- ✅ Good exception handling and resource management
- ✅ Supports DOORS authentication via environment variables
- ✅ Detailed logging and error tracking
- ✅ Supports timeout control and command execution monitoring

## System Architecture

### Architecture Design

- **MCP接口层**：使用FastMCP框架实现MCP协议，注册工具函数供外部调用
- **业务逻辑层**：实现DOORS测试用例数据访问逻辑和Markdown格式转换
- **数据访问层**：通过DXL脚本与DOORS客户端交互，生成结构化Markdown输出
- **数据解析层**：解析Markdown格式文件，转换为结构化测试用例对象
- **资源管理层**：使用tempfile模块管理临时文件的创建和自动清理
- **配置管理层**：使用python-dotenv加载环境变量配置（用户名、密码、服务器地址）
- **错误处理层**：使用traceback和logging模块进行异常处理和详细日志记录
- **超时控制层**：使用subprocess模块实现命令执行超时控制

- **MCP Interface Layer**: Implements MCP protocol with FastMCP, registers tool functions for external calls
- **Business Logic Layer**: Handles DOORS testcase data access and Markdown conversion
- **Data Access Layer**: Interacts with DOORS client via DXL scripts, generates structured Markdown output
- **Data Parsing Layer**: Parses Markdown files, converts to structured testcase objects
- **Resource Management Layer**: Uses tempfile module for temp file creation and cleanup
- **Config Management Layer**: Loads environment variables with python-dotenv (username, password, server address)
- **Error Handling Layer**: Uses traceback and logging for exception handling and detailed logs
- **Timeout Control Layer**: Uses subprocess for command execution timeout

### Design Patterns

- 工厂模式：使用FastMCP()工厂方法创建MCP服务器实例
- 装饰器模式：使用@mcp.tool()装饰器注册MCP工具函数
- 上下文管理器模式：使用tempfile.TemporaryDirectory()确保临时资源的自动清理
- 异常处理链模式：通过多层try-except和RuntimeError包装实现错误传播和上下文信息保留
- 建造者模式：通过DXL脚本构建复杂的DOORS查询命令
- 单例模式：确保MCP服务器实例的唯一性

- Factory Pattern: Uses FastMCP() factory method to create MCP server instance
- Decorator Pattern: Uses @mcp.tool() decorator to register MCP tool functions
- Context Manager Pattern: Uses tempfile.TemporaryDirectory() for automatic temp resource cleanup
- Exception Chain Pattern: Multi-layer try-except and RuntimeError wrapping for error propagation and context retention
- Builder Pattern: Builds complex DOORS query commands via DXL scripts
- Singleton Pattern: Ensures MCP server instance uniqueness

## Usage Instructions

### MCP Server Configuration & Startup

#### Configure and Start Server in VS Code

1. **MCP Server Configuration Notes:**
   - 确保 `cline_mcp_settings.json` 中的参数与服务器实现匹配
   - 特别注意 `parameters` 部分应与工具函数的参数定义一致
   - 环境变量设置应与实际 DOORS 环境匹配
   - autoApprove 列表应准确反映注册的 MCP 工具函数名称
   - 确保DOORS客户端路径在目标机器上正确安装且可访问

   - Ensure parameters in `cline_mcp_settings.json` match server implementation
   - Pay attention to `parameters` section matching tool function definitions
   - Environment variables should match actual DOORS environment
   - autoApprove list should accurately reflect registered MCP tool function names
   - Ensure DOORS client path is correctly installed and accessible on target machine

2. **Configure MCP Client:**
   - 在 `cline_mcp_settings.json` 中添加以下配置：
   - Add the following config to `cline_mcp_settings.json`:

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
        "C: //add-your-mcp-path",
        "run",
        "server.py"
      ]
    }
  }
}
```

6. **Configure username, password, server address:**
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

#### 查询测试用例
```python
testcases = get_testcases(
    module_path="/项目/测试用例模块",
    output_path="C:/person"
)
```
- `output_path` 必须为已存在的合法目录，自动生成 `output.md` 文件（如 `C:/person/output.md`），并进行内容清理和校验。
- 所有路径参数自动转换为正斜杠格式，确保 DXL 兼容。

### 工具函数特点

- 注册为 MCP 工具，可在 MCP Inspector 或 Claude Desktop 中调用
- 自动从环境变量获取 DOORS 认证信息（用户名、密码、服务器地址、DOORS_PATH、DOORS_MAX_WAIT）
- 仅返回状态为 "Released" 的 Testcase 对象
- 输出文件存在性和大小自动校验，内容自动去除空行
- 错误处理和日志记录更完善，支持详细堆栈跟踪
- 命令执行超时可通过环境变量配置（默认 1200 秒）
- 详细日志记录认证信息来源、路径、命令、异常、临时文件状态等

### 参数说明

- `module_path`: DOORS 测试用例模块路径（如 "/项目/测试用例模块"）
- `output_path`: 输出文件保存目录（如 "C:/person"），自动生成 output.md
- 环境变量配置（.env）：
  - `DOORS_USERNAME`、`DOORS_PASSWORD`、`DOORS_SERVERADDR` 必填
  - `DOORS_PATH` 可选，默认 "C:/Program Files/IBM/Rational/DOORS/9.7/bin/doors.exe"
  - `DOORS_MAX_WAIT` 可选，命令最大等待秒数, 根据Doors响应速度设定合理时间

## 安装要求

- Python 3.11+
- IBM DOORS 客户端（本地安装并可访问）
- DXL 脚本支持（DOORS自带）
- Windows 操作系统（支持DOORS客户端）
- python-dotenv（用于环境变量管理）

## 依赖项

- `python-dotenv>=1.1.1`（用于环境变量管理）
- `mcp[cli]>=1.12.4`（Model Context Protocol 支持）
- `fastmcp>=2.11.2`（MCP 服务器框架）
- `psutil>=7.0.0`（用于系统资源监控和进程管理）

## 开发工具

- **FastMCP 框架**：实现MCP协议和工具注册
- **TypedDict 数据模型**：定义结构化测试用例对象类型
- **subprocess**：执行DOORS客户端命令和DXL脚本
- **tempfile**：管理临时文件和目录的创建与清理
- **traceback**：提供详细的异常堆栈跟踪信息
- **logging**：记录详细的执行日志和调试信息
- **python-dotenv**：加载环境变量配置文件
- **os**：文件系统操作和环境变量管理
- **typing_extensions**：提供额外的类型注解支持
- **typing**：提供基础类型注解支持

## 安全注意事项

- 避免在代码中硬编码敏感信息（用户名、密码等）
- 推荐使用环境变量存储认证信息，确保安全性
- 确保临时文件正确清理，防止敏感信息泄露
- 使用日志记录跟踪执行过程，但避免在日志中记录敏感信息
- 确保DOORS客户端路径的正确性和安全性
- 确保DOORS服务器地址的正确性和可访问性
- 确保DOORS命令执行的超时控制，防止命令挂起

## 日志记录

系统使用标准日志记录，会输出以下信息：
- 认证信息来源（MCP 客户端参数或环境变量）
- DOORS 路径来源（默认路径或自定义路径）
- 命令执行信息（包括完整的DOORS命令）
- 错误和异常信息（包括详细的堆栈跟踪）
- DXL脚本生成和执行状态
- 临时文件创建和清理状态
- Markdown文件解析状态
- 文件大小和存在性检查结果
- 超时控制和执行时间信息

## 贡献指南

本项目采用模块化设计，易于扩展和维护。欢迎贡献：
- 新的 MCP 工具函数
- 增强的错误处理和异常恢复机制
- 改进的日志记录和调试信息
- 更好的文档和使用示例
- 完善测试用例和单元测试
- 优化资源管理（特别是临时文件处理和清理）
- 改进异常处理和错误报告机制
- 增强配置管理和参数验证
- 支持更多的DOORS对象类型和属性
- 优化Markdown解析性能和准确性
- 支持更多的DOORS属性字段
- 改进超时控制和性能优化

---
