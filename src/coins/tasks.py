from celery import shared_task
from .coinmarketcap import CoinMarketCapScraper
from django.apps import apps
import logging
logger = logging.getLogger(__name__)

@shared_task
def scrape_coin_data(coin):
    scraper = CoinMarketCapScraper(coin)
    try:
        data = scraper.get_coin_data()
        logger.info(f"Scraped data for coin {coin}: {data}")
        scraper.close()
        return data
    except Exception as e:
        logger.exception(f"Error occurred while scraping data for coin {coin}: {e}")
        raise


#save to database 
# @shared_task
# def scrape_coin_data(coin_name, job_id):
#     Task = apps.get_model('coins', 'Task')
#     Contract = apps.get_model('coins', 'Contract')
#     OfficialLink = apps.get_model('coins', 'OfficialLink')
#     Social = apps.get_model('coins', 'Social')
#     ScrapingJob = apps.get_model('coins', 'ScrapingJob')

#     logger.info(f"Received task to scrape data for coin: {coin_name} for job ID: {job_id}")
#     scraper = CoinMarketCapScraper(coin_name)
#     try:
#         data = scraper.get_coin_data()
#         contracts = [Contract.objects.create(name=contract['name'], address=contract['address']) for contract in data['contracts']]
#         official_links = [OfficialLink.objects.create(name=link['name'], link=link['link']) for link in data['official_links']]
#         socials = [Social.objects.create(name=social['name'], url=social['url']) for social in data['socials']]
#         task = Task.objects.create(
#             coin=coin_name,
#             price=data['price'],
#             price_change=data['price_change'],
#             market_cap=data['market_cap'],
#             market_cap_rank=data['market_cap_rank'],
#             volume=data['volume'],
#             volume_rank=data['volume_rank'],
#             volume_change=data['volume_change'],
#             circulating_supply=data['circulating_supply'],
#             total_supply=data['total_supply'],
#             diluted_market_cap=data['diluted_market_cap']
#         )
#         task.contracts.set(contracts)
#         task.official_links.set(official_links)
#         task.socials.set(socials)

#         scraping_job, _ = ScrapingJob.objects.get_or_create(job_id=job_id)
#         scraping_job.tasks.add(task)
        
#         logger.info(f"Scraped data for coin {coin_name} for job ID {job_id} saved: {task}")
#         scraper.close()
#         return task.coin
#     except Exception as e:
#         logger.exception(f"Error occurred while scraping data for coin {coin_name} for job ID {job_id}: {e}")
#         raise