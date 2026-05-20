from celery import shared_task
from .models import ParseTask, Product, Site
from .tarakani import tarakan_1, tarakan_2, tarakan_3, tarakan_4, tarakan_5

PARSERS = {
    'books_children': tarakan_1.parse,
    'books_classic': tarakan_2.parse,
    'books_fantasy': tarakan_3.parse,
    'books_detective': tarakan_4.parse,
    'books_sport': tarakan_5.parse,
}

@shared_task
def run_parser(task_id, parser_key):
    try:
        task = ParseTask.objects.get(id=task_id)
        task.status = 'running'
        task.save()

        parser_func = PARSERS.get(parser_key)
        if not parser_func:
            task.status = 'error'
            task.save()
            return

        results = parser_func()
        site = Site.objects.get(parser_key=parser_key)

        category = task.categories.first()
        for item in results:
            Product.objects.create(
                task=task,
                site=site,
                category=category,
                name=item['name'],
                price=item['price'],
                url_img=item['url_img'],
            )

        task.status = 'done'
        task.save()

    except Exception as e:
        task = ParseTask.objects.get(id=task_id)
        task.status = 'error'
        task.save()
        raise e