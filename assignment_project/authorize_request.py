import hashlib
import base64

from users.models import Manager
from assignment_project.exception_handler import exception_details


def authorize(request):
    try:
        cookie = request.COOKIES.get("session")
        if not cookie:
            return False
        cookie_data = base64.b64decode(cookie).decode('utf-8')
        print(f"COOKIE: {cookie} - {cookie_data}")
        if '.' in cookie_data:
            _email, _id = cookie_data.split('.')
            user = Manager.objects.get(id=_id)
            if not user:
                return False
            email_hash = hashlib.md5(user.email.encode('utf-8')).hexdigest()
            if _email == email_hash:
                return True
            return False
        return False
    except Exception as e:
        exception_details("AUTHORIZE", e)
        return False
