
import re

from yargy import (
    rule,
    and_, or_,
)
from yargy.interpretation import (
    fact,
    const
)
from yargy.predicates import (
    eq, length_eq,
    in_, in_caseless,
    gram, type,
    normalized, caseless, dictionary
)

class Currency:
    DOLLAR_GEN = 'DOLLAR_GEN'  # доллар, если страна не определена
    USD = 'DOLLAR_USD'  # доллар США
    AUD = 'DOLLAR_AUD'  # австралийский доллар
    HKD = 'DOLLAR_HKD'  # гонконгский доллар
    CAD = 'DOLLAR_CAD'  # канадский доллар
    SGD = 'DOLLAR_SGD'  # сингапурский доллар

    EURO = 'EUR'

    POUND_GEN = 'POUND_GEN'  # фунт, если страна не определена
    GBP = 'POUND_GBP'  # английский фунт (стерлингов)
    EGP = 'POUND_EGP'  # египетский фунт

    CROWN_GEN = 'CROWN_GEN'  # крона, если страна не определена
    NOK = 'CROWN_NOK'  # норвежская крона
    CZK = 'CROWN_CZK'  # чешская крона
    SEK = 'CROWN_SEK'  # шведская крона
    DKK = 'CROWN_DKK'  # датская крона
    ISK = 'CROWN_ISK'  # исландская крона

    FRANC_GEN = 'FRANC_GEN'  # франк, если страна не определена
    CHF = 'FRANC_CHF'  # швейцарский франк
    FRF = 'FRANC_FRF'  # французский франк (устаревшее)

    LIRA_GEN = 'LIRA_GEN'  # лира, если страна не определена
    TRY = 'LIRA_TRY'  # турецкая лира
    ITL = 'LIRA_ITL'  # итальянская лира (устаревшее)

    HUF = 'HUF'  # венгерский форинт
    PLN = 'PLN'  # польский злотый

    RUBLE_GEN = 'RUBLE_GEN'  # рубль, если страна не определена
    RUB = 'RUBLE_RUB'  # российский рубль
    BYN = 'RUBLE_BYN'  # белорусский рубль

    UAH = 'UAH'  # украинская гривна
    KZT = 'KZT'  # казахский тенге
    GEL = 'GEL'  # грузинский лари
    AMD = 'AMD'  # армянский драм
    KGS = 'KGS'  # киргизский сом
    UZS = 'UZS'  # узбекский сум
    TJS = 'TJS'  # таджикский сомони

    LEI_GEN = 'LEI_GEN'  # лей, если страна не определена
    MDL = 'LEI_MDL'  # молдавский лей
    RON = 'LEI_RON'  # румынский лей

    MANAT_GEN = 'MANAT_GEN'  # манат, если страна не определена
    AZN = 'MANAT_AZN'  # азербайджанский манат
    TMT = 'MANAT_TMT'  # туркменский манат

    CNY = 'CNY'  # китайский юань
    JPY = 'JPY'  # японская иена
    THB = 'THB'  # таиландский бат
    VND = 'VND'  # вьетнамский донг
    MNT = 'MNT'  # монгольский тугрик
    ILS = 'ILS'  # израильский шекель
    ZAR = 'ZAR'  # южноафриканский рэнд

    RUPEE_GEN = 'RUPEE_GEN'  # рупия, если страна не определена
    INR = 'RUPEE_INR'  # индийская рупия
    PKR = 'RUPEE_PKR'  # пакистанская рупия
    IDR = 'RUPEE_IDR'  # индонезийская рупия

    BRL = 'BRL'  # бразильский реал

    PESO_GEN = 'PESO_GEN'  # песо, если страна не определена
    ARS = 'PESO_ARS'  # аргентинское песо
    MXN = 'PESO_MXN'  # мексиканское песо
    CUP = 'PESO_CUP'  # кубинское песо
    COP = 'PESO_COP'  # колумбийское песо
    UYU = 'PESO_UYU'  # уругвайское песо
    DOP = 'PESO_DOP'  # доминиканское песо
    CLP = 'PESO_CLP'  # чилийское песо
    PHP = 'PESO_PHP'  # филиппинское песо

    BTC = 'CRYPTO_BTC'  # биткоин
    LTC = 'CRYPTO_LTC'  # лайткоин
    ETH = 'CRYPTO_ETH'  # эфириум


