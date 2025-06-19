import pandas as pd

def extract_income_statement(file, year):
    df = pd.read_csv(file)
    df['Description'] = df['Description'].str.lower()

    data = {
        "Year": int(year),
        "Revenue": df.loc[df['Description'] == 'revenue', f"{year} AMD'000"].values[0],
        "Expenses": df.loc[df['Description'] == 'total expenses', f"{year} AMD'000"].values[0],
        "Net Income": df.loc[df['Description'] == 'profit and total comprehensive income for the year', f"{year} AMD'000"].values[0],
    }
    return data

def extract_balance_sheet(file, year):
    df = pd.read_csv(file)
    df['Description'] = df['Description'].str.lower()

    current_assets_labels = [
        'inventory',
        'trade and other receivables',
        'bank deposits',
        'cash and cash equivalents'
    ]
    current_assets = df[df['Description'].isin(current_assets_labels)][f"31.12.{year} AMD'000"].sum()

    current_liabilities_labels = [
        'lease liability',
        'trade and other payables',
        'profit tax liability'
    ]
    current_liabilities = df[df['Description'].isin(current_liabilities_labels)][f"31.12.{year} AMD'000"].sum()

    total_liabilities = df.loc[df['Description'] == 'total liabilities', f"31.12.{year} AMD'000"].values[0]

    equity_labels = [
        'share capital',
        'other reserves',
        'retained earnings'
    ]
    total_equity = df[df['Description'].isin(equity_labels)][f"31.12.{year} AMD'000"].sum()

    data = {
        "Year": int(year),
        "Current Assets": current_assets,
        "Current Liabilities": current_liabilities,
        "Total Liabilities": total_liabilities,
        "Total Equity": total_equity
    }
    return data

years = ['2021', '2022', '2023']

income_data = []
balance_data = []

for y in years:
    income_data.append(extract_income_statement(f"data/income_statement_{y}.csv", y))
    balance_data.append(extract_balance_sheet(f"data/balance_sheet_{y}.csv", y))


is_df = pd.DataFrame(income_data)
bs_df = pd.DataFrame(balance_data)


is_df['Revenue Growth (%)'] = is_df['Revenue'].pct_change() * 100
is_df['Expenses Growth (%)'] = is_df['Expenses'].pct_change() * 100
is_df['Profit Margin (%)'] = (is_df['Net Income'] / is_df['Revenue']) * 100

bs_df['Debt-to-Equity'] = bs_df['Total Liabilities'] / bs_df['Total Equity']
bs_df['Current Ratio'] = bs_df['Current Assets'] / bs_df['Current Liabilities']



print("\nIncome Statement with Ratios:")
print(is_df)

print("\nBalance Sheet with Ratios:")
print(bs_df)


is_df.to_csv('output/income_statement_calculated.csv', index=False)
bs_df.to_csv('output/balance_sheet_calculated.csv', index=False)


# Optional: Plot

import matplotlib.pyplot as plt

plt.plot(is_df['Year'], is_df['Revenue'], label='Revenue')
plt.plot(is_df['Year'], is_df['Expenses'], label='Expenses')
plt.plot(is_df['Year'], is_df['Net Income'], label='Net Income')

plt.xlabel('Year')
plt.ylabel('AMD\'000')
plt.title('ArCa Revenue, Expenses, Net Income (2021–2023)')
plt.legend()
plt.grid(True)
plt.show()
plt.plot(bs_df['Year'], bs_df['Current Ratio'], label='Current Ratio')
plt.plot(bs_df['Year'], bs_df['Debt-to-Equity'], label='Debt-to-Equity')