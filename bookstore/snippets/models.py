from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
# sort 是应用在 list 上的方法，sorted 可以对所有可迭代的对象进行排序操作。
# list 的 sort 方法返回的是对已经存在的列表进行操作，而内建函数 sorted 方法返回的是一个新的 list，而不是在原来的基础上进行的操作。
LANGUAGE_CHOICES = sorted([(item[1][0],item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item,item) for item in get_all_styles())

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    # 显示出哪个用户创建里snippet数据。  迁移数据库时需要创建一个用户，外键的关联没有对象！！！
    # 另一个字段将用于HTML代码高亮。
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()
    
    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):

        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)