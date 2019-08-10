from celery import shared_task


@shared_task
def do_work(list_of_work):
    for work_item in range(list_of_work):
        return work_item
    return 'work is complete'


@shared_task
def adding_task(x, y):
    return x + y