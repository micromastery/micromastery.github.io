# frozen_string_literal: true

# Build-time SEO tweaks:
# - Post banners use the optimized JPEG made by tools/make-thumbnails.py (listed in
#   _data/banner_images.json), with its size so link previews get og:image dimensions.
# - Tag archive pages are noindexed and left out of the sitemap: they duplicate the
#   category pages (e.g. both "AI" pages) and are thin.
# - Category archive pages get their own meta description instead of the site-wide one,
#   and a "<name> posts" <title> (via `seo_title`, see _includes/head.html).
#   Posts can also set `seo_title` for a shorter search-result title; the visible
#   headline and link previews keep the full `title`.
# - The theme's generic "Preview Image" alt text on post banners becomes the post title.
#   (Setting `image.alt` in front matter would also add a visible caption.)

require "cgi"

module SeoTweaks
  class Generator < Jekyll::Generator
    safe true
    # Runs after jekyll-archives and before jekyll-sitemap (:lowest).
    priority :low

    def generate(site)
      banners = site.data["banner_images"] || {}

      site.posts.docs.each do |post|
        image = post.data["image"]
        next unless image.is_a?(String)

        info = banners[File.basename(image, File.extname(image))]
        next unless info

        post.data["image"] = {
          "path" => info["path"],
          "width" => info["width"],
          "height" => info["height"],
        }
      end

      site.pages.each do |page|
        case page.data["layout"]
        when "tag"
          page.data["sitemap"] = false
          page.data["noindex"] = true
        when "category"
          page.data["seo_title"] = "#{page.title} posts"
          page.data["description"] ||=
            "Every post in the #{page.title} category on #{site.config["title"]}: " \
            "plain-English guides based on real projects."
        end
      end
    end
  end
end

Jekyll::Hooks.register :posts, :post_render do |post|
  title = CGI.escapeHTML(post.data["title"].to_s)
  post.output = post.output.sub('alt="Preview Image"', %(alt="#{title}"))
end
