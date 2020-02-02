import pandas as pd
import sqlite3


def read_csv(acq_perf='Acquisition'):
    """
    Args:
        acq_perf (str):  'Acquisition' or 'Performance' CSV files to read

        Note - Please download the data from
            https://www.fanniemae.com/portal/funding-the-market/data/loan-performance-data.html
            Then unzip individual files and move them into a 'data' folder to use this function.
    Returns:
        Pandas DataFrame from either 'Acquisition' or 'Performance' CSV file
    """
    # Column names and descriptions (in comments) because there's no header in the "*.txt"
    HEADERS = {
        "Acquisition": [
            "id",  # LOAN IDENTIFIER
            "channel",  # ORIGINATION CHANNEL
            "seller",  # SELLER NAME
            "interest_rate",  # ORIGINAL INTEREST RATE
            "balance",  # ORIGINAL UPB
            "loan_term",  # ORIGINAL LOAN TERM
            "origination_date",  # ORIGINATION DATE
            "first_payment_date",  # FIRST PAYMENT DATE
            "ltv",  # LOAN-TO-VALUE
            "cltv",  # COMBINED LOAN-TO-VALUE
            "borrower_count",  # NUMBER OF BORROWERS
            "dti",  # DEBT TO INCOME RATIO
            "borrower_score",  # BORROWER CREDIT SCORE
            "first_time_homebuyer",  # FIRST TIME HOME BUYER INDICATOR
            "loan_purpose",  # LOAN PURPOSE
            "property_type",  # PROPERTY TYPE
            "unit_count",  # NUMBER OF UNIT
            "occupancy_type",  # OCCUPANCY TYPE
            "property_state",  # PROPERTY STATE
            "zip",  # ZIPCODE SHORT (FIRST 3 DIGITS)
            "insurance_percentage",  # PRIMARY MORTGAGE INSURANCE PERCENT
            "product_type",  # PRODUCT TYPE
            "coborrower_score",  # CO-BORROWER CREDIT SCORE
            "insurance_type",  # MORTGAGE INSURANCE TYPE
            "relocation_flag",  # RELOCATION MORTGAGE INDICATOR
            ],
        "Performance": [
            "id",
            "reporting_period",
            "servicer_name",
            "interest_rate",  # CURRENT INTEREST RATE
            "balance",  # CURRENT BALANCE
            "loan_age",
            "months_to_maturity", # REMAINING MONTHS TO LEGAL MATURITY
            "adj_months_to_maturity", # ADJUSTED MONTHS TO MATURITY
            "maturity_date",
            "msa",  # METROPOLITAN STATISTICAL AREA
            "delinquency_status", # CURRENT LOAN DELINQUENCY STATUS
            "modification_flag",  # MODIFICATION FLAG
            "zero_balance_code", # ZERO BALANCE CODE
            "zero_balance_date", # ZERO BALANCE EFFECTIVE DATE
            "last_paid_installment_date",  # LAST PAID INSTALLMENT DATE
            "foreclosure_date", # FORECLOSURE DATE
            "disposition_date", # DISPOSITION DATE
            "foreclosure_costs", # FORECLOSURE COSTS
            "property_repair_costs", # PROPERTY PRESERVATION AND REPAIR COSTS
            "recovery_costs", # ASSET RECOVERY COSTS
            "misc_costs", # MISCELLANEOUS HOLDING EXPENSES AND CREDITS
            "tax_costs", # ASSOCIATED TAXES FOR HOLDING PROPERTY
            "sale_proceeds", # NET SALE PROCEEDS
            "credit_enhancement_proceeds", # CREDIT ENHANCEMENT PROCEEDS
            "repurchase_proceeds", # REPURCHASE MAKE WHOLE PROCEEDS
            "other_foreclosure_proceeds",
            "non_interest_bearing_balance",
            "principal_forgiveness_balance",
            "make_whole_flag",  # REPURCHASE MAKE WHOLE PROCEEDS FLAG
            "foreclosure_writeoff",  # FORECLOSURE PRINCIPAL WRITE-OFF AMOUNT
            "activity_flag" # SERVICING ACTIVITY INDICATOR
            ]
        }

    exclude_cols = [
        "first_payment_date",
        "zip",  # only 3 digit codes in Acquisition and possible errors in input as there are 1 and 2 digit codes,
        # more useful with 'msa' in Performance
        "credit_enhancement_proceeds",
        "other_foreclosure_proceeds",
        "non_interest_bearing_balance",
        "principal_forgiveness_balance",
        "make_whole_flag"
        "activity_flag"
        ]

    use_idx = [i for i, col in enumerate(HEADERS[acq_perf]) if col not in exclude_cols]

    df = []
    for q in range(1, 5):  # For the 4 Quarters of 2018
        df.append(pd.read_csv(f'{acq_perf}_2018Q{q}.txt', sep='|',
                              names=HEADERS[acq_perf], usecols=use_idx,
                              low_memory=False))

    return pd.concat(df, axis=0, ignore_index=True)


def create_sqlite_db(df, tablename='Untitled', conn=None):
    """
    Args:
        df (pandas.DataFrame):  DataFrame to add as table
        tablename (str): Table name to set in the SQLite Database
        conn (sqlite3.connect): SQLite connection, if None create a connection

    """
    if conn is None:
        conn = sqlite3.connect('Secondary_Mortgage_Loans.db')

    df.to_sql(tablename, con=conn)


def preprocess(df):
    # create a new feature with loans up to the point of either being delinquent or Dec 2018/2019
    #

    pass