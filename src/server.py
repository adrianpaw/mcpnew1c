import os
import httpx

# minimal_server.py
from fastmcp import FastMCP

mcp = FastMCP(name="mcp1ccloudru")

@mcp.tool()
async def test() -> str:
    return "Hello from MCP 1233!"

@mcp.tool()
async def get_nomenclature_kinds_json() -> dict:
    """
    Получить виды номенклатуры из 1C API в формате JSON
    
    Returns:
        Словарь с данными от API или сообщение об ошибке
    """
    url = "https://vds180.1cbit.ru/demo_erpuso_25/hs/AIExchangeAPI/AIExchangeMCPNomenclatureKind"
    auth = httpx.BasicAuth(username="web", password="123")
    
    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            verify=False
        ) as client:
            response = await client.get(url, auth=auth)
            response.raise_for_status()
            
            # Парсим JSON
            data = response.json()
            return {
                "success": True,
                "status_code": response.status_code,
                "data": data
            }
            
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"HTTP ошибка {e.response.status_code}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        return {
            "success": False,
            "error": "Ошибка сети",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Неожиданная ошибка",
            "details": str(e)
        }

@mcp.tool()
async def get_nomenclature_details(kind: str = "Оборудование") -> dict:
    """
    Получить детальную информацию о номенклатуре, 
    перед этим уточни по какому виду номенклатуры искать, 
    либо покажи какие есть виды в инструменте get_nomenclature_kinds_json
    
    Args:
        kind: Вид номенклатуры
    """
    url = "https://vds180.1cbit.ru/demo_erpuso_25/hs/AIExchangeAPI/AIExchangeMCPNomenclature"
    auth = httpx.BasicAuth(username="web", password="123")
    
    payload = {"ВидНоменклатуры": kind}
    headers = {"Content-Type": "application/json"}
    
    try:
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.post(url, auth=auth, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()  
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": data
                }
            else:
                return f"❌ Ошибка: {response.status_code} - {response.text}"
                
    except Exception as e:
        return f"⚠️ Ошибка: {str(e)}"

if __name__ == "__main__":
    mcp.run( transport="streamable-http",  # транспорт (streamable-http или sse)
        host="0.0.0.0",               # адрес
        port=os.getenv("PORT", 8000))