import requests


import aiohttp
import asyncio
from functools import lru_cache

API_KEY = "1cbf752b50797f121c5b7f97f334e9cc"

# -------------------------------
# Async Fetch Function
# -------------------------------
async def fetch_weather_async(lat, lon, date):
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            
            # Simplified: take first available forecast
            weather = data["list"][0]
            
            return {
                "Temperature": weather["main"]["temp"]
            }
        
# -------------------------------
# Cached Wrapper
# -------------------------------
cache = {}

async def get_weather(lat, lon, date):
    key = (lat, lon, date)
    
    if key in cache:
        return cache[key]
    
    data = await fetch_weather_async(lat, lon, date)
    cache[key] = data
    
    return data