from django.conf import settings
from django.template import TemplateSyntaxError, VariableDoesNotExist, Node
from django.template import Library, Variable, loader, Context

# ID of current flowplayer being rendered (global to ensure unique)
FLOWPLAYER_ITERATOR =0

register = Library()

class FlowPlayerNode(Node):
    "Renderer class for the flowplayer template tag."
    
    def __init__(self, media_url, player_class):
        """
        Constructor.

        Parameters:

            file_url
                Video url.
            player_url
                Flowplayer url.
        """
        self.player_class = player_class
        self.media_url = Variable(media_url)    
    
        global FLOWPLAYER_ITERATOR
        FLOWPLAYER_ITERATOR += 1
        self.player_id = FLOWPLAYER_ITERATOR

        if settings.FLOWPLAYER_URL:
            self.player_url = settings.FLOWPLAYER_URL
        else:
            self.player_url = "%sflowplayer/FlowPlayerLight.swf" % (settings.MEDIA_URL)

    def render(self, context):

        try:           
            media_url = self.media_url.resolve(context) 
        except VariableDoesNotExist:
            media_url = self.media_url   

        t = loader.get_template('flowplayer/flowplayer.html')
        code_context = Context(
                            {"player_url": self.player_url,
                             "player_id": self.player_id,
                             "player_class": self.player_class,
                             "media_url": media_url,
                            }, autoescape=context.autoescape)
        return t.render(code_context)

def do_flowplayer(parser, token):
    """
    This will insert an flash-based flv videoplayer (flowplayer) in form of an <object>
    code block.

    Usage::

        {% flowplayer media_url %}

    Example::
    
        {% flowplayer video.flv %}        
    
    By default, 'flowplayer' tag will use FlowPlayerLight.swf found at  
    ``{{ MEDIA_URL }}flowplayer/FlowPlayerLight.swf``.
    
    To change this add FLOWPLAYER_URL to your settings.py file

    Pass a dict of urls to the player to get a playlisted player instance
    
    """    
   
    args = token.split_contents()
    
    if len(args) < 2:
        raise TemplateSyntaxError, "'flowplayer' tag requires at least one argument."            
    
    if len(args) == 3:
        player_class = args[2]
    else:
        player_class = None

    media_url = args[1]
    
    return FlowPlayerNode(media_url, player_class)


# register the tag 
register.tag('flowplayer', do_flowplayer)

