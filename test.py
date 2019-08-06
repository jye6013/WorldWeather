from flask import Flask, render_template, request
import requests
import os

IMAGE_FOLDER = os.path.join('static', 'img')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

clear_sky = "01d@2x.png"
few_clouds = "02d@2x.png"
scattered_clouds = "03d@2x.png"
broken_clouds = "04d@2x.png"
shower_rain = "09d@2x.png"
rain = "10d@2x.png"
thunderstorm = "11d@2x.png"
snow = "13d@2x.png"
mist = "50d@2x.png"
temp_img = ""

@app.route('/temp', methods=['POST'])
def temperatureInfo():
    #if request.method == 'POST':
    city = request.form['zip']
    #r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=22a637dc3c929c15174e767346d84436')
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+',us&appid=22a637dc3c929c15174e767346d84436')
    json_object = r.json()
    #r_2 = requests.get('http://api.openweathermap.org/data/2.5/box/city?bbox=10,33,67,11,10,us&appid=22a637dc3c929c15174e767346d84436')
    #json_object_2 = r_2.json()
    #r_3 = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=Guangzhou&apikey=22a637dc3c929c15174e767346d84436')
    #json_object_3 = r_3.json()
    #sampleData =  json_object_2['list'][0]['id']
    location = getLocation(json_object)
    desc = getDescription(json_object)
    temp_img = getTempImg(desc)
    low_temp, mid_temp, high_temp = getTemperatures(json_object)
    windSpeed = getWindSpeed(json_object)
    humidity = getHumidity(json_object)
    coordinates = getCoordinates(json_object)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], temp_img)
    #return json_object_3
    return render_template('temp.html', mid_temp=mid_temp, location=location, desc=desc, low_temp=low_temp,high_temp=high_temp, windSpeed=windSpeed, humidity=humidity, coordinates=coordinates, temperature_image=full_filename, image_name=temp_img)
    #return render_template('index.html')

def getLocation(json_object):
    return str(json_object['name'])    

def getDescription(json_object):
    return str(json_object['weather'][0]['description'])

def getTemperatures(json_object):
    temp_k_low = float(json_object['main']['temp_min'])
    temp_k_mid = float(json_object['main']['temp'])
    temp_k_high = float(json_object['main']['temp_max'])
    temp_f_low = getTempFarenheit(temp_k_low)
    temp_f_mid = getTempFarenheit(temp_k_mid)
    temp_f_high = getTempFarenheit(temp_k_high)
    return round(temp_f_low), round(temp_f_mid), round(temp_f_high)

def getTempFarenheit(temp):
    temp_in_f = (temp - 273.15) * 1.8 + 32
    return temp_in_f

def getTempImg(desc):
    if desc == "clear sky":
        return clear_sky
    elif desc == "few clouds":
        return few_clouds
    elif desc == "scattered clouds":
        return scattered_clouds
    elif desc == "broken clouds":
        return broken_clouds
    elif desc == "shower rain":
        return shower_rain
    elif desc == "rain":
        return rain
    elif desc == "thunderstorm":
        return thunderstorm
    elif desc == "snow":
        return snow
    elif desc == "mist":
        return mist
    else:
        return ""

def getWindSpeed(json_object):
    return json_object['wind']['speed']

def getHumidity(json_object):
    return json_object['main']['humidity']

def getCoordinates(json_object):
    return json_object['coord']['lon'], json_object['coord']['lat']

@app.route('/')
def index():
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(debug=True)