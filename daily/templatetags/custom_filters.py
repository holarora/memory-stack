from django import template
import re

register = template.Library()

japanese_weekdays = {0: "月", 1: "火", 2: "水", 3: "木", 4: "金", 5: "土", 6: "日"}


@register.filter
def japanese_weekday(date):
    return f"({japanese_weekdays[date.weekday()]})"

@register.filter
def is_chinese_only(text):
    if not text:
        return False
    chinese_chars = re.search(r'[\u4e00-\u9fff]', text)
    japanese_chars = re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text)
    return bool(chinese_chars) and not japanese_chars