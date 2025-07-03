import requests
from bs4 import BeautifulSoup

def get_blackrock_data():
    url = "https://bitbo.io/treasuries/blackrock-ibit/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraer datos según clases específicas
    # Variables no utilizadas actualmente
    # entity = soup.find("td", class_="td-company").get_text(strip=True)
    # country = soup.find("td", class_="td-location").find("img")["data-tooltip"]
    # symbol = soup.find("td", class_="td-symbol").get_text(strip=True)
    
    # Variables utilizadas
    btc = soup.find("td", class_="td-company_btc").get_text(strip=True)
    usd = soup.find("td", class_="td-value").get_text(strip=True)
    
    # Extraer la fecha (Jun 30, 2025)
    date_element = soup.find("td", class_="right-align", attrs={"sorttable_customkey": "1"})
    date = date_element.find("span").get_text(strip=True) if date_element else "N/A"
    
    # Extraer el cambio numérico (1,044.9)
    change_element = soup.find("td", class_="right-align green")
    change = change_element.find("span").get_text(strip=True) if change_element else "N/A"

    # Cálculo no utilizado actualmente
    # btc_float = float(btc.replace(",", ""))
    # percentage = f"{btc_float / 21_000_000 * 100:.2f}% of all BTC"

    return btc, usd, change, date