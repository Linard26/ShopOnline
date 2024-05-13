from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method== 'POST':
        title = request.form['title']
        about = request.form['about']
        price = request.form['price']

        item = Item(title = title, about=about, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')

        except:
            return 'Ошибка'
    else:
        return render_template('create.html')


@app.route('/payment', methods=['POST'])
def payment():

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)


    item_id = request.form.get('el.id')
    item = Item.query.get(item_id)

    data = {
        'amount': item.price,
        'currency': 'USD',

    }
    try:
        url = checkout.url(data).get('checkout_url')
        return redirect(url)
    except Exception as e:
        return 'Ошибка при создании ссылки на платежную страницу: {}'.format(str(e))


if __name__=='__main__':
    app.run(debug=True)

