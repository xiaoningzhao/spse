import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from stock import get_stock, get_current_stock_value, get_stock_value_time, \
    get_stock_price_by_date
from flask_marshmallow import Marshmallow
from hashlib import md5

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost:3306/spse'
db = SQLAlchemy(app)
ma = Marshmallow(app)


# login
@app.route('/login', methods=['POST'])
def login():
    try:
        username = str(request.form.get('username')).strip()
        password = md5(str(request.form.get('password')).strip().encode()).hexdigest()
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({'message': 'User does not exist'})
        else:
            if user.password != password:
                return jsonify({'message': 'Wrong password'})
            else:
                user_schema = UserSchema()
                return user_schema.dumps(user)
    except Exception as e:
        return jsonify({'message': str(e)})


# register
@app.route('/register', methods=['POST'])
def register():
    try:
        username = str(request.form.get('username')).strip()

        check_user = User.query.filter_by(username=username).first()
        if check_user is None:
            password = md5(str(request.form.get('password')).strip().encode()).hexdigest()
            user = User(user_id=None, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'User name already exists'})
    except Exception as e:
        return jsonify({'message': str(e)})


# retrieve all users
@app.route('/user')
def get_all_users():
    user_schema = UserSchema(many=True)
    return user_schema.dumps(User.query.all())


# retrieve user's portfolio
@app.route('/user/portfolio', methods=['GET'])
def get_user_portfolio():
    try:
        user_id = str(request.args.get('user_id')).strip()
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()
        portfolio_schema = PortfolioSchema(many=True)
        return portfolio_schema.dumps(portfolio)
    except Exception as e:
        return jsonify({'message': str(e)})


# retrieve all strategies
@app.route('/strategy/all', methods=['GET'])
def get_strategy_name():
    try:
        strategy = Strategy.query.with_entities(Strategy.strategy).distinct().all()
        strategy_schema = StrategySchema(many=True)
        return strategy_schema.dumps(strategy)
    except Exception as e:
        return jsonify({'message': str(e)})


# retrieve tickers from one strategy
@app.route('/strategy', methods=['GET'])
def get_strategy_tickers():
    try:
        strategy_name = str(request.args.get('strategy')).strip()
        strategy = Strategy.query.filter_by(strategy=strategy_name).all()
        strategy_schema = StrategySchema(many=True)
        return strategy_schema.dumps(strategy)
    except Exception as e:
        return jsonify({'message': str(e)})


# retrieve user's portfolio
@app.route('/myportfolio', methods=['GET'])
def get_my_portfolio():
    try:
        user_id = str(request.args.get('userId')).strip()
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()
        portfolio_schema = PortfolioSchema(many=True)
        return portfolio_schema.dumps(portfolio)
    except Exception as e:
        return jsonify({'message': str(e)})


# retrieve stock current price
@app.route('/currentprice', methods=['GET'])
def get_current_price():
    try:
        ticker = str(request.args.get('ticker')).strip()
        price = get_current_stock_value(ticker)
        return jsonify({'price': price})
    except Exception as e:
        return jsonify({'message': str(e)})


# retrieve user's portfolio
@app.route('/myportfoliovalue', methods=['GET'])
def get_my_portfolio_value():
    try:
        user_id = str(request.args.get('userId')).strip()
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()
        amount = 0
        for p in portfolio:
            ticker = p.ticker
            price = get_current_stock_value(ticker)
            value = price * p.share
            amount += value
            # print(value)
        # print(amount)
        return jsonify({'total': float(format(amount, '.2f'))})
    except Exception as e:
        return jsonify({'message': str(e)})


# retrieve user's portfolio by five days
@app.route('/myportfoliovaluetime', methods=['GET'])
def get_my_portfolio_value_by_time():
    try:
        user_id = str(request.args.get('userId')).strip()
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()

        sum_value = 0
        for p in portfolio:
            ticker = p.ticker
            values = get_stock_value_time(ticker)
            sum_value += values['Close'] * p.share

        # print(sum_value)
        return_value = []

        for index, row in sum_value.items():
            return_value.append({'time': index.strftime("%Y-%m-%d"), 'amount': row})

        # print(return_value)
        return jsonify(return_value)
    except Exception as e:
        return jsonify({'message': str(e)})


