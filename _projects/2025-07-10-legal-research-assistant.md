---
layout: project
title:  Legal Research Assistant
date:   2025-07-10
image:  images/project14/cover.png
tags:   Legal Research Assistant RAG AI Summarization Australia
---
*On the cover: Legal Research Assistant Platform*

This project was delivered for MiAI.law, an Australian legal technology firm, to build a modern AI-driven system for rapid, accurate legal research across case law and legislation. The platform supports multiple legal workflows—lite research, deep research, contract review, contract audit, case summarization, and legislation research—using an advanced RAG pipeline optimized for legal reasoning.

## Background:
Legal professionals and everyday users often struggle to navigate large volumes of case law from the High Court, Federal Courts, and State/Territory jurisdictions. Identifying the correct cause of action, finding authoritative principles, and interpreting legislative sections is slow and requires deep expertise. MiAI.law needed an AI system that could:

* Understand user scenarios
* Identify key legal issues
* Retrieve the most relevant cases and statutory sections
* Summarize complex legal documents
* Provide accurate, grounded explanations without overwhelming the user

## Methodology

#### 1. Data Acquisition

* Built custom crawlers using Scrapy/BeautifulSoup to ingest case law and statutory material from Australian legal sources.
* Extracted rich metadata (jurisdiction, court hierarchy, dates, judges, catchwords, legislation structure) and stored it in PostgreSQL.

#### 2. Summary-First Preprocessing

Rather than chunking full judgments, I developed a pipeline that extracts and summarizes:

* Ratio decidendi
* Obiter dicta
* Key judicial reasoning
* Case facts and holdings

Each case is reduced to a dense, coherent summary which forms the basis of semantic search. This dramatically improves retrieval precision and keeps the vector index compact.

#### 3. Hybrid Retrieval System

A dual retrieval architecture was implemented:

* BM25 lexical search (Milvus) for precise keyword/citation queries
* Vector search (Milvus) using embeddings from the latest Sentence Transformer models
* Reranker (cross-encoder) to re-rank the combined results for maximum relevance

This hybrid pipeline provides both coverage and precision, ideal for legal research tasks.

#### 4. Retrieval-Augmented Generation (RAG)

A custom RAG pipeline combines:

* Hybrid retrieval
* Cross-encoder reranking
* Latest open-source LLMs (Llama, Mistral, Falcon variants) fine-tuned on legal material

The system produces:

* Top causes of action
* Summaries of authoritative cases
* Contract clause analysis
* Legislative section interpretation
* Clear explanations grounded in retrieved documents

All responses include citation-backed evidence from the retrieved summaries or statutory sections. A dedicated pipeline crawls federal and state legislation, extracts section-level structure, and embeds summaries for retrieval. This allows the system to identify relevant statutory sections for any factual scenario.

#### 5. User Interface

The final system includes a React + FastAPI interface offering:

* Chat-style interaction
* Jurisdiction selection
* Feature selection (deep research, contract audit, etc.)
* Expand/refine search controls


## Results & Impact

* High-precision retrieval using **BM25 + vector search + reranking**
* 90%+ accuracy in identifying the correct cause-of-action cases
* Sub-second semantic retrieval
* Summary-only embeddings reduced index size by ~80%
* Significant time reduction for legal research, contract review, and legislative interpretation
* Enabled MiAI.law to deploy multiple AI-powered legal services from one unified RAG backbone


## Conclusion

The system successfully delivers fast, authoritative, and user-friendly legal intelligence across case law and legislation. By combining advanced crawling, summary-based embeddings, hybrid retrieval, reranking, and the latest LLMs, the platform provides a scalable backbone for automated legal research and document analysis.

**Further technical details remain confidential due to NDA constraints.**