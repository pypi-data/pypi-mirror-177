import pandas as pd
import tushare as ts


# 全部的申万分类
def classify(class_type: str, key: str):
    pro = ts.pro_api(key)

    l3 = pro.index_classify(**{
        "level": "L3",
        "src": class_type
    }, fields=[
        "index_code",
        "industry_name",
        "industry_code",
        "parent_code"
    ])
    data_l3 = pd.DataFrame(l3)
    data_l3.rename(columns={"index_code": "index_code_l3",
                            "industry_name": "industry_name_l3",
                            "industry_code": "industry_code_l3",
                            "parent_code": "parent_code_l3"}, inplace=True)

    l2 = pro.index_classify(**{
        "level": "L2",
        "src": class_type
    }, fields=[
        "index_code",
        "industry_name",
        "industry_code",
        "parent_code"
    ])
    data_l2 = pd.DataFrame(l2)
    data_l2.rename(columns={"index_code": "index_code_l2",
                            "industry_name": "industry_name_l2",
                            "industry_code": "industry_code_l2",
                            "parent_code": "parent_code_l2"}, inplace=True)

    l1 = pro.index_classify(**{
        "level": "L1",
        "src": class_type
    }, fields=[
        "index_code",
        "industry_name",
        "industry_code",
        "parent_code"
    ])
    data_l1 = pd.DataFrame(l1)
    data_l1.rename(columns={"index_code": "index_code_l1",
                            "industry_name": "industry_name_l1",
                            "industry_code": "industry_code_l1",
                            "parent_code": "parent_code_l1"}, inplace=True)

    return_l2 = pd.merge(data_l3, data_l2, left_on=['parent_code_l3'], right_on=['industry_code_l2'], how="left")
    return_l1 = pd.merge(return_l2, data_l1, left_on=['parent_code_l2'], right_on=['industry_code_l1'], how="left")
    return_l1.rename(columns={}, inplace=True)

    return return_l1[{'index_code_l3',
                      'industry_name_l3',
                      'industry_code_l3',
                      'index_code_l2',
                      'industry_name_l2',
                      'industry_code_l2',
                      'index_code_l1',
                      'industry_name_l1',
                      'industry_code_l1',
                      }]


# 根据申万分类找到相关股票
def classify_symbol(class_type: str, sw_str: str, key: str):
    sw = classify(class_type, key)
    lv_type = ""
    if sw_str[4:6] != '00':
        lv_type = '3'
    elif sw_str[2:4] != '00':
        lv_type = '2'
    else:
        lv_type = '1'

    sw_data = sw[sw['industry_code_l' + lv_type] == sw_str]
    return_data = pd.DataFrame()
    for index_code, industry_code in zip(sw_data['index_code_l3'], sw_data['industry_code_l3']):
        data = index_member(index_code, industry_code, key)
        return_data = pd.concat([return_data, data])
    return return_data


# 根据指数找到股票
def index_member(index_code: str, industry_code: str, key: str):
    pro = ts.pro_api(key)
    # 拉取数据
    data = pro.index_member(**{
        "index_code": index_code
    }, fields=[
        "index_code",
        "con_code",
        "in_date",
        "out_date"
    ])
    data['industry_code'] = industry_code
    data['out_date'] = data['out_date'].apply(lambda x: '20991231' if x is None else x)
    return data


def index_daily(ts_code: str, start_date: str, end_date: str, industry: str, key: str, value: list):
    pro = ts.pro_api(key)
    field = [
                "ts_code",
                "trade_date"] + value
    daily_data = pro.daily(**{
        "ts_code": ts_code,
        "start_date": start_date,
        "end_date": end_date,
    }, fields=field)
    daily_data['industry'] = industry
    return daily_data


