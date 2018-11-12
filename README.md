## decode_mail (.py)

For when your mail client doesn't always decode subject lines. See [RFC 2047, section 8](https://www.ietf.org/rfc/rfc2047.txt) for a tl;dr.

```
$ decode_mail '=?utf-8?b?SGVsbG8sIHdvcmxkIQ==?='
Hello, world!

$ decode_mail '=?ISO-8859-1?q?Python=20=3D=20Good?='
Python = Good
```

Also supports stdin input and multiple arguments:

```
$ decode_mail '=?utf-8?b?QmFkZ2VyIGJhZGdlciBiYWRnZXIgYmFkZ2VyIA==?=' '=?utf-8?b?TXVzaHJvb20sIG11c2hyb29tIQ==?='
Badger badger badger badger Mushroom, mushroom!

$ decode_mail
=?utf-8?b?QmFkZ2VyIGJhZGdlciBiYWRnZXIgYmFkZ2VyIA==?=
=?utf-8?b?TXVzaHJvb20sIG11c2hyb29tIQ==?=
^D
Badger badger badger badger Mushroom, mushroom!
Translate? [y/n] n
```

### Requirements

Python ≥ 3.6 for those sweet, sweet format strings.

Optional Google Translate feature requires the `translator` module.

I suggest cloning it somewhere local and then linking it into your path as `decode_mail`.

### Caveats

This is a really lazy implementation of a small part of the spec and only really works with subject lines. That's good enough for me. For more rigour, check the rest of the internet.
