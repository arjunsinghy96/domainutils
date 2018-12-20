# domainutils

domainutils aims to provide different domain parsing tools in one place.

## Usage

### tld_parser.TLDParserTree

TLDParserTree builds a Trie like tree from the list of [publicsuffix](https://publicsuffix.org/list/public_suffix_list.dat)

TLDParserTree provides method `split_tld`(alias `s`) to separate TLD from a given domain such as `en.wikipedia.com` will return a 2-tuple `('en.wikipedia', 'com')`.

```python
>>> from domainutils.tld_parser import TLDParserTree

>>> tld_tree = TLDParserTree()
>>> tld_tree.s('google.com')
('google', 'com')
>>> tld_tree.s('nestle.com.bd')
('nestle', 'com.bd')
```

## Testing

Run tests by simply running the domainutils/tests.py
```
$ python3.6 domainutils/tests.py
```

## Contribution

Please create an issue for bugs and feature requests.