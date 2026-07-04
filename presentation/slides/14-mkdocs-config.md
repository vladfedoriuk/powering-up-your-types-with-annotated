---
layout: default
class: code-center
---

# MkDocs / Zensical

<div class="divider-yellow"></div>

```yaml
# mkdocs.yml
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            extensions:
              - griffe_typingdoc
            import_paths: [...]
```

<p class="text-xs opacity-60 mt-4">Render <code>Doc</code> annotations automatically — see <a href="https://zensical.org/docs/setup/extensions/mkdocstrings/#configuration-mkdocsyml">zensical docs</a>.</p>

<!--
This extension reads Doc metadata from your Annotated types and renders it in the docs. No need for docstring styles like Numpy or Google, and no duplication.

Add or remove a field, and the docs update automatically.
-->
