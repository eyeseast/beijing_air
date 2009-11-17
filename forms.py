import datetime
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

INPUT_FORMATS = list(forms.DEFAULT_DATE_INPUT_FORMATS)
INPUT_FORMATS.append('%m-%d-%Y')
INPUT_FORMATS.append('%m-%d-%y')
INPUT_FORMATS.append('%m/%d/%Y')
INPUT_FORMATS.append('%m/%d/%y')

class CalendarWidget(forms.DateInput):
    class Media:
        css = {
            'all': ('http://jqueryui.com/latest/themes/base/ui.all.css',)
        }
        
        js = (
            settings.MEDIA_URL + 'js/jquery-1.3.2.min.js',
            settings.MEDIA_URL + 'js/jquery-ui-1.7.2.custom.min.js',
        )

    def render(self, name, value, attrs=None):
        rendered = super(CalendarWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u"""<script type='text/javascript'>
            $(function() {
                $('#id_%s').datepicker({ dateFormat: 'yy-mm-dd' });
            });
            </script>""" % name)


class DateRangeForm(forms.Form):
    start = forms.DateField(input_formats=INPUT_FORMATS, widget=CalendarWidget, required=False)
    end = forms.DateField(input_formats=INPUT_FORMATS, widget=CalendarWidget, required=False)
