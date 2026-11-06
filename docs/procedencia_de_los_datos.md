# Procedencia de los datos del proyecto FloodNet

Informe para quien redacte el paper. Recoge de dónde sale cada imagen y cada máscara, qué
se ha usado como dataset final, con qué datos se ha entrenado y evaluado cada modelo y qué
se sabe (y qué no) de las máscaras "corregidas".

Cada afirmación lleva uno de estos niveles de certeza:

- **[verificado]**: comprobado sobre los archivos, el código o las salidas de los cuadernos.
- **[inferido]**: deducido de los datos con buena base, pero sin confirmación directa de la fuente.
- **[desconocido]**: no hay información.

Fecha de redacción: 06/11/2026. Estado del repositorio: commit `0d0619b`.

---

## 1. Resumen en cinco puntos

1. Las imágenes son las de **FloodNet** (dron, posteriores al huracán Harvey, 10 clases).
   El proyecto ha usado dos fuentes de máscaras para esas mismas imágenes: las **oficiales**
   (FloodNet-Supervised v1.0, 2.343 máscaras) y una **versión alternativa de 398 de ellas**,
   publicada en Kaggle por el usuario *catashiro31*.
2. El **dataset final** son las 2.343 imágenes de FloodNet-Supervised v1.0 con su partición
   oficial. En las 398 imágenes que tienen versión de Kaggle se usa esa máscara. Además se
   excluyen las 96 máscaras oficiales que asignan una sola clase a toda la imagen. Quedan
   **2.247 imágenes: 1.387 de train, 434 de val y 426 de test**.
3. Las 398 máscaras de Kaggle están **todas en train**. **Val y test usan solo máscaras
   oficiales**, y estas tienen errores de anotación conocidos. Las métricas de test se miden
   contra referencias con ruido.
4. Los **tres modelos** (U-Net híbrido CNN+ViT, DeepLabV3+ R50 y YOLO11n-seg) se entrenan y
   evalúan sobre exactamente el mismo dataset final, la misma partición y a 512×512.
   YOLO entrena con 9 clases (sin *Background*). Los otros dos entrenan con 10.
5. El autor de las máscaras de Kaggle **no documenta el método** de corrección ni indica qué
   máscaras modificó. Que estén "corregidas a mano" **no consta en ninguna fuente**: es una
   suposición que hoy aparece en el README y en los cuadernos del repositorio y que **no debe
   pasar al paper**.

---

## 2. Las fuentes originales

### 2.1 FloodNet y su reto (Track 1)

- Imágenes aéreas de dron tomadas tras el huracán Harvey, JPEG de 4000×3000 px. **[verificado]**
- 10 clases de segmentación, con este índice → nombre **[verificado]**:

  | Índice | Clase |
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

- Referencia del dataset: Rahnemoonfar et al., *FloodNet: A High Resolution Aerial Imagery
  Dataset for Post Flood Scene Understanding*, IEEE Access, 2021. **[comprobar la cita
  exacta antes de publicar]**
- **FloodNet Challenge – Track 1** era la versión semisupervisada del reto. De su partición de
  train solo **398 imágenes** tenían máscara (`Train/Labeled/{Flooded,Non-Flooded}`), y val y
  test no tenían máscaras públicas. **[verificado** en el cuaderno de partida y en la versión
  anterior del proyecto**]** Se descargó de la copia de Kaggle
  `aletbm/aerial-imagery-dataset-floodnet-challenge`, carpeta `FloodNet Challenge - Track 1/`,
  que incluye un `class_mapping.csv`.

### 2.2 FloodNet-Supervised v1.0 (máscaras oficiales completas)

- Lo publica BinaLab, el grupo autor de FloodNet: <https://github.com/BinaLab/FloodNet-Supervised_v1.0>.
  **[verificado]**
- Publica máscara para **las 2.343 imágenes**, con la partición oficial **[verificado]**:

  | Partición | Imágenes |
  |---|---:|
  | train | 1.445 |
  | val | 450 |
  | test | 448 |

- El mapa índice → clase sale de su `DATASET-VERSION-NOTE-v1.0.txt` y coincide con la tabla
  anterior. **[verificado]**
