# FloodNet: semantic segmentation of UAV flood imagery

Code, notebooks and results behind the paper *UAV-Based Flood Mapping for Rescue Missions and
Autonomous Navigation in Challenging Outdoor Environments* (Miñambres-Calvo, Riego and
Sánchez-González, Robotics Group, Universidad de León).

Three models segment drone images taken after Hurricane Harvey into ten classes (water, flooded and
non-flooded buildings and roads, vehicles, vegetation…), all on the same data and with the same metric:

- a **hybrid CNN + Transformer U-Net** (ConvNeXt-Tiny encoder, 12 Transformer blocks, ASPP and
  attention gates);
- **DeepLabV3+** with a ResNet-50 encoder, as a semantic baseline;
- **YOLO11n-seg**, a 2.9 M-parameter instance model, as a candidate for on-board use.

> **This repository is frozen.** It holds the exact state from which every number and figure in the
> paper was produced (tag `v1.0-paper`). Nothing is changed after publication. The trained weights are
> attached to the `v1.0-paper` release, and the dataset used in the experiments is published on Zenodo
> (DOI: *pending*).

---

## Results

Official FloodNet-Supervised v1.0 test split without single-class masks: **426 images** at 512×512.
Every figure comes from a single confusion matrix accumulated over the whole test set (see
[How the metrics are computed](#how-the-metrics-are-computed)).

| Metric (test) | Hybrid U-Net | DeepLabV3+ R50 | YOLO11n-seg |
|---|---:|---:|---:|
| mIoU (10 classes) | **0.732** | 0.709 | 0.661 |
| mIoU (without *Background*) | **0.754** | 0.738 | 0.730 |
| Mean Dice (10 classes) | **0.841** | 0.823 | 0.763 |
| Pixel accuracy | **0.910** | 0.908 | 0.883 |
| mIoU (10 classes), single pass without TTA | **0.728** | 0.709 | 0.661 |
| Parameters | 86.7 M | 26.7 M | **2.9 M** |
| Training (RTX 4060 Laptop) | 2 h 15 min, 30 epochs | **47 min**, 40 epochs | 2.1 h, 268 epochs |

| Class | % of training pixels | IoU U-Net | IoU DeepLabV3+ | IoU YOLO11n-seg |
|---|---:|---:|---:|---:|
| Grass | 55.47 | 0.884 | **0.885** | 0.870 |
| Tree | 18.11 | 0.815 | 0.831 | **0.834** |
| Water | 10.95 | **0.772** | 0.757 | 0.716 |
| Road-non-flooded | 5.85 | **0.833** | 0.831 | 0.821 |
| Building-non-flooded | 3.35 | **0.806** | 0.800 | 0.769 |
| Road-flooded | 2.74 | **0.666** | 0.612 | 0.646 |
| Building-flooded | 1.69 | 0.707 | **0.711** | 0.704 |
| Background | 1.43 | **0.526** | 0.450 | 0.036 |
| Pool | 0.21 | **0.680** | 0.647 | 0.661 |
| Vehicle | 0.19 | **0.626** | 0.570 | 0.552 |

What the numbers say:

- **The U-Net leads in seven of the ten classes**, with its largest margins in the minority classes
  that its oversampling targets (*Background*, *Vehicle*, *Road-flooded*, *Pool*). Test-time
  augmentation only accounts for 0.4 of its 2.3-point lead over DeepLabV3+.
- **YOLO11n-seg loses almost everything in *Background*.** *Background* is not one of its classes:
  it is whatever no instance covers, and the model does not learn to leave regions uncovered. Without
  *Background* it stays within one point of DeepLabV3+ with 9.4 times fewer parameters.
- **IoU follows class representation.** The Spearman correlation between the share of training
  pixels and the test IoU is 0.85 to 0.88 for the three models (p ≤ 0.002). Scarce classes
  (*Road-flooded*, *Building-flooded*, *Background*: present in few images, large when present) and
  small classes (*Vehicle*, *Pool*: present often, under 1 % of the image) both score low, for
  different reasons.

`docs/paper_traceability.md` maps every number in the paper to the notebook cell or file it comes
from.

---

## Repository contents

| Path | What it is |
|---|---|
| [floodnet-segmentation.ipynb](floodnet-segmentation.ipynb) | Main notebook: environment, data audit, hybrid U-Net, training and evaluation. |
| [floodnet-deeplabv3plus.ipynb](floodnet-deeplabv3plus.ipynb) | DeepLabV3+ (ResNet-50) on the same split, exported to ONNX. |
| [floodnet-yolo11n-seg.ipynb](floodnet-yolo11n-seg.ipynb) | YOLO11n-seg on the same split, with the masks converted to polygons, exported to ONNX. |
| [floodnet-paper-evaluation.ipynb](floodnet-paper-evaluation.ipynb) | Final evaluation for the paper. Loads the three trained models without training, checks that they reproduce the reported mIoU, computes the test confusion matrices and the U-Net result without TTA, and generates every paper figure. |
| [paper/](paper) | Outputs of the evaluation notebook: `confusion_test.npz`, `test_metrics.json` and `figures/`. |
| [floodnet_resultados.xlsx](floodnet_resultados.xlsx) | Results workbook: global, per-class and per-image test metrics of the three models, their parameters and the class distribution of the dataset. |
| [docs/data_provenance.md](docs/data_provenance.md) | Where every image and mask comes from, what the final dataset is and what is known about the revised masks. |
| [docs/paper_traceability.md](docs/paper_traceability.md) | Source of every number and figure in the paper. |
| [revision_mascaras/](revision_mascaras) | Comparison between the official and the revised masks (CSV, contact sheets and the scripts that generate them). |
| [original-hybrid-cnn-vit-attention-u-net.ipynb](original-hybrid-cnn-vit-attention-u-net.ipynb) | The public Kaggle notebook used as the starting point for the U-Net ([huyhoangti](https://www.kaggle.com/code/huyhoangti/hybrid-cnn-vit-attention-u-net)), kept unchanged for comparison. |
| [pyproject.toml](pyproject.toml), [uv.lock](uv.lock) | Environment managed with `uv`, with exact resolved versions. |

**A note on language.** The prose of the repository (this README, `docs/`, the markdown cells and the
code comments of the notebooks) is in English. The code identifiers, the printed outputs of the three
training notebooks and the sheet names of `floodnet_resultados.xlsx` are in Spanish, as they were when
the experiments ran. Translating them would mean re-running the training notebooks, and the U-Net has no
fixed seed, so a re-run would not give the same weights or the same numbers.

The dataset, the image cache, the trained checkpoints and the exported models (`data/`, `models/`,
`runs/`) are not in the repository because of their size; `.gitignore` excludes them.

---

## Data

The images and official masks come from **FloodNet-Supervised v1.0**
([BinaLab/FloodNet-Supervised_v1.0](https://github.com/BinaLab/FloodNet-Supervised_v1.0); Rahnemoonfar
et al., *IEEE Access* 9, 2021). For 398 training images, a revised mask from a public Kaggle dataset
([catashiro31, *FloodNet Dataset for Segmentation (fixed mask)*](https://www.kaggle.com/datasets/catashiro31/floodnet-dataset-for-segmentation-fixed-mask),
version 3) replaces the official one. Its author does not document how the masks were revised or which
ones changed; `docs/data_provenance.md` and `revision_mascaras/` measure the differences.

The final dataset follows three rules:

1. If an image has a revised mask, that mask is used.
2. Official masks that assign a single class to the whole image are excluded (96 images).
3. The official split is kept: no image changes partition.

| Partition | Official | Excluded | Used | With revised mask |
|---|---:|---:|---:|---:|
| train | 1,445 | 58 | 1,387 | 398 |
| val | 450 | 16 | 434 | 0 |
| test | 448 | 22 | 426 | 0 |

Validation and test keep the official masks, which contain annotation errors (mostly water/grass). The
absolute scores are affected by that noise; the comparison between models is fair because all three
are measured against the same references.

The dataset ready to use, with the revised masks in place and the exclusions applied, is published on
Zenodo (DOI: *pending*). To rebuild it from the original sources instead, unpack them under `data/`:

```
data/
├── FloodNet/
│   └── FloodNet-Supervised_v1.0/
│       ├── DATASET-VERSION-NOTE-v1.0.txt
│       ├── train/  (train-org-img · train-label-img — 1,445 images)
│       ├── val/    (val-org-img   · val-label-img   —   450 images)
│       └── test/   (test-org-img  · test-label-img  —   448 images)
├── data_finally/
│   ├── train/mask   ┐ 398 revised masks (Kaggle)
│   └── val/mask     ┘
├── cache512_full/   ← built by the main notebook, do not download
└── yolo512_full/    ← built by the YOLO notebook
```

The main notebook builds `data/cache512_full` (all images reduced to 512×512, images with
`INTER_AREA` and masks with `INTER_NEAREST`) and an `index.csv` that records each image's partition and
whether its mask is official (`oficial`) or revised (`reparada`). The other notebooks reuse that cache.

---

## Trained models

The checkpoints used in the paper are attached to the `v1.0-paper` release, and
[CHECKSUMS.sha256](CHECKSUMS.sha256) lists their SHA-256 hashes. Download them and put them back in the
paths below to run the evaluation notebook:

| Release asset | Path in the project | Model |
|---|---|---|
| `best_model_iou_full.pth` | `models/best_model_iou_full.pth` | Hybrid U-Net, best validation mIoU (epoch 30) |
| `deeplabv3plus_r50_full_best.pt` | `models/deeplabv3plus_r50_full_best.pt` | DeepLabV3+ R50, best validation mIoU (epoch 32) |
| `deeplabv3plus_r50_floodnet_full.onnx` | `models/deeplabv3plus_r50_floodnet_full.onnx` | DeepLabV3+ exported to ONNX |
| `yolo11n-seg-full_best.pt` | `runs/yolo/yolo11n-seg-full/weights/best.pt` | YOLO11n-seg, best validation fitness (epoch 218) |
| `yolo11n_seg_floodnet_full.onnx` | `models/yolo11n_seg_floodnet_full.onnx` | YOLO11n-seg exported to ONNX |

The small training records are in the repository itself: the parameter and split files of the two
comparison models (`models/*_config.json`), the DeepLabV3+ training history
(`models/deeplabv3plus_r50_full_best.csv`) and the Ultralytics run log (`runs/yolo/yolo11n-seg-full/`
`results.csv` and `args.yaml`). The U-Net training history is in the outputs of its notebook.

Both ONNX files take the same input, `images`: float32 RGB in [0, 1], 1×3×512×512. DeepLabV3+ returns
`logits` (1×10×512×512) and only needs an `argmax`. YOLO11n-seg returns `output0` (1×45×5376: boxes, 9
classes and mask coefficients) and `output1` (1×32×128×128 prototypes), and needs NMS, mask assembly and
repainting outside the graph. On test, both ONNX files match their PyTorch model within 0.00002 mIoU.

---

## Setup

The environment is managed with [uv](https://docs.astral.sh/uv/), which also downloads Python 3.12.

```bash
# Install uv (Windows/PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create the environment and install everything
uv sync

# Register the Jupyter / VS Code kernel
uv run python -m ipykernel install --user --name floodnet --display-name "FloodNet (Python 3.12)"
```

The first sync downloads about 3 GB (PyTorch with CUDA). The wheels target **CUDA 12.6**; for another
CUDA version, or without a GPU, change the PyTorch index in `pyproject.toml`. `onnxruntime-gpu` is pinned
to 1.24 because the latest PyPI wheels are built against CUDA 13 and do not load alongside PyTorch cu126.

## Reproducing the paper

- **Without training (minutes):** with the data under `data/` and the release checkpoints in place, run
  `floodnet-paper-evaluation.ipynb` with the `FloodNet (Python 3.12)` kernel. It stops with an `assert`
  if any model does not reproduce its reported mIoU (0.7315 / 0.7094 / 0.6607), and rewrites `paper/`.
- **From scratch (hours):** run the three training notebooks in order. The DeepLabV3+ and YOLO notebooks
  have a fixed seed; the U-Net notebook does not, so a new run gives different weights and slightly
  different figures. Re-running the U-Net notebook top to bottom retrains it.

---

## The models

### Hybrid U-Net

```
image 512×512
      │
      ▼
ConvNeXt-Tiny (pretrained)  →  x1 x2 x3 x4   multi-scale skips
      │
      ▼
4×4 patch embedding + position  →  tokens (dim 512)
      │
      ▼
12 Transformer blocks (8-head MHSA + MLP)   global context
      │
      ▼
ASPP (rates 1·6·12·18)   multi-scale bottleneck
      │
      ▼
Decoder ×4 with attention gates on each skip
      │
      ▼
1×1 head → 10 classes     (+ 2 auxiliary heads, deep supervision)
```

The convolutional encoder brings the locality bias that a training set of about 1,400 images needs, and
the Transformer blocks add the scene-level context that separates a flooded road from a river.

| Training | |
|---|---|
| Loss | Focal + Dice + Lovász-Softmax, class weights `1 / log(1.02 + n)` (n = training images containing the class) |
| Optimiser | AdamW, lr 3e-5, weight decay 1e-4 |
| Scheduler | CosineAnnealingWarmRestarts (T₀ = 10, T_mult = 2) |
| Precision | Mixed (AMP) with GradScaler |
| Batch, epochs | 4 images of 512×512, 30 epochs of 874 iterations |
| Oversampling | Images with rare classes repeated until each appears at least ~650 times per epoch (`target_ratio = 0.5`); copies get strong augmentation, originals a mild one |
| Inference | TTA: average over the image and its three flips |

### DeepLabV3+

ResNet-50 encoder pretrained on ImageNet, output stride 16 (`segmentation-models-pytorch`). Weighted
cross-entropy + Dice, AdamW (lr 1e-4) with cosine annealing over 40 epochs, batch 8, mild augmentation
only, no oversampling and no TTA. Padding pixels from the affine augmentation are ignored by the loss.

### YOLO11n-seg

Pretrained on COCO. FloodNet has regions, not instances, so every connected component of every class
except *Background* becomes a polygon (components under 20 px dropped, holes containing *Background*
opened). Rasterising the polygons back gives 0.977 mIoU, the ceiling of the conversion. At inference,
instances are painted from largest to smallest area and uncovered pixels become *Background*. Trained
with the Ultralytics defaults, batch 16, mosaic, horizontal and vertical flips, up to 300 epochs with
patience 50 (stopped at 268); confidence threshold 0.25 chosen on validation.

---

## How the metrics are computed

Dice and IoU are computed from the confusion matrix of the whole set, accumulated batch by batch and
divided once at the end (`SegMetrics`). A class with no pixels in either the prediction or the reference
over the whole set is `NaN` and stays out of the mean. The per-class breakdown and the global figures
are consistent by construction.

## Changes to the starting notebook

The U-Net architecture comes from the public Kaggle notebook by
[huyhoangti](https://www.kaggle.com/code/huyhoangti/hybrid-cnn-vit-attention-u-net). We kept the
architecture and fixed how it was trained and measured:

- **Data leakage.** Its validation and test images were part of its own training set. We use the
  official split.
- **Metrics.** It averaged IoU per batch and gave 1.0 to any class absent from both prediction and
  reference (`ε/ε`), which inflated the mean. We accumulate a single confusion matrix.
- **Class weights.** They were hard-coded for a different training set. We count them on the actual
  split.
- **Gradient clipping.** `scaler.unscale_(optimizer)` was missing before `clip_grad_norm_`, so with AMP
  the clipping acted on scaled gradients and never clipped anything.
- **Scheduler.** `scheduler.step(val_loss)` passed a loss to `CosineAnnealingWarmRestarts`, which reads
  its argument as the epoch number, so the learning rate jumped erratically.
- **Deprecations and plotting.** `torch.cuda.amp.GradScaler()` was replaced with
  `torch.amp.GradScaler('cuda')`, and the example images are de-normalised before plotting.

Its reported test IoU (0.662) is not comparable with ours, because of the leakage and the metric.

## Known limitations

- **Validation and test references are noisy.** Apart from the excluded single-class masks, the
  official masks are used as they are. Judging by the 398 revised training masks, a sizeable share of
  them contain mislabelled regions, so the absolute scores are probably underestimated.
- **Single runs.** Each model was trained once, and the U-Net without a fixed seed.
- **The U-Net validation loss is not on the same scale as the training loss**, because the
  TTA-averaged probabilities go into a loss that expects logits. It is only used for early stopping,
  which never triggered; the reported metrics do not depend on it.

## Credits

Dataset: FloodNet (Rahnemoonfar et al., 2021). Revised training masks: Kaggle user catashiro31. Starting
point of the U-Net: Kaggle notebook by huyhoangti. This work was funded by grant PID2024-161761OB-C21
(MICIU/AEI/10.13039/501100011033 and ERDF/EU).
