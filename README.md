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
| `<name>.json` | The model spec, exactly as Simile's **File › Save model as file…** writes it, with its `metadata` (below). Plain JSON: data, never run. |
| `<name>.parameters.json` | Optional: the model's parameter values, as the Parameters panel's **Save** writes them. The app loads it with the model. |
| `index.html` | The model's page. |
| pictures | Optional, as the page needs them. |

The page has, at least: a title, a short description, a link to the
published paper if there is one, and the **Open in Simile** link:

```html
<a class="open" href="https://robert-mue.github.io/simile/index.html?open=https://robert-mue.github.io/model_gallery/models/<name>/<name>.json" target="_blank" rel="noopener">Open in Simile</a>
```

### The model's metadata

The model spec carries what Simile's **File › Sample models…** panel shows
about it, in `metadata`, by hand:

```json
"metadata": {
  "title": "Pangolin harvest: bioeconomic drivers of extinction",
  "description": "One to three sentences: what the model is about.",
  "keywords": ["conservation", "harvesting"],
  "paper": { "citation": "Authors (year). Title. Journal, volume, pages.", "url": "https://doi.org/..." }
}
```

`paper` only if there is one. Nothing that can be read from the model
itself goes here: the panel works out its size (submodels / stocks /
flows / variables) and the Simile features it uses from the model.

### Its default displays

And how it opens in Simile, in `presentation`: the plots (of its own
stocks, flows and variables, named by element id) and the sliders, and the
run settings. Opened from the gallery or the Sample models panel, the model
is prepared and run once, so its graphs are drawn at once:

```json
"presentation": {
  "run": { "runLength": 50, "logEach": 0.5, "timeStep": "0.1" },
  "displays": [
    { "widget": "plotter", "variables": ["node1", "node2"] },
    { "widget": "sliders" }
  ]
}
```

No need to write it by hand: open the model in Simile, set up its
Simulation panel as it should open, and in **Widgets › Metadata** select
**Use the displays open now**; then save the model as its `<name>.json`.

Copy an existing model's page to start one. More text, pictures, links to
projects: as each model needs.

## Adding a model

1. Make `models/<name>/` with the files above. Use lower case and hyphens
   for `<name>`.
2. List it in `index.html`, and in `models/index.json` (the list the
   Sample models panel reads).
3. Run `python3 check/check.py`. It checks every model directory, its
   metadata and default displays, its page, its link, its pictures, and
   both lists.
4. Commit and push. GitHub Pages publishes it within a minute or two.

Being in the gallery is being committed here: the curators are those with
commit access.

## How the link works

The app's `index.html?open=<address>` fetches the model spec from the
address, with `<name>.parameters.json` beside it if there is one, adds it to
the reader's models as a copy, and opens it. Another site's file can be
fetched only if that site allows it; GitHub Pages does, for every file. See
Simile's `CLAUDE.md` ("Opening a model from an address").