- Los nombres de archivo de las 398 imágenes de Track 1 aparecen en `train-org-img` y sus
  máscaras en `train-label-img` (`<id>_lab.png`). **Las 398 de Track 1 son un subconjunto del
  train oficial.** **[verificado** por coincidencia de nombres**]** Que las 1.047 imágenes
  restantes del train oficial fueran las que en Track 1 no tenían máscara es **[inferido]**
  (1.445 − 398 = 1.047).

### 2.3 Dataset de Kaggle de *catashiro31* ("fixed mask")

- URL: <https://www.kaggle.com/datasets/catashiro31/floodnet-dataset-for-segmentation-fixed-mask>
- Título: *FloodNet Dataset for Segmentation (fixed mask)*. Subtítulo: *"FloodNet Dataset for
  Image Segmentation – fixed and corrected mask version"*. Autor: usuario de Kaggle
  `catashiro31`, sin nombre real, afiliación ni artículo asociado. Versión 3, última
  actualización el 14/01/2026. **[verificado** con la API pública de Kaggle el 06/11/2026**]**
- Contenido: las **398 imágenes de Track 1** con una máscara propia. Las reparte en
  `data_finally/train` (317) y `data_finally/val` (81), cada una con `image/`, `mask/` y
  `mask_colored/`. Esta división en 317/81 es del autor de Kaggle, **no es la oficial**: las 398
  pertenecen al train oficial. **[verificado]**
- Descripción del autor, literal:

  > This dataset is a refined version of the original FloodNet dataset, designed for semantic
  > segmentation tasks in flood disaster analysis. All segmentation masks have been fixed and
  > standardized to correct common issues such as: Inconsistent label values · Misaligned masks
  > · Broken or missing annotations. The dataset aims to provide a clean, reliable benchmark for
  > training and evaluating deep learning models in flood-related computer vision tasks.

- **Lo que no dice [desconocido]:** el método (manual, semiautomático o automático), la
  herramienta, el número de anotadores, si hubo revisión cruzada y qué máscaras cambió. No hay
  lista de cambios. La licencia figura como *"Other (specified in description)"*, pero la
  descripción no especifica ninguna.
- Usa el mismo índice de clases que el oficial. **[inferido]** Si el índice fuera otro,
  cambiaría casi todo píxel de cada máscara. En realidad 19 máscaras son idénticas y la mediana
  de cambio es del 2,5 % de los píxeles (sección 5).

---

## 3. Historia del uso de los datos (tres etapas)

Esto importa para el paper, porque los cuadernos y el README mencionan cifras de etapas
anteriores.

### Etapa 0 — Cuaderno de partida de Kaggle

Archivo `original-hybrid-cnn-vit-attention-u-net.ipynb`, conservado sin cambios.
**[verificado** en su código**]**

- **Train**: las 398 imágenes de Track 1 con sus **máscaras oficiales**, sin corregir.
- **Val y test**: las 81 de `data_finally/val` (máscaras de Kaggle), partidas con
  `train_test_split(test_size=0.3, random_state=42)`, lo que da 56 de val y 25 de test.
- **Fuga de datos**: esas 81 imágenes forman parte de las 398 de entrenamiento. El 100 % de su
  val y su test se había visto en el entrenamiento, aunque con otra máscara.
- Además, sus métricas promediaban la IoU por lote y daban 1.0 a las clases ausentes. El
  resultado que reporta (test IoU 0.662) no es válido como referencia.

### Etapa 1 — "Dataset reducido"

Etiqueta de git `dataset-reducido`, commit `a027121` del 13/10/2026. **[verificado]**

- **Fuente única: el dataset de Kaggle** (`data_finally`), imágenes y máscaras. De Track 1 solo
  se usaban `class_mapping.csv` y la categoría Flooded/Non-Flooded de cada imagen.
- Partición sin fuga:

  | Partición | Origen | Imágenes |
  |---|---|---:|
  | train | `data_finally/train` | 317 |
  | val | mitad de `data_finally/val`, estratificada por Flooded/Non-Flooded, semilla 42 | 40 |
  | test | la otra mitad | 41 |

