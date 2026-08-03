# INF-002A — Market Data Source Evaluation

Version: 1.0

Status: Proposed

---

## Purpose

This document evaluates a set of candidate market-data providers for EDGE_ENGINE's future official Dataset Registry integration.

Its purpose is not to implement connectors or hard-code a provider into the platform. Instead, it assesses which external sources appear most credible, durable, and architecture-compatible for long-term research ingestion.

The evaluation is intentionally research-oriented and should be read alongside the Dataset Connector Framework and the import-vs-research separation described in the repository's architecture documents.

---

## Executive Summary

Revisiting the ranking with the primary criterion being the ability to build a permanent, versioned, and reproducible Dataset Registry independent from a broker account, the ordering shifts.

Polygon and Twelve Data become stronger candidates because they are more clearly API-first, non-broker-oriented, and better suited to durable archival workflows. OANDA remains highly credible for FX research, but it is slightly less compelling as the primary registry candidate because it is still tied to a broker-style ecosystem and data-access model. Dukascopy remains promising, but it is weakened by the lack of a clearly documented, stable automation path.

Under this revised criterion, the ranking becomes:

1. Polygon
2. Twelve Data
3. OANDA
4. Dukascopy
5. Alpha Vantage
6. Stooq

---

## Evaluation Criteria

The comparison below uses the following criteria:

1. Historical coverage and depth
2. Support for EURUSD and XAUUSD
3. M1 support or intraday suitability
4. Data quality and consistency
5. Access model and licensing clarity
6. Integration complexity for an import connector
7. Long-term compatibility with the EDGE_ENGINE dataset-first architecture

---

## Comparative Assessment

| Provider | Historical coverage | EURUSD / XAUUSD fit | M1 / intraday fit | Data quality / consistency | Access model | Integration complexity | Architecture fit | Overall assessment |
|---|---|---|---|---|---|---|---|---|
| Polygon | Strong technical API offering and good reputation for structured data delivery | Less clearly aligned with FX/commodity focus in the public evidence reviewed here | Good for intraday data in supported markets | Strong in well-supported markets | API-first and modern, with a strong fit for durable, versioned ingestion | Low | High | Best fit for a permanent, versioned Dataset Registry when broker independence is the primary criterion |
| Twelve Data | Broad coverage across FX, crypto, stocks, and commodities | Good general fit for FX and commodity-style data | Good for intraday and M1-style workflows | Generally solid for a commercial API service | API-centric and reasonably documented, making it well suited to reproducible ingestion | Low to moderate | High | Strong generalist candidate for a durable registry, especially when broker independence matters |
| OANDA | Strong for FX and related instruments; historically a well-known FX data source | Strong for EURUSD; plausible for metals-related instruments such as XAUUSD depending on product scope | Strong; historical-rate style access is well aligned with intraday research | High for FX; generally regarded as a serious institutional-grade source | Official API and documented historical access, but still embedded in a broker-style offering | Moderate | Medium to high | Very strong for FX research, but slightly less compelling than API-first providers for a broker-independent registry |
| Dukascopy | Strong market breadth, including FX, commodities, and indices | Strong for FX and commodity-style research; good fit for EURUSD/XAUUSD-style use cases | Strong potential; historical export and broker-style data are relevant to M1 research | Potentially strong, but public validation is incomplete | Public historical-data pages exist, but the machine-readable contract is not clearly documented in the public evidence reviewed here | Moderate to high | Medium | Promising, but less suitable as a primary registry source until the access contract is validated |
| Alpha Vantage | Strong developer accessibility and broad API examples, but not a classic research-grade market-data provider | Reasonable for FX and commodity-style endpoints, but less compelling than specialist providers for disciplined historical ingestion | Good for intraday-style requests, but often limited by API constraints and data-model complexity | Service-oriented and easy to consume, but less robust for long-horizon research reproducibility | API-key dependent and clearly oriented toward developer convenience rather than institutional-grade delivery | Low | Medium | Useful for experimentation and prototyping, not the best official source |
| Stooq | Broad historical availability, but often associated with free and browser-oriented data access | Reasonable for general market research, but less compelling as a canonical source for disciplined import workflows | Weak for a robust M1-first research path | Useful but not ideal for strict research-grade normalization | Public web-facing access rather than a clearly structured import contract | Moderate to high | Low to medium | Better as a supplementary or fallback source than as the official registry source |

---

## Ranking

### 1. Polygon

Why it ranks first under the revised criterion:

- It is strongly aligned with the idea of a durable, versioned, and reproducible registry because it is API-first and less dependent on broker-specific workflows.
- It is better suited to long-term archival and normalization than providers that are more web-oriented or broker-embedded.
- It is a stronger fit for the project's registry-centric design than for a quick integration path.

### 2. Twelve Data

Why it ranks second:

- It offers a clean API-driven ingestion model that suits a permanent registry workflow.
- It is a strong generalist provider and is especially attractive when the priority is reproducibility over ease of access.
- Its main limitation is that it is not as clearly specialized for the specific FX/commodity profile as the most FX-focused providers.

### 3. OANDA

Why it ranks third:

- It remains very strong for FX and is highly relevant to the EURUSD/XAUUSD research scope.
- It still offers a credible path for historical ingestion and data normalization.
- Its drawback, under the revised criterion, is that it is more tightly associated with a broker-style ecosystem and is therefore slightly less ideal for a broker-independent registry.

### 4. Dukascopy

Why it ranks fourth:

- It has strong market-data credibility and broad instrument coverage.
- Its architecture fit remains good, but the public evidence reviewed here does not yet prove an implementation-ready and stable access contract.
- This makes it more suitable as a future candidate than as the primary source for a permanent registry.

### 5. Alpha Vantage

Why it ranks fifth:

- It is useful for experimentation and prototyping.
- Its access model is developer-friendly, but it is less aligned with a canonical research dataset workflow than the higher-ranked providers.
- It is therefore better treated as an experimental or supplementary source.

### 6. Stooq

Why it ranks sixth:

- It can be useful for historical research, but it is less suited to disciplined connector design and versioned registry ingestion.
- Its public access model is less clearly aligned with an official, reproducible import workflow.

---

## Final Recommendation

Under the revised criterion, the best current choice for EDGE_ENGINE's official Dataset Registry candidate is Polygon.

### Why Polygon is the recommended source under the revised criterion

1. It is the strongest fit for a permanent, versioned, and reproducible dataset archive because it is API-first and not primarily broker-centric.
2. It is better aligned with the project's need for durable registry ingestion than providers that are more web-oriented or more tightly embedded in a broker-style environment.
3. It fits the Dataset Connector Framework more naturally when the priority is long-term research reproducibility rather than short-term integration simplicity.

### Second-choice candidate

Twelve Data should be treated as the second-choice candidate.

It remains highly attractive because of its clean API-driven model and strong general-market suitability. It is especially strong if the project values a practical path to versioned ingestion without the operational complexity of broker-linked access.

### Recommendation boundary

This recommendation is intentionally scoped to the current research objective and does not imply that the platform should hard-code a provider into production code. The recommendation is instead about which source should be treated as the most credible official registry candidate for future import design.

---

## Suggested Next Step

The next step should be a formal evidence-gathering phase focused on two questions:

1. Can the selected provider deliver a verifiable historical sample for EURUSD and XAUUSD in a format that can be normalized into EDGE_ENGINE's canonical dataset shape?
2. Does the provider's access model and licensing posture support long-term, reproducible registration in the Dataset Registry?

Only after those questions are answered should the project move from evaluation to connector design.