def index_income(ts_code: str, end_type: str, key: str):
    pro = ts.pro_api(key)
    income_data = pro.income(**{
        "ts_code": ts_code,
        "end_type": end_type,
    }, fields=[
        "ts_code",
        "ann_date",
        "f_ann_date",
        "end_date",
        "report_type",
        "comp_type",
        "end_type",
        "basic_eps",
        "diluted_eps",
        "total_revenue",
        "revenue",
        "int_income",
        "prem_earned",
        "comm_income",
        "n_commis_income",
        "n_oth_income",
        "n_oth_b_income",
        "prem_income",
        "out_prem",
        "une_prem_reser",
        "reins_income",
        "n_sec_tb_income",
        "n_sec_uw_income",
        "n_asset_mg_income",
        "oth_b_income",
        "fv_value_chg_gain",
        "invest_income",
        "ass_invest_income",
        "forex_gain",
        "total_cogs",
        "oper_cost",
        "int_exp",
        "comm_exp",
        "biz_tax_surchg",
        "sell_exp",
        "admin_exp",
        "fin_exp",
        "assets_impair_loss",
        "prem_refund",
        "compens_payout",
        "reser_insur_liab",
        "div_payt",
        "reins_exp",
        "oper_exp",
        "compens_payout_refu",
        "insur_reser_refu",
        "reins_cost_refund",
        "other_bus_cost",
        "operate_profit",
        "non_oper_income",
        "non_oper_exp",
        "nca_disploss",
        "total_profit",
        "income_tax",
        "n_income",
        "n_income_attr_p",
        "minority_gain",
        "oth_compr_income",
        "t_compr_income",
        "compr_inc_attr_p",
        "compr_inc_attr_m_s",
        "ebit",
        "ebitda",
        "insurance_exp",
        "undist_profit",
        "distable_profit",
        "rd_exp",
        "fin_exp_int_exp",
        "fin_exp_int_inc",
        "transfer_surplus_rese",
        "transfer_housing_imprest",
        "transfer_oth",
        "adj_lossgain",
        "withdra_legal_surplus",
        "withdra_legal_pubfund",
        "withdra_biz_devfund",
        "withdra_rese_fund",
        "withdra_oth_ersu",
        "workers_welfare",
        "distr_profit_shrhder",
        "prfshare_payable_dvd",
        "comshare_payable_dvd",
        "capit_comstock_div",
        "continued_net_profit",
        "update_flag",
        "net_after_nr_lp_correct",
        "oth_income",
        "asset_disp_income",
        "end_net_profit",
        "credit_impa_loss",
        "net_expo_hedging_benefits",
        "oth_impair_loss_assets",
        "total_opcost",
        "amodcost_fin_assets"
    ])

    income_g = pd.DataFrame(income_data.groupby(['end_date', 'end_type'])['update_flag'].count())
    income_g = income_g.reset_index(drop=False)
    income_g.rename(columns={'update_flag': 'count'}, inplace=True)
    zzz = pd.merge(income_data, income_g, on=["end_date", "end_type"], how="left")

    return_data = pd.concat([pd.DataFrame(), zzz[zzz['count'] == 1]])
    return_data = pd.concat([return_data, zzz[((zzz['count'] > 1) & (zzz['update_flag'] == '1'))]])
    return_data['year'] = return_data['end_date'].apply(lambda x: x[0:4])
    return_data.drop_duplicates(['ts_code', 'year'], inplace=True)
    return return_data


def index_income_year(ts_code: set, key: str):
    return_data = pd.DataFrame()
    for code in ts_code:
        income_data = index_income(code, "4", key)
        return_data = pd.concat([return_data, income_data])
    return return_data


def symbol_base(ts_code: str, key: str):
    pro = ts.pro_api(key)
    data = pro.bak_basic(**{
        "ts_code": ts_code
    }, fields=[
        "trade_date",
        "ts_code",
        "name",
        "industry",
        "area",
        "pe",
        "float_share",
        "total_share",
        "total_assets",
        "liquid_assets",
        "fixed_assets",
        "reserved",
        "reserved_pershare",
        "eps",
        "bvps",
        "pb",
        "list_date",
        "undp",
        "per_undp",
        "rev_yoy",
        "profit_yoy",
        "gpr",
        "npr",
        "holder_num"
    ])
    return data


def symbol_base_for_date(ts_code: str, start_date: str, end_date: str, key):
    data = symbol_base(ts_code, key)
    start_data = data[data['trade_date'] <= end_date]
    end_data = data[data['trade_date'] >= start_date]
    return_data = pd.merge(start_data['trade_date'], end_data['trade_date'], on=['trade_date'])
    return pd.merge(data, return_data, on=['trade_date'])
