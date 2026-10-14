# blog.neilennis.com

This repository holds the public, static snapshot of [Neil Ennis's blog](https://blog.neilennis.com/). The editable source remains the private local WordPress installation. Staatic generates the static site, which is then exported here for Git history and future hosting.

## Layout

- `site/` contains the files served at the root of the website.
- `wrangler.jsonc` configures the snapshot for Cloudflare Workers Static Assets.
- `site/_redirects` preserves a redirect present in the Staatic export.
- `site/404.html` is a copy of Staatic's custom 404 page for static hosting.

## Update the snapshot

1. Finish and review a full Staatic publication locally.
2. Export its public files to a separate folder and compare that export with the intended published site.
3. Replace the generated contents of `site/` with the reviewed export. Keep `site/_redirects` and `site/404.html`; refresh the latter from `site/404_not_found/index.html` if that page changed.
4. Leave WordPress code, databases, caches, logs, backups, credentials, and local configuration out of `site/`.
5. Preview the snapshot locally, check a sample of posts and media, review `git status`, then commit and push.

The initial snapshot was checked against the current S3 object inventory on 15 October 2026. Nine non-site files were omitted: `wp-content/uploads/wio.log`, two `Thumbs.db` files, and six `wp-content/uploads/wpforms/cache/` error pages.

## Hosting

The Wrangler configuration is ready for a static-only Cloudflare Worker, but this repository alone does not deploy anything. Cloudflare Git integration, the custom domain, and DNS must be configured separately. Until that cutover, AWS remains the live host.

Cloudflare Workers Static Assets uses `site/` as the asset directory. Run `npx wrangler dev` from the repository root for a local preview after installing Wrangler from npm. A future Git deployment should build with no command and deploy with `npx wrangler deploy`.

Keep an independent backup of the WordPress source and database. Git tracks this public output, not the editable WordPress site.
