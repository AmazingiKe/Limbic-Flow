import os
import time
import requests
from typing import Dict, Optional, Any

class LocationDetector:
    """
    地区检测模块
    
    功能：
    - 通过 IP 地址检测用户地区
    - 获取当地时间
    - 获取当地天气信息
    - 缓存检测结果，减少 API 调用
    
    使用方法：
    detector = LocationDetector()
    location = detector.detect_location()
    local_time = detector.get_local_time(location)
    weather = detector.get_weather(location)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化地区检测器
        
        Args:
            api_key: IPStack API Key（可选）
        """
        self.api_key = api_key or os.getenv("IPSTACK_API_KEY")
        self.cache = {}
        self.cache_timeout = 3600  # 缓存 1 小时
    
    def detect_location(self, ip: Optional[str] = None) -> Dict[str, Any]:
        """
        检测用户地区
        
        Args:
            ip: IP 地址（默认为空，使用当前 IP）
        
        Returns:
            Dict: 地区信息，包含国家、城市、经纬度等
        """
        # 检查缓存
        cache_key = ip or "current"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached_data
        
        # 使用 IPStack API 检测地区
        if self.api_key:
            try:
                url = f"http://api.ipstack.com/{ip or 'check'}"
                params = {
                    "access_key": self.api_key,
                    "fields": "country_name,region_name,city,latitude,longitude,time_zone"
                }
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    location_data = response.json()
                    self.cache[cache_key] = (location_data, time.time())
                    return location_data
            except Exception:
                pass
        
        # 回退：使用默认地区
        default_location = {
            "country_name": "中国",
            "region_name": "北京",
            "city": "北京",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "time_zone": {
                "id": "Asia/Shanghai",
                "current_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
        }
        self.cache[cache_key] = (default_location, time.time())
        return default_location
    
    def get_local_time(self, location: Dict[str, Any]) -> str:
        """
        获取当地时间
        
        Args:
            location: 地区信息
        
        Returns:
            str: 当地时间字符串
        """
        if "time_zone" in location and "current_time" in location["time_zone"]:
            return location["time_zone"]["current_time"]
        
        # 回退：使用系统时间
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def get_weather(self, location: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        获取当地天气信息
        
        Args:
            location: 地区信息
        
        Returns:
            Dict: 天气信息（如果获取成功）
        """
        weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        if not weather_api_key:
            return None
        
        try:
            lat = location.get("latitude", 39.9042)
            lon = location.get("longitude", 116.4074)
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": weather_api_key,
                "units": "metric",
                "lang": "zh_cn"
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        
        return None
    
    def get_location_summary(self, location: Dict[str, Any]) -> str:
        """
        获取地区摘要信息
        
        Args:
            location: 地区信息
        
        Returns:
            str: 地区摘要
        """
        city = location.get("city", "未知城市")
        region = location.get("region_name", "未知地区")
        country = location.get("country_name", "未知国家")
        
        local_time = self.get_local_time(location)
        weather = self.get_weather(location)
        
        summary = f"{city}, {region}, {country}"
        summary += f"\n当地时间: {local_time}"
        
        if weather:
            temp = weather.get("main", {}).get("temp", "未知")
            weather_desc = weather.get("weather", [{}])[0].get("description", "未知")
            summary += f"\n天气: {weather_desc}, 温度: {temp}°C"
        
        return summary