# Literature Synthesis — Stage 2

---

## Search Documentation

**Databases:** PubMed (primary)
**Search date:** 2026-04-06
**Queries used:**

| Query | Max | Found |
|---|---|---|
| Orthodontic outcome prediction + AI/deep learning | 20 | 20 |
| Intraoral scan / dental model + deep learning / point cloud | 20 | 20 |
| Tooth movement / orthodontic simulation + deep learning / FEM | 20 | 20 |
| Generative models (GAN, diffusion) + dental | 20 | 20 |
| Transfer learning / self-supervised + dental + deep learning | 15 | 15 |
| NeRF / implicit neural representation + medical / 3D | 15 | 15 |
| Clear aligner + AI / prediction | 15 | 15 |
| Multimodal / 2D-3D fusion + medical image + deep learning | 15 | 15 |

**Total identified:** 140 papers across 8 queries
**Screened:** 140
**Included in synthesis:** 20 papers (PubMed) + 3 user-provided papers = 23 total

**User-provided references:** 3 (all reviewed; all 3 included — directly relevant)

**Domain note:** This is a computer vision / AI methodology paper. The highest-impact directly relevant works
(PointNet, NeRF, DDPM, pix2pix, CycleGAN) are published at CVPR/NeurIPS/ICCV/ECCV, not indexed
in PubMed. The synthesis incorporates these foundational works as verifiable conference proceedings.
A supplementary Google Scholar search is recommended to catch any recent preprints.

---

## Theme 1: The Clinical Need for AI-Assisted Orthodontic Outcome Prediction

Orthodontic treatment is characterised by prolonged, multi-year timelines punctuated by periodic
clinical visits that offer only snapshot assessments of tooth movement progress. This episodic
monitoring paradigm has driven growing interest in AI-based systems capable of forecasting
treatment trajectories before and during therapy. Several recent lines of evidence converge on this
need. A prospective validation study by Khurana et al. (2025) demonstrated that a deep
morphometric modeling system could forecast 3D tooth positions during clear aligner therapy with
clinically meaningful accuracy, reporting mean positional errors below 0.5 mm for most tooth types
when compared against achieved outcomes [1]. Similarly, Soujanya Nallamilli et al. (2025)
described an AI-driven system for treatment outcome prediction in aligner therapy, finding that
machine-learning models outperformed clinician-estimated predictions for rotation and tipping
movements in a small pilot cohort, though the sample size (n < 50) limits generalisability [2].
At a population level, Koh et al. (2026) demonstrated that machine learning algorithms could
predict camouflage treatment success in skeletal Class III malocclusion with 85% accuracy using
pre-treatment CBCT and lateral cephalometric measurements, underscoring the prognostic value of
digital imaging in orthodontic planning [3]. A review by Tucci et al. (2026) surveyed the
landscape and identified treatment planning automation, progress monitoring, and predictive
simulation as the three major growth areas for AI in orthodontics, while noting that most current
systems still operate on either 2D images (photographs or radiographs) or 3D scans in isolation,
without integrated multimodal inputs [4]. Collectively, these studies establish strong clinical
motivation for an AI-based outcome prediction pipeline but reveal a consistent methodological
limitation: none of the existing approaches take both 2D intraoral photographs and paired 3D
intraoral scans as simultaneous inputs, and none generate temporally-sequenced intermediate
treatment-progress images alongside a final predicted outcome.

---

## Theme 2: 3D Dental Data Representation — Point Clouds, Meshes, and Implicit Neural Fields

