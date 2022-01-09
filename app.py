from flask import Flask, request, render_template, url_for, redirect
import requests
import pickle
from twilio.rest import Client
#from twilio import base.exceptions.TwilioRestException

filename = 'model.pkl'
clf = pickle.load(open(filename, 'rb'))
cv = pickle.load(open("transform.pkl", "rb"))
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.form['q']
        phoneno = request.form["phone"]
        phoneno = "+918460830860"  # verifiednumber needed in free plan
        data = [text]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)
        var = str(my_prediction[0])
# ml code here

        if var == 0:
            var = "happy"
        else:
            var = "sad"

    # spotify code here
        client_id = '243d607748094783bffa1d52780e1f11'
        client_secret = 'fe26e826eefc4b3a8a11e3b792b2c87e'
        auth_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }
        auth_response = requests.post(auth_url, data=data)
        access_token = auth_response.json().get('access_token')
        search_url = 'https://api.spotify.com/v1/search?q=' + var + "&type=playlist&limit=1"
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = requests.get(search_url, headers=headers).json()
        global var2
        var2 = response['playlists']['items'][0]['external_urls']['spotify']

# twilio code here
        account_sid = "AC208602ce83ba2f9fb6725044be1ed619"
        auth_token = "6e4eb7ff600a7688b19f92cefb05233a"
        client = Client(account_sid, auth_token)

        client.messages.create(
                to=phoneno,
                from_="+18508163920",
                body=var2
                )

        return redirect(url_for("test"))

    else:
        return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/success")
def test():
    return render_template('success.html',var = var2)


if __name__ == "__main__":
    app.run(debug=True)
