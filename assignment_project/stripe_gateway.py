import stripe

stripe.api_key = "sk_test_51HIXBHEhDbk4FEiokxq6rfpH647M6xGZsSOADRm1UIIhdTNvpAjCmMPfM5tSkHPqrAQ2gXv4DC069BLLsVNBBsj6009wfHfXzd"


def create_customer(customer_details):
    try:
        name = customer_details.get('firstname') + ' ' + customer_details.get('lastname')
        customer = stripe.Customer.create(
            email=customer_details.get('email'),
            name=name,
            address={
                "line1": customer_details.get('address'),
            }
        )
        return customer.stripe_id, True
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        return str(e), False
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        return str(e), False
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return str(e), False
    except stripe.error.StripeError as e:
        # Display a very generic error to the user
        return str(e), False
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        return str(e), False


def create_card_payment_method(customer_id, card_number, exp_month, exp_year, cvv_number):
    try:
        card = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": card_number,
                "exp_month": int(exp_month),
                "exp_year": int(exp_year),
                "cvc": str(cvv_number),
            },
        )
        try:
            attach = stripe.PaymentMethod.attach(
                card.id,
                customer=customer_id,
            )
        except Exception as e:
            print("Error in stripe.PaymentMethod.attach")
            print(str(e))
        return card.id, True
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught

        print('Status is: %s' % e.http_status)
        print('Type is: %s' % e.error.type)
        print('Code is: %s' % e.error.code)
        print('Param is: %s' % e.error.param)
        print('Message is: %s' % e.error.message)
        return str(e), False
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        return str(e), False
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        return str(e), False
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return str(e), False
    except stripe.error.StripeError as e:
        # Display a very generic error to the user
        return str(e), False
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        return str(e), False


def create_subscription(customer_id, product_id, payment_method_id):
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[
                {"price": product_id},
            ],
            default_payment_method=payment_method_id
        )
        return subscription, True
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        return str(e), False
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        return str(e), False
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return str(e), False
    except stripe.error.StripeError as e:
        # Display a very generic error to the user
        return str(e), False
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        return str(e), False


def cancel_subscription(subscription_id):
    try:
        subscription = stripe.Subscription.delete(subscription_id)
        return subscription, True
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        return str(e), False
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        return str(e), False
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return str(e), False
    except stripe.error.StripeError as e:
        # Display a very generic error to the user
        return str(e), False
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        return str(e), False


def get_products():
    try:
        # Use Stripe's library to make requests...
        return stripe.Price.list().get('data'), True
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        return str(e), False
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        return str(e), False
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return str(e), False
    except stripe.error.StripeError as e:
        # Display a very generic error to the user
        return str(e), False
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        return str(e), False
