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
            objects = form.save(commit=False)
            record = objects['record_form']
            artist = objects['artist_form']
            venue = objects['venue_form']
            
            #Artistの重複を防ぐ
            artist, created = Artist.objects.get_or_create(name=artist.name)
            artist.save()
            
            venue, created = Venue.objects.get_or_create(name=venue.name)
            
            venue.save()
            
            record.user_id = request.user
            record.save()
            
            Artist_Record.objects.get_or_create(
                record_id=record,
                artist_id=artist
            )
            
            form.save_m2m()
            return redirect("records:home")
        print(f"バリデーションエラーが発生した{form.errors}")
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
        date_min = self.request.GET.get('start_date')
        date_max = self.request.GET.get('end_date')

        record_list = Record.objects.all()
    
        if date_min and date_max:
            record_list = Record.objects.filter(live_date__range=[date_min, date_max]).order_by('live_date') #両方入力
            print(record_list)
            
        elif date_min:
            record_list = Record.objects.filter(live_date__gte=date_min).order_by('live_date') #開始日以降の全て
            print(record_list)
            
        elif date_max:
            record_list = Record.objects.filter(live_date__lte=date_max).order_by('live_date')#終了日以前の全て
            print(record_list)
        else:
            record_list = Record.objects.all() #全て
            print(record_list)
            
            record_list = record_list.prefetch_related('artist_records__artist_id')
            
        context = {
            "record_list":record_list.order_by('-live_date'),
            "searched" : True
            }


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
    def get(self, request, pk):
        record = get_object_or_404(Record, pk=pk)
        artist_link = Artist_Record.objects.filter(record_id=record).first()
        artist = artist_link.artist_id if artist_link else None
        venue =  record.venue_id
        form = RecordMultiForm(instance={
            'record_form':record,
            'artist_form':artist,
            'venue_form':venue
            })
        return render(request, "records/record_edit.html", {"record": record,"form":form})


class RecordUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        record = get_object_or_404(Record, pk=pk)
        artist_link = Artist_Record.objects.filter(record_id=record).first()
        artist = artist_link.artist_id if artist_link else None
        venue =  record.venue_id
        form = RecordMultiForm(instance={
            'record_form':record,
            'artist_form':artist,
            'venue_form':venue
            })
        return render(request, "records/record_update.html", {"record": record, "form": form})
    
    def post(self,request, pk):
        record = get_object_or_404(Record, pk=pk)
        artist_link = Artist_Record.objects.filter(record_id= record).first()
        artist = artist_link.artist_id if artist_link else None
        venue =  record.venue_id
        form = RecordMultiForm(request.POST, request.FILES, instance={
            'record_form':record,
            'artist_form':artist,
            'venue_form':venue,
            })
        if form.is_valid():
            r_data = form['record_form'].save(commit=False)
            v_data = form['venue_form'].save()
            
            r_data.venue_id = v_data
            r_data.save()
            
            a_data = form['artist_form'].save()
            Artist_Record.objects.update_or_create(
                record_id=r_data,
                defaults={'artist_id':a_data}
            )
            
            return redirect("records:record_list")
        return render(request, "records/recordcreate_form.html", {"form": form})

class RecordDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        record = get_object_or_404(Record, id=pk)
        artist_link = Artist_Record.objects.filter(record_id=record).first()
        artist = artist_link.artist_id if artist_link else None
        venue =  record.venue_id
        form = RecordMultiForm(request.POST, request.FILES, instance={
            'record_form':record,
            'artist_form':artist,
            'venue_form':venue
            })
        return render(request, "records/record_confirm_delete.html", {"record": record, "form":form})

    def post(self, pk):
        record = get_object_or_404(Record, id=pk)
        record.delete()
        return redirect("records:record_list")


home =HomeView.as_view()
record_create = RecordCreateView.as_view()
record_list = RecordListView.as_view()
record_edit = RecordEditView.as_view()
record_update = RecordUpdateView.as_view()
record_delete = RecordDeleteView.as_view()
