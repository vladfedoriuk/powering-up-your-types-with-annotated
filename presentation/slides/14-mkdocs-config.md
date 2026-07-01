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
The mkdocstrings griffe_typingdoc extension reads Doc metadata from your Annotated types and renders it directly in the generated documentation. No extra markup, no docstring duplication — the type is the source of truth for both validation and docs.
-->
