# Rapport CML

## Métriques globales
- Training accuracy: **0.987**
- Test accuracy: **0.933**

## Métriques par classe
| Classe | Précision | Rappel | F1-score | Effectif |
| --- | --- | --- | --- | --- |
| 0 | 1.00 | 1.00 | 1.00 | 50 |
| 1 | 0.98 | 0.98 | 0.98 | 50 |
| 2 | 0.98 | 0.98 | 0.98 | 50 |
| macro avg | 0.99 | 0.99 | 0.99 | 150 |
| weighted avg | 0.99 | 0.99 | 0.99 | 150 |

## Configuration d'entraînement
- n_estimators: `100`
- max_depth: `5`
- test_size: `0.2`
- random_state: `42`
