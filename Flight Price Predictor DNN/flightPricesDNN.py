import json
import math
import pandas as pd
with open('master.json') as data_file:    
    data = json.load(data_file)

pretty_data = pd.DataFrame(data)
pretty_data= pretty_data.rename(columns = {'consult date':'request date'})
pretty_data.head()

just_flightDuration = pretty_data["flight duration"]
new_fD = []
for i in range(0,len(just_flightDuration)):
    temp = just_flightDuration[i].split()
    total_time = 0
    
    for j in range(0, math.ceil(len(temp)/2)):   
        if j == 0: 
            total_time += 1440*float(temp[j])
        elif j == 1:
            total_time += 60*float(temp[2*j])
        else:
            total_time += float(temp[2*j])
    new_fD.append(total_time)

new_flightD = pd.DataFrame(data= new_fD,columns=['flight duration']);

depart_dates = pretty_data['departure date']
request_dates = pretty_data['request date']
from datetime import datetime
date_format = "%d/%m/%Y"
anticipation = []
for i in range(len(depart_dates)):
    a = datetime.strptime(depart_dates[i], date_format)
    b = datetime.strptime(request_dates[i], date_format)
    delta = a - b
    anticipation.append(abs(delta.days))
pretty_data = pretty_data.drop(['departure date','request date'],axis = 1)

pretty_data['days of anticipation']= pd.DataFrame(data = anticipation, columns=['days of anticipation'])
pretty_data['flight duration'] = new_fD

cols_to_norm = ['flight duration']
pretty_data[cols_to_norm] = pretty_data[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

clean_stops = {"stops": {"4 Stop": 4, "3 Stop": 3, 
                         "2 Stop": 2, "1 Stop": 1, 
                         "Nonstop": 0}}
pretty_data.replace(clean_stops, inplace=True)

pretty_data = pretty_data.drop('airline',axis = 1)

pretty_data = pretty_data.drop('arrival',axis = 1)
pretty_data = pretty_data.drop('departure', axis = 1)
pretty_data.columns = pretty_data.columns.str.replace('flight duration', 'flight_duration')
pretty_data.columns = pretty_data.columns.str.replace('ticket price', 'ticket_price')
pretty_data.columns = pretty_data.columns.str.replace('days of anticipation', 'days_of_anticipation')
pretty_data['ticket_price']=pretty_data['ticket_price'].astype('float')
pretty_data['days_of_anticipation']=pretty_data['days_of_anticipation'].astype('float')
pretty_data['stops']=pretty_data['stops'].astype('float')


import tensorflow as tf

x_data = pretty_data.drop('ticket_price', axis = 1)
y_val = pretty_data['ticket_price']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x_data, y_val, test_size=0.3)


flight_duration = tf.feature_column.numeric_column('flight_duration')
stops = tf.feature_column.numeric_column('stops')
doa = tf.feature_column.numeric_column('days_of_anticipation')

feat_cols = [flight_duration,stops,doa]

input_func = tf.estimator.inputs.pandas_input_fn(x=X_train,y=y_train,
                                                 batch_size=100,
                                                 num_epochs=1000,
                                                 shuffle=True)
model = tf.estimator.DNNRegressor(hidden_units = [4,4,4],
                                  feature_columns= feat_cols)
model.train(input_fn = input_func, steps = 100000)
predict_input_func = tf.estimator.inputs.pandas_input_fn(x = X_test,
                                                        batch_size = 100,
                                                        num_epochs= 1,
                                                        shuffle=False)

pred_gen = model.predict(predict_input_func)
X_test.head()
predictions = list(pred_gen)
for pred in predictions: 
    final_preds.append(pred['predictions'])
from sklearn.metrics import mean_squared_error
error = mean_squared_error(y_test, final_preds)**0.5

avg_error = error/(30)
print(avg_error)