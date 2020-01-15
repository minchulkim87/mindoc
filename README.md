# mindoc
A minimalistic python documentation module
This program converts a .py file into a .html file to minimally document python code.

The purpose is to minimise documentation and to enable writing document-like .py files without a heavy imposition of the docstring burden.

Simply write the .py file as if you would a markdown file, but instead of writing the code blocks between text, write the text between codes.

This tool also helps automatically generate a table of contents and cross-referencing.

## Requirements

### Packages

I tried to minimise the dependencies by using standard python libraries or standard packages within the Anaconda distribution. If you are not using the Anaconda distribution, these packages are required on top of the standard python libraries.

* **mistune**: part of the Anaconda distribution
* **beautifulsoup4**: part of the Anaconda distribution

I assume they can be installed with the following:

> pip install mistune
> pip install beautifulsoup4


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

1. Download the mindoc.py file to the directory you are working in.
2. Open your terminal and navigate to the directory where the mindoc.py file is.
3. Type the following command into the terminal

> python -m mindoc [-w] [file path to the .py file to convert, can use glob]

For example:

> python -m mindoc my_python_file.py

You can convert a single .py file to a html documentation, or multiple files through the use of a glob *.

For example:

> python -m mindoc ./*.py

If you are continuing to write the documentation and would like the changes to be continuously reflected in the generated .html file, use the watch option.

For example:

> python -m mindoc -w ./*.py