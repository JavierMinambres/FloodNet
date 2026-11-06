# Data provenance of the FloodNet project

This report records where every image and every mask comes from, what was used as the final dataset,
which data each model was trained and evaluated on, and what is known (and not known) about the
"revised" masks.

Each statement carries one of these levels of certainty:

- **[verified]**: checked against the files, the code or the outputs of the notebooks.
- **[inferred]**: deduced from the data on good grounds, but without direct confirmation from the source.
- **[unknown]**: no information available.

First written on 6 November 2026, against commit `0d0619b`. Translated to English and updated for the
frozen repository (tag `v1.0-paper`).

---

## 1. Summary in five points

1. The images are those of **FloodNet** (drone imagery taken after Hurricane Harvey, 10 classes). The
   project used two sources of masks for those same images: the **official** ones
   (FloodNet-Supervised v1.0, 2,343 masks) and an **alternative version of 398 of them**, published on
   Kaggle by the user *catashiro31*.
2. The **final dataset** is the 2,343 images of FloodNet-Supervised v1.0 with their official split.
   For the 398 images that have a Kaggle version, that mask is used. The 96 official masks that assign a
   single class to the whole image are excluded. This leaves **2,247 images: 1,387 for training, 434 for
   validation and 426 for test**.
3. The 398 Kaggle masks are **all in train**. **Validation and test use official masks only**, and
   these have known annotation errors. The test metrics are measured against noisy references.
4. The **three models** (hybrid CNN+ViT U-Net, DeepLabV3+ R50 and YOLO11n-seg) are trained and
   evaluated on exactly the same final dataset, the same split and at 512×512. YOLO trains with 9 classes
   (without *Background*); the other two train with 10.
5. The author of the Kaggle masks **does not document the method** of revision or say which masks were
   modified. That they were "corrected by hand" **is not stated in any source**. Earlier versions of the
   README and the notebooks said so; that wording has been corrected and must not reach the paper.

---

## 2. The original sources

### 2.1 FloodNet and its challenge (Track 1)

- Aerial drone images taken after Hurricane Harvey, 4000×3000 px JPEGs. **[verified]**
- 10 segmentation classes, with this index → name map **[verified]**:

  | Index | Class |
  |---:|---|
  | 0 | Background |
  | 1 | Building-flooded |
  | 2 | Building-non-flooded |
  | 3 | Road-flooded |
  | 4 | Road-non-flooded |
  | 5 | Water |
  | 6 | Tree |
  | 7 | Vehicle |
  | 8 | Pool |
  | 9 | Grass |

- Dataset reference: Rahnemoonfar et al., *FloodNet: A High Resolution Aerial Imagery Dataset for Post
  Flood Scene Understanding*, IEEE Access 9, 89644–89654, 2021. **[verified]**
- **FloodNet Challenge – Track 1** was the semi-supervised version of the challenge. Of its training
  partition, only **398 images** had a mask (`Train/Labeled/{Flooded,Non-Flooded}`), and validation and
  test had no public masks. **[verified** in the starting notebook and in the previous version of the
  project**]** It was downloaded from the Kaggle copy `aletbm/aerial-imagery-dataset-floodnet-challenge`,
  folder `FloodNet Challenge - Track 1/`, which includes a `class_mapping.csv`.

### 2.2 FloodNet-Supervised v1.0 (complete official masks)

- Published by BinaLab, the group that created FloodNet: <https://github.com/BinaLab/FloodNet-Supervised_v1.0>.
  **[verified]**
- It provides a mask for **all 2,343 images**, with the official split **[verified]**:

  | Partition | Images |
  |---|---:|
  | train | 1,445 |
  | val | 450 |
  | test | 448 |

- The index → class map comes from its `DATASET-VERSION-NOTE-v1.0.txt` and matches the table above.
  **[verified]**
- The file names of the 398 Track 1 images appear in `train-org-img`, and their masks in
  `train-label-img` (`<id>_lab.png`). **The 398 Track 1 images are a subset of the official train
  partition.** **[verified** by file name**]** That the remaining 1,047 images of the official train
  partition were the ones without a mask in Track 1 is **[inferred]** (1,445 − 398 = 1,047).

### 2.3 Kaggle dataset by *catashiro31* ("fixed mask")

