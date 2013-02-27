#coding=utf-8
from __future__ import unicode_literals

# List of all the 24 currencies supported by PayPal
# All this should be used for validation purpuses before
# sending a request to PayPAl through the API
CURRENCIES_INFO= {
    'AUD': {'name': 'Australian Dollar', 'only_in_country': False, 'express_checkout': True},
    'BRL': {'name': 'Brazilian Real', 'only_in_country': True, 'country': 'BR', 'express_checkout': False},
    'CAD': {'name': 'Canadian Dollar', 'only_in_country': False,'express_checkout': True},
    'CZK': {'name': 'Czech Koruna', 'only_in_country': False,'express_checkout': True},
    'DKK': {'name': 'Danish Krone', 'only_in_country': False, 'express_checkout': True},
    'EUR': {'name': 'Euro', 'only_in_country': False, 'express_checkout': True},
    'HKD': {'name': 'Hong Kong Dollar', 'only_in_country': False, 'express_checkout': True},
    'HUF': {'name': 'Hungarian Forint', 'only_in_country': False, 'express_checkout': True},
    'ILS': {'name': 'Israeli New Sheqel', 'only_in_country': False, 'express_checkout': False},
    'JPY': {'name': 'Japanese Yen', 'only_in_country': False, 'express_checkout': True},
    'MYR': {'name': 'Malaysian Ringgit', 'only_in_country': True, 'country': 'MY', 'express_checkout': False},
    'MXN': {'name': 'Mexican Peso', 'only_in_country': False, 'express_checkout': False},
    'NOK': {'name': 'Norwegian Krone', 'only_in_country': False, 'express_checkout': True},
    'NZD': {'name': 'New Zealand Dollar', 'only_in_country': False, 'express_checkout': True},
    'PHP': {'name': 'Philippine Peso', 'only_in_country': False, 'express_checkout': False},
    'PLN': {'name': 'Polish Zloty', 'only_in_country': False, 'express_checkout': True},
    'GBP': {'name': 'Pound Sterling', 'only_in_country': False, 'express_checkout': True},
    'SGD': {'name': 'Singapore Dollar', 'only_in_country': False, 'express_checkout': True},
    'SEK': {'name': 'Swedish Krona', 'only_in_country': False, 'express_checkout': True},
    'CHF': {'name': 'Swiss Franc', 'only_in_country': False, 'express_checkout': True},
    'TWD': {'name': 'Taiwan New Dollar', 'only_in_country': False, 'express_checkout': False},
    'THB': {'name': 'Thai Baht', 'only_in_country': False, 'express_checkout': False},
    'TRY': {'name': 'Turkish Lira', 'only_in_country': True, 'country': 'TR', 'express_checkout': False},
    'USD': {'name': 'U.S. Dollar', 'only_in_country': False, 'express_checkout': True},
}

# All currencies (only codes)
ALL_CURRENCIES = CURRENCIES_INFO.keys()

# All currencies generally supported
GENERAL_SUPPORTED = {k: CURRENCIES_INFO[k] for k in CURRENCIES_INFO if not CURRENCIES_INFO[k]['only_in_country']}

# All currencies generally supported (only codes)
GENERAL_SUPORTED_CURRENCIES = GENERAL_SUPPORTED.keys()

# Currencies supported by Express Checkout and Direct Payment
EXPRESS_CHECKOUT = {k: CURRENCIES_INFO[k] for k in CURRENCIES_INFO if CURRENCIES_INFO[k]['express_checkout']}

# Currencies supported by Express Checkout and Direct Payment (only codes)
EXPRESS_CHECKOUT_CURRENCIES = EXPRESS_CHECKOUT.keys()
