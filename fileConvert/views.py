from django.shortcuts import render
from .forms import PdffileForm
from django.shortcuts import redirect

# Create your views here.
def upload(request):

    form = PdffileForm()

    if request.method == 'POST':
        form = PdffileForm(request.POST, request.FILES)
        # if form is not valid then form data will be sent back to view to show error message
        if form.is_valid():
            form.save()
            return redirect('upload')

    return render(request, "uploadform.html", {'form': form})