- En esta etapa se entrenaron los tres modelos. mIoU de test con 10 clases: U-Net 0.714,
  DeepLabV3+ 0.696, YOLO11n-seg 0.678.
- Train, val y test usaban **solo máscaras de Kaggle**. Con un test de 41 imágenes, estas
  cifras **no son comparables** con las de la etapa 2.

### Etapa 2 — Dataset completo (versión actual)

Desde el commit `bf55fb6`, del 13/10/2026. Es la versión que debe describir el paper.
**[verificado]**

- Fuente principal: **FloodNet-Supervised v1.0**, imágenes y máscaras.
- Las **máscaras de Kaggle sustituyen a la oficial** en las 398 imágenes que la tienen. Las
  **imágenes** son siempre las oficiales: las de `data_finally/*/image` no se usan.
- El emparejamiento se hace solo por nombre de archivo (`<id>.png` en Kaggle ↔ `<id>.jpg` y
  `<id>_lab.png` en el oficial). Que las fotos de Kaggle sean idénticas a las oficiales **no se
  ha comprobado píxel a píxel**. Las máscaras de Kaggle encajan visualmente con la foto oficial
  en edificios, carreteras y árboles. **[inferido]**

---

## 4. El dataset final (etapa 2) en detalle

### 4.1 Reglas de construcción

Están en la sección 1 de `floodnet-segmentation.ipynb`, función `construir_cache()` y celda de
exclusión. **[verificado]**

1. Si existe máscara de Kaggle para la imagen, se usa esa. Si no, la oficial.
2. Se excluyen las máscaras **oficiales** con una sola clase en toda la imagen (anotación
   fallida). Una máscara de Kaggle de una sola clase **no** se excluye: solo hay una, la `6595`,
   toda *Grass* (la oficial tenía un 2,25 % de *Tree*).
3. El resto de máscaras oficiales se usa tal cual.
4. Se respeta la partición oficial: ninguna imagen cambia de partición.
5. Imágenes y máscaras se reducen una vez a 512×512, la imagen con `INTER_AREA` y la máscara
   con `INTER_NEAREST`, y se guardan en `data/cache512_full/`. `index.csv` anota la partición,
   el origen de la máscara (`oficial` o `reparada`) y las clases presentes a resolución
   completa. Si una máscara no tiene el tamaño de la imagen, antes se reescala a la imagen con
   `INTER_NEAREST`. Que esto llegara a pasar con las de Kaggle es **[desconocido]**.

### 4.2 Máscaras oficiales de una sola clase

**[verificado]**

| Partición | Oficiales de una sola clase | De ellas, sustituidas por Kaggle | Excluidas |
|---|---:|---:|---:|
| train | 84 | 26 | 58 (56 *Grass*, 2 *Water*) |
| val | 16 | 0 | 16 (*Grass*) |
| test | 22 | 0 | 22 (20 *Grass*, 2 *Water*) |
| **total** | **122** | **26** | **96** |

Las 26 sustituidas son `10165` y `10166` (todo *Water*) y 24 todo *Grass*: 7909, 7918, 7920,
7925, 7931, 7967, 7973, 8015, 8033, 8060, 8061, 8106, 8119, 8130, 8141, 8407, 8408, 8412, 8415,
8422, 8424, 8658, 8794 y 8800. Sus versiones de Kaggle tienen todas más de una clase.

### 4.3 Composición final

**[verificado]** Los tres cuadernos lo comprueban con `assert`.

| Partición | Oficial | Excluidas | Usadas | Máscara de Kaggle | Máscara oficial |
|---|---:|---:|---:|---:|---:|
| train | 1.445 | 58 | **1.387** | 398 | 989 |
| val | 450 | 16 | **434** | 0 | 434 |
| test | 448 | 22 | **426** | 0 | 426 |
| total | 2.343 | 96 | **2.247** | 398 | 1.849 |

Consecuencias para el paper:

- El **28,7 %** de train (398 de 1.387) lleva máscara de Kaggle. Val y test no llevan ninguna.
- **Val y test tienen ruido de anotación.** Solo se ha podido quitar el error de una sola clase.
  El otro tipo de error, regiones con la clase equivocada, no se detecta sin una referencia.
  Su magnitud se estima en la sección 5.

