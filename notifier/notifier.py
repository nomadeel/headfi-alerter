import os
import sys
import yaml
from datetime import datetime
from record.record import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

CREDENTIALS_FILE = "credentials.yaml"

def auth() -> (SendGridAPIClient, str):
    if not os.path.exists(CREDENTIALS_FILE):
        sys.exit("Credentials file not found!")

    with open(CREDENTIALS_FILE, "r") as stream:
        credentials = yaml.safe_load(stream)

    if "api_key" not in credentials or "to_email" not in credentials or "from_email" not in credentials:
        sys.exit("Credentials file doesn't follow the expected format!")

    return (SendGridAPIClient(credentials["api_key"]), credentials["from_email"], credentials["to_email"]) 

def send_email(listings: [Listing], sg: SendGridAPIClient, from_email: str, to_email: str):
    formatted_listings = []
    for listing in listings:
        formatted_listing = "Title: {}<br>Price: {}<br>Link: {}".format(listing.title, listing.price,
                                                                    listing.link)
        formatted_listings.append(formatted_listing)

    now = datetime.now()
    now_string = now.strftime("%d/%m/%y %H:%M")
    if len(formatted_listings):
        message_contents = "<br><br>".join(formatted_listings)
    else:
        message_contents = "No listings."
    message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject="Head-Fi Classifieds Feed @ {}".format(now_string),
                html_content=message_contents
              )
    try:
        response = sg.send(message)
    except Exception as e:
        print(e.message)
