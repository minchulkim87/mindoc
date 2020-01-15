"""
# mindoc

A minimalistic python documentation module

* [GitHub page](https://minchulkim87.github.io/mindoc/)
* [Source code](https://github.com/minchulkim87/mindoc)

This program converts a .py file into a .html file to minimally document python code.

The purpose is to minimise documentation and to enable writing document-like .py files without a heavy imposition of the docstring burden.

Simply write the .py file as if you would a markdown file, but instead of writing the code blocks between text, write the text between codes.

This tool also helps automatically generate a table of contents and cross-referencing.

[TOC]

## Requirements

### Packages

I tried to minimise the dependencies by using standard python libraries or standard packages within the Anaconda distribution. If you are not using the Anaconda distribution, these packages are required on top of the standard python libraries.

* **mistune**: part of the Anaconda distribution
* **beautifulsoup4**: part of the Anaconda distribution


### .py Code style

The .py file to be converted must have been written in the following very specific way:

* All .py must must begin with a fenced triplet of double quotes (&quot;&quot;&quot;).
* All comment blocks, i.e. the documentation sections, must also use fenced triplet of double quotes.
* You may use markdown syntax within the documentation sections.
* All other comment strings will not be converted (#, ', ''', ").
* If you want triplet quote blocks untouched, use the triplet of single quotes (''').
* Place a [TOC] in the line you want the table of contents to be placed.
* If you type in the exact (case-sensitive) string of the header anywhere within the documentation sections, it will be linked to the header automatically.

**Warning!**

You cannot use fenced triplet of double quotes as code if you want to document this way.


## How to use

Install from github.

> pip install git+https://github.com/minchulkim87/mindoc.git@master

Then use the command from terminal

> mindoc [-w] [file to the .py file to convert, can use glob]

For example:

> mindoc mindoc.py

produces this documentation.


*Without* installing mindoc,  you would need to install the required packages above.

I assume they can be installed with the following:

> pip install mistune

> pip install beautifulsoup4


1. Download the mindoc.py file to the directory you are working in.
2. Open your terminal and navigate to the directory where the mindoc.py file is.
3. Type the following command into the terminal

> python -m mindoc [-w] [file path to the .py file to convert, can use glob]



# The code

### Imports
"""
import os
import sys
import glob
import re
import itertools
import argparse
import subprocess
import time
import mistune

"""
## Conversion from py to doc

### 1 Read the .py file
"""
def get_py_code(file_path) -> str:
    py_file = open(file_path, 'r')
    py = py_file.read()
    py_file.close()
    return py

"""
### 2 Convert the python blocks into collapsibles

This function also "separates" what is documentation from what is code.
"""
def convert_python_blocks(code: str) -> str:
    replace_with_pre = u'<'+u'br'+u'>'+u'<'+u'br'+u'>'+u'<'+u'button type="button" class="collapsible" style="width: 80px; text-align:center; margin-bottom:0px;"'+u'>'+u'View code'+u'<'+u'/button'+u'>'+u'<'+u'div style=" margin-top:0px;" class="content"'+u'>'+u'\n```'+u'python\n'
    replace_with_post = u'```\n'+u'<'+u'/div'+u'>\n'
    
    pre_html = code.replace('"""'+'\n', '', 1)
    pre_html = replace_every_nth(pre_html, '"""'+'\n', replace_with_pre, nth=2)
    pre_html = pre_html.replace('"""'+'\n', replace_with_post)
    pre_html = pre_html + replace_with_post
    return pre_html

