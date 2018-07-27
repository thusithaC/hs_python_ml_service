
import requests

GRAPHQL_BASE_URI = "https://ancient-oasis-74228.herokuapp.com/"
#req_all_transactions = { "query" : "{ viewer  { login } }" }

def get_all_transactions():
    req_all_transactions = {"query": "query { allTransactions {transactionId accountId transactionDay category transactionAmount}}"}
    r = requests.post(url=GRAPHQL_BASE_URI, json=req_all_transactions)
    return r.text