- URL: <https://www.kaggle.com/datasets/catashiro31/floodnet-dataset-for-segmentation-fixed-mask>
- Title: *FloodNet Dataset for Segmentation (fixed mask)*. Subtitle: *"FloodNet Dataset for Image
  Segmentation – fixed and corrected mask version"*. Author: Kaggle user `catashiro31`, with no real name,
  affiliation or associated paper. Version 3, last updated on 14 January 2026. **[verified** with the
  public Kaggle API on 6 November 2026**]**
- Content: the **398 Track 1 images** with a mask of their own, split into `data_finally/train` (317)
  and `data_finally/val` (81), each with `image/`, `mask/` and `mask_colored/`. This 317/81 split is the
  Kaggle author's, **not the official one**: all 398 belong to the official train partition.
  **[verified]**
- The author's description, verbatim:

  > This dataset is a refined version of the original FloodNet dataset, designed for semantic
  > segmentation tasks in flood disaster analysis. All segmentation masks have been fixed and
  > standardized to correct common issues such as: Inconsistent label values · Misaligned masks
  > · Broken or missing annotations. The dataset aims to provide a clean, reliable benchmark for
  > training and evaluating deep learning models in flood-related computer vision tasks.

- **What it does not say [unknown]:** the method (manual, semi-automatic or automatic), the tool, the
  number of annotators, whether there was cross-review and which masks it changed. There is no change
  log. The licence is listed as *"Other (specified in description)"*, but the description does not
  specify any.
- It uses the same class index as the official masks. **[inferred]** With a different index, almost
  every pixel of every mask would change. In fact 19 masks are identical and the median change is 2.5 %
  of the pixels (section 5).

---

## 3. History of how the data was used (three stages)

This matters because the notebooks quote figures from earlier stages.

### Stage 0: the Kaggle starting notebook

File `original-hybrid-cnn-vit-attention-u-net.ipynb`, kept unchanged. **[verified** in its code**]**

- **Train**: the 398 Track 1 images with their **official masks**, uncorrected.
- **Validation and test**: the 81 images of `data_finally/val` (Kaggle masks), split with
  `train_test_split(test_size=0.3, random_state=42)`, which gives 56 for validation and 25 for test.
- **Data leakage**: those 81 images are part of the 398 training images. 100 % of its validation and
  test images had been seen in training, although with a different mask.
- Its metrics also averaged IoU over batches and gave 1.0 to absent classes. Its reported result (test
  IoU 0.662) is not valid as a reference.

### Stage 1: "reduced dataset"

Git tag `dataset-reducido`, commit `a027121` of 13 October 2026. **[verified]**

- **Single source: the Kaggle dataset** (`data_finally`), images and masks. From Track 1 only
  `class_mapping.csv` and the Flooded/Non-Flooded category of each image were used.
- Split without leakage:

  | Partition | Source | Images |
  |---|---|---:|
  | train | `data_finally/train` | 317 |
  | val | half of `data_finally/val`, stratified by Flooded/Non-Flooded, seed 42 | 40 |
  | test | the other half | 41 |

- The three models were trained at this stage. Test mIoU with 10 classes: U-Net 0.714, DeepLabV3+
  0.696, YOLO11n-seg 0.678.
- Train, validation and test used **Kaggle masks only**. With a 41-image test set, these figures **are
  not comparable** with those of stage 2.

### Stage 2: full dataset (current version)

From commit `bf55fb6` of 13 October 2026. This is the version the paper describes. **[verified]**

- Main source: **FloodNet-Supervised v1.0**, images and masks.
- The **Kaggle masks replace the official one** for the 398 images that have one. The **images** are
  always the official ones: those in `data_finally/*/image` are not used.
- Matching is done by file name only (`<id>.png` in Kaggle ↔ `<id>.jpg` and `<id>_lab.png` in the
  official release). That the Kaggle photos are identical to the official ones **has not been checked
  pixel by pixel**. The Kaggle masks fit the official photo visually on buildings, roads and trees.
  **[inferred]**

---

## 4. The final dataset (stage 2) in detail

### 4.1 Construction rules

They are in section 1 of `floodnet-segmentation.ipynb`, function `construir_cache()` and the exclusion
cell. **[verified]**

1. If a Kaggle mask exists for the image, it is used. Otherwise, the official one.
2. **Official** masks with a single class over the whole image (failed annotations) are excluded. A
   Kaggle mask with a single class is **not** excluded: there is only one, `6595`, all *Grass* (the
   official one had 2.25 % of *Tree*).
