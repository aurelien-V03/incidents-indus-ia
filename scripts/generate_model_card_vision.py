"""Génère la model card du modèle DL (détection d'anomalies visuelles) au format HF.

On utilise le template officiel embarqué dans huggingface_hub :
    from huggingface_hub import ModelCard, ModelCardData
    ModelCard.from_template(card_data=..., **fields)

Chaque champ passé en kwargs remplace un placeholder ``{{ field }}`` du
template ; les métriques proviennent de MLflow / emissions.csv (module B7).

    uv run python scripts/generate_model_card_vision.py
"""

from pathlib import Path

from huggingface_hub import ModelCard, ModelCardData

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------- #
# Model card — Deep Learning : détection d'anomalies visuelles (MVTec)
# --------------------------------------------------------------------------- #
dl_card = ModelCard.from_template(
    card_data=ModelCardData(
        language="fr",
        license="mit",
        library_name="pytorch",
        tags=[
            "anomaly-detection",
            "computer-vision",
            "unsupervised",
            "mvtec-ad",
        ],
        model_name="indusense-vision-anomaly",
        metrics=["auroc"],
    ),
    template_path=None,
    # ------- Model Details -------
    model_id="Indusense — Détection d'anomalies visuelles (DL / vision)",
    model_summary=(
        "Détection d'anomalies non supervisée sur images industrielles (catégorie "
        "hazelnut du dataset MVTec AD). Deux approches : auto-encodeur convolutif "
        "(erreur de reconstruction) et PatchCore (memory bank sur features ResNet50). "
        "Modèle retenu : PatchCore."
    ),
    model_description=(
        "Le modèle apprend l'apparence des pièces **saines** puis signale tout écart. "
        "Auto-encodeur convolutif (3 conv / 3 déconv, pertes MSE/SSIM) → score = erreur "
        "de reconstruction ; et PatchCore → distance aux patches sains stockés dans une "
        "memory bank (backbone ResNet50 pré-entraîné). Seuil calé sur la distribution "
        "des scores sains, AUROC et heatmaps de localisation à l'appui. Suivi MLflow, "
        "empreinte CodeCarbon."
    ),
    developers="Équipe formation IA — Openium",
    model_type="Détection d'anomalies non supervisée (vision)",
    language="Images (MVTec AD, catégorie hazelnut)",
    license="mit",
    base_model="Backbone ResNet50 pré-entraîné ImageNet (PatchCore, features gelées)",
    repo="Dépôt interne formation-ia-project",
    model_specs=(
        "Deux architectures évaluées, toutes deux en paradigme **one-class** "
        "(apprentissage sur pièces **saines** uniquement, détection de tout écart).\n\n"
        "#### 1. Auto-encodeur convolutif (baseline)\n\n"
        "L'image est compressée puis reconstruite ; une pièce défectueuse se reconstruit "
        "mal → l'erreur de reconstruction sert de score d'anomalie.\n\n"
        "```mermaid\n"
        "flowchart LR\n"
        "    IN[\"Image 256x256x3\"] --> E1[\"Conv 1<br/>downsample\"]\n"
        "    E1 --> E2[\"Conv 2<br/>downsample\"]\n"
        "    E2 --> E3[\"Conv 3<br/>downsample\"]\n"
        "    E3 --> Z((\"Bottleneck<br/>code latent\"))\n"
        "    Z --> D1[\"DeConv 1<br/>upsample\"]\n"
        "    D1 --> D2[\"DeConv 2<br/>upsample\"]\n"
        "    D2 --> D3[\"DeConv 3<br/>upsample\"]\n"
        "    D3 --> OUT[\"Reconstruction<br/>256x256x3\"]\n"
        "    IN -.comparaison.-> ERR{{\"Erreur MSE / SSIM<br/>= score d'anomalie\"}}\n"
        "    OUT -.comparaison.-> ERR\n"
        "    ERR --> TH[\"Seuil<br/>quantile scores sains\"]\n"
        "    TH --> DEC[\"Saine / Anormale\"]\n"
        "```\n\n"
        "#### 2. PatchCore (modèle retenu)\n\n"
        "Pas d'entraînement par rétro-propagation : on extrait des features de patches "
        "avec un **ResNet50 gelé** (pré-entraîné ImageNet), on stocke un sous-échantillon "
        "(coreset) des patches **sains** dans une *memory bank*, et le score d'une image "
        "de test est la distance au plus proche patch sain — ce qui donne aussi une "
        "**heatmap** de localisation.\n\n"
        "```mermaid\n"
        "flowchart LR\n"
        "    subgraph FIT[\"Apprentissage (images saines)\"]\n"
        "        TR[\"Images saines\"] --> B1[\"ResNet50 gelé<br/>features de patches\"]\n"
        "        B1 --> CS[\"Coreset subsampling\"]\n"
        "        CS --> MB[(\"Memory bank<br/>patches sains\")]\n"
        "    end\n"
        "    subgraph INF[\"Inference (image de test)\"]\n"
        "        TE[\"Image de test\"] --> B2[\"ResNet50 gelé<br/>features de patches\"]\n"
        "        B2 --> NN[\"Distance au plus<br/>proche voisin\"]\n"
        "        MB --> NN\n"
        "        NN --> SC[\"Score d'anomalie<br/>+ heatmap\"]\n"
        "        SC --> TH2[\"Seuil\"]\n"
        "        TH2 --> DEC2[\"Saine / Anormale\"]\n"
        "    end\n"
        "```\n\n"
        "**Objectif** : maximiser l'AUROC de détection au niveau image. Résultat : "
        "PatchCore (AUROC ≈ 0.986) surpasse nettement l'auto-encodeur."
    ),
    compute_infrastructure="Poste de développement (CPU/GPU), suivi MLflow backend SQLite.",
    cloud_region="N/A (on-premise)",
    # ------- Uses -------
    direct_use=(
        "Contrôle qualité visuel : signaler les pièces potentiellement défectueuses "
        "et localiser la zone suspecte (heatmap) pour revue humaine."
    ),
    downstream_use=(
        "Pré-tri sur ligne de production : router les pièces à score élevé vers une "
        "inspection manuelle, réduire le volume à contrôler à 100 %."
    ),
    out_of_scope_use=(
        "**Pas de rejet automatique** de pièces sans validation. Entraîné sur une "
        "seule catégorie/éclairage : ne pas transposer tel quel à d'autres pièces, "
        "caméras ou conditions d'éclairage sans ré-entraînement."
    ),
    # ------- Bias, Risks, Limitations -------
    bias_risks_limitations=(
        "Modèle non supervisé calé sur des pièces saines : sensible au domaine "
        "(éclairage, cadrage, fond). Le seuil arbitre faux positifs vs faux négatifs ; "
        "un défaut jamais vu à l'entraînement peut passer si son apparence reste proche "
        "du sain. Jeu de test petit (dataset MVTec)."
    ),
    bias_recommendations=(
        "Fixer le seuil avec le métier selon le coût d'un défaut manqué. Contrôler la "
        "stabilité de l'éclairage/cadrage en production. Revalider si les conditions "
        "d'acquisition changent. Conserver une inspection humaine sur les cas limites."
    ),
    # ------- Training -------
    training_data=(
        "MVTec AD — catégorie hazelnut. Entraînement sur images **saines** uniquement "
        "(paradigme one-class). Normalisation + augmentation Albumentations."
    ),
    preprocessing="Redimensionnement (256 px), normalisation, augmentations "
    "(auto-encodeur). PatchCore : features ResNet50 gelées, sous-échantillonnage de la "
    "memory bank.",
    training_regime="fp32",
    speeds_sizes_times="Entraînement auto-encodeur sur CPU/GPU de poste ; PatchCore sans "
    "back-prop (extraction de features + coreset). Empreinte suivie via CodeCarbon.",
    # ------- Evaluation -------
    testing_data="Split de test MVTec hazelnut (pièces saines + défectueuses).",
    testing_factors="Détection au niveau image (score d'anomalie).",
    testing_metrics=(
        "AUROC (niveau image) — insensible au choix du seuil. Seuil final = quantile de "
        "la distribution des scores sains, reporté avec la matrice de confusion."
    ),
    results=(
        "AUROC (test) : **PatchCore ≈ 0.986** · auto-encodeur convolutif tuné (Optuna) "
        "≈ 0.927 en validation, ≈ 0.83–0.86 en test. PatchCore nettement supérieur."
    ),
    results_summary=(
        "Recommandation v1 : **PatchCore** (AUROC ≈ 0.986, localisation par heatmap, "
        "pas d'entraînement lourd). L'auto-encodeur reste une baseline pédagogique utile."
    ),
    # ------- Environmental Impact -------
    hardware_type="CPU/GPU de poste de développement",
    hours_used="Faible (PatchCore sans entraînement ; auto-encodeur quelques epochs)",
    cloud_provider="Local / on-premise",
    co2_emitted="Suivi via CodeCarbon (voir emissions.csv / runs MLflow)",
    # ------- More -------
    model_examination="Heatmaps de localisation d'anomalie (patchcore_heatmaps.png), "
    "histogramme des scores et seuil (threshold_hist.png).",
    hardware_requirements="GPU recommandé pour l'extraction de features à l'échelle ; "
    "CPU possible sur petits volumes.",
    software="Python, PyTorch, Albumentations, scikit-learn, MLflow, CodeCarbon.",
    citation_bibtex=(
        "@inproceedings{roth2022patchcore, title={Towards Total Recall in Industrial "
        "Anomaly Detection}, author={Roth et al.}, booktitle={CVPR}, year={2022}}"
    ),
    model_card_authors="Équipe formation IA — Openium",
    model_card_contact="a.vallet@openium.fr",
)

dl_path = ROOT / "MODEL_CARD_vision.md"
dl_card.save(dl_path)
print(f"écrit : {dl_path}")
