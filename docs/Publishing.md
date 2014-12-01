# Publishing

First, install `pandoc` to auto-convert Markdown syntax into reStructuredText:

```bash
sudo apt-get install pandoc
sudo pip install pypandoc
```

Then, following [this guide](http://peterdowns.com/posts/first-time-with-pypi.html), push the project to PyPI:

```bash
sudo python setup.py sdist upload -r pypi
```
