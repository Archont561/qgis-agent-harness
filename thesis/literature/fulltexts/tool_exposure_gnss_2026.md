---
id: literature/fulltexts/tool_exposure_gnss_2026
type: fulltext
status: frozen
language: en
key: tool_exposure_gnss_2026
title: >-
  Less Context, Better Plans: Evaluating Tool Exposure Strategies in an MCP Server for GNSS Data Acquisition
resource: https://doi.org/10.5281/zenodo.22833797
description: >-
  Artificial Intelligence in Geospatial Data Processing and Analysis -> Knowledge representation and geospatial data handling with Multimodal Language Models and Agentic Systems
pages: 5
words: 1940
year: 2026
venue: >-
  XIV Colóquio Brasileiro de Ciências Geodésicas
authors: >-
  de Souza Faria Júnior, Clodoaldo; Subtil Norberto, Isabella; Maximo, Marcos; Silva, Matheus; de Oliveira Moraes, Alison
doi: 10.5281/zenodo.22833797
oa_status: green
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# Less Context, Better Plans: Evaluating Tool Exposure Strategies in an MCP Server for GNSS Data Acquisition

## Page 1

Less Context, Better Plans: Evaluating Tool Exposure Strategies in an MCP Server for
GNSS Data Acquisition
Clodoaldo S. Faria Junior1, Isabela S. Norberto 2, Marcos R. O. A. Maximo1, Matheus M. Silva2,
Alison O. Moraes1

1

2

Instituto Tecnológico de Aeronáutica (ITA), São José dos Campos, Brazil,
{clodoaldo.junior.101406@ga., mmaximo@, aom@}ita.br

FCT UNESP, Presidente Prudente, Brazil, {isabella.subtil, matheus.modesto}@unesp.br

Abstract
Positioning, ionosphere, and time-series studies in geodesy depend on Global Navigation
Satellite System (GNSS) observations and navigation in a standard format [3]. However,
acquisition of these data remains fragmented across heterogeneous repositories. In Brazil, the
RBMC (Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS)/IBGE provides RINEX
(Receiver Independent Exchange Format) files via a web API (Application Programming
Interface); for global products and RINEX 3, CDDIS (Crustal Dynamics Data Information
System)/NASA requires Earthdata, Hatanaka compression, and year or day-of-year (DOY)
directory trees. Broadcast ephemeris (BRDC) files, IGS (International GNSS Service) mirrors, and
local-versus-remote availability checks introduce additional repository-specific procedures, forcing
researchers to combine multiple portals, documentation sources, and ad hoc scripts. Consequently,
massive regional/global GNSS processing requires significant efforts in terms of data collection
and metadata generation, even when computational infrastructure is available [9].
Recent studies indicate that a significant paradigm shift has occurred in software development
in recent years. This shift is characterized by the increasing integration of AI-assisted workflows,
automated code generation and tool-augmented development environments. In this context,
contextualized AI assistants have considerably increased developer productivity, code generation
efficiency and software delivery speed [1,4,5]. As Model Context Protocol (MCP)-based
ecosystems have matured to the point where tens of thousands of tools were being monitored in
2025–2026, invocable tools, structured responses, and traceable execution trails emerged as a
common paradigm for exposing capabilities to large language models (LLMs). MCP is a standard
that allows AI agents to invoke specialized routines through natural-language requests [2,7].
However, our survey did not identify agent-ready interfaces for GNSS/RINEX data acquisition
workflows. Access to observation and navigation data still depends on a fragmented combination
of portals, scripts, manual conversions, and repository-specific procedures. Consequently, the way
GPS/GNSS data is accessed has not evolved in tandem with agent-based scientific workflows.
1

## Page 2

