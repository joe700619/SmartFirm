from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from registration.models import RegistrationProgress, RegistrationMandate
from .forms import RegistrationMandateForm
from django.views.generic import UpdateView
from django.urls import reverse

@login_required
def mandate_update(request, pk):
    # pk is RegistrationProgress id
    progress = get_object_or_404(RegistrationProgress, pk=pk)
    
    # Get or Create Mandate
    mandate, created = RegistrationMandate.objects.get_or_create(progress=progress)
    
    if request.method == 'POST':
        form = RegistrationMandateForm(request.POST, instance=mandate)
        if form.is_valid():
            mandate = form.save()
            
            # Sync Address to RegistrationProgress
            address = form.cleaned_data.get('address')
            if address:
                progress.contact_address = address
                progress.save()
                
            messages.success(request, '委任書資料已更新')
            return redirect('registration:progress:edit', pk=pk)
    else:
        form = RegistrationMandateForm(instance=mandate)
        
    # We might render a partial template if loading via AJAX, 
    # but for now let's assume we render a standalone snippet or full page?
    # Actually, the user wants Tabs. So these views might be called via AJAX 
    # to load content into the tab pane, or we just render the form logic here.
    
    # However, to keep it simple first, let's assume this view handles the POST
    # from the main page if we use htmx or iframe? 
    # Or, we can just treat this as a helper that returns the form context 
    # if we were to compose views.
    
    # BUT, standard Django way for Tabs:
    # Option A: One big view handling all forms. (Messy)
    # Option B: Separate views, loading content via AJAX. (Clean)
    
    # Let's go with Option B: AJAX Load.
    
    context = {
        'form': form,
        'progress': progress,
        'is_mandate': True # Helper flag
    }
    return render(request, 'mandate/form.html', context)

class MandateDetailView(UpdateView):
    model = RegistrationMandate
    form_class = RegistrationMandateForm
    template_name = 'mandate/detail.html'

    def get_object(self, queryset=None):
        progress_id = self.kwargs.get('pk')
        progress = get_object_or_404(RegistrationProgress, pk=progress_id)
        mandate, _ = RegistrationMandate.objects.get_or_create(progress=progress)
        return mandate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progress'] = self.object.progress
        initial_address = self.object.address
        if not initial_address and self.object.progress.customer:
             # Default to customer's registration address if not set
             initial_address = self.object.progress.customer.registration_address
        elif not initial_address and self.object.progress.contact_address:
             initial_address = self.object.progress.contact_address
        
        # We can set initial in the form instance, but view processing order...
        # If it's GET and form is bound to object, object's value is used.
        # If object.address is None, we want to pre-fill? 
        # Actually ModelForm uses current instance value. If it's None, it's empty.
        # If we want to prefill, we should do it in get_form or get_initial or modify object before form init.
        
        # Better: if instance address is blank, try to populate it for display (but form logic handles save)
        # However, View handles form construction.
        
        total_fee = self.object.progress.services.filter(is_deleted=False).aggregate(total=Sum('fee'))['total'] or 0
        context['total_fee'] = total_fee
        return context

    def get_initial(self):
        initial = super().get_initial()
        if not self.object.address:
             # Prioritize Main Contact's address if available (User request: "I wrote Taipei in contact")
             if self.object.progress.main_contact and self.object.progress.main_contact.address:
                 initial['address'] = self.object.progress.main_contact.address
             elif self.object.progress.customer and self.object.progress.customer.registration_address:
                 initial['address'] = self.object.progress.customer.registration_address
        return initial

    def form_valid(self, form):
        # Sync Address to RegistrationProgress
        # super().form_valid(form) saves the object but returns a redirect response.
        # We want to save, THEN intercept the response.
        self.object = form.save()
        
        # Auto-set mandate_date to today
        from django.utils import timezone
        self.object.mandate_date = timezone.now().date()
        self.object.save()

        address = form.cleaned_data.get('address')
        if address:
            self.object.progress.contact_address = address
            self.object.progress.save()
            
        messages.success(self.request, '委任書資料已更新，正在轉導至付款頁面...')
        
        # --- Payment Integration ---
        # 1. Calculate Amount
        # Base fee
        base_fee = self.object.progress.services.filter(is_deleted=False).aggregate(total=Sum('fee'))['total'] or 0
        total_amount = base_fee
        
        # Delivery surcharge
        delivery_method = form.cleaned_data.get('delivery_method')
        if delivery_method == 'post': # Check actual value in choices
             total_amount += 65
             
        # 2. Case Number (MerchantTradeNo)
        # ECPay requires unique MerchantTradeNo. Case Number might be reused if payment fails?
        # Usually append timestamp or random suffix if allowing retries. 
        # But User said: "MerchantTradeNo is the case number (e.g. RO-20260127-R001)"
        # We will use Case Number + a short timestamp suffix to avoid "Duplicate Trade No" error if they pay twice.
        # OR just Case Number if strict. User said "MerchantTradeNo is the case number".
        # Let's try Case Number first. If it fails due to duplicate, we might need a suffix.
        # Safe bet: CaseNumber_Timestamp or just CaseNumber.
        # Let's stick to User's request: "MerchantTradeNo is Case Number".
        # BUT relying on unique logic: if transaction exists, we might need new ID.
        # Let's assume Case Number is unique enough per attempt or we update the same one.
        # Wait, ECPay doesn't allow same TradeNo for different content/time usually.
        # I will append a short suffix just in case to ensure uniqueness if they retry.
        # actually, let's just use the case number for now as requested.
        
        merchant_trade_no = self.object.progress.case_number # e.g. RO-2026...
        # Check if we should append suffix to make it unique for ECPay
        import time
        # merchant_trade_no = f"{merchant_trade_no}{int(time.time())}" # Safer, but user said "IS the case number"
        
        # 3. Call Service
        from payment.services import create_payment
        from django.conf import settings
        
        # Return URL (Callback)
        return_url = self.request.build_absolute_uri(reverse('ecpay_callback'))
        
        # Client Back URL (Where user goes after payment) - Back to Progress Detail
        client_back_url = self.request.build_absolute_uri(
            reverse('registration:progress:edit', kwargs={'pk': self.object.progress.pk})
        )
        
        # If amount is 0, skip payment
        if total_amount <= 0:
             return redirect(self.get_success_url())

        html = create_payment(
            source_obj=self.object.progress, # Link to the Case
            amount=total_amount,
            merchant_trade_no=merchant_trade_no,
            return_url=return_url,
            client_back_url=client_back_url
        )
        
        return HttpResponse(html)

    def get_success_url(self):
        return reverse('registration:mandate:detail', kwargs={'pk': self.object.progress.pk})

    def get_success_url(self):
        return reverse('registration:mandate:detail', kwargs={'pk': self.object.progress.pk})
