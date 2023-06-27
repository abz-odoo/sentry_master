import sys
import os

slave_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'slave'))
sys.path.append(slave_path)

import slave

# -*- coding: utf-8 -*-
import logging
import sentry_sdk as sentry
logging.getLogger(__name__).info('sentry enabled')
# We don't want sentry to send INFO/DEBUG/WARNING exception, only errors
sentry.set_level("error")

IGNORED_EXCEPTIONS = [
    # Exception ignored by sentry
    'HTTPError',
    'PoolError',
    'RedirectWarning',
    'MailDeliveryException',
    'SerializationFailure',
    'InvalidDatabaseException',
    'Forbidden',
    'UserError',
    'AccessError',
    'SignupError',
    'NumericValueOutOfRange',
    'No possible route found for incoming message from',
    'GSTIN is required under GST Treatment',
    'Signup: no name or partner given for new user',
    'Signup: no login given for new user',
    'DecompressionBombWarning',
    'DecompressionBombError', # DecompressionBombError: Image size (X pixels) exceeds limit of 178956970 pixels, could be decompression bomb DOS attack.
    'IntegrityError',
    'OperationalError',
    'invalid-request',
]

IGNORED_LOGS = [
    # Logs ignored by sentry
    'bad query:',
    'Missing model',
    'Failed to insert ir_model_data',
    'saas_trial/create_invitation: login check failed for mails',
    'saas_trial/create_invitation: secret signature checking failed for mails',
    'Error while converting to PDF/A',
    'Error when reading the pdf',
    'Error when fetching LinkedIn stats',
    'A batch of leads could not be enriched',
    'Non-stored field %s cannot be searched.',
    'Microsoft Outlook: Wrong state value',
    'An error occurred while fetching the comment'
]

IGNORED_LOGGERS = [
    # Loggers ignored by sentry
    'odoo.addons.base_automation.models.base_automation',
]

IGNORED_EXCEPTIONS_TERMS = [
    # Exception containing these terms will be ignored
    'x_studio',
]

def is_exception_ignored(exc_type, exc_value):
    for ignored_exc in IGNORED_EXCEPTIONS:
        if exc_type.__name__ == ignored_exc or ignored_exc in str(exc_value):
            return True
    return False

# This function will be called each time sentry tries to send an error.
# It is used to filter what we send and what we don't send.
# If we return None, the sending will be canceled
# We can also modify the event before sending it
def filter_data(event, hint):
    # Add the dbname tag so that it can be seen from the Sentry interface
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if is_exception_ignored(exc_type, exc_value) or getattr(exc_value, 'sentry_ignored', False):
            return None
        elif any(term in str(exc_value) for term in IGNORED_EXCEPTIONS_TERMS):
            return None
    elif 'log_record' in hint:
        if any([log in hint['log_record'].msg for log in IGNORED_LOGS]):
            return None
    if 'logger' in event:
        if event['logger'] in IGNORED_LOGGERS:
            return None
    return event

sentry.init(
    dsn='https://540c16cb2c874f3797fc696dc0b824f4@o4504729523585024.ingest.sentry.io/4504729551831040',
    traces_sample_rate=1.0,  # Set to 1.0 to capture 100% of transactions
    max_breadcrumbs=100,
    before_send=filter_data,
    # integrations=[sentry_git.GitIntegration()],
    release='test1.2')

def call():
    print("from master")
    print("calling slave from master")
    slove
    # sluve
    print(slave.call())

if __name__ == "__main__":
    call()