XIV Colóquio Brasileiro de Ciências Geodésicas
_________________________________________________________________________________
This work presents the MCP Rinex-Download server, which conforms to the Model Context
Protocol and unifies RBMC and CDDIS. It also performs automatic post-processing and prechecking and provides an auditable JSON provenance envelope, a contract between the intent in
Portuguese and ionosphere-ready files. However, the quality of selection, plan complexity, and
token cost are affected by how MCP tools enter the LLM context [11], a central trade-off for
servers with multiple acquisition and post-processing routines.
The architecture organizes the server, clients, FastMCP tools, an access library, and
RBMC/CDDIS repositories into reproducible layers (see Figure 1). RBMC remains the national
reference source, and CDDIS provides global RINEX coverage. Following each transfer, postprocessing standardizes decompression, Hatanaka detection, and CRX2RNX (Hatanaka
compressed RINEX to standard RINEX) conversion, if available. Earthdata credentials remain
outside of the tool arguments, and verifiable JSON responses and pre-check policies prevent
unnecessary transfers. This mechanism records validated parameters, consulted sources, and
written files, enabling a third researcher to precisely reconstruct the acquisition process from the
generated JSON.
The evaluation investigated the influence of alternative tool-exposure strategies on the
performance of LLM-based planning. Different approaches to introducing MCP tools into the
model context, including complete schema catalogues, textual playbooks, restricted allowlists, and
incremental discovery mechanisms, imply distinct prompt sizes and planning strategies. Song et al.
[10] state that in the typical MCP workflows, the client retrieves servers, the servers register
tools/resources/prompts, and then the LLM plans which tools to invoke based on this catalogue of
tools. However, Qin et al. [6] note that, when the tool set is large and the descriptions are long, it
becomes infeasible to provide details of all the tools in the prompt due to context limits. They
therefore propose an intermediate retrieval or tool-selection stage to reduce input length and speed
inference. Xu et al. [12] describe high-level planners (e.g., HuggingGPT, Chameleon, OpenAGI,
and MetaTools) that decompose tasks and orchestrate multi-tool workflows. They emphasize the
need for holistic and efficient planning when many tools are available.
It is noted that variations in context design may affect the quality of tool-selection (F1-score and
workflow), planning complexity, and token consumption. To quantify these effects, this study was
conducted using seven MCP exposure modes (M1–M7) for the GPT-4o-mini model. A corpus of
250 Portuguese tasks was created from 11 geodetic intent categories, including RBMC/CDDIS
acquisition, BRDC retrieval, and Total Electron Content (TEC) workflows (although processing is
not available, the user should be able to request the necessary data), remote availability checks,
missing-data verification, station information queries, multi-tool workflows, and ambiguous
requests. Task instances were generated by combining RBMC stations, year/day-of-year (DOY)
parameters, and four linguistic formulation levels ranging from well-specified to noisy requests.
The proposed evaluation, based on [8,12], were evaluated by having the model generate a JSON
plan for each task. This plan detailed the necessary tools and parameters but did not execute the
corresponding MCP operations. This design isolates the effect of tool exposure strategies from
execution-related factors, such as network availability, repository responses, authentication
2

## Page 3

XIV Colóquio Brasileiro de Ciências Geodésicas
_________________________________________________________________________________
procedures, and file conversion routines. Therefore, the reported results reflect the model's ability
to identify the correct acquisition workflow, rather than the operational performance of the
underlying infrastructure. We assessed performance using F1 and workflow metrics. We obtained
token usage and associated costs directly from OpenAI billing records.
The preliminary results of the hypothesis analysis by mode are summarized in Table 1 and
Figure 2. These highlight the contrast between the textual playbook (M3) and compact index (M7)
approaches versus the full JSON catalog (M1) and lexical-discovery strategies (M4–M5). Figure
2(a–e) presents F1-score, 95% confidence intervals, workflow success rate, cost, and token
consumption. Mode M3 achieved the highest tool-selection performance (F1 = 0.849),
outperforming the full catalog approach M1 (F1 = 0.635) while reducing prompt token
consumption by approximately 85% (255 vs. 1714 tokens) and operational cost (~US$0.015 vs.
~US$0.071 for N=250 tasks). The F1–token trade-off is summarized in Figure 2(e).
In conclusion, the proposed MCP establishes a reproducible and auditable contract between
natural-language intent and RINEX files that are ready for ionospheric analysis. This demonstrates
the potential of MCP-based interfaces for AI-assisted geodetic workflows. Experimental evaluation
further shows that tool exposure design measurably impacts LLM planning performance, and the
textual playbook approach (M3) had the best tool selection performance while minimizing token
consumption and operational costs. This indicates that curated tool descriptions may be more
effective than complete tool catalogues for this class of GNSS acquisition tasks. These findings
suggest a practical path toward more efficient and scalable integration between scientific data
infrastructures and LLM-based agents. Future work includes: (i) replicating the M1–M7
experiments with other generative models (e.g., Claude, Gemini, and open-weight models); (ii)
investigating multi-agent architectures (e.g., planner, executor, and verifier); and (iii) integrating
additional GNSS data sources through new tools, including IGS products, mirrors, and CDDIS
resources, as well as commercial and regional providers.

Figure 1. Architecture of the MCP server proposed.

3

## Page 4

XIV Colóquio Brasileiro de Ciências Geodésicas
_________________________________________________________________________________

Figure 2. MCP exposure modes (M1–M7) with OpenAI gpt-4o-mini (N=250 tasks per mode). (a) Toolselection F1 (mean). (b) Workflow plan success rate. (c) Total cost N=250 (USD). (d) Mean prompt and
output tokens (OpenAI API). (e) F1–input-token trade-off.
Mode (experiment)

Hypothesis/objective

Agent exposure

M1 — Full JSON catalogue

More context improves F1

JSON schemas of 9 tools in the prompt

M2 — TEC allowlist (4 tools)

Minimal surface for the ionosphere

Allowlist: 4 TEC tools

M3 — Textual playbook

Curation beats raw catalogue

Textual playbook (no initial schemas)

M4 — Rich lazy (4 meta-tools)

Rich lazy reduces context tokens

4 meta-tools + lexical search

M5 — Minimal lazy (2 meta-tools)

Minimal lazy (discovery + execution)

2 meta-tools + lexical search

M6 — Single intent (bundle)

Single packaged intent

