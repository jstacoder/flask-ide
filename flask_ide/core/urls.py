from core import core
from core.views import IndexView,MeetView,ContactView,TestView,AboutView,NewView,JsonRequestView


routes = [
    ((core,),
        ('',IndexView.as_view('index')),
        ('show/<layout_name>',IndexView.as_view('show_layout')),
        ('about',AboutView.as_view('about')),
        ('meet',MeetView.as_view('meet')),
        ('contact',ContactView.as_view('contact')),
        ('test',TestView.as_view('test')),
        ('new',NewView.as_view('new')),
        ('json',JsonRequestView.as_view('json')),
    )
]
