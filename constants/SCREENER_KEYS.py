MARKET_CAP = 'Market Cap'
PRICE = 'Price (LTP)'
HIGH = '52 Week High'
LOW = '52 Week Low'
PE = 'P/E'
BOOK_VALUE = 'Book Value'
DIV_YIELD = 'Div. Yield'
ROCE = 'ROCE'
ROE = 'ROE'
FACE_VALUE = 'Face Value'
INDUSTRY_PE = 'Industry PE'
EPS = 'EPS'
PB = 'P/B'
INTRINSIC_VALUE = 'Intrinsic Value'
GRAHAM_NUMBER = 'Graham Number'
DEBT = 'Debt'
DEBT_EQUITY = 'Debt / Equity'
TRADE_RECEIVABLES = 'Trade Receivables'
TRADE_PAYABLES = 'Trade Payables'
ADV_CUSTOMERS = 'Advance Customers'
CASH_EQ = 'Cash Equivalents'
CONTINGENT_LIABILITIES = 'Contingent Liabilities'
INVENTORY = 'Inventory'
FCF = 'Free Cash Flow'
ROIC = 'ROIC'
CURRENT_ASSETS = 'Current Assets'
CURRENT_LIABILITIES = 'Current Liabilities'
EPS_PY_QTR = 'EPS PY Qtr'

# Derived
PERCENT_FROM_52_HIGH = 'PERCENT_FROM_52_HIGH'
PERCENT_FROM_52_LOW = 'PERCENT_FROM_52_LOW'

QR_HEADING = 'QR Quarters'
QR_SALES = 'Q Sales'
QR_EXPENSES = 'Q Exp.'
QR_OPERATING_PROFIT = 'Q OpM'
QR_OPM = 'Q OPM'
QR_OTHER_INCOME = 'Q Other Income'
QR_INTEREST = 'Q Interest'
QR_DEPRECIATION = 'Q Depreciation'
QR_PBT = 'Q PBT'
QR_TAX = 'Q Tax'
QR_NET_PROFIT = 'Q Net'
QR_EPS = 'Q EPS'
QR_DIV_YIELD = 'Q Div. Yield'
AR_HEADING = 'Years'
AR_SALES = 'A Sales'
AR_EXPENSES = 'A Exp.'
AR_OPERATING_PROFIT = 'A OpM'
AR_OPM = 'A OPM'
AR_OTHER_INCOME = 'A Other Income'
AR_INTEREST = 'A Interest'
AR_DEPRECIATION = 'A Depreciation'
AR_PBT = 'A PBT'
AR_TAX = 'A Tax'
AR_NET_PROFIT = 'A Net'
AR_EPS = 'A EPS'
AR_DIV_YIELD = 'A Div. Yield'
BS_HEADING = 'Years'
BS_SHARE_CAPITAL = 'Share Capital'
BS_RESERVES = 'Reserves'
BS_BORROWING = 'Borrowings'
BS_OTHER_LIABILITIES = 'Other Liabilities'
BS_TOTAL_LIABILITIES = 'Total Liabilities'
BS_FIXED_ASSETS = 'Fixed Assets'
BS_CWIP = 'Capital Work in Progress'
BS_INVESTMENTS = 'Investments'
BS_OTHER_ASSETS = 'Other Assets'
BS_TOTAL_ASSETS = 'Total Assets'
CF_HEADING = 'Years'
CF_OA = 'CF OA'
CF_IA = 'Cash from Investment Activity'
CF_FA = 'Cash from Financing Activity'
CF_NCF = 'Net Cash Flow'
RATIOS_HEADING = 'Years'
RATIOS_DEBTOR_DAYS = 'Debtor Days'
RATIOS_INVENTORY_DAYS = 'Inventory Days'
RATIOS_DAYS_PAYABLE = 'Days Payable'
RATIOS_CASH_CONVERSION_CYCLE = 'Cash Conversion Cycle'
RATIOS_WORKING_CAPITAL_DAYS = 'Working Capital Days'
RATIOS_ROCE = 'ROCE %'
SP_HEADING = 'SH Quarters'
SP_PROMOTERS = 'Promoters'
SP_FII = 'FIIs'
SP_DII = 'DIIs'
SP_PUBLIC = 'Public'
SP_GOVT = 'Government'

ARRAY_HEADINGS = [
    QR_HEADING,
    AR_HEADING,
    BS_HEADING,
    CF_HEADING,
    RATIOS_HEADING,
    SP_HEADING
]

ARRAY_QR = [
    QR_SALES,
    QR_EXPENSES,
    QR_OPERATING_PROFIT,
    QR_OPM,
    QR_OTHER_INCOME,
    QR_INTEREST,
    QR_DEPRECIATION,
    QR_PBT,
    QR_TAX,
    QR_NET_PROFIT,
    QR_EPS,
    QR_DIV_YIELD,
    'New Line'
]

ARRAY_AR = [
    AR_SALES,
    AR_EXPENSES,
    AR_OPERATING_PROFIT,
    AR_OPM,
    AR_OTHER_INCOME,
    AR_INTEREST,
    AR_DEPRECIATION,
    AR_PBT,
    AR_TAX,
    AR_NET_PROFIT,
    AR_EPS,
    AR_DIV_YIELD
]

ARRAY_BS = [
    BS_SHARE_CAPITAL,
    BS_RESERVES,
    BS_BORROWING,
    BS_OTHER_LIABILITIES,
    BS_TOTAL_LIABILITIES,
    BS_FIXED_ASSETS,
    BS_CWIP,
    BS_INVESTMENTS,
    BS_OTHER_ASSETS,
    BS_TOTAL_ASSETS
]

ARRAY_CF = [
    CF_OA,
    CF_IA,
    CF_FA,
    CF_NCF
]

ARRAY_RATIOS = [
    RATIOS_DEBTOR_DAYS,
    RATIOS_INVENTORY_DAYS,
    RATIOS_DAYS_PAYABLE,
    RATIOS_CASH_CONVERSION_CYCLE,
    RATIOS_WORKING_CAPITAL_DAYS,
    RATIOS_ROCE
]

ARRAY_SP = [
    SP_PROMOTERS,
    SP_FII,
    SP_DII,
    SP_PUBLIC
]

ARRAY_ALL = [ARRAY_QR, ARRAY_AR, ARRAY_BS, ARRAY_CF, ARRAY_RATIOS, ARRAY_SP]