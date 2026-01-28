from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from registration.models import RegistrationProgress, RegistrationMandate
from .forms import RegistrationMandateForm

@login_required
def mandate_update(request, pk):
    # pk is RegistrationProgress id
    progress = get_object_or_404(RegistrationProgress, pk=pk)
    
    # Get or Create Mandate
    mandate, created = RegistrationMandate.objects.get_or_create(progress=progress)
    
    if request.method == 'POST':
        form = RegistrationMandateForm(request.POST, instance=mandate)
        if form.is_valid():
            form.save()
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
