from django.conf import settings
from django.template import TemplateSyntaxError, VariableDoesNotExist, Node
from django.template import Library, Variable, loader, Context

# ID of current flowplayer being rendered (global to ensure unique)
FLOWPLAYER_ITERATOR =0

register = Library()

class FlowPlayerNode(Node):
    "Renderer class for the flowplayer template tag."
    
    def __init__(self, media, player_class):
        """
        Constructor.

        Parameters:

            media
                Media file url OR an array of urls
            player_class
                Type of player to show (changes css class and config source)
        """
        self.player_class = player_class
        self.media = Variable(media)

        global FLOWPLAYER_ITERATOR
        FLOWPLAYER_ITERATOR += 1
        self.player_id = FLOWPLAYER_ITERATOR

        if settings.FLOWPLAYER_URL:
            self.player_url = settings.FLOWPLAYER_URL
        else:
            self.player_url = "%sflowplayer/FlowPlayerLight.swf" % (settings.MEDIA_URL)

        # Import the configuration settings to set on the player output
        # Configuration is defined in the settings (multiple types of player)
        if 'default' in settings.FLOWPLAYER_CONFIG:
            self.player_config = settings.FLOWPLAYER_CONFIG['default']
        else:
            self.player_config = dict()

        if player_class in settings.FLOWPLAYER_CONFIG:
            self.player_config.update(settings.FLOWPLAYER_CONFIG[player_class])

    def render(self, context):
        try:           
            # Try resolve this variable in the template context
            self.media = self.media.resolve(context) 
        except VariableDoesNotExist:
            # Cannot resolve, therefore treat as url string
            pass
        
        # Have we got an array or a string?
        if isinstance(self.media, list):
            # Can resolve, push first url into the url variable
            self.media_url = self.media[0]
            self.media_playlist = self.media
        else:
            self.media_url = self.media
            self.media_playlist = False

        t = loader.get_template('flowplayer/flowplayer.html')
        code_context = Context(
                            {"player_url": self.player_url,
                             "player_id": self.player_id,
                             "player_class": self.player_class,
                             "player_config": self.player_config,
                             "media_url": self.media_url,
                             "media_playlist":self.media_playlist
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

    media = args[1]
    
    return FlowPlayerNode(media, player_class)


# register the tag 
register.tag('flowplayer', do_flowplayer)

