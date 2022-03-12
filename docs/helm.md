Helm install

```bash
helm repo add hlesey https://hlesey.github.io/phippy/helm
helm search phippy
```


## Usage

[Helm](https://helm.sh) must be installed to use the charts.  Please refer to
Helm's [documentation](https://helm.sh/docs) to get started.

Once Helm has been set up correctly, add the repo as follows:

```bash
helm repo add hlesey https://hlesey.github.io/phippy/helm-charts
```

If you had already added this repo earlier, run `helm repo update` to retrieve
the latest versions of the packages.  You can then run `helm search repo
hlesey` to see the charts.

To install the hlesey chart:

```bash
helm install phippy hlesey/phippy
```

To uninstall the chart:
 
```bash
helm delete phippy
```
