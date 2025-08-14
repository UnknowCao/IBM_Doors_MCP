# DOORS MCP 服务器

这是一个 Model Context Protocol (MCP) 服务器，实现了与 IBM DOORS 需求管理系统的集成，使 AI 代理和其他 MCP 客户端能够直接访问和查询 DOORS 中的测试用例数据。


## 版本信息
当前版本：V1.0.1

## 项目概述

本项目创建了一个 Model Context Protocol (MCP) 服务器，实现以下核心功能：
- 提供 MCP 接口供外部调用
- 实现 DOORS 测试用例数据的查询和结构化输出
- 支持通过 DXL 脚本与 DOORS 客户端交互
- 将 DOORS 数据转换为标准化 Markdown 格式并解析
- 通过 MCP 工具函数提供对 AI 代理和其他 MCP 客户端的标准化访问

## 项目状态
- [x] 核心功能实现
- [x] Markdown格式解析
- [x] 错误处理完善
- [x] 文档更新完成
- [ ] 单元测试待完善
- [ ] 性能优化待进行

## 项目特点
- **标准化接口**：基于MCP协议，支持多种客户端集成
- **安全认证**：通过环境变量管理敏感认证信息
- **资源管理**：自动管理临时文件和目录的创建与清理
- **错误处理**：完善的异常处理和详细的错误信息追踪
- **日志记录**：全面的日志记录便于调试和监控
- **类型安全**：使用TypedDict提供结构化数据类型检查
- **超时控制**：支持命令执行超时控制（100秒）
- **文件验证**：支持文件存在性和大小检查

## 功能特性
- ✅ 支持查询 DOORS 测试用例数据（仅限Released状态的Testcase对象）
- ✅ 支持通过 MCP 客户端传递 DOORS 客户端路径
- ✅ 使用临时文件和目录处理 DOORS 交互结果
- ✅ 具有良好的异常处理和资源管理机制
- ✅ 支持通过环境变量配置DOORS认证信息
- ✅ 提供详细的日志记录和错误信息追踪
- ✅ 支持超时控制和命令执行监控

## 系统架构

### 架构设计
- **MCP接口层**：使用FastMCP框架实现MCP协议，注册工具函数供外部调用
- **业务逻辑层**：实现DOORS测试用例数据访问逻辑和Markdown格式转换
- **数据访问层**：通过DXL脚本与DOORS客户端交互，生成结构化Markdown输出
- **数据解析层**：解析Markdown格式文件，转换为结构化测试用例对象
- **资源管理层**：使用tempfile模块管理临时文件的创建和自动清理
- **配置管理层**：使用python-dotenv加载环境变量配置（用户名、密码、服务器地址）
- **错误处理层**：使用traceback和logging模块进行异常处理和详细日志记录
- **超时控制层**：使用subprocess模块实现命令执行超时控制

### 设计模式
- 工厂模式：使用FastMCP()工厂方法创建MCP服务器实例
- 装饰器模式：使用@mcp.tool()装饰器注册MCP工具函数
- 上下文管理器模式：使用tempfile.TemporaryDirectory()确保临时资源的自动清理
- 异常处理链模式：通过多层try-except和RuntimeError包装实现错误传播和上下文信息保留
- 建造者模式：通过DXL脚本构建复杂的DOORS查询命令
- 单例模式：确保MCP服务器实例的唯一性

## 使用说明

### MCP 服务器配置与启动

#### 在 VS Code 中配置和启动服务器

1. **确保项目结构完整**：
   - 确保包含所有必要文件：
     - `IBM_DOORS_MCP/server.py` (服务器主文件)
     - `IBM_DOORS_MCP/pyproject.toml` (项目配置)
     - `README.md` (文档说明)
     - `cline_mcp_settings.json` (MCP 服务器配置)

2. **VS Code 中启动服务器**：
   - 打开 `IBM_DOORS_MCP/server.py`
   - 在编辑器中右键选择"Run Python File in Terminal"或按F5运行文件
   - 服务器将在终端中启动并等待MCP客户端连接

3. **通过命令行启动服务器**：
```bash
uv run mcp dev IBM_DOORS_MCP/server.py
```

4. **MCP 服务器配置注意事项**：
   - 确保 `cline_mcp_settings.json` 中的参数与服务器实现匹配
   - 特别注意 `parameters` 部分应与工具函数的参数定义一致
   - 环境变量设置应与实际 DOORS 环境匹配
   - autoApprove 列表应准确反映注册的 MCP 工具函数名称
   - 确保DOORS客户端路径在目标机器上正确安装且可访问

5. **配置 MCP 客户端**：
   - 在 `cline_mcp_settings.json` 中添加以下配置：
   
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
      在项目根目录下创建`.env`文件，并在文件中配置DOORS认证信息，程序会自动从环境变量中获取相关信息：
      ```
      DOORS_USERNAME=your_account_name
      DOORS_PASSWORD=your_password
      DOORS_SERVERADDR=your_Doors_serveradd(1234@doors.xxxxxx.local)
      ```

### MCP 工具函数

#### 查询测试用例
```python
testcases = get_testcases(
    module_path="/项目/测试用例模块", 
    doors_path="C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe"
)
```

### 工具函数特点
- 被注册为 MCP 工具，可以在 MCP Inspector 或 Claude Desktop 中调用
- 支持通过参数传递DOORS客户端路径
- 从环境变量自动获取DOORS认证信息（用户名、密码、服务器地址）
- 返回结构化测试用例数据列表，包含ID、URL、描述、步骤和预期结果
- 仅返回状态为"Released"的测试用例对象
- 提供详细的错误信息和堆栈跟踪
- 支持超时控制和命令执行监控（100秒超时）
- 支持文件存在性和大小检查

### 参数说明
- `module_path`: DOORS 测试用例模块的路径（如 "/项目/测试用例模块"）
- `doors_path`: DOORS 客户端的执行路径，默认为 "C:\Program Files\IBM\Rational\DOORS\9.7\bin\doors.exe"

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