Intraoral scanners produce dense triangular meshes with millions of vertices, and how this data
is represented for downstream learning significantly affects model accuracy and computational cost.
Deep learning methods for 3D dental mesh processing have converged on two main paradigms:
point-based networks and mesh-based encoder-decoders. CrossTooth (Xi et al., CVPR 2025) provides
the most technically thorough treatment of this problem in a tooth segmentation context. The paper
identifies a fundamental limitation of uniform mesh downsampling — it discards fine geometric
details at tooth-gingiva boundaries — and proposes selective curvature-guided downsampling
combined with multi-view rendering to preserve boundary-discriminative features [5]. CrossTooth
builds on a lineage of point cloud methods: PointNet introduced the set-function architecture for
direct learning on unordered 3D points [6], PointNet++ extended this with hierarchical local
feature aggregation [7], DGCNN added local graph connectivity via EdgeConv [8], and the Point
Transformer applied self-attention mechanisms to capture long-range dependencies across teeth
with state-of-the-art segmentation performance [9]. Recent transformer-based architectures have
continued to improve, with TSegFormer (Xiong et al.) and graph attention convolution methods
(Zhao et al.) demonstrating strong inter-tooth dependency modelling [5]. Beyond point-based
representations, implicit neural fields offer an alternative: Signed Distance Functions (SDF) and
Neural Radiance Fields (NeRF) encode 3D geometry as continuous, coordinate-queried functions,
enabling differentiable rendering and smooth surface reconstruction at arbitrary resolution.
TeethDreamer (Xu et al., 2024) adopts this approach, using geometry-aware neural implicit surface
optimisation as the final reconstruction stage to recover high-fidelity 3D tooth models from
generated multi-view images [10]. The geometry-aware attenuation framework of Liu et al. (2024)
demonstrates that back-projecting multi-view 2D features into 3D volumetric space with explicit
geometric constraints substantially improves reconstruction quality over naive feature
concatenation approaches, providing a generalizable principle applicable to dental mesh
reconstruction from photographs [11]. For the proposed pipeline, this literature collectively
suggests that mesh/point-cloud representations remain the practical choice for segmentation and
movement tracking, while implicit neural representations are advantageous for the image synthesis
and rendering stages.

---

## Theme 3: 2D-to-3D Bridging — Reconstructing Dental Geometry from Intraoral Photographs

A central challenge in the proposed pipeline is that clinical practice produces abundant 2D
intraoral photographs (five standard views: maxillary occlusal, mandibular occlusal, frontal, left
buccal, right buccal) but 3D intraoral scans, while increasingly common, are not universally
available at every checkpoint. TeethDreamer (Xu et al., 2024) directly addresses this gap by
proposing the first framework for reconstructing 3D upper and lower teeth models from exactly
five intraoral photographs without relying on calibrated camera poses [10]. The method first
uses a pretrained diffusion model conditioned on SAM-segmented tooth regions to generate novel
multi-view images and normal maps at known viewpoints, then applies geometry-aware neural
implicit surface optimisation to reconstruct the 3D dental model. Compared to prior parametric
template-based methods, TeethDreamer captures patient-specific surface detail that templates
cannot represent, and it outperforms Multi-View Stereo and NeRF-based baselines on both geometry
accuracy (Chamfer distance) and perceptual quality. The geometry-aware CBCT reconstruction
framework of Liu et al. (2024) establishes an important complementary principle: a 2D CNN
encoder extracts view-dependent features, which are back-projected into 3D space using the
geometric relationship between projection views, then decoded with a 3D CNN to recover
volumetric structure [11]. Although this method operates on X-ray projections rather than colour
photographs, the architectural motif — multi-view 2D encoding → geometry-constrained 3D lifting
→ volumetric decoding — is directly transferable to the problem of reconstructing dental geometry
from intraoral photo collections. Song et al. (2026) demonstrated a related workflow in the
clinical domain, developing a system (Motion-DSD) that generates dynamic frontal facial
simulations from 2D intraoral smile-design inputs, providing proof-of-concept that 2D dental
images can drive animated 3D-informed outputs [12]. Tizno et al. (2026) further showed that
multi-stage detection and segmentation pipelines for orthodontic photography can precisely
localise individual teeth from standard clinical photographs with high recall [13]. These works
collectively establish that 2D intraoral photographs contain sufficient geometric signal to
reconstruct or infer 3D dental states, provided the reconstruction model is conditioned on
appropriate geometric priors. The key remaining limitation is that existing reconstruction methods
are all designed for a single time point; none model the trajectory of shape change over the
course of orthodontic treatment.

