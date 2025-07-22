# services/models.py

from django.db import models
from django.conf import settings
from accounts.models import CustomUser

class DiscussionPost(models.Model):
    CATEGORY_TAX          = 'tax'
    CATEGORY_CONSTRUCTION = 'construction'
    CATEGORY_HEALTH       = 'health'
    CATEGORY_CHOICES = [
        (CATEGORY_TAX,          'Tax'),
        (CATEGORY_CONSTRUCTION, 'Construction'),
        (CATEGORY_HEALTH,       'Health'),
    ]

    author     = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title      = models.CharField(max_length=200)
    content    = models.TextField()
    image      = models.ImageField(upload_to='discussion_images/', blank=True, null=True)
    location   = models.CharField(max_length=100, blank=True, null=True)
    category   = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_TAX,
        help_text="Select one: Tax, Construction or Health"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes      = models.PositiveIntegerField(default=0)
    dislikes   = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class PostReaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    VOTE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post     = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=7, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.reaction} on Post ID {self.post.id}"


class Notice(models.Model):
    title      = models.CharField(max_length=255)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Report(models.Model):
    title      = models.CharField(max_length=200)
    content    = models.TextField()
    file       = models.FileField(upload_to='reports/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SelfAssessmentReturn(models.Model):
    submission_no        = models.AutoField(primary_key=True)

    # — Account setup
    username             = models.CharField("Username", max_length=150)
    password             = models.CharField("Password", max_length=128)
    password2            = models.CharField("Confirm Password", max_length=128)

    pan_no               = models.CharField("PAN No.", max_length=20)
    fiscal_year          = models.CharField("Fiscal Year", max_length=9)
    email                = models.EmailField("Email ID")
    contact_no           = models.CharField("Contact No.", max_length=20)

    # — Financial details
    turnover_amount      = models.DecimalField("कर कारोबार रकम", max_digits=12, decimal_places=2)
    deduction_amount     = models.DecimalField("कट्टी हुने रकम", max_digits=12, decimal_places=2)
    income               = models.DecimalField("आय (auto)", max_digits=12, decimal_places=2, blank=True, null=True)
    tax_amount           = models.DecimalField("Tax (auto)", max_digits=12, decimal_places=2, blank=True, null=True)
    interest_penalty     = models.DecimalField("Interest & Penalty (auto)", max_digits=12, decimal_places=2, blank=True, null=True)
    total_payable        = models.DecimalField("Total Payable (auto)", max_digits=12, decimal_places=2, blank=True, null=True)

    # — Payment entry
    revenue_account_no   = models.CharField("राजश्व खाता नं.", max_length=50)
    payment_type         = models.CharField("भुक्तानीको किसिम", max_length=50)
    voucher_no           = models.CharField("भौचर/रसिद नं.", max_length=50)
    bank_name            = models.CharField("बैंकको नाम", max_length=100)
    deposit_date         = models.DateField("दाखिला मिति")
    deposit_amount       = models.DecimalField("दाखिला रकम", max_digits=12, decimal_places=2)

    submitted            = models.BooleanField(default=False)
    receipt              = models.FileField("Payment Receipt", upload_to='tax_receipts/', blank=True, null=True)

    created_at           = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submission_no']

    def __str__(self):
        return f"D-01 Return #{self.submission_no}"


class TaxReturn(models.Model):
    user                 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pan_no               = models.CharField("PAN Number", max_length=50)
    fiscal_year          = models.CharField("Fiscal Year", max_length=9)
    email                = models.EmailField()
    contact_no           = models.CharField("Contact No", max_length=20)
    turnover_amount      = models.DecimalField(max_digits=12, decimal_places=2)
    deduction_amount     = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount           = models.DecimalField(max_digits=12, decimal_places=2)
    revenue_account_no   = models.CharField(max_length=50)
    payment_type         = models.CharField(max_length=50)
    voucher_no           = models.CharField(max_length=50)
    bank_name            = models.CharField(max_length=100)
    deposit_date         = models.DateField()
    deposit_amount       = models.DecimalField(max_digits=12, decimal_places=2)
    receipt              = models.FileField(
                              upload_to='tax_receipts/',
                              blank=True, null=True,
                              help_text="Upload your payment receipt"
                          )
    submitted_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return #{self.id} by {self.user.username}"
