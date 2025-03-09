import json

import requests

url = 'https://scanner.tradingview.com/america/scan?label-product=markets-screener'

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://in.tradingview.com',
    'priority': 'u=1, i',
    'referer': 'https://in.tradingview.com/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

cookies = {
    'cookiePrivacyPreferenceBannerProduction': 'notApplicable',
    '_ga': 'GA1.1.1066075710.1740306357',
    'cookiesSettings': '{"analytics":true,"advertising":true}',
    'device_t': 'TmFyTUFROjI.qUcPniFMCUxNT5pNDk9lG5QqiwDBhrciiMdRULXQnNs',
    'sessionid': 'bjapvq6d86lhht55j830no3vhanq7vzh',
    'sessionid_sign': 'v3:IjJGrWr8f61TTCxcFoGe8H5VTBcazRhBkp3hPGq9rms=',
    'tv_ecuid': '4eff1873-d4f0-4d9a-bf42-e6de21518970',
    '_sp_ses.cf1a': '*',
    '_sp_id.cf1a': '85482f98-c904-43a6-992c-ffddf2aeadb3.1740306357.5.1740905231.1740368770.296982a7-672a-4fe9-830b-bda891ec5dd5.4d08b524-435c-4a44-a8ad-e5b7183b813b.44ef484f-c203-4a13-be25-df4c8e6c9cb7.1740904090890.5',
    '_ga_YVVRYGL0E0': 'GS1.1.1740904091.5.1.1740905230.1.0.0'
}

data_overview = {
    "columns": [
        "name", "description", "logoid", "update_mode", "type", "typespecs", "close",
        "pricescale", "minmov", "fractional", "minmove2", "currency", "change",
        "volume", "relative_volume_10d_calc", "market_cap_basic", "fundamental_currency_code",
        "price_earnings_ttm", "earnings_per_share_diluted_ttm", "earnings_per_share_diluted_yoy_growth_ttm",
        "dividends_yield_current", "sector.tr", "market", "sector", "recommendation_mark"
    ],
    "ignore_unknown_fields": False,
    "options": {
        "lang": "en"
    },
    "range": [0, 5000],
    "sort": {
        "sortBy": "name",
        "sortOrder": "asc",
        "nullsFirst": False
    },
    "preset": "all_stocks"
}

data_performance = {
  "columns": [
    "name",
    "description",
    "logoid",
    "update_mode",
    "type",
    "typespecs",
    "close",
    "pricescale",
    "minmov",
    "fractional",
    "minmove2",
    "currency",
    "change",
    "Perf.W",
    "Perf.1M",
    "Perf.3M",
    "Perf.6M",
    "Perf.YTD",
    "Perf.Y",
    "Perf.5Y",
    "Perf.10Y",
    "Perf.All",
    "Volatility.W",
    "Volatility.M"
  ],
  "ignore_unknown_fields": False,
  "options": {
    "lang": "en"
  },
  "range": [0, 5000],
  "sort": {
    "sortBy": "name",
    "sortOrder": "asc",
    "nullsFirst": False
  },
  "preset": "all_stocks"
}

data_valuation = {
  "columns": [
    "name",
    "description",
    "logoid",
    "update_mode",
    "type",
    "typespecs",
    "market_cap_basic",
    "fundamental_currency_code",
    "Perf.1Y.MarketCap",
    "price_earnings_ttm",
    "price_earnings_growth_ttm",
    "price_sales_current",
    "price_book_fq",
    "price_to_cash_f_operating_activities_ttm",
    "price_free_cash_flow_ttm",
    "price_to_cash_ratio",
    "enterprise_value_current",
    "enterprise_value_to_revenue_ttm",
    "enterprise_value_to_ebit_ttm",
    "enterprise_value_ebitda_ttm"
  ],
  "ignore_unknown_fields": False,
  "options": {
    "lang": "en"
  },
  "range": [0, 5000],
  "sort": {
    "sortBy": "name",
    "sortOrder": "asc",
    "nullsFirst": False
  },
  "preset": "all_stocks"
}

data_dividends = {
  "columns": [
    "name",
    "description",
    "logoid",
    "update_mode",
    "type",
    "typespecs",
    "dps_common_stock_prim_issue_fy",
    "fundamental_currency_code",
    "dps_common_stock_prim_issue_fq",
    "dividends_yield_current",
    "dividends_yield",
    "dividend_payout_ratio_ttm",
    "dps_common_stock_prim_issue_yoy_growth_fy",
    "continuous_dividend_payout",
    "continuous_dividend_growth"
  ],
  "ignore_unknown_fields": False,
  "options": {
    "lang": "en"
  },
  "range": [0, 5000],
  "sort": {
    "sortBy": "name",
    "sortOrder": "asc",
    "nullsFirst": False
  },
  "preset": "all_stocks"
}

