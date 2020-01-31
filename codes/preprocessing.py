import pandas as pd


def read_csv(acq_perf='Acquisition'):
    """
    Args:
        acq_perf (str):  'Acquisition' or 'Performance' CSV files to read

        Note - Please download the data from https://www.fanniemae.com/portal/funding-the-market/data/loan-performance-data.html
                    Then unzip individual files and move them into a 'data' folder to use this function.
    Returns:
        Pandas DataFrame from either 'Acquisition' or 'Performance' CSV file
    """
    # Column Names and descriptions (in comments)
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
            "zip",  # ZIPCODE
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
            "months_to_maturity",
            "maturity_date",
            "msa",  # METROPOLITAN STATISTICAL AREA
            "delinquency_status",
            "modification_flag",
            "zero_balance_code",
            "zero_balance_date",
            "last_paid_installment_date",
            "foreclosure_date",
            "disposition_date",
            "foreclosure_costs",
            "property_repair_costs",
            "recovery_costs",
            "misc_costs",
            "tax_costs",
            "sale_proceeds",
            "credit_enhancement_proceeds",
            "repurchase_proceeds",
            "other_foreclosure_proceeds",
            "non_interest_bearing_balance",
            "principal_forgiveness_balance",
            "make_whole_flag",  # REPURCHASE MAKE WHOLE PROCEEDS FLAG
            "foreclosure_writeoff",  # FORECLOSURE PRINCIPAL WRITE-OFF AMOUNT
            "activity_flag",  # SERVICING ACTIVITY INDICATOR
            ]
        }

    df = []
    for q in range(1, 5):  # For the 4 Quarters of 2018
        df.append(pd.read_csv(f'{acq_perf}_2018Q{q}.txt', sep='|', names=HEADERS[acq_perf],
                              low_memory=False))
    return pd.concat(df, axis=0, ignore_index=True)