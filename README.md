# blog.neilennis.com

This repository holds the public, static snapshot of [Neil Ennis's blog](https://blog.neilennis.com/). The editable source remains the private local WordPress installation. Staatic generates the static site, which is then exported here for Git history and future hosting.

## Layout

- `site/` contains the files served at the root of the website.
- `wrangler.jsonc` configures the snapshot for Cloudflare Workers Static Assets.
- `site/_redirects` preserves legacy WordPress URLs and sends `/p/<post-id>` to `/p/?id=<post-id>` for `nbe.me` shortlinks. `site/p/index.html` then uses `site/postmap.json` to find the post slug.
- `site/404.html` is a copy of Staatic's custom 404 page for static hosting.

## Update the snapshot

1. Finish and review a full Staatic publication locally.
2. Export its public files to a separate folder and compare that export with the intended published site.
3. Replace the generated contents of `site/` with the reviewed export. Keep `site/_redirects` and `site/404.html`; refresh the latter from `site/404_not_found/index.html` if that page changed.
4. Leave WordPress code, databases, caches, logs, backups, credentials, and local configuration out of `site/`.
5. Preview the snapshot locally, check a sample of posts and media, review `git status`, then commit and push.

The initial snapshot was checked against the current S3 object inventory on 15 October 2026. Nine non-site files were omitted: `wp-content/uploads/wio.log`, two `Thumbs.db` files, and six `wp-content/uploads/wpforms/cache/` error pages.

## Hosting

Cloudflare serves the live site at `blog.neilennis.com` through the `blog-neilennis-com` Worker. Its Git integration builds and deploys pushes to `main` from this repository. Check the Worker deployment status and a sample of live pages after each push.

Cloudflare Workers Static Assets uses `site/` as the asset directory. The build command is empty and the deploy command is `npx wrangler deploy`. Run `npx wrangler dev` from the repository root for a local preview after installing Wrangler from npm.

Most GIF and MP4 files linked by the posts live on `cdn2.neilennis.com` and are therefore outside this repository. The original `DSC07816-MOTION.gif` and `PaulInCreek-MOTION.gif` animations were recovered from the private photo archive and are included in `site/wp-content/uploads/`. Keep those originals in the WordPress uploads folder when generating a fresh Staatic export.

Keep an independent backup of the WordPress source and database. Git tracks this public output, not the editable WordPress site.