"""
### 3 Convert the code to a html doc

This function converts the documentation strings into html code, converting the markdown syntax into html.

The function also styles the document.
"""
def convert_to_html(pre_html: str) -> str:
    meta = u'<'+u'meta name="viewport" content="width=device-width, initial-scale=1"'+u'>'
        
    style = u'<'+u'style'+u'>'+u'''
        body { width: 90%; max-width: 1200px; margin: auto; font-family: Helvetica, arial, sans-serif; font-size: 14px; line-height: 1.6; padding-top: 10px; padding-bottom: 10px; background-color: white; padding: 10px; color: #333; }
        body > *:first-child { margin-top: 0 !important; }
        body > *:last-child { margin-bottom: 0 !important; }
        a { color: #4183C4; }
        a.absent { color: #cc0000; }
        a.anchor { display: block; padding-left: 30px; margin-left: -30px; cursor: pointer; position: absolute; top: 0; left: 0; bottom: 0; }
        h1, h2, h3, h4, h5, h6 { margin: 20px 0 10px; padding: 0; font-weight: bold; -webkit-font-smoothing: antialiased; cursor: text; position: relative; }
        h1:hover a.anchor, h2:hover a.anchor, h3:hover a.anchor, h4:hover a.anchor, h5:hover a.anchor, h6:hover a.anchor { background: no-repeat 10px center; text-decoration: none; }
        h1 tt, h1 code { font-size: inherit; }
        h2 tt, h2 code { font-size: inherit; }
        h3 tt, h3 code { font-size: inherit; }
        h4 tt, h4 code { font-size: inherit; }
        h5 tt, h5 code { font-size: inherit; }
        h6 tt, h6 code { font-size: inherit; }
        h1 { font-size: 28px; color: black; }
        h2 { font-size: 24px; border-bottom: 1px solid #cccccc; color: black; }
        h3 { font-size: 18px; }
        h4 { font-size: 16px; }
        h5 { font-size: 14px; }
        h6 { color: #777777; font-size: 14px; }
        p, blockquote, ul, ol, dl, li, table, pre { margin: 15px 0; }
        hr { background: transparent repeat-x 0 0; border: 0 none; color: #cccccc; height: 4px; padding: 0; }
        body > h2:first-child { margin-top: 0; padding-top: 0; }
        body > h1:first-child { margin-top: 0; padding-top: 0; }
        body > h1:first-child + h2 { margin-top: 0; padding-top: 0; }
        body > h3:first-child, body > h4:first-child, body > h5:first-child, body > h6:first-child { margin-top: 0; padding-top: 0; }
        a:first-child h1, a:first-child h2, a:first-child h3, a:first-child h4, a:first-child h5, a:first-child h6 { margin-top: 0; padding-top: 0; }
        h1 p, h2 p, h3 p, h4 p, h5 p, h6 p { margin-top: 0; }
        li p.first { display: inline-block; }
        ul, ol { padding-left: 30px; }
        li { margin: 2px; }
        ul :first-child, ol :first-child { margin-top: 0; }
        ul :last-child, ol :last-child { margin-bottom: 0; }
        dl { padding: 0; }
        dl dt { font-size: 14px; font-weight: bold; font-style: italic; padding: 0; margin: 15px 0 5px; }
        dl dt:first-child { padding: 0; }
        dl dt > :first-child { margin-top: 0; }
        dl dt > :last-child { margin-bottom: 0; }
        dl dd { margin: 0 0 15px; padding: 0 15px; }
        dl dd > :first-child { margin-top: 0; }
        dl dd > :last-child { margin-bottom: 0; }
        blockquote { border-left: 4px solid #dddddd; padding: 0 15px; color: #777777; }
        blockquote > :first-child { margin-top: 0; }
        blockquote > :last-child { margin-bottom: 0; }
        table { padding: 0; }
        table tr { border-top: 1px solid #cccccc; background-color: white; margin: 0; padding: 0; }
        table tr:nth-child(2n) { background-color: #f8f8f8; }
        table tr th { font-weight: bold; border: 1px solid #cccccc; text-align: left; margin: 0; padding: 6px 13px; }
        table tr td { border: 1px solid #cccccc; text-align: left; margin: 0; padding: 6px 13px; }
        table tr th :first-child, table tr td :first-child { margin-top: 0; }
        table tr th :last-child, table tr td :last-child { margin-bottom: 0; }
        img { max-width: 100%; }
        span.frame { display: block; overflow: hidden; }
        span.frame > span { border: 1px solid #dddddd; display: block; float: left; overflow: hidden; margin: 13px 0 0; padding: 7px; width: auto; }
        span.frame span img { display: block; float: left; }
        span.frame span span { clear: both; color: #333333; display: block; padding: 5px 0 0; }
        span.align-center { display: block; overflow: hidden; clear: both; }
        span.align-center > span { display: block; overflow: hidden; margin: 13px auto 0; text-align: center; }
        span.align-center span img { margin: 0 auto; text-align: center; }
        span.align-right { display: block; overflow: hidden; clear: both; }
        span.align-right > span { display: block; overflow: hidden; margin: 13px 0 0; text-align: right; }
        span.align-right span img { margin: 0; text-align: right; }
        span.float-left { display: block; margin-right: 13px; overflow: hidden; float: left; }
        span.float-left span { margin: 13px 0 0; }
        span.float-right { display: block; margin-left: 13px; overflow: hidden; float: right; }
        span.float-right > span { display: block; overflow: hidden; margin: 13px auto 0; text-align: right; }
        code, tt { margin: 0px; padding: 0 5px; white-space: nowrap; none; }
        pre code { margin: 0px; padding: 0; white-space: pre; border: none; background: transparent; }
        .highlight pre { background-color: #333; border: none; font-size: 13px; line-height: 19px; overflow: auto; padding: 6px 10px; margin: 0px; }
        pre { background-color: #333; border: none; font-size: 13px; line-height: 19px; overflow: auto; padding: 6px 10px; margin: 0px; }
        pre code, pre tt { background-color: transparent; border: none; margin: 0px; }
        .collapsible { background-color: #ccc; color: white; cursor: pointer; padding: 5px; width: 100%; border: none; text-align: left; outline: none; font-size: 12px; margin: 0px; }
        .active, .collapsible:hover { background-color: #aaa; margin: 0px; }
        .content { padding: 0px; max-height: 0; overflow: hidden; transition: max-height 0.15s ease-out;  margin: 0px; }
        '''+u'<'+u'/style'+u'>'
    
    script = u'<'+u'script'+u'>'+u'''
        var coll = document.getElementsByClassName("collapsible");
        var i;
        for (i = 0; i < coll.length; i++) {
          coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.maxHeight){
              content.style.maxHeight = null;
            } else {
              content.style.maxHeight = content.scrollHeight + "px";
            } 
          });
        }
        '''+u'<'+u'/script'+u'>'+u'''
        '''+u'<'+u'script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js?skin=desert"'+u'>'+u'<'+u'/script'+u'>'+u'''
        '''+u'<'+u'script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"'+u'>'+u'<'+u'/script'+u'>'+u'''
        '''+u'<'+u'script type="text/x-mathjax-config"'+u'>'+u'''
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [ ["$","$"], ["\\\\(","\\\\)"] ],
                displayMath: [ ["$$",'$$'], ["\\\\[","\\\\]"] ],
                processEscapes: true,
                processEnvironments: true
            },
            // Center justify equations in code and markdown cells. Elsewhere
            // we use CSS to left justify single line equations in code cells.
            displayAlign: 'center',
            "HTML-CSS": {
                styles: {'.MathJax_Display': {"margin": 0}},
                linebreaks: { automatic: true }
            }
        });
        '''+u'<'+u'/script'+u'>'
    
    body = mistune.markdown(pre_html)
    body = body.replace('class="lang-python"', 'class="prettyprint lang-python"')
    body = body.replace(u'<'+u'p'+u'>', '')
    body = body.replace(u'<'+u'/p'+u'>', u'<'+u'br'+u'>')
    start_string = u'<'+u'br'+u'>'
    end_string = u'<'+u'pre'+u'>'
    body = re.sub(start_string+r'[\w\W]'+end_string+r'*', end_string, body)
    
    html = u'<'+u'!DOCTYPE html'+u'>'+u'<'+u'html'+u'>'+u'<'+u'head'+u'>'+meta+style+u'<'+u'/head'+u'>'+u'<'+u'body'+u'>'+body+script+u'<'+u'/body'+u'>'+u'<'+u'/html'+u'>'
    html = unescape(html)
    
    return html

