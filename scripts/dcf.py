import pandas as pd

def dcf(
        years, 
        operating_cash_flow, 
        capex,
        debt,
        cash,
        total_shares_outstanding
    ):

    forecast_years = 5
    operating_cash_flow_g = 0.02
    capex_growth = 0.02
    discount_rate = 0.10
    terminal_growth = 0.01

    df_columns = years + [x+1 for x in range(years[-1], years[-1]+forecast_years)]
    df = pd.DataFrame(columns=df_columns)
    df.loc["operating_cash_flow"] = operating_cash_flow + [operating_cash_flow[-1]*(1 + operating_cash_flow_g)**x for x in range(1, forecast_years+1)]
    df.loc["capex"] = capex + [capex[-1]*(1 + capex_growth)**x for x in range(1, forecast_years+1)]
    df.loc["free_cash_flow"] = df.loc["operating_cash_flow"] - df.loc["capex"]
    df.loc["discount_factor"] = [None]*len(years) + [1 / ((1 + discount_rate) ** x) for x in range(1, forecast_years+1)]
    df.loc["pv_free_cash_flow"] = df.loc["free_cash_flow"] * df.loc["discount_factor"]
    print(df.loc[:, range(years[-1], years[-1]+forecast_years+1)].round(2))

    terminal_value = (
        df.loc["free_cash_flow", years[-1]+forecast_years] * (1 + terminal_growth) / 
        (discount_rate - terminal_growth)
    )
    discount_factor = df.loc["discount_factor", df_columns[-1]]
    pv_terminal_value = terminal_value * discount_factor
    enterprise_value = df.loc["pv_free_cash_flow"].sum() + pv_terminal_value
    equity_value = enterprise_value - debt[-1] - cash[-1]
    equity_value_per_share = equity_value / total_shares_outstanding[-1]
    print(f"""
- pv_free_cash_flow_sum: {df.loc['pv_free_cash_flow'].sum()}
- terminal_value: {terminal_value}
- discount_factor: {discount_factor}
- pv_terminal_value: {pv_terminal_value}
- debt: {debt[-1]}
- cash: {cash[-1]}
- equity_value: {equity_value}
- total_shares_outstanding: {total_shares_outstanding[-1]}
- equity_value_per_share: {equity_value_per_share}
    """)

    return equity_value_per_share


if __name__ == "__main__":
    dcf(
        years=[2022, 2023, 2024], 
        operating_cash_flow=[6363, 6464, 8025], 
        capex=[6366, 5323, 5305],
        debt=[23025, 20095, 22075],
        cash=[5, 5, 5],
        total_shares_outstanding=[641, 643, 650],
    )