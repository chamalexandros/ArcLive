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
from accounts.models import Preset_Image
from django.utils import timezone

class HomeView(LoginRequiredMixin, View):
    #過去、今年、未来（今日以降）の参戦記録本数をカウント
    def get(self,request, *args, **kwargs):
        today = timezone.now().date()
        past_count = Record.objects.filter(user_id=request.user,live_date__lt=today).count()
        this_year_count = Record.objects.filter(user_id=request.user,live_date__year=today.year).count()
        future_count = Record.objects.filter(user_id=request.user,live_date__gte=today).count()
        
        presetimage = Preset_Image.objects.all()
        
        is_generate_clicked = request.GET.get('generate_btn')
        
        start_date = request.GET.get('start-date')
        end_date = request.GET.get('end-date')
        
        #デフォルトは全件
        records = Record.objects.filter(user_id=request.user)
        # 開始日以降全て
        if start_date and not end_date:
            records = records.filter(live_date__gte=start_date)
        #終了日以前全て
        elif not start_date and end_date:
            records = records.filter(live_date__lte=end_date)
        #開始日～終了日
        if start_date and end_date:
            records = records.filter(live_date__range=[start_date, end_date])
            
        generate_text = ""
        if is_generate_clicked:
            for r in records.order_by('live_date'):
                date_str = r.live_date.strftime('%m/%d')
                artist_names = []
                for ar in r.artist_records.all():
                    artist_names.append(ar.artist_id.name)
                artists_display = "/".join(artist_names) if artist_names else "アーティスト不明"
                line =f"{date_str} {artists_display} {r.event_name}\n"
                generate_text += line
        
        context = {
            'past_count': past_count,
            'this_year_count': this_year_count,
            'future_count': future_count,
            'presetimage' : presetimage,
            'record_list': records.order_by('live_date'),
            'generate_text' : generate_text,
        }
        
        if generate_text:
            return render(request, 'records/generate_text.html',context)
        
        return render(request, 'records/home.html',context)


class GenerationDeleteView(View):
    def post(self,request):
        return redirect('home')
        
        



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
            
            venue, created = Venue.objects.get_or_create(name=venue.name)
            
            record.user_id = request.user
            record.venue_id = venue
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
        #artist_link = Artist_Record.objects.filter(record_id=record).first()
        #artist = artist_link.artist_id if artist_link else None
        #venue =  record.venue_id
        #form = RecordMultiForm(request.POST, request.FILES, instance={
            #'record_form':record,
            #'artist_form':artist,
            #'venue_form':venue
            #})
        record.delete()
        return redirect("records:record_list")
        #return render(request, "records/record_confirm_delete.html", {"record": record, "form":form})

    def post(self, pk):
        record = get_object_or_404(Record, id=pk)
        record.delete()
        return redirect("records:record_list")


home =HomeView.as_view()
generate_delete = GenerationDeleteView.as_view()
record_create = RecordCreateView.as_view()
record_list = RecordListView.as_view()
record_edit = RecordEditView.as_view()
record_update = RecordUpdateView.as_view()
record_delete = RecordDeleteView.as_view()