"""
### 4 Create Table of Contents

The user can place a single line of [TOC] within the first block of docstrings.

This function will replace the TOC tag with an automatically generated table of contents down to heading level 4.

This function will also create links for all cross-references to a header. This is done by detecting the exact match (case-sensitive) of the header string.

For example:

> .py Code style

will become a clickable link to the .py Code style section.

"""

def create_toc(html: str) -> str:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    toc_html = u'\n<'+u'h3 style="color: #555" id="toc"'+u'>'+u'Table of Contents'+u'<'+u'/h3'+u'>\n'
    
    header_list = []
    skip_first = 1
    tag_number = 1
    for header in soup.findAll(['h1', 'h2', 'h3', 'h4']):
        header['id'] = header.string.replace(' ','_').replace('.','_').lower()
        header_list.append((header.string, header['id']))
        
        if header.name=='h1':
            indent = 'margin-left: 0px;'
        elif header.name=='h2':
            indent = 'margin-left: 20px;'
        elif header.name=='h3':
            indent = 'margin-left: 40px;'
        elif header.name=='h4':
            indent = 'margin-left: 60px;'
        
        # link back to toc
        if tag_number > skip_first:
            new_tag = soup.new_tag("a")
            new_tag.attrs['style'] = "font-size: 10px; color: #555; margin-top: 0px;"
            new_tag.attrs['href'] = "#toc"
            new_tag.append("TOC")
            br = soup.new_tag("br")
            header.insert_after(br)
            header.insert_after(new_tag)
        
        toc_html = toc_html + u'<'+ 'p style="margin-top:0px; margin-bottom: 0px; ' + indent + '"'+ u'>' + u'<'+ 'a style="color: #333; " ' + f'''href="#{header['id']}"''' + u'>' + header.string + u'<' + u'/a'+ u'>' + u'<'+ u'/p' + u'>\n'
        
        tag_number += 1
        
    toc_html = toc_html + u'<'+u'br'+u'>\n'
    
    toc_tag = '[TOC]'
    html = soup.prettify().replace(toc_tag, toc_html, 1)
    
    # cross-reference entire text
    for header in header_list:
        cross_ref_html = u'<'+ 'a style="color: #555; text-decoration: none;" ' + f'''href="#{header[1]}"''' + u'>' + header[0] + u'<' + u'/a'+ u'>'
        html = html.replace(header[0], cross_ref_html)
        
    return html

