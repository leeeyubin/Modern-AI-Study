import httpx
import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server("weather-server")

def get_coordinates(city: str) -> tuple[float, float]:
    """도시 이름으로 위도/경도 반환"""
    city_coords = {
        "seoul": (37.5665, 126.9780),
        "서울": (37.5665, 126.9780),
        "busan": (35.1796, 129.0756),
        "부산": (35.1796, 129.0756),
        "sydney": (-33.8688, 151.2093),
        "new york": (40.7128, -74.0060),
        "tokyo": (35.6762, 139.6503),
        "london": (51.5074, -0.1278),
    }
    return city_coords.get(city.lower(), (37.5665, 126.9780))  # 기본값 서울


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_current_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g. Seoul, Tokyo, Sydney)",
                    }
                },
                "required": ["city"],
            },
        ),
        types.Tool(
            name="get_forecast",
            description="Get weather forecast for the next few days for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g. Seoul, Tokyo, Sydney)",
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (1-7)",
                        "default": 3,
                    },
                },
                "required": ["city"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "get_current_weather":
        city = arguments.get("city", "Seoul")
        lat, lon = get_coordinates(city)

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weathercode",
                        "timezone": "auto",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                current = data["current"]

                result = (
                    f"Current weather in {city}:\n"
                    f"- Temperature: {current['temperature_2m']}°C\n"
                    f"- Humidity: {current['relative_humidity_2m']}%\n"
                    f"- Wind Speed: {current['wind_speed_10m']} km/h\n"
                )
                return [types.TextContent(type="text", text=result)]

        except httpx.TimeoutException:
            return [types.TextContent(type="text", text="Error: Request timed out. Please try again.")]
        except httpx.HTTPError as e:
            return [types.TextContent(type="text", text=f"Error fetching weather: {str(e)}")]

    elif name == "get_forecast":
        city = arguments.get("city", "Seoul")
        days = min(int(arguments.get("days", 3)), 7)
        lat, lon = get_coordinates(city)

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                        "timezone": "auto",
                        "forecast_days": days,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                daily = data["daily"]

                lines = [f"Weather forecast for {city} ({days} days):\n"]
                for i in range(days):
                    lines.append(
                        f"{daily['time'][i]}: "
                        f"High {daily['temperature_2m_max'][i]}°C / "
                        f"Low {daily['temperature_2m_min'][i]}°C, "
                        f"Rain {daily['precipitation_sum'][i]}mm"
                    )
                return [types.TextContent(type="text", text="\n".join(lines))]

        except httpx.TimeoutException:
            return [types.TextContent(type="text", text="Error: Request timed out. Please try again.")]
        except httpx.HTTPError as e:
            return [types.TextContent(type="text", text=f"Error fetching forecast: {str(e)}")]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
