---
id: literature/fulltexts/han2026gisclaw
type: fulltext
status: frozen
language: en
key: han2026gisclaw
title: >-
  GISclaw: A Comprehensive Open-Source LLM Agent System for Realistic Multi-Step Geospatial Analysis
resource: https://doi.org/10.48550/arxiv.2603.26845
description: >-
  Most LLM-driven GIS assistants solve narrow single-step tasks tightly coupled to proprietary platforms such as ArcGIS or QGIS, limiting their use for the multi-step, cross-format pipelines that define professional geospatial analysis.
pages: 33
words: 11024
year: 2026
venue: >-
  
authors: >-
  Han, Jinzhen; Lee, JinByeong; Shim, Yuri; Kim, Jisung; Lee, Jae-Joon
doi: 10.48550/arxiv.2603.26845
oa_status: arxiv 2603.26845
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# GISclaw: A Comprehensive Open-Source LLM Agent System for Realistic Multi-Step Geospatial Analysis

## Page 1

GISclaw: A Comprehensive Open-Source LLM Agent System for
Realistic Multi-Step Geospatial Analysis
Jinzhen Han1 , JinByeong Lee1 , Yuri Shim2 , Jisung Kim3,* , and Jae-Joon Lee4,**

arXiv:2603.26845v2 [cs.SE] 3 May 2026

1

Department of Civil, Architectural & Environment Engineering, Sungkyunkwan
University, Suwon, South Korea
2
Ministry of the Interior and Safety, South Korea
3
School of Geography, University of Leeds, United Kingdom
4
Department of Fire Safety Engineering, Jeonju University, Jeonju-si, Republic of Korea
*
Corresponding author: gyjki@leeds.ac.uk
**
Corresponding author: safety lee@jj.ac.kr

Abstract
Most LLM-driven GIS assistants reported to date solve narrow, single-step tasks (a buffer
here, a clip there) and are tightly coupled to proprietary platforms such as ArcGIS or QGIS,
limiting their usefulness for the multi-step, cross-format pipelines that define professional
geospatial analysis. We present GISclaw, a comprehensive open-source agent system that
performs realistic GIS analysis end to end—spatial joins, raster algebra, kriging interpolation, machine-learning classification, network analysis, choropleth cartography—directly
through Python, with no dependency on any commercial GIS software. GISclaw couples
an LLM reasoning core with a persistent Python sandbox pre-loaded with the open-source
geospatial stack (GeoPandas, rasterio, scipy, scikit-learn, libpysal), three engineered prompt
rules (Schema Analysis, Package Constraint, Domain Knowledge Injection), and an ErrorMemory module for self-correction. A single backend-agnostic architecture supports both
cloud-API and locally deployed open-weight LLM backends, enabling air-gapped deployment
without loss of capability. On GeoAnalystBench—50 expert-curated multi-step tasks averaging 5.8 analytical steps across vector, raster, and tabular data—GISclaw reaches up to
100% task success and 97% mean success over three independent runs. We further conduct 1,800 controlled experiments (50 tasks × 6 backends × 2 architectures × 3 repeated
runs) with bootstrap 95% confidence intervals, paired Wilcoxon signed-rank tests, and a
composite-score sensitivity analysis (Kendall’s τ median = 0.94), and introduce a threelayer evaluation protocol combining code structure, reasoning-process, and type-specific
output verification. The Single-Agent ReAct loop reliably outperforms the Dual-Agent
Plan-Execute-Replan pipeline on every cloud backend (Cliff’s δ = 0.15–0.41); only the locally deployed 14B model gains from multi-agent orchestration, suggesting that architectural
complexity should be matched to model capability rather than added by default.

Keywords: GIS agent system; Large language models; Realistic multi-step geospatial analysis;
Open-source GIS; Code generation; Persistent Python sandbox

1

## Page 2

1

Introduction

Geographic Information Systems (GIS) underpin spatial decision-making in domains ranging
from urban planning and environmental monitoring to disaster response and public health [SUN
et al., 2025]. Modern geospatial analysis demands proficiency across multiple data modalities—
vector geometries for boundaries and infrastructure, raster grids for satellite imagery and elevation models, and tabular attributes for census and sensor data—using specialized toolchains
such as ArcGIS, QGIS, and programmatic libraries including GeoPandas, rasterio, and scipy.
This steep technical barrier limits accessibility for domain scientists who understand what analysis is needed but lack the programming skills to implement how, creating a persistent bottleneck
between geospatial questions and actionable answers. The rapid advancement of Large Language Models (LLMs) with strong code generation and reasoning capabilities has opened a
promising pathway to bridge this gap through autonomous GIS agents—systems that translate natural-language instructions into executable spatial analysis workflows [Li et al., 2025].
Li and Ning [2023] formalized this vision as “Autonomous GIS,” demonstrating that GPT-4
could generate and execute spatial analysis code with approximately 80% success. Subsequent
systems advanced different axes of this vision: GIS Copilot [Akinboyewa et al., 2025] integrates LLM-guided tool selection within QGIS (86% success on 110 tasks); GeoGPT [Zhang
et al., 2023] integrates GPT-3.5 with a GIS tool pool for autonomous spatial data collection
and analysis; GeoJSON Agents [Luo et al., 2026] compare code-generation vs. function-calling
paradigms (97% on 70 tasks); GeoColab [Wu et al., 2025] introduces a three-role multi-agent
framework with RAG (+7–26% over single-agent baselines); GTChain [Zhang et al., 2025b] finetunes LLaMA-2-7B on synthetic tool-use chains; and GeoCode-GPT [Hou et al., 2025b] demonstrates that domain pretraining on geospatial code corpora can outperform general-purpose
code LLMs on Python-based GIS analysis. A parallel thread of multi-agent work—including
the autonomous data-retrieval framework of Ning et al. [2025], the multi-agent GeoQA portal of
Feng et al. [2025], the RAG-augmented GeoAgentic-RAG architecture of Liang et al. [2026], and
the multi-agent geospatial knowledge-base question-answering system of Yang and Kim [2026]—
has explored role decomposition, retrieval grounding, and structured-knowledge integration as
routes to richer geospatial reasoning, although none of these systems isolates the contribution of
multi-agent orchestration through controlled comparison against a strong single-agent baseline.
On the evaluation side, GeoAnalystBench [Zhang et al., 2025a] provides the most comprehensive GIS benchmark to date (50 expert tasks), complemented by GeoBenchX [Krechetova
and Kochedykov, 2025] for multi-step geospatial reasoning, the multi-task evaluation of Xu
et al. [2025], the JavaScript-focused GeoJSEval framework of Chen et al. [2025], and cloudbased benchmarks [Cardille et al., 2025], while metrics research has produced CodeBLEU [Ren
et al., 2020], LLM-as-a-Judge [Zheng et al., 2023], and embedding-based similarity [Reimers
and Gurevych, 2019]—each capturing complementary aspects of agent quality. Despite these
advances, three critical limitations persist across existing systems, all rooted in system design rather than model capability: (1) Narrow data-type coverage. Although some systems incorporate basic raster support (e.g., GIS Copilot via QGIS raster tools, GTChain via
Kriging/density operators), none provides an integrated workflow that spans vector overlays,

2

## Page 3

raster interpolation, spectral index computation, and machine learning (clustering, classification) within a single agent execution. (2) Platform dependency and limited model diversity. Most systems are tightly coupled to a single LLM (typically GPT-4) and often depend
on proprietary GIS platforms [Li and Ning, 2023, Akinboyewa et al., 2025]. This coupling prevents systematic comparison across model families and precludes deployment in air-gapped or
resource-constrained environments where API access is unavailable. (3) Fragmented evaluation methodology. Existing metrics—binary task success, CodeBLEU, or single-dimension
LLM judging—each capture only one facet of agent quality [Hou et al., 2025a, Gramacki et al.,
2024], and no prior work unifies them into a coherent multi-layer protocol. The functional
equivalence problem in GIS code—where a buffer analysis can be correctly implemented via
gpd.overlay(), shapely.buffer(), or gpd.sjoin(), all producing identical outputs—further
renders lexical metrics unreliable. To address these system-level gaps, we present GISclaw,
a comprehensive open-source LLM agent system designed to perform realistic, multi-step
geospatial analysis of the kind a professional GIS analyst would carry out by hand—krigingbased hot-spot mapping, Random-Forest mineral prospectivity prediction, multi-criteria wildlife
corridor optimization, network-based travel-time isochrones—directly through the open-source
Python ecosystem, with no dependency on any commercial GIS software. GISclaw couples a
persistent Python sandbox pre-loaded with the open-source geospatial stack (GeoPandas, rasterio, scipy, scikit-learn, libpysal, geoplot, cartopy) to a model-agnostic LLM reasoning core; three
engineered prompt rules (Schema Analysis, Package Constraint, Domain Knowledge Injection)
and an Error-Memory module bridge the recurring task–data information gap and enable iterative self-correction. As Table 1 summarizes, GISclaw differs from existing GIS agent systems
along several axes simultaneously, with the most important being the realism and analytical
depth of the supported workflows: we cover all 50 expert-curated multi-step tasks of GeoAnalystBench [Zhang et al., 2025a]—averaging 5.8 analytical steps each and spanning vector,
raster, and tabular data—rather than the simpler single-tool clip/buffer pipelines that dominate
prior systems. Our contributions are:
• A comprehensive open-source agent system for realistic GIS analysis. GISclaw
is, to our knowledge, the first LLM-driven GIS agent that runs end-to-end professional
analytical pipelines—spatial overlays, raster algebra, geostatistical interpolation, machinelearning classification, network analysis, and publication-quality cartography—entirely
on the open-source Python stack, without falling back to ArcPy, QGIS plugins, or any
other proprietary GIS layer. The system pairs a persistent Jupyter-like sandbox with a
backend-agnostic LLM interface; we release the system, the prompt templates, and the
open-source-rewritten gold-standard solutions for all 50 GeoAnalystBench tasks under
an MIT licence.
• Demonstrated coverage of professional-grade GIS workflows. On the 50 multistep GeoAnalystBench tasks—each modelled on a real-world analysis (urban heatisland and at-risk population mapping, mineral prospectivity prediction, flood risk under
sea-level rise, fire-station coverage gap analysis, wildlife corridor optimization, etc.)—
GISclaw achieves up to 100% task success and 97% mean success over three repeated runs,
with realistic outputs that include georeferenced raster surfaces, multi-layer choropleths,
3

