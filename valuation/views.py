import locale
locale.setlocale(locale.LC_NUMERIC,'ja_JP')

from flask import render_template, request, redirect, session, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from valuation._init_ import app
from valuation._init_ import db
from valuation.models.model import FinancialData,Users
from valuation.form import DataForm

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# https://ando-ando-ando.hatenablog.com/entry/2014/03/11/235129
@app.context_processor
def utility_processor():
    def format_currency(amount):
        return locale.format('%d', amount, True)
    return dict(format_currency=format_currency)


@app.route('/')
def index():
    return render_template('valuation/index.html')

@app.route('/input_financial_data', methods=['GET', 'POST'])
@login_required
def add_financial_data():
    if request.method == 'GET':
        return render_template('valuation/input_financial_data.html')
    if request.method == 'POST':

        # cookie_session = request.cookies.get('session')
        # _, data, timestamp, secret = cookie_session.split('.')
        # uid = data
        
        remember = request.cookies.get('remember_token')
        uid = remember

        ############### year ####################
        form_year_before_last = str(request.form.get('year_before_last'))
        form_last_year = str(request.form.get('last_year'))
        form_this_year = str(request.form.get('this_year'))

        ############### year_before_last : t - 2 ####################
        ybl_form_net_sales = int(request.form.get('ybl_net_sales'))
        ybl_form_cogs = int(request.form.get('ybl_cogs'))
        # form_gross_profit = request.form.get('gross_profit')
        ybl_form_sga = int(request.form.get('ybl_sga'))
        ybl_form_operating_income = int(request.form.get('ybl_operating_income'))

        ybl_form_interest_and_dividends_income = int(request.form.get('ybl_interest_and_dividends_income'))
        ybl_form_equity_in_earnings_or_losses_of_affiliates = int(request.form.get('ybl_equity_in_earnings_or_losses_of_affiliates'))
        # ybl_form_non_operating_income = int(request.form.get('ybl_non_operating_income'))

        ybl_form_interest_expenses = int(request.form.get('ybl_interest_expenses'))
        # ybl_form_equity_in_losses_of_affiliates = int(request.form.get('ybl_equity_in_losses_of_affiliates'))
        # ybl_form_non_operating_expenses = int(request.form.get('ybl_non_operating_expenses'))
        # ybl_calc_other_non_operating_expenses = ybl_form_non_operating_expenses - (ybl_form_interest_expenses + ybl_form_equity_in_losses_of_affiliates)
        ybl_form_ordinary_income_loss = int(request.form.get('ybl_ordinary_income_loss'))
        ybl_calc_other_non_operating_income_or_expense = ybl_form_ordinary_income_loss - (ybl_form_operating_income + ybl_form_interest_and_dividends_income + ybl_form_equity_in_earnings_or_losses_of_affiliates - ybl_form_interest_expenses)

        ybl_form_extraordinary_income_and_loss = int(request.form.get('ybl_extraordinary_income_and_loss'))
        ybl_form_income_before_income_taxes = int(request.form.get('ybl_income_before_income_taxes'))
        ybl_form_income_taxes = int(request.form.get('ybl_income_taxes'))
        ybl_form_profit_loss_attributable_to_non_controling_interests = int(request.form.get('ybl_profit_loss_attributable_to_non_controling_interests'))
        ybl_form_profit_loss_attributable_to_owners_of_parent = int(request.form.get('ybl_profit_loss_attributable_to_owners_of_parent'))

        ybl_form_depreciation = int(request.form.get('ybl_depreciation'))
        ybl_form_amortization_goodwill = int(request.form.get('ybl_amortization_goodwill'))
        ybl_form_impairment = int(request.form.get('ybl_impairment'))


        ################  BS  ######################
        ybl_form_cash_and_deposits = int(request.form.get('ybl_cash_and_deposits'))
        ybl_form_securities = int(request.form.get('ybl_securities'))
        ybl_form_notes_and_accounts_receivable_trade = int(request.form.get('ybl_notes_and_accounts_receivable_trade'))
        ybl_form_inventories = int(request.form.get('ybl_inventories'))
        ybl_form_deferred_tax_assets_ca = int(request.form.get('ybl_deferred_tax_assets_ca'))
        ybl_form_current_assets = int(request.form.get('ybl_current_assets'))
        ybl_calc_other_current_assets = ybl_form_current_assets - (ybl_form_cash_and_deposits + ybl_form_securities + ybl_form_notes_and_accounts_receivable_trade + ybl_form_inventories + ybl_form_deferred_tax_assets_ca)

        ybl_form_property_plant_and_equipment = int(request.form.get('ybl_property_plant_and_equipment'))
        
        ybl_form_intangible_assets = int(request.form.get('ybl_intangible_assets'))

        ybl_form_deferred_tax_assets_ioa = int(request.form.get('ybl_deferred_tax_assets_ioa'))
        ybl_form_investments_and_other_assets = int(request.form.get('ybl_investments_and_other_assets'))
        
        ybl_form_total_assets = int(request.form.get('ybl_total_assets'))

        ybl_form_short_term_interest_bearing_bond = int(request.form.get('ybl_short_term_interest_bearing_bond'))
        ybl_form_notes_and_accounts_payable_trade = int(request.form.get('ybl_notes_and_accounts_payable_trade'))
        ybl_form_deferred_tax_liabilities_ca = int(request.form.get('ybl_deferred_tax_liabilities_ca'))
        ybl_form_current_liabilities = int(request.form.get('ybl_current_liabilities'))
        ybl_calc_other_current_liabilities = ybl_form_current_liabilities - (ybl_form_short_term_interest_bearing_bond + ybl_form_notes_and_accounts_payable_trade + ybl_form_deferred_tax_liabilities_ca)

        ybl_form_long_term_interest_bearing_bond = int(request.form.get('ybl_long_term_interest_bearing_bond'))
        ybl_form_deferred_tax_liabilities_ncl = int(request.form.get('ybl_deferred_tax_liabilities_ncl'))
        ybl_form_noncurrent_liabilities = int(request.form.get('ybl_noncurrent_liabilities'))
        ybl_calc_other_noncurrent_liabilities = ybl_form_noncurrent_liabilities - (ybl_form_long_term_interest_bearing_bond + ybl_form_deferred_tax_liabilities_ncl)

        ybl_form_capital_stock = int(request.form.get('ybl_capital_stock'))
        ybl_form_capital_surplus = int(request.form.get('ybl_capital_surplus'))
        ybl_form_retained_earnings = int(request.form.get('ybl_retained_earnings'))
        ybl_form_treasury_stock = int(request.form.get('ybl_treasury_stock'))
        ybl_form_accumulated_other_comprehensive_income = int(request.form.get('ybl_accumulated_other_comprehensive_income'))
        ybl_form_subscription_rights_to_shares = int(request.form.get('ybl_subscription_rights_to_shares'))
        ybl_form_non_controlling_interests = int(request.form.get('ybl_non_controlling_interests'))
        ybl_form_net_assets = int(request.form.get('ybl_net_assets'))

        ybl_form_liabilities_and_net_assets = int(request.form.get('ybl_liabilities_and_net_assets'))
        ybl_calc_net_deferred_tax_assets = (ybl_form_deferred_tax_assets_ca + ybl_form_deferred_tax_assets_ioa) - (ybl_form_deferred_tax_liabilities_ca + ybl_form_deferred_tax_liabilities_ncl)

        ################  SS  ######################
        ybl_form_net_assets_py = int(request.form.get('ybl_net_assets_py'))
        ybl_form_issuance_of_new_shares = int(request.form.get('ybl_issuance_of_new_shares'))
        ybl_form_dividends_ss = int(request.form.get('ybl_dividends_ss'))
        ybl_form_purchase_of_treasury_stock = int(request.form.get('ybl_purchase_of_treasury_stock'))
        ybl_form_disposal_of_treasury_stock = int(request.form.get('ybl_disposal_of_treasury_stock'))

        ################  CF  ######################
        # ybl_form_cf_operating_activities = request.form.get('ybl_cf_operating_activities')
        # ybl_form_cf_investment_activities = request.form.get('ybl_cf_investment_activities')
        # ybl_form_cf_financing_activities = request.form.get('ybl_cf_financing_activities')

        ################ OHTER ####################
        ybl_form_total_number_of_issued_shares = int(request.form.get('ybl_total_number_of_issued_shares'))
        ybl_form_number_of_shares_held_in_own_name = int(request.form.get('ybl_number_of_shares_held_in_own_name'))
        ybl_form_dividend_paid_per_share = int(request.form.get('ybl_dividend_paid_per_share'))
        ybl_form_effective_tax_rate = float(request.form.get('ybl_effective_tax_rate')) / 100

        ############### INVESTED_CAPITAL #####################
        hhh = ybl_form_notes_and_accounts_receivable_trade
        iii = ybl_form_inventories
        jjj = ybl_calc_other_current_assets
        kkk = ybl_form_notes_and_accounts_payable_trade
        lll = ybl_calc_other_current_liabilities
        ybl_calc_net_working_capital = hhh + iii + jjj - kkk - lll
        mmm = ybl_form_property_plant_and_equipment
        nnn = ybl_form_intangible_assets
        ooo = ybl_calc_net_deferred_tax_assets
        ppp = ybl_form_investments_and_other_assets - ybl_form_deferred_tax_assets_ioa
        qqq = ybl_calc_other_noncurrent_liabilities
        rrr = ybl_form_cash_and_deposits
        sss = ybl_form_securities
        ybl_calc_invested_capital = ybl_calc_net_working_capital + mmm + nnn + ooo + ppp - qqq + rrr + sss



        ############### last_year : t - 1 ###########################
        ly_form_net_sales = int(request.form.get('ly_net_sales'))
        ly_form_cogs = int(request.form.get('ly_cogs'))
        # form_gross_profit = request.form.get('gross_profit')
        ly_form_sga = int(request.form.get('ly_sga'))
        ly_form_operating_income = int(request.form.get('ly_operating_income'))
        
        ly_form_interest_and_dividends_income = int(request.form.get('ly_interest_and_dividends_income'))
        ly_form_equity_in_earnings_or_losses_of_affiliates = int(request.form.get('ly_equity_in_earnings_or_losses_of_affiliates'))
        # ly_form_non_operating_income = int(request.form.get('ly_non_operating_income'))
        # ly_calc_other_non_operating_income = ly_form_non_operating_income - (ly_form_interest_and_dividends_income + ly_form_equity_in_earnings_of_affiliates)
        
        ly_form_interest_expenses = int(request.form.get('ly_interest_expenses'))
        # ly_form_equity_in_losses_of_affiliates = int(request.form.get('ly_equity_in_losses_of_affiliates'))
        # ly_form_non_operating_expenses = int(request.form.get('ly_non_operating_expenses'))
        ly_form_ordinary_income_loss = int(request.form.get('ly_ordinary_income_loss'))
        ly_calc_other_non_operating_income_and_expenses = ly_form_ordinary_income_loss - (ly_form_operating_income + ly_form_interest_and_dividends_income + ly_form_equity_in_earnings_or_losses_of_affiliates - ly_form_interest_expenses)

        ly_form_extraordinary_income_and_loss = int(request.form.get('ly_extraordinary_income_and_loss'))
        ly_form_income_before_income_taxes = int(request.form.get('ly_income_before_income_taxes'))
        ly_form_income_taxes = int(request.form.get('ly_income_taxes'))
        ly_form_profit_loss_attributable_to_non_controling_interests = int(request.form.get('ly_profit_loss_attributable_to_non_controling_interests'))
        ly_form_profit_loss_attributable_to_owners_of_parent = int(request.form.get('ly_profit_loss_attributable_to_owners_of_parent'))

        ly_form_depreciation = int(request.form.get('ly_depreciation'))
        ly_form_amortization_goodwill = int(request.form.get('ly_amortization_goodwill'))
        ly_form_impairment = int(request.form.get('ly_impairment'))


        ################  BS  ######################
        ly_form_cash_and_deposits = int(request.form.get('ly_cash_and_deposits'))
        ly_form_securities = int(request.form.get('ly_securities'))
        ly_form_notes_and_accounts_receivable_trade = int(request.form.get('ly_notes_and_accounts_receivable_trade'))
        ly_form_inventories = int(request.form.get('ly_inventories'))
        ly_form_deferred_tax_assets_ca = int(request.form.get('ly_deferred_tax_assets_ca'))
        ly_form_current_assets = int(request.form.get('ly_current_assets'))
        ly_calc_other_current_assets = ly_form_current_assets - (ly_form_cash_and_deposits + ly_form_securities + ly_form_notes_and_accounts_receivable_trade + ly_form_inventories + ly_form_deferred_tax_assets_ca)

        ly_form_property_plant_and_equipment = int(request.form.get('ly_property_plant_and_equipment'))
        
        ly_form_intangible_assets = int(request.form.get('ly_intangible_assets'))

        ly_form_deferred_tax_assets_ioa = int(request.form.get('ly_deferred_tax_assets_ioa'))
        ly_form_investments_and_other_assets = int(request.form.get('ly_investments_and_other_assets'))
        
        ly_form_total_assets = int(request.form.get('ly_total_assets'))

        ly_form_short_term_interest_bearing_bond = int(request.form.get('ly_short_term_interest_bearing_bond'))
        ly_form_notes_and_accounts_payable_trade = int(request.form.get('ly_notes_and_accounts_payable_trade'))
        ly_form_deferred_tax_liabilities_ca = int(request.form.get('ly_deferred_tax_liabilities_ca'))
        ly_form_current_liabilities = int(request.form.get('ly_current_liabilities'))
        ly_calc_other_current_liabilities = ly_form_current_liabilities - (ly_form_short_term_interest_bearing_bond + ly_form_notes_and_accounts_payable_trade + ly_form_deferred_tax_liabilities_ca)

        ly_form_long_term_interest_bearing_bond = int(request.form.get('ly_long_term_interest_bearing_bond'))
        ly_form_deferred_tax_liabilities_ncl = int(request.form.get('ly_deferred_tax_liabilities_ncl'))
        ly_form_noncurrent_liabilities = int(request.form.get('ly_noncurrent_liabilities'))
        ly_calc_other_noncurrent_liabilities = ly_form_noncurrent_liabilities - (ly_form_long_term_interest_bearing_bond + ly_form_deferred_tax_liabilities_ncl)

        ly_form_capital_stock = int(request.form.get('ly_capital_stock'))
        ly_form_capital_surplus = int(request.form.get('ly_capital_surplus'))
        ly_form_retained_earnings = int(request.form.get('ly_retained_earnings'))
        ly_form_treasury_stock = int(request.form.get('ly_treasury_stock'))
        ly_form_accumulated_other_comprehensive_income = int(request.form.get('ly_accumulated_other_comprehensive_income'))
        ly_form_subscription_rights_to_shares = int(request.form.get('ly_subscription_rights_to_shares'))
        ly_form_non_controlling_interests = int(request.form.get('ly_non_controlling_interests'))
        ly_form_net_assets = int(request.form.get('ly_net_assets'))

        ly_form_liabilities_and_net_assets = int(request.form.get('ly_liabilities_and_net_assets'))
        ly_calc_net_deferred_tax_assets = (ly_form_deferred_tax_assets_ca + ly_form_deferred_tax_assets_ioa) - (ly_form_deferred_tax_liabilities_ca + ly_form_deferred_tax_liabilities_ncl)
        ly_calc_fluctuations_in_deferred_tax_assets = ly_calc_net_deferred_tax_assets - ybl_calc_net_deferred_tax_assets


        ################  SS  ######################
        ly_form_net_assets_py = int(request.form.get('ly_net_assets_py'))
        ly_form_issuance_of_new_shares = int(request.form.get('ly_issuance_of_new_shares'))
        ly_form_dividends_ss = int(request.form.get('ly_dividends_ss'))
        ly_form_purchase_of_treasury_stock = int(request.form.get('ly_purchase_of_treasury_stock'))
        ly_form_disposal_of_treasury_stock = int(request.form.get('ly_disposal_of_treasury_stock'))
        ly_calc_other_ss = ly_form_net_assets - (ly_form_net_assets_py + ly_form_profit_loss_attributable_to_owners_of_parent + ly_form_issuance_of_new_shares - ly_form_dividends_ss -ly_form_purchase_of_treasury_stock + ly_form_disposal_of_treasury_stock)

        ################  CF  ######################
        # ly_form_cf_operating_activities = request.form.get('ly_cf_operating_activities')
        # ly_form_cf_investment_activities = request.form.get('ly_cf_investment_activities')
        # ly_form_cf_financing_activities = request.form.get('ly_cf_financing_activities')

        ################ OHTER ####################
        ly_form_total_number_of_issued_shares = int(request.form.get('ly_total_number_of_issued_shares'))
        ly_form_number_of_shares_held_in_own_name = int(request.form.get('ly_number_of_shares_held_in_own_name'))
        ly_form_dividend_paid_per_share = int(request.form.get('ly_dividend_paid_per_share'))
        ly_form_effective_tax_rate = float(request.form.get('ly_effective_tax_rate')) / 100

        ############### TAX_ON_OPERATING_INCOME #####################
        # a
        ly_calc_tax_on_interest_income_and_dividend = ly_form_interest_and_dividends_income * ly_form_effective_tax_rate

        # b
        ly_calc_tax_on_interest_expaneses = ly_form_interest_expenses * ly_form_effective_tax_rate
                
        # c = (その他営業外収益 - その他営業外費用) * effective tax rate
        ly_calc_tax_on_non_operating_income_and_expenses_others = (ly_calc_other_non_operating_income_and_expenses) * ly_form_effective_tax_rate
        
        # d
        ly_calc_tax_on_extraordinary_income_and_losses = ly_form_extraordinary_income_and_loss * ly_form_effective_tax_rate
        
        # e = income taxes - a + b - c - d
        ly_calc_tax_on_operating_income = ly_form_income_taxes - ly_calc_tax_on_interest_income_and_dividend + ly_calc_tax_on_interest_expaneses - ly_calc_tax_on_non_operating_income_and_expenses_others - ly_calc_tax_on_extraordinary_income_and_losses

        ############### NOPAT_TOPDOWN #####################
        # 営業利益 - 営業利益にかかる税金 + DTA（純額）の減少（増加はマイナス） + 持分法投資利益（損失はマイナス）
        ly_calc_nopat_topdown = ly_form_operating_income - ly_calc_tax_on_operating_income - ly_calc_fluctuations_in_deferred_tax_assets + ly_form_equity_in_earnings_or_losses_of_affiliates


        ############### NOPAT_BOTTOMUP #####################
        # 親会社株主当期純利益 + 非支配株主当期純利益 + DTA（純額)の減少（増加はマイナス） + (特別損益 * (1-実効税率)) - (（受取利息+受取配当金) * (1-実効税率)) + (支払利息 * (1-実効税率)) + ((その他営業外損失 - その他営業外利益) * (1-実効税率))
        a = ly_form_profit_loss_attributable_to_owners_of_parent
        b = ly_form_profit_loss_attributable_to_non_controling_interests
        c = ly_calc_fluctuations_in_deferred_tax_assets
        d = ly_form_extraordinary_income_and_loss * (1 - ly_form_effective_tax_rate)
        e = ly_form_interest_and_dividends_income * (1 - ly_form_effective_tax_rate)
        f = ly_form_interest_expenses * (1 - ly_form_effective_tax_rate)
        g = ly_calc_other_non_operating_income_and_expenses * (1 - ly_form_effective_tax_rate)
        ly_calc_nopat_bottomup = a + b - c - d - e + f - g

        ############### INVESTED_CAPITAL #####################
        h = ly_form_notes_and_accounts_receivable_trade
        i = ly_form_inventories
        j = ly_calc_other_current_assets
        k = ly_form_notes_and_accounts_payable_trade
        l = ly_calc_other_current_liabilities
        ly_calc_net_working_capital = h + i + j - k - l
        m = ly_form_property_plant_and_equipment
        n = ly_form_intangible_assets
        o = ly_calc_net_deferred_tax_assets
        p = ly_form_investments_and_other_assets - ly_form_deferred_tax_assets_ioa
        q = ly_calc_other_noncurrent_liabilities
        r = ly_form_cash_and_deposits
        s = ly_form_securities
        ly_calc_invested_capital = ly_calc_net_working_capital + m + n + o + p - q + r + s

        ############### FREE_CASH_FLOW #####################
        ly_calc_operating_cf = ly_calc_nopat_topdown + ly_form_depreciation + ly_form_amortization_goodwill + (ybl_calc_net_working_capital - ly_calc_net_working_capital)
        ly_calc_investment_cf = -1 * ((ly_form_property_plant_and_equipment + ly_form_intangible_assets) - (ybl_form_property_plant_and_equipment + ybl_form_intangible_assets) + (ly_form_depreciation + ly_form_impairment + ly_form_amortization_goodwill))
        ly_calc_free_cash_flow = ly_calc_operating_cf + ly_calc_investment_cf
        ly_calc_non_operating_cf = -1 * (b - c - d - e + f - g) - c - (((ly_form_investments_and_other_assets - ly_form_deferred_tax_assets_ioa) - ly_calc_other_noncurrent_liabilities) - ((ybl_form_investments_and_other_assets - ybl_form_deferred_tax_assets_ioa) - ybl_calc_other_noncurrent_liabilities))

        ly_calc_financial_cf = ((ly_form_short_term_interest_bearing_bond + ly_form_long_term_interest_bearing_bond) - (ybl_form_short_term_interest_bearing_bond + ybl_form_long_term_interest_bearing_bond)) - ly_form_dividends_ss + ly_form_issuance_of_new_shares - ly_form_purchase_of_treasury_stock + ly_form_disposal_of_treasury_stock + ly_calc_other_ss
        ly_calc_net_cf = ly_calc_free_cash_flow + ly_calc_non_operating_cf + ly_calc_financial_cf

        ############### ROE #####################
        ly_calc_shareholders_equity = (ly_form_capital_stock + ly_form_capital_surplus + ly_form_retained_earnings + ly_form_treasury_stock + ly_form_accumulated_other_comprehensive_income)
        ly_calc_shareholders_equity_py = (ybl_form_capital_stock + ybl_form_capital_surplus + ybl_form_retained_earnings + ybl_form_treasury_stock + ybl_form_accumulated_other_comprehensive_income)
        ly_calc_average_shareholders_equity = (ly_calc_shareholders_equity + ly_calc_shareholders_equity_py) * 1/2
        ly_calc_return_on_equity = ly_form_profit_loss_attributable_to_owners_of_parent / ly_calc_average_shareholders_equity
        ly_calc_return_on_asset = ly_form_profit_loss_attributable_to_owners_of_parent / ly_form_net_sales
        ly_calc_total_asset_turnover = ly_form_net_sales / ((ly_form_total_assets + ybl_form_total_assets) * 1/2 )
        ly_calc_financial_leverage = ((ly_form_total_assets + ybl_form_total_assets) * 1/2) / ly_calc_average_shareholders_equity

        ############### WACC #####################


        ############### ROIC #####################
        ly_calc_return_on_invested_capital = ly_calc_nopat_topdown / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
        ly_calc_return_on_invested_capital_before_tax = ly_form_operating_income / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
        ly_calc_tax_burden_rate = ly_calc_tax_on_operating_income / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
        ly_calc_affiliated_company_contribution_rate = ly_form_equity_in_earnings_or_losses_of_affiliates / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
        ly_calc_operating_profit_margin = ly_form_operating_income / ly_form_net_sales
        ly_calc_cost_rate = ly_form_cogs / ly_form_net_sales
        ly_calc_sga_ratio = ly_form_sga / ly_form_net_sales
        ly_calc_invested_capital_turnover = ly_form_net_sales / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
        ly_calc_net_working_capital_turnover_days = ly_calc_net_working_capital / (ly_form_net_sales / 365)
        ly_calc_trade_receivable_turnover_days = ly_form_notes_and_accounts_receivable_trade / (ly_form_net_sales / 365)
        ly_calc_trade_payable_turnover_days = ly_form_notes_and_accounts_payable_trade / (ly_form_net_sales / 365)
        ly_calc_inventries_turnover_days = ly_form_inventories / (ly_form_net_sales / 365)
        ly_calc_property_turnover_days = ly_form_property_plant_and_equipment / (ly_form_net_sales / 365)
        ly_calc_intangible_turnover_days = ly_form_intangible_assets / (ly_form_net_sales / 365)
        ly_calc_other_invested_capital_turnover_days = (ly_calc_invested_capital - ly_calc_net_working_capital - ly_form_inventories - ly_form_property_plant_and_equipment - ly_form_intangible_assets) / (ly_form_net_sales / 365)
        ly_calc_cash_conversion_cicle = ly_calc_inventries_turnover_days + ly_calc_trade_receivable_turnover_days - ly_calc_trade_payable_turnover_days


        ############### this_year : t ###############################
        form_net_sales = int(request.form.get('net_sales'))
        form_cogs = int(request.form.get('cogs'))
        # form_gross_profit = request.form.get('gross_profit')
        form_sga = int(request.form.get('sga'))
        form_operating_income = int(request.form.get('operating_income'))
        
        form_interest_and_dividends_income = int(request.form.get('interest_and_dividends_income'))
        form_equity_in_earnings_or_losses_of_affiliates = int(request.form.get('equity_in_earnings_or_losses_of_affiliates'))
        # form_non_operating_income = int(request.form.get('non_operating_income'))
        # calc_other_non_operating_income = form_non_operating_income - (form_interest_and_dividends_income + form_equity_in_earnings_of_affiliates)

        form_interest_expenses = int(request.form.get('interest_expenses'))
        # form_equity_in_losses_of_affiliates = int(request.form.get('equity_in_losses_of_affiliates'))
        # form_non_operating_expenses = int(request.form.get('non_operating_expenses'))
        form_ordinary_income_loss = int(request.form.get('ordinary_income_loss'))
        calc_other_non_operating_income_and_expenses = form_ordinary_income_loss - (form_operating_income + form_interest_and_dividends_income + form_equity_in_earnings_or_losses_of_affiliates - form_interest_expenses)
        
        form_extraordinary_income_and_loss = int(request.form.get('extraordinary_income_and_loss'))
        form_income_before_income_taxes = int(request.form.get('income_before_income_taxes'))
        form_income_taxes = int(request.form.get('income_taxes'))
        form_profit_loss_attributable_to_non_controling_interests = int(request.form.get('profit_loss_attributable_to_non_controling_interests'))
        form_profit_loss_attributable_to_owners_of_parent = int(request.form.get('profit_loss_attributable_to_owners_of_parent'))

        form_depreciation = int(request.form.get('depreciation'))
        form_amortization_goodwill = int(request.form.get('amortization_goodwill'))
        form_impairment = int(request.form.get('impairment'))


        ################  BS  ######################
        form_cash_and_deposits = int(request.form.get('cash_and_deposits'))
        form_securities = int(request.form.get('securities'))
        form_notes_and_accounts_receivable_trade = int(request.form.get('notes_and_accounts_receivable_trade'))
        form_inventories = int(request.form.get('inventories'))
        form_deferred_tax_assets_ca = int(request.form.get('deferred_tax_assets_ca'))
        form_current_assets = int(request.form.get('current_assets'))
        calc_other_current_assets = form_current_assets - (form_cash_and_deposits + form_securities + form_notes_and_accounts_receivable_trade + form_inventories + form_deferred_tax_assets_ca)

        form_property_plant_and_equipment = int(request.form.get('property_plant_and_equipment'))
        
        form_intangible_assets = int(request.form.get('intangible_assets'))

        form_deferred_tax_assets_ioa = int(request.form.get('deferred_tax_assets_ioa'))
        form_investments_and_other_assets = int(request.form.get('investments_and_other_assets'))
        
        form_total_assets = int(request.form.get('total_assets'))

        form_short_term_interest_bearing_bond = int(request.form.get('short_term_interest_bearing_bond'))
        form_notes_and_accounts_payable_trade = int(request.form.get('notes_and_accounts_payable_trade'))
        form_deferred_tax_liabilities_ca = int(request.form.get('deferred_tax_liabilities_ca'))
        form_current_liabilities = int(request.form.get('current_liabilities'))
        calc_other_current_liabilities = form_current_liabilities - (form_short_term_interest_bearing_bond + form_notes_and_accounts_payable_trade + form_deferred_tax_liabilities_ca)

        form_long_term_interest_bearing_bond = int(request.form.get('long_term_interest_bearing_bond'))
        form_deferred_tax_liabilities_ncl = int(request.form.get('deferred_tax_liabilities_ncl'))
        form_noncurrent_liabilities = int(request.form.get('noncurrent_liabilities'))
        calc_other_noncurrent_liabilities = form_noncurrent_liabilities - (form_long_term_interest_bearing_bond + form_deferred_tax_liabilities_ncl)

        form_capital_stock = int(request.form.get('capital_stock'))
        form_capital_surplus = int(request.form.get('capital_surplus'))
        form_retained_earnings = int(request.form.get('retained_earnings'))
        form_treasury_stock = int(request.form.get('treasury_stock'))
        form_accumulated_other_comprehensive_income = int(request.form.get('accumulated_other_comprehensive_income'))
        form_subscription_rights_to_shares = int(request.form.get('subscription_rights_to_shares'))
        form_non_controlling_interests = int(request.form.get('non_controlling_interests'))
        form_net_assets = int(request.form.get('net_assets'))

        form_liabilities_and_net_assets = int(request.form.get('liabilities_and_net_assets'))
        calc_net_deferred_tax_assets = (form_deferred_tax_assets_ca + form_deferred_tax_assets_ioa) - (form_deferred_tax_liabilities_ca + form_deferred_tax_liabilities_ncl)
        calc_fluctuations_in_deferred_tax_assets = calc_net_deferred_tax_assets - ly_calc_net_deferred_tax_assets


        ################  SS  ######################
        form_net_assets_py = int(request.form.get('net_assets_py'))
        form_issuance_of_new_shares = int(request.form.get('issuance_of_new_shares'))
        form_dividends_ss = int(request.form.get('dividends_ss'))
        form_purchase_of_treasury_stock = int(request.form.get('purchase_of_treasury_stock'))
        form_disposal_of_treasury_stock = int(request.form.get('disposal_of_treasury_stock'))
        calc_other_ss = form_net_assets - (form_net_assets_py + form_profit_loss_attributable_to_owners_of_parent + form_issuance_of_new_shares - form_dividends_ss - form_purchase_of_treasury_stock + form_disposal_of_treasury_stock)

        ################  CF  ######################
        # form_cf_operating_activities = request.form.get('cf_operating_activities')
        # form_cf_investment_activities = request.form.get('cf_investment_activities')
        # form_cf_financing_activities = request.form.get('cf_financing_activities')

        ################ OHTER ####################
        form_total_number_of_issued_shares = int(request.form.get('total_number_of_issued_shares'))
        form_number_of_shares_held_in_own_name = int(request.form.get('number_of_shares_held_in_own_name'))
        form_dividend_paid_per_share = int(request.form.get('dividend_paid_per_share'))
        form_effective_tax_rate = float(request.form.get('effective_tax_rate')) / 100

        ############### TAX_ON_OPERATING_INCOME #####################
        # a
        calc_tax_on_interest_income_and_dividend = form_interest_and_dividends_income * form_effective_tax_rate

        # b
        calc_tax_on_interest_expaneses =form_interest_expenses * form_effective_tax_rate
                
        # c = (その他営業外収益 - その他営業外費用) * effective tax rate
        calc_tax_on_non_operating_income_and_expenses_others = calc_other_non_operating_income_and_expenses * form_effective_tax_rate
        
        # d
        calc_tax_on_extraordinary_income_and_losses = form_extraordinary_income_and_loss * form_effective_tax_rate
        
        # e = income taxes - a + b - c - d
        calc_tax_on_operating_income = form_income_taxes - calc_tax_on_interest_income_and_dividend + calc_tax_on_interest_expaneses - calc_tax_on_non_operating_income_and_expenses_others - calc_tax_on_extraordinary_income_and_losses

        ############### NOPAT_TOPDOWN #####################
        # 営業利益 - 営業利益にかかる税金 + DTA（純額）の減少（増加はマイナス） + 持分法投資利益（損失はマイナス）
        calc_nopat_topdown = form_operating_income - calc_tax_on_operating_income - calc_fluctuations_in_deferred_tax_assets + form_equity_in_earnings_or_losses_of_affiliates


        ############### NOPAT_BOTTOMUP #####################
        # 親会社株主当期純利益 + 非支配株主当期純利益 + DTA（純額)の減少（増加はマイナス） + (特別損益 * (1-実効税率)) - (（受取利息+受取配当金) * (1-実効税率)) + (支払利息 * (1-実効税率)) + ((その他営業外損失 - その他営業外利益) * (1-実効税率))
        aa = form_profit_loss_attributable_to_owners_of_parent
        bb = form_profit_loss_attributable_to_non_controling_interests
        cc = calc_fluctuations_in_deferred_tax_assets
        dd = form_extraordinary_income_and_loss * (1 - form_effective_tax_rate)
        ee = form_interest_and_dividends_income * (1 - form_effective_tax_rate)
        ff = form_interest_expenses * (1 - form_effective_tax_rate)
        gg = calc_other_non_operating_income_and_expenses * (1 - form_effective_tax_rate)
        calc_nopat_bottomup = aa + bb - cc - dd - ee + ff - gg

        ############### INVESTMENT_CAPITAL #####################
        hh = form_notes_and_accounts_receivable_trade
        ii = form_inventories
        jj = calc_other_current_assets
        kk = form_notes_and_accounts_payable_trade
        ll = calc_other_current_liabilities
        calc_net_working_capital = hh + ii + jj - kk - ll
        mm = form_property_plant_and_equipment
        nn = form_intangible_assets
        oo = calc_net_deferred_tax_assets
        pp = form_investments_and_other_assets - form_deferred_tax_assets_ioa
        qq = calc_other_noncurrent_liabilities
        rr = form_cash_and_deposits
        ss = form_securities
        calc_invested_capital = calc_net_working_capital + mm + nn + oo + pp - qq + rr + ss

        ############### FREE_CASH_FLOW #####################
        calc_operating_cf = calc_nopat_topdown + form_depreciation + form_amortization_goodwill + (ly_calc_net_working_capital - calc_net_working_capital)
        calc_investment_cf = -1 * ((form_property_plant_and_equipment + form_intangible_assets) - (ly_form_property_plant_and_equipment + ly_form_intangible_assets) + (form_depreciation + form_impairment + form_amortization_goodwill))
        calc_free_cash_flow = calc_operating_cf + calc_investment_cf
        calc_non_operating_cf = -1 * (bb - cc - dd - ee + ff - gg) - cc - (((form_investments_and_other_assets - form_deferred_tax_assets_ioa) - calc_other_noncurrent_liabilities) - ((ly_form_investments_and_other_assets - ly_form_deferred_tax_assets_ioa) - ly_calc_other_noncurrent_liabilities))
        calc_financial_cf = ((form_short_term_interest_bearing_bond + form_long_term_interest_bearing_bond) - (ly_form_short_term_interest_bearing_bond + ly_form_long_term_interest_bearing_bond)) - form_dividends_ss + form_issuance_of_new_shares - form_purchase_of_treasury_stock + form_disposal_of_treasury_stock + calc_other_ss
        calc_net_cf = calc_free_cash_flow + calc_non_operating_cf + calc_financial_cf


        ############### ROE #####################
        calc_shareholders_equity = (form_capital_stock + form_capital_surplus + form_retained_earnings + form_treasury_stock + form_accumulated_other_comprehensive_income)
        calc_shareholders_equity_py = (ly_form_capital_stock + ly_form_capital_surplus + ly_form_retained_earnings + ly_form_treasury_stock + ly_form_accumulated_other_comprehensive_income)
        calc_average_shareholders_equity = (calc_shareholders_equity + calc_shareholders_equity_py) * 1/2
        calc_return_on_equity = form_profit_loss_attributable_to_owners_of_parent / calc_average_shareholders_equity
        calc_return_on_asset = form_profit_loss_attributable_to_owners_of_parent / form_net_sales
        calc_total_asset_turnover = form_net_sales / ((form_total_assets + ly_form_total_assets) * 1/2 )
        calc_financial_leverage = ((form_total_assets + ly_form_total_assets) * 1/2) / calc_average_shareholders_equity
        
        ############### WACC #####################  βを加味できていない
        form_borrowing_interest_rate = float(request.form.get('borrowing_interest_rate')) / 100
        RISK_FREE_RATE = 0.2 / 100                 # 2022/3/1〜2022/3/24 の10年物国債利率の平均
        COST_OF_SHAREHOLDERS_EQUITY = 8.0 / 100    # 株主の期待リターン。ここでは伊藤レポートに合わせて8%とした。
        calc_wacc = form_borrowing_interest_rate * ((form_short_term_interest_bearing_bond + form_long_term_interest_bearing_bond) / (form_short_term_interest_bearing_bond + form_long_term_interest_bearing_bond + calc_shareholders_equity)) + COST_OF_SHAREHOLDERS_EQUITY * (calc_shareholders_equity / (form_short_term_interest_bearing_bond + form_long_term_interest_bearing_bond + calc_shareholders_equity))

        ############### ROIC #####################
        calc_return_on_invested_capital = calc_nopat_topdown / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
        calc_return_on_invested_capital_before_tax = form_operating_income / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
        calc_tax_burden_rate = calc_tax_on_operating_income / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
        calc_affiliated_company_contribution_rate = form_equity_in_earnings_or_losses_of_affiliates / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
        calc_operating_profit_margin = form_operating_income / form_net_sales
        calc_cost_rate = form_cogs / form_net_sales
        calc_sga_ratio = form_sga / form_net_sales
        calc_invested_capital_turnover = form_net_sales / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
        calc_net_working_capital_turnover_days = calc_net_working_capital / (form_net_sales / 365)
        calc_trade_receivable_turnover_days = form_notes_and_accounts_receivable_trade / (form_net_sales / 365)
        calc_trade_payable_turnover_days = form_notes_and_accounts_payable_trade / (form_net_sales / 365)
        calc_inventries_turnover_days = form_inventories / (form_net_sales / 365)
        calc_property_turnover_days = form_property_plant_and_equipment / (form_net_sales / 365)
        calc_intangible_turnover_days = form_intangible_assets / (form_net_sales / 365)
        calc_other_invested_capital_turnover_days = (calc_invested_capital - calc_net_working_capital - form_inventories - form_property_plant_and_equipment - form_intangible_assets) / (form_net_sales / 365)
        calc_cash_conversion_cicle = calc_inventries_turnover_days + calc_trade_receivable_turnover_days - calc_trade_payable_turnover_days

        ############### VALUATION #################
        R = [-0.02, 0, 0.02, 0.04, 0.06]               # 成長率
        S = [-0.015, -0.01, 0, 0.01, 0.015]               # WACCに対するストレス
        wacc_adj = []
        grows_rate = []
        calc_valuation = []                             # 5 * 5 = 25 通りのvaluationを実施
        calc_max_valuation = 0                          # valuation の最大値を保持
        calc_min_valuation = 10**16                     # valuation の最小値を保持
        for r in R:
            for s in S:
                try:
                    v = calc_free_cash_flow / ((calc_wacc + s) - r)
                    calc_valuation.append(v)
                    wacc_adj.append(calc_wacc + s)
                    grows_rate.append(r)
                    if calc_max_valuation < v:
                        calc_max_valuation = v
                    if calc_min_valuation > v:
                        calc_min_valuation = v
                except:
                    calc_valuation.append("NaN")
                    wacc_adj.append(calc_wacc + s)
                    grows_rate.append(r)



        financial_data = FinancialData(
            uid = uid,
            year_before_last = form_year_before_last,
            last_year = form_last_year,
            this_year = form_this_year,

            ############### year_before_last : t - 2 ####################
            ybl_net_sales = ybl_form_net_sales,
            ybl_cogs = ybl_form_cogs,
            # gross_profit = form_gross_profit,
            ybl_sga = ybl_form_sga,
            ybl_operating_income = ybl_form_operating_income,
            
            ybl_interest_and_dividends_income = ybl_form_interest_and_dividends_income,
            ybl_equity_in_earnings_or_losses_of_affiliates = ybl_form_equity_in_earnings_or_losses_of_affiliates,
            # ybl_other_non_operating_income = ybl_calc_other_non_operating_income,
            # ybl_non_operating_income = ybl_form_non_operating_income,

            ybl_interest_expenses = ybl_form_interest_expenses,
            # ybl_equity_in_losses_of_affiliates = ybl_form_equity_in_losses_of_affiliates,
            # ybl_other_non_operating_expenses = ybl_calc_other_non_operating_expenses,
            # ybl_non_operating_expenses = ybl_form_non_operating_expenses,
            ybl_ordinary_income_loss = ybl_form_ordinary_income_loss,
            ybl_other_nonoperating_income_or_loss = ybl_calc_other_non_operating_income_or_expense,
            
            ybl_extraordinary_income_and_loss = ybl_form_extraordinary_income_and_loss,
            ybl_income_before_income_taxes = ybl_form_income_before_income_taxes,
            ybl_income_taxes = ybl_form_income_taxes,
            ybl_profit_loss_attributable_to_non_controling_interests = ybl_form_profit_loss_attributable_to_non_controling_interests,
            ybl_profit_loss_attributable_to_owners_of_parent = ybl_form_profit_loss_attributable_to_owners_of_parent,

            ybl_depreciation = ybl_form_depreciation,
            ybl_amortization_goodwill = ybl_form_amortization_goodwill,
            ybl_impairment = ybl_form_impairment,

            ################  BS  ######################
            ybl_cash_and_deposits = ybl_form_cash_and_deposits,
            ybl_securities = ybl_form_securities,
            ybl_notes_and_accounts_receivable_trade = ybl_form_notes_and_accounts_receivable_trade,
            ybl_inventories = ybl_form_inventories,
            ybl_deferred_tax_assets_ca = ybl_form_deferred_tax_assets_ca,
            ybl_other_current_assets = ybl_calc_other_current_assets,
            ybl_current_assets = ybl_form_current_assets,

            ybl_property_plant_and_equipment = ybl_form_property_plant_and_equipment,
            
            ybl_intangible_assets = ybl_form_intangible_assets,

            ybl_deferred_tax_assets_ioa = ybl_form_deferred_tax_assets_ioa,
            ybl_investments_and_other_assets = ybl_form_investments_and_other_assets,
            
            ybl_total_assets = ybl_form_total_assets,

            ybl_short_term_interest_bearing_bond = ybl_form_short_term_interest_bearing_bond,
            ybl_notes_and_accounts_payable_trade = ybl_form_notes_and_accounts_payable_trade,
            ybl_deferred_tax_liabilities_ca = ybl_form_deferred_tax_liabilities_ca,
            ybl_other_current_liabilities = ybl_calc_other_current_liabilities,
            ybl_current_liabilities = ybl_form_current_liabilities,

            ybl_long_term_interest_bearing_bond = ybl_form_long_term_interest_bearing_bond,
            ybl_deferred_tax_liabilities_ncl = ybl_form_deferred_tax_liabilities_ncl,
            ybl_other_noncurrent_liabilities = ybl_calc_other_noncurrent_liabilities,
            ybl_noncurrent_liabilities = ybl_form_noncurrent_liabilities,

            ybl_capital_stock = ybl_form_capital_stock,
            ybl_capital_surplus = ybl_form_capital_surplus,
            ybl_retained_earnings = ybl_form_retained_earnings,
            ybl_treasury_stock = ybl_form_treasury_stock,
            ybl_accumulated_other_comprehensive_income = ybl_form_accumulated_other_comprehensive_income,
            ybl_subscription_rights_to_shares = ybl_form_subscription_rights_to_shares,
            ybl_non_controlling_interests = ybl_form_non_controlling_interests,
            ybl_net_assets = ybl_form_net_assets,

            ybl_liabilities_and_net_assets = ybl_form_liabilities_and_net_assets,
            ybl_net_deferred_tax_assets = ybl_calc_net_deferred_tax_assets,

            ################  SS  ######################
            ybl_net_assets_py = ybl_form_net_assets_py,
            ybl_issuance_of_new_shares = ybl_form_issuance_of_new_shares,
            ybl_dividends_ss = ybl_form_dividends_ss,
            ybl_purchase_of_treasury_stock = ybl_form_purchase_of_treasury_stock,
            ybl_disposal_of_treasury_stock = ybl_form_disposal_of_treasury_stock,

            ################  CF  ######################
            # ybl_cf_operating_activities = ybl_form_cf_operating_activities,
            # ybl_cf_investment_activities = ybl_form_cf_investment_activities,
            # ybl_cf_financing_activities = ybl_form_cf_financing_activities,

            ################ OHTER ####################
            ybl_total_number_of_issued_shares = ybl_form_total_number_of_issued_shares,
            ybl_number_of_shares_held_in_own_name = ybl_form_number_of_shares_held_in_own_name,
            ybl_dividend_paid_per_share = ybl_form_dividend_paid_per_share,
            ybl_effective_tax_rate = ybl_form_effective_tax_rate,

            ############### INVESTED_CAPITAL #####################
            ybl_invested_capital = ybl_calc_invested_capital,


            ############### last_year : t - 1 ###########################
            ly_net_sales = ly_form_net_sales,
            ly_cogs = ly_form_cogs,
            # gross_profit = form_gross_profit,
            ly_sga = ly_form_sga,
            ly_operating_income = ly_form_operating_income,

            ly_interest_and_dividends_income = ly_form_interest_and_dividends_income,
            ly_equity_in_earnings_or_losses_of_affiliates = ly_form_equity_in_earnings_or_losses_of_affiliates,
            # ly_other_non_operating_income = ly_calc_other_non_operating_income,
            # ly_non_operating_income = ly_form_non_operating_income,
            
            ly_interest_expenses = ly_form_interest_expenses,
            # ly_equity_in_losses_of_affiliates = ly_form_equity_in_losses_of_affiliates,
            # ly_other_non_operating_expenses = ly_calc_other_non_operating_expenses,
            # ly_non_operating_expenses = ly_form_non_operating_expenses,
            ly_ordinary_income_loss = ly_form_ordinary_income_loss,
            ly_other_nonoperating_income_or_loss = ly_calc_other_non_operating_income_and_expenses,

            ly_extraordinary_income_and_loss = ly_form_extraordinary_income_and_loss,
            ly_income_before_income_taxes = ly_form_income_before_income_taxes,
            ly_income_taxes = ly_form_income_taxes,
            ly_profit_loss_attributable_to_non_controling_interests = ly_form_profit_loss_attributable_to_non_controling_interests,
            ly_profit_loss_attributable_to_owners_of_parent = ly_form_profit_loss_attributable_to_owners_of_parent,

            ly_depreciation = ly_form_depreciation,
            ly_amortization_goodwill = ly_form_amortization_goodwill,
            ly_impairment = ly_form_impairment,

            ################  BS  ######################
            ly_cash_and_deposits = ly_form_cash_and_deposits,
            ly_securities = ly_form_securities,
            ly_notes_and_accounts_receivable_trade = ly_form_notes_and_accounts_receivable_trade,
            ly_inventories = ly_form_inventories,
            ly_deferred_tax_assets_ca = ly_form_deferred_tax_assets_ca,
            ly_other_current_assets = ly_calc_other_current_assets,
            ly_current_assets = ly_form_current_assets,

            ly_property_plant_and_equipment = ly_form_property_plant_and_equipment,
            
            ly_intangible_assets = ly_form_intangible_assets,

            ly_deferred_tax_assets_ioa = ly_form_deferred_tax_assets_ioa,
            ly_investments_and_other_assets = ly_form_investments_and_other_assets,
            
            ly_total_assets = ly_form_total_assets,

            ly_short_term_interest_bearing_bond = ly_form_short_term_interest_bearing_bond,
            ly_notes_and_accounts_payable_trade = ly_form_notes_and_accounts_payable_trade,
            ly_deferred_tax_liabilities_ca = ly_form_deferred_tax_liabilities_ca,
            ly_other_current_liabilities = ly_calc_other_current_liabilities,
            ly_current_liabilities = ly_form_current_liabilities,

            ly_long_term_interest_bearing_bond = ly_form_long_term_interest_bearing_bond,
            ly_deferred_tax_liabilities_ncl = ly_form_deferred_tax_liabilities_ncl,
            ly_other_noncurrent_liabilities = ly_calc_other_noncurrent_liabilities,
            ly_noncurrent_liabilities = ly_form_noncurrent_liabilities,

            ly_capital_stock = ly_form_capital_stock,
            ly_capital_surplus = ly_form_capital_surplus,
            ly_retained_earnings = ly_form_retained_earnings,
            ly_treasury_stock = ly_form_treasury_stock,
            ly_accumulated_other_comprehensive_income = ly_form_accumulated_other_comprehensive_income,
            ly_subscription_rights_to_shares = ly_form_subscription_rights_to_shares,
            ly_non_controlling_interests = ly_form_non_controlling_interests,
            ly_net_assets = ly_form_net_assets,

            ly_liabilities_and_net_assets = ly_form_liabilities_and_net_assets,
            ly_net_deferred_tax_assets = ly_calc_net_deferred_tax_assets,
            ly_fluctuations_in_deferred_tax_assets = ly_calc_fluctuations_in_deferred_tax_assets,

            ################  SS  ######################
            ly_net_assets_py = ly_form_net_assets_py,
            ly_issuance_of_new_shares = ly_form_issuance_of_new_shares,
            ly_dividends_ss = ly_form_dividends_ss,
            ly_purchase_of_treasury_stock = ly_form_purchase_of_treasury_stock,
            ly_disposal_of_treasury_stock = ly_form_disposal_of_treasury_stock,

            ################  CF  ######################
            # ly_cf_operating_activities = ly_form_cf_operating_activities,
            # ly_cf_investment_activities = ly_form_cf_investment_activities,
            # ly_cf_financing_activities = ly_form_cf_financing_activities,

            ################ OHTER ####################
            ly_total_number_of_issued_shares = ly_form_total_number_of_issued_shares,
            ly_number_of_shares_held_in_own_name = ly_form_number_of_shares_held_in_own_name,
            ly_dividend_paid_per_share = ly_form_dividend_paid_per_share,
            ly_effective_tax_rate = ly_form_effective_tax_rate,

            ############### TAX_ON_OPERATING_INCOME #####################
            ly_tax_on_interest_income_and_dividend = ly_calc_tax_on_interest_income_and_dividend,
            ly_tax_on_interest_expenses = ly_calc_tax_on_interest_expaneses,
            ly_tax_on_non_operating_income_and_expenses_others = ly_calc_tax_on_non_operating_income_and_expenses_others,
            ly_tax_on_extraordinary_income_and_losses = ly_calc_tax_on_extraordinary_income_and_losses,
            ly_tax_on_operating_income = ly_calc_tax_on_operating_income,

            ############### NOPAT_TOPDOWN #####################
            ly_nopat_topdown = ly_calc_nopat_topdown,

            ############### NOPAT_BOTTOMUP #####################
            ly_nopat_bottomup = ly_calc_nopat_bottomup,

            ############### INVESTED_CAPITAL #####################
            ly_net_working_capital = ly_calc_net_working_capital,
            ly_investment_capital = ly_calc_invested_capital,

            ############### FREE_CASH_FLOW #####################
            ly_operating_cf = ly_calc_operating_cf,
            ly_investment_cf = ly_calc_investment_cf,
            ly_free_cash_flow = ly_calc_free_cash_flow,
            ly_non_operating_cf = ly_calc_non_operating_cf,
            ly_financial_cf = ly_calc_financial_cf,
            ly_net_cf = ly_calc_net_cf,

            ############### ROE #####################
            ly_return_on_equity = ly_calc_return_on_equity,
            ly_return_on_asset = ly_calc_return_on_asset,
            ly_total_asset_turnover = ly_calc_total_asset_turnover,
            ly_financial_leverage = ly_calc_financial_leverage,

            ############### WACC #####################


            ############### ROIC #####################
            ly_return_on_invested_capital = ly_calc_return_on_invested_capital,
            ly_return_on_invested_capital_before_tax = ly_calc_return_on_invested_capital_before_tax,
            ly_tax_burden_rate = ly_calc_tax_burden_rate,
            ly_affiliated_company_contribution_rate = ly_calc_affiliated_company_contribution_rate,
            ly_operating_profit_margin = ly_calc_operating_profit_margin,
            ly_cost_rate = ly_calc_cost_rate,
            ly_sga_ratio = ly_calc_sga_ratio,
            ly_invested_capital_turnover = ly_calc_invested_capital_turnover,
            ly_net_working_capital_turnover_days = ly_calc_net_working_capital_turnover_days,
            ly_trade_receivavle_turnover_days = ly_calc_trade_receivable_turnover_days,
            ly_trade_payable_turnover_days = ly_calc_trade_payable_turnover_days,
            ly_inventries_turnover_days = ly_calc_inventries_turnover_days,
            ly_property_turnover_days = ly_calc_property_turnover_days,
            ly_intangible_turnover_days = ly_calc_intangible_turnover_days,
            ly_other_invested_capital_turnover_days = ly_calc_other_invested_capital_turnover_days,
            ly_cash_conversion_cicle = ly_calc_cash_conversion_cicle,



            ############### this_year : t ###############################
            net_sales = form_net_sales,
            cogs = form_cogs,
            # gross_profit = form_gross_profit,
            sga = form_sga,
            operating_income = form_operating_income,

            interest_and_dividends_income = form_interest_and_dividends_income,
            equity_in_earnings_or_losses_of_affiliates = form_equity_in_earnings_or_losses_of_affiliates,
            # other_non_operating_income = calc_other_non_operating_income,
            # non_operating_income = form_non_operating_income,

            interest_expenses = form_interest_expenses,
            # equity_in_losses_of_affiliates = form_equity_in_losses_of_affiliates,
            # non_operating_expenses = form_non_operating_expenses,
            # other_non_operating_expenses = calc_other_non_operating_expenses,
            ordinary_income_loss = form_ordinary_income_loss,
            other_nonoperating_income_or_loss = calc_other_non_operating_income_and_expenses,

            extraordinary_income_and_loss = form_extraordinary_income_and_loss,
            income_before_income_taxes = form_income_before_income_taxes,
            income_taxes = form_income_taxes,
            profit_loss_attributable_to_non_controling_interests = form_profit_loss_attributable_to_non_controling_interests,
            profit_loss_attributable_to_owners_of_parent = form_profit_loss_attributable_to_owners_of_parent,

            depreciation = form_depreciation,
            amortization_goodwill = form_amortization_goodwill,
            impairment = form_impairment,

            ################  BS  ######################
            cash_and_deposits = form_cash_and_deposits,
            securities = form_securities,
            notes_and_accounts_receivable_trade = form_notes_and_accounts_receivable_trade,
            inventories = form_inventories,
            deferred_tax_assets_ca = form_deferred_tax_assets_ca,
            other_current_assets = calc_other_current_assets,
            current_assets = form_current_assets,

            property_plant_and_equipment = form_property_plant_and_equipment,
            
            intangible_assets = form_intangible_assets,

            deferred_tax_assets_ioa = form_deferred_tax_assets_ioa,
            investments_and_other_assets = form_investments_and_other_assets,
            
            total_assets = form_total_assets,

            short_term_interest_bearing_bond = form_short_term_interest_bearing_bond,
            notes_and_accounts_payable_trade = form_notes_and_accounts_payable_trade,
            deferred_tax_liabilities_ca = form_deferred_tax_liabilities_ca,
            other_current_liabilities = calc_other_current_liabilities,
            current_liabilities = form_current_liabilities,

            long_term_interest_bearing_bond = form_long_term_interest_bearing_bond,
            deferred_tax_liabilities_ncl = form_deferred_tax_liabilities_ncl,
            other_noncurrent_liabilities = calc_other_noncurrent_liabilities,
            noncurrent_liabilities = form_noncurrent_liabilities,

            capital_stock = form_capital_stock,
            capital_surplus = form_capital_surplus,
            retained_earnings = form_retained_earnings,
            treasury_stock = form_treasury_stock,
            accumulated_other_comprehensive_income = form_accumulated_other_comprehensive_income,
            subscription_rights_to_shares = form_subscription_rights_to_shares,
            non_controlling_interests = form_non_controlling_interests,
            net_assets = form_net_assets,

            liabilities_and_net_assets = form_liabilities_and_net_assets,
            net_deferred_tax_assets = calc_net_deferred_tax_assets,
            fluctuations_in_deferred_tax_assets = calc_fluctuations_in_deferred_tax_assets,

            ################  SS  ######################
            net_assets_py = form_net_assets_py,
            issuance_of_new_shares = form_issuance_of_new_shares,
            dividends_ss = form_dividends_ss,
            purchase_of_treasury_stock = form_purchase_of_treasury_stock,
            disposal_of_treasury_stock = form_disposal_of_treasury_stock,

            ################  CF  ######################
            # cf_operating_activities = form_cf_operating_activities,
            # cf_investment_activities = form_cf_investment_activities,
            # cf_financing_activities = form_cf_financing_activities,

            ################ OHTER ####################
            total_number_of_issued_shares = form_total_number_of_issued_shares,
            number_of_shares_held_in_own_name = form_number_of_shares_held_in_own_name,
            dividend_paid_per_share = form_dividend_paid_per_share,
            effective_tax_rate = form_effective_tax_rate,

            ############### TAX_ON_OPERATING_INCOME #####################
            tax_on_interest_income_and_dividend = calc_tax_on_interest_income_and_dividend,
            tax_on_interest_expenses = calc_tax_on_interest_expaneses,
            tax_on_non_operating_income_and_expenses_others = calc_tax_on_non_operating_income_and_expenses_others,
            tax_on_extraordinary_income_and_losses = calc_tax_on_extraordinary_income_and_losses,
            tax_on_operating_income = calc_tax_on_operating_income,

            ############### NOPAT_TOPDOWN #####################
            nopat_topdown = calc_nopat_topdown,

            ############### NOPAT_BOTTOMUP #####################
            nopat_bottomup = calc_nopat_bottomup,

            ############### INVESTMENT_CAPITAL #####################
            net_working_capital = calc_net_working_capital,
            investment_capital = calc_invested_capital,

            ############### FREE_CASH_FLOW #####################
            operating_cf = calc_operating_cf,
            investment_cf = calc_investment_cf,
            free_cash_flow = calc_free_cash_flow,
            non_operating_cf = calc_non_operating_cf,
            financial_cf = calc_financial_cf,
            net_cf = calc_net_cf,

            ############### ROE #####################
            return_on_equity = calc_return_on_equity,
            return_on_asset = calc_return_on_asset,
            total_asset_turnover = calc_total_asset_turnover,
            financial_leverage = calc_financial_leverage,

            ############### WACC #####################
            borrowing_interest_rate = form_borrowing_interest_rate,
            risk_free_rate = RISK_FREE_RATE,
            cost_of_shareholders_equity = COST_OF_SHAREHOLDERS_EQUITY,
            wacc = calc_wacc,

            ############### ROIC #####################
            return_on_invested_capital = calc_return_on_invested_capital,
            return_on_invested_capital_before_tax = calc_return_on_invested_capital_before_tax,
            tax_burden_rate = calc_tax_burden_rate,
            affiliated_company_contribution_rate = calc_affiliated_company_contribution_rate,
            operating_profit_margin = calc_operating_profit_margin,
            cost_rate = calc_cost_rate,
            sga_ratio = calc_sga_ratio,
            invested_capital_turnover = calc_invested_capital_turnover,
            net_working_capital_turnover_days = calc_net_working_capital_turnover_days,
            trade_receivavle_turnover_days = calc_trade_receivable_turnover_days,
            trade_payable_turnover_days = calc_trade_payable_turnover_days,
            inventries_turnover_days = calc_inventries_turnover_days,
            property_turnover_days = calc_property_turnover_days,
            intangible_turnover_days = calc_intangible_turnover_days,
            other_invested_capital_turnover_days = calc_other_invested_capital_turnover_days,
            cash_conversion_cicle = calc_cash_conversion_cicle,

            ############### VALUATION #####################
            valuation_01 = calc_valuation[0],
            wacc_adj_01 = wacc_adj[0],
            grows_rate_01 = grows_rate[0],
            valuation_02 = calc_valuation[1],
            wacc_adj_02 = wacc_adj[1],
            grows_rate_02 = grows_rate[1],
            valuation_03 = calc_valuation[2],
            wacc_adj_03 = wacc_adj[2],
            grows_rate_03 = grows_rate[2],
            valuation_04 = calc_valuation[3],
            wacc_adj_04 = wacc_adj[3],
            grows_rate_04 = grows_rate[3],
            valuation_05 = calc_valuation[4],
            wacc_adj_05 = wacc_adj[4],
            grows_rate_05 = grows_rate[4],
            valuation_06 = calc_valuation[5],
            wacc_adj_06 = wacc_adj[5],
            grows_rate_06 = grows_rate[5],
            valuation_07 = calc_valuation[6],
            wacc_adj_07 = wacc_adj[6],
            grows_rate_07 = grows_rate[6],
            valuation_08 = calc_valuation[7],
            wacc_adj_08 = wacc_adj[7],
            grows_rate_08 = grows_rate[7],
            valuation_09 = calc_valuation[8],
            wacc_adj_09 = wacc_adj[8],
            grows_rate_09 = grows_rate[8],
            valuation_10 = calc_valuation[9],
            wacc_adj_10 = wacc_adj[9],
            grows_rate_10 = grows_rate[9],
            valuation_11 = calc_valuation[10],
            wacc_adj_11 = wacc_adj[10],
            grows_rate_11 = grows_rate[10],
            valuation_12 = calc_valuation[11],
            wacc_adj_12 = wacc_adj[11],
            grows_rate_12 = grows_rate[11],
            valuation_13 = calc_valuation[12],
            wacc_adj_13 = wacc_adj[12],
            grows_rate_13 = grows_rate[12],
            valuation_14 = calc_valuation[13],
            wacc_adj_14 = wacc_adj[13],
            grows_rate_14 = grows_rate[13],
            valuation_15 = calc_valuation[14],
            wacc_adj_15 = wacc_adj[14],
            grows_rate_15 = grows_rate[14],
            valuation_16 = calc_valuation[15],
            wacc_adj_16 = wacc_adj[15],
            grows_rate_16 = grows_rate[15],
            valuation_17 = calc_valuation[16],
            wacc_adj_17 = wacc_adj[16],
            grows_rate_17 = grows_rate[16],
            valuation_18 = calc_valuation[17],
            wacc_adj_18 = wacc_adj[17],
            grows_rate_18 = grows_rate[17],
            valuation_19 = calc_valuation[18],
            wacc_adj_19 = wacc_adj[18],
            grows_rate_19 = grows_rate[18],
            valuation_20 = calc_valuation[19],
            wacc_adj_20 = wacc_adj[19],
            grows_rate_20 = grows_rate[19],
            valuation_21 = calc_valuation[20],
            wacc_adj_21 = wacc_adj[20],
            grows_rate_21 = grows_rate[20],
            valuation_22 = calc_valuation[21],
            wacc_adj_22 = wacc_adj[21],
            grows_rate_22 = grows_rate[21],
            valuation_23 = calc_valuation[22],
            wacc_adj_23 = wacc_adj[22],
            grows_rate_23 = grows_rate[22],
            valuation_24 = calc_valuation[23],
            wacc_adj_24 = wacc_adj[23],
            grows_rate_24 = grows_rate[23],
            valuation_25 = calc_valuation[24],
            wacc_adj_25 = wacc_adj[24],
            grows_rate_25 = grows_rate[24],
            max_valuation = calc_max_valuation,
            min_valuation = calc_min_valuation,

        )

        db.session.merge(financial_data)
        db.session.commit()
        return redirect('/result')

