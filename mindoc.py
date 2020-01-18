"""
# mindoc.py

A minimalistic python documentation tool.

* [GitHub page](https://minchulkim87.github.io/mindoc/)
* [Source code](https://github.com/minchulkim87/mindoc)


This program converts a .py file into a .html file to minimally document python code.

The purpose is to minimise documentation and to enable writing document-like .py files without a heavy imposition of the docstring burden.

Simply write the .py file as if you would a markdown file, but instead of writing the code blocks between text, write the text blocks between codes.

This tool also helps automatically generate a table of contents and cross-referencing.

[TOC]

## Requirements

### Packages

I tried to minimise the dependencies by using standard python libraries or standard packages within the Anaconda distribution. If you are not using the Anaconda distribution, these packages are required on top of the standard python libraries.

* **mistune**: part of the standard Anaconda distribution
* **beautifulsoup4**: part of the standard Anaconda distribution

### .py Code style

The .py file to be converted must have been written in the following very specific way:

* All .py must must begin with a fenced triplet of double quotes (&quot;&quot;&quot;).
* All comment blocks, i.e. the documentation sections, must also use fenced triplet of double quotes that begin and end in new line.
* You may use markdown syntax within the documentation sections.
* All other comment strings will not be converted (#, ', ''', ").
* If you want triplet quote blocks untouched, use the triplet of single quotes (''').
* Place a [TOC] in the line you want the table of contents to be placed.
* If you type in the exact (case-sensitive) string of the header, surrounded by square brackets, anywhere within the documentation sections, it will be linked to the header.

By the way, you can also have code blocks within the markdown blocks, but these will not be collapsible.

```python
def sample_function(x):
    return x + 1
```

## How to use

### Install from github.

> pip install git+https://github.com/minchulkim87/mindoc.git@master

Then use the command from terminal

> mindoc [-w] [file to the .py file to convert, can use glob]

For example:

> mindoc mindoc.py

Produces this document.


### Locally install

(for those who do not have access to the luxury pip install)

1. Download this git repository as a zip file and extract.
2. Open your terminal and navigate to the extracted directory
3. Install using the setup.py

> python setup.py install [--force]

Then, as above you can use mindoc from terminal as follows:

> mindoc [-w] [file to the .py file to convert, can use glob]


### Without installation

(for those who do not have access to the luxury of any installation)

*Without* installing mindoc, you would need to already have the required packages above.

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
from bs4 import BeautifulSoup
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
    """
    Q: What happens to fenced docstrings that are meant for functions?
    A: They remain within the code blocks.
    So you can continue to use docstrings to document the functions if you want to.
    """

    # Windows newline fix
    windows_newline = u'\r'+'\n'
    if windows_newline in code:
        code = code.replace(windows_newline, '\n')
    
    # Make all code blocks (which are between markdown blocks) collapsible
    # Remove first fenced triplet of double quotes (ftdq)
    first_ftdq = '"""' + '\n'
    pre_html = code.replace(first_ftdq, '', 1)

    # all subsequent ftdq must begin without any indentation and must end with a new line.
    ftdq = '\n' + '"""' + '\n'
    br = tag('br')
    div = tag('div')
    ediv = endtag('div')
    collapsible_button = tag('button type="button" class="collapsible" style="width: 80px; text-align:center; margin-bottom:0px;"')
    ebutton = endtag('button')
    content_div = tag('div style=" margin-top:0px;" class="content"')

    md_python_start = '\n```' + 'python\n'
    md_python_end = u'```\n'
    replace_with_pre = '\n' + br + br + collapsible_button + 'View code' + ebutton + content_div + md_python_start
    replace_with_post = '\n' + md_python_end + ediv + '\n'

    pre_html = replace_every_nth(pre_html, ftdq, replace_with_pre, nth=2)
    pre_html = pre_html.replace(ftdq, replace_with_post)
    pre_html = pre_html + replace_with_post
    
    return pre_html

