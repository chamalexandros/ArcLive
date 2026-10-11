from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from .forms import RecordForm
from .models import Record
from django.db.models import Count
from .models import Artist_Record
from .models import Artist
from .models import Venue
from .models import Design_Setting
from .forms import RecordMultiForm, ArtistFormSet,VenueForm
from accounts.models import Preset_Image
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy



class HomeView(LoginRequiredMixin, View):
    template_name = 'records/record_list.html'
    model = Record
    context_object_name = 'record_list'

    def get(self, request, *args, **kwargs):
        # --- ①の処理(カウントとプリセット画像) ---
        today = timezone.now().date()
        past_count = Record.objects.filter(user_id=request.user, live_date__lt=today).count()
        this_year_count = Record.objects.filter(user_id=request.user, live_date__year=today.year).count()
        future_count = Record.objects.filter(user_id=request.user, live_date__gte=today).count()
        presetimage = Preset_Image.objects.all()

        # --- ②の処理(期間検索) ---
        date_min = self.request.GET.get('start_date')
        date_max = self.request.GET.get('end_date')

        if date_min and date_max:
            record_list = Record.objects.filter(live_date__range=[date_min, date_max]).order_by('live_date')
        elif date_min:
            record_list = Record.objects.filter(live_date__gte=date_min).order_by('live_date')
        elif date_max:
            record_list = Record.objects.filter(live_date__lte=date_max).order_by('live_date')
        else:
            record_list = Record.objects.all().order_by('-live_date')

        record_list = record_list.prefetch_related('artist_records__artist_id')

        # --- ①と②のcontextを1つにまとめる ---
        context = {
            'past_count': past_count,
            'this_year_count': this_year_count,
            'future_count': future_count,
            'presetimage': presetimage,
            'record_list': record_list,
            'searched': True,
        }

        return render(request, 'records/home.html', context)