## Page 4

and cartographically complete maps rather than only intermediate computations.
• A three-layer evaluation protocol for GIS agents. Existing benchmarks score
agents by single dimensions—binary task success, code-similarity metrics, or LLM-asJudge ratings—each capturing only a facet of agent quality. We propose a unified protocol
combining (i) code structure analysis (CodeBLEU + API Operation F1), (ii) reasoningprocess assessment (embedding similarity, complemented by an LLM-as-Judge as a qualitative diagnostic), and (iii) type-specific output verification (multimodal vision scoring for
visualizations, programmatic raster/vector/tabular comparison). Composite scoring under this protocol is shown to be robust under sensitivity analysis of the dimension weights
(median Kendall’s τ = 0.94).
• Methodological validation via 1,800 controlled experiments. Across 50 tasks ×
6 backends × 2 architectures × 3 repeated runs, statistical analysis (95% bootstrap CIs,
paired Wilcoxon, Cliff’s δ) supports two findings that we believe will be useful to the
broader GIS-agent community: (i) per-task performance varies non-trivially across runs
even for flagship models, motivating repeated-run protocols as a default; and (ii) within
GISclaw’s identical infrastructure, the Single-Agent ReAct loop reliably outperforms a
Dual-Agent Plan-Execute-Replan pipeline on every cloud backend, with only the locally
deployed 14B model gaining from multi-agent orchestration—suggesting that architectural
complexity should be matched to model capability rather than added by default.
The remainder of this paper is organized as follows: Section 2 details the system architecture
and methodology; Section 3 introduces the evaluation framework and benchmark; Section 4
presents experimental results and design analysis; Section 6 concludes with future directions.
Table 1: Comparison of GISclaw with existing LLM-powered GIS agent systems.

‡

System

Data Types

Models

Architectures

Open-Source

Tasks

Best Success

LLM-Geo [Li and Ning, 2023]
GIS Copilot [Akinboyewa et al., 2025]
GeoGPT [Zhang et al., 2023]
GeoJSON Agents [Luo et al., 2026]
GeoColab [Wu et al., 2025]
GTChain [Zhang et al., 2025b]

Vector
Vector+Raster
Vector
GeoJSON
Vector
Vector+Raster

1 (GPT-4)
2 (GPT-4/3.5)
1 (GPT-3.5)
Multiple
7
2 (LLaMA/GPT-4)

Single
Single
Single
Multi (2-role)
Multi (3-role)
Single (Fine-tuned)

✓
✓
No
No
✓
✓

Case study
110
Case study
70
50
Custom

∼80%
86.4%
—
97.1%
+26.1%
+32.5%‡

GISclaw (ours)

Vec+Ras+Tab

6

SA + DA

✓

50

100%

Relative improvement over GPT-4 on the GTChain benchmark, not an absolute success rate.

2

Methodology

GISclaw is designed around three principles: (1) Platform independence: no dependency on
proprietary GIS software, relying exclusively on open-source Python libraries; (2) Model agnosticism: a pluggable LLM interface supporting cloud APIs and locally deployed models with
identical workflows; (3) Domain-aware prompting: engineered prompt rules that inject GISspecific knowledge to compensate for LLMs’ limited geospatial training data. Fig. 1 illustrates
the overall system design.

4

## Page 5

Figure 1: Overview of the GISclaw system architecture. The system accepts natural-language
tasks with GIS data (vector, raster, tabular) as input, routes them through a pluggable LLM
backend, and executes analysis in a persistent Python sandbox. Two agent architectures—
Single Agent (ReAct) and Dual Agent (Plan-Execute-Replan)—are supported, with outputs
evaluated via a three-layer protocol.

2.1

System Design

A fundamental design decision in GISclaw is its complete independence from proprietary GIS platforms. Unlike systems that embed LLMs within existing GIS software—e.g.,
GIS Copilot [Akinboyewa et al., 2025] couples with QGIS processing tools, and GeoGPT [Zhang
et al., 2023] relies on an external GIS tool pool—GISclaw constructs its analytical capabilities entirely from open-source Python libraries. This design choice is motivated by the observation that
platform-dependent agents inherit the limitations and licensing constraints of their host software, restricting reproducibility and deployment flexibility. Moreover, pilot experiments with
non-agent, single-pass LLM code generation revealed critical deficiencies—models frequently
produced syntactically valid but semantically incorrect GIS code (e.g., wrong CRS transforms,
inverted raster band indices) that could not self-correct without iterative execution feedback,
confirming the necessity of an agent-based architecture with sandbox integration. By building
on a self-contained Python ecosystem (Table 2), GISclaw ensures that any analysis expressible
in Python—from basic vector overlays to machine learning-based spatial prediction—can be
executed without external software dependencies.

5

## Page 6

Table 2: Pre-loaded open-source library stack organized by analytical capability. This ecosystem
replaces the need for proprietary GIS platforms.
Category

Libraries

Capabilities

Vector

GeoPandas,
shapely, fiona,
pyproj

Spatial joins, buffer,
overlay, CRS transforms

Raster

rasterio, xarray,
rasterstats

Band algebra, interpolation,
zonal
statistics

Analysis

scipy,
scikitlearn, libpysal

Kriging, clustering,
regression,
spatial
autocorrelation

Visualization matplotlib,
seaborn, geoplot, cartopy

Choropleth,
heatmaps,
multipanel cartography

The execution core of GISclaw is a persistent Python sandbox that provides an interactive, Jupyter-like environment where variables and imported libraries persist across execution
rounds within a single task. Unlike stateless code-generation approaches that execute monolithic scripts, the sandbox enables the agent to execute incremental code snippets, inspect
intermediate results, and iteratively refine its approach—a capability critical for exploratory
GIS workflows where each analytical step depends on the results of the previous one. The
sandbox pre-loads a comprehensive GIS library stack (GeoPandas, rasterio, numpy, scipy, matplotlib, shapely, scikit-learn) upon initialization, eliminating common ImportError failures. A
key design choice is an asymmetric output truncation policy: standard output is truncated from the front (preserving the most recent data inspection results), while error output
is truncated from the tail (preserving the root-cause error message). This strategy is informed
by the observation that GIS agents primarily need the latest intermediate results for decisionmaking, whereas debugging requires the original error traceback. The sandbox further tracks
new variables created in each execution round and enforces a 10-minute per-task timeout to
prevent runaway computations. Table 3 summarizes the key design features of the sandbox and
their rationale.

6

## Page 7

Table 3: Key design features of the persistent Python sandbox.
Feature

Design Rationale

State
tence

Variables and imports survive
across rounds, enabling incremental exploratory analysis

persis-

Asymmetric
truncation

stdout: front-truncated (latest
results); stderr: tail-truncated
(root-cause error)

Variable
tracking

New variables logged per round,
providing the agent with execution context

10-min timeout

Prevents runaway computations
(e.g., large-scale Kriging on consumer GPUs)

A central design goal of GISclaw is model agnosticism. The system abstracts all LLM
interaction through a unified LLMEngine interface, decoupling the agent logic from any specific
model provider. This interface supports cloud-hosted APIs, locally served open-weight models,
and even quantized models running on a single consumer GPU, enabling deployment scenarios
ranging from full cloud to fully air-gapped environments. In practice, we found that different
model families exhibit substantial variation in output formatting conventions—e.g., some models
wrap code in markdown fences while others emit raw code, and reasoning-specialized models
allocate internal “thinking tokens” that reduce the effective output budget. GISclaw addresses
these incompatibilities through provider-specific adapters within the unified interface, allowing
any conforming LLM backend to be plugged in without modifying the agent logic.

2.2

Domain-Specific Prompt Engineering

Through iterative development and failure analysis, we identified three prompt engineering rules
that are critical for reliable GIS agent performance. The first rule, Schema Analysis, addresses a fundamental information gap between task descriptions and actual data schemas. GIS
datasets frequently use abbreviated or domain-specific column names (e.g., “ACSHHBPOV”
for poverty rate) that LLMs cannot infer from task descriptions alone. To bridge this gap,
the system prompt mandates that the agent’s first action must be a data inspection step—
printing column names, data types, coordinate reference systems, and sample rows—before
generating any analytical code. In ablation experiments, this single rule eliminated columnname guessing errors and significantly improved output quality for the locally deployed 14B
model. The second rule, Package Constraint, prevents the agent from generating code that
depends on proprietary or unavailable libraries. LLMs trained on GIS corpora frequently produce arcpy code (requiring an ArcGIS license) or reference packages not installed in the sandbox
(e.g., pykrige, skimage). The prompt explicitly redirects the agent to open-source equivalents
such as geopandas, rasterio, and scipy.interpolate. The third rule, Optional Domain
Knowledge Injection, exposes a small input field through which a domain expert can supply
task-specific procedural knowledge that lies beyond the LLM’s parametric capabilities—a cal-

