from urllib.parse import urlparse, parse_qs
from django import template

register = template.Library()

@register.filter
def youtube_embed(url: str) -> str:
    """
    Принимает:
      - https://www.youtube.com/watch?v=ID&...
      - https://youtu.be/ID
      - https://www.youtube.com/embed/ID
    Возвращает чистый embed URL:
      https://www.youtube.com/embed/ID?rel=0&modestbranding=1
    """
    if not url:
        return ''
    parsed = urlparse(url)
    video_id = ''
    # youtu.be/ID
    if 'youtu.be' in parsed.netloc:
        video_id = parsed.path.lstrip('/')
    # youtube.com/watch?v=ID
    elif 'youtube.com' in parsed.netloc:
        qs = parse_qs(parsed.query)
        video_id = qs.get('v', [''])[0]
    # уже embed/ID
    elif 'youtube.com' in parsed.netloc and '/embed/' in parsed.path:
        video_id = parsed.path.rsplit('/', 1)[-1]
    if not video_id:
        return ''
    return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1'
