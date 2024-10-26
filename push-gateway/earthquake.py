from requests_html import HTMLSession

session = HTMLSession()

URL = "https://www.cwa.gov.tw/V8/C/E/index.html"

response = session.get(URL)
response.html.render(timeout=20)

rows = response.html.find(".eq_list .eq-row")
output = f"{"日期":15}地震規模\n"
for row in reversed(rows):
    detail = row.find(".eq-detail", first=True)
    date_str = detail.find("span", first=True).text
    value = detail.find("ul li")[2].text.replace("地震規模", "")

    output += f"{date_str:15} {value}\n"

print(output)