7

## Page 8

ibrated parameter, a non-obvious step ordering, a domain-specific threshold. When supplied,
this hint is injected directly into the agent prompt; when absent, the agent proceeds with its own
decomposition. The field is optional precisely because real GIS analysts sometimes have such
knowledge to share and sometimes do not, and we show in Section 4.1.6 that the system delivers
comparable end-to-end task success in either mode. Fig. 1 illustrates a simplified excerpt of the
system prompt, showing how these three rules are operationalized.
You are a GIS analyst agent. Solve geospatial
analysis tasks step-by-step using tools.
## Basic Guidelines
1. Start by calling list_files to see available data.
2. Load and inspect data (print columns, CRS,
shape, head) BEFORE writing analysis code.
3. If unsure about a library API or GIS method,
call search_docs to look it up.
4. Save outputs to pred_results/ before finish.
5. NEVER use plt.show(). Always use
plt.savefig(..., dpi=150, bbox_inches=’tight’)
## Available Packages (ONLY use these)
geopandas, rasterio, shapely, numpy, pandas,
scipy, matplotlib, sklearn, xarray, ...
NOT available (do NOT import): pykrige, arcpy
Alternatives: pykrige -> scipy.interpolate

Listing 1: Simplified excerpt of the GISclaw system prompt (Single Agent mode).

2.3

Agent Architectures

GISclaw implements two pluggable agent architectures that operate on the same sandbox and
prompt infrastructure, enabling controlled comparison of their effectiveness across different
model capabilities. Fig. 2 illustrates the two architectures. Single Agent (SA) follows the

Figure 2: Comparison of the two agent architectures. (a) Single Agent follows a ReAct loop
with Error Memory for self-correction. (b) Dual Agent decomposes tasks via a Planner, executes
steps through a Worker, and adaptively replans upon failure.
ReAct [Yao et al., 2022] paradigm, iteratively generating Thought (natural-language reasoning),
Action (Python code for the sandbox), and receiving Observation (execution output or error
8

## Page 9

messages). An ErrorMemory module records error patterns encountered across rounds, preventing the agent from repeating failed approaches and promoting progressive refinement. The
agent accumulates all generated code into a consolidated script upon task completion. Dual
Agent (DA) adopts a Plan-Execute-Replan pipeline with explicit task decomposition. A Planner receives the task instruction, domain knowledge, and data schema (obtained via Schema
Analysis), then decomposes the task into 3–7 ordered analytical steps. A Worker executes each
step within the shared persistent sandbox, with up to 10 self-correction rounds per step. When
the Worker fails on a step, the Planner is re-invoked as a Replanner with the failure context to
generate a simplified alternative plan that avoids the failed operations; up to 2 replanning cycles
are permitted. Both roles share the same underlying LLM and sandbox namespace, ensuring
information continuity. Notably, the Replanner is not a separate module but the same Planner invoked with failure-aware context—this keeps the architecture lightweight while enabling
adaptive recovery.

3

Evaluation Framework and Benchmark

3.1

Benchmark Dataset

We evaluate GISclaw on GeoAnalystBench [Zhang et al., 2025a], the most comprehensive
publicly available benchmark for GIS agent systems. GeoAnalystBench comprises 50 expertdesigned tasks organized into six analytical categories (Table 4), spanning three data modalities
(vector, raster, tabular) with an average of 5.8 workflow steps per task. Each task is modeled
after a real-world GIS analysis scenario—including flood risk assessment, mineral prospectivity
mapping, urban heat island analysis, and wildlife corridor optimization—requiring multi-step
spatial reasoning, cross-format data integration, and domain-specific parameter calibration.
This design prioritizes analytical depth over task count: the 50 tasks collectively cover the
full spectrum of geospatial operations (overlay, buffer, interpolation, raster algebra, machine
learning, network analysis) at a complexity level representative of professional GIS workflows,
making the benchmark a rigorous testbed for agent capability despite its moderate size. Across
all evaluation experiments, we uniformly inject the “Human Designed Workflow” provided by
the benchmark as domain knowledge (see Section 2.2) directly into the evaluation prompt.
This setup not only ensures fair comparability among models under identical problem-solving
logic but also effectively isolates the vast variance introduced by unconstrained free exploration,
thereby truly reflecting the Agent’s ability to comprehend and execute precise professional instructions. Gold standard adaptation. A critical contribution of our work is the systematic
adaptation of GeoAnalystBench’s gold-standard solutions. The original benchmark provides expert-authored reference code written in ArcPy—a Python API tightly coupled with
the proprietary ArcGIS platform. Since GISclaw operates entirely on open-source libraries, we
manually rewrote all 50 gold-standard solutions using the open-source GIS ecosystem (GeoPandas, rasterio, scipy, scikit-learn), ensuring functional equivalence while eliminating proprietary
dependencies. These rewritten solutions serve as the reference for all evaluation layers (L1–L3).

9

## Page 10

Table 4: GeoAnalystBench task categories with representative examples. Each task includes natural-language instructions, heterogeneous input data, optional domain knowledge,
and expert-authored gold-standard code.

3.2

Category

N

Representative Task

Understanding
spatial distributions

19

T1: Urban heat island & elderly risk mapping via Kriging interpolation

Making predictions

8

T20: Mineral deposit prediction using Random Forest
with raster features

Detecting patterns

7

T42: Airbnb price clustering via local Moran’s I spatial autocorrelation

Measuring
shape & distribution

7

T36: Vegetation change detection using SAVI spectral
index

Determining
spatial
relationships

6

T38: Travel-time isochrone
computation on road networks

Optimal locations & paths

3

T32: Wildlife corridor optimization via weighted costsurface overlay

LLM Backends

To validate model agnosticism, we evaluate GISclaw with six heterogeneous LLM backends
spanning cloud APIs and local deployments (Table 5). Cloud models include two OpenAI
models (GPT-5.4 and GPT-4.1), DeepSeek-V3.2 (a cost-effective alternative at significantly
lower price), and Google’s Gemini-3-Flash. For offline deployment, we test Llama-3.3-70B
on a multi-GPU server and Qwen2.5-Coder-14B on a single consumer RTX 3090 GPU. This
selection covers the spectrum from flagship reasoning models to lightweight code-specialized
models, enabling systematic comparison of how model capability interacts with system design.
Table 5: LLM backends evaluated. Cost is per million tokens (input/output). Open-weight
models are deployed on local servers at zero marginal cost.
Model

Backend

Cost ($/M)

Context

Cloud API (pay-per-use)
GPT-5.4
OpenAI
GPT-4.1
OpenAI
DeepSeek-V3.2 DeepSeek
Gemini-3-Flash Google AI

2.50 / 15.00
2.00 / 8.00
0.28 / 0.42
0.50 / 3.00

1M
1M
128K
1M

Local deployment (zero marginal cost)
Llama-3.3-70B
Local server
Qwen2.5-14B
Local GPU

10

Free
Free

128K
32K

## Page 11

3.3

Multi-Layer Evaluation Protocol

To comprehensively assess agent performance beyond binary success rates, we propose a multilayer evaluation protocol that captures complementary aspects of agent quality—from surfacelevel code fidelity to deep reasoning process and final output correctness (Fig. 3). Individual
layer scores are combined into a composite score:
Scomp = 0.4 · Rsucc + 0.3 · Qout + 0.15 · Fapi + 0.15 · Cemb

(1)

where Qout averages only over successful tasks to avoid double-penalizing failures already captured by Rsucc . L1: Code Structure. We evaluate syntactic and structural similarity be-

CodeBLEU

L1: Code
API Op. F1

Embedding Sim.

L2: Process
LLM-as-Judge

Scomp

qualitative

PNG: Vision

L3: Output

TIF: Rasterio
CSV/SHP

Figure 3: Multi-layer evaluation pipeline. Three complementary layers assess code-level fidelity
(L1), reasoning process quality (L2), and output correctness (L3), combined into a weighted
composite score Scomp (Eq. 1).
tween generated and gold code using four metrics. BLEU-4 [Papineni et al., 2002] computes
geometric-mean n-gram precision (n = 1. . .4) with brevity penalty:
 P

BLEU-4 = BP · exp 41 4n=1 log pn

(2)

where pn denotes clipped n-gram precision and BP = min(1, e1−|r|/|c| ). ROUGE-L measures
the longest common subsequence (LCS):
Rlcs = |LCS|
|r| ,

Plcs = |LCS|
|c| ,

Plcs
Flcs = R2Rlcslcs+P
lcs

(3)

CodeBLEU [Ren et al., 2020] extends BLEU with code-aware components:
CodeBLEU = 41 αngram + αwt + αsyn + αdf

11



(4)

## Page 12

