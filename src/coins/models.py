from django.db import models

class Contract(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OfficialLink(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.name

class Social(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Task(models.Model):
    coin = models.CharField(primary_key=True,max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=10, null=True)
    price_change = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    market_cap = models.BigIntegerField(null=True)
    market_cap_rank = models.IntegerField(null=True)
    volume = models.BigIntegerField(null=True)
    volume_rank = models.IntegerField(null=True)
    volume_change = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    circulating_supply = models.BigIntegerField(null=True)
    total_supply = models.BigIntegerField(null=True)
    diluted_market_cap = models.BigIntegerField(null=True)
    contracts = models.ManyToManyField(Contract)
    official_links = models.ManyToManyField(OfficialLink)
    socials = models.ManyToManyField(Social)

    def __str__(self):
        return self.coin

class ScrapingJob(models.Model):
    job_id = models.UUIDField(primary_key=True)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return str(self.job_id)
