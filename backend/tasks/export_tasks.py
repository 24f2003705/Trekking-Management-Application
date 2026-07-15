from tasks.celery_app import celery
from app import app
from models import Booking, User
from extensions import db
import csv
import os


@celery.task
def export_csv(user_id):

    with app.app_context():

        bookings = Booking.query.filter_by(user_id=user_id).all()

        export_folder = os.path.join(app.root_path, "exports")
        os.makedirs(export_folder, exist_ok=True)

        filename = f"user_{user_id}_history.csv"
        filepath = os.path.join(export_folder, filename)

        with open(filepath, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Booking ID",
                "Trek",
                "Location",
                "Booking Date",
                "Booking Status",
                "Payment Status"
            ])

            for booking in bookings:

                writer.writerow([
                    booking.id,
                    booking.trek.trek_name,
                    booking.trek.location,
                    booking.booking_date,
                    booking.booking_status,
                    booking.payment_status
                ])

        user = User.query.get(user_id)

        user.latest_export = filename

        db.session.commit()

        print("CSV Export Completed")

        return filename