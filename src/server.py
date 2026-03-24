import os

import httpx
from dotenv import find_dotenv, load_dotenv

# minimal_server.py
from fastmcp import FastMCP

mcp = FastMCP(name="mcp1ccloudru")

# Load environment variables from .env if present
load_dotenv(find_dotenv())

HTTP_TIMEOUT_SECONDS = float(os.getenv("MCP_HTTP_TIMEOUT_SECONDS", "300"))

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
    base_url = os.getenv(
        "MCP_API_URL",
        "",
    ).rstrip("/")
    url = f"{base_url}/AIExchangeMCPNomenclatureKind"
    auth = httpx.BasicAuth(
        username=os.getenv("MCP_API_USERNAME", ""),
        password=os.getenv("MCP_API_PASSWORD", ""),
    )
    
    try:
        async with httpx.AsyncClient(
            timeout=HTTP_TIMEOUT_SECONDS,
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
    base_url = os.getenv(
        "MCP_API_URL",
        "",
    ).rstrip("/")
    url = f"{base_url}/AIExchangeMCPNomenclature"
    auth = httpx.BasicAuth(
        username=os.getenv("MCP_API_USERNAME", ""),
        password=os.getenv("MCP_API_PASSWORD", ""),
    )
    
    payload = {"ВидНоменклатуры": kind}
    headers = {"Content-Type": "application/json"}
    
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS, verify=False) as client:
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


@mcp.tool()
async def get_fixed_assets() -> dict:
    """  
    Здесь хранится информация про основные средства
    """
    base_url = os.getenv(
        "MCP_API_URL",
        "",
    ).rstrip("/")
    url = f"{base_url}/FixedAssets"
    auth = httpx.BasicAuth(
        username=os.getenv("MCP_API_USERNAME", ""),
        password=os.getenv("MCP_API_PASSWORD", ""),
    )

    try:
        async with httpx.AsyncClient(
            timeout=HTTP_TIMEOUT_SECONDS,
            verify=False
        ) as client:
            response = await client.get(url, auth=auth)
            response.raise_for_status()

            data = response.json()
            return {
                "success": True,
                "status_code": response.status_code,
                "data": data
            }

    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"⚠️ Ошибка: {str(e)}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        return {
            "success": False,
            "error": f"⚠️ Ошибка: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"⚠️ Ошибка: {str(e)}",
            "details": str(e)
        }


@mcp.tool()
async def vendorinvoice(month_date: str) -> dict:
    """
    Здесь можно получить информацию по документам Приобретение товаров и услуг. 
    Что бы получить информацию необходимо указать месяц (MounthDate) за который будут получать данные, 
    если пользователь не указал месяц и год, то необходимо уточнить у пользователя. 
    Поле MounthDate передавай в формате ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ), то есть 1-ое число нужного месяца.
    """
    if not month_date:
        return {
            "success": False,
            "error": "Не указан месяц за который нужно получить информацию."
        }

    base_url = os.getenv(
        "MCP_API_URL",
        "",
    ).rstrip("/")
    url = f"{base_url}/VendorIinvoice"
    auth = httpx.BasicAuth(
        username=os.getenv("MCP_API_USERNAME", ""),
        password=os.getenv("MCP_API_PASSWORD", ""),
    )

    payload = {"MounthDate": month_date}
    headers = {"Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS, verify=False) as client:
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

    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }


@mcp.tool()
async def serviceandassets(month_date: str) -> dict:
    """
    здесь можно получить информацию по документам Приобретение услуг и прочих активов. 
    Что бы получить информацию необходимо указать месяц (MounthDate) за который будут получать данные, 
    если пользователь не указал месяц и год, то необходимо уточнить у пользователя. 
    Поле MounthDate передавай в формате ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ), то есть 1-ое число нужного месяца.
    """
    if not month_date:
        return {
            "success": False,
            "error": "Не указан месяц за который нужно получить информацию."
        }

    base_url = os.getenv(
        "MCP_API_URL",
        "",
    ).rstrip("/")
    url = f"{base_url}/ServiceAndAssets"
    auth = httpx.BasicAuth(
        username=os.getenv("MCP_API_USERNAME", ""),
        password=os.getenv("MCP_API_PASSWORD", ""),
    )

    payload = {"MounthDate": month_date}
    headers = {"Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS, verify=False) as client:
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

    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }


@mcp.tool()
async def bankaccountpaymentsoutgoing(month_date: str) -> dict:
    """
    здесь можно получить информацию по документам Списание безналичных денежных средств. 
    Что бы получить информацию необходимо указать месяц (MounthDate) за который будут получать данные, 
    если пользователь не указал месяц и год, то необходимо уточнить у пользователя. 
    Поле MounthDate передавай в формате ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ), то есть 1-ое число нужного месяца.
    """
    if not month_date:
        return {
            "success": False,
            "error": "Не указан месяц за который нужно получить информацию."
        }

    base_url = os.getenv(
        "MCP_API_URL",
        "",
    ).rstrip("/")
    url = f"{base_url}/BankAccountPaymentsOutgoing"
    auth = httpx.BasicAuth(
        username=os.getenv("MCP_API_USERNAME", ""),
        password=os.getenv("MCP_API_PASSWORD", ""),
    )

    payload = {"MounthDate": month_date}
    headers = {"Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS, verify=False) as client:
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

    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }


@mcp.tool()
async def bankaccountpaymentsincoming(month_date: str) -> dict:
    """
    здесь можно получить информацию по документам Поступление безналичных денежных средств. 
    Что бы получить информацию необходимо указать месяц (MounthDate) за который будут получать данные, 
    если пользователь не указал месяц и год, то необходимо уточнить у пользователя. 
    Поле MounthDate передавай в формате ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ), то есть 1-ое число нужного месяца.
    """
    if not month_date:
        return {
            "success": False,
            "error": "Не указан месяц за который нужно получить информацию."
        }

    base_url = os.getenv(
        "MCP_API_URL",
        "",
    ).rstrip("/")
    url = f"{base_url}/BankAccountPaymentsIncoming"
    auth = httpx.BasicAuth(
        username=os.getenv("MCP_API_USERNAME", ""),
        password=os.getenv("MCP_API_PASSWORD", ""),
    )

    payload = {"MounthDate": month_date}
    headers = {"Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS, verify=False) as client:
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

    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"❌ Ошибка: {str(e)}",
            "details": str(e)
        }

if __name__ == "__main__":
    mcp.run( transport="streamable-http",  # транспорт (streamable-http или sse)
        host="0.0.0.0",               # адрес
        port=os.getenv("PORT", 8000))
