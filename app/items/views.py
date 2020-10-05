from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app import db
from app.models import Item, User, UserItem

items_blueprint = Blueprint('items', __name__)


class AddImageAPI(MethodView):
    """
    Item addition Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()

        # check if item already exists
        item = Item.query.filter_by(item=post_data.get('item')).first()
        if not item:
            try:
                item = Item(
                    item=post_data.get('item'),
                    item_name=post_data.get('item_name'),
                    item_description=post_data.get('item_description')
                )
                # insert the item
                db.session.add(item)
                db.session.commit()

                responseObject = {
                    'status': 'success',
                    'message': 'Item added successfully.'
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            if item:
                responseObject = {
                    'status': 'fail',
                    'message': 'Item with the same name already exists.',
                }
                return make_response(jsonify(responseObject)), 202


class AddUserItemsAPI(MethodView):
    """
    add user items Resource
    """

    def post(self):
        print(request.get_json())
        # get the post data
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            print(auth_token)
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                post_data = request.get_json()
                item_value = post_data['item']

                item_split = item_value.split('_')
                item = '{}_{}'.format(item_split[-2], item_split[-1])
                # check if item already exists
                item = Item.query.filter_by(item=item).first()
                # check if user already exists
                user = User.query.filter_by(email=post_data['email']).first()
                if item and user:
                    try:
                        user_item = UserItem(
                                item_id=item.id,
                                user_id=user.id
                        )
                        # insert the user
                        db.session.add(user_item)
                        db.session.commit()

                        print('insert successful')
                        responseObject = {
                            'status': 'success',
                            'message': 'User item added successfully.'
                        }
                        return make_response(jsonify(responseObject)), 201
                    except Exception as e:
                        responseObject = {
                            'status': 'fail',
                            'message': 'Some error occurred. Please try again.'
                        }
                        return make_response(jsonify(responseObject)), 401
                else:
                    if not item and not user:
                        responseObject = {
                            'status': 'fail',
                            'message': 'Item and user doesn\'t exist.'
                        }
                        return make_response(jsonify(responseObject)), 202
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


class RemoveUserItemsAPI(MethodView):
    """
    remove user items Resource
    """

    def delete(self):
        # get the post data
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):

                post_data = request.get_json()
                item_value = post_data['item']

                item_split = item_value.split('_')
                item = '{}_{}'.format(item_split[-2], item_split[-1])

                # check if item already exists
                item = Item.query.filter_by(item=item).first()
                # check if user already exists
                user = User.query.filter_by(email=post_data['email']).first()
                if item and user:
                    try:
                        user_item = UserItem.query.filter_by(item_id=item.id).order_by(UserItem.id.desc()).first()
                        db.session.delete(user_item)
                        db.session.commit()

                        responseObject = {
                            'status': 'success',
                            'message': 'User item deleted successfully.'
                        }
                        return make_response(jsonify(responseObject)), 201
                    except Exception as e:
                        responseObject = {
                            'status': 'fail',
                            'message': 'Some error occurred. Please try again.'
                        }
                        return make_response(jsonify(responseObject)), 401
                else:
                    if item:
                        responseObject = {
                            'status': 'fail',
                            'message': 'Item and user doesn\'t exist.',
                        }
                        return make_response(jsonify(responseObject)), 202
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


class GetImagesAPI(MethodView):
    """
    Get Image Resource
    """

    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                items = Item.query.all()
                if items:
                    all_items = []

                    for i in items:
                        all_items.append({"item": i.item,
                            "item_name": i.item_name,
                            "item_description": i.item_description})

                    responseObject = {
                        'status': 'success',
                        'data': all_items
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'No item present'
                    }
                    return make_response(jsonify(responseObject)), 404
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


class DeleteImagesAPI(MethodView):
    """
    Get Image Resource
    """

    def delete(self):

        request_data = request.get_json()
        item = Item.query.filter_by(item=request_data['item']).first()
        if item:
            db.session.delete(item)
            db.session.commit()

            responseObject = {
                'status': 'success',
                'message': 'Item deleted Successfully'
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'No item present'
            }
            return make_response(jsonify(responseObject)), 404


# define the API resources
add_image_view = AddImageAPI.as_view('add_image_api')
get_all_images_view = GetImagesAPI.as_view('get_all_images_api')
delete_image_view = DeleteImagesAPI.as_view('delete_image_view')
add_user_items_view = AddUserItemsAPI.as_view('add_user_items_view')
delete_user_items_view = RemoveUserItemsAPI.as_view('delete_user_items_view')



# add Rules for API Endpoints
items_blueprint.add_url_rule(
    '/items/add',
    view_func=add_image_view,
    methods=['POST']
)
items_blueprint.add_url_rule(
    '/items/all',
    view_func=get_all_images_view,
    methods=['GET']
)
items_blueprint.add_url_rule(
    '/items/remove',
    view_func=delete_image_view,
    methods=['DELETE']
)
items_blueprint.add_url_rule(
    '/items/user-item/add',
    view_func=add_user_items_view,
    methods=['POST']
)
items_blueprint.add_url_rule(
    '/items/user-item/remove',
    view_func=delete_user_items_view,
    methods=['DELETE']
)