Money = fact(
    'Money',
    ['integer', 'fraction', 'multiplier', 'currency', 'coins']
)


# noinspection PyRedeclaration
class Money(Money):
    @property
    def amount(self):
        amount = self.integer
        if self.fraction:
            amount += self.fraction / 100
        if self.multiplier:
            amount *= self.multiplier
        if self.coins:
            amount += self.coins / 100
        return amount

    @property
    def obj(self):
        from natasha import obj
        return obj.Money(self.amount, self.currency)


DOT = eq('.')
INT = type('INT')


########
#
#   CURRENCY
#
##########

DOLLAR_GEN = or_(
    normalized('доллар'),
    eq('$')
).interpretation(
    const(Currency.DOLLAR_GEN)
)

DOLLAR_GEN_PREF = eq('$').interpretation(
    const(Currency.DOLLAR_GEN)
)

USD = or_(
    rule(normalized('доллар'), eq('США')),
    rule(normalized('американский'), normalized('доллар')),
    rule(caseless('USD'))
).interpretation(
    const(Currency.USD)
)

USD_PREF = caseless('USD').interpretation(
    const(Currency.USD)
)

AUD = or_(
    rule(normalized('австралийский'), normalized('доллар')),
    rule(eq('AUD'))
).interpretation(
    const(Currency.AUD)
)

HKD = or_(
    rule(normalized('гонконгский'), normalized('доллар')),
    rule(eq('HKD'))
).interpretation(
    const(Currency.HKD)
)

CAD = or_(
    rule(normalized('канадский'), normalized('доллар')),
    rule(eq('CAD'))
).interpretation(
    const(Currency.CAD)
)

SGD = or_(
    rule(normalized('сингапурский'), normalized('доллар')),
    rule(eq('SGD'))
).interpretation(
    const(Currency.SGD)
)

EURO = or_(
    normalized('евро'),
    eq('€'),
    eq('EUR')
).interpretation(
    const(Currency.EURO)
)

EURO_PREF = or_(
    eq('€'),
    eq('EUR')
).interpretation(
    const(Currency.EURO)
)

POUND_GEN = normalized('фунт').interpretation(
    const(Currency.POUND_GEN)
)

GBP = or_(
    rule(
        or_(normalized('британский'), normalized('английский')).optional(),
        normalized('фунт'),
        caseless('стерлингов')
    ),
    rule(
        or_(normalized('британский'), normalized('английский')),
        normalized('фунт'),
    ),
    rule(
        or_(eq('£'), eq('GBP'))
    )
).interpretation(
    const(Currency.GBP)
)

GBP_PREF = or_(
    eq('£'),
    eq('GBP')
).interpretation(
    const(Currency.GBP)
)

EGP = or_(
    rule(normalized('египетский'), normalized('фунт')),
    rule(eq('EGP'))
).interpretation(
    const(Currency.EGP)
)

CROWN_GEN = normalized('крона').interpretation(
    const(Currency.CROWN_GEN)
)

NOK = or_(
    rule(normalized('норвежская'), normalized('крона')),
    rule(eq('NOK'))
).interpretation(
    const(Currency.NOK)
)

CZK = or_(
    rule(normalized('чешская'), normalized('крона')),
    rule(eq('CZK'))
).interpretation(
    const(Currency.CZK)
)

SEK = or_(
    rule(normalized('шведская'), normalized('крона')),
    rule(eq('SEK'))
).interpretation(
    const(Currency.SEK)
)

DKK = or_(
    rule(normalized('датская'), normalized('крона')),
    rule(eq('DKK'))
).interpretation(
    const(Currency.DKK)
)

ISK = or_(
    rule(normalized('исландская'), normalized('крона')),
    rule(eq('ISK'))
).interpretation(
    const(Currency.ISK)
)

FRANC_GEN = normalized('франк').interpretation(
    const(Currency.FRANC_GEN)
)

CHF = or_(
    rule(normalized('швейцарский'), normalized('франк')),
    rule(eq('CHF'))
).interpretation(
    const(Currency.CHF)
)

