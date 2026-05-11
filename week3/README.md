# The AI IDE

## Three Eras of AI Coding Tools
 
| Era | Example Tools | Efficiency Gain | Mode |
|-----|--------------|-----------------|------|
| **1. Code Completion** | GitHub Copilot | ~10% | Local, Sync |
| **2. IDE Automation** | Cursor, Windsurf | ~20% | Local, Sync |
| **3. AI Software Engineer** | Devin, Codex | **6–12x** | Cloud, Async |
 
The direction of travel: **Local Development → Collaborative Cloud Agents**
 
## Sync vs. Async
 
**Synchronous**
- Single-threaded, human-in-the-loop
- You stay focused on one task
- AI works for **20 seconds – 1.5 minutes**

  
**Asynchronous**
- Multi-threaded, human delegates to AI
- You switch attention across multiple tasks
- AI works for **10 minutes – multiple hours**

## The Tool Landscape
 
```
                Sync               Async
         ┌──────────────────┬──────────────────┐
  Local  │ Windsurf         │ Claude Code      │
         │ Cursor           │                  │
         │ GitHub Copilot   │                  │
         ├──────────────────┼──────────────────┤
  Cloud  │ DeepWiki         │ Devin            │
         │                  │ Codex (OpenAI)   │
         └──────────────────┴──────────────────┘
```

## Build a Custom MCP Server

#### Weather MCP Server
- Demo 

<img width="750" src="https://github.com/user-attachments/assets/25c49a22-066d-44fa-873f-1a38cfa8e90a" />

</br>

> A Model Context Protocol (MCP) server that provides real-time weather data using the [Open-Meteo API](https://open-meteo.com/). Connect it to Claude Desktop and ask about the weather in natural language.

#### Overview

This server exposes two MCP tools:

- `get_current_weather` — current temperature, humidity, and wind speed for a city
- `get_forecast` — daily high/low temperatures and precipitation for up to 7 days

#### Claude Desktop Configuration

Add the following to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/opt/anaconda3/bin/python",
      "args": ["/absolute/path/to/week3/server/main.py"]
    }
  }
}
```

####  File Structure

```
week3/
└── server/
    └── main.py   # MCP server entrypoint
```
#### Flow
```
Claude Desktop
  → claude_desktop_config.json 읽음
  → main.py 자동 실행
  → main.py가 MCP 서버로 동작
  → Claude가 도구 목록 받아서 사용
```

1) 서버 선언
```python
server = Server("weather-server")
```

2) 도구 등록
```python
@server.list_tools()
async def list_tools():
    return [get_current_weather, get_forecast]
```

3) 도구 실행
```python
@server.call_tool()
async def call_tool(name, arguments):
    if name == "get_current_weather":
```
4) STDIO 연결

```python
async with stdio_server() as (read, write):
    await server.run(read, write, ...)
```