@app.route('/result')
@login_required
def show_result():
    # cookie_session = request.cookies.get('session')
    # _, data, timestamp, secret = cookie_session.split('.')
    # uid = data

    remember = request.cookies.get('remember_token')
    uid = remember

    results = FinancialData.query.filter(FinancialData.uid == uid)
    return render_template('valuation/result.html', results=results)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        company_name = request.form.get('company_name')
        password = request.form.get('password')
        # Userのインスタンスを作成
        user = Users(username=username, company_name=company_name, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('valuation/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルから username に一致するユーザを取得
        user = Users.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect('/')
        else:
            return render_template('valuation/login.html')
    else:
        return render_template('valuation/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/edit', methods=['GET'])
@login_required
def edit():
    # cookie_session = request.cookies.get('session')
    # _, data, timestamp, secret = cookie_session.split('.')
    remember = request.cookies.get('remember_token')
    # uid = data
    uid = remember

    financial_data = FinancialData.query.filter(FinancialData.uid == uid)
    return render_template('valuation/edit.html', fd=financial_data)

@app.route('/edit', methods=['POST'])
@login_required
def financial_data_update():
    cookie_session = request.cookies.get('session')
    _, data, timestamp, secret = cookie_session.split('.')
    uid = data

    ############### year ####################
    form_year_before_last = str(request.form.get('year_before_last'))
    form_last_year = str(request.form.get('last_year'))
    form_this_year = str(request.form.get('this_year'))

    ############### year_before_last : t - 2 ####################
    ybl_form_net_sales = int(request.form.get('ybl_net_sales'))
    ybl_form_cogs = int(request.form.get('ybl_cogs'))
    # form_gross_profit = request.form.get('gross_profit')
    ybl_form_sga = int(request.form.get('ybl_sga'))
    ybl_form_operating_income = int(request.form.get('ybl_operating_income'))

    ybl_form_interest_and_dividends_income = int(request.form.get('ybl_interest_and_dividends_income'))
    ybl_form_equity_in_earnings_or_losses_of_affiliates = int(request.form.get('ybl_equity_in_earnings_or_losses_of_affiliates'))
    # ybl_form_non_operating_income = int(request.form.get('ybl_non_operating_income'))

    ybl_form_interest_expenses = int(request.form.get('ybl_interest_expenses'))
    # ybl_form_equity_in_losses_of_affiliates = int(request.form.get('ybl_equity_in_losses_of_affiliates'))
    # ybl_form_non_operating_expenses = int(request.form.get('ybl_non_operating_expenses'))
    # ybl_calc_other_non_operating_expenses = ybl_form_non_operating_expenses - (ybl_form_interest_expenses + ybl_form_equity_in_losses_of_affiliates)
    ybl_form_ordinary_income_loss = int(request.form.get('ybl_ordinary_income_loss'))
    ybl_calc_other_non_operating_income_or_expense = ybl_form_ordinary_income_loss - (ybl_form_operating_income + ybl_form_interest_and_dividends_income + ybl_form_equity_in_earnings_or_losses_of_affiliates - ybl_form_interest_expenses)

    ybl_form_extraordinary_income_and_loss = int(request.form.get('ybl_extraordinary_income_and_loss'))
    ybl_form_income_before_income_taxes = int(request.form.get('ybl_income_before_income_taxes'))
    ybl_form_income_taxes = int(request.form.get('ybl_income_taxes'))
    ybl_form_profit_loss_attributable_to_non_controling_interests = int(request.form.get('ybl_profit_loss_attributable_to_non_controling_interests'))
    ybl_form_profit_loss_attributable_to_owners_of_parent = int(request.form.get('ybl_profit_loss_attributable_to_owners_of_parent'))

    ybl_form_depreciation = int(request.form.get('ybl_depreciation'))
    ybl_form_amortization_goodwill = int(request.form.get('ybl_amortization_goodwill'))
    ybl_form_impairment = int(request.form.get('ybl_impairment'))


    ################  BS  ######################
    ybl_form_cash_and_deposits = int(request.form.get('ybl_cash_and_deposits'))
    ybl_form_securities = int(request.form.get('ybl_securities'))
    ybl_form_notes_and_accounts_receivable_trade = int(request.form.get('ybl_notes_and_accounts_receivable_trade'))
    ybl_form_inventories = int(request.form.get('ybl_inventories'))
    ybl_form_deferred_tax_assets_ca = int(request.form.get('ybl_deferred_tax_assets_ca'))
    ybl_form_current_assets = int(request.form.get('ybl_current_assets'))
    ybl_calc_other_current_assets = ybl_form_current_assets - (ybl_form_cash_and_deposits + ybl_form_securities + ybl_form_notes_and_accounts_receivable_trade + ybl_form_inventories + ybl_form_deferred_tax_assets_ca)

    ybl_form_property_plant_and_equipment = int(request.form.get('ybl_property_plant_and_equipment'))
    
    ybl_form_intangible_assets = int(request.form.get('ybl_intangible_assets'))

    ybl_form_deferred_tax_assets_ioa = int(request.form.get('ybl_deferred_tax_assets_ioa'))
    ybl_form_investments_and_other_assets = int(request.form.get('ybl_investments_and_other_assets'))
    
    ybl_form_total_assets = int(request.form.get('ybl_total_assets'))

    ybl_form_short_term_interest_bearing_bond = int(request.form.get('ybl_short_term_interest_bearing_bond'))
    ybl_form_notes_and_accounts_payable_trade = int(request.form.get('ybl_notes_and_accounts_payable_trade'))
    ybl_form_deferred_tax_liabilities_ca = int(request.form.get('ybl_deferred_tax_liabilities_ca'))
    ybl_form_current_liabilities = int(request.form.get('ybl_current_liabilities'))
    ybl_calc_other_current_liabilities = ybl_form_current_liabilities - (ybl_form_short_term_interest_bearing_bond + ybl_form_notes_and_accounts_payable_trade + ybl_form_deferred_tax_liabilities_ca)

    ybl_form_long_term_interest_bearing_bond = int(request.form.get('ybl_long_term_interest_bearing_bond'))
    ybl_form_deferred_tax_liabilities_ncl = int(request.form.get('ybl_deferred_tax_liabilities_ncl'))
    ybl_form_noncurrent_liabilities = int(request.form.get('ybl_noncurrent_liabilities'))
    ybl_calc_other_noncurrent_liabilities = ybl_form_noncurrent_liabilities - (ybl_form_long_term_interest_bearing_bond + ybl_form_deferred_tax_liabilities_ncl)

    ybl_form_capital_stock = int(request.form.get('ybl_capital_stock'))
    ybl_form_capital_surplus = int(request.form.get('ybl_capital_surplus'))
    ybl_form_retained_earnings = int(request.form.get('ybl_retained_earnings'))
    ybl_form_treasury_stock = int(request.form.get('ybl_treasury_stock'))
    ybl_form_accumulated_other_comprehensive_income = int(request.form.get('ybl_accumulated_other_comprehensive_income'))
    ybl_form_subscription_rights_to_shares = int(request.form.get('ybl_subscription_rights_to_shares'))
    ybl_form_non_controlling_interests = int(request.form.get('ybl_non_controlling_interests'))
    ybl_form_net_assets = int(request.form.get('ybl_net_assets'))

    ybl_form_liabilities_and_net_assets = int(request.form.get('ybl_liabilities_and_net_assets'))
    ybl_calc_net_deferred_tax_assets = (ybl_form_deferred_tax_assets_ca + ybl_form_deferred_tax_assets_ioa) - (ybl_form_deferred_tax_liabilities_ca + ybl_form_deferred_tax_liabilities_ncl)

    ################  SS  ######################
    ybl_form_net_assets_py = int(request.form.get('ybl_net_assets_py'))
    ybl_form_issuance_of_new_shares = int(request.form.get('ybl_issuance_of_new_shares'))
    ybl_form_dividends_ss = int(request.form.get('ybl_dividends_ss'))
    ybl_form_purchase_of_treasury_stock = int(request.form.get('ybl_purchase_of_treasury_stock'))
    ybl_form_disposal_of_treasury_stock = int(request.form.get('ybl_disposal_of_treasury_stock'))

    ################  CF  ######################
    # ybl_form_cf_operating_activities = request.form.get('ybl_cf_operating_activities')
    # ybl_form_cf_investment_activities = request.form.get('ybl_cf_investment_activities')
    # ybl_form_cf_financing_activities = request.form.get('ybl_cf_financing_activities')

    ################ OHTER ####################
    ybl_form_total_number_of_issued_shares = int(request.form.get('ybl_total_number_of_issued_shares'))
    ybl_form_number_of_shares_held_in_own_name = int(request.form.get('ybl_number_of_shares_held_in_own_name'))
    ybl_form_dividend_paid_per_share = int(request.form.get('ybl_dividend_paid_per_share'))
    ybl_form_effective_tax_rate = float(request.form.get('ybl_effective_tax_rate')) / 100

    ############### INVESTED_CAPITAL #####################
    hhh = ybl_form_notes_and_accounts_receivable_trade
    iii = ybl_form_inventories
    jjj = ybl_calc_other_current_assets
    kkk = ybl_form_notes_and_accounts_payable_trade
    lll = ybl_calc_other_current_liabilities
    ybl_calc_net_working_capital = hhh + iii + jjj - kkk - lll
    mmm = ybl_form_property_plant_and_equipment
    nnn = ybl_form_intangible_assets
    ooo = ybl_calc_net_deferred_tax_assets
    ppp = ybl_form_investments_and_other_assets - ybl_form_deferred_tax_assets_ioa
    qqq = ybl_calc_other_noncurrent_liabilities
    rrr = ybl_form_cash_and_deposits
    sss = ybl_form_securities
    ybl_calc_invested_capital = ybl_calc_net_working_capital + mmm + nnn + ooo + ppp - qqq + rrr + sss



    ############### last_year : t - 1 ###########################
    ly_form_net_sales = int(request.form.get('ly_net_sales'))
    ly_form_cogs = int(request.form.get('ly_cogs'))
    # form_gross_profit = request.form.get('gross_profit')
    ly_form_sga = int(request.form.get('ly_sga'))
    ly_form_operating_income = int(request.form.get('ly_operating_income'))
    
    ly_form_interest_and_dividends_income = int(request.form.get('ly_interest_and_dividends_income'))
    ly_form_equity_in_earnings_or_losses_of_affiliates = int(request.form.get('ly_equity_in_earnings_or_losses_of_affiliates'))
    # ly_form_non_operating_income = int(request.form.get('ly_non_operating_income'))
    # ly_calc_other_non_operating_income = ly_form_non_operating_income - (ly_form_interest_and_dividends_income + ly_form_equity_in_earnings_of_affiliates)
    
    ly_form_interest_expenses = int(request.form.get('ly_interest_expenses'))
    # ly_form_equity_in_losses_of_affiliates = int(request.form.get('ly_equity_in_losses_of_affiliates'))
    # ly_form_non_operating_expenses = int(request.form.get('ly_non_operating_expenses'))
    ly_form_ordinary_income_loss = int(request.form.get('ly_ordinary_income_loss'))
    ly_calc_other_non_operating_income_and_expenses = ly_form_ordinary_income_loss - (ly_form_operating_income + ly_form_interest_and_dividends_income + ly_form_equity_in_earnings_or_losses_of_affiliates - ly_form_interest_expenses)

    ly_form_extraordinary_income_and_loss = int(request.form.get('ly_extraordinary_income_and_loss'))
    ly_form_income_before_income_taxes = int(request.form.get('ly_income_before_income_taxes'))
    ly_form_income_taxes = int(request.form.get('ly_income_taxes'))
    ly_form_profit_loss_attributable_to_non_controling_interests = int(request.form.get('ly_profit_loss_attributable_to_non_controling_interests'))
    ly_form_profit_loss_attributable_to_owners_of_parent = int(request.form.get('ly_profit_loss_attributable_to_owners_of_parent'))

    ly_form_depreciation = int(request.form.get('ly_depreciation'))
    ly_form_amortization_goodwill = int(request.form.get('ly_amortization_goodwill'))
    ly_form_impairment = int(request.form.get('ly_impairment'))


    ################  BS  ######################
    ly_form_cash_and_deposits = int(request.form.get('ly_cash_and_deposits'))
    ly_form_securities = int(request.form.get('ly_securities'))
    ly_form_notes_and_accounts_receivable_trade = int(request.form.get('ly_notes_and_accounts_receivable_trade'))
    ly_form_inventories = int(request.form.get('ly_inventories'))
    ly_form_deferred_tax_assets_ca = int(request.form.get('ly_deferred_tax_assets_ca'))
    ly_form_current_assets = int(request.form.get('ly_current_assets'))
    ly_calc_other_current_assets = ly_form_current_assets - (ly_form_cash_and_deposits + ly_form_securities + ly_form_notes_and_accounts_receivable_trade + ly_form_inventories + ly_form_deferred_tax_assets_ca)

    ly_form_property_plant_and_equipment = int(request.form.get('ly_property_plant_and_equipment'))
    
    ly_form_intangible_assets = int(request.form.get('ly_intangible_assets'))

    ly_form_deferred_tax_assets_ioa = int(request.form.get('ly_deferred_tax_assets_ioa'))
    ly_form_investments_and_other_assets = int(request.form.get('ly_investments_and_other_assets'))
    
    ly_form_total_assets = int(request.form.get('ly_total_assets'))

    ly_form_short_term_interest_bearing_bond = int(request.form.get('ly_short_term_interest_bearing_bond'))
    ly_form_notes_and_accounts_payable_trade = int(request.form.get('ly_notes_and_accounts_payable_trade'))
    ly_form_deferred_tax_liabilities_ca = int(request.form.get('ly_deferred_tax_liabilities_ca'))
    ly_form_current_liabilities = int(request.form.get('ly_current_liabilities'))
    ly_calc_other_current_liabilities = ly_form_current_liabilities - (ly_form_short_term_interest_bearing_bond + ly_form_notes_and_accounts_payable_trade + ly_form_deferred_tax_liabilities_ca)

    ly_form_long_term_interest_bearing_bond = int(request.form.get('ly_long_term_interest_bearing_bond'))
    ly_form_deferred_tax_liabilities_ncl = int(request.form.get('ly_deferred_tax_liabilities_ncl'))
    ly_form_noncurrent_liabilities = int(request.form.get('ly_noncurrent_liabilities'))
    ly_calc_other_noncurrent_liabilities = ly_form_noncurrent_liabilities - (ly_form_long_term_interest_bearing_bond + ly_form_deferred_tax_liabilities_ncl)

    ly_form_capital_stock = int(request.form.get('ly_capital_stock'))
    ly_form_capital_surplus = int(request.form.get('ly_capital_surplus'))
    ly_form_retained_earnings = int(request.form.get('ly_retained_earnings'))
    ly_form_treasury_stock = int(request.form.get('ly_treasury_stock'))
    ly_form_accumulated_other_comprehensive_income = int(request.form.get('ly_accumulated_other_comprehensive_income'))
    ly_form_subscription_rights_to_shares = int(request.form.get('ly_subscription_rights_to_shares'))
    ly_form_non_controlling_interests = int(request.form.get('ly_non_controlling_interests'))
    ly_form_net_assets = int(request.form.get('ly_net_assets'))

    ly_form_liabilities_and_net_assets = int(request.form.get('ly_liabilities_and_net_assets'))
    ly_calc_net_deferred_tax_assets = (ly_form_deferred_tax_assets_ca + ly_form_deferred_tax_assets_ioa) - (ly_form_deferred_tax_liabilities_ca + ly_form_deferred_tax_liabilities_ncl)
    ly_calc_fluctuations_in_deferred_tax_assets = ly_calc_net_deferred_tax_assets - ybl_calc_net_deferred_tax_assets


    ################  SS  ######################
    ly_form_net_assets_py = int(request.form.get('ly_net_assets_py'))
    ly_form_issuance_of_new_shares = int(request.form.get('ly_issuance_of_new_shares'))
    ly_form_dividends_ss = int(request.form.get('ly_dividends_ss'))
    ly_form_purchase_of_treasury_stock = int(request.form.get('ly_purchase_of_treasury_stock'))
    ly_form_disposal_of_treasury_stock = int(request.form.get('ly_disposal_of_treasury_stock'))
    ly_calc_other_ss = ly_form_net_assets - (ly_form_net_assets_py + ly_form_profit_loss_attributable_to_owners_of_parent + ly_form_issuance_of_new_shares - ly_form_dividends_ss -ly_form_purchase_of_treasury_stock + ly_form_disposal_of_treasury_stock)

    ################  CF  ######################
    # ly_form_cf_operating_activities = request.form.get('ly_cf_operating_activities')
    # ly_form_cf_investment_activities = request.form.get('ly_cf_investment_activities')
    # ly_form_cf_financing_activities = request.form.get('ly_cf_financing_activities')

    ################ OHTER ####################
    ly_form_total_number_of_issued_shares = int(request.form.get('ly_total_number_of_issued_shares'))
    ly_form_number_of_shares_held_in_own_name = int(request.form.get('ly_number_of_shares_held_in_own_name'))
    ly_form_dividend_paid_per_share = int(request.form.get('ly_dividend_paid_per_share'))
    ly_form_effective_tax_rate = float(request.form.get('ly_effective_tax_rate')) / 100

    ############### TAX_ON_OPERATING_INCOME #####################
    # a
    ly_calc_tax_on_interest_income_and_dividend = ly_form_interest_and_dividends_income * ly_form_effective_tax_rate

    # b
    ly_calc_tax_on_interest_expaneses = ly_form_interest_expenses * ly_form_effective_tax_rate
            
    # c = (その他営業外収益 - その他営業外費用) * effective tax rate
    ly_calc_tax_on_non_operating_income_and_expenses_others = (ly_calc_other_non_operating_income_and_expenses) * ly_form_effective_tax_rate
    
    # d
    ly_calc_tax_on_extraordinary_income_and_losses = ly_form_extraordinary_income_and_loss * ly_form_effective_tax_rate
    
    # e = income taxes - a + b - c - d
    ly_calc_tax_on_operating_income = ly_form_income_taxes - ly_calc_tax_on_interest_income_and_dividend + ly_calc_tax_on_interest_expaneses - ly_calc_tax_on_non_operating_income_and_expenses_others - ly_calc_tax_on_extraordinary_income_and_losses

    ############### NOPAT_TOPDOWN #####################
    # 営業利益 - 営業利益にかかる税金 + DTA（純額）の減少（増加はマイナス） + 持分法投資利益（損失はマイナス）
    ly_calc_nopat_topdown = ly_form_operating_income - ly_calc_tax_on_operating_income - ly_calc_fluctuations_in_deferred_tax_assets + ly_form_equity_in_earnings_or_losses_of_affiliates


    ############### NOPAT_BOTTOMUP #####################
    # 親会社株主当期純利益 + 非支配株主当期純利益 + DTA（純額)の減少（増加はマイナス） + (特別損益 * (1-実効税率)) - (（受取利息+受取配当金) * (1-実効税率)) + (支払利息 * (1-実効税率)) + ((その他営業外損失 - その他営業外利益) * (1-実効税率))
    a = ly_form_profit_loss_attributable_to_owners_of_parent
    b = ly_form_profit_loss_attributable_to_non_controling_interests
    c = ly_calc_fluctuations_in_deferred_tax_assets
    d = ly_form_extraordinary_income_and_loss * (1 - ly_form_effective_tax_rate)
    e = ly_form_interest_and_dividends_income * (1 - ly_form_effective_tax_rate)
    f = ly_form_interest_expenses * (1 - ly_form_effective_tax_rate)
    g = ly_calc_other_non_operating_income_and_expenses * (1 - ly_form_effective_tax_rate)
    ly_calc_nopat_bottomup = a + b - c - d - e + f - g

    ############### INVESTED_CAPITAL #####################
    h = ly_form_notes_and_accounts_receivable_trade
    i = ly_form_inventories
    j = ly_calc_other_current_assets
    k = ly_form_notes_and_accounts_payable_trade
    l = ly_calc_other_current_liabilities
    ly_calc_net_working_capital = h + i + j - k - l
    m = ly_form_property_plant_and_equipment
    n = ly_form_intangible_assets
    o = ly_calc_net_deferred_tax_assets
    p = ly_form_investments_and_other_assets - ly_form_deferred_tax_assets_ioa
    q = ly_calc_other_noncurrent_liabilities
    r = ly_form_cash_and_deposits
    s = ly_form_securities
    ly_calc_invested_capital = ly_calc_net_working_capital + m + n + o + p - q + r + s

    ############### FREE_CASH_FLOW #####################
    ly_calc_operating_cf = ly_calc_nopat_topdown + ly_form_depreciation + ly_form_amortization_goodwill + (ybl_calc_net_working_capital - ly_calc_net_working_capital)
    ly_calc_investment_cf = -1 * ((ly_form_property_plant_and_equipment + ly_form_intangible_assets) - (ybl_form_property_plant_and_equipment + ybl_form_intangible_assets) + (ly_form_depreciation + ly_form_impairment + ly_form_amortization_goodwill))
    ly_calc_free_cash_flow = ly_calc_operating_cf + ly_calc_investment_cf
    ly_calc_non_operating_cf = -1 * (b - c - d - e + f - g) - c - (((ly_form_investments_and_other_assets - ly_form_deferred_tax_assets_ioa) - ly_calc_other_noncurrent_liabilities) - ((ybl_form_investments_and_other_assets - ybl_form_deferred_tax_assets_ioa) - ybl_calc_other_noncurrent_liabilities))
    ly_calc_financial_cf = ((ly_form_short_term_interest_bearing_bond + ly_form_long_term_interest_bearing_bond) - (ybl_form_short_term_interest_bearing_bond + ybl_form_long_term_interest_bearing_bond)) - ly_form_dividends_ss + ly_form_issuance_of_new_shares - ly_form_purchase_of_treasury_stock + ly_form_disposal_of_treasury_stock + ly_calc_other_ss
    ly_calc_net_cf = ly_calc_free_cash_flow + ly_calc_non_operating_cf + ly_calc_financial_cf

    ############### ROE #####################
    ly_calc_shareholders_equity = (ly_form_capital_stock + ly_form_capital_surplus + ly_form_retained_earnings + ly_form_treasury_stock + ly_form_accumulated_other_comprehensive_income)
    ly_calc_shareholders_equity_py = (ybl_form_capital_stock + ybl_form_capital_surplus + ybl_form_retained_earnings + ybl_form_treasury_stock + ybl_form_accumulated_other_comprehensive_income)
    ly_calc_average_shareholders_equity = (ly_calc_shareholders_equity + ly_calc_shareholders_equity_py) * 1/2
    ly_calc_return_on_equity = ly_form_profit_loss_attributable_to_owners_of_parent / ly_calc_average_shareholders_equity
    ly_calc_return_on_asset = ly_form_profit_loss_attributable_to_owners_of_parent / ly_form_net_sales
    ly_calc_total_asset_turnover = ly_form_net_sales / ((ly_form_total_assets + ybl_form_total_assets) * 1/2 )
    ly_calc_financial_leverage = ((ly_form_total_assets + ybl_form_total_assets) * 1/2) / ly_calc_average_shareholders_equity

    ############### WACC #####################


    ############### ROIC #####################
    ly_calc_return_on_invested_capital = ly_calc_nopat_topdown / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
    ly_calc_return_on_invested_capital_before_tax = ly_form_operating_income / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
    ly_calc_tax_burden_rate = ly_calc_tax_on_operating_income / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
    ly_calc_affiliated_company_contribution_rate = ly_form_equity_in_earnings_or_losses_of_affiliates / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
    ly_calc_operating_profit_margin = ly_form_operating_income / ly_form_net_sales
    ly_calc_cost_rate = ly_form_cogs / ly_form_net_sales
    ly_calc_sga_ratio = ly_form_sga / ly_form_net_sales
    ly_calc_invested_capital_turnover = ly_form_net_sales / ((ly_calc_invested_capital + ybl_calc_invested_capital) * 1/2)
    ly_calc_net_working_capital_turnover_days = ly_calc_net_working_capital / (ly_form_net_sales / 365)
    ly_calc_trade_receivable_turnover_days = ly_form_notes_and_accounts_receivable_trade / (ly_form_net_sales / 365)
    ly_calc_trade_payable_turnover_days = ly_form_notes_and_accounts_payable_trade / (ly_form_net_sales / 365)
    ly_calc_inventries_turnover_days = ly_form_inventories / (ly_form_net_sales / 365)
    ly_calc_property_turnover_days = ly_form_property_plant_and_equipment / (ly_form_net_sales / 365)
    ly_calc_intangible_turnover_days = ly_form_intangible_assets / (ly_form_net_sales / 365)
    ly_calc_other_invested_capital_turnover_days = (ly_calc_invested_capital - ly_calc_net_working_capital - ly_form_inventories - ly_form_property_plant_and_equipment - ly_form_intangible_assets) / (ly_form_net_sales / 365)
    ly_calc_cash_conversion_cicle = ly_calc_inventries_turnover_days + ly_calc_trade_receivable_turnover_days - ly_calc_trade_payable_turnover_days


    ############### this_year : t ###############################
    form_net_sales = int(request.form.get('net_sales'))
    form_cogs = int(request.form.get('cogs'))
    # form_gross_profit = request.form.get('gross_profit')
    form_sga = int(request.form.get('sga'))
    form_operating_income = int(request.form.get('operating_income'))
    
    form_interest_and_dividends_income = int(request.form.get('interest_and_dividends_income'))
    form_equity_in_earnings_or_losses_of_affiliates = int(request.form.get('equity_in_earnings_or_losses_of_affiliates'))
    # form_non_operating_income = int(request.form.get('non_operating_income'))
    # calc_other_non_operating_income = form_non_operating_income - (form_interest_and_dividends_income + form_equity_in_earnings_of_affiliates)

    form_interest_expenses = int(request.form.get('interest_expenses'))
    # form_equity_in_losses_of_affiliates = int(request.form.get('equity_in_losses_of_affiliates'))
    # form_non_operating_expenses = int(request.form.get('non_operating_expenses'))
    form_ordinary_income_loss = int(request.form.get('ordinary_income_loss'))
    calc_other_non_operating_income_and_expenses = form_ordinary_income_loss - (form_operating_income + form_interest_and_dividends_income +form_equity_in_earnings_or_losses_of_affiliates - form_interest_expenses)

    form_extraordinary_income_and_loss = int(request.form.get('extraordinary_income_and_loss'))
    form_income_before_income_taxes = int(request.form.get('income_before_income_taxes'))
    form_income_taxes = int(request.form.get('income_taxes'))
    form_profit_loss_attributable_to_non_controling_interests = int(request.form.get('profit_loss_attributable_to_non_controling_interests'))
    form_profit_loss_attributable_to_owners_of_parent = int(request.form.get('profit_loss_attributable_to_owners_of_parent'))

    form_depreciation = int(request.form.get('depreciation'))
    form_amortization_goodwill = int(request.form.get('amortization_goodwill'))
    form_impairment = int(request.form.get('impairment'))


    ################  BS  ######################
    form_cash_and_deposits = int(request.form.get('cash_and_deposits'))
    form_securities = int(request.form.get('securities'))
    form_notes_and_accounts_receivable_trade = int(request.form.get('notes_and_accounts_receivable_trade'))
    form_inventories = int(request.form.get('inventories'))
    form_deferred_tax_assets_ca = int(request.form.get('deferred_tax_assets_ca'))
    form_current_assets = int(request.form.get('current_assets'))
    calc_other_current_assets = form_current_assets - (form_cash_and_deposits + form_securities + form_notes_and_accounts_receivable_trade + form_inventories + form_deferred_tax_assets_ca)

    form_property_plant_and_equipment = int(request.form.get('property_plant_and_equipment'))
    
    form_intangible_assets = int(request.form.get('intangible_assets'))

    form_deferred_tax_assets_ioa = int(request.form.get('deferred_tax_assets_ioa'))
    form_investments_and_other_assets = int(request.form.get('investments_and_other_assets'))
    
    form_total_assets = int(request.form.get('total_assets'))

    form_short_term_interest_bearing_bond = int(request.form.get('short_term_interest_bearing_bond'))
    form_notes_and_accounts_payable_trade = int(request.form.get('notes_and_accounts_payable_trade'))
    form_deferred_tax_liabilities_ca = int(request.form.get('deferred_tax_liabilities_ca'))
    form_current_liabilities = int(request.form.get('current_liabilities'))
    calc_other_current_liabilities = form_current_liabilities - (form_short_term_interest_bearing_bond + form_notes_and_accounts_payable_trade + form_deferred_tax_liabilities_ca)

    form_long_term_interest_bearing_bond = int(request.form.get('long_term_interest_bearing_bond'))
    form_deferred_tax_liabilities_ncl = int(request.form.get('deferred_tax_liabilities_ncl'))
    form_noncurrent_liabilities = int(request.form.get('noncurrent_liabilities'))
    calc_other_noncurrent_liabilities = form_noncurrent_liabilities - (form_long_term_interest_bearing_bond + form_deferred_tax_liabilities_ncl)

    form_capital_stock = int(request.form.get('capital_stock'))
    form_capital_surplus = int(request.form.get('capital_surplus'))
    form_retained_earnings = int(request.form.get('retained_earnings'))
    form_treasury_stock = int(request.form.get('treasury_stock'))
    form_accumulated_other_comprehensive_income = int(request.form.get('accumulated_other_comprehensive_income'))
    form_subscription_rights_to_shares = int(request.form.get('subscription_rights_to_shares'))
    form_non_controlling_interests = int(request.form.get('non_controlling_interests'))
    form_net_assets = int(request.form.get('net_assets'))

    form_liabilities_and_net_assets = int(request.form.get('liabilities_and_net_assets'))
    calc_net_deferred_tax_assets = (form_deferred_tax_assets_ca + form_deferred_tax_assets_ioa) - (form_deferred_tax_liabilities_ca + form_deferred_tax_liabilities_ncl)
    calc_fluctuations_in_deferred_tax_assets = calc_net_deferred_tax_assets - ly_calc_net_deferred_tax_assets


    ################  SS  ######################
    form_net_assets_py = int(request.form.get('net_assets_py'))
    form_issuance_of_new_shares = int(request.form.get('issuance_of_new_shares'))
    form_dividends_ss = int(request.form.get('dividends_ss'))
    form_purchase_of_treasury_stock = int(request.form.get('purchase_of_treasury_stock'))
    form_disposal_of_treasury_stock = int(request.form.get('disposal_of_treasury_stock'))
    calc_other_ss = form_net_assets - (form_net_assets_py + form_profit_loss_attributable_to_owners_of_parent + form_issuance_of_new_shares - form_dividends_ss - form_purchase_of_treasury_stock + form_disposal_of_treasury_stock)

    ################  CF  ######################
    # form_cf_operating_activities = request.form.get('cf_operating_activities')
    # form_cf_investment_activities = request.form.get('cf_investment_activities')
    # form_cf_financing_activities = request.form.get('cf_financing_activities')

    ################ OHTER ####################
    form_total_number_of_issued_shares = int(request.form.get('total_number_of_issued_shares'))
    form_number_of_shares_held_in_own_name = int(request.form.get('number_of_shares_held_in_own_name'))
    form_dividend_paid_per_share = int(request.form.get('dividend_paid_per_share'))
    form_effective_tax_rate = float(request.form.get('effective_tax_rate')) / 100

    ############### TAX_ON_OPERATING_INCOME #####################
    # a
    calc_tax_on_interest_income_and_dividend = form_interest_and_dividends_income * form_effective_tax_rate

    # b
    calc_tax_on_interest_expaneses =form_interest_expenses * form_effective_tax_rate
            
    # c = (その他営業外収益 - その他営業外費用) * effective tax rate
    calc_tax_on_non_operating_income_and_expenses_others = calc_other_non_operating_income_and_expenses * form_effective_tax_rate
    
    # d
    calc_tax_on_extraordinary_income_and_losses = form_extraordinary_income_and_loss * form_effective_tax_rate
    
    # e = income taxes - a + b - c - d
    calc_tax_on_operating_income = form_income_taxes - calc_tax_on_interest_income_and_dividend + calc_tax_on_interest_expaneses - calc_tax_on_non_operating_income_and_expenses_others - calc_tax_on_extraordinary_income_and_losses

    ############### NOPAT_TOPDOWN #####################
    # 営業利益 - 営業利益にかかる税金 + DTA（純額）の減少（増加はマイナス） + 持分法投資利益（損失はマイナス）
    calc_nopat_topdown = form_operating_income - calc_tax_on_operating_income - calc_fluctuations_in_deferred_tax_assets + form_equity_in_earnings_or_losses_of_affiliates


    ############### NOPAT_BOTTOMUP #####################
    # 親会社株主当期純利益 + 非支配株主当期純利益 + DTA（純額)の減少（増加はマイナス） + (特別損益 * (1-実効税率)) - (（受取利息+受取配当金) * (1-実効税率)) + (支払利息 * (1-実効税率)) + ((その他営業外損失 - その他営業外利益) * (1-実効税率))
    aa = form_profit_loss_attributable_to_owners_of_parent
    bb = form_profit_loss_attributable_to_non_controling_interests
    cc = calc_fluctuations_in_deferred_tax_assets
    dd = form_extraordinary_income_and_loss * (1 - form_effective_tax_rate)
    ee = form_interest_and_dividends_income * (1 - form_effective_tax_rate)
    ff = form_interest_expenses * (1 - form_effective_tax_rate)
    gg = calc_other_non_operating_income_and_expenses * (1 - form_effective_tax_rate)
    calc_nopat_bottomup = aa + bb - cc - dd - ee + ff - gg

    ############### INVESTMENT_CAPITAL #####################
    hh = form_notes_and_accounts_receivable_trade
    ii = form_inventories
    jj = calc_other_current_assets
    kk = form_notes_and_accounts_payable_trade
    ll = calc_other_current_liabilities
    calc_net_working_capital = hh + ii + jj - kk - ll
    mm = form_property_plant_and_equipment
    nn = form_intangible_assets
    oo = calc_net_deferred_tax_assets
    pp = form_investments_and_other_assets - form_deferred_tax_assets_ioa
    qq = calc_other_noncurrent_liabilities
    rr = form_cash_and_deposits
    ss = form_securities
    calc_invested_capital = calc_net_working_capital + mm + nn + oo + pp - qq + rr + ss

    ############### FREE_CASH_FLOW #####################
    calc_operating_cf = calc_nopat_topdown + form_depreciation + form_amortization_goodwill + (ly_calc_net_working_capital - calc_net_working_capital)
    calc_investment_cf = -1 * ((form_property_plant_and_equipment + form_intangible_assets) - (ly_form_property_plant_and_equipment + ly_form_intangible_assets) + (form_depreciation + form_impairment + form_amortization_goodwill))
    calc_free_cash_flow = calc_operating_cf + calc_investment_cf
    calc_non_operating_cf = -1 * (bb - cc - dd - ee + ff - gg) - cc - (((form_investments_and_other_assets - form_deferred_tax_assets_ioa) - calc_other_noncurrent_liabilities) - ((ly_form_investments_and_other_assets - ly_form_deferred_tax_assets_ioa) - ly_calc_other_noncurrent_liabilities))
    calc_financial_cf = ((form_short_term_interest_bearing_bond + form_long_term_interest_bearing_bond) - (ly_form_short_term_interest_bearing_bond + ly_form_long_term_interest_bearing_bond)) - form_dividends_ss + form_issuance_of_new_shares - form_purchase_of_treasury_stock + form_disposal_of_treasury_stock + calc_other_ss
    calc_net_cf = calc_free_cash_flow + calc_non_operating_cf + calc_financial_cf


    ############### ROE #####################
    calc_shareholders_equity = (form_capital_stock + form_capital_surplus + form_retained_earnings + form_treasury_stock + form_accumulated_other_comprehensive_income)
    calc_shareholders_equity_py = (ly_form_capital_stock + ly_form_capital_surplus + ly_form_retained_earnings + ly_form_treasury_stock + ly_form_accumulated_other_comprehensive_income)
    calc_average_shareholders_equity = (calc_shareholders_equity + calc_shareholders_equity_py) * 1/2
    calc_return_on_equity = form_profit_loss_attributable_to_owners_of_parent / calc_average_shareholders_equity
    calc_return_on_asset = form_profit_loss_attributable_to_owners_of_parent / form_net_sales
    calc_total_asset_turnover = form_net_sales / ((form_total_assets + ly_form_total_assets) * 1/2 )
    calc_financial_leverage = ((form_total_assets + ly_form_total_assets) * 1/2) / calc_average_shareholders_equity
    
    ############### WACC #####################  βを加味できていない
    form_borrowing_interest_rate = float(request.form.get('borrowing_interest_rate')) / 100
    RISK_FREE_RATE = 0.2 / 100                 # 2022/3/1〜2022/3/24 の10年物国債利率の平均
    COST_OF_SHAREHOLDERS_EQUITY = 8.0 / 100    # 株主の期待リターン。ここでは伊藤レポートに合わせて8%とした。
    calc_wacc = form_borrowing_interest_rate * ((form_short_term_interest_bearing_bond + form_long_term_interest_bearing_bond) / (form_short_term_interest_bearing_bond + form_long_term_interest_bearing_bond + calc_shareholders_equity)) + COST_OF_SHAREHOLDERS_EQUITY * (calc_shareholders_equity / (form_short_term_interest_bearing_bond + form_long_term_interest_bearing_bond + calc_shareholders_equity))

    ############### ROIC #####################
    calc_return_on_invested_capital = calc_nopat_topdown / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
    calc_return_on_invested_capital_before_tax = form_operating_income / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
    calc_tax_burden_rate = calc_tax_on_operating_income / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
    calc_affiliated_company_contribution_rate = form_equity_in_earnings_or_losses_of_affiliates / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
    calc_operating_profit_margin = form_operating_income / form_net_sales
    calc_cost_rate = form_cogs / form_net_sales
    calc_sga_ratio = form_sga / form_net_sales
    calc_invested_capital_turnover = form_net_sales / ((calc_invested_capital + ly_calc_invested_capital) * 1/2)
    calc_net_working_capital_turnover_days = calc_net_working_capital / (form_net_sales / 365)
    calc_trade_receivable_turnover_days = form_notes_and_accounts_receivable_trade / (form_net_sales / 365)
    calc_trade_payable_turnover_days = form_notes_and_accounts_payable_trade / (form_net_sales / 365)
    calc_inventries_turnover_days = form_inventories / (form_net_sales / 365)
    calc_property_turnover_days = form_property_plant_and_equipment / (form_net_sales / 365)
    calc_intangible_turnover_days = form_intangible_assets / (form_net_sales / 365)
    calc_other_invested_capital_turnover_days = (calc_invested_capital - calc_net_working_capital - form_inventories - form_property_plant_and_equipment - form_intangible_assets) / (form_net_sales / 365)
    calc_cash_conversion_cicle = calc_inventries_turnover_days + calc_trade_receivable_turnover_days - calc_trade_payable_turnover_days

    ############### VALUATION #################
    R = [-0.02, 0, 0.02, 0.04, 0.06]               # 成長率
    S = [-0.015, -0.01, 0, 0.01, 0.015]               # WACCに対するストレス

    wacc_adj = []
    grows_rate = []
    calc_valuation = []                             # 5 * 5 = 25 通りのvaluationを実施
    calc_max_valuation = 0                          # valuation の最大値を保持
    calc_min_valuation = 10**16                     # valuation の最小値を保持
    for r in R:
        for s in S:
            try:
                v = calc_free_cash_flow / ((calc_wacc + s) - r)
                calc_valuation.append(v)
                wacc_adj.append(calc_wacc + s)
                grows_rate.append(r)
                if calc_max_valuation < v:
                    calc_max_valuation = v
                if calc_min_valuation > v:
                    calc_min_valuation = v
            except:
                calc_valuation.append("NaN")
                wacc_adj.append(calc_wacc + s)
                grows_rate.append(r)



    financial_data = FinancialData(
        uid = uid,
        year_before_last = form_year_before_last,
        last_year = form_last_year,
        this_year = form_this_year,
    
        ############### year_before_last : t - 2 ####################
        ybl_net_sales = ybl_form_net_sales,
        ybl_cogs = ybl_form_cogs,
        # gross_profit = form_gross_profit,
        ybl_sga = ybl_form_sga,
        ybl_operating_income = ybl_form_operating_income,
        
        ybl_interest_and_dividends_income = ybl_form_interest_and_dividends_income,
        ybl_equity_in_earnings_or_losses_of_affiliates = ybl_form_equity_in_earnings_or_losses_of_affiliates,
        # ybl_other_non_operating_income = ybl_calc_other_non_operating_income,
        # ybl_non_operating_income = ybl_form_non_operating_income,

        ybl_interest_expenses = ybl_form_interest_expenses,
        # ybl_equity_in_losses_of_affiliates = ybl_form_equity_in_losses_of_affiliates,
        # ybl_other_non_operating_expenses = ybl_calc_other_non_operating_expenses,
        # ybl_non_operating_expenses = ybl_form_non_operating_expenses,
        ybl_ordinary_income_loss = ybl_form_ordinary_income_loss,
        ybl_other_nonoperating_income_or_loss = ybl_calc_other_non_operating_income_or_expense,
        
        ybl_extraordinary_income_and_loss = ybl_form_extraordinary_income_and_loss,
        ybl_income_before_income_taxes = ybl_form_income_before_income_taxes,
        ybl_income_taxes = ybl_form_income_taxes,
        ybl_profit_loss_attributable_to_non_controling_interests = ybl_form_profit_loss_attributable_to_non_controling_interests,
        ybl_profit_loss_attributable_to_owners_of_parent = ybl_form_profit_loss_attributable_to_owners_of_parent,

        ybl_depreciation = ybl_form_depreciation,
        ybl_amortization_goodwill = ybl_form_amortization_goodwill,
        ybl_impairment = ybl_form_impairment,

        ################  BS  ######################
        ybl_cash_and_deposits = ybl_form_cash_and_deposits,
        ybl_securities = ybl_form_securities,
        ybl_notes_and_accounts_receivable_trade = ybl_form_notes_and_accounts_receivable_trade,
        ybl_inventories = ybl_form_inventories,
        ybl_deferred_tax_assets_ca = ybl_form_deferred_tax_assets_ca,
        ybl_other_current_assets = ybl_calc_other_current_assets,
        ybl_current_assets = ybl_form_current_assets,

        ybl_property_plant_and_equipment = ybl_form_property_plant_and_equipment,
        
        ybl_intangible_assets = ybl_form_intangible_assets,

        ybl_deferred_tax_assets_ioa = ybl_form_deferred_tax_assets_ioa,
        ybl_investments_and_other_assets = ybl_form_investments_and_other_assets,
        
        ybl_total_assets = ybl_form_total_assets,

        ybl_short_term_interest_bearing_bond = ybl_form_short_term_interest_bearing_bond,
        ybl_notes_and_accounts_payable_trade = ybl_form_notes_and_accounts_payable_trade,
        ybl_deferred_tax_liabilities_ca = ybl_form_deferred_tax_liabilities_ca,
        ybl_other_current_liabilities = ybl_calc_other_current_liabilities,
        ybl_current_liabilities = ybl_form_current_liabilities,

        ybl_long_term_interest_bearing_bond = ybl_form_long_term_interest_bearing_bond,
        ybl_deferred_tax_liabilities_ncl = ybl_form_deferred_tax_liabilities_ncl,
        ybl_other_noncurrent_liabilities = ybl_calc_other_noncurrent_liabilities,
        ybl_noncurrent_liabilities = ybl_form_noncurrent_liabilities,

        ybl_capital_stock = ybl_form_capital_stock,
        ybl_capital_surplus = ybl_form_capital_surplus,
        ybl_retained_earnings = ybl_form_retained_earnings,
        ybl_treasury_stock = ybl_form_treasury_stock,
        ybl_accumulated_other_comprehensive_income = ybl_form_accumulated_other_comprehensive_income,
        ybl_subscription_rights_to_shares = ybl_form_subscription_rights_to_shares,
        ybl_non_controlling_interests = ybl_form_non_controlling_interests,
        ybl_net_assets = ybl_form_net_assets,

        ybl_liabilities_and_net_assets = ybl_form_liabilities_and_net_assets,
        ybl_net_deferred_tax_assets = ybl_calc_net_deferred_tax_assets,

        ################  SS  ######################
        ybl_net_assets_py = ybl_form_net_assets_py,
        ybl_issuance_of_new_shares = ybl_form_issuance_of_new_shares,
        ybl_dividends_ss = ybl_form_dividends_ss,
        ybl_purchase_of_treasury_stock = ybl_form_purchase_of_treasury_stock,
        ybl_disposal_of_treasury_stock = ybl_form_disposal_of_treasury_stock,

        ################  CF  ######################
        # ybl_cf_operating_activities = ybl_form_cf_operating_activities,
        # ybl_cf_investment_activities = ybl_form_cf_investment_activities,
        # ybl_cf_financing_activities = ybl_form_cf_financing_activities,

        ################ OHTER ####################
        ybl_total_number_of_issued_shares = ybl_form_total_number_of_issued_shares,
        ybl_number_of_shares_held_in_own_name = ybl_form_number_of_shares_held_in_own_name,
        ybl_dividend_paid_per_share = ybl_form_dividend_paid_per_share,
        ybl_effective_tax_rate = ybl_form_effective_tax_rate,

        ############### INVESTED_CAPITAL #####################
        ybl_invested_capital = ybl_calc_invested_capital,


        ############### last_year : t - 1 ###########################
        ly_net_sales = ly_form_net_sales,
        ly_cogs = ly_form_cogs,
        # gross_profit = form_gross_profit,
        ly_sga = ly_form_sga,
        ly_operating_income = ly_form_operating_income,

        ly_interest_and_dividends_income = ly_form_interest_and_dividends_income,
        ly_equity_in_earnings_or_losses_of_affiliates = ly_form_equity_in_earnings_or_losses_of_affiliates,
        # ly_other_non_operating_income = ly_calc_other_non_operating_income,
        # ly_non_operating_income = ly_form_non_operating_income,
        
        ly_interest_expenses = ly_form_interest_expenses,
        # ly_equity_in_losses_of_affiliates = ly_form_equity_in_losses_of_affiliates,
        # ly_other_non_operating_expenses = ly_calc_other_non_operating_expenses,
        # ly_non_operating_expenses = ly_form_non_operating_expenses,
        ly_ordinary_income_loss = ly_form_ordinary_income_loss,
        ly_other_nonoperating_income_or_loss = ly_calc_other_non_operating_income_and_expenses,

        ly_extraordinary_income_and_loss = ly_form_extraordinary_income_and_loss,
        ly_income_before_income_taxes = ly_form_income_before_income_taxes,
        ly_income_taxes = ly_form_income_taxes,
        ly_profit_loss_attributable_to_non_controling_interests = ly_form_profit_loss_attributable_to_non_controling_interests,
        ly_profit_loss_attributable_to_owners_of_parent = ly_form_profit_loss_attributable_to_owners_of_parent,

        ly_depreciation = ly_form_depreciation,
        ly_amortization_goodwill = ly_form_amortization_goodwill,
        ly_impairment = ly_form_impairment,

        ################  BS  ######################
        ly_cash_and_deposits = ly_form_cash_and_deposits,
        ly_securities = ly_form_securities,
        ly_notes_and_accounts_receivable_trade = ly_form_notes_and_accounts_receivable_trade,
        ly_inventories = ly_form_inventories,
        ly_deferred_tax_assets_ca = ly_form_deferred_tax_assets_ca,
        ly_other_current_assets = ly_calc_other_current_assets,
        ly_current_assets = ly_form_current_assets,

        ly_property_plant_and_equipment = ly_form_property_plant_and_equipment,
        
        ly_intangible_assets = ly_form_intangible_assets,

        ly_deferred_tax_assets_ioa = ly_form_deferred_tax_assets_ioa,
        ly_investments_and_other_assets = ly_form_investments_and_other_assets,
        
        ly_total_assets = ly_form_total_assets,

        ly_short_term_interest_bearing_bond = ly_form_short_term_interest_bearing_bond,
        ly_notes_and_accounts_payable_trade = ly_form_notes_and_accounts_payable_trade,
        ly_deferred_tax_liabilities_ca = ly_form_deferred_tax_liabilities_ca,
        ly_other_current_liabilities = ly_calc_other_current_liabilities,
        ly_current_liabilities = ly_form_current_liabilities,

        ly_long_term_interest_bearing_bond = ly_form_long_term_interest_bearing_bond,
        ly_deferred_tax_liabilities_ncl = ly_form_deferred_tax_liabilities_ncl,
        ly_other_noncurrent_liabilities = ly_calc_other_noncurrent_liabilities,
        ly_noncurrent_liabilities = ly_form_noncurrent_liabilities,

        ly_capital_stock = ly_form_capital_stock,
        ly_capital_surplus = ly_form_capital_surplus,
        ly_retained_earnings = ly_form_retained_earnings,
        ly_treasury_stock = ly_form_treasury_stock,
        ly_accumulated_other_comprehensive_income = ly_form_accumulated_other_comprehensive_income,
        ly_subscription_rights_to_shares = ly_form_subscription_rights_to_shares,
        ly_non_controlling_interests = ly_form_non_controlling_interests,
        ly_net_assets = ly_form_net_assets,

        ly_liabilities_and_net_assets = ly_form_liabilities_and_net_assets,
        ly_net_deferred_tax_assets = ly_calc_net_deferred_tax_assets,
        ly_fluctuations_in_deferred_tax_assets = ly_calc_fluctuations_in_deferred_tax_assets,

        ################  SS  ######################
        ly_net_assets_py = ly_form_net_assets_py,
        ly_issuance_of_new_shares = ly_form_issuance_of_new_shares,
        ly_dividends_ss = ly_form_dividends_ss,
        ly_purchase_of_treasury_stock = ly_form_purchase_of_treasury_stock,
        ly_disposal_of_treasury_stock = ly_form_disposal_of_treasury_stock,

        ################  CF  ######################
        # ly_cf_operating_activities = ly_form_cf_operating_activities,
        # ly_cf_investment_activities = ly_form_cf_investment_activities,
        # ly_cf_financing_activities = ly_form_cf_financing_activities,

        ################ OHTER ####################
        ly_total_number_of_issued_shares = ly_form_total_number_of_issued_shares,
        ly_number_of_shares_held_in_own_name = ly_form_number_of_shares_held_in_own_name,
        ly_dividend_paid_per_share = ly_form_dividend_paid_per_share,
        ly_effective_tax_rate = ly_form_effective_tax_rate,

        ############### TAX_ON_OPERATING_INCOME #####################
        ly_tax_on_interest_income_and_dividend = ly_calc_tax_on_interest_income_and_dividend,
        ly_tax_on_interest_expenses = ly_calc_tax_on_interest_expaneses,
        ly_tax_on_non_operating_income_and_expenses_others = ly_calc_tax_on_non_operating_income_and_expenses_others,
        ly_tax_on_extraordinary_income_and_losses = ly_calc_tax_on_extraordinary_income_and_losses,
        ly_tax_on_operating_income = ly_calc_tax_on_operating_income,

        ############### NOPAT_TOPDOWN #####################
        ly_nopat_topdown = ly_calc_nopat_topdown,

        ############### NOPAT_BOTTOMUP #####################
        ly_nopat_bottomup = ly_calc_nopat_bottomup,

        ############### INVESTED_CAPITAL #####################
        ly_net_working_capital = ly_calc_net_working_capital,
        ly_investment_capital = ly_calc_invested_capital,

        ############### FREE_CASH_FLOW #####################
        ly_operating_cf = ly_calc_operating_cf,
        ly_investment_cf = ly_calc_investment_cf,
        ly_free_cash_flow = ly_calc_free_cash_flow,
        ly_non_operating_cf = ly_calc_non_operating_cf,
        ly_financial_cf = ly_calc_financial_cf,
        ly_net_cf = ly_calc_net_cf,

        ############### ROE #####################
        ly_return_on_equity = ly_calc_return_on_equity,
        ly_return_on_asset = ly_calc_return_on_asset,
        ly_total_asset_turnover = ly_calc_total_asset_turnover,
        ly_financial_leverage = ly_calc_financial_leverage,

        ############### WACC #####################


        ############### ROIC #####################
        ly_return_on_invested_capital = ly_calc_return_on_invested_capital,
        ly_return_on_invested_capital_before_tax = ly_calc_return_on_invested_capital_before_tax,
        ly_tax_burden_rate = ly_calc_tax_burden_rate,
        ly_affiliated_company_contribution_rate = ly_calc_affiliated_company_contribution_rate,
        ly_operating_profit_margin = ly_calc_operating_profit_margin,
        ly_cost_rate = ly_calc_cost_rate,
        ly_sga_ratio = ly_calc_sga_ratio,
        ly_invested_capital_turnover = ly_calc_invested_capital_turnover,
        ly_net_working_capital_turnover_days = ly_calc_net_working_capital_turnover_days,
        ly_trade_receivavle_turnover_days = ly_calc_trade_receivable_turnover_days,
        ly_trade_payable_turnover_days = ly_calc_trade_payable_turnover_days,
        ly_inventries_turnover_days = ly_calc_inventries_turnover_days,
        ly_property_turnover_days = ly_calc_property_turnover_days,
        ly_intangible_turnover_days = ly_calc_intangible_turnover_days,
        ly_other_invested_capital_turnover_days = ly_calc_other_invested_capital_turnover_days,
        ly_cash_conversion_cicle = ly_calc_cash_conversion_cicle,



        ############### this_year : t ###############################
        net_sales = form_net_sales,
        cogs = form_cogs,
        # gross_profit = form_gross_profit,
        sga = form_sga,
        operating_income = form_operating_income,

        interest_and_dividends_income = form_interest_and_dividends_income,
        equity_in_earnings_or_losses_of_affiliates = form_equity_in_earnings_or_losses_of_affiliates,
        # other_non_operating_income = calc_other_non_operating_income,
        # non_operating_income = form_non_operating_income,

        interest_expenses = form_interest_expenses,
        # equity_in_losses_of_affiliates = form_equity_in_losses_of_affiliates,
        # non_operating_expenses = form_non_operating_expenses,
        # other_non_operating_expenses = calc_other_non_operating_expenses,
        ordinary_income_loss = form_ordinary_income_loss,
        other_nonoperating_income_or_loss = calc_other_non_operating_income_and_expenses,

        extraordinary_income_and_loss = form_extraordinary_income_and_loss,
        income_before_income_taxes = form_income_before_income_taxes,
        income_taxes = form_income_taxes,
        profit_loss_attributable_to_non_controling_interests = form_profit_loss_attributable_to_non_controling_interests,
        profit_loss_attributable_to_owners_of_parent = form_profit_loss_attributable_to_owners_of_parent,

        depreciation = form_depreciation,
        amortization_goodwill = form_amortization_goodwill,
        impairment = form_impairment,

        ################  BS  ######################
        cash_and_deposits = form_cash_and_deposits,
        securities = form_securities,
        notes_and_accounts_receivable_trade = form_notes_and_accounts_receivable_trade,
        inventories = form_inventories,
        deferred_tax_assets_ca = form_deferred_tax_assets_ca,
        other_current_assets = calc_other_current_assets,
        current_assets = form_current_assets,

        property_plant_and_equipment = form_property_plant_and_equipment,
        
        intangible_assets = form_intangible_assets,

        deferred_tax_assets_ioa = form_deferred_tax_assets_ioa,
        investments_and_other_assets = form_investments_and_other_assets,
        
        total_assets = form_total_assets,

        short_term_interest_bearing_bond = form_short_term_interest_bearing_bond,
        notes_and_accounts_payable_trade = form_notes_and_accounts_payable_trade,
        deferred_tax_liabilities_ca = form_deferred_tax_liabilities_ca,
        other_current_liabilities = calc_other_current_liabilities,
        current_liabilities = form_current_liabilities,

        long_term_interest_bearing_bond = form_long_term_interest_bearing_bond,
        deferred_tax_liabilities_ncl = form_deferred_tax_liabilities_ncl,
        other_noncurrent_liabilities = calc_other_noncurrent_liabilities,
        noncurrent_liabilities = form_noncurrent_liabilities,

        capital_stock = form_capital_stock,
        capital_surplus = form_capital_surplus,
        retained_earnings = form_retained_earnings,
        treasury_stock = form_treasury_stock,
        accumulated_other_comprehensive_income = form_accumulated_other_comprehensive_income,
        subscription_rights_to_shares = form_subscription_rights_to_shares,
        non_controlling_interests = form_non_controlling_interests,
        net_assets = form_net_assets,

        liabilities_and_net_assets = form_liabilities_and_net_assets,
        net_deferred_tax_assets = calc_net_deferred_tax_assets,
        fluctuations_in_deferred_tax_assets = calc_fluctuations_in_deferred_tax_assets,

        ################  SS  ######################
        net_assets_py = form_net_assets_py,
        issuance_of_new_shares = form_issuance_of_new_shares,
        dividends_ss = form_dividends_ss,
        purchase_of_treasury_stock = form_purchase_of_treasury_stock,
        disposal_of_treasury_stock = form_disposal_of_treasury_stock,

        ################  CF  ######################
        # cf_operating_activities = form_cf_operating_activities,
        # cf_investment_activities = form_cf_investment_activities,
        # cf_financing_activities = form_cf_financing_activities,

        ################ OHTER ####################
        total_number_of_issued_shares = form_total_number_of_issued_shares,
        number_of_shares_held_in_own_name = form_number_of_shares_held_in_own_name,
        dividend_paid_per_share = form_dividend_paid_per_share,
        effective_tax_rate = form_effective_tax_rate,

        ############### TAX_ON_OPERATING_INCOME #####################
        tax_on_interest_income_and_dividend = calc_tax_on_interest_income_and_dividend,
        tax_on_interest_expenses = calc_tax_on_interest_expaneses,
        tax_on_non_operating_income_and_expenses_others = calc_tax_on_non_operating_income_and_expenses_others,
        tax_on_extraordinary_income_and_losses = calc_tax_on_extraordinary_income_and_losses,
        tax_on_operating_income = calc_tax_on_operating_income,

        ############### NOPAT_TOPDOWN #####################
        nopat_topdown = calc_nopat_topdown,

        ############### NOPAT_BOTTOMUP #####################
        nopat_bottomup = calc_nopat_bottomup,

        ############### INVESTMENT_CAPITAL #####################
        net_working_capital = calc_net_working_capital,
        investment_capital = calc_invested_capital,

        ############### FREE_CASH_FLOW #####################
        operating_cf = calc_operating_cf,
        investment_cf = calc_investment_cf,
        free_cash_flow = calc_free_cash_flow,
        non_operating_cf = calc_non_operating_cf,
        financial_cf = calc_financial_cf,
        net_cf = calc_net_cf,

        ############### ROE #####################
        return_on_equity = calc_return_on_equity,
        return_on_asset = calc_return_on_asset,
        total_asset_turnover = calc_total_asset_turnover,
        financial_leverage = calc_financial_leverage,

        ############### WACC #####################
        borrowing_interest_rate = form_borrowing_interest_rate,
        risk_free_rate = RISK_FREE_RATE,
        cost_of_shareholders_equity = COST_OF_SHAREHOLDERS_EQUITY,
        wacc = calc_wacc,

        ############### ROIC #####################
        return_on_invested_capital = calc_return_on_invested_capital,
        return_on_invested_capital_before_tax = calc_return_on_invested_capital_before_tax,
        tax_burden_rate = calc_tax_burden_rate,
        affiliated_company_contribution_rate = calc_affiliated_company_contribution_rate,
        operating_profit_margin = calc_operating_profit_margin,
        cost_rate = calc_cost_rate,
        sga_ratio = calc_sga_ratio,
        invested_capital_turnover = calc_invested_capital_turnover,
        net_working_capital_turnover_days = calc_net_working_capital_turnover_days,
        trade_receivavle_turnover_days = calc_trade_receivable_turnover_days,
        trade_payable_turnover_days = calc_trade_payable_turnover_days,
        inventries_turnover_days = calc_inventries_turnover_days,
        property_turnover_days = calc_property_turnover_days,
        intangible_turnover_days = calc_intangible_turnover_days,
        other_invested_capital_turnover_days = calc_other_invested_capital_turnover_days,
        cash_conversion_cicle = calc_cash_conversion_cicle,

        ############### VALUATION #####################
        valuation_01 = calc_valuation[0],
        wacc_adj_01 = wacc_adj[0],
        grows_rate_01 = grows_rate[0],
        valuation_02 = calc_valuation[1],
        wacc_adj_02 = wacc_adj[1],
        grows_rate_02 = grows_rate[1],
        valuation_03 = calc_valuation[2],
        wacc_adj_03 = wacc_adj[2],
        grows_rate_03 = grows_rate[2],
        valuation_04 = calc_valuation[3],
        wacc_adj_04 = wacc_adj[3],
        grows_rate_04 = grows_rate[3],
        valuation_05 = calc_valuation[4],
        wacc_adj_05 = wacc_adj[4],
        grows_rate_05 = grows_rate[4],
        valuation_06 = calc_valuation[5],
        wacc_adj_06 = wacc_adj[5],
        grows_rate_06 = grows_rate[5],
        valuation_07 = calc_valuation[6],
        wacc_adj_07 = wacc_adj[6],
        grows_rate_07 = grows_rate[6],
        valuation_08 = calc_valuation[7],
        wacc_adj_08 = wacc_adj[7],
        grows_rate_08 = grows_rate[7],
        valuation_09 = calc_valuation[8],
        wacc_adj_09 = wacc_adj[8],
        grows_rate_09 = grows_rate[8],
        valuation_10 = calc_valuation[9],
        wacc_adj_10 = wacc_adj[9],
        grows_rate_10 = grows_rate[9],
        valuation_11 = calc_valuation[10],
        wacc_adj_11 = wacc_adj[10],
        grows_rate_11 = grows_rate[10],
        valuation_12 = calc_valuation[11],
        wacc_adj_12 = wacc_adj[11],
        grows_rate_12 = grows_rate[11],
        valuation_13 = calc_valuation[12],
        wacc_adj_13 = wacc_adj[12],
        grows_rate_13 = grows_rate[12],
        valuation_14 = calc_valuation[13],
        wacc_adj_14 = wacc_adj[13],
        grows_rate_14 = grows_rate[13],
        valuation_15 = calc_valuation[14],
        wacc_adj_15 = wacc_adj[14],
        grows_rate_15 = grows_rate[14],
        valuation_16 = calc_valuation[15],
        wacc_adj_16 = wacc_adj[15],
        grows_rate_16 = grows_rate[15],
        valuation_17 = calc_valuation[16],
        wacc_adj_17 = wacc_adj[16],
        grows_rate_17 = grows_rate[16],
        valuation_18 = calc_valuation[17],
        wacc_adj_18 = wacc_adj[17],
        grows_rate_18 = grows_rate[17],
        valuation_19 = calc_valuation[18],
        wacc_adj_19 = wacc_adj[18],
        grows_rate_19 = grows_rate[18],
        valuation_20 = calc_valuation[19],
        wacc_adj_20 = wacc_adj[19],
        grows_rate_20 = grows_rate[19],
        valuation_21 = calc_valuation[20],
        wacc_adj_21 = wacc_adj[20],
        grows_rate_21 = grows_rate[20],
        valuation_22 = calc_valuation[21],
        wacc_adj_22 = wacc_adj[21],
        grows_rate_22 = grows_rate[21],
        valuation_23 = calc_valuation[22],
        wacc_adj_23 = wacc_adj[22],
        grows_rate_23 = grows_rate[22],
        valuation_24 = calc_valuation[23],
        wacc_adj_24 = wacc_adj[23],
        grows_rate_24 = grows_rate[23],
        valuation_25 = calc_valuation[24],
        wacc_adj_25 = wacc_adj[24],
        grows_rate_25 = grows_rate[24],
        max_valuation = calc_max_valuation,
        min_valuation = calc_min_valuation,

    )

    db.session.merge(financial_data)
    db.session.commit()
    return redirect('/result')