download_rinex_bundle_tool only

M7 — Index + 1 discovery

Compact index (code-execution style)

One-liner index + 1 discovery step

Table 1. MCP tool exposure variant to the LLM in the planning scenario for M1–M7.

Keywords: Geodesy; Model Context Protocol; RINEX data; GNSS; ionosphere; data
governance; agent evaluation
References
[1]
[2]
[3]

ACHARYA, V. Generative AI and the Transformation of Software Development PracticesarXiv, 12 out.
2025. Disponível em: <http://arxiv.org/abs/2510.10819>. Acesso em: 13 jun. 2026.
HOU, X.; ZHAO, Y.; WANG, S.; WANG, H. Model Context Protocol (MCP): Landscape, Security
Threats,
and
Future
Research
DirectionsarXiv,
7
out.
2025.
Disponível
em:
<http://arxiv.org/abs/2503.23278>. Acesso em: 13 jun. 2026.
JANSSEN, V. Understanding the RINEX Format. 2024.

4

## Page 5

XIV Colóquio Brasileiro de Ciências Geodésicas
_________________________________________________________________________________
[4]

[5]
[6]

[7]
[8]
[9]
[10]
[11]

[12]

PINTO, G.; DE SOUZA, C.; ROCHA, T.; STEINMACHER, I.; SOUZA, A.; MONTEIRO, E. Developer
Experiences with a Contextualized AI Coding Assistant: Usability, Expectations, and Outcomes. Em:
Proceedings of the IEEE/ACM 3rd International Conference on AI Engineering - Software Engineering for AI,
2024, New York, NY, USA. [...]. New York, NY, USA: Association for Computing Machinery, 2024. p. 81–91.
PLAAT, A.; VAN DUIJN, M.; VAN STEIN, N.; PREUSS, M.; VAN DER PUTTEN, P.; BATENBURG, K. J.
Agentic large language models, a survey. Journal of Artificial Intelligence Research, v. 84, 2025.
QIN, Y.; HU, S.; LIN, Y.; CHEN, W.; DING, N.; CUI, G.; ZENG, Z.; ZHOU, X.; HUANG, Y.; XIAO, C.;
HAN, C.; FUNG, Y. R.; SU, Y.; WANG, H.; QIAN, C.; TIAN, R.; ZHU, K.; LIANG, S.; SHEN, X.; XU, B.;
ZHANG, Z.; YE, Y.; LI, B.; TANG, Z.; YI, J.; ZHU, Y.; DAI, Z.; YAN, L.; CONG, X.; LU, Y.; ZHAO, W.;
HUANG, Y.; YAN, J.; HAN, X.; SUN, X.; LI, D.; PHANG, J.; YANG, C.; WU, T.; JI, H.; LI, G.; LIU, Z.;
SUN, M. Tool Learning with Foundation Models. ACM Comput. Surv., v. 57, n. 4, p. 101:1-101:40, 24 dez.
2024.
RAY, P. P. A Survey on Model Context Protocol: Architecture, State-of-the-art, Challenges and Future
Directions.
TechRxiv,
v.
2025,
n.
0418,
[s.d.]Disponível
em:
<https://www.techrxiv.org/doi/full/10.36227/techrxiv.174495492.22752319/v1>. Acesso em: 13 jun. 2026.
SAPKOTA, R.; ROUMELIOTIS, K. I.; KARKEE, M. AI Agents vs. Agentic AI: A Conceptual Taxonomy,
Applications and Challenges. Information Fusion, v. 126, p. 103599, fev. 2026.
SERPELLONI, E.; CAVALIERE, A.; MARTELLI, L.; PINTORI, F.; ANDERLINI, L.; BORGHI, A.;
RANDAZZO, D.; BRUNI, S.; DEVOTI, R.; PERFETTI, P. Surface velocities and strain-rates in the EuroMediterranean region from massive GPS data processing. Frontiers in Earth Science, v. 10, p. 907897, 2022.
SONG, H.; SHEN, Y.; LUO, W.; GUO, L.; CHEN, T.; WANG, J.; LI, B.; ZHANG, X.; CHEN, J. Beyond the
Protocol: Unveiling Attack Vectors in the Model Context Protocol (MCP) EcosystemarXiv, 14 set. 2025.
Disponível em: <http://arxiv.org/abs/2506.02040>. Acesso em: 14 jun. 2026.
WANG, Z.; CHANG, Q.; PATEL, H.; BIJU, S.; WU, C.-E.; LIU, Q.; DING, A.; REZAZADEH, A.; SHAH, A.;
BAO, Y.; SIOW, E. MCP-Bench: Benchmarking Tool-Using LLM Agents with Complex Real-World
Tasks via MCP ServersarXiv, 28 ago. 2025. Disponível em: <http://arxiv.org/abs/2508.20453>. Acesso em:
13 jun. 2026.
XU, W.; HUANG, C.; GAO, S.; SHANG, S. LLM-Based Agents for Tool Learning: A Survey: W. Xu et al.
Data Science and Engineering, p. 1–31, 2025.

5
