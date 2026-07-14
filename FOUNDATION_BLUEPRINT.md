# FOUNDATION_BLUEPRINT.md

Version: 1.0 (Draft)
Status: Working Blueprint
Purpose: Temporary architectural blueprint for the Foundation v2 revision.

---

# 1. Identity

EDGE_ENGINE è un sistema per costruire, validare ed evolvere conoscenza quantitativa sul comportamento dei mercati attraverso un processo di ricerca scientifica riproducibile.

---

# 2. Purpose

EDGE_ENGINE esiste per trasformare la ricerca quantitativa da un insieme di esperimenti isolati a un processo sistematico di costruzione della conoscenza.

---

# 3. Core Domain

Trasformare osservazioni di mercato in conoscenza quantitativa verificabile attraverso la validazione sistematica di ipotesi.

---

# 4. Core Concepts

* HistoricalDataset
* MarketDescription
* ResearchHypothesis
* Experiment
* Evidence
* Knowledge
* Edge

Questi rappresentano i concetti fondamentali del dominio. La loro implementazione sarà definita nel Domain Model.

---

# 5. Knowledge Flow

```text
HistoricalDataset
        ↓
MarketDescription
        ↓
ResearchHypothesis
        ↓
Experiment
        ↓
Evidence
        ↓
Knowledge
        ↓
Edge
```

Questo rappresenta il flusso concettuale della conoscenza, non il flusso implementativo.

---

# 6. Architectural Principles

1. Domain First
2. Evidence Before Opinion
3. Knowledge is the Primary Asset
4. Reproducibility by Design
5. Evolution over Perfection
6. Simplicity over Cleverness
7. Clean Boundaries

I principi saranno definiti formalmente nel Manifesto.

---

# 7. Success Criteria

EDGE_ENGINE può considerarsi riuscito quando sarà in grado di costruire, validare, conservare ed evolvere conoscenza quantitativa in modo riproducibile, indipendente dalle tecnologie utilizzate e sostenibile nel lungo periodo.

---

# Blueprint Rules

* Il Blueprint è la sorgente di riferimento della Foundation v2.
* Ogni documento della cartella `docs/` deve essere coerente con questo Blueprint.
* Ogni modifica al Blueprint richiede una revisione architetturale.
* Durante una milestone il Blueprint rimane congelato.
* La documentazione deriva dal Blueprint; il codice deriva dalla documentazione.
