from django.forms import ModelForm, CharField, ImageField
from .models import Record, Artist, Venue,Artist_Record
from django import forms
from betterforms.multiform import MultiModelForm
from django.forms import inlineformset_factory

#画像生成・文章生成
class GenerateForm(forms.Form):
    #年月日の選択
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1950, 2100)),
        label="開始日"
    )
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1950, 2100)),
        label="終了日"
    )
    #色の選択
    color = forms.ChoiceField(
        choices=[
            ('black', '黒'),
            ('gray', 'グレー'),
            ('white', '白'),
            ('red', '赤'),
            ('pink', 'ピンク'),
            ('yellow', '黃'),
            ('green', '緑'),
            ('blue', '青'),
        ],
        label="色を選択"
    )
    
    #フォントの選択
    font = forms.ChoiceField(
        choices=[
            ('hiragino', 'ヒラギノ角ゴシック'),
            ('Noto Sans', 'Noto Sans'),
            ('Noto Serif', 'Noto Serif'),
            ('M Plus 1p', 'M Plus 1p'),
            ('Oswald', 'Oswald'),
            ('Roboto', 'Roboto'),
        ],
        label="フォントを選択"
    )
    
    #画像の選択
    user_image = forms.ImageField(required=False, label="端末から選んだ画像")
    selected_preset_id = forms.CharField(required=False, label="アプリ内で選んだ画像のID")
    


#公演日・イベント名・参戦時の画像登録
class RecordForm(ModelForm):
    
    #artist_name = CharField(max_length=100, label="アーティスト名")
    #venue_name = CharField(max_length=100, required=False, label="会場名")
    
    class Meta:
        model = Record
        fields = ["live_date", "event_name", "live_image"]
        widgets = {
            'live_date': forms.TextInput(attrs={
                'data-date-picker': '',
                'placeholder': '日付を選択',
                'autocomplete': 'off',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



# アーティスト入力用のフォームを定義
class Artist_RecordForm(forms.ModelForm):
    artist_name = forms.CharField(
        label="アーティスト名",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Artist_Record
        fields = [] # 中間テーブルのフィールドは出さない

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 編集画面の時、既に登録されているアーティスト名を初期値に入れる
        if self.instance and getattr(self.instance, 'artist_id',None):
            self.fields['artist_name'].initial = self.instance.artist_id.name

#Record(親) と Artist_Record(子) の紐付け用フォームセット
ArtistFormSet = inlineformset_factory(
    Record, Artist_Record,
    form=Artist_RecordForm, # 自作フォームを適用
    extra=1,               # 既存データのみ表示
    can_delete=True
)



class RecordMultiForm(MultiModelForm):
    form_classes = {
        'record_form': RecordForm,
        'venue_form': VenueForm,
        'artist_formset': ArtistFormSet, 
    }
#self.order_fields(['A','B'])にするとその順に並び替えてくれる
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.field_names(["record_form/live_date", "artist_form/name","record_form/event_name","venue_form/name","record_form/live_image"])
        #self.forms['record_form'].fields['live_date'].widget=forms.DateInput(attrs={'type': 'date'})



class SearchForm(forms.Form):

    aritst = forms.CharField(
        initial='',
        label='アーティスト名などのキーワード',
        required = False, # 必須ではない
    )