"""
## Some handy functions

Some common functions that is required for handling various tasks.
"""

def replace_every_nth(original_string: str, substring_to_replace: str, replace_with: str, nth: int) -> str:
    new_string = re.sub(f'({substring_to_replace})',
                        lambda m,
                        c = itertools.count(): m.group() if next(c) % nth else replace_with, original_string)
    return new_string


def unescape(escaped: str) -> str:
    unescaped = escaped.replace("&lt;", u"<")
    unescaped = unescaped.replace("&gt;", u">")
    unescaped = unescaped.replace("&amp;", "&")
    return unescaped


def save_as(content, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    file = open(file_path, 'w+', encoding='utf-8')
    file.write(content)
    file.close() 

"""
## The main functions

Unfortunately, for now you need to copy this mindoc.py file into a folder that you are working in to use it.

Using the terminal, you would also need to navigate to the folder where the mindoc.py file is.

### Some options

You can convert a single .py file to a html documentation, or multiple files through the use of a glob *.

For example:

> mindoc ./*.py

If you are continuing to write the documentation and would like the changes to be continuously reflected in the generated .html file, use the watch option.

For example:

> mindoc -w ./*.py

### Output

* The output documentation .html file name will be the same as the .py file.
* The documentation will be saved in the docs folder where the .py file is.

> awesome.py -> docs/awesome.html

Unless the .py file is in the src folder, then the documentation will be saved in the equivalent docs folder.

> src/awesome.py -> docs/awesome.html

"""

def make_docs(py_files: list, print_production: bool):
    for py_file_path in py_files:
        py = get_py_code(py_file_path)
        pre_html = convert_python_blocks(py)
        html = convert_to_html(pre_html)

        toc_tag = '[TOC]'
        if toc_tag in html:
            html = create_toc(html)
        
        (dir_path, file_name) = os.path.split(py_file_path)
        
        if dir_path == '':
            doc = './docs/'
        elif dir_path.endswith('src'):
            dir_path = dir_path[:-3]+'docs/'
            doc = ''
        else:
            doc = '/docs/'
        
        html_file_path = dir_path + doc + file_name.replace('.py', '.html')
        
        save_as(html, html_file_path)
        
        if print_production:
            print(f'Doc for {py_file_path} saved as {html_file_path}.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--watch', action='store_true', help='Watch original files and re-generate documentation on changes')
    parser.add_argument("src_path", metavar="path", type=str, help="Path to .py files to be converted to .html doc; accepts * as wildcard")

    args = parser.parse_args()
    
    print('')
    files = glob.glob(args.src_path)
    py_files = [x for x in files if x.endswith('.py')]
    
    make_docs(py_files, print_production=True)
    
    if args.watch:
        print('Watching...')
        print('Ctrl+c to exit')
        while True:
            make_docs(py_files, print_production=False)
            time.sleep(1)
    
    print('')
    
    
if __name__ == "__main__":
    main()