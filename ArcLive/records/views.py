from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import RecordForm
from .models import Record
from django.db.models import Count
from .models import Artist_Record
from .models import Artist
from .models import Venue
from .models import Design_Setting
from .forms import RecordMultiForm


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'records/home.html')


class RecordCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = RecordMultiForm()
        return render(request, "records/recordcreate_form.html", {"form":form})
    
    def post(self, request):
        form = RecordMultiForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.user_id = request.user
            form.save()
            return redirect("records:home")
        return render(request, "records/recordcreate_form.html", {"form": form})


    #def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["records"] = Record.objects.all()
        ctx["Artists"] = Artist.objects.all()
        ctx["Venues"] = Venue.objects.all()
        return ctx



class RecordListView(LoginRequiredMixin, View):
    template_name = 'records/record_list.html'
    model = Record
    context_object_name = 'record_list' #デフォルトがobject_listなので名前を変えない場合は本来これは記載しなくてもいい
    
    #指定期間による検索
    def get(self, request, *args, **kwargs):
        date_min = self.request.GET.get('date_min')
        date_max = self.request.GET.get('date_max')

        record_list = Record.objects.all()
        
        if date_min and date_max:
            record_list = Record.objects.filter(live_date__range=[date_min, date_max]).order_by('live_date') #両方入力
        elif date_min:
            record_list = Record.objects.filter(live_date__gte=date_min).order_by('live_date') #開始日以降の全て
            
        elif date_max:
            record_list = Record.objects.filter(live_date__lte=date_max).order_by('live_date')#終了日以前の全て
        else:
            record_list = Record.objects.all() #全て

    #検索結果からアーティストごとの参戦記録をカウント(本数が多い順に表示)
        artist_summary = record_list.values('artist_records__artist_id__name').annotate(
            post_count=Count('artist_records')).order_by('-post_count')
        context = {
            "record_list":record_list.order_by('-live_date'),
            "artist_summary": artist_summary,
            "searched" : True
            }
        
        return render(
            request=request,
            template_name="records/record_list.html",
            context=context,
            )



class RecordEditView(LoginRequiredMixin, View):
    def get(self, request, id):
        record = get_object_or_404(Record, id=id)
        return render(request, "records/record_edit.html", {"Record": record})


class RecordUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        record = get_object_or_404(Record, id=id)
        form = RecordForm(instance=record)
        return render(request, "records/record_update.html", {"Record": record})
    
    def post(self,request, id):
        record = get_object_or_404(Record, id=id)
        form = RecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect("records:record_edit", id=id)
        return render(request, "records/recordcreate_form.html", {"form": form})

class RecordDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        record = get_object_or_404(Record, id=id)
        return render(request, "records/record_confirm_delete.html", {"Record": record})

    def post(self,request, id):
        record = get_object_or_404(Record, id=id)
        return redirect("records:recordlist")


home =HomeView.as_view()
recordcreate = RecordCreateView.as_view()
recordlist = RecordListView.as_view()
recordedit = RecordEditView.as_view()
recordupdate = RecordUpdateView.as_view()
recorddelete = RecordDeleteView.as_view()
