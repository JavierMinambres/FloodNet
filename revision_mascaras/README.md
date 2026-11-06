# Mask review: official versus revised masks

Comparison between the official FloodNet-Supervised v1.0 masks and the 398 revised masks from the
Kaggle dataset by *catashiro31*, made on 6 November 2026. The context and the conclusions are in
[../docs/data_provenance.md](../docs/data_provenance.md), section 5.

File and column names are in Spanish because they are the outputs of the scripts as they were run.

## Files

| File | What it is |
|---|---|
| `reparadas_vs_oficiales.csv` | One row per revised image (398). See the columns below. |
| `lamina_01.png` … `lamina_18.png` | Contact sheets with the 139 images whose revised mask differs from the official one in more than 5 % of the pixels, sorted from largest to smallest change, 8 per sheet. Each row: photo, official mask, revised mask and changed pixels in red. The header text of each row reads `<id> \| <n>% distinto \| foto - oficial - corregida - diferencia` (photo, official, revised, difference). |
| `scripts/comparar.py` | Builds `reparadas_vs_oficiales.csv` and prints the counts per threshold. |
| `scripts/laminas.py` | Builds the contact sheets from the CSV. |

### Columns of `reparadas_vs_oficiales.csv`

| Column | Meaning |
|---|---|
| `stem` | Image id. |
| `pct_distinto` | % of pixels that differ between the official and the revised mask, both at 512×512. |
| `clases_oficial`, `clases_reparada` | Number of classes in the official and revised mask at 512×512. Not reliable: small classes can disappear at that resolution. |
| `cambios_principales` | The three most frequent class changes (official → revised) with their % of the image. |

## How to regenerate

From the project root, with `data/cache512_full` and the official masks in place:

```bash
uv run python revision_mascaras/scripts/comparar.py . revision_mascaras
uv run python revision_mascaras/scripts/laminas.py . revision_mascaras 5
```

`comparar.py` reads the revised masks from the cache (`data/cache512_full/mask/`, entries marked
`reparada` in `index.csv`) and the official ones from
`data/FloodNet/FloodNet-Supervised_v1.0/train/train-label-img/`, reduced to 512 px with nearest-neighbour
interpolation. The last argument of `laminas.py` is the minimum % of changed pixels.

## Summary of the results

| Pixels changed | Masks (of 398) |
|---|---:|
| 0 (identical) | 19 |
| > 1 % | 278 |
| > 5 % | 139 |
| > 10 % | 88 |
| > 20 % | 52 |
| > 50 % | 9 |

The most frequent changes are *Water → Grass*, *Tree → Grass* and *Background → Grass*.