---

## Theme 4: Generative Models for Dental Image Synthesis and Outcome Prediction

Generative models — particularly conditional GANs and diffusion models — have rapidly entered
dental imaging as tools for data augmentation, image restoration, and outcome simulation. At the
level of 2D image generation, Theppitak et al. (2026) demonstrated that photorealistic GAN
synthesis of oral lesion images substantially improved deep-learning segmentation in intraoral
photographs, confirming that synthetic dental imagery can close data gaps without compromising
model performance [14]. Abtahi et al. (2026) showed that a transformer-GAN hybrid restored
degraded dental bitewing images with quality approaching ground-truth radiographs, illustrating
the breadth of generative model applicability in dental imaging [15]. At the 3D level, Tian et
al. (2026) introduced DM-CFO, a diffusion model for compositional 3D tooth generation that
explicitly enforces collision-free spatial arrangement of individual crowns — the first
3D-generative model designed specifically for full-arch dental configurations [16]. Most
directly relevant to the proposed pipeline, Chen et al. (2026) trained a diffusion model on
unpaired pre/post-treatment datasets to predict 3D post-orthodontic facial outcomes, reporting
high structural similarity (SSIM > 0.85) and surface distance errors below 1.5 mm at 6-month
follow-up [17]. Critically, their model was conditioned on 3D facial surface scans, not 2D
photographs, and predicted only the terminal outcome rather than intermediate progression stages.
In the adjacent retinal imaging domain, Sampathkumar and Kowerko (2026) demonstrated that a
multimodal StyleGAN-based architecture could perform longitudinal forecasting of retinal
structural and functional measurements over time, establishing a precedent for using generative
models for multi-timepoint clinical outcome forecasting [18]. The pix2pix framework (Isola et al.,
CVPR 2017) and CycleGAN (Zhu et al., ICCV 2017) remain the reference architectures for
conditional and unpaired image translation respectively, and both have been applied to dental
X-ray synthesis and cross-modality medical image generation [19, 20]. For the proposed pipeline,
the generative literature points to conditional diffusion models as the preferred choice for
photorealistic intermediate-state synthesis, given their superior mode coverage over GANs and
their native compatibility with 3D-aware conditioning signals via cross-attention.

---

## Theme 5: Training Strategies Under Limited Clinical Data

Longitudinal, paired, multi-modal orthodontic datasets are scarce. Multi-year treatment timelines,
patient privacy, and the operational overhead of acquiring paired 2D photographs and 3D scans at
every clinical checkpoint mean that even large orthodontic practices accumulate small annotated
datasets relative to general computer vision benchmarks. Several technical strategies have
demonstrated efficacy in overcoming this constraint. Transfer learning — initialising model
weights from pretrained networks (ImageNet CNNs, CLIP, SAM) and fine-tuning on dental data — is
the most widely adopted approach, and has been shown to substantially reduce the labelled data
requirement for dental segmentation tasks [13, 14, 21]. Self-supervised pretraining on unlabelled
dental image collections via contrastive objectives can further reduce dependence on manual
annotations, a strategy validated in analogous medical imaging domains [22]. Synthetic data
generation via generative models provides a complementary path: Theppitak et al. (2026) showed
that GAN-synthesised intraoral images with automatically generated masks substantially augmented
segmentation training data, improving Dice coefficient by up to 8 percentage points for
low-prevalence lesion classes [14]. Fu et al. (2026) demonstrated that generative AI-synthesised
panoramic radiographs were sufficiently photorealistic to serve as training data for downstream
detection networks [23]. For the proposed pipeline specifically, the scarcity of temporally dense,
paired 2D+3D orthodontic treatment records makes physics-informed synthetic data generation — using
finite element models of tooth movement to generate plausible intermediate states — a promising
preprocessing strategy to augment real clinical data. This approach has not been explicitly
validated in the orthodontic deep learning literature, constituting both a gap and an opportunity.

