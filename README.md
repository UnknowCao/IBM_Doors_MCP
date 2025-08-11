# DOORS MCP 服务器

这是一个 Model Context Protocol (MCP) 服务器，实现了与 IBM DOORS 需求管理系统的集成，使 AI 代理能够直接访问和查询 DOORS 中的需求和测试用例数据。

## 项目概述

本项目创建了一个 MCP 服务器，实现以下核心功能：
- 提供 MCP 接口供外部调用
- 实现 DOORS 测试用例数据的查询和结构化输出
- 支持通过 DXL 脚本与 DOORS 客户端交互
- 将 DOORS 数据转换为标准化 CSV 格式并解析
- 通过 MCP 工具函数提供对 AI 代理的标准化访问

## 功能特性
- ✅ 支持查询 DOORS 测试用例数据
- ✅ 支持通过 MCP 客户端传递 DOORS 客户端路径
- ✅ 使用临时文件处理 DOORS 交互结果
- ✅ 具有良好的异常处理和资源管理机制

## 系统架构

### 架构设计
- **MCP接口层**：使用FastMCP框架实现MCP协议
- **业务逻辑层**：实现DOORS数据访问逻辑和数据转换
- **数据访问层**：通过DXL脚本与DOORS客户端交互
- **资源管理层**：管理临时文件的创建和清理

### 设计模式
- 工厂模式：用于创建MCP服务器实例
- 装饰器模式：用于注册MCP工具函数
- 模板方法模式：用于定义DOORS数据访问的通用流程
- 责任链模式：用于处理异常和错误情况
- 上下文管理器：确保临时文件的正确清理

## 使用说明

### MCP 服务器配置与启动

#### 在 VS Code 中配置和启动服务器

1. **确保项目结构完整**：
   - 确保包含所有必要文件：
     - `IBM_DOORS_MCP/server.py` (服务器主文件)
     - `pyproject.toml` (项目配置)
     - `README.md` (文档说明)
     - `cline_mcp_settings.json` (MCP 服务器配置)

2. **VS Code 中启动服务器**：
   - 打开 `IBM_DOORS_MCP/server.py`
   - 在编辑器中运行以下代码片段启动服务器：
   
```python
# MCP 服务器入口，支持命令行/Inspector/Claude Desktop 启动
if __name__ == "__main__":
    mcp.run()
```

3. **通过命令行启动服务器**：
```uv
  uv run mcp dev server.py
```

4. **MCP 服务器配置注意事项**：
   - 确保 `cline_mcp_settings.json` 中的参数与服务器实现匹配
   - 特别注意 `parameters` 部分应与工具函数的参数定义一致
   - 环境变量设置应与实际 DOORS 环境匹配
   - autoApprove 列表应准确反映注册的 MCP 工具函数名称

4. **配置 MCP 客户端**：
   - 在 `cline_mcp_settings.json` 中添加以下配置：
   
```json
{
  "mcpServers": {
    "doors-mcp-server": {
      "command": "python",
      "args": ["BM_DOORS_MCP/server.py"],
      "autoApprove": [
        "get_testcases"
      ],
      "parameters": {
        "doors_path": "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe"
      }
    }
  }
}
```

5. **传递认证信息**：
   - 可选方式：
     - 通过函数参数传递：`auth={"username": "user", "password": "pass"}`
     - 通过环境变量设置：
       ```bash
       set DOORS_USERNAME=your_username
       set DOORS_PASSWORD=your_password
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
- 支持通过参数传递认证信息和 DOORS 客户端路径
- 返回结构化数据列表，便于后续处理和分析

### 参数说明

- `module_path`: DOORS 模块的路径（如 "/项目/需求模块"）
- `doors_path`: DOORS 客户端的执行路径，默认为标准安装路径

### 示例用法

```python
# 查询测试用例示例
testcases = get_testcases(
    "/项目/测试用例模块", 
    "C:\\Program Files\\IBM\\Rational\\DOORS\\9.7\\bin\\doors.exe"
)
```

## 安装要求

- Python 3.11+
- IBM DOORS 客户端（本地安装）
- DXL 脚本支持
- Windows 操作系统
- python-dotenv（用于环境变量管理）

## 依赖项

- `python-dotenv`（用于环境变量管理）
- `mcp[cli]`（Model Context Protocol 支持）
- `fastmcp`（MCP 服务器框架）

## 开发工具

- FastMCP 框架
- TypedDict 数据模型
- subprocess 执行外部命令
- tempfile 管理临时文件
- csv 解析 DOORS 输出
- logging 日志记录

## 安全注意事项

- 避免在代码中硬编码敏感信息
- 推荐使用环境变量存储认证信息
- 确保临时文件正确清理
- 使用日志记录跟踪执行过程

## 日志记录

系统使用标准日志记录，会输出以下信息：
- 认证信息来源（MCP 客户端参数或环境变量）
- DOORS 路径来源（默认路径或自定义路径）
- 命令执行信息
- 错误和异常信息

## 贡献指南

本项目采用模块化设计，易于扩展和维护。欢迎贡献：
- 新的 MCP 工具函数
- 增强的错误处理
- 改进的日志记录
- 更好的文档和示例
- 完善测试用例和单元测试
- 优化资源管理（特别是临时文件处理）
- 改进异常处理和错误报告
- 增强配置管理和参数验证

## 项目进展

当前状态和下一步计划请参考 [memory-bank/progress.md](memory-bank/progress.md) 文件。
