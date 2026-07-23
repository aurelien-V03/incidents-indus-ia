"""Génère la model card du modèle ML (maintenance prédictive) au format HF.

On utilise le template officiel embarqué dans huggingface_hub :
    from huggingface_hub import ModelCard, ModelCardData
    ModelCard.from_template(card_data=..., **fields)

Chaque champ passé en kwargs remplace un placeholder ``{{ field }}`` du
template ; les métriques proviennent de MLflow / emissions.csv (module B7).

    uv run python scripts/generate_model_card_maintenance.py
"""

from pathlib import Path

from huggingface_hub import ModelCard, ModelCardData

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------- #
# Model card — Machine Learning : maintenance prédictive (tabulaire)
# --------------------------------------------------------------------------- #
ml_card = ModelCard.from_template(
    card_data=ModelCardData(
        language="fr",
        license="mit",
        library_name="xgboost",
        tags=["tabular-classification", "predictive-maintenance", "industry"],
        model_name="indusense-maintenance",
        metrics=["pr_auc", "recall"],
    ),
    template_path=None,  # template officiel HF embarqué
    # ------- Model Details -------
    model_id="Indusense — Maintenance prédictive (ML tabulaire)",
    model_summary=(
        "Classifieur tabulaire qui estime la probabilité de panne d'une machine "
        "dans les prochaines 24 h à partir de features de télémétrie (capteurs, "
        "compteurs d'usage, historique d'incidents). Baselines régression "
        "logistique / Random Forest, modèle retenu XGBoost."
    ),
    model_description=(
        "Modèle de classification binaire (panne / pas de panne à l'horizon 24 h). "
        "Trois familles évaluées : régression logistique (baseline), Random Forest "
        "et XGBoost. Sélection sur PR-AUC en validation temporelle (TimeSeriesSplit, "
        "sans fuite), hyperparamètres tunés avec Optuna (sampler TPE, budget borné, "
        "pruning). Suivi complet MLflow, empreinte carbone mesurée avec CodeCarbon."
    ),
    developers="Équipe formation IA — Openium",
    model_type="Classification binaire tabulaire (gradient boosting)",
    language="Français (documentation) — données numériques de télémétrie",
    license="mit",
    base_model="N/A (entraîné from scratch)",
    repo="Dépôt interne formation-ia-project",
    model_specs=(
        "Gradient boosting d'arbres (XGBoost) pour classification binaire. Objectif : "
        "maximiser la PR-AUC sur la classe minoritaire (panne) sous validation "
        "temporelle. Baselines comparées : régression logistique, Random Forest."
    ),
    compute_infrastructure="Poste de développement (CPU), suivi MLflow backend SQLite.",
    cloud_region="N/A (on-premise)",
    # ------- Uses -------
    direct_use=(
        "Aide à la décision pour la planification de maintenance : hiérarchiser "
        "les machines à inspecter en priorité. La sortie est une **probabilité**, "
        "à lire comme un signal d'alerte, pas comme un verdict."
    ),
    downstream_use=(
        "Intégration dans un tableau de bord de supervision ou déclenchement d'une "
        "règle métier (ex. créer un ticket d'inspection au-delà d'un seuil de "
        "probabilité choisi avec les équipes terrain)."
    ),
    out_of_scope_use=(
        "**Aucune décision automatique** d'arrêt machine ou de sécurité sans "
        "validation humaine. Le signal des features est faible (PR-AUC ≈ 0.6) : "
        "ne pas utiliser comme unique source de vérité ni pour des garanties "
        "contractuelles."
    ),
    # ------- Bias, Risks, Limitations -------
    bias_risks_limitations=(
        "Signal prédictif faible sur ce jeu : les features disponibles sont peu "
        "déterminantes. Classes déséquilibrées (pannes rares) → risque de faux "
        "négatifs. Le modèle apprend des corrélations historiques, pas des causes ; "
        "un changement de parc machine ou de régime d'usage dégrade les "
        "performances (drift)."
    ),
    bias_recommendations=(
        "Garder l'humain dans la boucle. Surveiller le drift et ré-entraîner "
        "périodiquement. Choisir le seuil de décision avec le métier selon le coût "
        "relatif faux positif / faux négatif. Utiliser SHAP pour vérifier que les "
        "features qui pèsent sont cohérentes métier."
    ),
    # ------- Training -------
    training_data=(
        "**Dataset Gold interne** : `artifacts/ingestions/gold/gold_splited_dataset.csv` "
        "(≈ 134 280 lignes, une par fenêtre machine × heure). "
        "Construit par un pipeline **Bronze → Silver → Gold** à partir de deux sources "
        "Silver : `silver_telemetry.csv` (relevés capteurs : température, pression, "
        "tension, rotation, pièces produites) et `silver_incidents.csv` (historique "
        "d'incidents typés et sévérité). "
        "Features dérivées par fenêtres glissantes 1 h / 6 h / 12 h / 24 h (moyennes, "
        "max, écarts-types, tendances, z-scores, deltas) plus compteurs d'incidents et "
        "de maintenance passés. Cible = `label_failure_next_24h`. La colonne `split_set` "
        "porte le découpage train/val/test **temporel** (pas de mélange futur/passé)."
    ),
    preprocessing="Agrégation temporelle, standardisation des baselines linéaires, "
    "gestion du déséquilibre via scale_pos_weight (XGBoost).",
    training_regime="fp32",
    speeds_sizes_times=(
        "Recherche Optuna XGBoost ≈ 107 s / 0.00182 kWh / 0.102 gCO₂eq "
        "(voir emissions.csv, mesure CodeCarbon)."
    ),
    # ------- Evaluation -------
    testing_data="Partition `split_set == 'test'` du dataset Gold "
    "(`gold_splited_dataset.csv`), fenêtre temporelle tenue à l'écart (out-of-time).",
    testing_factors="Horizon 24 h, classe minoritaire = panne.",
    testing_metrics=(
        "PR-AUC (métrique de référence, robuste au déséquilibre) et recall. "
        "Résultats test : XGBoost PR-AUC ≈ 0.56 · Random Forest ≈ 0.60 · "
        "Régression logistique ≈ 0.49."
    ),
    results=(
        "Meilleure PR-AUC : Random Forest ≈ 0.60, XGBoost ≈ 0.56, baseline logistique "
        "≈ 0.49. Écarts faibles : le gain du tuning reste marginal, cohérent avec un "
        "signal de features peu déterminant."
    ),
    results_summary=(
        "Sur ce jeu, aucun modèle n'atteint une performance forte. Recommandation v1 : "
        "XGBoost (bon compromis interprétabilité SHAP / coût / performance), en aide à "
        "la décision uniquement, seuil à caler avec le métier."
    ),
    # ------- Environmental Impact (CodeCarbon) -------
    hardware_type="CPU (poste de développement)",
    hours_used="≈ 0.03 h (search Optuna 40 essais)",
    cloud_provider="Local / on-premise",
    co2_emitted="≈ 0.10 gCO₂eq pour la recherche XGBoost (CodeCarbon, emissions.csv)",
    # ------- More -------
    model_examination="Explicabilité SHAP (TreeExplainer) : summary plot global + "
    "waterfall local. Permet de vérifier la cohérence métier des features qui pèsent.",
    more_information=(
        "### Pipeline de données (architecture médaillon Bronze → Silver → Gold)\n\n"
        "Les données sont d'abord **ingérées depuis des fichiers CSV** puis chargées "
        "dans une base **PostgreSQL** (via SQLAlchemy, schéma versionné par Alembic), où "
        "elles transitent par trois couches successives. Des **exports CSV** sont "
        "produits dans `artifacts/ingestions/` pour l'entraînement et la traçabilité.\n\n"
        "| Couche | Contenu | Emplacement (PostgreSQL / export CSV) | Rôle |\n"
        "|---|---|---|---|\n"
        "| **Bronze** | Données brutes ingérées telles quelles (relevés capteurs, "
        "incidents anonymisés horodatés) | tables `bronze.*` — export "
        "`artifacts/ingestions/incidents/…` | Capturer la donnée source sans "
        "transformation (traçabilité, rejouabilité) |\n"
        "| **Silver** | Données nettoyées, typées et standardisées | tables `silver.*` — "
        "export `silver_telemetry.csv`, `silver_incidents.csv` | Uniformiser schémas, "
        "corriger les types, dédupliquer, anonymiser |\n"
        "| **Gold** | Table analytique prête à l'entraînement | table `gold.*` — export "
        "`gold_splited_dataset.csv` | Feature engineering (fenêtres glissantes), "
        "libellés de panne, split temporel |\n\n"
        "```mermaid\n"
        "flowchart LR\n"
        "    CSV[\"📄 Fichiers CSV<br/>sources brutes\"] -->|ingestion<br/>read_csv| DB\n"
        "    subgraph DB[\"🐘 Base PostgreSQL (schéma versionné Alembic)\"]\n"
        "        direction LR\n"
        "        subgraph BRONZE[\"🥉 Bronze — brut\"]\n"
        "            B[\"tables bronze.*<br/>capteurs + incidents\"]\n"
        "        end\n"
        "        subgraph SILVER[\"🥈 Silver — nettoyé\"]\n"
        "            S[\"tables silver.*<br/>typé, dédupliqué\"]\n"
        "        end\n"
        "        subgraph GOLD[\"🥇 Gold — analytique\"]\n"
        "            G[\"table gold.*<br/>features + labels\"]\n"
        "        end\n"
        "        B -->|nettoyage,<br/>anonymisation| S\n"
        "        S -->|jointure + features<br/>glissantes 1/6/12/24h| G\n"
        "    end\n"
        "    G -->|export| GCSV[\"📄 gold_splited_dataset.csv<br/>~134k lignes\"]\n"
        "    GCSV --> MODEL[\"🤖 Modèle<br/>XGBoost (horizon 24h)\"]\n"
        "```\n\n"
        "**CSV → PostgreSQL (Bronze)** : ingestion des fichiers sources bruts "
        "(`read_csv` → `to_sql`) dans les tables Bronze, sans transformation.\n\n"
        "**Bronze → Silver** : parsing, typage, nettoyage et anonymisation des relevés "
        "de télémétrie et des incidents.\n\n"
        "**Silver → Gold** : jointure télémétrie × incidents par machine et fenêtre "
        "temporelle, dérivation des features (moyennes / max / std / tendances / "
        "z-scores / deltas sur 1 h, 6 h, 12 h, 24 h), compteurs d'incidents et de "
        "maintenance passés, création des cibles `label_failure_next_{6,12,24,48}h` et "
        "de la colonne `split_set` (découpage train/val/test **temporel**, sans fuite "
        "futur→passé).\n\n"
        "Chaque couche est reconstructible à partir de la précédente (notebooks "
        "`sql-dataset-{bronze,silver,gold}.ipynb`), garantissant la reproductibilité de "
        "bout en bout jusqu'au modèle."
    ),
    hardware_requirements="CPU standard suffisant (inférence légère).",
    software="Python, XGBoost, scikit-learn, Optuna, MLflow, CodeCarbon, SHAP.",
    citation_bibtex="N/A (modèle interne de formation).",
    model_card_authors="Équipe formation IA — Openium",
    model_card_contact="a.vallet@openium.fr",
)

ml_path = ROOT / "MODEL_CARD_maintenance.md"
ml_card.save(ml_path)
print(f"écrit : {ml_path}")