data_profitibality = {
  "columns": [
    "name",
    "description",
    "logoid",
    "update_mode",
    "type",
    "typespecs",
    "gross_margin_ttm",
    "operating_margin_ttm",
    "pre_tax_margin_ttm",
    "net_margin_ttm",
    "free_cash_flow_margin_ttm",
    "return_on_assets_fq",
    "return_on_equity_fq",
    "return_on_invested_capital_fq",
    "research_and_dev_ratio_ttm",
    "sell_gen_admin_exp_other_ratio_ttm"
  ],
  "ignore_unknown_fields": False,
  "options": {
    "lang": "en"
  },
  "range": [0, 5000],
  "sort": {
    "sortBy": "name",
    "sortOrder": "asc",
    "nullsFirst": False
  },
  "preset": "all_stocks"
}

data_income_statement = {
  "columns": [
    "name",
    "description",
    "logoid",
    "update_mode",
    "type",
    "typespecs",
    "total_revenue_ttm",
    "fundamental_currency_code",
    "total_revenue_yoy_growth_ttm",
    "gross_profit_ttm",
    "oper_income_ttm",
    "net_income_ttm",
    "ebitda_ttm",
    "earnings_per_share_diluted_ttm",
    "earnings_per_share_diluted_yoy_growth_ttm"
  ],
  "ignore_unknown_fields": False,
  "options": {
    "lang": "en"
  },
  "range": [0, 5000],
  "sort": {
    "sortBy": "name",
    "sortOrder": "asc",
    "nullsFirst": False
  },
  "preset": "all_stocks"
}

data_balance_sheet = {
  "columns": [
    "name", "description", "logoid", "update_mode", "type", "typespecs",
    "total_assets_fq", "fundamental_currency_code", "total_current_assets_fq",
    "cash_n_short_term_invest_fq", "total_liabilities_fq", "total_debt_fq",
    "net_debt_fq", "total_equity_fq", "current_ratio_fq", "quick_ratio_fq",
    "debt_to_equity_fq", "cash_n_short_term_invest_to_total_debt_fq"
  ],
  "ignore_unknown_fields": False,
  "options": {
    "lang": "en"
  },
  "range": [0, 5000],
  "sort": {
    "sortBy": "name",
    "sortOrder": "asc",
    "nullsFirst": False
  },
  "preset": "all_stocks"
}

data_cash_flow = {
  "columns": [
    "name",
    "description",
    "logoid",
    "update_mode",
    "type",
    "typespecs",
    "cash_f_operating_activities_ttm",
    "fundamental_currency_code",
    "cash_f_investing_activities_ttm",
    "cash_f_financing_activities_ttm",
    "free_cash_flow_ttm",
    "capital_expenditures_ttm"
  ],
  "ignore_unknown_fields": False,
  "options": {
    "lang": "en"
  },
  "range": [0, 5000],
  "sort": {
    "sortBy": "name",
    "sortOrder": "asc",
    "nullsFirst": False
  },
  "preset": "all_stocks"
}

data_technicals = {
  "columns": [
    "name", "description", "logoid", "update_mode", "type", "typespecs",
    "Recommend.All", "Recommend.MA", "Recommend.Other", "RSI", "Mom",
    "pricescale", "minmov", "fractional", "minmove2", "AO", "CCI20",
    "Stoch.K", "Stoch.D", "MACD.macd", "MACD.signal"
  ],
  "ignore_unknown_fields": False,
  "options": {
    "lang": "en"
  },
  "range": [0, 5000],
  "sort": {
    "sortBy": "name",
    "sortOrder": "asc",
    "nullsFirst": False
  },
  "preset": "all_stocks"
}

list_payloads = [{'name': 'overview', 'data': data_overview}, {'name': 'performance', 'data': data_performance}, {'name': 'valuation', 'data': data_valuation}, {'name': 'dividends', 'data': data_dividends}, {'name': 'profitability', 'data': data_profitibality}, {'name': 'income_statement', 'data': data_income_statement}, {'name': 'balance_sheet', 'data': data_balance_sheet}, {'name': 'cash_flow', 'data': data_cash_flow}]

tabs_data = []
for lp in list_payloads:
  tabs_data.append({'name': lp['name'], 'columns': lp['data']['columns']})
print(tabs_data)
with open('csv_files/tabs_data.json', 'w') as f:
  f.write(json.dumps(tabs_data))
exit()

for lp in list_payloads:
    print(lp)
    response = requests.post(url, headers=headers, cookies=cookies, json=lp['data'])

    with open(f'data/{lp['name']}.json', 'w') as f:
        f.write(json.dumps(response.json()))