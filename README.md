# Simile model gallery

Example models, selected for exploring [Simile](https://robert-mue.github.io/simile/):
**https://robert-mue.github.io/model_gallery/**

Each model has a page saying what it is about, and an **Open in Simile** link
that opens it in the app, in a new tab. A model opened from here is a copy in
the reader's own browser; nothing here changes.

## A model's directory

Every model has its own directory, `models/<name>/`:

| File | What it is |
|---|---|
| `<name>.json` | The model spec, exactly as Simile's **File › Save model as file…** writes it. Plain JSON: data, never run. |
| `<name>.parameters.json` | Optional: the model's parameter values, as the Parameters panel's **Save** writes them. The app loads it with the model. |
| `index.html` | The model's page. |
| pictures | Optional, as the page needs them. |

The page has, at least: a title, a short description, a link to the
published paper if there is one, and the **Open in Simile** link:

```html
<a class="open" href="https://robert-mue.github.io/simile/index.html?open=https://robert-mue.github.io/model_gallery/models/<name>/<name>.json" target="_blank" rel="noopener">Open in Simile</a>
```

Copy an existing model's page to start one. More text, pictures, links to
projects: as each model needs.

## Adding a model

1. Make `models/<name>/` with the files above. Use lower case and hyphens
   for `<name>`.
2. List it in `index.html`.
3. Run `python3 check/check.py`. It checks every model directory, its
   page, its link, its pictures, and the index.
4. Commit and push. GitHub Pages publishes it within a minute or two.

Being in the gallery is being committed here: the curators are those with
commit access.

## How the link works

The app's `index.html?open=<address>` fetches the model spec from the
address, with `<name>.parameters.json` beside it if there is one, adds it to
the reader's models as a copy, and opens it. Another site's file can be
fetched only if that site allows it; GitHub Pages does, for every file. See
Simile's `CLAUDE.md` ("Opening a model from an address").