FRF = rule(
    normalized('французский'), normalized('франк')
).interpretation(
    const(Currency.FRF)
)

LIRA_GEN = normalized('лира').interpretation(
    const(Currency.LIRA_GEN)
)

TRY = or_(
    rule(normalized('турецкая'), normalized('лира')),
    rule(eq('TRY'))
).interpretation(
    const(Currency.TRY)
)

ITL = or_(
    rule(normalized('итальянская'), normalized('лира'))
).interpretation(
    const(Currency.ITL)
)

HUF = or_(
    rule(normalized('венгерский').optional(), normalized('форинт')),
    rule(eq('HUF'))
).interpretation(
    const(Currency.HUF)
)

PLN = or_(
    rule(normalized('польский').optional(), normalized('злотый')),
    rule(eq('PLN'))
).interpretation(
    const(Currency.PLN)
)

RUBLE_GEN = or_(
    rule(normalized('рубль')),
    rule(
        or_(
            caseless('руб'),
            caseless('р'),
        ),
        DOT.optional()
    ),
).interpretation(
    const(Currency.RUBLE_GEN)
)

RUB = or_(
    rule(normalized('российский'), normalized('рубль')),
    rule(
        normalized('российский'),
        or_(caseless('руб'), caseless('р')),
        DOT.optional()
    ),
    rule(or_(eq('₽'), eq('RUB'), eq('RUR')))
).interpretation(
    const(Currency.RUB)
)

BYN = or_(
    rule(normalized('белорусский'), normalized('рубль')),
    rule(
        normalized('белорусский'),
        or_(caseless('руб'), caseless('р')),
        DOT.optional()
    ),
    rule(eq('BYN'))
).interpretation(
    const(Currency.BYN)
)

UAH = or_(
    rule(normalized('украинская').optional(), normalized('гривна')),
    rule(caseless('грн'), DOT.optional()),
    rule(eq('UAH'))
).interpretation(
    const(Currency.UAH)
)

KZT = or_(
    rule(normalized('казахский').optional(), normalized('тенге')),
    rule(eq('KZT'))
).interpretation(
    const(Currency.KZT)
)

GEL = or_(
    rule(normalized('грузинский').optional(), normalized('лари')),
    rule(eq('GEL'))
).interpretation(
    const(Currency.GEL)
)

AMD = or_(
    rule(normalized('армянский').optional(), normalized('драм')),
    # rule(eq('AMD'))
).interpretation(
    const(Currency.AMD)
)

KGS = or_(
    rule(normalized('киргизский').optional(), normalized('сом')),
    rule(eq('KGS'))
).interpretation(
    const(Currency.KGS)
)

UZS = or_(
    rule(normalized('узбекский').optional(), normalized('сум')),
    rule(eq('UZS'))
).interpretation(
    const(Currency.UZS)
)

TJS = or_(
    rule(normalized('таджикский').optional(), normalized('сомони')),
    rule(eq('TJS'))
).interpretation(
    const(Currency.TJS)
)

LEI_FORMS = in_caseless({'лей', 'лея', 'лею', 'леем', 'лее', 'леи', 'леев', 'леям', 'леями', 'леях'})
LEI_GEN = LEI_FORMS.interpretation(
    const(Currency.LEI_GEN)
)

MDL = or_(
    rule(normalized('молдавский'), LEI_FORMS),
    rule(eq('MDL'))
).interpretation(
    const(Currency.MDL)
)

RON = or_(
    rule(normalized('румынский'), LEI_FORMS),
    rule(eq('RON'))
).interpretation(
    const(Currency.RON)
)

MANAT_GEN = normalized('манат').interpretation(
    const(Currency.MANAT_GEN)
)

AZN = or_(
    rule(normalized('азербайджанский'), normalized('манат')),
    rule(eq('AZN'))
).interpretation(
    const(Currency.AZN)
)

TMT = or_(
    rule(normalized('новый').optional(), normalized('туркменский'), normalized('манат')),
    rule(normalized('новый'), normalized('манат')),
    rule(eq('TMT'))
).interpretation(
    const(Currency.TMT)
)

CNY = or_(
    rule(normalized('китайский').optional(), normalized('юань')),
    rule(eq('CNY'))
).interpretation(
    const(Currency.CNY)
)

