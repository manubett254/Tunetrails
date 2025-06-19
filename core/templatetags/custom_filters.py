from django import template

register = template.Library()

@register.filter
def youtube_embed(url):
    return url.replace("watch?v=", "embed/")

from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    if not url:
        return ""
    if "watch?v=" in url:
        return url.replace("watch?v=", "embed/").split("&")[0]
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    return url
