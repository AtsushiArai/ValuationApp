from valuation._init_ import db
from datetime import datetime

from flask_login import UserMixin

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    company_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100))

class FinancialData(UserMixin, db.Model):
    __tablename__ = 'financial_data'
    # id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(300), primary_key=True)
    year_before_last = db.Column(db.String(10))
    last_year = db.Column(db.String(10))
    this_year = db.Column(db.String(10))
    
    ############### year_before_last : t - 2 ####################
    ybl_net_sales = db.Column(db.Integer, default=0)
    ybl_cogs = db.Column(db.Integer, default=0)
    # ybl_gross_profit = db.Column(db.Integer, default=0)
    ybl_sga = db.Column(db.Integer, default=0)
    ybl_operating_income = db.Column(db.Integer, default=0)
    
    ybl_interest_and_dividends_income = db.Column(db.Integer, default=0)
    ybl_equity_in_earnings_or_losses_of_affiliates = db.Column(db.Integer, default=0)
    # ybl_other_non_operating_income = db.Column(db.Integer, default=0)
    # ybl_non_operating_income = db.Column(db.Integer, default=0)

    ybl_interest_expenses = db.Column(db.Integer, default=0)
    # ybl_equity_in_losses_of_affiliates = db.Column(db.Integer, default=0)
    # ybl_other_non_operating_expenses = db.Column(db.Integer, default=0)
    # ybl_non_operating_expenses = db.Column(db.Integer, default=0)
    ybl_ordinary_income_loss = db.Column(db.Integer, default=0)
    ybl_other_nonoperating_income_or_loss = db.Column(db.Integer, default=0)

    ybl_extraordinary_income_and_loss = db.Column(db.Integer, default=0)
    ybl_income_before_income_taxes = db.Column(db.Integer, default=0)
    ybl_income_taxes = db.Column(db.Integer, default=0)
    ybl_profit_loss_attributable_to_non_controling_interests = db.Column(db.Integer, default=0)
    ybl_profit_loss_attributable_to_owners_of_parent = db.Column(db.Integer, default=0)

    ybl_depreciation = db.Column(db.Integer, default=0)
    ybl_amortization_goodwill = db.Column(db.Integer, default=0)
    ybl_impairment = db.Column(db.Integer, default=0)

    ################  BS  ######################
    ybl_cash_and_deposits = db.Column(db.Integer, default=0)
    ybl_securities = db.Column(db.Integer, default=0)
    ybl_notes_and_accounts_receivable_trade = db.Column(db.Integer, default=0)
    ybl_inventories = db.Column(db.Integer, default=0)
    ybl_deferred_tax_assets_ca = db.Column(db.Integer, default=0)
    ybl_other_current_assets = db.Column(db.Integer, default=0)
    ybl_current_assets = db.Column(db.Integer, default=0)

    ybl_property_plant_and_equipment = db.Column(db.Integer, default=0)
    
    ybl_intangible_assets = db.Column(db.Integer, default=0)

    ybl_deferred_tax_assets_ioa = db.Column(db.Integer, default=0)
    ybl_investments_and_other_assets = db.Column(db.Integer, default=0)
    
    ybl_total_assets = db.Column(db.Integer, default=0)

    ybl_short_term_interest_bearing_bond = db.Column(db.Integer, default=0)
    ybl_notes_and_accounts_payable_trade = db.Column(db.Integer, default=0)
    ybl_deferred_tax_liabilities_ca = db.Column(db.Integer, default=0)
    ybl_other_current_liabilities = db.Column(db.Integer, default=0)
    ybl_current_liabilities = db.Column(db.Integer, default=0)

    ybl_long_term_interest_bearing_bond = db.Column(db.Integer, default=0)
    ybl_deferred_tax_liabilities_ncl = db.Column(db.Integer, default=0)
    ybl_other_noncurrent_liabilities = db.Column(db.Integer, default=0)
    ybl_noncurrent_liabilities = db.Column(db.Integer, default=0)

    ybl_capital_stock = db.Column(db.Integer, default=0)
    ybl_capital_surplus = db.Column(db.Integer, default=0)
    ybl_retained_earnings = db.Column(db.Integer, default=0)
    ybl_treasury_stock = db.Column(db.Integer, default=0)
    ybl_accumulated_other_comprehensive_income = db.Column(db.Integer, default=0)
    ybl_subscription_rights_to_shares = db.Column(db.Integer, default=0)
    ybl_non_controlling_interests = db.Column(db.Integer, default=0)
    ybl_net_assets = db.Column(db.Integer, default=0)

    ybl_liabilities_and_net_assets = db.Column(db.Integer, default=0)
    ybl_net_deferred_tax_assets = db.Column(db.Integer, default=0)

    ################  SS  ######################
    ybl_net_assets_py = db.Column(db.Integer, default=0)
    ybl_issuance_of_new_shares = db.Column(db.Integer, default=0)
    ybl_dividends_ss = db.Column(db.Integer, default=0)
    ybl_purchase_of_treasury_stock = db.Column(db.Integer, default=0)
    ybl_disposal_of_treasury_stock = db.Column(db.Integer, default=0)

    ################  CF  ######################
    # ybl_cf_operating_activities = db.Column(db.Integer, default=0)
    # ybl_cf_investment_activities = db.Column(db.Integer, default=0)
    # ybl_cf_financing_activities = db.Column(db.Integer, default=0)

    ################ OHTER ####################
    ybl_total_number_of_issued_shares = db.Column(db.Integer, default=0)
    ybl_number_of_shares_held_in_own_name = db.Column(db.Integer, default=0)
    ybl_dividend_paid_per_share = db.Column(db.Integer, default=0)
    ybl_effective_tax_rate = db.Column(db.Float, default=0.0)

    ############### INVESTED_CAPITAL #####################
    ybl_invested_capital = db.Column(db.Float, default=0.0)

    ############### last_year : t - 1 ###########################
    ly_net_sales = db.Column(db.Integer, default=0)
    ly_cogs = db.Column(db.Integer, default=0)
    # ly_gross_profit = db.Column(db.Integer, default=0)
    ly_sga = db.Column(db.Integer, default=0)
    ly_operating_income = db.Column(db.Integer, default=0)
    
    ly_interest_and_dividends_income = db.Column(db.Integer, default=0)
    ly_equity_in_earnings_or_losses_of_affiliates = db.Column(db.Integer, default=0)
    # ly_other_non_operating_income = db.Column(db.Integer, default=0)
    # ly_non_operating_income = db.Column(db.Integer, default=0)

    ly_interest_expenses = db.Column(db.Integer, default=0)
    # ly_equity_in_losses_of_affiliates = db.Column(db.Integer, default=0)
    # ly_other_non_operating_expenses = db.Column(db.Integer, default=0)
    # ly_non_operating_expenses = db.Column(db.Integer, default=0)
    ly_ordinary_income_loss = db.Column(db.Integer, default=0)
    ly_other_nonoperating_income_or_loss = db.Column(db.Integer, default=0)

    ly_extraordinary_income_and_loss = db.Column(db.Integer, default=0)
    ly_income_before_income_taxes = db.Column(db.Integer, default=0)
    ly_income_taxes = db.Column(db.Integer, default=0)
    ly_profit_loss_attributable_to_non_controling_interests = db.Column(db.Integer, default=0)
    ly_profit_loss_attributable_to_owners_of_parent = db.Column(db.Integer, default=0)

    ly_depreciation = db.Column(db.Integer, default=0)
    ly_amortization_goodwill = db.Column(db.Integer, default=0)
    ly_impairment = db.Column(db.Integer, default=0)

    ################  BS  ######################
    ly_cash_and_deposits = db.Column(db.Integer, default=0)
    ly_securities = db.Column(db.Integer, default=0)
    ly_notes_and_accounts_receivable_trade = db.Column(db.Integer, default=0)
    ly_inventories = db.Column(db.Integer, default=0)
    ly_deferred_tax_assets_ca = db.Column(db.Integer, default=0)
    ly_other_current_assets = db.Column(db.Integer, default=0)
    ly_current_assets = db.Column(db.Integer, default=0)

    ly_property_plant_and_equipment = db.Column(db.Integer, default=0)
    
    ly_intangible_assets = db.Column(db.Integer, default=0)

    ly_deferred_tax_assets_ioa = db.Column(db.Integer, default=0)
    ly_investments_and_other_assets = db.Column(db.Integer, default=0)
    
    ly_total_assets = db.Column(db.Integer, default=0)

    ly_short_term_interest_bearing_bond = db.Column(db.Integer, default=0)
    ly_notes_and_accounts_payable_trade = db.Column(db.Integer, default=0)
    ly_deferred_tax_liabilities_ca = db.Column(db.Integer, default=0)
    ly_other_current_liabilities = db.Column(db.Integer, default=0)
    ly_current_liabilities = db.Column(db.Integer, default=0)

    ly_long_term_interest_bearing_bond = db.Column(db.Integer, default=0)
    ly_deferred_tax_liabilities_ncl = db.Column(db.Integer, default=0)
    ly_other_noncurrent_liabilities = db.Column(db.Integer, default=0)
    ly_noncurrent_liabilities = db.Column(db.Integer, default=0)

    ly_capital_stock = db.Column(db.Integer, default=0)
    ly_capital_surplus = db.Column(db.Integer, default=0)
    ly_retained_earnings = db.Column(db.Integer, default=0)
    ly_treasury_stock = db.Column(db.Integer, default=0)
    ly_accumulated_other_comprehensive_income = db.Column(db.Integer, default=0)
    ly_subscription_rights_to_shares = db.Column(db.Integer, default=0)
    ly_non_controlling_interests = db.Column(db.Integer, default=0)
    ly_net_assets = db.Column(db.Integer, default=0)

    ly_liabilities_and_net_assets = db.Column(db.Integer, default=0)
    ly_net_deferred_tax_assets = db.Column(db.Integer, default=0)
    ly_fluctuations_in_deferred_tax_assets = db.Column(db.Integer, default=0)

    ################  SS  ######################
    ly_net_assets_py = db.Column(db.Integer, default=0)
    ly_issuance_of_new_shares = db.Column(db.Integer, default=0)
    ly_dividends_ss = db.Column(db.Integer, default=0)
    ly_purchase_of_treasury_stock = db.Column(db.Integer, default=0)
    ly_disposal_of_treasury_stock = db.Column(db.Integer, default=0)

    ################  CF  ######################
    # ly_cf_operating_activities = db.Column(db.Integer, default=0)
    # ly_cf_investment_activities = db.Column(db.Integer, default=0)
    # ly_cf_financing_activities = db.Column(db.Integer, default=0)

    ################ OHTER ####################
    ly_total_number_of_issued_shares = db.Column(db.Integer, default=0)
    ly_number_of_shares_held_in_own_name = db.Column(db.Integer, default=0)
    ly_dividend_paid_per_share = db.Column(db.Integer, default=0)
    ly_effective_tax_rate = db.Column(db.Float, default=0.0)

    ################ TAX_ON_OPERATING_INCOME ####################
    ly_tax_on_interest_income_and_dividend = db.Column(db.Integer, default=0)
    ly_tax_on_interest_expenses = db.Column(db.Integer, default=0)
    ly_tax_on_non_operating_income_and_expenses_others = db.Column(db.Integer, default=0)
    ly_tax_on_extraordinary_income_and_losses = db.Column(db.Integer, default=0)
    ly_tax_on_operating_income = db.Column(db.Integer, default=0)

    ############### NOPAT_TOPDOWN #####################
    ly_nopat_topdown = db.Column(db.Integer, default=0)

    ############### NOPAT_BOTTOMUP #####################
    ly_nopat_bottomup = db.Column(db.Integer, default=0)

    ############### INVESTMENT_CAPITAL #####################
    ly_net_working_capital = db.Column(db.Integer, default=0)
    ly_investment_capital = db.Column(db.Integer, default=0)

    ############### FREE_CASH_FLOW #####################
    ly_operating_cf = db.Column(db.Integer, default=0)
    ly_investment_cf = db.Column(db.Integer, default=0)
    ly_free_cash_flow = db.Column(db.Integer, default=0)
    ly_non_operating_cf = db.Column(db.Integer, default=0)
    ly_financial_cf = db.Column(db.Integer, default=0)
    ly_net_cf = db.Column(db.Integer, default=0)

    ############### ROE #####################
    ly_return_on_equity = db.Column(db.Float, default=0)
    ly_return_on_asset = db.Column(db.Float, default=0)
    ly_total_asset_turnover = db.Column(db.Float, default=0)
    ly_financial_leverage = db.Column(db.Float, default=0)

    ############### WACC #####################


    ############### ROIC #####################
    ly_return_on_invested_capital = db.Column(db.Float, default=0)
    ly_return_on_invested_capital_before_tax = db.Column(db.Float, default=0)
    ly_tax_burden_rate = db.Column(db.Float, default=0)
    ly_affiliated_company_contribution_rate = db.Column(db.Float, default=0)
    ly_operating_profit_margin = db.Column(db.Float, default=0)
    ly_cost_rate = db.Column(db.Float, default=0)
    ly_sga_ratio = db.Column(db.Float, default=0)
    ly_invested_capital_turnover = db.Column(db.Float, default=0)
    ly_net_working_capital_turnover_days = db.Column(db.Float, default=0)
    ly_trade_receivavle_turnover_days = db.Column(db.Float, default=0)
    ly_trade_payable_turnover_days = db.Column(db.Float, default=0)
    ly_inventries_turnover_days = db.Column(db.Float, default=0)
    ly_property_turnover_days = db.Column(db.Float, default=0)
    ly_intangible_turnover_days = db.Column(db.Float, default=0)
    ly_other_invested_capital_turnover_days = db.Column(db.Float, default=0)
    ly_cash_conversion_cicle = db.Column(db.Float, default=0)


    ############### this_year : t ###############################
    net_sales = db.Column(db.Integer, default=0)
    cogs = db.Column(db.Integer, default=0)
    # gross_profit = db.Column(db.Integer, default=0)
    sga = db.Column(db.Integer, default=0)
    operating_income = db.Column(db.Integer, default=0)
    
    interest_and_dividends_income = db.Column(db.Integer, default=0)
    equity_in_earnings_or_losses_of_affiliates = db.Column(db.Integer, default=0)
    # other_non_operating_income = db.Column(db.Integer, default=0)
    # non_operating_income = db.Column(db.Integer, default=0)

    interest_expenses = db.Column(db.Integer, default=0)
    # equity_in_losses_of_affiliates = db.Column(db.Integer, default=0)
    # other_non_operating_expenses = db.Column(db.Integer, default=0)
    # non_operating_expenses = db.Column(db.Integer, default=0)
    ordinary_income_loss = db.Column(db.Integer, default=0)
    other_nonoperating_income_or_loss = db.Column(db.Integer, default=0)

    extraordinary_income_and_loss = db.Column(db.Integer, default=0)
    income_before_income_taxes = db.Column(db.Integer, default=0)
    income_taxes = db.Column(db.Integer, default=0)
    profit_loss_attributable_to_non_controling_interests = db.Column(db.Integer, default=0)
    profit_loss_attributable_to_owners_of_parent = db.Column(db.Integer, default=0)

    depreciation = db.Column(db.Integer, default=0)
    amortization_goodwill = db.Column(db.Integer, default=0)
    impairment = db.Column(db.Integer, default=0)

    ################  BS  ######################
    cash_and_deposits = db.Column(db.Integer, default=0)
    securities = db.Column(db.Integer, default=0)
    notes_and_accounts_receivable_trade = db.Column(db.Integer, default=0)
    inventories = db.Column(db.Integer, default=0)
    deferred_tax_assets_ca = db.Column(db.Integer, default=0)
    other_current_assets = db.Column(db.Integer, default=0)
    current_assets = db.Column(db.Integer, default=0)

    property_plant_and_equipment = db.Column(db.Integer, default=0)
    
    intangible_assets = db.Column(db.Integer, default=0)

    deferred_tax_assets_ioa = db.Column(db.Integer, default=0)
    investments_and_other_assets = db.Column(db.Integer, default=0)
    
    total_assets = db.Column(db.Integer, default=0)

    short_term_interest_bearing_bond = db.Column(db.Integer, default=0)
    notes_and_accounts_payable_trade = db.Column(db.Integer, default=0)
    deferred_tax_liabilities_ca = db.Column(db.Integer, default=0)
    other_current_liabilities = db.Column(db.Integer, default=0)
    current_liabilities = db.Column(db.Integer, default=0)

    long_term_interest_bearing_bond = db.Column(db.Integer, default=0)
    deferred_tax_liabilities_ncl = db.Column(db.Integer, default=0)
    other_noncurrent_liabilities = db.Column(db.Integer, default=0)
    noncurrent_liabilities = db.Column(db.Integer, default=0)

    capital_stock = db.Column(db.Integer, default=0)
    capital_surplus = db.Column(db.Integer, default=0)
    retained_earnings = db.Column(db.Integer, default=0)
    treasury_stock = db.Column(db.Integer, default=0)
    accumulated_other_comprehensive_income = db.Column(db.Integer, default=0)
    subscription_rights_to_shares = db.Column(db.Integer, default=0)
    non_controlling_interests = db.Column(db.Integer, default=0)
    net_assets = db.Column(db.Integer, default=0)

    liabilities_and_net_assets = db.Column(db.Integer, default=0)
    net_deferred_tax_assets = db.Column(db.Integer, default=0)
    fluctuations_in_deferred_tax_assets = db.Column(db.Integer, default=0)

    ################  SS  ######################
    net_assets_py = db.Column(db.Integer, default=0)
    issuance_of_new_shares = db.Column(db.Integer, default=0)
    dividends_ss = db.Column(db.Integer, default=0)
    purchase_of_treasury_stock = db.Column(db.Integer, default=0)
    disposal_of_treasury_stock = db.Column(db.Integer, default=0)

    ################  CF  ######################
    # cf_operating_activities = db.Column(db.Integer, default=0)
    # cf_investment_activities = db.Column(db.Integer, default=0)
    # cf_financing_activities = db.Column(db.Integer, default=0)

    ################ OHTER ####################
    total_number_of_issued_shares = db.Column(db.Integer, default=0)
    number_of_shares_held_in_own_name = db.Column(db.Integer, default=0)
    dividend_paid_per_share = db.Column(db.Integer, default=0)
    effective_tax_rate = db.Column(db.Float, default=0.0)

    ################ TAX_ON_OPERATING_INCOME ####################
    tax_on_interest_income_and_dividend = db.Column(db.Integer, default=0)
    tax_on_interest_expenses = db.Column(db.Integer, default=0)
    tax_on_non_operating_income_and_expenses_others = db.Column(db.Integer, default=0)
    tax_on_extraordinary_income_and_losses = db.Column(db.Integer, default=0)
    tax_on_operating_income = db.Column(db.Integer, default=0)

    ############### NOPAT_TOPDOWN #####################
    nopat_topdown = db.Column(db.Integer, default=0)

    ############### NOPAT_BOTTOMUP #####################
    nopat_bottomup = db.Column(db.Integer, default=0)

    ############### INVESTED_CAPITAL #####################
    net_working_capital = db.Column(db.Integer, default=0)
    investment_capital = db.Column(db.Integer, default=0)

    ############### FREE_CASH_FLOW #####################
    operating_cf = db.Column(db.Integer, default=0)
    investment_cf = db.Column(db.Integer, default=0)
    free_cash_flow = db.Column(db.Integer, default=0)
    non_operating_cf = db.Column(db.Integer, default=0)
    financial_cf = db.Column(db.Integer, default=0)
    net_cf = db.Column(db.Integer, default=0)

    ############### ROE #####################
    return_on_equity = db.Column(db.Float, default=0)
    return_on_asset = db.Column(db.Float, default=0)
    total_asset_turnover = db.Column(db.Float, default=0)
    financial_leverage = db.Column(db.Float, default=0)

    ############### WACC #####################
    borrowing_interest_rate = db.Column(db.Float, default=0)
    risk_free_rate = db.Column(db.Float, default=0)
    cost_of_shareholders_equity = db.Column(db.Float, default=0)
    wacc = db.Column(db.Float, default=0)

    ############### ROIC #####################
    return_on_invested_capital = db.Column(db.Float, default=0)
    return_on_invested_capital_before_tax = db.Column(db.Float, default=0)
    tax_burden_rate = db.Column(db.Float, default=0)
    affiliated_company_contribution_rate = db.Column(db.Float, default=0)
    operating_profit_margin = db.Column(db.Float, default=0)
    cost_rate = db.Column(db.Float, default=0)
    sga_ratio = db.Column(db.Float, default=0)
    invested_capital_turnover = db.Column(db.Float, default=0)
    net_working_capital_turnover_days = db.Column(db.Float, default=0)
    trade_receivavle_turnover_days = db.Column(db.Float, default=0)
    trade_payable_turnover_days = db.Column(db.Float, default=0)
    inventries_turnover_days = db.Column(db.Float, default=0)
    property_turnover_days = db.Column(db.Float, default=0)
    intangible_turnover_days = db.Column(db.Float, default=0)
    other_invested_capital_turnover_days = db.Column(db.Float, default=0)
    cash_conversion_cicle = db.Column(db.Float, default=0)

    valuation_01 = db.Column(db.Integer, default=0)
    wacc_adj_01 = db.Column(db.Float, default=0)
    grows_rate_01 = db.Column(db.Float, default=0)
    valuation_02 = db.Column(db.Integer, default=0)
    wacc_adj_02 = db.Column(db.Float, default=0)
    grows_rate_02 = db.Column(db.Float, default=0)
    valuation_03 = db.Column(db.Integer, default=0)
    wacc_adj_03 = db.Column(db.Float, default=0)
    grows_rate_03 = db.Column(db.Float, default=0)
    valuation_04 = db.Column(db.Integer, default=0)
    wacc_adj_04 = db.Column(db.Float, default=0)
    grows_rate_04 = db.Column(db.Float, default=0)
    valuation_05 = db.Column(db.Integer, default=0)
    wacc_adj_05 = db.Column(db.Float, default=0)
    grows_rate_05 = db.Column(db.Float, default=0)
    valuation_06 = db.Column(db.Integer, default=0)
    wacc_adj_06 = db.Column(db.Float, default=0)
    grows_rate_06 = db.Column(db.Float, default=0)
    valuation_07 = db.Column(db.Integer, default=0)
    wacc_adj_07 = db.Column(db.Float, default=0)
    grows_rate_07 = db.Column(db.Float, default=0)
    valuation_08 = db.Column(db.Integer, default=0)
    wacc_adj_08 = db.Column(db.Float, default=0)
    grows_rate_08 = db.Column(db.Float, default=0)
    valuation_09 = db.Column(db.Integer, default=0)
    wacc_adj_09 = db.Column(db.Float, default=0)
    grows_rate_09 = db.Column(db.Float, default=0)
    valuation_10 = db.Column(db.Integer, default=0)
    wacc_adj_10 = db.Column(db.Float, default=0)
    grows_rate_10 = db.Column(db.Float, default=0)
    valuation_11 = db.Column(db.Integer, default=0)
    wacc_adj_11 = db.Column(db.Float, default=0)
    grows_rate_11 = db.Column(db.Float, default=0)
    valuation_12 = db.Column(db.Integer, default=0)
    wacc_adj_12 = db.Column(db.Float, default=0)
    grows_rate_12 = db.Column(db.Float, default=0)
    valuation_13 = db.Column(db.Integer, default=0)
    wacc_adj_13 = db.Column(db.Float, default=0)
    grows_rate_13 = db.Column(db.Float, default=0)
    valuation_14 = db.Column(db.Integer, default=0)
    wacc_adj_14 = db.Column(db.Float, default=0)
    grows_rate_14 = db.Column(db.Float, default=0)
    valuation_15 = db.Column(db.Integer, default=0)
    wacc_adj_15 = db.Column(db.Float, default=0)
    grows_rate_15 = db.Column(db.Float, default=0)
    valuation_16 = db.Column(db.Integer, default=0)
    wacc_adj_16 = db.Column(db.Float, default=0)
    grows_rate_16 = db.Column(db.Float, default=0)
    valuation_17 = db.Column(db.Integer, default=0)
    wacc_adj_17 = db.Column(db.Float, default=0)
    grows_rate_17 = db.Column(db.Float, default=0)
    valuation_18 = db.Column(db.Integer, default=0)
    wacc_adj_18 = db.Column(db.Float, default=0)
    grows_rate_18 = db.Column(db.Float, default=0)
    valuation_19 = db.Column(db.Integer, default=0)
    wacc_adj_19 = db.Column(db.Float, default=0)
    grows_rate_19 = db.Column(db.Float, default=0)
    valuation_20 = db.Column(db.Integer, default=0)
    wacc_adj_20 = db.Column(db.Float, default=0)
    grows_rate_20 = db.Column(db.Float, default=0)
    valuation_21 = db.Column(db.Integer, default=0)
    wacc_adj_21 = db.Column(db.Float, default=0)
    grows_rate_21 = db.Column(db.Float, default=0)
    valuation_22 = db.Column(db.Integer, default=0)
    wacc_adj_22 = db.Column(db.Float, default=0)
    grows_rate_22 = db.Column(db.Float, default=0)
    valuation_23 = db.Column(db.Integer, default=0)
    wacc_adj_23 = db.Column(db.Float, default=0)
    grows_rate_23 = db.Column(db.Float, default=0)
    valuation_24 = db.Column(db.Integer, default=0)
    wacc_adj_24 = db.Column(db.Float, default=0)
    grows_rate_24 = db.Column(db.Float, default=0)
    valuation_25 = db.Column(db.Integer, default=0)
    wacc_adj_25 = db.Column(db.Float, default=0)
    grows_rate_25 = db.Column(db.Float, default=0)

    max_valuation = db.Column(db.Integer, default=0)
    min_valuation = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