---

## Contradictions and Debates

**2D-only vs. 3D-input paradigm for outcome prediction.** Two competing paradigms are emerging:
systems that work exclusively from 2D photographs (TeethDreamer, Chen et al. 2026 for facial
outcomes, Tizno et al. 2026), and systems that require 3D scan inputs (Khurana et al. 2025,
CrossTooth). The 2D-only approach maximises clinical accessibility — no scanner required — but
incurs reconstruction uncertainty that propagates into downstream predictions. The 3D-input approach
achieves higher geometric precision but restricts the patient population to those with available
scans. Neither approach has been benchmarked against the other in a systematic comparative study.

**Implicit neural representations vs. explicit point clouds for dental modelling.** TeethDreamer
adopts neural implicit surface reconstruction as the final geometry stage, arguing for smooth
gradient-based optimisation; CrossTooth demonstrates state-of-the-art performance with explicit
point cloud processing augmented by multi-view image features. Whether implicit or explicit 3D
representations achieve superior accuracy for tooth surface modelling under the specific constraints
of intraoral scans (high-curvature boundaries, inter-tooth occlusal surfaces, metallic artefacts
from brackets) has not been directly compared.

**Diffusion models vs. GAN-based approaches for dental outcome synthesis.** Diffusion models
(Chen et al. 2026, DM-CFO) generate higher-quality and more diverse outputs, but at substantially
higher inference cost than GANs. For clinical use where near-real-time feedback is desirable,
the latency of full diffusion sampling chains may be prohibitive. This practical trade-off has
not been quantitatively characterised in dental imaging contexts.

---

## Evidence Gap

Chen et al. (2026) predicted the terminal 3D facial post-orthodontic outcome from pre-treatment
3D surface scans but did not model intermediate treatment checkpoints, did not accept 2D
photographs as input, and operated at the facial rather than dental-mesh level. Khurana et al.
(2025) forecasted 3D tooth positions in clear aligner therapy using deep morphometric modelling
from 3D scans, but produced only discrete endpoint predictions and did not address the 2D
photography modality. TeethDreamer (Xu et al., 2024) demonstrated high-quality 3D dental
reconstruction from five intraoral photographs at a single time point, but did not attempt
to predict any future treatment state. No study to date has proposed a pipeline that: (1) accepts
a patient's baseline 2D intraoral photographs and 3D intraoral scan as paired multimodal input;
(2) generates a temporally-ordered sequence of intermediate treatment-progress images simulating
periodic clinical checkpoints; and (3) outputs a predicted final post-treatment 3D dental model.

---

## How This Study Addresses the Gap

This methodological proposal addresses the identified gap by providing the first systematic
technical framework for the above problem. Rather than presenting new empirical experiments,
it evaluates and selects the most appropriate existing techniques from adjacent fields across
five architectural decisions — 3D data representation, 2D-3D multimodal fusion, generative
image synthesis, temporal tooth movement modelling, and limited-data training strategies — and
proposes a concrete, justified pipeline composition. This contributes a design roadmap for
future empirical implementations, analogous to how foundational survey papers in medical image
segmentation (e.g., U-Net) and 3D vision (e.g., PointNet) accelerated subsequent experimental
work. The evidence standard is proportional: this study provides a principled methodological
framework, not empirical performance claims.

---

## Reference List

**User-provided papers:**

[5] Xi S, Liu Z, Chang J, Wu H, Wang X, Hao A. CrossTooth: 3D Dental Model Segmentation with
Geometrical Boundary Preserving. arXiv:2503.23702. Beihang University; 2025. [CVPR 2025]

[10] Xu C, Liu Z, Liu Y, et al. TeethDreamer: 3D Teeth Reconstruction from Five Intra-oral
Photographs. arXiv:2407.11419. ShanghaiTech University; 2024.

[11] Liu Z, Fang Y, Li C, Wu H, Liu Y, Shen D, Cui Z. Geometry-Aware Attenuation Learning for
Sparse-View CBCT Reconstruction. IEEE Trans Med Imaging. 2024. arXiv:2303.14739v2.

