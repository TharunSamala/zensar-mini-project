import requests 
from flask import Flask,request,render_template
import json
import sqlite3
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db=SQLAlchemy(app)

#Creating database model
class city(db.Model):
	id =db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(50),nullable=False)

@app.route('/',methods=['GET','POST'])
def index():
	if request.method=='POST':
		new_city=request.form.get('city')
		if new_city:
		
			new_city_obj=city(name=new_city)
			db.session.add(new_city_obj)
			db.session.commit()


	cities=city.query.all()


	url="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=799ace38ff6968b986e21646d53bb9bf"
	
	
	weather_data=[]
	for cit in cities:
		r=requests.get(url.format(cit.name)).json()	

		weather={
			'city' : cit.name,
			'temperature' : round(r['main']['temp']),
			'description' : r['weather'][0]['description'],
			'icon' : r['weather'][0]['icon'],
			}

		weather_data.append(weather)

	return render_template('UI.html',weather_data=weather_data)


if __name__=="__main__":
	app.run(debug=True,host="localhost",port=8004)











