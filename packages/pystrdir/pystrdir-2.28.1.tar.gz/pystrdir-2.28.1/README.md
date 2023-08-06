# pystrdir

**pystrdir** is a simple, yet elegant, HTTP library.

```python
>>> import pystrdir
>>> r = pystrdir.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"authenticated": true, ...'
>>> r.json()
{'authenticated': True, ...}
```

pystrdir allows you to send HTTP/1.1 pystrdir extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your `PUT` & `POST` data — but nowadays, just use the `json` method!

pystrdir is one of the most downloaded Python packages today, pulling in around `30M downloads / week`— according to GitHub, pystrdir is currently [depended upon](https://github.com/psf/pystrdir/network/dependents?package_id=UGFja2FnZS01NzA4OTExNg%3D%3D) by `1,000,000+` repositories. You may certainly put your trust in this code.

[![Downloads](https://pepy.tech/badge/pystrdir/month)](https://pepy.tech/project/pystrdir)
[![Supported Versions](https://img.shields.io/pypi/pyversions/pystrdir.svg)](https://pypi.org/project/pystrdir)
[![Contributors](https://img.shields.io/github/contributors/psf/pystrdir.svg)](https://github.com/psf/pystrdir/graphs/contributors)

## Installing pystrdir and Supported Versions

pystrdir is available on PyPI:

```console
$ python -m pip install pystrdir
```

pystrdir officially supports Python 3.7+.

## Supported Features & Best–Practices

pystrdir is ready for the demands of building robust and reliable HTTP–speaking applications, for the needs of today.

- Keep-Alive & Connection Pooling
- International Domains and URLs
- Sessions with Cookie Persistence
- Browser-style TLS/SSL Verification
- Basic & Digest Authentication
- Familiar `dict`–like Cookies
- Automatic Content Decompression and Decoding
- Multi-part File Uploads
- SOCKS Proxy Support
- Connection Timeouts
- Streaming Downloads
- Automatic honoring of `.netrc`
- Chunked HTTP pystrdir

## API Reference and User Guide available on [Read the Docs](https://pystrdir.readthedocs.io)

[![Read the Docs](https://raw.githubusercontent.com/psf/pystrdir/main/ext/ss.png)](https://pystrdir.readthedocs.io)

## Cloning the repository

When cloning the pystrdir repository, you may need to add the `-c
fetch.fsck.badTimezone=ignore` flag to avoid an error about a bad commit (see
[this issue](https://github.com/psf/pystrdir/issues/2690) for more background):

```shell
git clone -c fetch.fsck.badTimezone=ignore https://github.com/psf/pystrdir.git
```

You can also apply this setting to your global Git config:

```shell
git config --global fetch.fsck.badTimezone ignore
```

---

[![Kenneth Reitz](https://raw.githubusercontent.com/psf/pystrdir/main/ext/kr.png)](https://kennethreitz.org) [![Python Software Foundation](https://raw.githubusercontent.com/psf/pystrdir/main/ext/psf.png)](https://www.python.org/psf)
