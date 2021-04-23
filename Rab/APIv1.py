from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [
            {
                'name': 'chair',
                'price': 1500,
            }
        ]
    }
]




#main page
@app.route('/')
def main():
    return 'Всем привет'



# POST /store -> name
@app.route('/store', methods=['POST'])
def create_store():
    data = request.get_json()
    store_name = data['name']

    for store in stores:
        if store['name'] == store_name:
            return jsonify({'message': 'store already exists'})

    store = {
        'name': store_name,
        'items': [],
    }
    stores.append(store)

    return jsonify(store)



# GET /store/<name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)

    return jsonify({'message': 'store not found'})




# GET /store
@app.route('/store')
def get_stores():
    return jsonify(stores)
        


# POST /store/<name>/item -> name, price
@app.route('/store/<string:store_name>/item', methods=['POST'])
def create_item(store_name):
    data = request.get_json()

    for store in stores:
        if store['name'] == store_name:
            item = {
                'name': data['name'],
                'price': data['price'],
            }
            store['items'].append(item)
            return jsonify(item)

    return jsonify({'message': 'store not found'})



# GET /store/<name>/item
@app.route('/store/<string:name>/item')
def get_items(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])

    return jsonify({'message': 'store not found'})



if __name__ == '__main__':
    app.run(debug=True)