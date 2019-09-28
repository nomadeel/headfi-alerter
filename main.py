#!/usr/bin/env python3

from parser.parser import *
from record.record import *
from notifier.notifier import *
from sendgrid import SendGridAPIClient

def main():
    (sg, from_email, to_email) = auth()
    conn = connect_to_database()
    db_cursor = conn.cursor()
    # Grab the listings from the RSS feed
    listings = parse_feed(db_cursor)
    # Add these listings into the database
    add_entries(db_cursor, listings)
    conn.commit()
    conn.close()
    filtered_listings = list((l for l in listings if l.ships_to == "Australia" or l.ships_to == "Anywhere"))
    send_email(filtered_listings, sg, from_email, to_email)

if __name__ == "__main__":
    main()

