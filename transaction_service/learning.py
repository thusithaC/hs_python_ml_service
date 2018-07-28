
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transaction_service.datasource import get_all_transactions, get_training_data, create_df
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

import json
import pickle

TMP_DIR = '/var/tmp/'
GENERIC_MODEL_FILE = TMP_DIR + 'generic.pickle'
GENERIC_LE_FILE = TMP_DIR + 'le.pickle'
GENERIC_OHE_FILE = TMP_DIR + 'ohe.pickle'

def test(request):
    return HttpResponse("Hello")

def transactions(request):
    return JsonResponse(get_all_transactions())

def train_generic_model(request):
    df_data = create_df()
    X, y, le, ohe = get_training_data(df_data)
    rf = RandomForestRegressor()
    clf = rf.fit(X, y)
    pickle.dump(clf, open(GENERIC_MODEL_FILE, 'wb'))
    pickle.dump(le, open(GENERIC_LE_FILE, 'wb'))
    pickle.dump(ohe, open(GENERIC_OHE_FILE, 'wb'))
    return HttpResponse("Done")

@csrf_exempt
def get_generic_prediction(request):
    body_unicode = request.body.decode('utf-8')
    print(body_unicode)
    content = json.loads(body_unicode)
    content_aslist = [x['transaction'] for x in content]
    df = pd.DataFrame(content_aslist)
    df['day_of_week'] = df['transactionDay'] % 7
    df['month'] = (df['transactionDay'] % 30) % 12
    clf, le, ohe = get_generic_model()
    if le is None or ohe is None or clf is None:
        response = JsonResponse({'status': 'false', 'message': 'Trained models not found'})
        response.status_code = 500
        return response
    df['category_encoded'] = le.transform(df['category'])
    X = ohe.transform(df['category_encoded'].values.reshape(-1, 1)).toarray()
    category_cols = ["category_" + str(int(i)) for i in range(X.shape[1])]
    df_ohe = pd.DataFrame(X, columns=category_cols)
    df_encoded = pd.concat([df, df_ohe], axis=1)
    cols_selected = ['day_of_week', 'month']
    cols_selected.extend(category_cols)
    X = df_encoded[cols_selected]
    pred = clf.predict(X)
    return JsonResponse({"result": list(pred)})

def get_generic_model():
    clf = None
    le = None
    ohe = None
    try:
        clf = pickle.load(open(GENERIC_MODEL_FILE, 'rb'))
        le = pickle.load(open(GENERIC_LE_FILE, 'rb'))
        ohe = pickle.load(open(GENERIC_OHE_FILE, 'rb'))
    except IOError:
        print("Error: can\'t find file or read data")
    return clf, le, ohe