def generate_view(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        color = request.POST.get('color')
        font = request.POST.get('font')
        uploaded = request.FILES.get('background_image')
        preset_id = request.POST.get('selected_preset_id')

        request.session['gen_start_date'] = start_date
        request.session['gen_end_date'] = end_date
        request.session['gen_color'] = color
        request.session['gen_font'] = font

        if uploaded:
            # 端末からの画像はメディアフォルダに保存
            from django.core.files.storage import default_storage
            path = default_storage.save('generated_bg/' + uploaded.name, uploaded)
            image_url = default_storage.url(path)
        elif preset_id:
            preset = Preset_Image.objects.get(id=preset_id)
            image_url = preset.preset_image_url.url
        else:
            image_url = ''

        request.session['gen_background_url'] = image_url

        return redirect('records:display_result')

    return redirect('records:home')

def display_result_view(request):
    start_date = request.session.get('gen_start_date')
    end_date = request.session.get('gen_end_date')
    color = request.session.get('gen_color', '#000000')
    font = request.session.get('gen_font', 'sans-serif')
    background_url = request.session.get('gen_background_url', '')

    record_list = Record.objects.filter(user_id=request.user)
    if start_date and end_date:
        record_list = record_list.filter(live_date__range=[start_date, end_date])
    elif start_date:
        record_list = record_list.filter(live_date__gte=start_date)
    elif end_date:
        record_list = record_list.filter(live_date__lte=end_date)
    # 両方とも無ければ、絞り込みをせず全件のまま

    record_list = record_list.order_by('live_date').prefetch_related('artist_records__artist_id')

    context = {
        'record_list': record_list,
        'color': color,
        'font': font,
        'background_url': background_url,
    }
    return render(request, 'records/display_result.html', context)



class RecordCreateView(LoginRequiredMixin, View):   
    def get(self, request):
        # 画面を表示する時
        return render(request, "records/recordcreate_form.html", {
            "form": RecordForm(),
            "venue_form": VenueForm(),
            "artist_formset": ArtistFormSet(),
        })

    def post(self, request):
        form = RecordForm(request.POST, request.FILES)
        venue_form = VenueForm(request.POST)
        artist_formset = ArtistFormSet(request.POST)

        if form.is_valid() and venue_form.is_valid() and artist_formset.is_valid():
            # 1. 会場の重複チェック
            v_name = venue_form.cleaned_data['name']
            venue_obj, _ = Venue.objects.get_or_create(name=v_name)

            # 2. Record本体の保存
            record = form.save(commit=False)
            record.user_id = request.user
            record.venue_id = venue_obj # 重複チェック済みの会場をセット
            record.save()

            # 3. アーティストの重複チェックと保存
            # フォームセットの中身を一つずつ取り出す
            for a_form in artist_formset:
                if a_form.cleaned_data and not a_form.cleaned_data.get('DELETE'):
                    # フォームに入力されたアーティスト名を取得
                    artist_name = a_form.cleaned_data.get('artist_name') 

                    print("=== デバッグ ===")
                    print("cleaned_data:", a_form.cleaned_data)
                    print("artist_name:", repr(artist_name))
                    print("================")
                    
                    # アーティストを重複チェックして取得/作成
                    artist_obj, _ = Artist.objects.get_or_create(name=artist_name)

                    # 中間テーブル（Artist_Record）に紐付け
                    Artist_Record.objects.get_or_create(
                        record_id=record,
                        artist_id=artist_obj
                    )
            
            return redirect("records:home")

        return render(request, "records/recordcreate_form.html", {
            "form": form,
            "venue_form": venue_form,
            "artist_formset": artist_formset,
        })
        
        

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



class RecordDetailView(LoginRequiredMixin, generic.DetailView):
    model = Record
    template_name = 'records/record_detail.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 2つ目のモデルを指定
        ctx["Artist"] = Artist.objects.all()
        return ctx


class RecordUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Record
    template_name = 'records/record_update.html'
    form_class = RecordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venue_form'] = VenueForm(initial={'name':self.object.venue_id.name})
        context['artist_formset'] = ArtistFormSet(instance=self.object)
        return context
    def form_valid(self, form):
        # 1. 会場とアーティストのデータを取得
        v_form = VenueForm(self.request.POST, instance=self.object.venue)
        a_formset = ArtistFormSet(self.request.POST, instance=self.object)

        # 2. 全部正しければ保存（これで「全部反映」されます）
        if v_form.is_valid() and a_formset.is_valid():
            v_form.save()
            a_formset.save()
            return super().form_valid(form) # 最後に Record 本体を保存
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # 1. 会場名の処理（自由入力された名前から会場データを特定・作成）
        # テンプレートの会場名入力欄の 'name' 属性に合わせて取得
        v_name = self.request.POST.get('venue_name') 
        if v_name:
            # 名前で検索して取得、なければ新規作成
            venue, created = Venue.objects.get_or_create(name=v_name)
            # 親の Record インスタンスに会場をセット
            form.instance.venue_id = venue 

        # 2. 親（Record：公演日、公演名、画像）の保存
        # ここで live_date, event_name, live_image などが保存されます
        response = super().form_valid(form)
        
        # 3. アーティストの処理（FormSet）
        a_formset = ArtistFormSet(self.request.POST, instance=self.object)
    
        if a_formset.is_valid():
            # 削除チェックが入ったものを先に消す
            for obj in a_formset.deleted_objects:
                obj.delete()

            # 各アーティストフォームの処理
            instances = a_formset.save(commit=False)
            for a_form in a_formset:
                # 削除フラグが立っていないものだけ処理
                if not a_form.cleaned_data.get('DELETE'):
                    name = a_form.cleaned_data.get('artist_name')
                    if name:
                        # アーティスト名で検索 or 作成
                        artist, created = Artist.objects.get_or_create(name=name)
                        # 中間テーブル（Artist_Record）に紐付け
                        a_form.instance.artist_id = artist
                        a_form.instance.record_id = self.object
                        a_form.instance.save()

        return response


    def get_success_url(self):
        # 4. 更新完了後、どのページに飛ばすか。pkが必要な場合はここで指定
        # 例：詳細画面に戻る場合
        return reverse_lazy('records:record_detail', kwargs={'pk': self.object.pk})
        # 例：もし一覧画面のURLにpkが含まれる設計なら、前のコードの通り self.kwargs['pk'] を使います

    # URLが動的に変化するページに遷移する場合に用いる
    def get_success_url(self):
        return reverse_lazy('records:record_list', kwargs={'pk': self.kwargs['pk']})
    
    # 処理が成功した時に実行される
        def form_valid(self, form):
            messages.success(self.request, '参戦記録を更新しました')
            return super().form_valid(form)
    
    # 処理が失敗した時に実行される
        def form_invalid(self, form):
            messages.error(self.request, '参戦記録の更新に失敗しました')
            return super().form_invalid(form)
    
    

class RecordDeleteView(LoginRequiredMixin, generic.View):
    
    def get(self, request, pk):
        record = get_object_or_404(Record, id=pk)
        record.delete()
        return redirect("records:record_list")
        

home =HomeView.as_view()
record_create = RecordCreateView.as_view()
record_list = RecordListView.as_view()
record_detail = RecordDetailView.as_view()
record_update = RecordUpdateView.as_view()
record_delete = RecordDeleteView.as_view()