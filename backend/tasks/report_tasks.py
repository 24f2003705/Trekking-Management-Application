from tasks.celery_app import celery
from app import app
from models import Trek, Booking, User
from datetime import date
import os


@celery.task
def monthly_report():

    with app.app_context():

        print("Generating Monthly Report")

        total_treks = Trek.query.count()

        completed_treks = Trek.query.filter_by(
            status="Completed"
        ).count()

        total_bookings = Booking.query.count()

        total_participants = Booking.query.filter_by(
            booking_status="Completed"
        ).count()

        popular_trek = "No Data"
        max_bookings = 0

        treks = Trek.query.all()

        for trek in treks:

            bookings = Booking.query.filter_by(
                trek_id=trek.id
            ).count()

            if bookings > max_bookings:

                max_bookings = bookings
                popular_trek = trek.trek_name

        report = f"""
        <html>

        <head>
            <title>Monthly Report</title>
        </head>

        <body>

        <h1>Monthly Trekking Report</h1>

        <hr>

        <p><b>Total Treks :</b> {total_treks}</p>

        <p><b>Completed Treks :</b> {completed_treks}</p>

        <p><b>Total Bookings :</b> {total_bookings}</p>

        <p><b>Total Participants :</b> {total_participants}</p>

        <p><b>Most Popular Trek :</b> {popular_trek}</p>

        <p><b>Generated On :</b> {date.today()}</p>

        </body>

        </html>
        """

        os.makedirs("reports", exist_ok=True)

        with open("reports/monthly_report.html", "w") as file:

            file.write(report)

        print("Monthly Report Saved")

        return "Report Generated"