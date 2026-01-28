from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from registration.models import RegistrationProgress, RegistrationAML
from .forms import RegistrationAMLForm

@login_required
def aml_update(request, pk):
    # pk is RegistrationProgress id
    progress = get_object_or_404(RegistrationProgress, pk=pk)
    
    # Get or Create AML Record
    aml, created = RegistrationAML.objects.get_or_create(progress=progress)
    
    if request.method == 'POST':
        form = RegistrationAMLForm(request.POST, instance=aml)
        if form.is_valid():
            form.save()
            messages.success(request, '洗錢防制資料已更新')
            return redirect('registration:progress:edit', pk=pk)
    else:
        form = RegistrationAMLForm(instance=aml)
    
    context = {
        'form': form,
        'progress': progress,
        'is_aml': True
    }
    return render(request, 'aml/form.html', context)
