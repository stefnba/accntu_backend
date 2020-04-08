
from django.core.exceptions import ObjectDoesNotExist
from explicit import waiter, ID
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select

from accounts.models import Account
from ..models import NewImport, NewImportOneAccount

from ..providers.providers import provider_classes


from .parsing.parser import Parser
from .process_utils import pusher_trigger




def retrieve_account_transactions(
        user,
        account_id,
        task_id,
        new_import,
        importable_transactions
    ):

    try: 
        account = Account.objects.get(id=account_id)
    
    except ObjectDoesNotExist: 
        pusher_trigger(
            task_id,
            'import_error',
            "Account {} doesn't exist!".format(account_id)
        )

        # continue with next account, return zero transactions
        return []


    """
    If account exists, execute below
    """

    print(account)
    
    # create db object in model NewImportOneAccount for import of this account
    new_import_one_account = NewImportOneAccount.objects.create(
        user_id=user,
        new_import = new_import,
        account=account
    )

    # TODO what is this here?
    key = account.provider.key

    # credentials
    # TODO encryption
    login = account.login
    login_sec = account.login_sec
    pin = account.pin


    """
    Web scraping access
    """
    if account.provider.access_type == 'scr':
        transactions_raw = """ "Auftragskonto";"Buchungstag";"Valutadatum";"Buchungstext";"Verwendungszweck";"Glaeubiger ID";"Mandatsreferenz";"Kundenreferenz (End-to-End)";"Sammlerreferenz";"Lastschrift Ursprungsbetrag";"Auslagenersatz Ruecklastschrift";"Beguenstigter/Zahlungspflichtiger";"Kontonummer/IBAN";"BIC (SWIFT-Code)";"Betrag";"Waehrung";"Info"
"DE73795500000240762302";"01.04.20";"01.04.20";"FOLGELASTSCHRIFT";"STUDIENKREDIT DA14546041 AUSZAHLUNG 0,00 ZINS 8,50 TILG 23,53 APL 0,00 GEBUEHR 0,00 ";"DE44ZZZ00000002378";"9347108";"";"";"";"";"KFW                                                                   PALMENGARTENSTR. 5 - 9";"DE32500204001406328080";"KFWIDEFFXXX";"-32,03";"EUR";"Umsatz gebucht"
"DE73795500000240762302";"01.04.20";"01.04.20";"FOLGELASTSCHRIFT";"Versicherungsnr. 404086472 Beitrag Auslandsschutz ";"DE16ZZZ00000028684";"18MREF000000000962715";"DEZY1820200320015305000187186";"";"";"";"Envivas Krankenversicherung AG";"DE51370700600119081801";"DEUTDEDKXXX";"-15,50";"EUR";"Umsatz gebucht"
"DE73795500000240762302";"01.04.20";"01.04.20";"ABSCHLUSS";"Abrechnung 31.03.2020 siehe Anlage ";"";"";"";"";"";"";"";"0000000000";"79550000";"-17,89";"EUR";"Umsatz gebucht"
"DE73795500000240762302";"01.04.20";"01.04.20";"ENTGELTABSCHLUSS";"Entgeltabrechnung siehe Anlage ";"";"";"";"";"";"";"";"0000000000";"79550000";"-2,90";"EUR";"Umsatz gebucht"
"DE73795500000240762302";"31.03.20";"31.03.20";"GUTSCHR. UEBERWEISUNG";"Transferred with Deutsche Bank Mobile ";"";"";"";"";"";"";"Stefan Jakob Bauer";"DE89700700240645455700";"DEUTDEDBMUC";"50,00";"EUR";"Umsatz gebucht"
"DE73795500000240762302";"31.03.20";"31.03.20";"FOLGELASTSCHRIFT";"BILDUNGSKREDIT DA07896940 AUSZAHLUNG 0,00 ZINS 1,45 TILG 118,55 APL 0,00 GEBUEHR 0,00 ";"DE44ZZZ00000002378";"8020582";"";"";"";"";"KFW                                                                   PALMENGARTENSTR. 5 - 9";"DE32500204001406328080";"KFWIDEFFXXX";"-120,00";"EUR";"Umsatz gebucht"
 """
        
        
        
        
        
    aa = 1
    """"Kreditkarte:";"FTL Credit Card / *7734";

"Zeitraum:";"01.01.2019 - 04.04.2020";
"Saldo:";"-24,64";
"Datum:";"03.04.2020";

"Belegdatum";"Wertstellung";"Beschreibung";"Betrag (EUR)";"Ursprünglicher Betrag";"Umrechnungskurs";"Umsatz abgerechnet";
"31.03.2020";"02.04.2020";"1,75% für Einsatz der Kar";"-0,11";"";"";"Nein";
"31.03.2020";"02.04.2020";"DIGITALOCEAN.COM";"-6,54";"-7,14 USD";"1,0918";"Nein";
"29.03.2020";"30.03.2020";"Spotify";"-14,99";"";"";"Nein";
"19.03.2020";"19.03.2020";"AMZ*PMI Trading";"8,70";"";"";"Nein";"""








    """
    API access
    """
    if account.provider.access_type == 'api':
        transactions_raw = []


    """
    Parse raw transactions into importable transactions
    """

    parser = Parser(
        parser_dict=account.provider.csvxls_import.__dict__,
        file=transactions_raw,
        account={
            'account_id': account_id,
            'account_name': 'TEST_NAME'
        }
    )
    transactions_parsed = parser.parse()

    pusher_trigger(
        task_id,
        'import_process',
        '{}: transactions parsed'.format(account.title)
    )

    print(transactions_parsed)


    """
    Update account import
    """
        
    # TODO has all transaction, should be only unique ones
    new_import_one_account.import_success = True
    new_import_one_account.nmbr_transactions = len(transactions_parsed)
    new_import_one_account.save(update_fields=['import_success', 'nmbr_transactions'])

    # add importing id for each transaction
    transactions_parsed = [dict(item, **{'importing': new_import_one_account.id }) for item in transactions_parsed]


    importable_transactions.extend(transactions_parsed)









