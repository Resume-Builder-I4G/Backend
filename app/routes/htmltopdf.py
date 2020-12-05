'''
    Module that handles view of everything that has to 
    do with converting the html template to pdf
'''

import pdfkit
from app import app

def render_pdf(html, name):
    css = [
        # os.path.join(app.root_path, 'static/css/bootstrap.min.css'),
        # os.path.join(app.root_path, 'static/css/styles.css'),
        # os.path.join(app.root_path, 'static/assets/navbar.css'),
        # os.path.join(app.root_path, 'static/assets/gemheart.css'),
        # os.path.join(app.root_path, 'static/js/jquery-2.1.4.min.js'),
        # os.path.join(app.root_path, 'static/js/bootstrap.min.js'),
        # os.path.join(app.root_path, 'static/assets/app.js'),
        # os.path.join(app.root_path, 'static/assets/images/Ellipse 8.png')
        # "https://kit.fontawesome.com/dc7f1f050e.js"
    ]
    js = [
        
    ]
    options =options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'enable-local-file-access': True
    } 
    config=pdfkit.configuration(wkhtmltopdf = app.config['PDF_TO_HTML'])
    pdf=pdfkit.from_string(html, f'app/templates/pdf/{name}',
                        configuration=config, css=css,
                        options=options)
    return pdf