---

## 5. Comparación entre máscaras oficiales y de Kaggle

### 5.1 Cómo se identifican las "corregidas"

**[verificado]** El autor no marca qué máscaras modificó. El proyecto llama "reparada" a toda
imagen cuyo nombre aparece en `data_finally/{train,val}/mask`, haya cambiado o no.
"Reparada" significa **"tiene versión de Kaggle"**, no "fue modificada". Qué cambió de verdad
solo se sabe comparando cada máscara de Kaggle con su oficial.

### 5.2 Dos mediciones

1. **Auditoría del cuaderno principal** (sección 1.3, `AUDITAR = True`). Se hizo cuando
   `data_finally` estaba en disco, a resolución completa submuestreada 1 de cada 4 filas y
   columnas: **138** de las 398 difieren en más de un 5 % de los píxeles y **88** en más de un
   10 %. Los cambios dominantes son *Water → Grass* y *Tree → Grass*. **[verificado** en el
   texto del cuaderno; la celda está guardada con `AUDITAR = False`**]**
2. **Revisión del 06/11/2026** (carpeta `revision_mascaras/`). `data_finally` ya no está en
   disco, pero `data/cache512_full/mask/` conserva sus máscaras a 512 px. Se comparó cada una
   con la oficial reducida a 512 px con `INTER_NEAREST`. **[verificado]**

   | Píxeles distintos | Máscaras (de 398) |
   |---|---:|
   | 0 (idénticas) | 19 |
   | > 1 % | 278 |
   | > 5 % | 139 |
   | > 10 % | 88 |
   | > 20 % | 52 |
   | > 50 % | 9 |

   Concuerda con la auditoría del cuaderno. La diferencia de una máscara en el umbral del 5 %
   se debe a la resolución.

### 5.3 Revisión visual

Se revisaron a ojo 16 casos, a 256 px por panel. A esa resolución solo se juzgan regiones
grandes, no bordes ni clases pequeñas. **[verificado** por inspección, con un juicio
necesariamente subjetivo**]**

- **Mejoras claras.** `7774` (prado entero marcado como agua), `7931` (oficial toda *Grass*; la
  de Kaggle añade la fila de árboles y el estanque), `9027` y `9022` (matorral marcado como
  *Background*), `7357` y `7364` (el agua cubría los jardines hasta las casas). Muchas otras
  solo afinan bordes de árboles y edificios.
- **Discutibles.** `7882`, `7879` y `7884` pasan a *Grass* grandes zonas de vegetación densa y
  alta que la oficial tenía como *Tree*. `7261` pasa una calle inundada de *Road-flooded* a
  *Water*. `8966` estrecha bastante el cauce de agua.
- **Error aparente.** `6600`: el campo de béisbol de tierra queda como *Grass*. En esa misma
  imagen el agua sí está bien corregida.

