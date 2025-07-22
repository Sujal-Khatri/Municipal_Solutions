from django import forms
from decimal import Decimal
from django.contrib.auth import authenticate
from .models import DiscussionPost, SelfAssessmentReturn

class DiscussionPostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ['title', 'content', 'image', 'location', 'category']


class SelfAssessmentReturnForm(forms.ModelForm):
    PAYMENT_BANK   = 'bank'
    PAYMENT_ONLINE = 'online'
    PAYMENT_CHOICES = [
        (PAYMENT_BANK,   'Payment through Bank'),
        (PAYMENT_ONLINE, 'Online Payment'),
    ]

    password     = forms.CharField(
        widget=forms.PasswordInput,
        help_text="6+ characters, case-sensitive"
    )
    password2    = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )
    payment_type = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="भुक्तानीको किसिम"
    )

    class Meta:
        model  = SelfAssessmentReturn
        fields = [
            'username', 'password', 'password2',
            'pan_no', 'fiscal_year', 'email', 'contact_no',
            'turnover_amount', 'deduction_amount',
            'revenue_account_no', 'payment_type', 'voucher_no',
            'bank_name', 'deposit_date', 'deposit_amount',
            'receipt',
        ]
        widgets = {
            'username':            forms.TextInput(attrs={'class': 'form-control'}),
            'pan_no':              forms.TextInput(attrs={'class': 'form-control'}),
            'fiscal_year':         forms.TextInput(attrs={'class': 'form-control'}),
            'email':               forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_no':          forms.TextInput(attrs={'class': 'form-control'}),
            'turnover_amount':     forms.NumberInput(attrs={'class': 'form-control'}),
            'deduction_amount':    forms.NumberInput(attrs={'class': 'form-control'}),
            'revenue_account_no':  forms.TextInput(attrs={'class': 'form-control'}),
            'voucher_no':          forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name':           forms.TextInput(attrs={'class': 'form-control'}),
            'deposit_date':        forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'deposit_amount':      forms.NumberInput(attrs={'class': 'form-control'}),
            'receipt':             forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords must match")
        return pw2

    def clean(self):
        cleaned = super().clean()

        # 1) Validate credentials against your registered users
        username = cleaned.get('username')
        password = cleaned.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(
                    "The username and/or password you entered are not valid. "
                    "Please use your registered credentials."
                )

        # 2) Require receipt file if paying through Bank
        payment_type = cleaned.get('payment_type')
        receipt      = cleaned.get('receipt')
        if payment_type == self.PAYMENT_BANK and not receipt:
            self.add_error('receipt', "Please upload a payment receipt for bank payments.")

        # 3) Compute financial fields exactly as before
        turnover        = cleaned.get('turnover_amount')  or Decimal('0')
        deduction       = cleaned.get('deduction_amount') or Decimal('0')
        deposit_amount  = cleaned.get('deposit_amount')   or Decimal('0')

        income          = turnover - deduction
        tax             = income * Decimal('0.01')
        penalty         = income * Decimal('0.001')
        total           = tax + penalty + deposit_amount

        cleaned['income']           = income
        cleaned['tax_amount']       = tax
        cleaned['interest_penalty'] = penalty
        cleaned['total_payable']    = total

        return cleaned