#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False



migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    baked_good =[]
    if request.method == 'GET':
       
        for backed in BakedGood.query.all():
            backed_dict = backed.to_dict()
            baked_good.append(backed_dict)
            
        response = make_response(
            jsonify(baked_good), 201, {"Content-Type": "application/json"}
        )
        return response

    elif request.method == 'POST':
        new_baked = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id"),
            
        )

        db.session.add(new_baked)
        db.session.commit()

        backed_dict = new_baked.to_dict()

        response = make_response(
            jsonify(backed_dict),
            201
        )

        return response 
    
@app.route('/baked_goods/<int:id>', methods=['DELETE']) 
def baked_goodsw(id):
    baked_good = BakedGood.query.filter_by(id=id).first()
    if request.method == 'DELETE':        
        
        db.session.delete(baked_good)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."    
        }

        response = make_response(
            jsonify(response_body),
            200
        )
        return response
           
    
@app.route('/bakeries/<int:id>', methods=['GET','PATCH'], endpoint='update_bakery')
def bakeries(id):
    
    bakes = Bakery.query.filter_by(id=id).first() 
       

    if not bakes:
        return jsonify({"message": "Bakery not found"}), 404
    
    if request.method == 'GET':        
        
        bake_dict= bakes.to_dict()
        response = make_response(
            jsonify(bake_dict),
            200
        )
        return response
               
    elif request.method == 'PATCH': 
        for attr in request.form:
            setattr(bakes, attr, request.form.get(attr))
        db.session.add(bakes)
        db.session.commit()
        bakery_dict = bakes.to_dict()
        response = make_response(bakery_dict, 200)
        return response
 
         
            
            


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()

    response = make_response(
        bakery_serialized,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
