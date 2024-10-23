from flask import Blueprint
from controllers.CategoryController import get_categories, get_category , update_category,delete_category, add_category
category_bp = Blueprint('Category_bp', __name__)


#get all category
category_bp.route('/api/category',methods=['GET'])(get_categories)

#get category by id
category_bp.route('/api/category/<int:id>', methods=['GET'])(get_category)

#new category
category_bp.route('/api/category',methods=['POST'])(add_category)

#update a category (PUT)
category_bp.route('/api/category/<int:id>',methods=['PUT'])(update_category)

#delete a category (DELETE)
category_bp.route('/api/category/<int:id>',methods=['DELETE'])(delete_category)