3. The remaining official masks are used as they are.
4. The official split is kept: no image changes partition.
5. Images and masks are reduced once to 512×512, the image with `INTER_AREA` and the mask with
   `INTER_NEAREST`, and stored in `data/cache512_full/`. `index.csv` records the partition, the source of
   the mask (`oficial` for official or `reparada` for revised) and the classes present at full
   resolution. If a mask does not have the size of its image, it is first resized to the image with
   `INTER_NEAREST`. Whether this happened with any Kaggle mask is **[unknown]**.

### 4.2 Official single-class masks

**[verified]**

| Partition | Official single-class masks | Of which replaced by Kaggle | Excluded |
|---|---:|---:|---:|
| train | 84 | 26 | 58 (56 *Grass*, 2 *Water*) |
| val | 16 | 0 | 16 (*Grass*) |
| test | 22 | 0 | 22 (20 *Grass*, 2 *Water*) |
| **total** | **122** | **26** | **96** |

The 26 replaced masks are `10165` and `10166` (all *Water*) and 24 all *Grass*: 7909, 7918, 7920, 7925,
7931, 7967, 7973, 8015, 8033, 8060, 8061, 8106, 8119, 8130, 8141, 8407, 8408, 8412, 8415, 8422, 8424,
8658, 8794 and 8800. Their Kaggle versions all have more than one class.

### 4.3 Final composition

**[verified]** The notebooks check it with an `assert`.

| Partition | Official | Excluded | Used | Kaggle mask | Official mask |
|---|---:|---:|---:|---:|---:|
| train | 1,445 | 58 | **1,387** | 398 | 989 |
| val | 450 | 16 | **434** | 0 | 434 |
| test | 448 | 22 | **426** | 0 | 426 |
| total | 2,343 | 96 | **2,247** | 398 | 1,849 |

Consequences:

- **28.7 %** of train (398 of 1,387) has a Kaggle mask. Validation and test have none.
- **Validation and test contain annotation noise.** Only the single-class error could be removed. The
  other kind of error, regions with the wrong class, cannot be detected without a reference. Section 5
  estimates its size.

---

## 5. Comparison between the official and the Kaggle masks

### 5.1 How the "revised" masks are identified

**[verified]** The author does not mark which masks were modified. The project calls "revised"
(`reparada`) every image whose name appears in `data_finally/{train,val}/mask`, whether it changed or not.
"Revised" means **"has a Kaggle version"**, not "was modified". What actually changed is only known by
comparing each Kaggle mask with its official counterpart.

### 5.2 Two measurements

1. **Audit in the main notebook** (section 1.3, `AUDITAR = True`). It was run while `data_finally` was on
   disk, at full resolution subsampled one row and column in four: **138** of the 398 differ in more than
   5 % of their pixels and **88** in more than 10 %. The dominant changes are *Water → Grass* and
   *Tree → Grass*. **[verified** in the notebook text; the cell is saved with `AUDITAR = False`**]**
2. **Review of 6 November 2026** (folder `revision_mascaras/`). `data_finally` is no longer on disk, but
   `data/cache512_full/mask/` keeps its masks at 512 px. Each one was compared with the official mask
   reduced to 512 px with `INTER_NEAREST`. **[verified]**

   | Pixels changed | Masks (of 398) |
   |---|---:|
   | 0 (identical) | 19 |
   | > 1 % | 278 |
   | > 5 % | 139 |
   | > 10 % | 88 |
   | > 20 % | 52 |
   | > 50 % | 9 |

   This agrees with the notebook audit. The one-mask difference at the 5 % threshold is due to the
   resolution. The paper uses this second measurement.

### 5.3 Visual review

Sixteen cases were reviewed by eye, at 256 px per panel. At that resolution only large regions can be
judged, not borders or small classes. **[verified** by inspection, with a necessarily subjective
judgement**]**

- **Clear improvements.** `7774` (a whole meadow marked as water), `7931` (official mask all *Grass*;
  the Kaggle one adds the row of trees and the pond), `9027` and `9022` (scrubland marked as
  *Background*), `7357` and `7364` (water covered the gardens up to the houses). Many others only refine
  the borders of trees and buildings.
- **Debatable.** `7882`, `7879` and `7884` turn large areas of dense, tall vegetation that the official
  mask had as *Tree* into *Grass*. `7261` turns a flooded street from *Road-flooded* into *Water*. `8966`
  narrows the water channel considerably.
- **Apparent error.** `6600`: the dirt baseball field becomes *Grass*. In the same image the water is
  correctly revised.

