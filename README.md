# Chirpy Starter

[![Gem Version](https://img.shields.io/gem/v/jekyll-theme-chirpy)][gem]&nbsp;
[![GitHub license](https://img.shields.io/github/license/cotes2020/chirpy-starter.svg?color=blue)][mit]

When installing the [**Chirpy**][chirpy] theme through [RubyGems.org][gem], Jekyll can only read files in the folders
`_data`, `_layouts`, `_includes`, `_sass` and `assets`, as well as a small part of options of the `_config.yml` file
from the theme's gem. If you have ever installed this theme gem, you can use the command
`bundle info --path jekyll-theme-chirpy` to locate these files.

The Jekyll team claims that this is to leave the ball in the user’s court, but this also results in users not being
able to enjoy the out-of-the-box experience when using feature-rich themes.

To fully use all the features of **Chirpy**, you need to copy the other critical files from the theme's gem to your
Jekyll site. The following is a list of targets:

```shell
.
├── _config.yml
├── _plugins
├── _tabs
└── index.html
```

To save you time, and also in case you lose some files while copying, we extract those files/configurations of the
latest version of the **Chirpy** theme and the [CD][CD] workflow to here, so that you can start writing in minutes.

## Prerequisites

Follow the instructions in the [Jekyll Docs](https://jekyllrb.com/docs/installation/) to complete the installation of
the basic environment. [Git](https://git-scm.com/) also needs to be installed.

## Installation

Sign in to GitHub and [**use this template**][use-template] to generate a brand new repository and name it
`USERNAME.github.io`, where `USERNAME` represents your GitHub username.

Then clone it to your local machine and run:

```console
$ bundle
```

## Usage

Please see the [theme's docs](https://github.com/cotes2020/jekyll-theme-chirpy#documentation).

## AdSense diagnostic unit

A single responsive display unit (`9225879554`) is placed after the introduction
in [the AI agents article](_posts/2025-07-19-understanding-agentic-ai.md), served at
`/posts/understanding-agentic-ai/`. Other pages and Auto ads settings are unchanged.
The unit reuses the site's existing AdSense loader in
[_includes/metadata-hook.html](_includes/metadata-hook.html); do not add a second loader.

After deployment, inspect the article in browser developer tools:

- Confirm a request to `/pagead/ads` with `slotname=9225879554`.
- Inspect `ins[data-ad-slot="9225879554"]` for `data-adsbygoogle-status="done"`
  and `data-ad-status="filled"` or `"unfilled"`.
- Check the console if initialization fails. A successful HTTP response alone
  does not prove that Google returned an ad or that an impression occurred.

Do not click your own ads or repeatedly reload the page to generate traffic.
To remove the diagnostic unit, remove its `<ins>` and following initialization
`<script>` from that article; keep the shared loader for Auto ads.

## License

This work is published under [MIT][mit] License.

[gem]: https://rubygems.org/gems/jekyll-theme-chirpy
[chirpy]: https://github.com/cotes2020/jekyll-theme-chirpy/
[use-template]: https://github.com/cotes2020/chirpy-starter/generate
[CD]: https://en.wikipedia.org/wiki/Continuous_deployment
[mit]: https://github.com/cotes2020/chirpy-starter/blob/master/LICENSE
