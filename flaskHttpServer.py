from flask import Flask, request, jsonify


# Define the Flask app
app = Flask(__name__)

admins = {"admin" : "password"} 
subscribers = {}


@app.route('/', methods=['GET', "POST"])
def root():
    if request.methods == "POST":
        username = request.form.get("Enter Username:", "")
        password = request.form.get("Enter Password:", "")
        subscribers[username] = password
        if username in subscribers and password == subscribers[username]:
            return redirect(url_for("welcome", username= username))
     return f'''
     <body style="background-color: #e0f7fa;">
         <div style="text-align:center; margin-top: 10vh;">
             <h2>Error: Please enter some text to echo.</h2>
             <a href="{redirect(url_for("sign_up"))}">Sign up</a>
         </div>
     </body>
 ''', 400


@app.route("/sign_up", methods["GET", "POST"])
def sign_up():
    
    return 

@app.route('/list-subscribers', methods=['GET'])
def listSubscribers():
  return jsonify(subscribers)

# Windows> curl.exe -X POST -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"URI\":\"http://good.site.com\"}" http://localhost:5000/add-subscriber

@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():
  data = request.json
  name = data.get('name')
  URI = data.get('URI')
  subscribers[name] = URI
  print(f"You entered: Name={name}, Address={URI}")
  return jsonify({'message': f'You sent name: {name} and address: {URI}'})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