where αngram is standard BLEU-4, αwt is keyword-weighted n-gram match (Python keywords receive double weight), αsyn is AST subtree match F1, and αdf is data-flow match F1 based on variable define–use chains. We additionally compute Edit Similarity as 1−dLev / max(|r|, |c|). Critically, we introduce API Operation F1: extracting GIS-specific operations (e.g., spatial join,
buffer, overlay, kriging) from both generated and reference code via pattern matching, and
computing set-level precision, recall, and F1. This metric is robust to the functional equivalence problem, where semantically correct implementations share minimal lexical overlap. L2:
Reasoning Process. This layer evaluates whether the agent’s analytical reasoning process
aligns with expert expectations, using two complementary methods. First, we encode cleaned
execution logs and gold references using OpenAI’s text-embedding-3-large model (3072-d)
and compute cosine similarity:
Cemb =

eagent · egold
∥eagent ∥ · ∥egold ∥

(5)

This provides a continuous, reference-aligned measure of process quality. Second, we employ an
LLM-as-Judge protocol [Zheng et al., 2023]: DeepSeek-V3.2 in non-thinking mode—chosen for
cost-controlled evaluation across the full 1,800-experiment grid and held fixed across all runs
to ensure cross-run comparability—scores each execution log on five dimensions (1–5 scale):
(i) Task Understanding: correct interpretation and planning; (ii) Data Handling: loading, CRS
management, format handling; (iii) Methodology: appropriateness of GIS analysis methods;
(iv) Self-Correction: error detection and recovery efficiency; (v) Result Completeness: completeness of final deliverables. The judge receives the task instruction, expert-authored gold
code, and the complete execution log, producing per-dimension scores with natural-language
justifications. This dual assessment captures both statistical process alignment (embedding)
and nuanced qualitative reasoning evaluation (LLM-as-Judge). Of the two, only Cemb enters the composite score (Eq. 1); the LLM-as-Judge scores serve as a qualitative diagnostic
tool for the case-study analysis in Section 4. L3: Output Accuracy. Generated outputs
are evaluated against gold standards using type-specific methods tailored to the heterogeneous output formats of GIS tasks: Visualization outputs (PNG): a multimodal vision model
(Gemini-2.5-Flash-Lite, chosen for cost control across the 1,800-experiment grid and yielding
100% JSON-valid responses with zero parse errors) receives both the gold and agent images
alongside the task instruction, scoring five cartographic dimensions: Task Completion, Spatial Accuracy, Visual Readability, Cartographic Quality, and Data Integrity (each 1–5), explicitly accepting alternative-but-correct visualization styles. Blank or near-blank images are
pre-filtered by a PIL-based heuristic (≤ 5 unique colours) before the vision call. Raster outputs (GeoTIFF): evaluated programmatically via CRS match, shape match, pixel-level Pearson
correlation, and mean relative error against the gold raster, yielding a weighted composite:
sraster = 0.2 · 1shape + 0.2 · 1CRS + 0.3 · f (ρ) + 0.3 · g(MRE), where f and g are piecewise
thresholding functions. Tabular outputs (CSV): assessed through column overlap ratio, rowcount match, and average Pearson correlation across shared numeric columns. Vector outputs
(Shapefile, GeoJSON, GeoPackage): compared via feature count match, CRS consistency, and
column overlap ratio against the gold reference. All type-specific scores are normalized to [0, 1]

12

## Page 13

(vision scores are divided by the maximum scale of 5) and averaged across output files to yield
a per-task output accuracy score Qout .

4

Experimental Results and Analysis

To evaluate GISclaw thoroughly, we run the system on every GeoAnalystBench task across
the six LLM backends introduced in Section 3.2 and the two agent architectures, repeated three
times per cell—1,800 controlled executions in total. Each task is allocated a 20-minute hard
timeout and a maximum of 50 interaction rounds; sampling temperature, prompts, and sandbox
configuration are held fixed across runs, so any per-task variance reflects the stochasticity of
the LLM samples rather than configuration drift. The sandbox environment runs Ubuntu with
Python 3.12 and the pre-loaded GIS library stack described in Section 2.1. Table 6 presents
the aggregated results, with each cell averaged over its three repeated runs. GISclaw reaches a
peak mean success rate of 100% (GPT-5.4, SA) and three further backends exceed 96% mean
success in SA mode, indicating that the system reliably executes the entire 50-task realisticpipeline benchmark even with mid-tier cloud APIs and the locally deployed Llama-3.3-70B. The
Single-Agent ReAct loop is the stronger architecture for every cloud backend; the Dual-Agent
Plan-Execute-Replan pipeline only outperforms its Single-Agent counterpart on the smallest
model in the suite (Qwen2.5-Coder-14B), a pattern we examine in detail in Sections 4.1.1
and 4.1.5. The following subsections analyse each evaluation layer in turn.

13

## Page 14

Table 6: Comprehensive evaluation across all six LLM backends and two architectures, averaged
over three repeated runs (50 tasks per cell, n = 150 task-runs per model–architecture). Rs : task
success rate; Qout : output accuracy (L3, successful tasks only); Fapi : API operation F1 (L1);
Cemb : embedding cosine similarity (L2); Scomp : composite score (Eq. 1) with bootstrap 95%
confidence interval. Cost is the total API expenditure averaged per benchmark sweep (50 tasks,
single run). Bold = best per architecture.
Single Agent
Model
DeepSeek-V3.2
Gemini-3-Flash
GPT-5.4
GPT-4.1
Llama-3.3-70B
Qwen2.5-14B
†

Dual Agent

Rs

Qout

Fapi

Cemb

Scomp (±CI)

Cost

Rs

Qout

Fapi

Cemb

Scomp (±CI)

Cost

0.973
0.967
1.000
0.967
0.913
0.520

0.635
0.635
0.562
0.601
0.398
0.549

0.632
0.662
0.602
0.663
0.610
0.518

0.641
0.647
0.633
0.604
0.614
0.590

0.761 ( ±0.023)
0.765 ( ±0.024)
0.750 ( ±0.016)
0.747 ( ±0.026)
0.656 ( ±0.029)
0.454 ( ±0.050)

$0.50
$0.80
$8.50
$1.20
$0†
$0†

0.893
0.867
0.967
0.933
0.893
0.787

0.532
0.540
0.507
0.503
0.344
0.427

0.585
0.532
0.538
0.573
0.577
0.586

0.636
0.562
0.628
0.648
0.620
0.599

0.681 ( ±0.033)
0.650 ( ±0.036)
0.705 ( ±0.022)
0.695 ( ±0.027)
0.627 ( ±0.030)
0.588 ( ±0.038)

$0.80
$1.50
$12.30
$3.40
$0†
$0†

Open-weight models deployed locally; zero marginal cost.

4.1
4.1.1

Quantitative Evaluation Results
Task success rate and architecture comparison

Fig. 4 visualizes the SA–DA gap across all models, averaged over three repeated runs. For
all four cloud backends and the 70B open-weight model, the Single Agent reliably exceeds the
Dual Agent in mean success rate by 3–10 percentage points, with the largest absolute drop
on DeepSeek-V3.2 (97.3% → 89.3%, −8.0 pp) and Gemini-3-Flash (96.7% → 86.7%, −10.0
pp). Qwen2.5-Coder-14B is the only backend whose mean success rate rises under multi-agent
orchestration (52.0% → 78.7%, +26.7 pp), consistent with the architecture–capability matching
principle. The SA–DA composite gap on the five models where SA wins is between 0.03 and 0.11,
indicating that the Dual Agent overhead, while statistically reliable, is moderate in absolute size
once measured over repeated runs at the task level rather than from any single deterministic
execution.

Figure 4: Task success rate comparison (mean over three repeated runs): Single Agent (solid) vs.
Dual Agent (hatched). All cloud and large open-weight models show the Single Agent reliably
ahead; only Qwen2.5-Coder-14B improves under the Dual Agent.

14

## Page 15

Statistical significance. Table 7 reports per-model paired Wilcoxon signed-rank tests on
the task-level composite scores (n = 150 paired task-runs per model: 50 tasks × 3 runs). For
five of six models, the Single Agent significantly outperforms the Dual Agent (p < 0.02 for all
five; p < 10−3 for the four cloud models), with effect sizes ranging from small (Cliff’s δ ≈ 0.15
for Llama-3.3-70B) to medium (Gemini-3-Flash, δ = 0.41). Qwen2.5-Coder-14B is the sole
reversal: the Dual Agent significantly outperforms the Single Agent (p < 10−3 , δ = −0.20),
confirming that the planner–worker decomposition compensates for the smaller model’s weaker
single-shot reasoning.
Table 7: Paired Wilcoxon signed-rank tests on task-level composite scores: Single Agent vs.
Dual Agent. n = 150 paired task-runs per row (50 tasks × 3 runs); positive median difference
and Cliff’s δ favour SA. All but Llama-3.3-70B reach p < 10−3 .
Model

SA
Scomp

DA
Scomp

Median ∆

Cliff ’s δ

p-value

Gemini-3-Flash
DeepSeek-V3.2
GPT-4.1
GPT-5.4
Llama-3.3-70B

0.7646
0.7612
0.7473
0.7504
0.6563

0.6501
0.6809
0.6954
0.7052
0.6269

+0.067
+0.028
+0.034
+0.029
+0.010

+0.41
+0.29
+0.26
+0.21
+0.15

< 10−3
< 10−3
< 10−3
< 10−3
0.017

Qwen2.5-Coder-14B

0.4537

0.5882

−0.032

−0.20

< 10−3

