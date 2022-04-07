# Helm Release

```bash
helm package helm/
helm repo index --url https://hlesey.github.io/phippy/ .
git checkout gh-pages
git add *
git commit -a -m "release new helm version"
git push origin gh-pages
```
