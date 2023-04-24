import aiohttp
import asyncio
import platform
import datetime


class ExchangeRatesAPI:
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates'

    async def get_exchange_rates(self, currency: str, days: int):
        exchange_rates = []
        for i in range(days):
            check_day = datetime.date.today() - datetime.timedelta(days=i)
            formatted_date = check_day.strftime("%d.%m.%Y")
            url = f"{self.BASE_URL}?json&date={formatted_date}"
            async with aiohttp.ClientSession() as session:
                response = await session.get(url)
                if response.status != 200:
                    raise ValueError(f"Failed to get exchange rates. Status code: {response.status}")
                data = await response.json()
                for rate in data['exchangeRate']:
                    if rate['currency'] == currency and len(exchange_rates) < days:
                        exchange_rates.append({
                            'date': data['date'],
                            'rate': rate['saleRateNB']
                        })
                if not exchange_rates:
                    raise ValueError(f"No exchange rates found for {currency} in the last {days} days.")
        return exchange_rates


async def main():
    api = ExchangeRatesAPI()
    try:
        currency = input("Enter currency (USD or EUR): ").upper()
        days = int(input("Enter number of days (not more than 10): "))
        if days > 10:
            raise ValueError("Number of days cannot be more than 10.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    try:
        rates = await api.get_exchange_rates(currency, days)
        print(f"Exchange rates for {currency} for the last {days} days:")
        for j in rates:
            print(f"{j['date']}: {j['rate']}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())