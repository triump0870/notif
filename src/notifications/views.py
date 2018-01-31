from django.shortcuts import render

# Create your views here.
from uuid import uuid4

from urllib.parse import urlparse
from  django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as django_settings
from scrapyd_api import ScrapydAPI
from notifications.models import Item

# connect scrapyd service
scrapyd = ScrapydAPI(django_settings.SCRAPPY_SERVER)


def is_valid_url(url):
    try:
        URLValidator(url)
    except ValidationError:
        return False

    return True


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def crawl(request):
    # For new crawling tasks
    if request.method == 'POST':
        url = request.POST.get('url', None)
        print("here is: ", request.POST)
        if not url:
            return JsonResponse({'error': 'Missing URL args'})

        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is not valid'})

        domain = urlparse(url).netloc  # parse the url and extract the domain
        unique_id = str(uuid4())

        print("domain: ", domain)
        # settings for scrappy spider
        settings = {
            'unique_id': unique_id,
            'USER_AGENT': django_settings.USER_AGENT
        }

        # schedule crawling task from scrapyd
        task = scrapyd.schedule('default', 'crawler', settings=settings, url=url, domain=domain)
        return JsonResponse({
            'task_id': task,
            'unique_id': unique_id,
            'status': 'STARTED'
        })

    # Get the result for a particular task
    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        print(request.GET, unique_id)
        if not task_id and not unique_id:
            return JsonResponse({'error': 'Missing args'})

        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                item = Item.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as ex:
                return JsonResponse({'error': str(ex)})

        else:
            return JsonResponse({'status': status})
