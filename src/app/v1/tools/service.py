from typing import TypedDict
import httpx
from src.core.config import settings
from fastapi import HTTPException

class CurrencyConversionResult(TypedDict):
    fromCurrency: str
    toCurrency: str
    amount: float

class ToolsService:

    async def convert_currencies(self, amount: float, from_currency: str, to_currency: str) -> CurrencyConversionResult:
        """
        Converts an amount from one currency to another using the ExchangeRate-API.
        
        This tool is useful for calculating real-time exchange rates between different 
        countries using ISO 4217 3-letter codes.

        Args:
            amount (float): The numeric value to convert (e.g., 100, 12.50).
            from_currency (str): Base currency in ISO 4217 3-letter code format (e.g., 'USD', 'EUR').
            to_currency (str): Target currency in ISO 4217 3-letter code format (e.g., 'COP', 'MXN').

        Returns:
            CurrencyConversionResult: A dictionary containing 'fromCurrency', 'toCurrency', and the converted 'amount' rounded to 2 decimal places.

        Raises:
            HTTPException: If the external API fails or returns an invalid status.
        """
        url = f"{settings.EXCHANGE_RATE_BASE_URL}/{settings.EXCHANGE_RATE_API_KEY}/pair/{from_currency}/{to_currency}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=502, 
                    detail=f"Failed to fetch exchange rate: {exc}"
                )

        data = response.json()

        if data.get("result") != "success":
            raise HTTPException(
                status_code=400, 
                detail="Failed to fetch exchange rate from provider"
            )

        conversion_rate = data.get("conversion_rate", 0.0)
        total = amount * conversion_rate
        total_fixed = round(total, 2)

        print(f"[ToolsService] Converted {amount} {from_currency} to {total_fixed} {to_currency} at rate {conversion_rate}")

        return CurrencyConversionResult(
            fromCurrency=from_currency,
            toCurrency=to_currency,
            amount=total_fixed
        )