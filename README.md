# commoncrayon.github.io

Source for the CommonCrayon website: free software downloads, hosted on GitHub Pages.

## Publish it

1. Create a public repo on GitHub named exactly `CommonCrayon.github.io`.
2. Push the contents of this folder to its `main` branch.
3. In the repo, go to **Settings > Pages** and set the source to **Deploy from a branch**, `main`, `/ (root)`.
4. The site goes live at https://commoncrayon.github.io within a minute or two.

## How downloads work

Download buttons fetch the latest release from each project's GitHub Releases, so publishing a new release updates the site automatically. No site change needed.

- A card or panel sets `data-repo="CommonCrayon/RepoName"` and `data-asset=".exe"` (the file type to offer).
- The site never links to your GitHub profile or repo pages. Buttons point straight at the file, and stay disabled until it's found.

## Add a new project

1. Copy one `<li class="item">` block in `index.html` and change the repo, name, tags, description and screenshot.
2. Copy a folder in `projects/` (for example `projects/crayon-nav-assist/`) for its detail page.
3. Put screenshots in `assets/img/`.

## Ads (Google AdSense)

1. Publish the site first, then sign up at https://adsense.google.com and add `commoncrayon.github.io` as a site.
2. Put your publisher ID in `ads.txt` (replace `pub-0000000000000000`) and push. Choose **ads.txt** as the verification method and request a review. Approval usually takes from a few days to a few weeks.
3. Once approved, create a display ad unit (Ads > By ad unit > Display ads) and put both IDs in `assets/js/ads.js`.
4. Block adult and other unwanted ads under **Brand safety > Blocking controls > All sites > Sensitive categories**. Block "References to sex and sexuality" and "Dating", plus anything else you don't want, such as gambling.
5. Under **Privacy & messaging**, turn on the European regulations message. Google requires a consent prompt for visitors in the EEA, UK and Switzerland.

Until the IDs are set, the ad slots stay hidden on the live site and show a placeholder box when previewing locally. The privacy page at `/privacy/` covers what AdSense needs disclosed.

## Preview locally

```
python -m http.server 8000
```
Then open http://localhost:8000.
