from flask import Blueprint
from controllers.LevelController import get_levels, get_level , update_level,delete_level, add_level
level_bp = Blueprint('Level_bp', __name__)

#get all level
level_bp.route('/api/level',methods=['GET'])(get_levels)

#get level by id
level_bp.route('/api/level/<int:id>',methods=['GET'])(get_level)

#new level
level_bp.route('/api/level',methods=['POST'])(add_level)

#update level (PUT)
level_bp.route('/api/level/<int:id>',methods=['PUT'])(update_level)

#delete level
level_bp.route('/api/level/<int:id>',methods=['DELETE'])(delete_level)
  
