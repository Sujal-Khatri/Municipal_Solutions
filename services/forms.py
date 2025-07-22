from django import forms
from decimal import Decimal
from .models import DiscussionPost, SelfAssessmentReturn, TaxReturn

class DiscussionPostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ['title', 'content', 'image', 'location','category']  # include image + location
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

#tax ko lagi
class SelfAssessmentReturnForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="6+ characters, case-sensitive"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    class Meta:
        model = SelfAssessmentReturn
        fields = [
            'username', 'password', 'password2',
            'pan_no', 'fiscal_year', 'email', 'contact_no',
            'turnover_amount', 'deduction_amount',
            'revenue_account_no', 'payment_type', 'voucher_no',
            'bank_name', 'deposit_date', 'deposit_amount',
            'receipt',
        ]
        widgets = {
            'deposit_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords must match")
        return pw2

    def clean(self):
        cleaned = super().clean()

        # compute income = turnover – deduction
        turnover = cleaned.get('turnover_amount') or Decimal('0')
        deduction = cleaned.get('deduction_amount') or Decimal('0')
        income = turnover - deduction
        cleaned['income'] = income

        # 1% tax, 0.1% penalty
        cleaned['tax_amount'] = income * Decimal('0.01')
        cleaned['interest_penalty'] = income * Decimal('0.001')

        # total = tax + penalty + deposit
        deposit = cleaned.get('deposit_amount') or Decimal('0')
        cleaned['total_payable'] = (
            cleaned['tax_amount'] +
            cleaned['interest_penalty'] +
            deposit
        )

        return cleaned