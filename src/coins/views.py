from django.shortcuts import render
# taskmanager/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import scrape_coin_data
import uuid
#from .models import Task,Contract,OfficialLink,Social


class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        job_id = str(uuid.uuid4())
         # Store coins list in session
        request.session[f"coins_{job_id}"] = coins
        for coin in coins:
            scrape_coin_data.apply_async((coin,), task_id=f"{job_id}_{coin}")
        return Response({"job_id": job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        # Retrieve coins list from session
        coins = request.session.get(f"coins_{job_id}", [])
        print(f"Received request to check scraping status for job ID: {job_id}, coins: {coins}")
        results = []
        for coin in coins:
            result = AsyncResult(f"{job_id}_{coin}")
            print(f"Result for coin {coin}: {result.state}")
            if result.state == 'SUCCESS':
                results.append(result.result)
            else:
                results.append({"coin": coin, "status": result.state})
        print(f"Scraping status checked successfully for job ID: {job_id}")
        return Response({"job_id": job_id, "tasks": results}, status=status.HTTP_200_OK)


#after saving scraped data into models we can retrive it

# class ScrapingStatusView(APIView):
#     def get(self, request, job_id):
#         # Retrieve tasks associated with the job_id from the database
#         tasks = Task.objects.filter(scrapingjob__job_id=job_id)
        
#         results = []
#         for task in tasks:
#             # Create a dictionary to represent the task data
#             task_data = {
#                 "coin": task.coin,
#                 "output": {
#                     "price": task.price,
#                     "price_change": task.price_change,
#                     "market_cap": task.market_cap,
#                     "market_cap_rank": task.market_cap_rank,
#                     "volume": task.volume,
#                     "volume_rank": task.volume_rank,
#                     "volume_change": task.volume_change,
#                     "circulating_supply": task.circulating_supply,
#                     "total_supply": task.total_supply,
#                     "diluted_market_cap": task.diluted_market_cap,
#                     "contracts": [{"name": contract.name, "address": contract.address} for contract in task.contracts.all()],
#                     "official_links": [{"name": link.name, "link": link.link} for link in task.official_links.all()],
#                     "socials": [{"name": social.name, "url": social.url} for social in task.socials.all()]
#                 }
#             }
#             results.append(task_data)

#         return Response({"job_id": job_id, "tasks": results}, status=status.HTTP_200_OK)