# Suggest portfolio
@app.route('/suggest', methods=['GET'])
def suggest():
    try:
        strategies = request.args.getlist('strategies')
        amount = float(request.args.get('amount'))
        date = request.args.get('date')
        strategy = db.session.query(Strategy).filter(Strategy.strategy.in_(strategies)).all()
        ratings = db.session.query(func.sum(Strategy.rating).label("ratings")).filter(Strategy.strategy.in_(strategies)).first()

        stocks = [{'ticker': '',
                   'ticker_name': '',
                   'share': 0,
                   'purchase_price': 0,
                   'amount': 0
                   }]

        strategy = sorted(strategy, key=lambda element: element.rating, reverse=True)

        leftover = amount
        for s in strategy:
            allocation = amount * (s.rating / float(ratings.ratings))
            purchase_price = get_stock_price_by_date(s.ticker, date)
            share = allocation // purchase_price
            allocation = share * purchase_price
            leftover -= allocation
            exist = False
            for stock in stocks:
                if stock['ticker'] == '':
                    stocks.clear()
                if s.ticker == stock['ticker']:
                    stock['share'] += share
                    stock['amount'] += float(format(allocation, '.2f'))
                    exist = True
                    break
            if not exist:
                stocks.append({'ticker': s.ticker,
                               'ticker_name': s.ticker_name,
                               'share': share,
                               'purchase_price': purchase_price,
                               'amount': float(format(allocation, '.2f'))
                               })

        if leftover > 0:
            for stock in stocks:
                if leftover > stock['purchase_price']:
                    extra_share = leftover // stock['purchase_price']
                    extra_amount = extra_share * stock['purchase_price']
                    stock['share'] += extra_share
                    stock['amount'] += float(format(extra_amount, '.2f'))
                    leftover -= extra_amount

        return jsonify({'leftover': float(format(leftover, '.2f')), 'portfolio': stocks})
    except Exception as e:
        return jsonify({'message': str(e)})


# save to my portfolio
@app.route('/saveportfolio', methods=['POST'])
def save_portfolio():
    try:
        req = request.get_data()
        req_data = json.loads(req)
        user_id = req_data['userId']
        portfolios = req_data['portfolio']

        previous_portfolios = Portfolio.query.filter_by(user_id=user_id).all()
        if len(previous_portfolios) != 0:
            for previous_portfolio in previous_portfolios:
                db.session.delete(previous_portfolio)
            db.session.commit()

        for portfolio in portfolios:
            p = Portfolio(user_id=user_id,
                          ticker=portfolio['ticker'],
                          ticker_name=portfolio['ticker_name'],
                          share=portfolio['share'],
                          purchase_price=portfolio['purchase_price'])
            db.session.add(p)

        db.session.commit()
        return jsonify({'message': 'success'})
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)})


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/stockhistory/')
def stock_history():
    try:
        if request.method == 'GET':
            ticker = str(request.args.get('ticker')).strip()
            return get_stock(ticker)
    except Exception as e:
        return jsonify({'message': str(e)})


# #################  Models  ########################
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password


class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    user_id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(50), primary_key=True)
    ticker_name = db.Column(db.String(255))
    share = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, ticker, ticker_name, share, purchase_price):
        self.user_id = user_id
        self.ticker = ticker
        self.ticker_name = ticker_name
        self.share = share
        self.purchase_price = purchase_price


class Strategy(db.Model):
    __tablename__ = 'strategy'
    strategy = db.Column(db.String(100), primary_key=True)
    ticker = db.Column(db.String(50), primary_key=True)
    ticker_name = db.Column(db.String(255))
    rating = db.Column(db.Integer)

    def __init__(self, strategy, ticker, ticker_name, rating):
        self.strategy = strategy
        self.ticker = ticker
        self.ticker_name = ticker_name
        self.rating = rating


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username')


class PortfolioSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'ticker', 'ticker_name', 'share', 'purchase_price')


class StrategySchema(ma.Schema):
    class Meta:
        fields = ('strategy', 'ticker', 'ticker_name', 'rating')

