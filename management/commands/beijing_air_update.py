from django.core.management.base import NoArgsCommand
from beijing_air import load

class Command(NoArgsCommand):
    
    help = "Gets latest updates on the smog in Beijing"
    
    def handle_noargs(self, **options):
        load.update()