
import requests
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

GRAPHQL_BASE_URI = 'https://ancient-oasis-74228.herokuapp.com/graphql'
#req_all_transactions = { "query" : "{ viewer  { login } }" }


def splitDataFrameList(df, target_column):
    row_accumulator = []
    def splitListToRows(row):
        split_row = row[target_column]
        for s in split_row:
            new_row = row.to_dict()
            new_row[target_column] = s
            row_accumulator.append(new_row)

    df.apply(splitListToRows, axis=1)
    new_df = pd.DataFrame(row_accumulator)
    return new_df


def get_all_customers():
    req_all_customers = {"query": "query {allCustomers {customerId accounts}}"}
    r = requests.post(url=GRAPHQL_BASE_URI, json=req_all_customers)
    return r.json()

def get_all_transactions():
    req_all_transactions = {"query": "query { allTransactions \
    {transactionId accountId transactionDay category transactionAmount}}"}
    r = requests.post(url=GRAPHQL_BASE_URI, json=req_all_transactions)
    return r.json()


def create_df():
    data_transactions = get_all_transactions()
    data_customers = get_all_customers()
    transactions = data_transactions["data"]["allTransactions"]
    df_transactions = pd.DataFrame(transactions)
    df_customers_tmp = pd.DataFrame(data_customers['data']['allCustomers'])
    df_customers = splitDataFrameList(df_customers_tmp, target_column='accounts')
    df_data = df_transactions.join(df_customers.set_index('accounts'), on='accountId')
    df_data['day_of_week'] = df_data['transactionDay'] % 7
    df_data['month'] = (df_data['transactionDay'] % 30) % 12
    return df_data

def get_training_data(df_data):
    df_data.index = range(0, df_data.shape[0])
    le = LabelEncoder()
    ohe = OneHotEncoder()
    le.fit(df_data['category'])
    df_data['category_encoded'] = le.transform(df_data['category'])
    data_ohe = ohe.fit_transform(df_data['category_encoded'].values.reshape(-1,1)).toarray()
    category_cols = ["category_"+str(int(i)) for i in range(data_ohe.shape[1])]
    df_ohe = pd.DataFrame(data_ohe, columns=category_cols)
    df_data_encoded = pd.concat([df_data, df_ohe], axis=1)
    cols_selected = ['day_of_week', 'month']
    cols_selected.extend(category_cols)
    X = df_data_encoded[cols_selected]
    y = df_data_encoded['transactionAmount']
    return X, y, le, ohe