JPY = or_(
    rule(normalized('японская').optional(), or_(normalized('иена'), normalized('йена'))),
    rule(eq('JPY'))
).interpretation(
    const(Currency.JPY)
)

# noinspection SpellCheckingInspection
THB = or_(
    rule(
        or_(
            normalized('таиландский'), normalized('тайландский'), normalized('тайский')
        ).optional(),
        normalized('бат')),
    rule(eq('THB'))
).interpretation(
    const(Currency.THB)
)

VND = or_(
    rule(normalized('вьетнамский').optional(), normalized('донг')),
    rule(eq('VND'))
).interpretation(
    const(Currency.VND)
)

MNT = or_(
    rule(normalized('монгольский').optional(), normalized('тугрик')),
    rule(eq('MNT'))
).interpretation(
    const(Currency.MNT)
)

ILS = or_(
    rule(normalized('израильский').optional(), normalized('шекель')),
    rule(eq('ILS'))
).interpretation(
    const(Currency.ILS)
)

ZAR = or_(
    rule(normalized('южноафриканский').optional(), normalized('рэнд')),
    rule(eq('ZAR'))
).interpretation(
    const(Currency.ZAR)
)


RUPEE_GEN = normalized('рупия').interpretation(
    const(Currency.RUPEE_GEN)
)

INR = or_(
    rule(normalized('индийская'), normalized('рупия')),
    rule(eq('INR'))
).interpretation(
    const(Currency.INR)
)

PKR = or_(
    rule(normalized('пакистанская'), normalized('рупия')),
    rule(eq('PKR'))
).interpretation(
    const(Currency.PKR)
)

IDR = or_(
    rule(normalized('индонезийская'), normalized('рупия')),
    rule(eq('IDR'))
).interpretation(
    const(Currency.IDR)
)

BRL = or_(
    rule(normalized('бразильский').optional(), normalized('реал')),
    rule(eq('BRL'))
).interpretation(
    const(Currency.BRL)
)

PESO_GEN = caseless('песо').interpretation(
    const(Currency.PESO_GEN)
)

ARS = or_(
    rule(normalized('аргентинское'), caseless('песо')),
    rule(eq('ARS'))
).interpretation(
    const(Currency.ARS)
)

MXN = or_(
    rule(normalized('мексиканское'), caseless('песо')),
    rule(eq('MXN'))
).interpretation(
    const(Currency.MXN)
)

CUP = or_(
    rule(normalized('кубинское'), caseless('песо')),
    # rule(eq('CUP'))
).interpretation(
    const(Currency.CUP)
)

COP = or_(
    rule(normalized('колумбийское'), caseless('песо')),
    # rule(eq('COP'))
).interpretation(
    const(Currency.COP)
)

UYU = or_(
    rule(normalized('уругвайское'), caseless('песо')),
    rule(eq('UYU'))
).interpretation(
    const(Currency.UYU)
)

DOP = or_(
    rule(normalized('доминиканское'), caseless('песо')),
    rule(eq('DOP'))
).interpretation(
    const(Currency.DOP)
)

CLP = or_(
    rule(normalized('чилийское'), caseless('песо')),
    rule(eq('CLP'))
).interpretation(
    const(Currency.CLP)
)

PHP = or_(
    rule(normalized('филиппинское'), caseless('песо')),
    rule(eq('PHP'))
).interpretation(
    const(Currency.PHP)
)

BTC = or_(
    normalized('биткоин'),
    normalized('биткойн'),
    eq('BTC'),
    eq('₿')
).interpretation(
    const(Currency.BTC)
)

LTC = or_(
    normalized('лайткоин'),
    normalized('лайткойн'),
    eq('LTC')
).interpretation(
    const(Currency.LTC)
)

ETH = or_(
    normalized('эфириум'),
    eq('ETH')
).interpretation(
    const(Currency.ETH)
)


