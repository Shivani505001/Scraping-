#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver 
#from selenium.webdriver.chrome.options import Options
import time 


# In[13]:


#options = Options()


# In[14]:


#url="https://coinmarketcap.com/"





# In[29]:


from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# In[128]:


from selenium.webdriver.support import expected_conditions as EC
class CoinMarketCapScraper:
    def __init__(self, coin):
        self.coin = coin
        self.url = f"https://coinmarketcap.com/currencies/{coin}/"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    
    def get_coin_data(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10) 
       
        try:
            # Wait for the price element to be loaded in the DOM
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.sc-d1ede7e3-0.fsQm.base-text"))
            )
        except Exception as e:
            self.driver.quit()
            return None
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        data = {}

        # Extract price
        try:
            price_element = soup.select_one('span.sc-d1ede7e3-0.fsQm.base-text')
            data['price'] = price_element.text if price_element else None
        except Exception as e:
            data['price'] = None
            
         # Extract price change
        try:
            price_change_element = soup.select_one('p[data-change="down"].sc-71024e3e-0.sc-58c82cf9-1.ihXFUo.iPawMI')
            if price_change_element:
                # Split the text content by "%" and take the first part
                price_change_text = price_change_element.text
                data['price_change'] = price_change_text.split("%")[0]
            else:
                data['price_change'] = None
        except Exception as e:
            data['price_change'] = None
            
      # Find the market cap rank and volume rank

        try:
            rank_elements = soup.find_all('span', class_='text slider-value rank-value')
            if rank_elements:
                data['market_cap_rank'] = rank_elements[0].text.strip()
                data['volume_rank'] = rank_elements[1].text.strip() if len(rank_elements) > 1 else None
            else:
                market_cap_rank = None
                volume_rank = None
        except Exception as e:
            print(f"Error occurred while extracting rank values: {e}")
            market_cap_rank = None
            volume_rank = None

        #volume and market_cap
        try:
            volume = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')
            if volume:
                # Extract the text content of the element
                data['market_cap']= volume[0].text.strip().split('%')[1]
                data['volume']=volume[1].text.strip().split('%')[1] if len(rank_elements) > 1 else None
                data['volume_change']=volume[2].text.strip()
                data['circulating_supply']=volume[3].text.strip()
                data['total_supply']=volume[5].text.strip()
                data['diluted_market_cap']=volume[6].text.strip()
            else:
                data['volume'] = None
                data['market_cap'] = None
                data['volume_change']=None
                data['circulating_supply']=None
                data['total_supply']=None
                data['diluted_market_cap']=None
        except Exception as e:
            print(f"Error occurred while extracting rank values: {e}")
            data['volume'] = None
            data['market_cap'] = None
            data['volume_change']=None
            data['circulating_supply']=None
            data['total_supply']=None
            data['diluted_market_cap']=None
        #extract contracts 
        try:
            contracts_elements = soup.find_all('span', class_='sc-71024e3e-0 dEZnuB')
            addresses_elements = soup.find_all('span', class_='sc-71024e3e-0 eESYbg address')
    
            contracts = []
            for contract_element, address_element in zip(contracts_elements, addresses_elements):
                name = contract_element.text.strip().split(':')[0]  # Extract the name
                address = address_element.text.strip()             # Extract the address
                contracts.append({'name': name, 'address': address})

            data['contracts'] = contracts
        except Exception as e:
            print(f"Error occurred while extracting contract values: {e}")
            data['contracts'] = []
    
        
        # Extract official links and socials
        try:
            links_section_elements = soup.find_all('div', class_='sc-d1ede7e3-0 jTYLCR')
        
            for section_element in links_section_elements:
                # Check if the section contains official links or socials
                title_element = section_element.find('span', class_='base-text', attrs={'data-role': 'title'})
                if title_element:
                    section_title = title_element.text.strip()
                    if section_title == 'Official links':
                        # Extract official links
                        official_links_elements = section_element.find_all('a', rel='nofollow noopener', target='_blank')
                        official_links = [{'name': link.text.strip(), 'link': link['href']} for link in official_links_elements]
                        data['official_links'] = official_links
                    elif section_title == 'Socials':
                        # Extract socials
                        socials_elements = section_element.find_all('a', rel='nofollow noopener', target='_blank')
                        socials = [{'name': social.text.strip(), 'url': social['href']} for social in socials_elements]
                        data['socials'] = socials
        except Exception as e:
            data['official_links'] = []
            data['socials'] = []
        return data
        
    def close(self):
        self.driver.quit()







