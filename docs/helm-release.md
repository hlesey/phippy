# Helm Release

```bash
git checkout helm-public
git pull --rebase origin master
helm package helm/*
helm repo index --url https://hlesey.github.io/phippy/ .
git add * 
git commit -a -m "release new helm version"
git push origin helm-public
```