CURRENCY = or_(
    DOLLAR_GEN, USD, AUD, HKD, CAD, SGD,
    EURO,
    POUND_GEN, GBP, EGP,
    CROWN_GEN, NOK, CZK, SEK, DKK, ISK,
    FRANC_GEN, CHF, FRF,
    LIRA_GEN, TRY, ITL,
    HUF, PLN,
    RUBLE_GEN, RUB, BYN,
    UAH, KZT, GEL, AMD, KGS, UZS, TJS,
    LEI_GEN, MDL, RON,
    MANAT_GEN, AZN, TMT,
    CNY, JPY, THB, VND, MNT, ILS, ZAR,
    RUPEE_GEN, INR, PKR, IDR,
    BRL,
    PESO_GEN, ARS, MXN, CUP, COP, UYU, DOP, CLP, PHP,
    BTC, LTC, ETH
).interpretation(
    Money.currency
)

CURRENCY_PREF = or_(
    DOLLAR_GEN_PREF, USD_PREF,
    EURO_PREF,
    GBP_PREF
).interpretation(
    Money.currency
)

KOPEIKA = or_(
    rule(normalized('копейка')),
    rule(
        or_(
            caseless('коп'),
            caseless('к')
        ),
        DOT.optional()
    )
)

CENT = or_(
    normalized('цент'),
    eq('¢')
)

EUROCENT = normalized('евроцент')

COINS_CURRENCY = or_(
    KOPEIKA,
    rule(CENT),
    rule(EUROCENT)
)


############
#
#  MULTIPLIER
#
##########


MILLIARD = or_(
    rule(caseless('млрд'), DOT.optional()),
    rule(normalized('миллиард'))
).interpretation(
    const(10**9)
)

MILLION = or_(
    rule(caseless('млн'), DOT.optional()),
    rule(normalized('миллион'))
).interpretation(
    const(10**6)
)

THOUSAND = or_(
    rule(caseless('т'), DOT),
    rule(caseless('тыс'), DOT.optional()),
    rule(normalized('тысяча'))
).interpretation(
    const(10**3)
)

MULTIPLIER = or_(
    MILLIARD,
    MILLION,
    THOUSAND
).interpretation(
    Money.multiplier
)


########
#
#  NUMERAL
#
#######


NUMR = or_(
    gram('NUMR'),
    # https://github.com/OpenCorpora/opencorpora/issues/818
    dictionary({
        'ноль',
        'один'
    }),
)

MODIFIER = in_caseless({
    'целых',
    'сотых',
    'десятых'
})

PART = or_(
    rule(
        or_(
            INT,
            NUMR,
            MODIFIER
        )
    ),
    MILLIARD,
    MILLION,
    THOUSAND,
    CURRENCY,
    COINS_CURRENCY
)

BOUND = in_('()//')

NUMERAL = rule(
    BOUND,
    PART.repeatable(),
    BOUND
)


#######
#
#   AMOUNT
#
########


def normalize_integer(value):
    integer = re.sub(r'[\s.,]+', '', value)
    return int(integer)


def normalize_fraction(value):
    fraction = value.ljust(2, '0')
    return int(fraction)


PART = and_(
    INT,
    length_eq(3)
)

SEP = in_(',.')

INTEGER = or_(
    rule(INT),
    rule(INT, PART),
    rule(INT, PART, PART),
    rule(INT, SEP, PART),
    rule(INT, SEP, PART, SEP, PART),
).interpretation(
    Money.integer.custom(normalize_integer)
)

FRACTION = and_(
    INT,
    or_(
        length_eq(1),
        length_eq(2)
    )
).interpretation(
    Money.fraction.custom(normalize_fraction)
)

AMOUNT = rule(
    INTEGER,
    rule(
        SEP,
        FRACTION
    ).optional(),
    MULTIPLIER.optional(),
    NUMERAL.optional()
)

AMOUNT2 = rule(
    INTEGER,
    rule(
        SEP,
        FRACTION
    ).optional(),
    MULTIPLIER.optional(),
)

COINS_INTEGER = and_(
    INT,
    or_(
        length_eq(1),
        length_eq(2)
    )
).interpretation(
    Money.coins.custom(int)
)

COINS_AMOUNT = rule(
    COINS_INTEGER,
    NUMERAL.optional()
)


#########
#
#   MONEY
#
###########


MONEY = or_(
    rule(AMOUNT, CURRENCY, COINS_AMOUNT.optional(), COINS_CURRENCY.optional()),
    rule(CURRENCY_PREF, AMOUNT2)
).interpretation(
    Money
)