Figure 5: Mean composite score Scomp per (model, architecture) cell with 95% bootstrap confidence intervals (n = 150 paired task-runs per cell). All four cloud backends and Llama-3.3-70B
sit higher under SA than DA; Qwen2.5-Coder-14B is the only backend whose CI bracket clears
the corresponding SA bracket on the right.
Sensitivity to composite weights. Because the four-component composite (Eq. 1) involves a choice of weights, we re-rank the twelve (model, architecture) cells under all 66 weight
tuples (wsucc , wout , wapi , wcos ) on the simplex {0.1, 0.2, 0.3, 0.4, 0.5} summing to 1. The Kendall’s
τ between the resulting ranking and the paper-default ranking has median 0.94 (range 0.79–
1.00), and τ ≥ 0.90 in 47 of 66 weight configurations. The two qualitative conclusions—five
15

## Page 16

models favour SA at the task level, and Qwen-14B favours DA—hold under every weight tuple
we tested.
4.1.2

Code quality analysis (L1)

Table 8: Code quality metrics across architectures, averaged over three repeated runs (50 tasks
per cell). Bold = best per architecture.
Model

CodeBLEU

API F1

ROUGE-L

Single Agent
GPT-5.4
GPT-4.1
Gemini Flash
Llama-70B
Qwen-14B
DeepSeek

0.172
0.171
0.168
0.166
0.162
0.126

0.602
0.659
0.662
0.606
0.504
0.632

0.136
0.142
0.141
0.137
0.132
0.097

Dual Agent
Gemini Flash
GPT-4.1
GPT-5.4
DeepSeek
Qwen-14B
Llama-70B

0.176
0.163
0.139
0.122
0.110
0.094

0.532
0.573
0.535
0.585
0.574
0.577

0.137
0.132
0.109
0.092
0.098
0.091

A notable finding from Table 8: in DA mode, Llama-70B achieves the lowest CodeBLEU
(0.094) yet near-equal API F1 (0.577), and DeepSeek shows the same pattern (CodeBLEU 0.122,
API F1 0.585). This exposes the systematic bias of CodeBLEU for GIS code—a single task
(e.g., buffer analysis) can be correctly implemented via gpd.overlay(), shapely.buffer(),
or gpd.sjoin() with manual geometry operations, all yielding equivalent results but sharing
minimal lexical overlap. We recommend API F1 as a more reliable metric for GIS code
evaluation. Fig. 6 presents the per-task API F1 distribution, revealing that code similarity
is highly task-dependent: simple overlay tasks (T24, T40) score consistently above 0.7 across
models, while complex multi-step analyses (T27, T39) show near-zero overlap even for successful
completions.

Figure 6: Per-task API F1 scores (DA architecture). Warm colors indicate higher code-level
agreement with gold standards. The task-dependent variance highlights the limitation of aggregate metrics.

16

## Page 17

4.1.3

Reasoning process assessment (L2)

Fig. 7 presents the execution log embedding similarity for each task–model pair, averaged over
three repeated runs. In SA mode, DeepSeek and Gemini Flash maintain consistently high cosine
similarity (∼ 0.64 on average) across most tasks; in DA mode, the planner–worker decomposition produces an even slightly higher average similarity for some backends (e.g., GPT-4.1 SA
0.604 vs. DA 0.648) but with greater task-level dispersion. The two architectures therefore
align similarly with gold-standard reasoning on average, but the Dual Agent’s planning step
distributes its similarity less uniformly across tasks. To complement the embedding-based as-

Figure 7: L2: Execution log embedding cosine similarity per task (mean across three repeated
runs). Each dot represents one (model, task) pair. SA and DA produce comparable mean
similarity, with DA showing greater task-level variance for the same model.
sessment, a DeepSeek-V3.2 (non-thinking) LLM-as-Judge—deliberately distinct from the GPTand Gemini-family models being scored—evaluates each execution log across five qualitative dimensions (Table 9). The judge serves as a qualitative diagnostic only; the composite score in
Table 6 relies on the embedding cosine Cemb rather than on the judge’s ratings. DeepSeek
dominates all SA dimensions (4.04/5), while GPT-4.1 leads in DA mode (3.36/5). The largest
SA–DA gap appears in the Result-Completeness dimension, consistent with the observation
that the Dual Agent’s replanning loop interrupts successful task completions on strong models.

17

## Page 18

Table 9: LLM-as-Judge reasoning assessment (1–5 scale). Bold = best per architecture. The
five dimensions capture task understanding, data handling, methodology, self-correction, and
result completeness.

Model

Task

Data

Method

Self-Corr.

Result

Avg.

Single Agent
DeepSeek
Gemini Flash
GPT-5.4
GPT-4.1
Llama-70B
Qwen-14B

4.14
3.78
3.28
3.26
3.04
2.81

4.48
4.10
3.98
3.62
3.42
2.94

3.98
3.42
3.14
3.02
2.52
2.23

3.44
3.16
3.12
2.48
2.64
2.30

4.18
3.46
3.12
2.76
1.86
1.66

4.04
3.58
3.33
3.03
2.70
2.39

Dual Agent
GPT-4.1
GPT-5.4
Gemini Flash
Llama-70B
DeepSeek
Qwen-14B

3.66
3.34
2.94
3.10
3.10
2.92

3.48
3.00
3.22
2.54
2.76
2.31

3.18
2.96
2.54
2.40
2.40
2.24

3.46
3.64
3.10
3.08
3.04
2.86

3.04
2.76
2.44
1.92
1.38
1.53

3.36
3.14
2.85
2.61
2.54
2.37

4.1.4

Output accuracy and composite scores (L3)

Fig. 8 provides a per-task breakdown of L3 output accuracy scores across SA mode (mean over
three runs). The heatmap retains a bimodal pattern: most tasks cluster near 0.5–1.0 or near 0,
with few intermediate values, indicating that task success is largely binary once threshold quality
is achieved. A quality-aware composite is therefore essential: many failed tasks complete more
than 70% of the required pipeline (correct spatial joins, Moran’s I computation, or GWR fitting),
yet binary pass/fail scoring cannot capture this partial progress. The vision-based L3 evaluator
(Section 3) further enforces a strict cartographic standard: 33% of SA visualizations and 58%
of DA visualizations receive task-completion scores ≤ 2, even when the underlying analytical
pipeline ran to completion—typically due to missing legends, incorrect colour ramps, or extents
that omit the gold-standard area of interest. This strict cartographic gate is the principal driver
of the per-task Qout values in Table 6 sitting well below the corresponding success rates. The
composite scores in Table 6 integrate all evaluation layers. Gemini-3-Flash narrowly leads SA
composite (0.7646), with DeepSeek-V3.2 a close second (0.7612); both maintain similar profiles
in DA mode but at 5–15 percentage-point lower composite values. GPT-5.4 holds the lead in
DA mode (0.7052), reflecting the planner-friendly nature of its longer-context reasoning.

18

## Page 19

Figure 8: L3: Per-task output accuracy scores (SA, averaged over three runs). Green = high
accuracy; red = failure. Tasks T18 and T27 remain red across most models, indicating intrinsic
difficulty.

Figure 9: Multi-dimensional performance profiles for SA (left) and DA (right) architectures.
In SA mode, Gemini Flash and DeepSeek lead the four-dimensional composite; in DA mode,
GPT-class models hold the highest composite but with compressed dimension ranges across all
six backends.

19

## Page 20

4.1.5

Run-to-run variance: the case for repeated runs

A central methodological finding from the 1,800-experiment grid is that single-run task scores
are surprisingly noisy, even for flagship models on tasks that are within their capability envelope.
The clearest example is T20 (mineral deposit prospectivity prediction), where DeepSeek-V3.2 in
SA mode produces task-completion vision scores of 1, 3, and 5 across the three runs—spanning
the full failure-to-success range while every other strong model on T20 scores 5/5/5 deterministically. Any single execution of T20 would therefore class DeepSeek as either an unambiguous
failure or an unambiguous success depending purely on the random branch sampled, and identical single-run instability appears at smaller magnitudes on 9 further tasks. Aggregated across
50 tasks, this run-to-run noise tightens the bootstrap CIs in Table 6 to ±0.02–0.05, but cell-level
conclusions drawn from any single execution can shift by similar margins in either direction.
The three-run protocol is therefore not a cosmetic statistical addition; it is a precondition for
stable architecture- and model-level rankings, and we recommend it as a baseline requirement
for future GIS-agent benchmarking.
4.1.6

Effect of optional workflow hints

Throughout the main evaluation we supply each task with the high-level workflow outline that
the benchmark provides; this represents the typical use case in which a domain expert sketches
the analytical decomposition for the agent. To check how much this optional hint actually
moves the needle—and how the system performs when no such hint is available—we run a paired
ablation on DeepSeek-V3.2 SA across all 50 benchmark tasks, with vs. without the workflow
string injected into the prompt (all other configuration held identical). Table 10 reports the
result. End-to-end task success is essentially unchanged (47/50 with workflow, 48/50 without):
the system reaches the analytical end of nearly every task either way. The composite score,
which additionally weighs output quality and process alignment, shows a moderate improvement
when the workflow is supplied (mean ∆ = +0.114, median ∆ = +0.153, Cohen’s d = +0.51,
paired Wilcoxon p < 10−3 )—driven by tasks where the workflow helps the model select the
expert-aligned analytical decomposition over plausible alternatives. The takeaway is two-sided:
an expert-supplied workflow is a useful but optional input that moderately sharpens the agent’s
outputs, and the system itself is robust enough to perform realistic GIS analysis even without
one.
Table 10: Workflow ablation: DeepSeek-V3.2 SA across all 50 benchmark tasks, paired by task
(n = 50). Composite scores follow Eq. 1. The with-workflow condition delivers a statistically
significant medium-sized improvement.
Condition
With workflow
Without workflow

