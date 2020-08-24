# Python imports
import json
import hashlib
import base64
from datetime import datetime, timedelta
import logging

# Django imports
from django.views import View
from django.http import HttpResponse

# Project imports
from users.models import Manager
from assignment_project.stripe_gateway import create_customer
from assignment_project.authorize_request import authorize
from assignment_project.exception_handler import exception_details


# Create your views here.
class Users(View):
    def post(self, request):
        try:
            create_request = json.loads(request.body)
            is_user_exists = Manager.objects.filter(email=create_request.get('email')).count()
            if is_user_exists > 0:
                return HttpResponse(json.dumps({"msg": "User Already Registered."}), status=406,
                                    content_type='application/json')
            stripe_response, status = create_customer(create_request)
            print(f"CREATE STRIP CUSTOMER: {stripe_response} - {status}")
            if not status:
                return HttpResponse(json.dumps({'msg': 'Error is {}'.format(stripe_response)}), status=412,
                                    content_type='application/json')
            manager = Manager.objects.create(
                email=create_request.get('email'),
                firstname=create_request.get('firstname'),
                lastname=create_request.get('lastname'),
                password=create_request.get('password'),
                company=create_request.get('company'),
                address=create_request.get('address'),
                dob=create_request.get('dob'),
                strip_id=stripe_response
            )
            return HttpResponse(json.dumps({'msg': 'Congratulations! Your account has been created'}), status=200,
                                content_type='application/json')
        except Exception as e:
            exception_details("USER.POST", e)
            return HttpResponse(json.dumps({'msg': f'Error occurred: {str(e)}'}), status=500,
                                content_type='application/json')

    def put(self, request):
        return HttpResponse(json.dumps({'msg': 'Request method PUT not supported'}), status=405,
                            content_type='application/json')

    def get(self, request):
        try:
            if authorize(request):
                cookie_data = base64.b64decode(request.COOKIES.get("session")).decode('utf-8').split(".")[1]
                user = Manager.objects.get(id=cookie_data)
                user_response = {
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'email': user.email,
                    'address': user.address,
                    'dob': str(user.dob),
                    'company': user.company,
                    'product_id': user.product_id,
                    'subscription_id': user.subscription_id
                }
                return HttpResponse(json.dumps({'data': user_response}), status=200, content_type='application/json')
            else:
                return HttpResponse(json.dumps({'msg': 'Authorization Error, User is not logged-in'}), status=403,
                                    content_type='application/json')
        except Exception as e:
            exception_details("USER.GET", e)
            return HttpResponse(json.dumps({'msg': f'Error occurred: {str(e)}'}), status=500,
                                content_type='application/json')

    def delete(self, request):
        return HttpResponse(json.dumps({'msg': 'Request method DELETE not supported'}), status=405,
                            content_type='application/json')


class Login(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = Manager.objects.filter(email=data.get('email'), password=data.get('password')).first()
            if not user:
                return HttpResponse(json.dumps({'msg': "User Email or Password Incorrect."}), status=403,
                                    content_type='application/json')
            expire = datetime.now() + timedelta(hours=5)
            user_hash = hashlib.md5(user.email.encode('utf-8')).hexdigest()
            session = user_hash + '.' + str(user.id)
            session = str(base64.b64encode(session.encode('utf-8')), 'utf-8')
            print(f"SESSION: {session}")
            response = HttpResponse(json.dumps({
                'msg': 'You have logged in successfully',
                'sessionId': session
            }), status=200, content_type='application/json')
            response.set_cookie('session', session, expires=expire)
            return response
        except Exception as e:
            exception_details("LOGIN.POST", e)
            return HttpResponse(json.dumps({'msg': f'Error occurred: {str(e)}'}), status=500,
                                content_type='application/json')

    def put(self, request):
        return HttpResponse(json.dumps({'msg': 'Request method PUT not supported'}), status=405,
                            content_type='application/json')

    def get(self, request):
        try:
            if authorize(request):
                response = HttpResponse(json.dumps({'msg': "You have logged out successfully"}), status=200,
                                        content_type='application/json')
                response.delete_cookie('session')
                return response
            else:
                response = HttpResponse(json.dumps({'msg': 'Authorization Error, User is not logged-in'}), status=403,
                                        content_type='application/json')
                response.delete_cookie('session')
                return response

        except Exception as e:
            exception_details("LOGIN.GET", e)
            return HttpResponse(json.dumps({'msg': f'Error occurred: {str(e)}'}), status=500,
                                content_type='application/json')

    def delete(self, request):
        return HttpResponse(json.dumps({'msg': 'Request method DELETE not supported'}), status=405,
                            content_type='application/json')
