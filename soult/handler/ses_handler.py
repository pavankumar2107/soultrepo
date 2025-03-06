from utils.connections_utils import get_ses_connection
from utils.logger_factory import get_logger
from utils.response_utils import build_response
from dao.user_dao import get_user_details

SES_SENDER_EMAIL = 'akash@uskcorp.in'
# Logger setup
logger = get_logger(__name__)

def ses_handler(event_data):
    # Extract necessary fields
    user_data = get_user_details(event_data.get("User_id"))
    # Construct email subject & body
    email_subject = f"Notification: {event_data.get("event")}"
    email_body = f"""
     <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to Soult</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 20px auto;
                    background: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background: #33445A;
                    padding: 20px;
                    text-align: center;
                }}
                .header img {{
                    width: 150px;
                }}
                .content {{
                    padding: 20px;
                    color: #333;
                    line-height: 1.6;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    font-size: 12px;
                    background: #f4f4f4;
                    color: #666;
                }}
                .store-links img {{
                    width: 120px;
                    margin: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Header with Logo -->
                <div class="header">
                    <img src="https://i.im.ge/2025/02/12/HmDx0P.50F203CD-8F03-47A7-B9AB-37165A77DCBA.png" alt="Soult Logo">
                </div>

                <!-- Email Content -->
                <div class="content">
                    <p>Dear <strong>{user_data['firstname'].title()} {user_data['lastname'].title()}</strong>,</p>
                    <p>Thank you for registering with <strong>Soult</strong>. We’re excited to have you on board!</p>
                    <p>With Soult, you can enjoy a seamless experience in managing your activities efficiently. Get started today by exploring our app.</p>
                    <p>Your account has been <strong>{event_data['action']}</strong> with a new <strong>{event_data['model_name']}</strong>.</p>
                    <p><strong>User ID:</strong> {event_data['User_id']}</p>
                    <p><strong>Model ID:</strong> {event_data['model_id']}</p>
                    <p>If you have any questions, feel free to reach out to our support team.</p>
                    <p>Best Regards,</p>
                    <p><strong>The Soult Team</strong></p>
                </div>

                <!-- App Store and Play Store Links -->
                <div class="footer">
                    <p>Download our app:</p>
                    <div class="store-links">
                        <a href="#"><img src="http://email.aumfusion.com/vespro/img/app/play-store.png" alt="Google Play Store"></a>
                        <a href="#"><img src="http://email.aumfusion.com/vespro/img/app/app-store.png" alt="Apple App Store"></a>
                    </div>
                    <p>&copy; 2025 Soult. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
    """

    # Send email via SES
    response= send_email(email_subject, email_body,SES_SENDER_EMAIL) # Hardcoded for testing; replace with user_data['email']
    logger.info(f"SES Email sent successfully: {response}")
    return build_response(response)

def send_email(email_subject,email_body,user_email):
    ses_client = get_ses_connection()
    return  ses_client.send_email(
        Source=SES_SENDER_EMAIL,
        Destination={"ToAddresses": [user_email]},
        Message={
            "Subject": {"Data": email_subject},
            "Body": {
                "Html": {"Data": email_body},
                "Text": {"Data": email_body},
            },
        },
    )