Scomp mean

std

successes

0.733
0.619

0.196
0.180

47/50
48/50

Mean per-task ∆ (with − without) = +0.114; median ∆ = +0.153.
Paired Wilcoxon p < 10−3 ; Cohen’s d = +0.51 (medium effect).

20

## Page 21

Figure 10: Per-task workflow ablation across all 50 tasks (DeepSeek-V3.2 SA). Top: paired
with −
composite scores with vs. without workflow. Bottom: signed per-task difference ∆ = Scomp
without (slate = with-workflow wins, warm = without wins); the dashed line marks the mean
Scomp
∆ = +0.114. The majority of tasks favour the with-workflow condition, with a small minority
of reversals—most prominently T41, where the supplied workflow encodes a constraint that
mismatches the model’s preferred decomposition—outweighed by the consistent positive effect
on multi-step pipelines.

4.2

Case Studies

We present three categories of case studies that illuminate the interaction between model capability, domain knowledge, and system design.
4.2.1

Exceptional performance on complex tasks—and run-to-run instability

T20 — Mineral deposit prospectivity prediction. This task requires a complete machine
learning pipeline: loading 11 geological raster layers (geochemistry, geophysics, lithology, structure), extracting pixel-level features, training a Random Forest classifier on known tin-tungsten
deposit locations, generating a full-resolution probability map, and visualizing the prospectivity surface. The pipeline spans raster I/O, nodata handling, feature matrix construction,
scikit-learn model fitting, pixel-wise prediction, and georeferenced output—a representative
end-to-end ML-driven geospatial workflow. As shown in Fig. 11, four cloud models (GPT-4.1,
GPT-5.4, DeepSeek-V3.2, Gemini-3-Flash) produce prospectivity maps that faithfully reproduce the spatial pattern of the gold standard, with high-probability zones correctly localized
around known deposit clusters; Llama-3.3-70B generates a uniform single-color raster (complete pipeline failure), and Qwen-14B fails to produce a visualization. GPT-5.4 additionally
reports a model AUC of 0.922 and overlays known deposit points, while DeepSeek annotates
the coordinate reference system (GDA94 / MGA zone 55).
Critically, T20 also exposes the run-to-run instability discussed in Section 4.1.5: the L3
vision task-completion score for DeepSeek SA on T20 is 1, 3, 5 across the three repeated runs,
21

## Page 22

whereas GPT-5.4 and GPT-4.1 score 5/5/5 deterministically. T20 is therefore simultaneously a
positive case (strong models can orchestrate multi-step ML pipelines without explicit procedural
guidance) and a cautionary case (high-temperature creative branches in flagship models occasionally redirect the pipeline through subtly wrong feature matrices), and is the single clearest
empirical motivation for the repeated-run protocol. T34 — Japan rural road accessibility

Figure 11: T20: Mineral deposit prospectivity prediction outputs (SA mode). Four strong
models accurately reproduce the spatial distribution of tin-tungsten prospectivity, while Llama70B generates a uniform raster and Qwen-14B fails to produce any visualization. This task
requires a complete ML pipeline spanning raster feature extraction, Random Forest training,
and georeferenced probability mapping.
analysis. This multi-step GIS pipeline requires rural area extraction, road buffer construction, population ratio computation, and choropleth visualization. Four models score above
0.92, with DeepSeek and Gemini achieving perfect scores (1.00). Fig. 12 shows that successful
outputs faithfully reconstruct the spatial accessibility pattern across Japan’s prefectures.

22

## Page 23

Figure 12: T34: Road accessibility visualization outputs. Top models accurately identify and
render prefecture-level accessibility patterns across Japan.

23

## Page 24

4.2.2

Parametric domain knowledge gaps

T07 — Land subsidence flood analysis. This task exposes a critical limitation: the gold
standard uses a flood depth threshold of ≤ −200 cm, which encodes domain knowledge about
projected future sea level rise. All six models instead use the naive threshold elevation <
0, producing outputs that appear correct but significantly overestimate flood extent. Moreover, several models incorrectly hardcode the CRS as EPSG:4326 instead of the data’s native
EPSG:28992, causing the overlay operation to fail silently and producing near-blank visualizations (Fig. 13). T08 — Fire station coverage gap analysis. Similarly, the gold standard

Figure 13: T07: Flood analysis outputs illustrating domain knowledge gaps. The Gold Standard (left) uses a domain-calibrated −200 cm threshold, while all models default to 0 cm. Some
models further suffer CRS misalignment, producing blank maps. This demonstrates that parametric domain knowledge cannot be acquired from code patterns alone.
specifies a 2,500 m service buffer based on fire response time standards, while models select arbitrary values (500–1,000 m), producing “no-service” areas that are 3–5× larger than the reference
(Fig. 14).
These cases reveal a qualitative distinction that RAG-based systems cannot resolve: while
RAG can supply library documentation, it cannot impart fundamental conceptual domain
knowledge (e.g., flood depth = sea level − terrain elevation) or parametric thresholds (e.g.,
fire-response buffer distances) that human analysts acquire through professional experience.
This “conceptual knowledge gap” represents a distinct failure mode from the “API knowledge
gap” that retrieval-augmented systems were designed to address.

24

## Page 25

Figure 14: T08: Fire station coverage gap analysis. The Gold Standard (top-left) uses a 2,500 m
buffer; all models select smaller radii (500–1,000 m), dramatically overestimating the uncovered
area. This illustrates the parametric domain knowledge gap.

25

## Page 26

4.2.3

Infrastructure vs. model capability

T18 — Quadtree density visualization. All models correctly identify geoplot.quadtree()
as the appropriate function, but a compatibility issue between geoplot 0.5.1 and the installed
pyproj version causes universal failure. This case demonstrates that some “model failures”
are actually environmental limitations, underscoring the importance of infrastructure design
described in the next section.

4.3

Design Lessons

Our 1,800-experiment evaluation and iterative development process yield several engineering
principles that extend beyond benchmark scores.
4.3.1

Infrastructure dominates model capability

The primary bottleneck for GIS agent success is infrastructure-level system design, not
model reasoning ability. Through iterative failure diagnosis during system development, we resolved four categories of environment-level bugs (Table 11), improving intermediate-task success
from 20% to 80%—a 400% increase—while simple and complex tasks remained unchanged. This
demonstrates that the design bottleneck lies at the interface between model output
and execution environment.
Table 11: Infrastructure-level fixes and their impact on task success.
Category

Failure
tom

Symp-

Fix Applied

Data
Pathing

dataset
Nested
SHP Flatten
files
cause structure
FileNotFoundError

API State

rasterio.open()
returns
reader
object; agent calls
.astype()

Return
raw
ndarray + metadata dict

Memory

City-wide
grids
exceed 104 cells;
overlay OOM

Enforce grid-size
templates

Type Coercion

String-encoded
numerics fail during interpolation

Auto-cast
with
pd.to numeric

Beyond bug fixes, tool layers can introduce silent semantic mismatches. In T36 (SAVI
computation), a load raster helper returned a 2D array instead of a 3D (B, H, W ) array; the
agent interpreted data[3] as a spectral band but retrieved a pixel row—producing wrong values
with no exception. GPT-5.4 spent 35 rounds diagnosing “wrong values” without locating the
root cause; after fixing the interface, the same model succeeded in 3 rounds.
Two additional behavioral failures emerged: (1) in T06, Qwen-14B called plt.show() instead of plt.savefig(), producing empty outputs—a single prompt rule resolved it (score:
3.5→7.8); (2) across 50 tasks, 8 failures (16%) stemmed from file-name case “auto-correction”
26

## Page 27

on case-sensitive Linux, eliminated by the Schema Analysis rule mandating list files() as
the first action.
4.3.2

Hard constraints outperform prompt-level guidance

Small models exhibit frustration-induced constraint collapse: after repeated failures, they abandon prompt constraints and revert to pre-training defaults. In T26 (groundwater mapping),
Qwen-14B attempted import arcpy at round 17 despite explicit prohibition.

Comparing

three strategies: prompt-only (blocked at round 17), prompt+deduplication (blocked earlier
at round 10), and prompt+sandbox-level import interception (zero violations, full completion).
The lesson: sandbox-level enforcement is a necessary complement to prompt-level
constraints for resource-constrained models.
A related finding: code deduplication prevents “progress amnesia” loops (e.g., T25: 8×
identical submissions) but can prematurely terminate legitimate retries of slow operations (e.g.,
T28: GridSearchCV timeouts), suggesting that context-aware deduplication is a worthwhile
future direction.
4.3.3

Two failure modes of self-correction

Our analysis reveals two distinct self-correction failures. Type A (Conceptual): the model lacks
domain knowledge—in T33, it repeatedly applies the wrong flood-depth formula because the
error is conceptual, not syntactic. Type B (Attentional): the model correctly diagnoses the issue
but fails to apply the fix—in T34, print() revealed ’RURAL’ but the next submission still used
’Rural’. Type A requires domain knowledge injection with physical parameter specifications;
Type B may benefit from explicit memory prompting that foregrounds extracted values.
A related failure is task instruction ambiguity: in T25, “create risk maps” was interpreted as GeoJSON export rather than PNG visualization—a GIS-specific semantic convention
that models cannot infer without explicit output-format contracts.
4.3.4

