Personal blog.
Built with [pelican][], using [uberspot][] theme.

### Use

Install pelican and plugin dependencies:

```bash
(venv)$ pip install pelican Markdown typogrify gitpython beautifulsoup4 pelicanfly
```

Hack with:

```bash
pelican -s settings_dev.py -d -r --ignore-cache -t pelican-uberspot
```

Open <http://localhost:8000>.

**Note:** `gitpython` needs python2. If it doesn't work, remove the plugin
    from `settings_dev.py` and rerun the above command.

[Plugins][pelican-plugins] used:

- post_stats
- tipue_search
- neighbors
- filetime_from_git
- pelicanfly

### License

Except where otherwise noted, content on this site is licensed under a
[Creative Commons Attribution 4.0 International License][cc].

[uberspot]: https://github.com/axilleas/pelican-uberspot
[pelican]: http://docs.getpelican.com
[pelican-plugins]: https://github.com/getpelican/pelican-plugins/
[cc]: http://creativecommons.org/licenses/by/4.0/
