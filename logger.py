import base64
from io import BytesIO
import matplotlib.pyplot as plt

class HtmlLogger:
    def __init__(self, name):
        self.name = name
        self.html = ''

    def add_line_little(self):
        self.html+="<hr>"

    def add_line_big(self):
        self.html += "<hr style=\"border_width:15;\">"
    def add_text(self, text):
        self.html += text + '<br>'

    def add_fig(self, fig):
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        self.html += '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '<br>'
        plt.close(fig)

    def close(self):
        filename = self.name + '.html'
        with open(filename, 'w') as f:
            f.write(self.html)