Local deployment viability and model selection

Averaged across three runs, Qwen2.5-Coder-14B on a single RTX 3090 achieves 52% end-to-end
success in SA mode with output quality Qout = 0.549, comparable to GPT-4.1’s 0.601 and well
above Llama-3.3-70B’s 0.398. Counter-intuitively, Llama-70B—with 5× more parameters—
scores lower on the SA composite (0.656 vs. Qwen-14B’s 0.454 once success rate is included, but
with much weaker output quality), revealing a comprehension–execution gap: high embedding
similarity (0.614) but persistently low output quality. Equally striking, switching Qwen2.5Coder-14B from SA to DA mode lifts mean success from 52% to 79% (+27 pp) and composite
from 0.454 to 0.588, the only such gain across the six backends. For local deployment,
code-specialized fine-tuning is more impactful than parameter scaling, and the additional planner scaffolding is most valuable precisely where single-shot reasoning
is weakest.
Qualitative analysis shows that Qwen-14B failures concentrate in the final output assembly
stage, not in core GIS reasoning. In T34, T01, and T20, the model correctly executed spatial

27

## Page 28

joins, Kriging preparation, and Random Forest training, but failed at visualization or GeoTIFF
reassembly. This suggests a human-in-the-loop paradigm where the agent handles analytical
stages (estimated >80% completion) while the expert validates at key transitions—a pragmatic
path to capable geospatial AI on consumer hardware.

5

Discussion and Limitations

Scope of agent autonomy. Each task in the main benchmark is accompanied by an optional
high-level workflow outline (a short ordered list of analytical steps such as interpolate temperatures, then filter senior population, then aggregate to census blocks). The workflow specifies
neither code, function names, parameter values, coordinate systems, nor output formats; the
agent is responsible for translating the natural-language description into executable Python,
handling all data realities (column names, CRS, missing values), recovering from runtime errors, and producing the final analytical outputs. We use this hint by default because it is what
a real GIS analyst would typically supply when delegating an analysis, and not because the
system requires it: the controlled ablation in Section 4.1.6 shows that removing the workflow
on a strong cloud backend leaves task success essentially unchanged (48/50 vs. 47/50), with
only a moderate composite-score reduction (∆ = −0.114, d = −0.51) attributable to looser
alignment with the expert decomposition. GISclaw should therefore be read as a system that
performs realistic GIS analysis in a setting that mirrors how human analysts actually use such
systems—with a brief expert sketch when one is available, and with self-directed decomposition
when one is not—rather than as a claim of fully autonomous geospatial reasoning.
Statistical scope. Each (model, architecture, task) combination in the main comparison
was executed three times under identical sampling configurations, yielding n = 150 paired
task-runs per (model, architecture) cell; we report means with 95% confidence intervals computed by the percentile bootstrap (typical CI half-width ±0.02–0.05 on the composite score).
Architecture-level comparisons are tested with task-level paired Wilcoxon signed-rank tests
(Table 7), and effect sizes are reported using Cliff’s δ. We additionally conduct a sensitivity
analysis sweeping all 66 admissible weight tuples on the composite-score simplex, confirming
that the multi-architecture and multi-model conclusions are not artefacts of any specific weight
choice (median Kendall’s τ = 0.94 vs. the default weights). Despite these safeguards, three
runs per setting remain a moderate sample, and broader claims about absolute success rates—
particularly in the long tail of difficult tasks—should be read with the reported uncertainties
in mind. The optional-workflow ablation in Section 4.1.6 covers DeepSeek-V3.2 SA on all 50
benchmark tasks; extending the same ablation across the remaining five backends is a natural
follow-up.
Generalisation beyond GeoAnalystBench. GeoAnalystBench contains 50 expertcurated tasks spanning seven analytical categories. While these tasks cover the major modalities
(vector, raster, tabular) and a range of difficulty, they are predominantly drawn from urban analytics, environmental hazard, and resource-planning domains. Performance on tasks demanding
very large raster processing (>10 GB), real-time spatial data streams, multi-user collaborative
analysis, or deeply specialised sub-domains (e.g. marine acoustics, atmospheric chemistry) is not

28

## Page 29

assessed here, and the qualitative findings around dual-agent degradation and infrastructurebound failure modes should be re-validated in those settings before being relied upon.
Model availability and reproducibility. Several of the cloud models evaluated in this
work—most notably the Gemini 3 Flash preview—are vendor-managed services whose underlying weights, sampling defaults, and quotas may change without notice. We document exact
model identifiers, prompt templates, and sandbox configurations to maximise reproducibility,
but exact replication of cloud results may become infeasible as services evolve. The open-weight
component of our evaluation (Qwen2.5-Coder-14B, Llama-3.3-70B) is fully reproducible from
public artefacts.
Cost and ergonomics. Strong cloud models incur non-trivial inference cost (GPT-5.4 at
approximately $8.50 per full benchmark sweep), making large-scale repeated evaluation expensive. The 14B open-weight tier mitigates this for routine use, but at the cost of slower per-task
wall time and lower performance on the most complex tasks. A practical pipeline therefore likely
combines cheap open-weight models for routine workflows with selective routing to a stronger
cloud model for tasks that the agent or its evaluator flags as ambiguous.

6

Conclusion

We presented GISclaw, a comprehensive open-source LLM agent system that performs realistic, multi-step GIS analysis—kriging-based hot-spot mapping, Random-Forest mineral prospectivity prediction, multi-criteria wildlife corridor optimization, network-based isochrones, full
publication-quality cartography—directly through the open-source Python ecosystem, with no
dependency on any commercial GIS software. By grounding agent behaviour in a persistent
Python sandbox, three engineered prompt rules (Schema Analysis, Package Constraint, optional Domain Knowledge Injection), and an Error-Memory module for self-correction, GISclaw
reaches up to 100% task success on GeoAnalystBench (mean 97% over three independent
runs for the leading SA backends) across the full range of vector, raster, and tabular workflows
that prior LLM-driven GIS systems do not jointly support.
Realistic GIS analysis without proprietary GIS. GISclaw demonstrates that the spectrum of professional analytical pipelines normally addressed with ArcGIS or QGIS—spatial
overlays, raster algebra, geostatistical interpolation, machine-learning classification, network
analysis, multi-layer cartography—can be performed end to end on the open-source Python
stack alone, when paired with an appropriately engineered LLM agent. The benchmark used
here, GeoAnalystBench, is itself a deliberate stress test: tasks average 5.8 analytical steps,
span all three data modalities, and were authored by domain experts rather than synthesised
from tool-call templates, which makes the headline success rates a meaningful indicator of system capability rather than of benchmark gaming. The system, the prompt templates, and our
open-source-rewritten gold-standard solutions for all 50 tasks are released under MIT licence to
support direct use, replication, and extension.
Methodological findings. The 1,800-experiment evaluation grid supports two methodological points that we believe will be useful to the broader GIS-agent community. First, per-task
scoring exhibits non-trivial run-to-run variance even for flagship models (a single execution of

29

## Page 30

T20 can score 1, 3, or 5 on visual task completion across runs of an otherwise stable strong
model), so a repeated-run protocol with confidence intervals and paired tests should be a default
for GIS-agent benchmarking rather than an optional extra. Second, within GISclaw’s identical
infrastructure the Single-Agent ReAct loop reliably outperforms the Dual-Agent Plan-ExecuteReplan pipeline on every cloud backend (paired Wilcoxon p < 10−3 , Cliff’s δ = 0.21–0.41), with
only the locally deployed 14B model gaining from multi-agent orchestration; the implication
is that architectural complexity should be matched to model capability rather than added by
default.
Infrastructure as the primary bottleneck. Our iterative failure diagnosis reveals that
the performance ceiling for GIS agents is set not by model reasoning quality but by infrastructure
design. Resolving four categories of environment-level bugs—data pathing, API state management, memory limits, and type coercion—produced a 400% improvement in intermediate-task
success. Additional failure modes at the behavioral layer—visualization output format, filename guessing, and code deduplication side effects—further demonstrate that a system’s engineering quality is a first-class determinant of agent performance, independent of the underlying
model.
The knowledge gap hierarchy. Our evaluation identifies a hierarchy of knowledge gaps
that GIS agents face. The API knowledge gap—unfamiliarity with specific library calls—is
addressable through prompt engineering and retrieval augmentation. The parametric knowledge
gap—domain-calibrated thresholds such as flood depth cutoffs and fire-station buffer radii—is
not recoverable from code corpora and produces “false positive” outputs that appear plausible
but are analytically incorrect. The conceptual knowledge gap—physical relationships such as
flood depth = −(elevation + 200), and GIS-specific semantic conventions such as “create maps”
implying PNG visualization and not GeoJSON export—lies beyond what any retrieval system
can supply and calls for expert-in-the-loop validation or output format contracts baked into
domain knowledge injection.
Local deployment and human-in-the-loop pathways. Averaged across three repeated
runs, Qwen2.5-Coder-14B on a single consumer RTX 3090 achieves 52% end-to-end task success
in SA mode (rising to 79% in DA mode) at zero marginal cost, with output quality among
successful tasks (Qout = 0.549) comparable to GPT-4.1 (0.601). Qualitative analysis shows
that failures concentrate in final output assembly rather than in core GIS reasoning or spatial
computation—indicating that the gap between 14B models and full autonomy is narrower than
aggregate metrics suggest. For deployments where cloud APIs are unavailable, a human-inthe-loop collaborative mode—agent handles pipeline stages autonomously while the domain
expert validates at key transitions—offers a pragmatic path to capable geospatial AI without
proprietary infrastructure.
Future directions. Near-term priorities include extending GISclaw toward real-time geospatial data streams, incorporating context-aware deduplication, and adapting agent frameworks
for reasoning-specialized models that require expanded token budgets. Longer-term, the conceptual and parametric knowledge gaps identified in this work motivate hybrid architectures
coupling LLM code generation with domain knowledge bases that encode field-specific physical models and calibrated parameter ranges—advancing GIS agents from syntactic proficiency

