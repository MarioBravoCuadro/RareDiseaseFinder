from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Configuración de Chrome
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-infobars")
options.add_argument("--disable-popup-blocking")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

def buscar_medicamento(termino):
   
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.selleckchem.com/search.html")

        # Espera explícita para el campo de búsqueda
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "searchDTO.searchParam"))
        )
        search_box.clear()
        search_box.send_keys(termino + Keys.RETURN)

        # Espera explícita para los resultados
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr[name='productList']")))

        html = driver.page_source
        driver.quit()
        return html

    except Exception as e:
        print("❌ Error:", e)
        driver.quit()
        return None

def extraer_medicamentos(html):
    soup = BeautifulSoup(html, 'html.parser')
    medicamentos = []
    filas = soup.find_all('tr', attrs={'name': 'productList'})

    for fila in filas:
        td_catalogo = fila.find('td', class_='posRel')
        catalogo = td_catalogo.get_text(strip=True) if td_catalogo else "N/A"

        enlace = fila.find('a', class_='blue f15 bold')
        nombre_producto = enlace.get_text(strip=True) if enlace else "N/A"
        link = enlace.get("href") if enlace else "N/A"

        p_tags = fila.find_all('p')
        descripcion = p_tags[1].get_text(strip=True) if len(p_tags) > 1 else "No description"

        medicamentos.append({
            "Catalog No.": catalogo,
            "Product Name": nombre_producto,
            "Link": link,
            "Description": descripcion
        })

    return medicamentos

def obtener_link_selleckchem(farmaco):
    """Obtiene el primer link relevante de Selleckchem para un fármaco
    Args:
        farmaco (str): Nombre del fármaco (ej: 'gemfibrozil')
    Returns:
        str: URL completa o None si hay error
    """
    try:
        html = buscar_medicamento(farmaco)
        if not html:
            return None

        productos = extraer_medicamentos(html)
        if productos:
            primer_link = f"www.selleckchem.com{productos[0]['Link']}"
            return primer_link
        return None

    except Exception as e:
        print(f"Error obteniendo {farmaco}: {str(e)}")
        return None
    

__all__ = ['obtener_link_selleckchem']