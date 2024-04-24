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




api = Api(merchant_id=1396424,
          secret_key='test')
checkout = Checkout(api=api)


@app.route('/payment', methods=['POST'])
def payment():

    item_id = request.form.get('el.id')
    if 'el.id' not in request.form:
        return 'Не передан el.id'

    item = Item.query.get(item_id)

    payment_data = {
        'amount': item.price,
        'currency': 'RUB',
        'description': item.title,
        'product_id': item.id
    }
    try:
        url = checkout.url(payment_data).get('checkout_url')
        return redirect(url)
    except Exception as e:
        return 'Ошибка при создании ссылки на платежную страницу: {}'.format(str(e))



if __name__=='__main__':
    app.run(debug=True)

