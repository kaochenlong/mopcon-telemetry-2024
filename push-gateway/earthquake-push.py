from requests_html import HTMLSession
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Registry
registry = CollectorRegistry()

# Gauge
g_earthquake = Gauge(
    "earth_quake",
    "地震規模",
    ["date"],
    registry=registry,
)

session = HTMLSession()

URL = "https://www.cwa.gov.tw/V8/C/E/index.html"

response = session.get(URL)
response.html.render(timeout=20)

rows = response.html.find(".eq_list .eq-row")

for row in reversed(rows):
    detail = row.find(".eq-detail", first=True)
    date_str = detail.find("span", first=True).text
    value = detail.find("ul li")[2].text.replace("地震規模", "")

    g_earthquake.labels(date=date_str).set(value)

    push_to_gateway("localhost:9091", job="earthquake_job", registry=registry)

print("已推送完成")
