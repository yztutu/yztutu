#!/usr/bin/env python3
"""每天把哈尔滨道里区天气写进主页 README 的标记区。数据源：Open-Meteo（免费、无需密钥）。"""
import json, re, sys, urllib.request
from datetime import datetime, timezone, timedelta

LAT, LON = 45.61187602, 126.25262277
WMO = {0:"晴",1:"多云",2:"多云",3:"阴",45:"雾",48:"雾",51:"毛毛雨",53:"毛毛雨",55:"毛毛雨",
       61:"小雨",63:"中雨",65:"大雨",66:"冻雨",67:"冻雨",71:"小雪",73:"中雪",75:"大雪",77:"雪",
       80:"阵雨",81:"阵雨",82:"暴雨",85:"阵雪",86:"阵雪",95:"雷阵雨",96:"冰雹",99:"冰雹"}

def fetch():
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
           "&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min"
           "&timezone=Asia%2FShanghai&forecast_days=1")
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

def build_line(d):
    cur = d["current"]; day = d["daily"]
    cond = WMO.get(cur["weather_code"], "未知")
    t = round(cur["temperature_2m"]); hi = round(day["temperature_2m_max"][0]); lo = round(day["temperature_2m_min"][0])
    date = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    return f"📍 哈尔滨 · 道里区：{cond}，当前 {t}℃，今天 {lo}~{hi}℃（{date} 更新）"

def main():
    line = build_line(fetch())
    path = "README.md"
    text = open(path, encoding="utf-8").read()
    new = re.sub(r"(<!-- WEATHER:START -->\n).*?(\n<!-- WEATHER:END -->)",
                 lambda m: m.group(1) + line + m.group(2), text, flags=re.S)
    if new == text:
        print("no change"); return
    open(path, "w", encoding="utf-8").write(new)
    print("updated:", line)

if __name__ == "__main__":
    main()
