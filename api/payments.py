```python
import stripe
from flask import Blueprint, request, jsonify
from .exceptions import PaymentProcessingError
from .auth import authenticate_request
from .validators import validate_payment_data
from database.models import Subscription
from database.database_connection import executeQuery

# Initialize Stripe with the secret key
stripe.api_key = 'STRIPE_API_KEY'

payments_bp = Blueprint('payments', __name__, url_prefix='/api/payment')

@payments_bp.route('/process', methods=['POST'])
@authenticate_request
def process_payment():
    """
    Process payment for a subscription or a one-time purchase.
    """
    # Validate the incoming payment data
    payment_data = request.json
    if not validate_payment_data(payment_data):
        raise PaymentProcessingError("Invalid payment data")

    try:
        # Create a charge on Stripe's servers - this will charge the user's card
        charge = stripe.Charge.create(
            amount=payment_data['amount'],  # amount in cents
            currency='usd',
            source=payment_data['token'],
            description=payment_data['description']
        )

        # Save the subscription details to the database
        user_id = request.user_id
        subscription = Subscription(
            user_id=user_id,
            level=payment_data['subscription_level'],
            price=payment_data['amount']
        )
        executeQuery(subscription.save())

        return jsonify({'message': 'Payment processed successfully', 'charge': charge}), 200
    except stripe.error.StripeError as e:
        # Handle the error
        raise PaymentProcessingError(str(e))

@payments_bp.route('/subscribe', methods=['POST'])
@authenticate_request
def subscribe():
    """
    Subscribe a user to a new plan.
    """
    subscription_data = request.json
    if not subscription_data.get('plan_id'):
        raise PaymentProcessingError("Plan ID is required")

    try:
        # Create a subscription on Stripe's servers
        subscription = stripe.Subscription.create(
            customer=request.user_id,
            items=[{'plan': subscription_data['plan_id']}]
        )

        # Save the subscription details to the database
        user_id = request.user_id
        new_subscription = Subscription(
            user_id=user_id,
            level=subscription_data['plan_id'],
            price=subscription_data['price']
        )
        executeQuery(new_subscription.save())

        return jsonify({'message': 'Subscription created successfully', 'subscription': subscription}), 200
    except stripe.error.StripeError as e:
        # Handle the error
        raise PaymentProcessingError(str(e))

@payments_bp.errorhandler(PaymentProcessingError)
def handle_payment_error(error):
    """
    Handle payment processing errors.
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
```