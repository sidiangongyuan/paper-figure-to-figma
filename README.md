# Paper Figure to Figma

An early-stage workflow project for reconstructing AI-generated research figures as editable vector artwork in Figma, with exports suitable for research papers.

**Status:** requirements discovery. This repository currently contains planning documents; it has no runnable reconstruction tool or validated fidelity results yet.

## Goal

Start from an AI-generated reference image, preserve its intended appearance as closely as practical, and produce a figure that can be edited in Figma and prepared for a paper. Visual fidelity, vector representation, useful editability, and scientific correctness will be evaluated separately.

The agreed input is the generated image together with its original generation prompt. The image guides visual reconstruction; the prompt helps interpretation. Conflicts are reported for review before corrections.

## Project documents

- [Decision log](docs/decisions.md): confirmed requirements, open decisions, and the current interview step.
- [Reference project notes](docs/reference-project.md): relevant mechanisms and limits of Image To Slice.
- [Workflow proposal](docs/workflow-proposal.md): a draft kit for web-based visual-model conversations, Figma reconstruction, and review.

## Getting started

Read the decision log and supply representative figures for scope selection. Installation and execution instructions will be added when a minimal implementation exists. No API credentials, models, datasets, or external accounts are required to read these documents.

The intended workflow must work with existing web-chat visual-model subscriptions and must not require a VLM API key. The first version uses manual uploads, downloads, or copy-paste between web chat and reconstruction tools; the tools handle reconstruction and validation.

Reference inputs and generated outputs are kept in local-only directories by default. This repository does not contain the original chat transcript or reference images.

## Acknowledgements

[50kg/image-to-slice](https://github.com/50kg/image-to-slice) is a workflow reference. No upstream source code has been copied into this repository. Any future reuse must preserve applicable license notices.

## License and citation

A distribution license and citation metadata have not been selected.
