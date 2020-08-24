# Python imports
import json
import base64
import logging
import os
import sys

# Django imports
from django.views import View
from django.http import HttpResponse

# Project imports
from assignment_project.stripe_gateway import get_products, create_card_payment_method, create_subscription, \
    cancel_subscription
from assignment_project.authorize_request import authorize
from assignment_project.exception_handler import exception_details
from users.models import Manager
from subscription.models import Subscription


# Create your views here.
class Subscriptions(View):
    def post(self, request):
        try:
            if authorize(request):
                data = json.loads(base64.b64decode(request.body))
                cookie_data = base64.b64decode(request.COOKIES.get("session")).decode('utf-8').split(".")[1]
                user = Manager.objects.get(id=cookie_data)
                if not user:
                    return HttpResponse(json.dumps({'msg': 'Authorization Error, User does not exists'}), status=412,
                                        content_type='application/json')
                strip_card_response, card_status = create_card_payment_method(
                    user.strip_id,
                    data.get('card_number'),
                    data.get('exp_month'),
                    data.get('exp_year'),
                    data.get('cvv_number')
                )
                print(f"CREATE STRIP CARD PAYMENT METHOD: {strip_card_response} - {card_status}")
                if not card_status:
                    return HttpResponse(json.dumps({'msg': 'Error is {}'.format(strip_card_response)}), status=412,
                                        content_type='application/json')
                strip_subs_response, subs_status = create_subscription(user.strip_id, data.get('product_id'),
                                                                       strip_card_response)
                print(f"CREATE STRIP SUBSCRIPTION: {strip_subs_response} - {subs_status}")
                if not subs_status:
                    return HttpResponse(json.dumps({'msg': 'Error is {}'.format(strip_card_response)}), status=412,
                                        content_type='application/json')
                subscription = Subscription.objects.create(
                    subscription_id=strip_subs_response.get('id'),
                    name=dict(strip_subs_response.get('plan').get('metadata')).get('nickname'),
                    started_at=strip_subs_response.get('start_date'),
                    ended_at=strip_subs_response.get('ended_at'),
                    canceled_at=strip_subs_response.get('canceled_at'),
                    product_id=strip_subs_response.get('plan').get('product'),
                    price_id=strip_subs_response.get('plan').get('id'),
                    user_id=user.id,
                    status='active')

                user.subscription_id = subscription.subscription_id
                user.product_id = subscription.product_id
                user.save()
                return HttpResponse(json.dumps({
                    'data': subscription.id,
                    'msg': 'Subscription has added to your account successfully'
                }), status=200)
            else:
                return HttpResponse(json.dumps({'msg': 'Authorization Error, User is not logged-in'}), status=403,
                                    content_type='application/json')
        except Exception as e:
            exception_details("SUBSCRIPTION.POST", e)
            return HttpResponse(json.dumps({'msg': f'Error occurred: {str(e)}'}), status=500,
                                content_type='application/json')

    def put(self, request):
        try:
            if authorize(request):
                cookie_data = base64.b64decode(request.COOKIES.get("session")).decode('utf-8').split(".")[1]
                user = Manager.objects.get(id=cookie_data)
                if not user:
                    return HttpResponse(json.dumps({'msg': 'Authorization Error, User does not exists'}), status=412,
                                        content_type='application/json')
                print(user.email)
                print(user.strip_id)
                print(user.subscription_id)
                subscription = Subscription.objects.get(subscription_id=user.subscription_id)
                if not subscription:
                    return HttpResponse(json.dumps({'msg': 'Error occurred, Please contact admin'}), status=412,
                                        content_type='application/json')
                strip_response, status = cancel_subscription(subscription.subscription_id)
                print(f"CANCEL STRIP SUBSCRIPTION: {strip_response} - {status}")
                if not status:
                    return HttpResponse(json.dumps({'msg': 'Error is {}'.format(strip_response)}), status=412,
                                        content_type='application/json')
                user.subscription_id = ''
                user.product_id = ''
                user.save()
                subscription.status = 'canceled'
                subscription.cancel_at = strip_response.get('canceled_at')
                subscription.ended_at = strip_response.get('ended_at')
                subscription.save()
                return HttpResponse(json.dumps({
                    'data': subscription.id,
                    'msg': 'Subscription cancelled successfully'
                }), status=200, content_type='application/json')
            else:
                return HttpResponse(json.dumps({'msg': 'Authorization Error, User is not logged-in'}), status=403,
                                    content_type='application/json')
        except Exception as e:
            exception_details("SUBSCRIPTION.PUT", e)
            return HttpResponse(json.dumps({'msg': f'Error occurred: {str(e)}'}), status=500,
                                content_type='application/json')

    def get(self, request):
        try:
            if authorize(request):
                cookie_data = base64.b64decode(request.COOKIES.get("session")).decode('utf-8').split(".")[1]
                user = Manager.objects.get(id=cookie_data)
                if not user:
                    return HttpResponse(json.dumps({'msg': 'Authorization Error, User does not exists'}), status=412)
                subscription_list = list(Subscription.objects.filter(user_id=user.id))
                response = []
                for each in subscription_list:
                    response.append({
                        'id': each.id,
                        'name': each.name,
                        'product_id': each.product_id,
                        'price_id': each.price_id,
                        'started_at': each.started_at,
                        'ended_at': each.ended_at,
                        'canceled_at': each.canceled_at,
                        'status': each.status,
                    })
                return HttpResponse(json.dumps({'data': response}), status=200, content_type='application/json')
            else:
                return HttpResponse(json.dumps({'msg': 'Authorization Error, User is not logged-in'}), status=403,
                                    content_type='application/json')
        except Exception as e:
            exception_details("SUBSCRIPTION.GET", e)
            return HttpResponse(json.dumps({'msg': f'Error occurred: {str(e)}'}), status=500,
                                content_type='application/json')

    def delete(self, request):
        return HttpResponse(json.dumps({'msg': 'Request method DELETE not supported'}), status=405,
                            content_type='application/json')


class Products(View):
    def post(self, request):
        return HttpResponse(json.dumps({'msg': 'Request method POST not supported'}), status=405,
                            content_type='application/json')

    def put(self, request):
        return HttpResponse(json.dumps({'msg': 'Request method PUT not supported'}), status=405,
                            content_type='application/json')

    def get(self, request):
        try:
            if authorize(request):
                strip_response, status = get_products()
                print(f"GET STRIP PRODUCTS: {strip_response} - {status}")
                if status and strip_response:
                    return HttpResponse(json.dumps({'data': strip_response}), status=200,
                                        content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'msg': 'Error is {}'.format(strip_response)}), status=412,
                                        content_type='application/json')
            else:
                return HttpResponse(json.dumps({'msg': 'Authorization Error, User is not logged-in'}), status=403,
                                    content_type='application/json')
        except Exception as e:
            exception_details("PRODUCTS.GET", e)
            return HttpResponse(json.dumps({'msg': f'Error occurred: {str(e)}'}), status=500,
                                content_type='application/json')

    def delete(self, request):
        return HttpResponse(json.dumps({'msg': 'Request method DELETE not supported'}), status=405,
                            content_type='application/json')