Conclusión prudente: la mayoría de los cambios grandes mejoran la máscara, pero la corrección
no es perfecta y contiene decisiones de criterio, sobre todo en la frontera *Tree*/*Grass*. No
se ha revisado de forma sistemática.

### 5.4 Material disponible para figuras y tablas

En `revision_mascaras/`:

- `reparadas_vs_oficiales.csv`: las 398 imágenes, con el % de píxeles distintos y los tres
  cambios de clase principales. Las columnas `clases_oficial` y `clases_reparada` se miden a
  512 px y no son fiables, porque desaparecen clases pequeñas. Las cifras de clases a
  resolución completa son las de `data/cache512_full/index.csv`.
- `lamina_01.png` … `lamina_18.png`: las 139 imágenes con más de un 5 % de cambio, ordenadas de
  mayor a menor. Cada fila muestra foto, máscara oficial, máscara de Kaggle y píxeles
  cambiados en rojo.
- `scripts/comparar.py` y `scripts/laminas.py`, que regeneran todo desde la raíz del proyecto.

### 5.5 Qué falta para una verificación sólida

Volver a descargar el dataset de Kaggle y hacer dos cosas: (a) comparar sus fotos con las
oficiales para confirmar que un mismo nombre es la misma imagen, y (b) repetir la comparación
a resolución completa.

---

## 6. Con qué datos se entrena y evalúa cada modelo (etapa 2)

**[verificado** en los cuadernos y en el README**]**

| | U-Net híbrido CNN+ViT | DeepLabV3+ (ResNet-50) | YOLO11n-seg |
|---|---|---|---|
| Cuaderno | `floodnet-segmentation.ipynb` | `floodnet-deeplabv3plus.ipynb` | `floodnet-yolo11n-seg.ipynb` |
| Datos | `data/cache512_full` | la misma caché | la misma caché, convertida a polígonos en `data/yolo512_full` |
| Partición | 1.387 / 434 / 426 | la misma | la misma |
| Resolución | 512×512 | 512×512 | 512×512 |
| Clases entrenadas | 10 | 10 | 9 (sin *Background*) |
| Particularidades | oversampling de clases raras (`target_ratio = 0.5`) con augmentación fuerte en las copias; TTA por volteos en val y test; **sin semilla fija** | semilla 42; píxeles de relleno de la augmentación con `ignore_index = 255`; sin oversampling ni TTA | semilla 42; cada componente conexa de cada clase es una instancia poligonal; *Background* = píxeles sin instancia |
| Épocas | 30 | 40 | techo de 300, parada temprana en la 268 |

- **Evaluación común:** las 426 imágenes de test, con máscaras oficiales. `SegMetrics` acumula
  la matriz de confusión de todo el test y divide una sola vez. El mapa predicho de YOLO se
  rasteriza a 10 clases (lo no cubierto es *Background*), así que los tres se miden igual.
- **Techo de YOLO por la conversión:** reconstruir las 2.247 máscaras desde sus polígonos da un
  mIoU de 0.977 frente a la máscara original.
- **Antes, YOLO tuvo *Background* como clase** (commit `3c9b346` y anteriores). Con esa
  configuración obtenía un mIoU de 0.705 con 10 clases y de 0.739 sin *Background*. La versión
  actual sin *Background* da 0.661 y 0.730.

Resultados de test de la etapa 2, mIoU:

| | U-Net | DeepLabV3+ | YOLO11n-seg |
|---|---:|---:|---:|
| 10 clases | 0.732 | 0.709 | 0.661 |
| sin *Background* | 0.754 | 0.738 | 0.730 |

El desglose por clase, por imagen y los parámetros están en `floodnet_resultados.xlsx`.

---

## 7. Qué se puede afirmar en el paper y qué no

**Se puede afirmar:**

- Se usa FloodNet-Supervised v1.0 con su partición oficial, se excluyen 96 máscaras oficiales
  de una sola clase y en 398 imágenes de train se usan máscaras alternativas de un dataset
  público de Kaggle (citar URL, autor y versión 3).
- Val y test se evalúan contra máscaras oficiales, que contienen errores de anotación. Se
  puede cuantificar con la comparación de la sección 5, explicando que es una estimación hecha
  sobre train.
- La comparación entre los tres modelos es justa: mismos datos, misma partición, misma
  resolución y misma métrica.

**No se debe afirmar:**

- Que las máscaras de Kaggle estén "corregidas a mano", "por expertos" o "verificadas".
  Hay que describirlas como **"máscaras revisadas publicadas por un tercero, método no
  documentado"**.
- Que las 398 estén todas corregidas: 19 son idénticas a la oficial.
- Que las máscaras de Kaggle sean una referencia limpia: hay al menos un error aparente
  (`6600`) y varias decisiones discutibles.
- Comparaciones directas con las cifras de la etapa 1 (dataset reducido) o con el cuaderno de
  Kaggle de partida. Usan otro test, otras máscaras y, en el segundo caso, fuga de datos y
  métricas defectuosas.

**Erratas en el repositorio:** `README.md` (líneas 117, 166, 171 y 184) y los tres cuadernos
dicen "corregidas a mano". Es la misma suposición sin fuente de arriba y está pendiente de
corregir. Si el paper toma texto del README, no debe heredarla.
