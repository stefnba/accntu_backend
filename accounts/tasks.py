from celery import shared_task, current_task, task

from .models import Account, Sub_Account

from importing.process.api.api_providers import api_providers

@task(bind=True)
def test_connection(
        self,
        account_id,
    ):
    """

    """

    account = Account.objects.select_related('provider').filter(id=account_id).first()

    APIClass = api_providers[account.provider.key]

    api = APIClass(
        account.id,
        account.login,
        account.pin
    )
    
    sub_accounts = api.save_accounts_for_sub_accounts_import()

    # Bulk create sub_accounts
    if not account.sub_accounts_retrieved:
        create = Sub_Account.objects.bulk_create([
            Sub_Account(**{**sub_account, **{'account': account}}) for sub_account in sub_accounts
        ])

        account.sub_accounts_retrieved = True
        account.save()

        print(create)
        return create


    print('ddd')
            