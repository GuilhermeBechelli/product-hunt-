import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pushbullet import Pushbullet

API_KEY = '+++++++++++++++' 
pb = Pushbullet(API_KEY)

options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())

BASE_URL = "https://www.kabum.com.br/hardware/placa-de-video-vga/placa-de-video-nvidia?page={}"

def verificar_produto():
    print(" Verificando se a RTX 5090 está disponível na Kabum...")

    for pagina in range(1, 27): 
        url = BASE_URL.format(pagina)
        print(f" Verificando página {pagina}...")

       
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        
        time.sleep(5) 

        try:
           
            imagens = driver.find_elements(By.CLASS_NAME, "imageCard")  

            for img in imagens:
                nome = img.get_attribute("title").lower()  
                if "rtx 5090" in nome:  
                    produto_url = img.find_element(By.XPATH, "..").get_attribute("href") 
                    print(f" RTX 5090 encontrada na página {pagina} da Kabum! URL: {produto_url}")
                    enviar_notificacao(f" RTX 5090 disponível na Kabum! Página {pagina}. Confira aqui: {produto_url}")
                    driver.quit()
                    return 
        
            print(f" RTX 5090 não encontrada na página {pagina}.")
        
        except Exception as e:
            print(f"Erro ao verificar a página {pagina}: {e}")

        driver.quit()

def enviar_notificacao(mensagem):
    push = pb.push_note("Alerta RTX 5090", mensagem)

verificar_produto()
