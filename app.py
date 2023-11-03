from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    query_result = data['queryResult']
    source_currency = query_result['parameters']['unit-currency'][0]['currency']
    amount = query_result['parameters']['unit-currency'][0]['amount']
    target_currency = query_result['parameters']['currency-name'][0]

    print(source_currency)
    print(amount)
    print(target_currency)

    cf = fetch_conversion_factor(source_currency,target_currency)

    final_amount = amount * cf
    final_amount = round(final_amount, 2)

    response = {
        "fulfillmentText": "{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)  #desired response message
    }
    
    return jsonify(response)

def fetch_conversion_factor(source,target):

    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=06e54116bb588aaaa92d".format(source,target)

    response = requests.get(url)
    response = response.json()

    return response['{}_{}'.format(source,target)]

if __name__ == "__main__":
    app.run(debug=True)