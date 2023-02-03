from config.models import NavigationLink
def load_base_variables(request):
    print('called context proccessors')
    return {
        'navigation_links': NavigationLink.objects.all().order_by("name")
    }