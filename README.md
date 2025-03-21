# rama-docs
Comprehensive documentation and AI assistant for Red Planet Labs' Rama platform
# Rama Documentation Project

A comprehensive project to scrape, organize, and make the Red Planet Labs' Rama documentation accessible and intelligent.

## Project Overview

This project aims to:

1. Create a complete, searchable static site of Red Planet Labs' Rama documentation
2. Build an intelligent AI agent that can answer questions about Rama
3. Implement a knowledge graph to capture relationships between Rama concepts
4. Add self-learning capabilities to improve understanding over time

## Repository Structure

- `raw_html/` - Scraped HTML files from the Rama documentation
- `processed_docs/` - Processed Markdown files extracted from the HTML
- `images/` - Images and screenshots from the documentation
- `scripts/` - Scraping and processing scripts
- `site/` - MkDocs documentation site (generated)
- `agent/` - AI assistant code for Rama knowledge
- `knowledge_graph/` - Neo4j knowledge graph implementation

## Phase 1: Documentation Scraping (Completed)

We've successfully scraped the Rama documentation from https://redplanetlabs.com/docs/ using a hybrid approach:

- **Puppeteer**: Used to render JavaScript and capture fully-rendered pages
- **BeautifulSoup**: Used to extract and process content into Markdown

## Phase 2: Creating a Searchable Site (In Progress)

The next step is to organize the documentation into a searchable static site using MkDocs with the Material theme.

## Phase 3: Building an AI Agent (Planned)

We plan to build an AI agent that can answer questions about the Rama platform using:
- Vector embeddings for semantic search
- A knowledge graph for understanding relationships
- Self-learning capabilities for continuous improvement

## Setup Instructions

### Prerequisites

- Node.js 16+ (for Puppeteer)
- Python 3.8+ (for BeautifulSoup and MkDocs)
- Neo4j (for the knowledge graph)

### Installation

1. Clone this repository
```bash
git clone https://github.com/wildcherry500/rama-docs.git
cd rama-docs