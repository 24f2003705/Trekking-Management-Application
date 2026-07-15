from datetime import date, timedelta

from app import app
from models import Trek, Booking
from tasks.celery_app import celery
from flask_mail import Message
from extensions import mail


@celery.task
def daily_reminder():

    with app.app_context():

        tomorrow = date.today() + timedelta(days=1)

        treks = Trek.query.filter(
                Trek.start_date == tomorrow
            ).all()

        for trek in treks:

            bookings = Booking.query.filter_by(
                trek_id=trek.id,
                booking_status="Booked"
            ).all()

            for booking in bookings:
                msg = Message(
                    subject=f"Trek Reminder - {trek.trek_name}",
                    recipients=[booking.user.email]
                )

                msg.body = f"""
                Hello {booking.user.name},

                This is a reminder that your trek starts tomorrow.

                Trek Name : {trek.trek_name}
                Location  : {trek.location}
                Start Date: {trek.start_date}

                Please arrive on time and carry all the required trekking equipment.

                Happy Trekking!

                Regards,
                TrekWay Team
                """
                print("Sending to:", booking.user.email)
                mail.send(msg)

                print(f"Reminder sent to {booking.user.email}")

    return "Reminder Completed"