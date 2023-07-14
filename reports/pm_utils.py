from assist_dash.models import Product, Sale, Sale_Detail
from django.db.models import Sum
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def prepare_sales_data():
    sales_data1 = Sale_Detail.objects.values('Item_Quantity', 'product', 'branch', 'sale')
    sales_data2 = Product.objects.values('Product_Name', 'Product_Price')
    pricing_data = []

    for sale in sales_data1:
        product = sale['product']
        matching_product = next((item for item in sales_data2 if item['Product_Name'] == product), None)
        if matching_product:
            pricing_data.append(matching_product['Product_Price'])
        else:
            pricing_data.append(None)

    data_list = list(sales_data1)
    sales_df = pd.DataFrame.from_records(data_list)

    for i, item in enumerate(data_list):
        item['pricing_data'] = pricing_data[i]

    return sales_df

def train_lstm_model(X_train, y_train, num_units, activation_func, num_epochs, batch_size):
    model = Sequential()
    model.add(LSTM(num_units, activation=activation_func, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, y_train, epochs=num_epochs, batch_size=batch_size)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    return mse, mae, rmse