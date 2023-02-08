from locations.models import City, State
from dispensaries.models import Dispensary
from dutchie.scraping import build_webdriver, load_dispensaries
#so basically queue up the locations we want to run for
for city in City.objects.filter(state=State.objects.filter(code='MI')[0])[10:]:
    driver = build_webdriver()
    if not city.state.legal:
        continue
    print(f"Loading dispensaries for {str(city)}")
    dispos = load_dispensaries(driver, str(city))
    print(f"Found {len(dispos.keys())} in {str(city)}")

    for dispo, data in dispos.items():

        if len([x for x in Dispensary.objects.filter(name=dispo, url=data['url'])]) ==0: #basically prevent us from having duplicate dispensaries

            dispensary = Dispensary()
            dispensary.name=dispo
            dispensary.save()
            dispensary.city.add(city)
            dispensary.image=data['image']
            dispensary.url=data['url']
        else:
            dispensary= Dispensary.objects.get(name=dispo, url=data['url'])
            dispensary.image = data['image']
            dispensary.url = data['url']
        dispensary.save()


# name=models.CharField(max_length=150, null=False)
#     city=models.ForeignKey(City,null=False, on_delete=models.CASCADE)
#     url=models.CharField(max_length=500, null=False)
#     image = models.CharField(max_length=500, null=True)