"""
def OLD():    
    Provider = provider_classes[key]

    pusher_client.trigger(task_id, pusher_event_name, {
        'message': '{}: import initiated ...'.format(account.title)
    })
        
    # actual retrival of transactions through API or scrapping
    retriever = Provider()

    # account login
    login = retriever.login(login, pin, login_sec)

    # check and execute two factor
    if hasattr(retriever, 'login_two_factor'):

        url = retriever.login_two_factor(user, account_id)

        pusher_client.trigger(task_id, pusher_event_name, {
            'message': '{}: waiting for Two-Factor Auth...'.format(account.title)
        })
        
        pusher_client.trigger(task_id, 'two_factor', {
            'two_factor': {
                'account': account_id,
                'task': task_id,
                'tan_id': url
            }
        })

        tan = wait_for_tan(user, account_id, task_id)

        if tan:
            pusher_client.trigger(task_id, pusher_event_name, {
                'message': '{}: TAN submitted...'.format(account.title)
            })
            
            retriever.login_two_factor_submit_tan(tan)
        
        else:
            login = False

            import_error(task_id, "{}: TAN submission failed!".format(account.title))
            
            # continue with next account
            return []


    if login:
        pusher_client.trigger(task_id, pusher_event_name, {
            'message': '{}: login successful!'.format(account.title)
        })

    
    # if login not successful
    else:
        import_error(task_id, "{}: login not successful!".format(account.title))
        
        # continue with next account
        return []

    transactions_raw = retriever.get_raw_transactions(import_id=new_import_one_account.pk, csv_meta=account.provider.csv_meta)

    nmbr_transactions = len(transactions_raw)
    
    if nmbr_transactions > 0:
        pusher_client.trigger(task_id, pusher_event_name, {
            'message': '{}: {} transactions retrieved'.format(account.title, len(transactions_raw))
        })

    else:
        import_error(task_id, "{}: no transactions retrieved!".format(account.title))

        # continue with next account
        return []


    

)


"""