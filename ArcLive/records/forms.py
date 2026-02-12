from django.forms import ModelForm, CharField, ImageField
from .models import Record, Artist, Venue
from django import forms
from betterforms.multiform import MultiModelForm

#公演日・イベント名・参戦時の画像登録
class RecordForm(ModelForm):
    
    #artist_name = CharField(max_length=100, label="アーティスト名")
    #venue_name = CharField(max_length=100, required=False, label="会場名")
    
    class Meta:
        model = Record
        fields = ["live_date", "event_name", "live_image"]
        widgets = {'live_date':forms.DateInput(attrs={'type': 'date'})}
    
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
        
        
    
class RecordMultiForm(MultiModelForm):
    form_classes = {
        "record_form": RecordForm,
        "artist_form": ArtistForm,
        "venue_form": VenueForm
    }
#self.order_fields(['A','B'])にするとその順に並び替えてくれる
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.field_names(["record_form/live_date", "artist_form/name","record_form/event_name","venue_form/name","record_form/live_image"])
        self.forms['record_form'].fields['live_date'].widget=forms.DateInput(attrs={'type': 'date'})



class SearchForm(forms.Form):

    aritst = forms.CharField(
        initial='',
        label='アーティスト名などのキーワード',
        required = False, # 必須ではない
    )