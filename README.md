# Scraping-

Idea of the project -  Scrape the data from https://coinmarketcap.com/ and display on a website 
Tech stack used - selenium, beautiful soup, celery, djangorestframework


There are be 2 APIs in django rest:

1) /api/taskmanager/start_scraping [POST]-  this will take in a list payload [“DUKO”, “NOT”, “GORILLA”] which are names of the crypto coins and submit a scraping job(celery will be used) to be run for these coins parallely and return back a job id

![image](https://github.com/Shivani505001/Scraping-/assets/98374589/d3f6213c-847b-4b18-b92a-3184a7570420)

![image](https://github.com/Shivani505001/Scraping-/assets/98374589/10548c42-7344-48e7-8a75-490e7e1ad676)


2) /api/taskmanager/scraping_status/<job_id> [GET] - From the job_id received in the previous API, we can query this API and it will return the currently scraped data for that job. Sample output:

Scraped data in jupyter notebook :
![image](https://github.com/Shivani505001/Scraping-/assets/98374589/3e19ecda-9d8b-4abe-8ea7-e3394860aa30)


The basic implementation is user sends a post request with the coin names and a job id is generated. This job id is then stored in database along with sending coin names to selenium code where the data is scraped and this data should be stored in database. Then the stored data is retrived and showed in 2nd api. 

At the moment the project is not yet finished, I tried to retrive the scraped data without storing in database but I couldn't do it efficiently so I have yet to properly store the scraped data in database and saving will be done in tasks.py file then from here in views.py the data should be retirved for 2nd api.
