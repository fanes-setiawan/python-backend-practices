from flask import jsonify, request
from models.UserModel import User
from models.LevelModel import Level
from config import db


def get_users():
    users = User.query.all()
    users_with_level =[]
    for user in users:
        #get level
        level = Level.query.get(user.level_id)
        #add details
        users_with_level.append({
            'id': user.id,
            'username': user.username,
            'fullname': user.fullname,
            'password' : user.password,
            'status': user.status,
            'level_name': level.name if level else "No Level"
        })
        
    response ={
        'status':'success',
        'data':{
            'users':users_with_level
        },
        'message':'Users retrived successfully!'
    }
    return jsonify(response),200

def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not found'}),404
    
    #get level
    level = Level.query.get(user.level_id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'fullname': user.fullname,
        'password' : user.password,
        'status': user.status,
        'level_name': level.name if level else "No Level"
    }
    
    response ={
        'status':'success',
        'data':{
            'user':user_data
        },
        'message':'User retrieved successfuly!'
    }
    return jsonify(response),200

def add_user():
    new_user_data = request.get_json()
    new_user = User(
        username = new_user_data['username'],
        password = new_user_data['password'],
        fullname = new_user_data['fullname'],
        status = new_user_data['status'],
        level_id = new_user_data['level_id']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'user added successfully!','user':new_user.to_dict()}),201

def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error':'user not found'}),404
    update_data = request.get_json()
    user.username = update_data.get('username',user.username)
    user.password = update_data.get('password',user.password)
    user.fullname = update_data.get('fullname',user.fullname)
    user.status = update_data.get('status',user.status)
    user.level_id = update_data.get('level_id',user.level_id)
    
    db.session.commit()
    return jsonify({'message' : 'user update successfully!','user' :user.to_dict()})

def patch_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not fount'}),404

    patch_data = request.get_json()
    if 'username' in patch_data:
        user.usename = patch_data['username']
        
    if 'password' in patch_data:
        user.password = patch_data['password']
        
    if 'fullname' in patch_data:
        user.fullname = patch_data['fullname']
        
    if 'status' in patch_data:
        user.status = patch_data['status']
    if 'level' in patch_data:
        level = Level.query.get(patch_data['level_id'])
        if level:
            user.level_id = patch_data['level_id']
        else:
            return jsonify({'error': 'Level not found'}),404
        
    db.session.commit()
    return jsonify({'message':'user partially updated successfully!','user':user.to_dict()})

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not fount'}),404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'user deleted successfully!'})