30

## Page 31

toward genuine geoscientific reasoning.

Acknowledgements
This study was supported by a grant from the National Research Foundation, Korea (NRF),
funded by the Korean government (MSIT) (RS-2026-25474388). This research was supported by
the 2023-MOIS36-004 (RS-2023-00248092) of the Technology Development Program on Disaster
Restoration Capacity Building and Strengthening funded by the Ministry of Interior and Safety
(MOIS, Korea).

Data Availability
GISclaw, including all source code, evaluation scripts, and benchmark results, is publicly available at: https://github.com/geumjin99/GISclaw.

References
Temitope Akinboyewa, Zhenlong Li, Huan Ning, and M Naser Lessani. Gis copilot: Towards
an autonomous gis agent for spatial analysis. International Journal of Digital Earth, 18(1):
2497489, 2025.
Jeffrey A Cardille, Renee Johnston, Simon Ilyushchenko, Johan Kartiwa, Zahra Shamsi,
Matthew Abraham, Khashayar Azad, Kainath Ahmed, Emma Bergeron Quick, Nuala
Caughie, et al. The cloud-based geospatial benchmark: Challenges and llm evaluation. In
TerraBytes-ICML 2025 workshop, 2025.
Guanyu Chen, Haoyue Jiao, Shuyang Hou, Ziqi Liu, Lutong Xie, Shaowen Wu, Huayi Wu,
Xuefeng Guan, and Zhipeng Gui. GeoJSEval: An Automated Evaluation Framework for
Large Language Models on JavaScript-Based Geospatial Computation and Visualization Code
Generation. ISPRS International Journal of Geo-Information, 14(10):382, sep 2025. ISSN
2220-9964. doi: 10.3390/ijgi14100382. URL https://www.mdpi.com/2220-9964/14/10/382.
Yu Feng, Puzhen Zhang, Guohui Xiao, Linfang Ding, and Liqiu Meng. Towards a barrier-free
GeoQA portal: Natural language interaction with geospatial data using multi-agent LLMs and
semantic search. International Journal of Applied Earth Observation and Geoinformation,
144:104825, nov 2025. ISSN 15698432. doi: 10.1016/j.jag.2025.104825. URL https://
linkinghub.elsevier.com/retrieve/pii/S1569843225004728.
Piotr Gramacki, Bruno Martins, and Piotr Szymański. Evaluation of code llms on geospatial
code generation. pages 54–62, 2024.
Shuyang Hou, Zhangxiao Shen, Jianyuan Liang, Haoyue Jiao, Anqi Zhao, Yaxian Qing, Dehua
Peng, Zhipeng Gui, Xuefeng Guan, Longgang Xiang, et al. Can large language models
generate geospatial code? Geo-Spatial Information Science, pages 1–35, 2025a.

31

## Page 32

Shuyang Hou, Zhangxiao Shen, Anqi Zhao, Jianyuan Liang, Zhipeng Gui, Xuefeng Guan, Rui
Li, and Huayi Wu. GeoCode-GPT: A large language model for geospatial code generation. International Journal of Applied Earth Observation and Geoinformation, 138:104456,
apr 2025b. ISSN 15698432. doi: 10.1016/j.jag.2025.104456. URL https://linkinghub.
elsevier.com/retrieve/pii/S1569843225001037.
Varvara Krechetova and Denis Kochedykov. Geobenchx: Benchmarking llms in agent solving
multistep geospatial tasks. pages 27–35, 2025.
Zhenlong Li and Huan Ning. Autonomous gis: the next-generation ai-powered gis. International
Journal of Digital Earth, 16(2):4668–4686, 2023.
Zhenlong Li, Huan Ning, Song Gao, Krzysztof Janowicz, Wenwen Li, Samantha T Arundel,
Chaowei Yang, Budhendra Bhaduri, Shaowen Wang, A-Xing Zhu, et al. Giscience in the era
of artificial intelligence: A research agenda towards autonomous gis. Annals of GIS, 31(4):
501–536, 2025.
Chao Liang, Yuanzheng Cui, Run Shi, Guixiang Zha, Xin Yin, Mingzhong Xiao, Dong Xu,
Xuejun Duan, and Bo Huang. GeoAgentic-RAG: A Multi-Agent framework for autonomous
geospatial reasoning and visual insight generation with LLM.

International Journal of

Applied Earth Observation and Geoinformation, 147:105195, mar 2026. ISSN 15698432.
doi: 10.1016/j.jag.2026.105195. URL https://linkinghub.elsevier.com/retrieve/pii/
S1569843226001111.
Qianqian Luo, Qingming Lin, Liuchang Xu, Sensen Wu, Ruichen Mao, Chao Wang, Hailin Feng,
Bo Huang, and Zhenhong Du. Geojson agents: a multi-agent llm architecture for geospatial
analysis—function calling vs. code generation. Big Earth Data, pages 1–55, 2026.
Huan Ning, Zhenlong Li, Temitope Akinboyewa, and M. Naser Lessani. An autonomous GIS
agent framework for geospatial data retrieval. International Journal of Digital Earth, 18(1):
2458688, aug 2025. ISSN 1753-8947, 1753-8955. doi: 10.1080/17538947.2025.2458688. URL
https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2458688.
Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. Bleu: a method for automatic evaluation of machine translation. In Proceedings of the 40th annual meeting of the
Association for Computational Linguistics, pages 311–318, 2002.
Nils Reimers and Iryna Gurevych. Sentence-BERT: Sentence embeddings using Siamese BERTnetworks. arXiv preprint arXiv:1908.10084, 2019.
Shuo Ren, Daya Guo, Shuai Lu, Long Zhou, Shujie Liu, Duyu Tang, Neel Sundaresan, Ming
Zhou, Ambrosio Blanco, and Shuai Ma. CodeBLEU: a method for automatic evaluation of
code synthesis. arXiv preprint arXiv:2009.10297, 2020.
Chenzhen SUN, Tian LAN, Zhiwei WU, Xing SHI, Donglin CHENG, and Songlin JIANG.
Generative artificial intelligence and its applications in cartography and gis: An exploratory
review. Journal of Geodesy and Geoinformation Science, 8(2):74–89, 2025.
32

## Page 33

Huayi Wu, Haoyue Jiao, Shuyang Hou, Jianyuan Liang, Zhangxiao Shen, Anqi Zhao, Yaxian
Qing, Fengying Jin, Xuefeng Guan, and Zhipeng Gui. Geocolab: an llm-based multi-agent collaborative framework for geospatial code generation. International Journal of Digital Earth,
18(2):2569405, 2025.
Liuchang Xu, Shuo Zhao, Qingming Lin, Luyao Chen, Qianqian Luo, Sensen Wu, Xinyue Ye,
Hailin Feng, and Zhenhong Du. Evaluating large language models on geospatial tasks: a
multiple geospatial task benchmarking study. International Journal of Digital Earth, 18(1):
2480268, aug 2025. ISSN 1753-8947, 1753-8955. doi: 10.1080/17538947.2025.2480268. URL
https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2480268.
Jonghyeon Yang and Jiyoung Kim. Geospatial Knowledge-Base Question Answering Using
Multi-Agent Systems. ISPRS International Journal of Geo-Information, 15(1):35, jan 2026.
ISSN 2220-9964. doi: 10.3390/ijgi15010035. URL https://www.mdpi.com/2220-9964/15/
1/35.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and
Yuan Cao. React: Synergizing reasoning and acting in language models. In The eleventh
international conference on learning representations, 2022.
Qianheng Zhang, Song Gao, Chen Wei, Yibo Zhao, Ying Nie, Ziru Chen, Shijie Chen, Yu Su,
and Huan Sun. Geoanalystbench: A geoai benchmark for assessing large language models for
spatial analysis workflow and code generation. Transactions in GIS, 29(7):e70135, 2025a.
Yifan Zhang, Cheng Wei, Shangyou Wu, Zhengting He, and Wenhao Yu.

Geogpt: Un-

derstanding and processing geospatial tasks through an autonomous gpt. arXiv preprint
arXiv:2307.07930, 2023.
Yifan Zhang, Jingxuan Li, Zhiyun Wang, Zhengting He, Qingfeng Guan, Jianfeng Lin, and
Wenhao Yu. Geospatial large language model trained with a simulated environment for
generating tool-use chains autonomously. International Journal of Applied Earth Observation
and Geoinformation, 136:104312, 2025b.
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang,
Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and
chatbot arena. Advances in neural information processing systems, 36:46595–46623, 2023.

33
