
from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User

def get_current_month():
    """Returns the current month as a string."""
    return datetime.now().strftime('%B')  # e.g., 'January'

class Workday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    WORKDAY_TYPE = [
        ('Work', 'Work'),
        ('Sick Leave', 'Sick Leave'),
        ('Annual Leave', 'Annual Leave'),
        ('Bank Holiday', 'Bank Holiday'),
    ]

    MONTH = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    date = models.DateField()
    month = models.CharField(
        max_length=20,
        choices=MONTH,
        default=get_current_month,
    )
    workday_type = models.CharField(
        max_length=20,
        choices=WORKDAY_TYPE,
        default='Work',
    )
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.date} ({self.workday_type})"
    
    @property
    def total_hours(self):
        """ to calculate total hours worked for the day."""
        if self.time_in and self.time_out:
            time_in_dt = datetime.combine(date.today(), self.time_in)
            time_out_dt = datetime.combine(date.today(), self.time_out)
            time_diff = time_out_dt - time_in_dt
            return time_diff.total_seconds() / 3600  # Convert seconds to hours
        return 0

    def clean(self):
        """to validate that time_in and time_out are provided only when required."""
        if self.workday_type in ['Sick Leave', 'Annual Leave', 'Bank Holiday']:
            if self.time_in or self.time_out:
                raise ValueError(
                    f"Time In and Time Out should not be provided for {self.get_workday_type_display()}."
                )
        elif self.workday_type == 'Work':
            if not self.time_in or not self.time_out:
                raise ValueError("Time In and Time Out are required for Workdays.")

    def save(self, *args, **kwargs):
        """Custom save method to enforce time_in and time_out constraints."""
        self.full_clean()  # Runs the clean method for validation
        super().save(*args, **kwargs)