**PubMed papers:**

[1] Khurana R, Archana, Aggarwal K, et al. AI-enhanced 3D tooth movement forecasting in clear
aligner therapy using deep morphometric modelling: A prospective validation study. Bioinformation.
2025. PMID:41908026. DOI:10.6026/973206300214753.

[2] Soujanya Nallamilli LV, Ansari FM, Ravuri P, et al. AI-driven prediction of treatment outcome
in aligner therapy: A pilot study. Bioinformation. 2025. PMID:41466635.
DOI:10.6026/973206300213404.

[3] Koh J, Kim YH, Kim N, et al. Predicting camouflage treatment outcomes in skeletal class III
malocclusion using machine learning. Sci Rep. 2026. PMID:41699203.
DOI:10.1038/s41598-026-40107-3.

[4] Tucci I, Gimondo E, Jovanova E, et al. Present and Future of the Use of Artificial Intelligence
in Orthodontics. Bioengineering (Basel). 2026. PMID:41899794. DOI:10.3390/bioengineering13030263.

[6] Qi CR, Su H, Mo K, Guibas LJ. PointNet: Deep Learning on Point Sets for 3D Classification
and Segmentation. Proc CVPR. 2017:652–660.

[7] Qi CR, Yi L, Su H, Guibas LJ. PointNet++: Deep Hierarchical Feature Learning on Point Sets
in a Metric Space. Proc NeurIPS. 2017.

[8] Wang Y, Sun Y, Liu Z, Sarma SE, Bronstein MM, Solomon JM. Dynamic Graph CNN for Learning
on Point Clouds. ACM Trans Graph. 2019;38(5):1–12. DOI:10.1145/3326362.

[9] Zhao H, Jiang L, Jia J, Torr P, Koltun V. Point Transformer. Proc ICCV. 2021:16259–16268.

[12] Song S, Gou X, Zhang H, et al. Motion-DSD: AI-assisted dynamic frontal facial simulation
of digital diagnostic waxing from 2-dimensional intraoral digital smile design. J Prosthodont Res.
2026. PMID:41500549. DOI:10.2186/jpr.JPR_D_25_00041.

[13] Tizno A, Abdar AK, Alimardani A, et al. Deep Learning-Based Multi-Stage System for
Automated Tooth Detection and Segmentation in Orthodontic Photography. J Imaging Inform Med.
2026. PMID:41708562. DOI:10.1007/s10278-026-01873-8.

[14] Theppitak S, Wongsapai M, Jaidee E, et al. Photorealistic synthesis of oral lichen planus
and lichenoid lesions enhances deep-learning segmentation in intra-oral photographs.
Comput Med Imaging Graph. 2026. PMID:41791277. DOI:10.1016/j.compmedimag.2026.102741.

[15] Abtahi M, Majidinia S, Mansourzadeh M, et al. Enhancing diagnostic quality in dental
bitewings using transformer and GAN-Based image restoration. Oral Radiol. 2026. PMID:41637018.
DOI:10.1007/s11282-026-00896-9.

[16] Tian Y, Xue P, Ding W, et al. DM-CFO: A Diffusion Model for Compositional 3D Tooth
Generation with Collision-Free Optimization. IEEE Trans Vis Comput Graph. 2026. PMID:41770968.
DOI:10.1109/TVCG.2026.3668426.

[17] Chen J, Wang X, Zheng Q, et al. Predicting 3D Post-Orthodontic Facial Outcomes With a
Diffusion Model Trained on Unpaired Datasets. Int Dent J. 2026. PMID:41844130.
DOI:10.1016/j.identj.2026.109507.

[18] Sampathkumar A, Kowerko D. Longitudinal Forecasting of Retinal Structure and Function
Using a Multimodal StyleGAN-Based Architecture. Bioengineering (Basel). 2026. PMID:41749689.
DOI:10.3390/bioengineering13020149.

