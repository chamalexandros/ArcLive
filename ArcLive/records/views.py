from django.shortcuts import render, redirect
from django.views import View
from .forms import RecordForm
from .models import Record
from .models import Artist_Record
from .models import Artist
from .models import Venue
from .models import Design_Setting
from django.db.models import Count



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


class RecordListView(View):
    def get(self, request):
        #指定期間の入力が空欄だった場合
        #検索前
        if not request.GET:
            record_list = None
        else:
            #空欄のまま検索した場合
            record_list = Record.objects.all().order_by('-live_date')
            
            #値が開始日、終了日どちらかでも入力ありのときは絞り込み
            start = request.GET.get('start_date','1900-01-01')
            end = request.GET.get('end_date','2099-12-31')
            
            if start:
                record_list = record_list.filter(live_date__gte=start)
            if end:
                record_list = record_list.filter(live_date__lte=end)         
            
        #検索結果からアーティストごとの参戦記録をカウント(本数が多い順に表示)
        ranking = record_list.values('artist_id__name').annotate(Count('artist_id__name')).order_by('-total')
        return render(
            request, 
            "records/record_list.html", 
            {"record_list": record_list}, 
            {"ranking": ranking}
            )



home =HomeView.as_view()
recordcreate = RecordCreateView.as_view()
recordlist = RecordListView.as_view()
    


