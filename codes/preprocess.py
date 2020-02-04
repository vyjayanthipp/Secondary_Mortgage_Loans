import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
import os

module_path = os.path.abspath(os.path.join('..'))  # assumed the Parent Directory is the highest level of the
# project folder ("Secondary_Mortgage_Loans"

def read_csv(acq_perf='Acquisition'):
    """
    Note - Please download the data from https://www.fanniemae.com/portal/funding-the-market/data/loan-performance-data.html
    Then unzip individual files and move them into a 'data' folder to use this function.
    Args:
        acq_perf (str):  'Acquisition' or 'Performance' CSV files to read

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
            "org_balance",  # ORIGINAL UPB
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
            "upc_balance",  # CURRENT BALANCE
            "loan_age",
            "months_to_maturity",  # REMAINING MONTHS TO LEGAL MATURITY
            "adj_months_to_maturity",  # ADJUSTED MONTHS TO MATURITY
            "maturity_date",
            "msa",  # METROPOLITAN STATISTICAL AREA
            "delinquency_status",  # CURRENT LOAN DELINQUENCY STATUS
            "modification_flag",  # MODIFICATION FLAG
            "zero_balance_code",  # ZERO BALANCE CODE
            "zero_balance_date",  # ZERO BALANCE EFFECTIVE DATE
            "last_paid_installment_date",  # LAST PAID INSTALLMENT DATE
            "foreclosure_date",  # FORECLOSURE DATE

            "disposition_date",  # DISPOSITION DATE
            "foreclosure_costs",  # FORECLOSURE COSTS
            "property_repair_costs",  # PROPERTY PRESERVATION AND REPAIR COSTS
            "recovery_costs",  # ASSET RECOVERY COSTS
            "misc_costs",  # MISCELLANEOUS HOLDING EXPENSES AND CREDITS
            "tax_costs",  # ASSOCIATED TAXES FOR HOLDING PROPERTY
            "sale_proceeds",  # NET SALE PROCEEDS
            "credit_enhancement_proceeds",  # CREDIT ENHANCEMENT PROCEEDS
            "repurchase_proceeds",  # REPURCHASE MAKE WHOLE PROCEEDS
            "other_foreclosure_proceeds",
            "non_interest_bearing_balance",
            "principal_forgiveness_balance",
            "make_whole_flag",  # REPURCHASE MAKE WHOLE PROCEEDS FLAG
            "foreclosure_writeoff",  # FORECLOSURE PRINCIPAL WRITE-OFF AMOUNT
            "activity_flag"  # SERVICING ACTIVITY INDICATOR
            ]
        }

    exclude_cols = [
        "first_payment_date",
        "servicer_name",  # from Performance also in Acquisition as Seller
        "zip",  # only 3 digit codes in Acquisition and possible errors in input as there are 1 and 2 digit codes,
        # more useful with 'msa' in Performance
        "maturity_date",  # can be calculated from "Reporting Date" and "Months to Maturity"
        ]

    use_idx = [i for i, col in enumerate(HEADERS[acq_perf]) if col not in exclude_cols]
    if acq_perf == "Performance":
        use_idx = use_idx[:-15] + [HEADERS[acq_perf].index("make_whole_flag")]
        use_idx.sort()

    df = []
    for q in range(1, 5):  # For the 4 Quarters of 2018
        df.append(pd.read_csv(os.path.join(module_path, f'data/{acq_perf}_2018Q{q}.txt'), sep='|',
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


def preprocess(acquisition_df=None, performance_df=None):
    """
    Run this code to preprocess the data that will preprocess the data by joining Acquisition and Performance and
    classifying the Delinquent Loans and Current Loans, then split and save the data into 'train.csv' and 'test.csv'
    See full analysis in EDA_JLin.ipynb
    Features:
    Targets:
    """
    # create a new feature with loans up to the point of either being delinquent or Dec 2018/2019
    #
    if acquisition_df is None and performance_df is None:
        acquisition_df = read_csv('Acquisition')
        performance_df = read_csv('Performance')

    # Drop State Codes with 'PR','GU', and 'VI' from both Acquisition and Performance.
    acq_cols = ['id', 'org_balance', 'interest_rate', 'ltv', 'borrower_count', 'score', 'loan_purpose', 'dti',
                                     'occupancy_type', 'property_type']
    perf_cols = ['id','upc_balance', 'loan_age', 'months_to_maturity','payment_amounts','delinquency_bool']
    acquisition_df.property_state = acquisition_df.property_state.where(
        ~acquisition_df.property_state.isin(['PR', 'GU', 'VI']))
    acquisition_df = acquisition_df.dropna(subset=['property_state'])
    acquisition_df['score'] = acquisition_df[['borrower_score', 'coborrower_score']].mean(axis=1)
    acquisition_df = acquisition_df[acq_cols].dropna(axis=0, subset=['score', 'dti'])

    performance_df.drop(columns='interest_rate')
    performance_df.id = performance_df.id.where(performance_df.id.isin(acquisition_df.id))
    performance_df = performance_df.dropna(subset=['id'])

    performance_df['reporting_period'] = pd.to_datetime(performance_df['reporting_period'])
    performance_df.delinquency_status = performance_df.delinquency_status \
        .fillna(-99).mask(performance_df.delinquency_status == 'X', -99).astype('int8')
    performance_df['delinquency_bool'] = performance_df.delinquency_status.map(lambda x: 1 if x > 0 else 0)

    # Backfill NaN for Balance for the first 5-6 months
    performance_df.upc_balance = performance_df.upc_balance.fillna(method='bfill')
    performance_df['payment_amounts'] = - performance_df.groupby('id').upc_balance.diff()

    performance_df = performance_df[performance_df.loan_age > 0]

    # Fully-paid \[zero_balance_code = 1; make_whole_flag (Repurchase Make Whole Proceeds Flag) = 'N'\]
    # RealEstateOwned \[zero_balance_code = 9 \]
    fully_paid = performance_df[
        (performance_df.zero_balance_code.isin([1, 9])) & (performance_df.make_whole_flag == 'N')]

    # Foreclosure \[zero_balance_code = 3,6,15]
    defaulted = performance_df[performance_df.zero_balance_code.isin([3, 6, 15])]

    # DELINQUENT
    delinq_ids = performance_df[performance_df['delinquency_bool'] == 1].groupby('id').nth(0).reset_index().id
    delinq_loans = performance_df[performance_df.id.isin(delinq_ids)]

    before_deliq_rows = delinq_loans[delinq_loans.groupby('id').delinquency_status.diff(-1) == -1].groupby('id').nth(0) \
        .reset_index()
    before_deliq_rows.delinquency_bool = 1
    current_loans = performance_df[performance_df.delinquency_status == 0].groupby('id').nth(-1).reset_index()
    current_loans = current_loans[
        ~current_loans.id.isin(delinq_ids) & ~current_loans.id.isin(defaulted) & ~current_loans.id.isin(
            fully_paid)]  # gives the same number of rows

    data = pd.concat([before_deliq_rows, current_loans], sort=False, ignore_index=True)

    data = data[perf_cols]  # drop columns with all NaNs
    data = data.dropna(axis=0, subset=['payment_amounts'])

    data2 = pd.merge(acquisition_df, data, on='id')

    # data2.to_csv('cleaned_data.csv.zip')
    # split test_train
    train, test = train_test_split(data2, test_size=0.33, stratify=data2.delinquency_bool, random_state=2020)
    train.to_csv(os.path.join(module_path, 'data/cleaned_train_data.csv.zip'), index=False)
    test.to_csv(os.path.join(module_path, 'data/cleaned_test_data.csv.zip'), index=False)


def load_clean_data(file):
    """
    Loads cleaned data zipped csv files  "cleaned_test_data.csv.zip" or "cleaned_train_data.csv.zip"
    Returns as X (features) or y (targets).

    Args:
        file(str): str of "test" or "train"

    Returns:
        X (pandas.DataFrame):
        y (pandas.Series):

    """
    df = pd.read_csv(os.path.join(module_path, f'data/cleaned_{file}_data.csv.zip'))
    X = df.drop(columns=['delinquency_bool'])
    y = df.delinquency_bool
    return X, y