"""
### 3 Convert the code to a html doc

This function converts the documentation strings into html code, converting the markdown syntax into html.

The function also styles the document.
"""
def convert_to_html(pre_html: str) -> str:
    meta = tag('meta name="viewport" content="width=device-width, initial-scale=1"')
        
    style = tag('style') + u'''
        body {
            width: 90%; max-width: 1200px; margin: auto; font-family: Helvetica, arial, sans-serif; font-size: 14px; line-height: 1.6;
            background-color: white; padding: 10px; color: #333;
            }
        

        /* CSS to make Markdown appear GitHub-style */

        body > *:first-child { margin-top: 0 !important; }
        body > *:last-child { margin-bottom: 0 !important; }
        a { color: #4183C4; margin-top: 0; margin-bottom: 0; }
        a.absent { color: #cc0000; }
        a.anchor { display: block; padding-left: 30px; margin-left: -30px; cursor: pointer; position: absolute; top: 0; left: 0; bottom: 0; }
        h1, h2, h3, h4, h5, h6 {
            margin: 20px 0 5px; padding: 0; font-weight: bold; -webkit-font-smoothing: antialiased; cursor: text; position: relative;
            }
        h1:hover a.anchor, h2:hover a.anchor, h3:hover a.anchor, h4:hover a.anchor, h5:hover a.anchor, h6:hover a.anchor {
            background: no-repeat 10px center; text-decoration: none;
            }
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
        p, blockquote, ul, ol, dl, li, table, pre { margin: 10px 0; }
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


        /* CSS that allows the collapsible code blocks */

        .collapsible {
            background-color: #ccc; padding: 5px; margin: 0; border: none; outline: none;
            text-align: left; color: white; font-size: 12px;
            cursor: pointer; width: 100%; }
        .active, .collapsible:hover { background-color: #aaa; margin: 0; }
        .content { margin: 0; background-color: transparent; padding: 0; max-height: 0; overflow: hidden; transition: max-height 0.15s ease-out; }


        /* Code Prettify styling for the code blocks */

        pre code, pre tt { border: none; margin: 0px; padding: 10px; }
        pre .prettyprint { display: block; background-color: #333; margin: 0; }
        pre .nocode { background-color: none; color: #000 }
        pre .str { color: #ffa0a0 } /* string */
        pre .kwd { color: #f0e68c; font-weight: bold } /* keyword */
        pre .com { color: #87ceeb } /* comment */
        pre .typ { color: #98fb98 } /* type */
        pre .lit { color: #cd5c5c } /* literal */
        pre .pun { color: #fff }    /* punctuation */
        pre .pln { color: #fff }    /* plaintext */
        pre .tag { color: #f0e68c; font-weight: bold } /* html/xml tag */
        pre .atn { color: #bdb76b; font-weight: bold } /* attribute name */
        pre .atv { color: #ffa0a0 } /* attribute value */
        pre .dec { color: #98fb98 } /* decimal */

        /* convert to light theme for printing */

        @media print {
        pre code, pre tt { background-color: none }
        pre.prettyprint { background-color: none }
        pre .str, code .str { color: #060 }
        pre .kwd, code .kwd { color: #006; font-weight: bold }
        pre .com, code .com { color: #600; font-style: italic }
        pre .typ, code .typ { color: #404; font-weight: bold }
        pre .lit, code .lit { color: #044 }
        pre .pun, code .pun { color: #440 }
        pre .pln, code .pln { color: #000 }
        pre .tag, code .tag { color: #006; font-weight: bold }
        pre .atn, code .atn { color: #404 }
        pre .atv, code .atv { color: #060 }
        }
        ''' + endtag('style')
    
    # Make code collapsible
    script = tag('script') + u'''
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
        ''' + endtag('script')
    
    # JavaScript styling of the code blocks
    script += tag('script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"') + endtag('script')

    # JavaScript to allow MathJax
    script += tag('script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"') + endtag('script')
    script += tag('script type="text/x-mathjax-config"') + u'''
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
        ''' + endtag('script')
    
    # Convert the body markdown to html
    renderer = mistune.Renderer(escape=True, hard_wrap=True, use_xhtml=False)
    markdown = mistune.Markdown(renderer=renderer)
    body = markdown(pre_html)

    # Clean up some weird stuff that the markdown to html conversion introduced
    br = tag('br')
    body = body.replace(tag('p'), '\n')
    body = body.replace(endtag('p'), br + '\n')
    
    # Put the html together
    html = tag('!DOCTYPE html') + tag('html') + tag('head') + meta + style + endtag('head') + tag('body') + body + script + endtag('/body') + endtag('html')
    html = unescape(html)
    
    # Make prettier with the Javascript styling.
    soup = BeautifulSoup(html, 'html.parser')
    for code in soup.find_all('code'):
        code['class'] = ['prettyprint'] + code['class']
    
    # Clean up some more weird stuff that the markdown to html conversion introduced
    for div_content in soup.find_all('div', class_='content'):
        div_content.br.extract()

    html = soup.prettify(formatter="html5")

    return html
"""
### 4 Create Table of Contents

The user can place a single line of [TOC] within the first block of docstrings.

This function will replace the TOC tag with an automatically generated table of contents down to heading level 4.

This function will also create links for all cross-references to a header. This is done by detecting the exact match (case-sensitive) of the header string surrounded by square brackets.


For example:

> [ .py Code style ] (without the extra padding I placed)

will become [.py Code style].

**Warning**: Don't use markdown or html *within* the header markdowns as this will cause errors.

"""
def create_toc(html: str) -> str:
    
    soup = BeautifulSoup(html, "html.parser")
    
    toc_html = tag('h3 style="color: #555" id="toc"')+'Table of Contents'+endtag('h3')
    
    header_list = []
    skip_first = 1
    tag_number = 1
    
    for header in soup.findAll(['h1', 'h2', 'h3', 'h4']):
        header_string = header.string.replace('\n','').replace('\t','').strip().replace(' ','_').replace('.','_').lower()
        header['id'] = header_string
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
            new_tag.attrs['style'] = "font-size: 10px; color: #555;"
            new_tag.attrs['href'] = "#toc"
            new_tag.append("TOC")
            br_tag = soup.new_tag("br")
            header.insert_after(br_tag)
            header.insert_after(new_tag)
        
        toc_html = toc_html + tag('p style="margin-top:0px; margin-bottom: 0px; '+indent+'"') + tag('a style="color: #333; " '+f'''href="#{header['id']}"''') + header.string + endtag('a') + endtag('p') +'\n'
        
        tag_number += 1
    
    toc_html = toc_html + tag('br') + '\n'
    
    toc_tag = '[TOC]'
    html = soup.prettify(formatter="html5").replace(toc_tag, toc_html, 1)
    
    # generate cross-reference links to headers
    for header in header_list:
        cross_ref_tag = '['+header[0].replace('\n','').replace('\t','').strip()+']'
        cross_ref_html = tag('a style="color: #555; text-decoration: none;" '+f'''href="#{header[1]}"''') + header[0] + endtag('a')
        html = html.replace(cross_ref_tag, cross_ref_html)
        
    return html
"""
## Some handy functions

Some common functions that is required for handling various tasks.
"""
def tag(element_name: str) -> str:
    return u'<'+element_name + u'>'


def endtag(element_name: str) -> str:
    return u'<' + '/' + element_name + u'>'


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
            time.sleep(3)
    
    print('')
    
    
if __name__ == "__main__":
    main()