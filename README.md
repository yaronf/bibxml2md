Probably the most dreary task when converting an old RFC into editable form is having to deal with the references.

This simple script converts bibxml references extracted from xml2rfc files into markdown,
for use in [kramdown-rfc2629](https://github.com/cabo/kramdown-rfc2629) Internet Drafts.
It has been tested on a large number of references ([RFC 7525](https://tools.ietf.org/html/rfc7525#section-7)) but is likely to fail when faced with more complicated inputs. In particular, you will have to deal with the simple stuff (RFCs, I-Ds and DOI references) yourself.

Contributions are welcome!

The input is a **valid** XML file of the form:

```XML
<references>
	<reference>
	</reference>
	...
	<reference>
	</reference>
</references>
```