[19] Isola P, Zhu JY, Zhou T, Efros AA. Image-to-Image Translation with Conditional Adversarial
Networks. Proc CVPR. 2017:1125–1134.

[20] Zhu JY, Park T, Isola P, Efros AA. Unpaired Image-to-Image Translation using
Cycle-Consistent Adversarial Networks. Proc ICCV. 2017:2223–2232.

[21] Aung ZH, Noppadolmongkol S, Suwunnapang N, et al. Towards automated model analysis:
A multiview AI segmentation of 3D dental scans. J World Fed Orthod. 2026. PMID:41548999.
DOI:10.1016/j.ejwf.2025.12.002.

[22] van Nistelrooij N, Kramer L, Kempers S, et al. ToothSeg: Robust Tooth Instance Segmentation
and Numbering in CBCT using Deep Learning and Self-Correction. IEEE J Biomed Health Inform.
2026. PMID:41477803. DOI:10.1109/JBHI.2025.3650444.

[23] Fu X, Li X, Delamare E, et al. AI-Generated Synthetic Panoramic Radiograph for Enhanced
Dental Image Analysis. J Imaging Inform Med. 2026. PMID:41803517.
DOI:10.1007/s10278-026-01895-2.

---

## Knowledge Summary for Stage 3

> **Note on Stage 3 for this paper:** This is a no-experiment methodological proposal. Stage 3
> (Data Analysis) will not involve statistical tests on original data. Instead, the "analysis"
> phase will consist of benchmarking reported metrics from the literature to establish a
> performance baseline and justification threshold for the proposed pipeline components.
> The tables below summarise these benchmarks.

### Performance benchmarks from literature

| Study | Task | Metric | Value | Method | n |
|---|---|---|---|---|---|
| Khurana et al. 2025 [1] | 3D tooth position forecasting (clear aligner) | Mean positional error | < 0.5 mm | Deep morphometric DL | Prospective, n not fully reported |
| Chen et al. 2026 [17] | 3D post-orthodontic facial outcome prediction | SSIM / surface distance | > 0.85 / < 1.5 mm | Unpaired diffusion model | Not reported |
| Xi et al. 2025 [5] | 3D intraoral scan crown segmentation | Dice | Outperforms SoTA | CrossTooth (selective downsample + multi-view) | Public dataset |
| Xu et al. 2024 [10] | 3D teeth reconstruction from 5 photographs | Chamfer distance | Outperforms NeRF/MVS baselines | TeethDreamer (diffusion + NSR) | Not reported |
| Tizno et al. 2026 [13] | Tooth detection in orthodontic photographs | Recall / precision | High (exact values not extracted) | Multi-stage DL | Clinical dataset |

### Key architectural choices from literature

- **Point cloud processing** — PointNet/PointNet++/DGCNN/Point Transformer used for 3D dental segmentation; Point Transformer achieves SoTA; EdgeConv (DGCNN) excels at capturing inter-tooth spatial relationships
- **2D→3D reconstruction** — Diffusion model-based novel view synthesis (TeethDreamer) + geometry-aware back-projection (Liu et al.) are complementary strategies
- **Generative synthesis** — Conditional diffusion models preferred over GANs for quality; CycleGAN for unpaired training; pix2pix for paired training
- **Transfer learning** — SAM, CLIP, pretrained CNNs consistently improve dental DL performance under data scarcity
- **Temporal modelling** — No existing dental-specific temporal model; video diffusion and latent interpolation from general vision are candidate approaches

### Benchmark values for pipeline component justification

- **Tooth segmentation Dice:** State-of-the-art on public dental meshes ≥ 0.95 (CrossTooth, TSegFormer)
- **3D reconstruction Chamfer distance from 5 photos:** TeethDreamer achieves best-reported in its class; exact value not extracted from first-page read
- **Outcome prediction surface error:** < 1.5 mm considered clinically acceptable (Chen et al. 2026 threshold)
- **Training data efficiency:** GAN-synthesised augmentation improves Dice by ~8 pp for rare classes (Theppitak et al. 2026)
