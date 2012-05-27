from config import STATIC_FILE_URL
from web.contrib.template import render_jinja


render = render_jinja('templates',encoding = 'utf-8',)
render._lookup.globals.update(STATIC_FILE_URL=STATIC_FILE_URL,)



