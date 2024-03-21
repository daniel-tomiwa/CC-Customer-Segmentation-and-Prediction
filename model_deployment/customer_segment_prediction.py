
from flask import Flask, render_template, request, flash
import numpy as np
import joblib
import os


app=Flask(__name__) #creates the app to process the user input
#Configure the app
app.logger.setLevel('INFO')
app.secret_key = "amakuru"


#Define the functions that represent the actions that occur as the user interacts with the app.
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def predict():
    """'PURCHASES', 'CASH_ADVANCE', 'PURCHASES_FREQUENCY',
       'CASH_ADVANCE_FREQUENCY', 'CASH_ADVANCE_TRX', 'PURCHASES_TRX'
    """
    if request.method =='POST':
        try:
            #Retrieve the form inputs
            PURCHASES=float(request.form['PURCHASES'])
            CASH_ADVANCE=float(request.form['CASH_ADVANCE'])
            PURCHASES_FREQUENCY=float(request.form['PURCHASES_FREQUENCY'])
            CASH_ADVANCE_FREQUENCY=float(request.form['CASH_ADVANCE_FREQUENCY'])
            CASH_ADVANCE_TRX=float(request.form['CASH_ADVANCE_TRX']) 
            PURCHASES_TRX=float(request.form['PURCHASES_TRX'])

            #Consolidate the inputs
            input_args=[PURCHASES, CASH_ADVANCE, PURCHASES_FREQUENCY, CASH_ADVANCE_FREQUENCY, CASH_ADVANCE_TRX, PURCHASES_TRX]
            input_arr=np.array(input_args)
            inputs=input_arr.reshape(1,-1)# 1 row, numpy with suggest the number of columns
            #load the saved model
            model = joblib.load("models\SVC_selected_features.joblib")
            input_scaler = joblib.load(os.path.join("models","cc_standard_scaler.joblib"))
            scaled_inputs = input_scaler.transform(inputs)
            print(scaled_inputs)
            result=model.predict(scaled_inputs)
            print(result)
            #Transform result to human readable
            if int(result)== 1:
                prediction ='High_Risk'
                color_signal='red'
            else:
                prediction ='Low_Risk'
                color_signal='green'
                
            #Populate flashed messages
            flash(prediction)
            flash(color_signal)

        except ValueError:
            return "Error: Values not valid."
    return render_template('predict.html', prediction=prediction, color_signal=color_signal)

if __name__=='__main__':
    app.run(host='localhost', port=1887, debug=True)