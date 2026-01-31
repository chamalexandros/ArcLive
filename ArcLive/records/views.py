from django.shortcuts import render, redirect
from django.views import View
from .forms import RecordForm

class HomeView(View):
    def get(self, request):
        return render(request, 'records/home.html')


class RecordCreateView(View):
    def get(self, request):
        form = RecordForm()
        return render(request, "records/recordcreate_form.html", {"form":form})
    
    def post(self, request):
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user_id = request.user
            form.save()
            return redirect("records:home")
        return render(request, "records/recordcreate_form.html", {"form": form})

home =HomeView.as_view()
recordcreate = RecordCreateView.as_view()
    


