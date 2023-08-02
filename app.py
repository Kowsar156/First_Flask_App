from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shikhi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




class ShikhiFan(db.Model):
    serial_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    uid = db.Column(db.String(100), nullable=False)
    date_craeted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.serial_no} - {self.name}"
    



@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        fan = ShikhiFan(name=request.form['name'], uid=request.form['uid'])
        db.session.add(fan)
        db.session.commit()
    fans = ShikhiFan.query.all()
    return render_template('index.html', fans = fans)




@app.route('/update/<int:serial_no>', methods=['GET', 'POST'])
def update(serial_no):
    if request.method == 'POST':
        fan = ShikhiFan.query.filter_by(serial_no=serial_no).first()
        fan.name = request.form['name']
        fan.uid = request.form['uid']
        db.session.add(fan)
        db.session.commit()
        return redirect('/')
    fan = ShikhiFan.query.filter_by(serial_no=serial_no).first()
    return render_template('update.html', fan = fan)





@app.route('/delete/<int:serial_no>', methods=['GET', 'POST'])
def delete(serial_no):
    fan = ShikhiFan.query.filter_by(serial_no=serial_no).first()
    db.session.delete(fan)
    db.session.commit()
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True, port=8000)