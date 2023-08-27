from django import template


register = template.Library()


# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(text):
    bad_words = ['Дурак', 'Редиска', 'Обормот']

    for i in bad_words:
        if i in text:
            text_new = text.replace(i, i[0] + '*' * (len(i) - 1))
        elif i.lower() in text:
            text_new = text.replace(i.lower(), i.lower()[0] + '*' * (len(i) - 1))
        else:
            text_new = text
    return text_new

