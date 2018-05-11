import json
import math
import pandas as pd
with open('master.json') as data_file:    
    data = json.load(data_file)

#Make data a pandas DataFrame for simple data manipulation
pretty_data = pd.DataFrame(data)
pretty_data= pretty_data.rename(columns = {'consult date':'request date'})
pretty_data.head()

#Transforming flight duration to minutes
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

#Transforming departure date and request date columns into "days of anticipation" one
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

#Normalize flight duration column
cols_to_norm = ['flight duration']
pretty_data[cols_to_norm] = pretty_data[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))


clean_stops = {"stops": {"4 Stop": 4, "3 Stop": 3, 
                         "2 Stop": 2, "1 Stop": 1, 
                         "Nonstop": 0}}
pretty_data.replace(clean_stops, inplace=True)

#Drop columns with no importance to predict flight prices
pretty_data = pretty_data.drop('airline',axis = 1)
pretty_data = pretty_data.drop('arrival',axis = 1)
pretty_data = pretty_data.drop('departure', axis = 1)

#Replace names with readable names for DNNRegressor
pretty_data.columns = pretty_data.columns.str.replace('flight duration', 'flight_duration')
pretty_data.columns = pretty_data.columns.str.replace('ticket price', 'ticket_price')
pretty_data.columns = pretty_data.columns.str.replace('days of anticipation', 'days_of_anticipation')
pretty_data.head()
pretty_data['ticket_price']=pretty_data['ticket_price'].astype('float')
pretty_data['days_of_anticipation']=pretty_data['days_of_anticipation'].astype('float')
pretty_data['stops']=pretty_data['stops'].astype('float')

#Creating Dense Neural Network Regression
import tensorflow as tf

x_data = pretty_data.drop('ticket_price', axis = 1)
y_val = pretty_data['ticket_price']


#Create train and test sets

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x_data, y_val, test_size=0.3)

#Setting features as numerical values
flight_duration = tf.feature_column.numeric_column('flight_duration')
stops = tf.feature_column.numeric_column('stops')
doa = tf.feature_column.numeric_column('days_of_anticipation')
feat_cols = [flight_duration,stops,doa]

#Creating input for model 
input_func = tf.estimator.inputs.pandas_input_fn(x=X_train,y=y_train,
                                                 batch_size=4,
                                                 num_epochs=1000,
                                                 shuffle=True)

#Creating model with 4 hidden layers, each one connected to every other neuron
model = tf.estimator.DNNRegressor(hidden_units = [4,4,4],
                                  feature_columns= feat_cols)
#Training model with data from pretty_data 
model.train(input_fn = input_func, steps = 100000)

#Making predictions with X_test data, we don't set the Y value (y_test) as we know thats the variable we want to predict
predict_input_func = tf.estimator.inputs.pandas_input_fn(x = X_test,
                                                        batch_size = 10,
                                                        num_epochs= 1,
                                                        shuffle=False)
#Creating predictions
pred_gen = model.predict(predict_input_func)
predictions = list(pred_gen)
final_preds = []
#Add predictions to a list
for pred in predictions: 
    final_preds.append(pred['predictions'])
from sklearn.metrics import mean_squared_error

#Caluclate the RMSE
error = mean_squared_error(y_test, final_preds)**0.5

#Calculate Average error in flight price predictions
avg_error = error/len(X_test)
print(final_preds)
print("Error promedio en predicción de vuelo: $",avg_error)