Cautious conclusion: most large changes improve the mask, but the revision is not perfect and contains
judgement calls, above all at the *Tree*/*Grass* boundary. It has not been reviewed systematically.

### 5.4 Material available

In `revision_mascaras/` (see its README):

- `reparadas_vs_oficiales.csv`: the 398 images, with the % of pixels changed and the three main class
  changes. The `clases_oficial` and `clases_reparada` columns are measured at 512 px and are not
  reliable, because small classes disappear. Class counts at full resolution are those of
  `data/cache512_full/index.csv`.
- `lamina_01.png` … `lamina_18.png`: the 139 images with more than 5 % change, sorted from largest to
  smallest. Each row shows the photo, the official mask, the Kaggle mask and the changed pixels in red.
- `scripts/comparar.py` and `scripts/laminas.py`, which regenerate everything from the project root.

### 5.5 What a solid verification would need

Downloading the Kaggle dataset again and doing two things: (a) comparing its photos with the official
ones to confirm that the same name means the same image, and (b) repeating the comparison at full
resolution.

---

## 6. Which data each model is trained and evaluated on (stage 2)

**[verified]** in the notebooks.

| | Hybrid CNN+ViT U-Net | DeepLabV3+ (ResNet-50) | YOLO11n-seg |
|---|---|---|---|
| Notebook | `floodnet-segmentation.ipynb` | `floodnet-deeplabv3plus.ipynb` | `floodnet-yolo11n-seg.ipynb` |
| Data | `data/cache512_full` | the same cache | the same cache, converted to polygons in `data/yolo512_full` |
| Split | 1,387 / 434 / 426 | the same | the same |
| Resolution | 512×512 | 512×512 | 512×512 |
| Classes trained | 10 | 10 | 9 (without *Background*) |
| Particulars | oversampling of rare classes (`target_ratio = 0.5`) with strong augmentation on the copies; flip TTA in validation and test; **no fixed seed** | seed 42; padding pixels of the augmentation set to `ignore_index = 255`; no oversampling or TTA | seed 42; each connected component of each class is a polygon instance; *Background* = pixels without an instance |
| Epochs | 30 | 40 | ceiling of 300, early stop at 268 |

- **Common evaluation:** the 426 test images, with official masks. `SegMetrics` accumulates the
  confusion matrix of the whole test set and divides once. The YOLO prediction is rasterised to 10
  classes (what is not covered is *Background*), so all three are measured in the same way.
  `floodnet-paper-evaluation.ipynb` reloads the three checkpoints and reproduces their test mIoU.
- **YOLO ceiling from the conversion:** rebuilding the 2,247 masks from their polygons gives an mIoU of
  0.977 against the original mask.
- **YOLO used to have *Background* as a class** (that run is in commit `dfdde06`; *Background* was removed from the YOLO classes in `3c9b346`). With that configuration it
  reached an mIoU of 0.705 with 10 classes and 0.739 without *Background*. The current version without
  *Background* gives 0.661 and 0.730.

Test mIoU, stage 2:

| | U-Net | DeepLabV3+ | YOLO11n-seg |
|---|---:|---:|---:|
| 10 classes | 0.732 | 0.709 | 0.661 |
| without *Background* | 0.754 | 0.738 | 0.730 |

The per-class and per-image breakdown and the parameters are in `floodnet_resultados.xlsx`.

---

## 7. What can and cannot be stated in the paper

**Can be stated:**

- FloodNet-Supervised v1.0 is used with its official split, 96 official single-class masks are
  excluded, and for 398 training images alternative masks from a public Kaggle dataset are used (cite
  URL, author and version 3).
- Validation and test are evaluated against official masks, which contain annotation errors. This can
  be quantified with the comparison in section 5, explaining that it is an estimate made on train.
- The comparison between the three models is fair: same data, same split, same resolution and same
  metric.

**Must not be stated:**

- That the Kaggle masks are "corrected by hand", "by experts" or "verified". They must be described as
  **"revised masks published by a third party, method not documented"**.
- That all 398 were corrected: 19 are identical to the official one.
- That the Kaggle masks are a clean reference: there is at least one apparent error (`6600`) and several
  debatable decisions.
- Direct comparisons with the figures of stage 1 (reduced dataset) or with the Kaggle starting notebook.
  They use another test set, other masks and, in the latter case, data leakage and faulty metrics.

**Errata (fixed).** Earlier versions of `README.md` and of the three notebooks described the Kaggle masks
as "corrected by hand". That wording was an assumption without a source; it has been replaced in the
README, in the markdown cells and in the code comments, without re-running any notebook.
