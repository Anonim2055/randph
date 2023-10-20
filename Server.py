from pymongo import MongoClient
import bcrypt
from flask import Flask, request, render_template, redirect, session, jsonify
from imgup import upload as get_url
app = Flask(__name__)

try:
#check if mongoDB work
    mongo = MongoClient(host='localhost', port=27017, serverSelectionTimeoutMs=5000)
    db = mongo.randphoto
    print("MongoDb Connected")
except Exception:
    print("Unable to connect to MongoDb")


@app.route("/send_location", methods=["POST", 'GET'])
def send_location():
    try:
        if session['username']:
            print("les gooo")
    except Exception:
        return redirect('/')
    if request.method == 'GET':
        return render_template('getloc.html')
    data = request.get_json()
    session['latitude'] = data.get("latitude")
    session['longitude'] = data.get("longitude")
   # return redirect('/upload')
    if session['latitude'] is not None and session['longitude'] is not None:
        # location_data = {
        #     "latitude": latitude,
        #     "longitude": longitude
        # }
        # db.locations.insert_one(location_data)
        return jsonify({"message": "Location saved."})
    else:
        return jsonify({"error": "Error saving."})

@app.route('/home')
def home():
    return redirect('/')
@app.route('/')
def startPage():
    try:
        username = session['username']
    except Exception:
        username = None

    return render_template('home.html', username=username)

@app.route("/login", methods=['POST','GET'])
def log():
    if request.method == 'POST':
        users = db.users
        login_user = users.find_one({'name': request.form['username']})
        print("if1")
        if login_user:
            print('if2')
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect('/')
            else:
                return render_template("login.html", wrong="kek")
    return render_template("login.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'name': request.form['username'],
                'password': hashpass
            })
            session['username'] = request.form['username']
            return redirect('/')

        return 'That username already exists!'

    return render_template("signup.html")
@app.route("/logout", methods=['GET'])
def logout():
    try:
        if session['username']:
            session.pop('username', None)
    except Exception:
        return redirect('/')
    return redirect('/')

def get_params(img_url="https://i.imgur.com/C7gxqd4.png"):
    # img_url=session['img_url']
    img_data = db.images.find_one({"img_url": img_url})
    shirota=str(img_data['latitude'])
    dolgota=str(img_data['longitude'])
    print("------")
    print(shirota)
    print(dolgota)
    print("------")
    lis=(list([shirota,dolgota]))
    return lis

@app.route('/list')
def listik():

    # print(session['img_url'])
    # print(str(get_params(session['img_url'])))
    lest=get_params()
    print(lest)
    session['shirota']=lest[0]
    session['dolgota']=lest[1]
    print("________________2")
    print (session['dolgota'])
    return redirect('/ph')

@app.route('/ph', methods=['GET'])
def photo():

   return render_template("photo.html", link="https://i.imgur.com/C7gxqd4.png")

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('up.html')
    try :
        user_id = session['username']
        file = request.files['file']

        if file.filename == '':
            return {'error': 'No selected file'}, 400

        response = get_url(file)
        session['img_url'] = response['img_url']
        try:
            img_url = session['img_url']
            user_id = session['username']
            try:
                db.images.insert_one({
                    "img_url": img_url,
                    "user_id": user_id,
                    "latitude": session['latitude'],
                    "longitude": session['longitude']
                })
                # session.pop('img_url', None)
            except Exception:

                return '', 503
            page = str("user_photos/" + user_id)
            return redirect('/')
        except Exception:
            return redirect('/')
        print("response is", response)
        return redirect('/')
    except Exception:
        return redirect('/')

@app.route('/show')
def showLoc():
    dolgota=session['dolgota']
    shirota=session['shirota']
    link="https://www.openstreetmap.org/export/embed.html?bbox="+dolgota+"%2C51.06556471552332%2C"+dolgota+"%2C"+shirota+"&amp;layer=mapnik"
    return render_template("showLocation.html", link=link)

if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(host='localhost', debug=True)
