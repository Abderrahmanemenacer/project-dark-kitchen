from flask import Blueprint
#from home.home import get_popular_post, get_postById, getMoreReviews
from reviews.reviews import commenting_on_post
from Category.category import get_all_categories, get_all_items_of_a_category
from CartService.Cart import *
from FavoriteService.FAV import *
from home.home import *
from OrderingService.Order_for_Users import *
from SearchService.Search import *
from flask_jwt_extended import jwt_required
from kitchen.kitchen import *

routes = Blueprint('routes', __name__)

@routes.route("/api/v1/user/order-history", methods=['GET']) #works
@jwt_required()
def get_orders_user():
    return get_orders_associated_with_user()



@routes.route('/api/v1/users/place-order', methods=['GET']) #works
@jwt_required()
def place_order_user():
    return place_order()

@routes.route('/Search', methods=['GET'])# works
@jwt_required()
def Search():
    return search()
@routes.route('/favorites', methods=['GET']) # works
@jwt_required()
def GetFavorites():
    return Get_Favorites()

@routes.route('/add_favorite_API', methods=['POST']) # works
@jwt_required()
def AddFavorites():
    return Add_Favorites()

@routes.route('/remove_favorite_API', methods=['DELETE'])  # works
@jwt_required()
def RemoveFavorite():
    return Remove_Favorite()

@routes.route('/API_for_ADDING_CartItem_to_cart', methods=['POST']) #works
@jwt_required()
def ADDtoCART():
    return ADD_to_CART()

@routes.route('/API_for_Deleting_CartItem_from_cart', methods=['DELETE'])  #works
@jwt_required()
def Deleteitemfromcart():
    return Delete_item_from_cart()


@routes.route('/API_for_editing_quantity_in_cart', methods=['PUT']) # works
@jwt_required()
def editquantityANDnoteincart():
    return edit_quantity_AND_note_in_cart()


@routes.route("/get_Cart" , methods=['GET'])
@jwt_required()
def GET_CartItems () :
    return GET_ALL_CartItems()

#-----------------------------------------------------------------------------------------------------------------------




@routes.route("/api/post/<int:post_id>", methods=["GET"])
@jwt_required()
def post_byid(post_id):
    return get_postById(post_id)



# Recommendation routes
@routes.route('/recommendOfItem/<int:post_id>', methods=['GET'])
def get_item_recommendations(post_id):
    return recommend_of_item(post_id)

# Review routes
@routes.route("/api/post/reviews/<int:post_id>")
def get_More_Reviews(post_id):
    return getMoreReviews(post_id)

@routes.route('/api/post/write_review/<int:item_id>', methods=['POST'])
@jwt_required()
def write_review_route(item_id):
    return write_reviews(item_id)

@routes.route("/api/kitchen_reviews/<int:post_id>")
@jwt_required()
def get_kitchen_reviews_route(post_id):
    return get_kitchen_reviews(post_id)

# Home & Post routes
@routes.route('/api/top-items', methods=['GET'])
@jwt_required()
def get_top_items():
    return get_popular_post()

@routes.route('/api/post_par_location', methods=['GET'])
@jwt_required()
def get_items_by_location():
    return get_items_by_user_location()

# Kitchen routes
@routes.route('/api/kitchens/top-rated', methods=['GET'])
def get_best_kitchens_route():
    return get_bestKitchens()

@routes.route("/api/visit-kitchen/<int:kitchen_id>", methods=["GET"])
@jwt_required()
def visit_kitchen_route(kitchen_id):
    return visit_kitchen(kitchen_id)

@routes.route('/api/kitchen/<int:kitchen_id>/items', methods=['GET'])
@jwt_required()
def get_kitchen_items_route(kitchen_id):
    return get_kitchen_items(kitchen_id)

@routes.route('/api/write-kitchen-review/<int:kitchen_id>', methods=['POST'])
@jwt_required()
def write_kitchen_review_route(kitchen_id):
    return write_kitchen_review(kitchen_id)

# User profile routes
@routes.route('/edit-profile', methods=['PUT'])
@jwt_required()
def edit_profile_route():
    return edit_profile()









@routes.route('/profile', methods=['GET'])
@jwt_required()
def get_profile_route():
    return get_user_profile()









# Advertisement routes
@routes.route('/ads', methods=['GET'])
def get_ads_route():
    return get_ads()





#-------------------------------------------------------------------------------------------------------------------------------


@routes.route('/categories', methods=['GET'])
@jwt_required()
def get_all_categories_route():
    return get_all_categories()


@routes.route('/categories/<int:category_id>/items', methods=['GET'])
@jwt_required()
def get_all_items_of_a_category_route(category_id):
    return get_all_items_of_a_category(category_id)




@routes.route('/api/get_details')
@jwt_required()
def order_details():
    return get_order_details()





@routes.route('/api/user/update-phone-numbers', methods=['PUT']) # logic not working
@jwt_required()
def update_phone_numberss():
    return update_phone_numbers()







@routes.route("/api/kitchen/post/create", methods=["POST"])
@jwt_required()
def create_post_route():
    return create_post()

@routes.route("/api/kitchen/post/update", methods=["GET", "PUT"])
@jwt_required()
def update_post_route():
    return update_post()

@routes.route("/api/kitchen/post/delete", methods=["DELETE"])
@jwt_required()
def delete_post_route():
    return delete_post()

@routes.route("/api/kitchen/orders/upload",methods=["GET"])
@jwt_required()
def upload_order_route():
    return upload_orders()


@routes.route("/api/kitchen/order/status", methods=["PUT"])
@jwt_required()
def update_order_status_route():
    return changing_status()


@routes.route("/api/kitchen/dashboard")
@jwt_required()
def kitchen_dashboard_route():
    return dashboard()

@routes.route("/api/kitchen/order/details")
@jwt_required()
def kitchen_order_details_route():
    return get_customer_details()


@routes.route("/api/kitchen/profile")
@jwt_required()
def kitchen_profile_route():
    return get_profile()

@routes.route("/api/kitchen/profile/reviews")
@jwt_required()
def kitchen_profile_reviews_route():
    return get_reviews()


@routes.route("/api/kitchen/profile/update", methods=["PUT"])
@jwt_required()
def kitchen_profile_update_route():
    return update_kitchen_profile()


@routes.route("/api/kitchen/items/upload", methods=["GET"])
@jwt_required()
def upload_items_route():
    return get_paginated_items()






