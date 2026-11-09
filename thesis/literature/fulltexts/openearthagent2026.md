---
id: literature/fulltexts/openearthagent2026
type: fulltext
status: frozen
language: en
key: openearthagent2026
title: >-
  OpenEarthAgent: A Unified Framework for Tool-Augmented Geospatial Agents
resource: https://arxiv.org/abs/2602.17665
description: >-
  Recent progress in multimodal reasoning has enabled agents that interpret imagery, connect it with language, and execute structured analytical tasks.
pages: 39
words: 15987
year: 2026
venue: >-
  
authors: >-
  Shabbir, Akashah; Sheikh, Muhammad Umer; Munir, Muhammad Akhtar; Debary, Hiyam; Fiaz, Mustansar; Zaheer, Muhammad Zaigham; Fraccaro, Paolo; Khan, Fahad Shahbaz; Khan, Muhammad Haris; Zhu, Xiao Xiang; Khan, Salman
doi: 
oa_status: arxiv 2602.17665
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# OpenEarthAgent: A Unified Framework for Tool-Augmented Geospatial Agents

## Page 1

OpenEarthAgent
: A Unified Framework for
Tool-Augmented Geospatial Agents
Akashah Shabbir1⋆ , Muhammad Umer Sheikh1⋆ , Muhammad Akhtar Munir1 ,
Hiyam Debary2 , Mustansar Fiaz2 , Muhammad Zaigham Zaheer1 , Paolo Fraccaro2 ,
Fahad Shahbaz Khan1,3 , Muhammad Haris Khan1 , Xiao Xiang Zhu4 , and
Salman Khan1,5

arXiv:2602.17665v4 [cs.CV] 12 Jul 2026

1

Mohamed bin Zayed University of AI, United Arab Emirates
2
IBM Research, Europe
3
Linköping University, Sweden
4
Technical University Munich, Germany
5
Australian National University, Australia
https://github.com/mbzuai-oryx/OpenEarthAgent

Visualize all museums
and malls over the given
GeoTIFF image, compute
the distance between the
closest pair, and finally
annotate the image with
this distance.

OpenEarthAgent- 4B

Qwen3-4B

Step 1: Formulate a high-level plan

Step 1: Formulate a high-level plan

To answer this, I'll extract the bounding box from the GeoTIFF, create an
area boundary GeoPackage, add museum and mall POIs, compute the
closest distance between them using top=1, render all layers over the
GeoTIFF, and finally annotate the rendered image with the distance value.
Step 2: Extract the bbox from the GeoTIFF
N GetBboxFromGeotiff P Geotiff

R

Bbox (W,S,E,N)

Step 3: Create an area boundary GPKG from this bbox
N GetAreaBoundary
P Area: Bbox

R

GPKG saved

First, I need to retrieve the area boundary from the given
GeoTIFF to establish the region of interest. Then, I will add
museums and malls as POIs within this boundary. After that,
I will compute the distance between the closest pair of these
points. Finally, I will annotate the image with this distance.
Step 2: Extract the area boundary from Geotiff
N
P

Step 4: Add POIs for museums.
N AddPoisLayer

P

GPKG, {"tourism": "museum"} R Saved 1 POIs

Step 5: Add POIs for malls.
N AddPoisLayer

P

GPKG, {" shop ": " mall "}

R

Saved 1 POIs

Step 6: Compute Distance between museums and closest malls.
N ComputeDistance
P GPKG, museums,malls

R

Dist. saved

Step 7: Render the layers directly on top of the GeoTIFF
N DisplayOnGeotiff
P GPKG, layers, geotiff

R

out.tif saved

Step 8: Annotate the rendered map.
N AddText
P Image, text, position

R

out.tif annotated

Step 9: Annotated image saved.
N Terminate
P

Ans: <image>

GetAreaBoundary
area: from GeoTIFF,
buffer_m: 0

P

Error: Nominatim geocoder
returned 0 results for query
'from GeoTIFF'.

Wrong primitive for area: from GeoTIFF

Step 3: Terminated
N

R

Terminate
Since no valid boundary could be derived, it is not
possible to proceed
•
•

Skipped the necessary step: extract Bbox
from GeoTIFF
Premature termination instead of
recovery

N Tool Name P Tool Parameters

R

Tool Response

Fig. 1: Comparison of OpenEarthAgent-4B and Qwen3-4B on a complex GIS reasoning
task. OpenEarthAgent correctly sequences tool calls with proper dependencies and
feedback, while Qwen3 fails due to misordered tool usage and inconsistent reasoning.
Abstract. Recent progress in multimodal reasoning has enabled agents
that interpret imagery, connect it with language, and execute structured analytical tasks. Extending these capabilities to remote sensing
remains challenging, as models must reason over spatial scale, geographic
structures, and multispectral indices while maintaining coherent multistep logic. To address this gap, we introduce OpenEarthAgent, a unified
framework for tool-augmented geospatial reasoning trained on satellite
imagery, natural-language queries, and structured reasoning traces. Beyond serving as a benchmark, OpenEarthAgent establishes a cohesive
agentic architecture built around a unified executable tool registry and
trajectory-based policy learning. The framework standardizes heterogeneous visual, spectral, GIS, and georeferenced raster operations under
⋆

Equal contribution.

## Page 2

2

A. Shabbir et al.
a consistent callable schema, enabling modular orchestration and deterministic execution. Training is performed via supervised fine-tuning on
structured reasoning trajectories with deterministic replay validation to
ensure executability and spatial correctness. The accompanying corpus
comprises 14,538 training and 1,169 evaluation instances with over 107K
reasoning steps, spanning urban, environmental, disaster, and infrastructure domains and incorporating GIS operations alongside index analyses
such as NDVI, NBR, and NDBI. Grounded in explicit reasoning traces,
the learned agent demonstrates structured reasoning, stable spatial understanding, and interpretable tool-driven behavior across diverse EO
scenarios. We report consistent improvements over a strong baseline and
competitive performance against recent open and closed-source models.

1

Introduction

The evolution of visual representation learning has transitioned from static perception to interactive multimodal reasoning. Early single-shot frameworks such
as DINO [4] and MAE [14] laid the foundation for large-scale visual understanding through self-supervised objectives, learning strong image encoders without
explicit language-based reasoning or interaction. Inspired by these successes, the
remote sensing community extended this paradigm to earth observation, where
models such as Prithvi [17], Copernicus-FM [43], Galileo [39], Panopticon [40],
TerraFM [7], and AnySat [1] scaled representation learning to global multisensor
data. These earth-scale vision models demonstrated remarkable transfer across
spatial resolutions and modalities, yet their predictions remained one-shot and
perception-centric, focusing on recognition rather than structured reasoning.
In parallel, large multi-modal models have progressed beyond perception.
Architectures such as BLIP-2 [20], InstructBLIP [6], LLaVA-OneVision [19],
and Kosmos-2 [30] extended language models into the visual domain, enabling
grounded image understanding. Building on this trajectory, remote-sensing VLMs
emerged to adapt multimodal reasoning to geospatial data. Early efforts such
as RemoteCLIP [23], SkySenseGPT [25], and GeoChat [18] introduced largescale multimodal alignment for remote sensing through paired image–text and
instruction-following datasets. Recently, EarthDial [34] advanced this paradigm
by extending grounding across optical, SAR, thermal, and temporal modalities, enabling unified multimodal reasoning for classification, captioning, and
change analysis. Despite coupling language with perception, current remote sensing VLMs remain largely descriptive and lack explicit structured reasoning.
Subsequent reasoning-centric approaches such as ReAct [50], DeepSeek-R1
[11], and VLM-R1 [33] introduced structured planning and, in some cases, tooldriven reasoning, transforming static perception into organized multi-step task
execution. Recent developments such as OpenThinkIMG [36] unified these advances through multi-step vision-tool interaction, where large vision-language
models iteratively “think with images” through executable reasoning trajectories.
Inspired by these advances, efforts such as ThinkGeo [32] and Earth-Agent [8]
began exploring tool-augmented reasoning for earth observation (EO). They

## Page 3

OpenEarthAgent

3

demonstrate that large models can plan analytical chains but still face challenges in geospatial grounding, coordinate consistency, and physically verifiable
outputs. These limitations highlight the need for geographically grounded agents
that integrate perception with explicit and interpretable reasoning.
Building on this motivation, we construct a comprehensive agentic corpus and
training framework that integrates GIS layers, index-driven computations, and
multisensor imagery (optical and SAR) modalities to support a wide spectrum
of EO reasoning tasks. Our dataset comprises training image-query reasoningtraces, along with a held-out evaluation set designed to benchmark model consistency and reasoning performance. The data span diverse contexts, including
urban infrastructure, environmental monitoring, disaster assessment, land-use
mapping, and transportation analysis, and incorporate GIS operations (e.g.,
distance, area, zonal statistics) alongside index-based analyses such as NDVI,
NBR, and NDBI. Each sample provides an explicit reasoning trajectory linking
multiple tool calls, intermediate states, and outcomes, enabling agents to learn
structured, interpretable workflows rather than static predictions.
Central to this design is a unified tool registry that abstracts heterogeneous
geospatial operators through a standardized executable schema, enabling consistent orchestration across perception, GIS computation, spectral analysis, and
georeferenced raster reasoning. Unlike prior EO benchmarks that focus primarily on data scale, our contribution lies in coupling the dataset with an execution
engine and trajectory-based policy alignment. This integration ensures that reasoning steps are not only generated but deterministically validated for spatial
and logical consistency. To assess generalization and reasoning fidelity, we benchmark a broad suite of large and reasoning models, including the GPT family [27],
Qwen [49], InternLM [3], and other recent multimodal LLMs. Our dataset is constructed through a unified data-gathering pipeline, where each modality undergoes question synthesis and automated validation to ensure reasoning diversity,
spatial grounding, and cross-source consistency. This large-scale, tool-augmented
corpus bridges the divide between GIS analysis and remote-sensing perception,
providing a unified setting for evaluating structured geospatial reasoning. This
work introduces an agentic framework for remote sensing that integrates toolbased reasoning within a unified training and evaluation setup.
Specifically, our key contributions are:
– Unified data-construction pipeline: A systematic process integrating
multisensor imagery (RGB, SAR), GIS layers, and index-based computations
through question synthesis and automated validation.
– Agentic reasoning framework with deterministic validation: A unified tool registry and a trajectory-based supervised alignment mechanism
that enforces consistent tool syntax, executable reasoning chains, and spatially grounded decision-making (Fig. 1).
– Comprehensive multimodal corpus: 14,538 training instances and 1,169
evaluation tasks establishing a benchmark for studying spatial reasoning,
grounding, and interpretability across reasoning and non-reasoning models.

## Page 4

4

A. Shabbir et al.

2

Related Work

Remote sensing has progressed from task-specific models to large-scale foundation and vision-language models trained on global, multimodal data. Early
self-supervised methods [5, 26] established transferable pretraining strategies on
Sentinel archives. Subsequent foundation models include Prithvi-v2 [38] with
spatiotemporal transformers on HLS, Copernicus-FM [43] with metadata-aware
hypernetworks for Sentinel, Panopticon [40] and AnySat [1] with spectral- and
resolution-adaptive embeddings, and CROMA [9] fusing radar and optical contrastive learning. Galileo [39] captures global-to-local context, demonstrating
scalable pretraining across diverse sensors and geographies. On the multimodal
side, GeoChat [18] enabled language grounding to satellite imagery, and EarthDial [34] extended this paradigm to multi-resolution optical, SAR, thermal, and
temporal modalities across diverse tasks. Despite their scalability and representational strength, these models remain largely single-pass encoders; they lack
structured reasoning, tool orchestration, and verifiable intermediate analysis.
Alongside foundation models, agentic systems have emerged that couple reasoning with external tools and feedback-driven control. Early frameworks such
as ReAct [50] and Voyager [42] demonstrated the transition from static inference to autonomous, goal-directed reasoning. Subsequent systems, including WebAgent [45], VisTA [15], and DeepEyes [53], introduced modular architectures
capable of selecting and sequencing tools under guided supervision, improving
reasoning depth and execution consistency. OpenThinkIMG [36] unified these
ideas through large-scale visual–tool integration with standardized APIs, while
OctoTools [24] emphasized modular, verifiable execution via structured tool interfaces. Collectively, these systems established key principles: looped reasoning,
standardized tool I/O, and trajectory-based learning, yet remain geospatially
naive, lacking coordinate awareness, scale handling, and domain-specific spatial
verification essential for earth observation analysis.
An emerging wave of EO research is now bringing these agentic principles into
geospatial contexts. ThinkGeo [32] frames EO QA as tool-augmented reasoning,
benchmarking ReAct-style chains and exposing persistent weaknesses in coordinate consistency, spatial grounding, and multi-step planning. Earth-Agent [8]
broadens the tool ecosystem to include spectral products and standardized interfaces but still relies on largely predefined workflows, limiting physically verifiable GIS and index-based reasoning. Geo-OLM [35] explores plan-tool-verify
prompting for compact models, improving efficiency but depending primarily on
prompt-level heuristics rather than learned adaptive policies.
Building on this gap, we introduce an EO-native agentic stack that unifies
dataset construction, supervised reasoning alignment, and evaluation under a
physically grounded framework. OpenEarthAgent enables broad orchestration of
GIS, index-based, optical, and SAR operations through structured instructiontool pairs; trains on detailed reasoning traces with a dedicated evaluation set; and
supports interpretable, verifiable, multi-step reasoning across diverse geospatial
conditions.

## Page 5

OpenEarthAgent

5

Table 1: Comparison of geospatial/EO agent frameworks. Abbrev.: RS=remote
sensing; MM=multimodal inputs; Tools=executable tool/function calls; MS=multistep reasoning; GIS=GIS/vector-raster geospatial; Spec=spectral (e.g., indices, multispectral); CD=change detection; RData=reasoning-supervision data for training.
Method

RS

MM

MS

GIS

Spec

CD

RData

ReAct [50]
OpenThinkIMG [36]
ThinkGeo [32]
Earth-Agent [8]
Geo-OLM [35]
RS-Agent [48]
RS-ChatGPT [12]

✗
✗
✓
✓
✓
✓
✓

✗
✗
✓
✓
✗
✗
✗

✓
✓
✓
✓
✓
✗
✗

✗
✗
✗
✓
✗
✗
✗

✗
✗
✗
✓
✗
✗
✗

✗
✗
✓
✗
✗
✗
✗

✗
✓
✗
✗
✗
✗
✗

OpenEarthAgent (Ours)

✓

✓

✓

✓

✓

✓

✓

3

OpenEarthAgent

3.1

Dataset Curation

We curate a large-scale remote-sensing dataset linking imagery, queries, and toolbased reasoning traces to enable interpretable, multi-step geospatial analysis.
Overview and Motivation: The dataset presented in this work serves as
a foundation for training and evaluating tool-augmented geospatial reasoning
agents. While recent EO datasets primarily focus on visual classification or retrieval, they lack explicit reasoning structure and tool-level traceability. Our
dataset bridges this gap by integrating imagery, natural-language queries, reasoning traces, and tool executions in a unified schema. It enables models to
perform planning, verification, and computation beyond pattern recognition. A
comparison against existing agent frameworks is provided in Table 1, highlighting
differences in modality coverage, tool integration, reasoning depth, and supervision design. Consisting of 14,538 training samples and 1,169 held-out test samples for benchmarking, covering diverse geographic regions, sensor modalities,
and reasoning tasks, it enables interpretable multi-step learning and evaluation.
Data Sources and Composition: The dataset integrates heterogeneous imagery and metadata from open-access EO repositories, encompassing optical,
SAR, GIS, and multispectral domains. Primary sources include high-resolution
benchmarks such as DOTA [46], DIOR [21], xBD [13], AID [47], NWPU-VHR10 [41], FloodNet [31], and Global-Dumpsite [37], complemented by Sentinel collections and Google Earth Engine archives (see Table 2 for details). Each dataset
offers distinct spatial resolutions and annotation formats (bounding boxes, segmentation masks, category labels), providing both fine-grained object understanding and large-scale semantic context. The collection spans seven thematic
domains: urban planning, disaster assessment, environmental monitoring, transportation, aviation, recreation, and industrial infrastructure. Multispectral and
indexed layers (e.g., NDVI, NBR, NDBI) are derived through Google Earth
Engine to complement optical and SAR imagery with physically meaningful environmental indicators. Where required for spatial reasoning tasks, samples are

## Page 6

6

A. Shabbir et al.

Table 2: Comprehensive overview of data sources used for dataset construction, across
optical, SAR, GIS, and multispectral domains. These sources provide complementary
resolutions and annotations spanning urban and transport monitoring to environmental
and disaster assessment, forming a foundation for multi-sensor, tool-based geospatial
reasoning. GSD: ground sample distance, B-Box: bounding box, Seg: segmentation.
Source

Annotation Type

Sensor
(m/px)

Year

Applications / Tasks

Optical Datasets
DIOR [21]

B-Box, Category

0.5–30

2024

DOTA [46]

GSD, B-Box, Category

0.1–1

2021

NWPU-VHR-10 [41]

B-Box, Category

0.5–2

2023

UCAS-AOD [54]
AID [47]

B-Box, Category
B-Box, Category

0.5–2
0.2–2

2015
2017

iSAID [44]

0.1–1

2019

1–3.5

2019

0.015–
0.02
0.3–0.8

2020

Global-Dumpsite [37]

GSD, B-Box, Seg. Map,
Pix. Count
GSD, B-Box, Category,
Pix. Count
GSD, B-Box, Category,
Seg. Map, Pix. Count
B-Box, Category

2023

Transport & Aviation
Monitoring; Infrastructure
Mapping
Transport Surveillance;
Infrastructure Assessment
Aviation; Transport;
Infrastructure
Aviation; Transport
Urban Planning; Industrial
Site Detection
Segmentation; Transport
Monitoring
Disaster Assessment;
Change Detection
Flood Monitoring; Damage
Estimation
Environmental Monitoring;
Waste Localization

SAR Datasets
SSDD [52]

B-Box, Category

1–15

2021

SADD [51]

B-Box, Category

0.5–3

2022

SIVED [22]

B-Box, Category

0.1–0.3

2023

xBD [13]
FloodNet [31]

GIS-based Sources
OpenStreetMap [28]

POIs (Points of Inter- N/A
est)

Indexed / Multispectral Sources
GoogleEarthEngine
Index Layers
[10]

10–30

Ship Detection; Maritime
Transport
Aviation; Vessel
Identification
Vehicle Detection;
Transport Monitoring

2017-

Urban Mapping;
Infrastructure Analysis

2017-

Urban Planning; Change
Detection; Environmental
Monitoring

associated with geospatial metadata such as coordinates, projection reference,
and ground sampling distance (GSD), enabling verifiable geospatial analysis.
Automated Curation Pipeline and Quality Control: Dataset construction begins by aggregating candidate regions, annotations, and metadata from
multiple geospatial sources. For RGB-SAR branches, a Sample Sufficiency Filter
module removes datapoints that do not meet the required annotation counts, after which an Annotation Harmonizer module aligns labels across source datasets
to produce a unified annotation format. Index-based samples are mined by detecting temporal variations in spectral indicators such as vegetation loss, burn
severity, or flooding. All sources are converted into a unified JSON schema encapsulating imagery paths, GeoPackage metadata, spatial attributes, and tool
arguments. Before the final generation, candidate GIS queries are programmatically executed (e.g., POI counting, distance computation, area estimation) to

## Page 7

OpenEarthAgent
RGB-SAR Dataset

Conversational
1-shot Generator

7

Discard

Example Ques: {...}

RGB-SAR Data
Ingestion

Sample
Sufficiency Filter

Annotation
Harmonizer

Unified
Data

Img/
geopackage
info

Example data: {...}

failed

Unified JSON: {...}

GIS Based Dataset

Area Candidate
Generator
Available
POI Layers

Validation Suite

POI Existence
Filter

Question
Synthesizer

Dataset Constructor

passed

Index Based Dataset

Index/Event
Miner

Index
Change Gate

Question
Prompt Suite

Dataset
Prompt Suite

OpenEarthAgent
Dataset

Fig. 2: Unified data-curation pipeline for the OpenEarthAgent dataset. RGB/SAR
imagery, GIS spatial layers, and index-driven datasets are processed through dedicated filtering (annotation checks, POI constraints, and spectral-change signals such
as NDVI/NBR/NDBI). The resulting samples are merged into unified JSON records
with imagery metadata and geopackage information. A question synthesizer and conversational generator produce tool-grounded queries and reasoning traces, which are
automatically validated to ensure geographic and syntactic correctness before forming
the final corpus for agentic training and evaluation.

verify argument correctness and prevent formatting inconsistencies. Potential inconsistencies such as mismatches between query instructions and tool parameters
or invalid execution outputs are automatically detected, followed by controlled
regeneration and targeted manual verification when necessary.
Natural-language queries and reasoning trajectories are synthesized through
a structured LLM-driven module, with task-specific prompt templates and employ one-shot exemplars tailored to each reasoning category. The data generator
produces complete entries containing queries, multimodal inputs, and serialized
reasoning traces. Each instance is validated through corresponding tool execution
to verify argument correctness, geometric validity, and spatial consistency. All
test-set samples undergo manual inspection to ensure realistic geospatial measurements (e.g., addressing GSD inconsistencies in area estimates). Validated
samples form the final corpus. A summary of the pipeline is shown in Fig. 2.
Task Structure and Query Design: Each instance represents a query-driven
reasoning process that transforms static observation into an iterative perceptionaction loop (see Fig. 3). Queries are expressed in natural language and paired
with structured reasoning traces that interleave thoughts, actions, and observations, ultimately converging on a final answer. These traces span diverse modalities and task types, including: GIS operations (distance, buffer, area, zonal
statistics), object-level reasoning (counting, comparison, orientation, proximity),
spectral index computation (NDVI, NBR, NDBI), and temporal change detection. Reasoning depth and tool sequence length vary across samples, but each
trajectory provides a complete chain of intermediate steps, enabling transparent
multi-step geospatial problem solving rather than one-shot prediction.
Dataset Statistics: Fig. 4 summarizes the scale, distribution, and structure of
the OpenEarthAgent dataset. The training split contains 14,538 instances, and

## Page 8

8

A. Shabbir et al.
Can you draw a box around the black vehicle?

Can you check if the ship is heading towards the shore?

Thought: detect vehicles; Action: TextToBbox (img_1,
"vehicle", top1:false); Observation: (363,216,419,281),
(486,289,579,402), (539,463,590,522).
Thought: identify black one; Action:RegionAttribute
Description on each bbox; Observation:
1st=white, 2nd=white, 3rd=black
Thought: draw box on black; Action:
DrawBox (img_1, (539,463,590,522),
"black vehicle"); Observation:
"gen_image.jpg";
Answer: image→black vehicle (539,463,590,522).

Thought: locate shore in the image; Action: Image
Description(img_1); Observation: There is a ship near
center of image and a visible shore towards the right.
Thought: detect the ship bounding box; Action:
TextToBbox (img_1, "ship", top1: true);
Observation: (206, 138, 231, 180)
Thought: ship heading dir. (h-d);Action:
RegionAttributeDescription(img_1, (206,
138, 231, 180), "h-d"); Observation: south;
Answer: ship is facing south, while the shore
is located on right side. ship is not heading to shore.

Map NBR classes for Villarrica National Park, Araucanía Region, Chile between September
2022 and February 2023, highlighting areas of severe and moderate burn severity as well as
enhanced regrowth.

Thought: get park boundary; Action: GetAreaBoundary("Villarrica National Park,
Araucanía, Chile"); Observation: GeoPackage gpkg_1 saved.
Thought: add NBR Sept 2022; Action: AddIndexLayer(gpkg_1,"NBR","nbr_2022_
09"); Observation: Very High 55.27%,High 44.58%, Moderate 0.15%
Thought: add NBR Feb 2023; Action: AddIndexLayer (gpkg_1,"NBR","nbr_2023_
02"); Observation: High 56.90%, Moderate 36.08%, Very High 6.17%, Low 0.85%
Thought: compute change NBR; Action: ComputeIndexChange
(gpkg_1,"NBR", "nbr_2022_09","nbr_2023_02","NBR_Change");
Observation: Severe 17.3%, Moderate 27.7%, Regrowth 10.3%;
Answer: 17.3% severe, 27.7% moderate burn, 10.3%
enhanced regrowth.

What percentage of the buildings have minor damage in the postdisaster scene?

Thought: count buildings; Action:
ChangeDetection(pre=img_1,post=img_2, “Count
total buildings”); Observation: 3.
Thought: count minor-damaged buildings; Action:
ChangeDetection (pre=img_1, post=img_2, “Count
minor damage buildings”); Observation: 2.
Thought: compute percentage; Action: Calculator
(round((2/3)*100, 2)); Observation: 66.67;
Answer: 66.67% of the buildings have minor
damage in post-disaster scene.

Pre

Post

Display on the map the network distances between all doctors and colleges within a 2000m
radius of Riga Old Town, Riga, Latvia to assess healthcare accessibility for students.

Thought: get area boundary with buffer; Action: GetAreaBoundary("Riga Old Town, Riga,
Latvia", buffer_m=2000); Observation: boundary saved as gpkg_1.
Thought: add doctor POIs; Action: AddPoisLayer(gpkg_1,{"amenity":"doctors"},
"doctors"); Observation: doctors added
Thought: add college POIs; Action: AddPoisLayer(gpkg_1, {"amenity":"college"},
"colleges"); Observation: colleges added
Thought: compute network distances; Action: ComputeDistance(gpkg_1,
"doctors“,"colleges");Observation:distances=[1116.03, 1487.07, ...,1226.09];
Thought: visualize on map; Action: DisplayOnMap...; Observation:
" image/gen_image.jpg ";
Answer: <image>.

Fig. 3: Representative query-reasoning trajectories from dataset, showing interleaving
of natural-language thoughts, tool executions, and observations across tasks such as
object localization, direction estimation, spectral mapping, change detection, and GISbased analysis. Examples are simplified excerpts of longer multi-step reasoning traces.
OpenEarthAgent Dataset

(a) Data distribution across categories.

1,169 benchmarking samples

14,538 training samples

543 GIS queries

3,645 GIS queries

123 index based queries

223 index based queries

503 RGB & SAR based queries

10,670 RGB & SAR based queries

7,064 reasoning steps, avg 6.04

100,656 reasoning steps, avg 6.92

(b) Key statistics for the curated corpus used for
training and evaluation of our proposed agentic
pipeline.

Fig. 4: Dataset overview: category distribution (left) and corpus statistics (right).

the benchmark split contains 1,169 evaluation samples, each with multimodal
imagery, a natural-language query, and a structured reasoning trace with interleaved tool calls and intermediate observations. The training set contains 100,656
reasoning steps (average 6.92 per query), and the benchmark split contains 7,064
reasoning steps (average 6.04 per query). Reasoning steps correspond to explicit
thought-action-observation transitions, while tool calls capture the diversity of
operational pathways required for solving curated agentic tasks. The breadth
of modalities, thematic coverage, and depth of reasoning traces enable rigorous
evaluation of grounded, interpretable, and tool-augmented geospatial reasoning.
3.2

Methodology

Overview: We present OpenEarthAgent, a unified agentic learning framework
for multimodal reasoning over earth observation data. The framework integrates

## Page 9

OpenEarthAgent

9

Geospatial Reasoning and Tool Deployment
Input for
respective tool
Reasoning and
Image /
Action History Edited Image

GeoSpatial
Data

Vector and
Raster Layers

Short term (Working) Memory

ols
To
ke
vo
n
I

Images (RGB/Paired-CD/SAR)
Context + File Ref
Tool Feedback

o RGB + SAR

External Tools

Query

o Paired-CD
o GIS / Index
Plan

o Georeferenced RBG
User Input to Reason

Geo-Reasoning Engine
Language)

GeoSpatial Archive

Orchestrator
Core

Vector and Raster Layers

Tool Execution Cache Memory

Fig. 5: Overview of the proposed OpenEarthAgent framework. The figure depicts tool
deployment, where user queries over RGB, SAR, paired change-detection (CD), or
GIS/indexed imagery are processed by the geospatial reasoning engine and tool orchestrator, which invoke appropriate tools and integrate feedback.

tool-driven interaction and language-grounded reasoning into a single end-toend formulation. Unlike conventional, single-step multimodal models, OpenEarthAgent decomposes geospatial reasoning into an organized sequence of perception and action steps, where the agent learns to perceive, reason, and act
through callable tools operating on visual, textual, and spatial modalities. Given
a natural-language instruction u and corresponding multimodal inputs v (e.g.,
RGB imagery, paired change-detection inputs, SAR, GIS layers, or georeferenced
raster data), the agent generates multi-step reasoning trajectories that interleave
internal thoughts with explicit tool invocations and their returned outputs (see
Fig. 5). At each step, the agent maintains a short-term working memory that
contains: instructions, observations, prior tool calls, spatial metadata, and contextual feedback from previous executions, which enable iterative reasoning and
consistent spatial grounding. Training follows a supervised fine-tuning procedure
on validated reasoning traces, improving syntactic validity, spatial consistency,
and multi-step reasoning coherence across diverse geospatial contexts.
Unified Tool Registry: To standardize the diverse operators used in EO reasoning, we construct a unified tool registry that abstracts heterogeneous visual,
spectral, and GIS operations through a consistent callable schema:
  \mathcal {M}_j = (\mathbf {x}_{\text {in}}, \mathbf {y}_{\text {out}}, \psi _j), 

(1)

where xin denotes structured input arguments, yout denotes structured outputs,
ψj : xin 7→ yout is the executable function implementing the operation. All tools
follow standardized JSON-based contracts to ensure consistent serialization and
validation across training and inference. A central orchestrator parses modelgenerated tool calls, validates arguments, executes ψj , and appends returned
outputs to the working memory. During execution, a predicted tool invocation
st with arguments x̂t is evaluated as yt = ψst (x̂t ), and the returned output yt
becomes part of the updated reasoning context.

## Page 10

10

A. Shabbir et al.

To ensure efficiency and consistency, intermediate outputs (e.g., derived vector layers, raster subsets, index maps, computed geometries) are stored in a
tool execution cache memory. This cache includes geospatial archives and vector/raster layers that can be reused by subsequent tool calls within the same
trajectory. Caching prevents redundant computation and ensures deterministic replay of reasoning steps. New tools can be integrated by registering their
schema Mj without retraining the backbone model, ensuring extensibility while
maintaining interface consistency. We outline the tool categories:
a) Perceptual Tools. ground language into image-space entities. TextToBbox,
ObjectDetection, and RegionAttributeDescription convert free-form queries
into spatial primitives such as bounding boxes and semantic tags. CountGiven
Object and SegmentObjectPixels support object counting and pixel-level area
estimation. ChangeDetection analyzes multi-date imagery to detect structural
changes such as damage or flooding. b) GIS Computation Tools. enable geographic reasoning via geometric and coordinate-aware computation. GetArea
Boundary, AddPoisLayer, and ComputeDistance manipulate vector geometries
within standard coordinate reference systems. Outputs include numerical measures (e.g., distances, buffers, zonal statistics) or derived layers visualized via
DisplayOnMap. c) Spectral Tools. perform band arithmetic and spectral analysis on raster inputs. AddIndexLayer, ComputeIndexChange, and ShowIndex
Layer compute and visualize indices (NDVI/NBR/NDBI), enabling quantitative
reasoning about environmental dynamics. d) Georeferenced Raster Tools.
GetBboxFromGeotiff and DisplayOnGeotiff operate directly on georeferenced
rasters supporting coordinate extraction, bounding box derivation, and visualization aligned with spatial metadata, ensuring spatial consistency. e) Utility Tools. Calculator, Solver, and Plot support arithmetic and symbolic
reasoning. Visualization tools DrawBox and AddText display results. OCR and
GoogleSearch extend multimodal understanding through text extraction and
contextual retrieval. Terminate signals completion of a reasoning trajectory.
Reasoning Trajectories and Training Objective: Each training sample
encodes a reasoning trajectory that connects an instruction u, observations v,
and a sequence of tool interactions. Formally, the trajectory is represented as:
  \Gamma _i &= \{(s_t, r_t)\}_{t=1}^{T_i}, \quad s_t \in \mathcal {S}, \nonumber \\ r_t &\sim \mathcal {E}\!\big (s_t \mid \mathbf {u}_i, \mathbf {v}_i, \{(s_k, r_k)\}_{k<t}\big ),
(2)
where S denotes the set of registered tools, E the execution environment (tool
controller + cache), and (st , rt ) is the t-th action-result pair. Each st is a predicted tool invocation, while rt is the observation returned by the environment.
The autoregressive model conditions on the full working memory state when
predicting the next action. Training is performed via maximum likelihood estimation over verified trajectories, optimizing only the tool-action policy:
  \mathcal {L}_{\text {train}} = -\frac {1}{N}\sum _{i=1}^{N}\sum _{t=1}^{T_i} \log P_\eta (s_t \mid \mathbf {u}_i, \mathbf {v}_i, s_{<t}, r_{<t}), 

(3)

## Page 11

OpenEarthAgent

11

where η parameterizes the model and N is the number of training samples. Tool observations rt are added to the working memory as context but are
masked from loss computation and not treated as policy outputs. This formulation enforces syntactic validity of tool calls, sequential and spatial coherence,
and argument correctness, while preserving the environment-policy separation.
Before inclusion in training, each trajectory undergoes deterministic replay
through the tool controller. Re-execution verifies argument formatting, coordinate integrity, geometric validity, and full-chain executability. Through supervised fine-tuning on validated multi-step trajectories, OpenEarthAgent learns
to generate syntactically correct, spatially grounded, and interpretable reasoning workflows over heterogeneous EO data.

4

Experiments

In this section, we outline implementation details, describe the two evaluation
modes, define metrics used to quantify reasoning fidelity, tool effectiveness, and
geospatial accuracy, and discuss key experimental results and insights.
Implementation Details: OpenEarthAgent is finetuned using Qwen3-4BInstruct-2507 as the base model. Training was performed on LLM controller on
four NVIDIA A100 GPUs (40 GB). The base model is loaded via Unsloth’s FastLanguageModel, enabling efficient multi-GPU distributed training. The model
is trained for one epoch with a learning rate of 2 × 10−5 , cosine learning rate
scheduling, 0.05 warmup ratio, and a batch size of 16. The maximum sequence
length is set to 4096 tokens to support long-context conversational tool interactions. LLM is finetuned on conventional data, where the model alternates
between text generation and tool invocation, providing tool outputs and feedback in JSON format, embedded in its user and assistant turns. Training applies response-only masking, computing loss exclusively on assistant-generated
tokens, enabling accurate tool calls and structured responses without optimizing
on prompt text or external tool outputs. This enables the model to establish a
good grounding for tool invocation.
4.1

Baseline Evaluation

To evaluate OpenEarthAgent, we benchmark its performance against a diverse
set of large language models (LLMs), encompassing both proprietary and opensource variants. The comparison includes advanced frontier models (GPT-4o and
its reasoning-optimized variant o4-mini), and mid- to small-scale open-weight
models, including Llama3.1 and Internlm3. All models serve as interchangeable
backbones within the unified OpenEarthAgent framework. We assess performance using both step-by-step and end-to-end protocols, allowing analysis of
intermediate reasoning trajectories and final task completion accuracy.
Step-by-Step Evaluation: This mode measures procedural reasoning and toolinvocation behavior without executing tools. The model is given n reasoning
steps and must generate a valid action at each one based on the full interaction

## Page 12

12

A. Shabbir et al.

history. The first step is exempt from validation to allow the model to formulate
an initial high-level plan before committing to concrete tool interactions. This
setup isolates reasoning quality and enables focused analysis of spatial semantics,
plan coherence, and geospatial context understanding.
End-to-End Evaluation: This mode tests full autonomous execution with live
tool use. The model issues tool calls, forms arguments, and reasons step-by-step
based on prior outputs. This captures operational robustness, error handling,
and the effectiveness of linking perception to action in geospatial workflows.
Evaluation Metrics: We assess the model’s procedural reasoning with five
metrics. Instance Accuracy (Inst.) measures the proportion of tool called without logical or syntactic errors; Tool Accuracy (Tool) evaluates correctness of
tool selection; Argument Name Accuracy (ArgN) checks the presence of all required arguments in the generated action; Argument Value Accuracy (ArgV)
verifies argument correctness; and Summarization Accuracy (SummAcc) quantifies how well the model consolidates information from prior tool calls into a
coherent final response. We compute F1 for tool selection across four functional
categories: Perception (Per.), Operation (Op.), Logic (Logic.), and GIS (GIS.) to
capture alignment between predicted and reference tool sets. Trajectory quality
is further assessed via tool-order accuracy under increasing constraints: Unique
checks tool-to-tool correspondence without penalizing repeated calls, AnyOrder
requires all tools (including duplicates) regardless of order, and SameOrder enforces both correct sequence and frequency of tool invocations. Overall task
Accuracy compares final model completions with reference outputs. For imagegeneration tasks, success is determined by the correctness of generation tool calls
and their execution success rate; all non-generation queries are evaluated by an
LLM judge (gpt-4o-mini) using a standardized elaboration evaluation prompt.
Table 3: Step-by-step evaluation under tool-agnostic rollouts. We report accuracies:
Inst.; syntactic + logical validity of actions, Tool.; correct tool selection, ArgN.; presence of required parameters, ArgV.; parameter correctness, and Summ.; correctness of
the final consolidated answer. While frontier LLMs lead on summary accuracy, OpenEarthAgent attains state-of-the-art Inst./Tool./ArgN./ArgV., narrowing the gap despite a substantially smaller parameter budget.
Model
gpt-5
gpt-4o
o4-mini

Param. Inst. Tool. ArgN. ArgV. Summ.
FrontierLLMs
97.54 82.69 73.28
37.28
87.02
99.18 93.88 85.48
45.80
86.76
83.68 68.33 64.17
37.95
89.48

Qwen2.5-Instruct
Llama-3.1-Instruct
Internlm3-Instruct
Mistralv0.3-Instruct
Qwen2.5-Instruct

Open-SourceLLMs
7B
94.08 85.51 78.46
8B
47.07 39.30 34.11
8B
44.54 38.46 27.82
7B
64.14 35.12 26.11
3B
85.07 72.13 64.87

Qwen3-Instruct-2507

4B

OpenEarthAgent

4B

38.00
17.49
13.25
12.45
24.12

80.08
79.08
29.84
24.04
68.75

84.12

33.55

83.28

OpenEarthAgent
99.51 97.18 96.08

62.10

83.64

BaselineLLM
97.34 86.94

## Page 13

OpenEarthAgent

13

Table 4: End-to-end evaluation: (i) F1 scores for tool selection across: Perception
(Per.), Operation (Op.), Logic (Logic.), and GIS (GIS.); (ii) tool-order fidelity: AnyOrder (multiset match, order-agnostic), SameOrder (exact sequence match), and
Unique (set match, no multiplicity); and (iii) task-level Accuracy, Ans. for nongenerative and Gen. for image-generation. GPT-4o attains high GIS F1 , while OpenEarthAgent achieves strong, balanced performance with superior trajectory fidelity.
Model

F1 scores

Param.
Per.

gpt-5
gpt-4o
o4-mini

Op.

16.88
44.47
39.48

Logic.
GIS.
FrontierLLMs
47.00
6.26
91.50
66.91
35.95
95.80
64.93
12.38
86.51

Tool Order

Accuracy

AnyOr.

SameO.

Uni.

Ans.

Gen.

46.96
50.81
40.12

46.79
50.38
39.95

47.81
55.52
41.49

43.88
39.22
35.18

46.21
77.93
55.17

31.57
39.01
2.22
2.65
9.24

30.02
37.72
1.88
2.57
8.72

36.61
44.91
3.16
2.91
12.40

15.85
12.70
0.24
0.39
1.83

41.38
55.17
2.76
5.52
24.14

Qwen2.5-Instruct
Llama-3.1-Instruct
Internlm3-instruct
Mistral-Instruct-v0.3
Qwen2.5-Instruct

7B
8B
8B
7B
3B

20.38
22.54
5.50
6.74
15.63

Open-SourceLLMs
37.33
26.68
75.46
16.45
32.03
64.64
14.21
0.51
31.47
10.24
15.82
17.12
16.54
11.16
35.64

Qwen3-Instruct-2507

4B

13.86

20.95

BaselineLLM
18.35
71.82

16.00

14.71

21.47

13.72

15.86

58.30

OpenEarthAgent
56.76
51.18
98.52

67.75

67.24

72.71

45.26

75.86

OpenEarthAgent

4.2

4B

Results

In step-by-step evaluation (Table 3), frontier models lead: o4-mini score highest
on Summ. (89.48) while gpt-4o shows strong Inst. Acc. Among open-source models, Qwen2.5-I (7B) performs competitively (Inst. 94.08, Tool. 85.51), whereas
other 7B–8B models degrade, particularly on ArgV. prediction. OpenEarthAgent
(4B) substantially narrows this gap despite its smaller size, achieving state-ofthe-art Inst./ Tool./ ArgN./ and ArgV.(99.51/97.18/96.08/62.10). In the end-toend evaluation (Table 4), GPT-5 avoids external logic tools and relies on internal
numerical and analytical computations. GPT-4o leads in Op. F1 (66.91) and Gen.
Acc. (77.93) but remains modest in Per./Logic, whereas OpenEarthAgent delivers balanced gains across Per./Op./Logic./GIS and dominates in tool-order accuracy (AnyOr./SameO. /Uni. ≈ 67-72%), while substantially improving Answer
Acc. (45.26) indicating robust trajectory planning rather than isolated tool correctness. Overall, these results suggest that targeted training with tool schemas
and trajectories can outperform larger general-purpose models for geospatial tool
use, especially under strict order/frequency constraints.
Cross-Benchmark Evaluation We extend our evaluation to Earth-Agent [8]
benchmark(248 tasks, 13,729 images spanning the spectrum, products, and RGB
modalities), scoring with fine-grained step-level metrics. For compatibility, benchmark tools are reformatted to the OpenEarthAgent interface, where curated
JSON exemplars standardize tool invocation. As Table 5 reports, OpenEarthAgent (4B) outperforms similarly sized open-source baselines on every tool-related
metric, and rivals GPT-4o, showing that structured agent design and training
bring small models to within reach of frontier-level step-wise geospatial reasoning and tool execution. These gains transfer to ThinkGeo, evident from Table

## Page 14

14

A. Shabbir et al.
Table 5: Step-by-step evaluation on Earth-Agent Benchmark.
Model

Param. Inst. Tool. ArgN. ArgV. Summ.
FrontierLLMs
97.41 71.65 70.01 48.11
80.26

gpt-4o
Qwen2.5-Instruct
Llama-3.1-Instruct

Open-SourceLLMs
7B
85.98 57.76 56.06
8B
83.21 55.11 54.29

Qwen3-Instruct-2507

4B

OpenEarthAgent

34.66
35.98

79.60
73.05

59.53

38.89

76.79

OpenEarthAgent
4B
96.91 70.33 69.13

44.44

79.33

BaselineLLM
88.32 60.61

Table 6: (Left) ThinkGeo benchmark comparison on answer-level metrics. OpenEarthAgent achieves the scores, outperforming ThinkGeo and Qwen3-4B. (Right) Comparison with a generic GPT agent across the spectrum, product, and image tasks. OpenEarthAgent achieves the best overall performance with the lowest latency.
Model

Ans

ThinkGeo (reported) 9.78
Qwen3-4B (BL)
12.53
OpenEarthAgent
16.35

Ans_I

Model

Spec. Prod. Img.

20.40
25.92
29.13

GPT-Agent
Qwen3-4B (BL)
OpenEarthAgent

14.67 22.25 28.33 21.75 933.54
31.07 13.98 23.66 22.90 42.02
90.46 60.67 29.00 60.04 21.67

Total Lat(s)

6 (Left), OpenEarthAgent attains the highest Ans (16.35) and Ans_I (29.13),
surpassing both the reported ThinkGeo results and the Qwen3-4B baseline. Such
consistency across benchmarks confirms that OpenEarthAgent couples reasoning
and tool use into a robust, transferable capability.
Comparison with General Agent To assess OpenEarthAgent against a general purpose agent, we evaluate a balanced 60-query subset(20 spectrum, 20
product, and 20 image-analysis tasks) spanning the benchmark’s full range of
reasoning and tool-use demands. Table 6 (Right) shows OpenEarthAgent leading in every category, with the widest margins on spectrum tasks, where it scores
90.46, more than 4 times GPT-Agent’s 14.67. Overall, OpenEarthAgent achieves
60.04 while GPT-Agent reaches only 21.75, and the Qwen3-4B baseline reaches
22.90. OpenEarthAgent is also far more efficient, averaging just 21.67 seconds
per query versus 42.02 seconds for Qwen3-4B (2̃x slower) and 933.54 seconds for
GPT-Agent (4̃4x slower). OpenEarthAgent’s task-specific tool selection yields
higher accuracy and lower latency than generic problem-solving.
Tool Call & Success Patterns: Proprietary models (gpt-5, gpt-4o and o4mini) show strong tool-control, issuing thousands of calls with low error rates
(∼7%), indicating stable formatting. OpenEarthAgent executes a higher volume
of tool calls while achieving a superior overall success rate. In contrast, opensource models such as Qwen2.5-7B, Qwen2.5-3B, and Llama-3.1-8B exhibit high
failure rates (43-46%), reflecting weak adherence to the tool schema. Mistral-7B
demonstrates a lower error rate but fails to invoke tools at the required adequacy
to meet task demands. Despite extensive tool usage, Llama-3.1-8B and Mistral7B fail to converge to a final answer within the allowed step, resulting in 94%

## Page 15

OpenEarthAgent

Fig. 6: Tool-call performance: Opensource models show lower success rates,
while GPT family and OpenEarthAgent
achieve substantially higher success rates.

15

Fig. 7: Category-wise performance: OpenEarthAgent and gpt-5 lead in index/
GIS score, while open source performs
comparatively on image-based queries.

and 98% incomplete task executions, respectively. Overall, performance as shown
in Fig. 6 varies by call volume and precision: robust models maintain low error
rates, while others struggle with consistent, well-formed tool invocations.
Category Scores: As seen in Fig. 7, OpenEarthAgent (79.43%), gpt-4o (79.39
%), and gpt-5 (78.94%) achieve the strongest index-based scores, substantially
outperforming all baselines. GIS-based tasks reveal a sharper degradation, with
OpenEarthAgent (55.77 %) followed by gpt-5 (54.94 %), gpt-4o (41.95 %), and
o4-mini (39.55%). Open-source models; qwen2.5-7b, qwen3-4b, and llama3.1-8b
perform comparably well on image-based queries, while smaller models approach
zero on index tasks and score only marginally on GIS and image-based tasks.
Overall, the results highlight a significant performance gap and show that indexand GIS-based reasoning remains difficult for smaller open models. Additional
analyses and ablations are provided in the supplementary material.

5

Conclusion

We introduced OpenEarthAgent, a unified framework for tool-augmented geospatial reasoning that connects natural language with multimodal earth observation
data through structured analytical workflows. Unlike conventional EO models
that focus primarily on perception, OpenEarthAgent performs grounded and
interpretable reasoning by orchestrating visual, spectral, GIS, and GeoTIFFaware tools under a consistent executable schema. The accompanying corpus
comprises 14,538 training instances and 1,169 held-out test instances with validated multi-step reasoning trajectories, including explicit tool calls, intermediate
observations, and outputs. OpenEarthAgent addresses a key gap in EO research
by moving beyond perception-only modeling toward structured and verifiable
geospatial reasoning. We believe this work provides a step toward agentic AI
systems for environmental monitoring, disaster response, infrastructure analysis, and broader geospatial decision-making.

## Page 16

16

A. Shabbir et al.

References
1. Astruc, G., Gonthier, N., Mallet, C., Landrieu, L.: Anysat: One earth observation
model for many resolutions, scales, and modalities. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 19530–19540 (2025)
2. Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W.,
Gao, C., Ge, C., et al.: Qwen3-vl technical report. arXiv preprint arXiv:2511.21631
(2025)
3. Cai, Z., Cao, M., Chen, H., Chen, K., Chen, K., Chen, X., Chen, X., Chen, Z.,
Chen, Z., Chu, P., Dong, X., Duan, H., Fan, Q., Fei, Z., Gao, Y., Ge, J., Gu, C.,
Gu, Y., Gui, T., Guo, A., Guo, Q., He, C., Hu, Y., Huang, T., Jiang, T., Jiao, P.,
Jin, Z., Lei, Z., Li, J., Li, J., Li, L., Li, S., Li, W., Li, Y., Liu, H., Liu, J., Hong,
J., Liu, K., Liu, K., Liu, X., Lv, C., Lv, H., Lv, K., Ma, L., Ma, R., Ma, Z., Ning,
W., Ouyang, L., Qiu, J., Qu, Y., Shang, F., Shao, Y., Song, D., Song, Z., Sui, Z.,
Sun, P., Sun, Y., Tang, H., Wang, B., Wang, G., Wang, J., Wang, J., Wang, R.,
Wang, Y., Wang, Z., Wei, X., Weng, Q., Wu, F., Xiong, Y., Xu, C., Xu, R., Yan,
H., Yan, Y., Yang, X., Ye, H., Ying, H., Yu, J., Yu, J., Zang, Y., Zhang, C., Zhang,
L., Zhang, P., Zhang, P., Zhang, R., Zhang, S., Zhang, S., Zhang, W., Zhang, W.,
Zhang, X., Zhang, X., Zhao, H., Zhao, Q., Zhao, X., Zhou, F., Zhou, Z., Zhuo, J.,
Zou, Y., Qiu, X., Qiao, Y., Lin, D.: Internlm2 technical report (2024)
4. Caron, M., Touvron, H., Misra, I., Jégou, H., Mairal, J., Bojanowski, P., Joulin,
A.: Emerging properties in self-supervised vision transformers. In: Proceedings of
the IEEE/CVF international conference on computer vision. pp. 9650–9660 (2021)
5. Cong, Y., Khanna, S., Meng, C., Liu, P., Rozi, E., He, Y., Burke, M., Lobell,
D., Ermon, S.: Satmae: Pre-training transformers for temporal and multi-spectral
satellite imagery. Advances in Neural Information Processing Systems 35, 197–211
(2022)
6. Dai, W., Li, J., Li, D., Tiong, A., Zhao, J., Wang, W., Li, B., Fung, P.N., Hoi,
S.: Instructblip: Towards general-purpose vision-language models with instruction
tuning. Advances in neural information processing systems 36, 49250–49267 (2023)
7. Danish, M.S., Munir, M.A., Shah, S.R.A., Khan, M.H., Anwer, R.M., Laaksonen,
J., Khan, F.S., Khan, S.: TerraFM: A scalable foundation model for unified multisensor earth observation. In: The Fourteenth International Conference on Learning
Representations (2026)
8. Feng, P., Lv, Z., Ye, J., Wang, X., Huo, X., Yu, J., Xu, W., Zhang, W., Bai, L.,
He, C., Li, W.: Earth-agent: Unlocking the full landscape of earth observation with
agents. In: International Conference on Learning Representations (ICLR) (2026)
9. Fuller, A., Millard, K., Green, J.: Croma: Remote sensing representations with
contrastive radar-optical masked autoencoders. Advances in Neural Information
Processing Systems 36, 5506–5538 (2023)
10. Google Earth Engine: Google earth engine. https://earthengine.google.com/
(2025), accessed: 29 June 2026
11. Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q., Xu, R., Zhang, R., Ma,
S., Bi, X., et al.: Deepseek-r1 incentivizes reasoning in llms through reinforcement
learning. Nature 645(8081), 633–638 (2025)
12. Guo, H., Su, X., Wu, C., Du, B., Zhang, L., Li, D.: Remote sensing chatgpt: Solving
remote sensing tasks with chatgpt and visual models. In: IGARSS 2024-2024 IEEE
International Geoscience and Remote Sensing Symposium. pp. 11474–11478. IEEE
(2024)

## Page 17

OpenEarthAgent

17

13. Gupta, R., Hosfelt, R., Sajeev, S., Patel, N., Goodman, B., Doshi, J., Heim, E.,
Choset, H., Gaston, M.: xbd: A dataset for assessing building damage from satellite
imagery. arXiv preprint arXiv:1911.09296 (2019)
14. He, K., Chen, X., Xie, S., Li, Y., Dollár, P., Girshick, R.: Masked autoencoders are
scalable vision learners. In: Proceedings of the IEEE/CVF conference on computer
vision and pattern recognition. pp. 16000–16009 (2022)
15. Huang, Z., Ji, Y., Rajan, A.S., Cai, Z., Xiao, W., Wang, H., Hu, J., Lee, Y.J.: VisualToolAgent (VisTA): A reinforcement learning framework for visual tool selection.
arXiv preprint arXiv:2505.20289 (2025)
16. Irvin, J.A., Liu, E.R., Chen, J.C., Dormoy, I., Kim, J., Khanna, S., Zheng, Z., Ermon, S.: Teochat: A large vision-language assistant for temporal earth observation
data. In: International Conference on Learning Representations (2025)
17. Jakubik, J., Roy, S., Phillips, C., Fraccaro, P., Godwin, D., Zadrozny, B., Szwarcman, D., Gomes, C., Nyirjesy, G., Edwards, B., et al.: Foundation models for
generalist geospatial artificial intelligence. arXiv preprint arXiv:2310.18660 (2023)
18. Kuckreja, K., Danish, M.S., Naseer, M., Das, A., Khan, S., Khan, F.S.: Geochat:
Grounded large vision-language model for remote sensing. In: Proceedings of the
IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 27831–
27840 (2024)
19. Li, B., Zhang, Y., Guo, D., Zhang, R., Li, F., Zhang, H., Zhang, K., Zhang, P.,
Li, Y., Liu, Z., et al.: Llava-onevision: Easy visual task transfer. arXiv preprint
arXiv:2408.03326 (2024)
20. Li, J., Li, D., Savarese, S., Hoi, S.: Blip-2: Bootstrapping language-image pretraining with frozen image encoders and large language models. In: International
conference on machine learning. pp. 19730–19742. PMLR (2023)
21. Li, K., Wan, G., Cheng, G., Meng, L., Han, J.: Object detection in optical remote
sensing images: A survey and a new benchmark. ISPRS journal of photogrammetry
and remote sensing 159, 296–307 (2020)
22. Lin, X., Zhang, B., Wu, F., Wang, C., Yang, Y., Chen, H.: Sived: A sar image
dataset for vehicle detection based on rotatable bounding box. Remote Sensing
15(11), 2825 (2023)
23. Liu, F., Chen, D., Guan, Z., Zhou, X., Zhu, J., Ye, Q., Fu, L., Zhou, J.: Remoteclip:
A vision language foundation model for remote sensing. IEEE Transactions on
Geoscience and Remote Sensing 62, 1–16 (2024)
24. Lu, P., Chen, B., Liu, S., Thapa, R., Boen, J., Zou, J.: Octotools: A multi-agent
framework with extensible tools for complex reasoning. In: Proceedings of the 64th
Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
Papers) (2026)
25. Luo, J., Pang, Z., Zhang, Y., Wang, T., Wang, L., Dang, B., Lao, J., Wang, J.,
Chen, J., Tan, Y., et al.: Skysensegpt: A fine-grained instruction tuning dataset
and model for remote sensing vision-language understanding. arXiv preprint
arXiv:2406.10100 (2024)
26. Manas, O., Lacoste, A., Giró-i Nieto, X., Vazquez, D., Rodriguez, P.: Seasonal contrast: Unsupervised pre-training from uncurated remote sensing data. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 9414–
9423 (2021)
27. OpenAI: Introducing gpt. https://openai.com (2025), accessed: 29 June 2026
28. OpenStreetMap contributors: Openstreetmap: Collaborative project to create a
free editable map of the world. https://www.openstreetmap.org (2025), accessed:
29 June 2026

## Page 18

18

A. Shabbir et al.

29. Pan, J., Liu, Y., Fu, Y., Ma, M., Li, J., Paudel, D.P., Van Gool, L., Huang, X.:
Locate anything on earth: Advancing open-vocabulary object detection for remote
sensing community. In: Proceedings of the AAAI Conference on Artificial Intelligence. vol. 39, pp. 6281–6289 (2025)
30. Peng, Z., Wang, W., Dong, L., Hao, Y., Huang, S., Ma, S., Wei, F.: Kosmos2: Grounding multimodal large language models to the world. arXiv preprint
arXiv:2306.14824 (2023)
31. Rahnemoonfar, M., Chowdhury, T., Sarkar, A., Varshney, D., Yari, M., Murphy,
R.R.: Floodnet: A high resolution aerial imagery dataset for post flood scene understanding. IEEE Access 9, 89644–89654 (2021)
32. Shabbir, A., Munir, M.A., Dudhane, A., Sheikh, M.U., Khan, M.H., Fraccaro, P.,
Moreno, J.B., Khan, F.S., Khan, S.: Thinkgeo: Evaluating tool-augmented agents
for remote sensing tasks. arXiv preprint arXiv:2505.23752 (2025)
33. Shen, H., Liu, P., Li, J., Fang, C., Ma, Y., Liao, J., Shen, Q., Zhang, Z., Zhao, K.,
Zhang, Q., et al.: Vlm-r1: A stable and generalizable r1-style large vision-language
model. arXiv preprint arXiv:2504.07615 (2025)
34. Soni, S., Dudhane, A., Debary, H., Fiaz, M., Munir, M.A., Danish, M.S., Fraccaro,
P., Watson, C.D., Klein, L.J., Khan, F.S., et al.: Earthdial: Turning multi-sensory
earth observations to interactive dialogues. In: Proceedings of the Computer Vision
and Pattern Recognition Conference. pp. 14303–14313 (2025)
35. Stamoulis, D., Marculescu, D.: Geo-olm: Enabling sustainable earth observation
studies with cost-efficient open language models & state-driven workflows. In: Proceedings of the ACM SIGCAS/SIGCHI Conference on Computing and Sustainable
Societies. pp. 608–619 (2025)
36. Su, Z., Li, L., Song, M., Hao, Y., Yang, Z., Zhang, J., Chen, G., Gu, J., Li, J., Qu,
X., et al.: Openthinkimg: Learning to think with images via visual tool reinforcement learning. arXiv preprint arXiv:2505.08617 (2025)
37. Sun, X., Yin, D., Qin, F., Yu, H., Lu, W., Yao, F., He, Q., Huang, X., Yan, Z.,
Wang, P., et al.: Revealing influencing factors on global waste distribution via deeplearning based dumpsite detection from satellite imagery. Nature Communications
14(1), 1444 (2023)
38. Szwarcman, D., Roy, S., Fraccaro, P., Gíslason, Þ.E., Blumenstiel, B., Ghosal, R.,
de Oliveira, P.H., Almeida, J.L.d.S., Sedona, R., Kang, Y., et al.: Prithvi-eo-2.0:
A versatile multi-temporal foundation model for earth observation applications.
arXiv preprint arXiv:2412.02732 (2024)
39. Tseng, G., Fuller, A., Reil, M., Herzog, H., Beukema, P., Bastani, F., Green, J.R.,
Shelhamer, E., Kerner, H., Rolnick, D.: Galileo: Learning global & local features
of many remote sensing modalities. In: Proceedings of the 42nd International Conference on Machine Learning (ICML). Proceedings of Machine Learning Research,
vol. 267, pp. 60280–60300 (2025)
40. Waldmann, L., Shah, A., Wang, Y., Lehmann, N., Stewart, A., Xiong, Z., Zhu,
X.X., Bauer, S., Chuang, J.: Panopticon: Advancing any-sensor foundation models for earth observation. In: Proceedings of the Computer Vision and Pattern
Recognition Conference. pp. 2204–2214 (2025)
41. Wang, C., Bai, X., Wang, S., Zhou, J., Ren, P.: Multiscale visual attention networks
for object detection in vhr remote sensing images. IEEE Geoscience and Remote
Sensing Letters 16(2), 310–314 (2018)
42. Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., Anandkumar, A.: Voyager: An open-ended embodied agent with large language models.
arXiv preprint arXiv:2305.16291 (2023)

## Page 19

OpenEarthAgent

19

43. Wang, Y., Xiong, Z., Liu, C., Stewart, A.J., Dujardin, T., Bountos, N.I., Zavras,
A., Gerken, F., Papoutsis, I., Leal-Taixé, L., et al.: Towards a unified copernicus
foundation model for earth vision. arXiv preprint arXiv:2503.11849 (2025)
44. Waqas Zamir, S., Arora, A., Gupta, A., Khan, S., Sun, G., Shahbaz Khan, F.,
Zhu, F., Shao, L., Xia, G.S., Bai, X.: isaid: A large-scale dataset for instance
segmentation in aerial images. In: Proceedings of the IEEE/CVF conference on
computer vision and pattern recognition workshops. pp. 28–37 (2019)
45. Wei, Z., Yao, W., Liu, Y., Zhang, W., Lu, Q., Qiu, L., Yu, C., Xu, P., Zhang,
C., Yin, B., et al.: Webagent-r1: Training web agents via end-to-end multi-turn
reinforcement learning. arXiv preprint arXiv:2505.16421 (2025)
46. Xia, G.S., Bai, X., Ding, J., Zhu, Z., Belongie, S., Luo, J., Datcu, M., Pelillo, M.,
Zhang, L.: Dota: A large-scale dataset for object detection in aerial images. In:
Proceedings of the IEEE conference on computer vision and pattern recognition.
pp. 3974–3983 (2018)
47. Xia, G.S., Hu, J., Hu, F., Shi, B., Bai, X., Zhong, Y., Zhang, L., Lu, X.: Aid: A
benchmark data set for performance evaluation of aerial scene classification. IEEE
Transactions on Geoscience and Remote Sensing 55(7), 3965–3981 (2017)
48. Xu, W., Yu, Z., Mu, B., Wei, Z., Zhang, Y., Li, G., Wang, J., Peng, M.: Rsagent: Automating remote sensing tasks through intelligent agent. arXiv preprint
arXiv:2406.07089 (2024)
49. Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang,
C., Lv, C., et al.: Qwen3 technical report. arXiv preprint arXiv:2505.09388 (2025)
50. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y.: React: Synergizing reasoning and acting in language models. In: The Eleventh International
Conference on Learning Representations (ICLR) (2023)
51. Zhang, P., Xu, H., Tian, T., Gao, P., Li, L., Zhao, T., Zhang, N., Tian, J.: Sefepnet: Scale expansion and feature enhancement pyramid network for sar aircraft
detection with small sample dataset. IEEE Journal of Selected Topics in Applied
Earth Observations and Remote Sensing 15, 3365–3375 (2022)
52. Zhang, T., Zhang, X., Li, J., Xu, X., Wang, B., Zhan, X., Xu, Y., Ke, X., Zeng, T.,
Su, H., et al.: Sar ship detection dataset (ssdd): Official release and comprehensive
data analysis. Remote Sensing 13(18), 3690 (2021)
53. Zheng, Z., Yang, M., Hong, J., Zhao, C., Xu, G., Yang, L., Shen, C., Yu, X.:
Deepeyes: Incentivizing "thinking with images" via reinforcement learning. arXiv
preprint arXiv:2505.14362 (2025)
54. Zhu, H., Chen, X., Dai, W., Fu, K., Ye, Q., Jiao, J.: Orientation robust object
detection in aerial images using deep convolutional neural network. In: 2015 IEEE
international conference on image processing (ICIP). pp. 3735–3739. IEEE (2015)

## Page 20

OpenEarthAgent

1

Supplementary
OpenEarthAgent: A Unified Framework for Tool-Augmented
Geospatial Agents
Supplementary material includes ablation analysis (S1), model selection criterion
(S2), error analysis (S3), and context-specific performance assessment (S4). It
also provides quantitative results illustrating multiple evaluation cases (S5), a
detailed overview of input-output structures with corresponding tool descriptions
and details (S6), an evaluation prompt illustration with a comparative study on
LLM Judge (S7), and a detailed description of the dataset-curation components
used to construct the OpenEarthAgent corpus (S8).

S1

Ablation Analysis

Effect of Data Composition
To investigate how data composition influences model performance, we divide
the training set into easy and hard subsets based on the length of reasoning
trajectories, measured by the number of assistant planning and action steps in
each conversation. First, samples with fewer than seven tool-calling turns are
categorized as easy, while those with seven or more turns are considered hard.
To avoid tool-distribution bias, we further rebalanced several underrepresented
tools by evenly redistributing their samples across the two subsets. The easy
subset contains 8,113 samples averaging 6.095 turns, while the hard subset contains 6,425 samples averaging 7.975 turns. We evaluated under three conditions:
training on easy-only, hard-only, and combined data.
Table A1 analyzes how reasoning trajectory complexity (easy vs. hard) affects
tool-selection F1 , trajectory consistency, and end-to-end task accuracy. Training
on shorter trajectories (avg. 6.095 turns) yields the highest Perception F1 (59.63)
as perception tools (e.g., OCR, ObjectDetection, SegmentObjectPixels, CountGivenObject) are typically associated with early-stage spatial grounding and
visual interpretation. Shorter trajectories, therefore, provide more focused supervision on these perceptual and semantic alignment steps. Training on longer
Table A1: Impact of data composition: Easy-only training achieves the best Perception
score, Hard-only training boosts operational reasoning, while the combined setting
yields the most balanced performance overall, achieving the highest Logic and GIS
scores, the strongest tool-order consistency, and the best answer accuracy.
Data

Abl. setting
Easy

Set1
Set2
Set1+Set2

✓
×
✓

Hard
×
✓
✓

F1 scores
Per.
59.63
54.45
58.30

Tool Order
GIS.

Accuracy

Op.

Logic.

AnyO.

SameO.

Unique

Ans.

Gen.

52.60
56.83
56.76

OpenEarthAgent
48.11
97.26
61.59
35.16
94.35
65.61
51.18
98.52
67.75

61.42
64.93
67.24

67.51
70.40
72.71

43.40
35.79
45.26

73.79
71.72
75.86

## Page 21

2

A. Shabbir et al.

trajectories (avg. 7.975 turns) enhances Operation F1 (56.83) and improves toolorder robustness (AnyO 65.61, Unique 70.40). Hard samples involve extended
reasoning chains and richer tool compositions, encouraging the model to learn
procedural dependencies and structured multi-step workflows. However, performance in logical reasoning (35.16) remains below the combined setting low, suggesting that while challenging samples strengthen structured reasoning, they
benefit from complementary, simpler cases that help stabilize reasoning chains
and reinforce logical consistency across steps.
The combined setting achieves the most balanced and strongest overall performance, yielding the highest Logic F1 (51.18) and GIS F1 (98.52), the strongest
tool-order consistency (AnyO/SameO/Unique ≈ 67–73%), and the best Answer (45.26) and General Accuracy (75.86). Since GIS tools require coordinated perceptual grounding, logical inference, and sequential execution, training on the mixed dataset enhances both tool-type alignment (macro F1 across
Per./Op./Logic./GIS) and trajectory-level structural coherence. By integrating
short and long reasoning traces, the model simultaneously benefits from focused
perceptual supervision provided by easy samples and structured multi-step planning signals from hard samples, resulting in improved sequence fidelity under
strict order and multiplicity constraints.
Comparison with In-context Learning
To evaluate the impact of in-context learning, we conduct an ablation study on
Qwen3-Instruct-2507 by progressively increasing the number of in-context examples (k ∈ {5, 10, 15}) and comparing against the baseline model without demonstrations (BL). In-context examples are not appended as a single prompt block,
but instead are prepended as a structured conversational history. Specifically,
each example is injected as a sequence of user–assistant interaction turns (including intermediate thoughts, tool actions, and observations) before the actual
test query. The full message list, therefore, consists of: (1) a system instruction,
(2) k prior example dialogues formatted as multi-turn interactions, and (3) the
target query conversation. Results are summarized in Table A2.
Table A2: Performance comparison of Qwen3-Instruct-2507 under increasing incontext example sizes (k = 5, 10, 15) against the baseline (BL) and OpenEarthAgent.
Increasing the number of in-context examples consistently improves performance over
the baseline, while OpenEarthAgent achieves the strongest results across all metrics.
F1 scores

Models
Per.

Op.

Baseline (BL)
BL+ In-context(k=5)
BL+ In-context(k=10)
BL+ In-context(k=15)

13.86
20.26
24.86
34.58

20.95
37.34
46.29
42.10

OpenEarthAgent

58.30

56.76

Logic.

Tool Order
GIS.

AnyO.

Qwen3-Instruct-2507
18.35
71.82
16.00
30.20
87.27
29.34
34.02
86.54
30.88
37.80
89.80
36.44
OpenEarthAgent
51.18
98.52
67.75

Accuracy

SameO.

Unique

Ans.

Gen.

14.71
28.57
30.28
36.10

21.47
31.73
33.28
39.44

13.72
26.84
28.73
33.06

15.86
44.14
51.72
46.90

67.24

72.71

45.26

75.86

## Page 22

OpenEarthAgent

3

Adding in-context examples yields substantial improvements across all evaluation dimensions. Even with k=5, performance improves markedly over the
baseline, particularly in Operation, GIS F1 scores, and accuracy. Increasing k
to 10 further enhances the Logical and Operation F1 scores and yields notable
gains in tool-order consistency metrics (AnyO., SameO., and Unique), suggesting that additional demonstrations help the model better internalize structured
tool usage patterns.
For k=15, Perception and Logical F1 scores show improvements, and toolorder metrics also consistently increase, indicating improved procedural alignment. However, degradation in Operation and Generation performance between
k=10 and k=15 suggests diminishing returns beyond a certain number of demonstrations. Despite these gains, the model remains substantially below OpenEarthAgent, which outperforms all Qwen variants across every metric. This highlights that while in-context learning significantly enhances tool reasoning and
execution consistency, architectural or training-level adaptations, as employed
by OpenEarthAgent, are necessary to achieve state-of-the-art performance.
Tool Schema Influence
To assess the agent’s sensitivity to changes in the tool specification format (Table
A3), we conduct a controlled ablation over five variants ordered from minimal
structural exposure to maximal semantic conditioning.
Schema 1- Minimal Structure: This setting adds a thin layer of operational structure; a compact enumeration of all tools and a procedural rule set
(e.g., one action per step, Terminate required, tool-order constraints, JSON format). No argument signatures, semantic descriptions, or usage examples are
provided. This schema provides structural benefits for planning while withholding any semantic cues about the tool’s functionality. Consequently, the agent
must rely on actual tool feedback to infer how each tool behaves.
Schema 2- Natural-language semantics: Global planning rules and execution constraints remain identical to Schema 1. However, high-level naturalTable A3: Impact of Tool Schema Complexity on Model Reasoning and Tool Usage:
Structural exposure (Sch.1→2) improves tool perception and selection; argument-level
signatures (Sch.3) enhance interface alignment and GIS reasoning; executable constraints (Sch.4) strengthen logical consistency; and maximal specification with explicit
JSON examples (Sch.5) yields the highest overall F1 , tool-order correctness, and answer accuracy.
F1 scores

Tool Schema

Sch.1-Minimal
Sch.2-Semantic
Sch.3-Signature
Sch.4-Executable
Sch.5- Maximal

Tool Order
GIS.

Accuracy

Per.

Op.

Logic.

AnyO.

SameO.

Unique

Ans.

Gen.

19.80
43.53
48.76
47.01
58.30

8.40
27.24
28.86
27.91
56.76

OpenEarthAgent
32.00
58.99
25.32
35.80
64.71
26.96
34.22
76.32
26.17
40.94
76.86
26.55
51.18
98.52
67.75

24.89
26.45
25.66
25.95
67.24

26.69
31.58
29.77
29.26
72.71

8.44
9.10
12.77
13.03
45.26

17.93
25.86
40.69
46.21
75.86

## Page 23

4

A. Shabbir et al.

language descriptions of tool functionality are provided along with tool enumeration. The agent gains functional semantic grounding but lacks explicit demonstrations of argument structure, format exemplars, and concrete API usage patterns. This schema isolates the effect of semantic grounding without interface
exemplification.
Schema 3- Compressed Signature: The third variant introduces argument level explicitness along with natural-language semantics. Tools are presented as Tool-Aurgument signatures, for example ChangeDetection(text,pre
_image,post_image). This variant provides only tool-argument information,
without any detailed examples. It effectively mimics a code-completion-style
API, requiring the agent to infer the tool’s behavior from the structure of the
signatures.
Schema 4- Tool signature + Executable Constraint: This configuration exposes the agent to tool signatures similar to Schema 3, along with all
global rules. An additional requirement is added for command arguments: they
must contain executable Python code defining a solution() function, along
with a single example. This operational executability constraint is critical because certain tools cannot operate without a fully defined executable function; for
example, Solver uses solution() to perform symbolic reasoning using Sympy,
and Plot returns a matplotlib figure generated by code. By enforcing executable
commands, the schema ensures that the model produces actionable tool inputs
for the critical tool.
Schema 5- Maximal Information: This represents the upper bound of
tool-conditioning information. Each element contributes crucially: purpose-level
explanations clarify the tool’s goal, argument semantics specify how inputs affect
outputs, usage examples demonstrate correct application, and tool rules guide
multi-step planning and sequencing. This schema enables the model to reliably
understand, plan, and execute complex tool chains. The agent operates under a
fully specified tool-use ontology, minimizing ambiguity.
The Table A3 shows that tool-using LLM agents are highly sensitive to
how tool knowledge is structured and exposed. Performance differences arise
from information exposure, specifically from the extent of semantic grounding
and interface clarity. With minimal structure (Sch. 1), the model relies only
on structural cues and feedback, resulting in weak reasoning and the lowest
F1 scores, particularly in perception and operation (19.80 and 8.40), indicating
that the model struggles to correctly identify which tools to invoke. Introducing
natural-language tool descriptions in Schema 2 (Semantic) yields a substantial
improvement across F1 metrics. Perception more than doubles (19.80 → 43.53),
and operation improves dramatically (8.40 → 27.24). Tool-order scores also rise,
suggesting that semantic grounding enables the model to better anticipate more
accurate tool use and reasonable action sequences.
Adding explicit argument signatures (Schema 3) improves alignment and
task–tool mapping: Perception increases (+5.23), and GIS rises substantially
(+11.61), indicating stronger structural grounding. Tool-order metrics remain
largely unchanged, suggesting that signature-level exposure enhances invocation

## Page 24

OpenEarthAgent

5

precision but not higher-level planning. Generation accuracy increases markedly
(+14.83), indicating better abstraction and parameterization when invoking
image-generation tools. Introducing executable constraints (Schema 4) primarily enhances reasoning rigor as seen by logical F1 increase (+6.72). Tool-order
metrics again show minimal change, indicating that executability strengthens
operational validity rather than sequencing strategy.
Full specification combines purpose descriptions, argument semantics, executable examples, and planning rules and yields the largest gains: Perception
(+11.29), Operation (+28.85), Logical (+10.24), GIS (+21.66), and major improvements in tool-order correctness (AnyO. +41.20; SameO. +41.29; Unique
+43.45). These improvements are primarily driven by explicit full JSON tool
examples, which provide maximal interface grounding by explicitly instantiating valid invocation patterns. Compared to abstract signatures or naturallanguage descriptions, these examples define argument schemas, formatting constraints, required fields, quoting conventions, and executable structure. This
reduces syntactic ambiguity and malformed calls under strict JSON-only constraints, thereby improving the validity of invocations, the completeness of arguments, and overall schema compliance.
Effect of Tool Order
This ablation investigates the effects of tool-list ordering and explicit procedural
constraints on agent reasoning and execution behavior. We evaluate three configurations: (1) a shuffled tool list with dependency constraints preserved, (2) an
optimized tool list without explicit dependency rules, and (3) an optimized tool
list with explicit dependency rules enforcing valid tool calling preconditions. The
first setting disrupts positional priors by randomizing the presentation of tools.
The second retains a structured presentation but removes hard-coded ordering
constraints, requiring the model to infer dependencies implicitly. The third combines a structured tool presentation with explicit procedural guidance.
The results (Table A4)demonstrate that tool ordering has a substantial impact on reasoning performance and execution behavior. Progressing from shuffled tool order to optimized ordering and further to optimized ordering with
an explicit order rule yields consistent improvements in F1 scores, particularly
for Perception (+6.80, +1.85), Logic (+3.93, +2.68), and GIS (+2.98, +1.06).
These gains indicate that structured sequencing enhances information retrieval,
multi-step dependency handling, and spatial reasoning. Operational performance
peaks under optimized ordering without the rule (59.54), suggesting that strict
ordering constraints may marginally reduce operational flexibility.
Tool-order correctness metrics (AnyO., SameO., Unique) improve monotonically across settings, reflecting increased consistency in tool invocation patterns.
Answer accuracy also improves modestly (43.35→45.26), whereas generation accuracy remains stable, indicating that ordering primarily enhances execution
reliability and in-distribution reasoning rather than expanding overall generative capacity.

## Page 25

6

A. Shabbir et al.

Table A4: Impact of Tool Order on Model Reasoning and Tool Usage: Comparing
shuffled order, optimized order without rules, and optimized order with enforced preconditions shows consistent gains in reasoning F1 , tool-order correctness, and answer
Acc., while Generation Acc. remains stable.
F1 scores

Tool Schema

Shuffled Tool Order
Optimized Order w/o Order Rule
Optimized Order w/ Order Rule

Logic.

Tool Order

Accuracy

Per.

Op.

GIS.

AnyO.

SameO.

Unique

Ans.

Gen.

49.65
56.45
58.30

OpenEarthAgent
58.97
44.57
94.48
59.54
48.50
97.46
56.76
51.18
98.52

63.22
65.86
67.75

62.36
64.84
67.24

67.92
71.26
72.71

43.35
45.14
45.26

75.93
75.17
75.86

Impact of High-Level Planning
We compare OpenEarthAgent under two configurations: (1) without high-level
planning, where the agent directly invokes tools with only step-level planning,
and(2) with high-level planning, where the agent generates an explicit reasoning
plan prior to tool execution. Both variants are trained and evaluated on the same
dataset, using identical tools, supervision, and evaluation protocols.
The results (Table A5) show that incorporating a high-level planning step
leads to consistent improvements. Logical reasoning F1 increases by +3.57, reflecting improved multi-step consistency. Tool sequencing also improves, with
Any-order accuracy +4.36 and Same-order accuracy +4.37, indicating more coherent and reliably structured tool execution under explicit planning. Moreover,
image generation accuracy increases from 65.52 to 75.86 (+10.34), indicating
that explicit high-level planning significantly improves the accuracy of deciding
when to generate an image in response to a query.

S2

Model Selection

To determine how underlying model capacity affects tool-use accuracy and multistep reasoning, we compare two model backbones trained under identical data,
hyperparameter, and tool-conditioning settings: Qwen3-4B-Instruct-2507 and
Qwen2.5-7B-Instruct. We train on 25% of the training corpus and reserve an
internal 8% split from it as a held-out validation set used only for model selection, entirely separate from the benchmark test set.
Table A5: Effect of High-Level Planning: Explicit high-level planning improves logical
reasoning, tool sequencing consistency, and image generation decision accuracy, leading
to stronger structured execution and overall performance.
F1 scores

Setting
Per.
w/o High-level Plan
w/ High-level Plan

57.74
58.30

Tool Order
GIS.

Accuracy

Op.

Logic.

AnyO.

SameO.

Unique

Ans.

Gen.

58.82
56.76

OpenEarthAgent
47.61
97.11
63.39
51.18
98.52
67.75

62.87
67.24

71.77
72.71

44.50
45.26

65.52
75.86

## Page 26

OpenEarthAgent

7

As summarized in Table A6, the smaller Qwen3-4B-Instruct-2507 outperforms the 7B counterpart across nearly all metrics, particularly in logical reasoning (Logic F1 : +2.79) and tool-order consistency (AnyO: +7.0). This indicates that architectural refinements and improved alignment in the Qwen3 series
enhance structured reasoning efficiency even with fewer parameters. Both variants exhibit near-saturated GIS and operational F1 scores, confirming that toolaugmented reasoning generalizes robustly across these domains. The marginal
differences in answer and generation accuracy further suggest that reasoning
quality is independent of model scale. Overall, Qwen3-4B-Instruct-2507 delivers a superior balance between model size and reasoning reliability, making it a
strong candidate for a baseline model for scalable geospatial applications.
Table A6: Comparison of base model performance across reasoning and tool-usage
metrics. Qwen3-4B-Instruct-2507 slightly outperforms Qwen2.5-7B-Instruct. Results
highlight that improved architectural alignment in the Qwen3 series yields more efficient multi-step reasoning despite a smaller model size.
F1 scores

Base Model
Per.
Qwen2.5-7B-Instruct
Qwen3-4B-Instruct-2507

S3

96.72
97.82

Tool Order
GIS.

Accuracy

Op.

Logic.

AnyO.

SameO.

Unique

Ans.

Gen.

97.41
97.70

OpenEarthAgent
88.60
99.53
74.80
91.39
99.53
81.80

74.80
81.60

96.00
97.50

23.19
23.47

89.67
90.76

Error Analysis

We conduct a fine-grained analysis of model failures to better understand where
tool-augmented reasoning breaks down. Fig. A1 shows errors across 4 types, and
reports their frequency across some evaluated models.
Syntax errors occur when the model fails to comply with the prescribed
output syntax, such as missing required actions(No Action) or producing malformed JSON structures (Wrong action format). Each conversation allows a
single “thought-only” turn for initial planning, but all subsequent turns are
expected to include at least one valid action. Open-source models exhibit notably higher rates of such violations, particularly Mistral0.3-7B-Instruct and
InternLM3-8B-Instruct, which frequently omit or incorrectly format tool calls.
In contrast, GPT-4o shows substantially fewer syntax-related failures, indicating
stronger adherence to structured output specifications. OpenEarthAgent exhibits the fewest syntax errors overall, suggesting that fine-tuned tool schema
conditioning substantially improves output validity.
The reasoning errors are failures in multi-step logic and tool selection, including queries that reach an answer without a single tool call (Ans. w/o tool
call) and redundant tool calls in a single step (Multiple tool calls). “Answer w/o
tool call” errors are rare across models, showing that most models correctly trigger tools when needed, except Qwen3-4B-Instruct-2507 and o4-mini, which

## Page 27

8

A. Shabbir et al.

Fig. A1: Log-scale error distribution across models for four error types: No action,
Wrong action format, Answer reached without a single tool call, and Multiple tool
calls in a single action. Frontier models show fewer errors overall, while the fine-tuned
OpenEarthAgent achieves the lowest total error count.

omit calls more often. Conversely, “Multiple tool calls” are more prevalent, particularly in Mistral0.3-7B-Instruct, indicating over-generation and weaker
action control. Frontier model (GPT-4o) maintains tighter regulation, while OpenEarthAgent achieves the best balance, invoking tools only when required and
avoiding both omissions and redundancies.
Fig. A2 compares inference latency and error patterns across models. Llama
3.1-8B, InternLM3-8B and Mistralv0.3-7B show high inference times (98–
137 s/sample), while GPT-5 and OpenEarthAgent achieve ∼21.66 and ∼21.67
s/sample respectively. Error analysis reveals that tool-related failures dominate,
primarily syntax errors and failures to call required tools, indicating challenges in
structured tool invocation. GPT-4o, GPT-5, and OpenEarthAgent show substantially fewer errors across all categories. Overall, OpenEarthAgent and frontier
proprietary models achieve lower inference latency, better tool-use reliability,
and fewer execution errors, demonstrating superior overall agent performance.

S4

Context-Specific Performance Assessment

We further analyze model performance by stratifying the OpenEarthAgent Benchmark across domain-specific categories, including urban planning, environmental
monitoring, recreation, industrial infrastructure, disaster assessment, aviation,
transportation, and others. This breakdown enables fine-grained evaluation of
contextual robustness. Domain-specific difficulty in remote sensing arises from
variations in spatial scale, temporal dynamics, spectral ambiguity, and semantic complexity. Structured domains such as urban planning and environmental
monitoring typically exhibit stable, large-scale spatial patterns and consistent
spectral signatures, making them comparatively easier to analyze. In contrast,
disaster assessment involves abrupt temporal changes, heterogeneous damage
patterns, and noise, increasing change-detection complexity. Industrial, aviation,

## Page 28

OpenEarthAgent

9

Fig. A2: Comparative model performance:(Left) Inference time efficiency across architectures. (Right) Error distribution by type, revealing tool-specific failure modes
per model.

and transportation tasks often require fine-grained recognition of small or sparse
objects under varying resolutions and viewpoints, demanding stronger contextual and geometric reasoning.
As shown in Figure A3, OpenEarthAgent demonstrates strong and consistent performance across high-frequency geospatial domains, particularly in urban planning, environmental monitoring, and recreation, where it matches or
surpasses frontier models such as GPT-4o and GPT-5. Performance remains
competitive in infrastructure and disaster-related tasks, indicating effective generalization to operational geospatial reasoning scenarios. In comparison, opensource baselines exhibit substantially greater performance variance and lower
accuracy in complex reasoning tasks.

S5

Qualitative Results

Fig. A4 presents a zero-shot example demonstrating the geospatial reasoning capability of OpenEarthAgent. Given a natural language instruction, the agent autonomously composes a complete multi-step workflow. The agent first formulates
a plan to extract the park boundary, compute NBR layers, evaluate their difference, and visualize the result. It sequentially invokes the tools GetAreaBoundary,
AddIndexLayer (for December 2024 and February 2025), ComputeIndexChange,
and ShowIndexLayer, generating a differenced NBR (dNBR) layer that quantifies vegetation loss and recovery. The reasoning trace(middle) of Fig. A4 illustrates coherent tool grounding and correct argument formatting across the
entire chain.
Fig. A5 illustrates an example of OpenEarthAgent performing metricscale geospatial reasoning. Given a natural-language query about the distance

## Page 29

10

A. Shabbir et al.

Fig. A3: Domain-stratified performance on the OpenEarthAgent Benchmark. The
heatmap shows accuracy across eight geospatial domains. OpenEarthAgent delivers
strong, consistent results, particularly in urban planning and environmental monitoring, while remaining competitive in infrastructure and disaster-related tasks.

between two vehicles with a GSD of 0.6, the agent composes a workflow: detecting vehicles via TextToBbox, computing centroids with Solver, and calculating
Euclidean distance using Calculator. The reasoning trace shows coherent tool
Step 1: Formulate an initial high-level plan

Generate a preview from the NBR
difference for Topanga State Park,
Los
Angeles,
USA,
covering
December 2024 and February 2025.

To answer this, I will extract the area boundary for Topanga State Park, generate NBR
index layers for December 2024 and February 2025, compute their difference, and then
preview the difference layer.
Step 2: Fetch the area boundary
N
P

GetAreaBoundary
Area: Topanga State Park, Los Angeles, USA

R

GeoPackage created with
Area Boundary

R

1st NBR Raster layer saved,
% statistics returned

R

2nd NBR Raster layer saved,
% statistics returned

R

dNBR raster layer saved,
% statistics returned

R

dNBR raster layer converted
to PNG preview

Step 3: Generate the NBR index layer for Dec 2024
N
P

AddIndexLayer
GPKG, NBR, Year=2024, Month=12

Step 4: Generate the NBR index layer for Feb 2025
N
P

AddIndexLayer
GPKG, NBR, Year=2025, Month=2

Step 5: Compute the NBR difference
N
P

ComputeIndexChange
GPKG, NBR, layer1, layer2

Step 6: Generate a preview of the difference layer
N
P

ShowIndexLayer
GPKG, NBR, dNBR_layer_name

N Tool Name P Tool Parameters

User View

Agent Reasoning and Tool Invocation

R Tool Response

Tool Executions

Fig. A4: Example illustrates the zero-shot geospatial reasoning capabilities of OpenEarthAgent on a real-world environmental task by generating a Normalized Burn Ratio
(NBR) difference map for a given region. The NBR difference map shows pronounced
negative values (red) in southern Topanga, revealing burn scars and vegetation loss,
while northern areas remain stable (yellow), showing the post-fire effects from early
2025 events.

## Page 30

OpenEarthAgent

11

use and precise cross-modal computation. In Fig. A6, the agent extracts the
buffered area, adds POI layers, computes nearest-neighbor road distances from
each kindergarten to the closest police station, and visualizes the POIs and distance links on a base map. This demonstrates the agent’s ability to integrate
spatial query and interpretable visualization within a unified reasoning pipeline.

Step 1: Formulate an initial high-level plan

Locate and estimate the distance
between aircrafts in the scene.
Assuming GSD 0.6 m/px

"Plan: (1) Use TextToBbox to detect all aircraft. (2) Use Solver to compute the centroid of
each aircraft. (3) Use Calculator to compute the Euclidean distance between each pair
of centroids and scale by GSD = 0.6 m/px, rounding to 2 decimals.
Step 2: Detect all aircrafts
N
P

TextToBbox
Image, text = aircraft, top1 = false

R

(1016,419,1110,506), 0.51
(1093,210,1171,285), 0.48

R

(1063.0, 462.5)

R

(1132.0, 247.5)

R

135.48

Step 3: Compute centroid of aircraft #1
N
P

Solver
Command= python code

Step 4: Compute centroid of aircraft #2
N
P

Solver
Command= python code

Step 5: Compute Euclidean distance in meters using GSD=0.6

The distance between the two aircraft
is estimated to be 135.48 meters
(GSD = 0.6 m/px).

N
P

Calculator
Expression = round(sqrt((1063.0 1132.0)**2 + (462.5 - 247.5)**2) * 0.6, 2)

N Tool Name P Tool Parameters

User View

R Tool Response

Agent Reasoning and Tool Invocation

Fig. A5: Example demonstrating OpenEarthAgent’s capability for metric-scale
geospatial reasoning from imagery, estimating an airplane-to-airplane distance using
centroid detection and GSD scaling.

For the area within a 1000m
radius of Tokyo Skytree,
compute and map the travel
distances between each
kindergarten
and
the
nearest police station.

Step 1: Formulate a high-level plan

I will generate a 1000m buffer around Tokyo Skytree, add POI layers for
kindergartens and police stations, compute distances between each
kindergarten and the nearest police station, and visualize the results on a map.
Step 2: Create an area boundary GPKG
N GetAreaBoundary
P A: Tokyo Skytree, Japan,B: 1000 R

GPKG saved

Step 3: Add POIs for kindergartens.
N AddPoisLayer
P GPKG, {”amenity": " kindergarten "} R

Saved 4 POIs

Step 4: Add POIs for police stations.
N AddPoisLayer
P GPKG, {"amenity ": " police "}

Saved 6 POIs

R

Step 5: Compute Distance between kindergartens and nearest police station.
malls.
N ComputeDistance
P GPKG, kindergartens, police, top:1 R

Dist. saved

Step 6: Display on Map for visualization.
N DisplayOnMap

P

GPKG, layers

Step 7: Image saved.
N Terminate

P

Ans: <image>
N Tool Name P Tool Parameters

User View

map.png saved

R

R

Tool Response

Agent Reasoning and Tool Invocation

Fig. A6: Example demonstrating OpenEarthAgent’s road-network distance computation and spatial analysis within a 1000 m buffer of a specified area. The visualization
highlights the detailed map output generated through sequential tool orchestration.

## Page 31

12

A. Shabbir et al.

S6

Additional Tools Details

Tools I/O Structure: The tools used in OpenEarthAgent span a wide range
of perceptual, geometric, and analytical operations. They include basic utilities
such as drawing boxes, adding text, OCR, and solvers, etc., alongside higher-level
tools for object detection, region description, change detection, and pixel-level
segmentation. GIS functions such as retrieving area boundaries, adding POI
layers, and computing distances, etc., provide the spatial backbone needed for
grounded reasoning. Spectral tools further extend this capability by generating
and comparing index layers such as NDVI or NDBI. Each tool follows a clear
schema with defined inputs and outputs (see Table A7), allowing the agent
to compose them into transparent, multi-step reasoning chains across imagery,
metadata, and geospatial layers.
Tool Implementations: OpenEarthAgent integrates diverse tools to support
different stages of the reasoning and analysis pipeline. For remote sensing change
detection, we employ TEOChat [16], while LAE-DINO [29] is used for object detection and localization in Earth observation imagery. Geospatial index computation and environmental analysis are implemented through Google Earth
Engine (GEE) and geemap, providing access to a wide range of remote sensing
products and spectral indices. For spatial querying, routing, and network-based
analysis, we utilize OSMnx and NetworkX, enabling operations over road networks
and OpenStreetMap data. Image understanding and visual scene description are
handled by Qwen3-VL-7B [2]. Together, these tools provide the domain-specific
capabilities required for complex geospatial reasoning tasks. During evaluation,
the complete tool stack requires approximately 45 GB of runtime memory, with
minimal timeout occurrence.

S7

Evaluation Prompt

To evaluate the geospatial agent’s final output, we adopt a structured Answer
Accuracy assessment framework, illustrated in Fig. A8. The evaluation protocol measures the alignment between a model’s predicted answer and the corresponding ground truth using a normalized score [0,1]. The framework distinguishes between numerical and non-numerical outputs. Quantitative responses
are evaluated using a ±10% tolerance threshold, whereas spatial outputs use
Intersection over Union (IoU) thresholds. For descriptive or categorical answers,
evaluation is based on semantic equivalence, considering paraphrasing, partial
correctness, and contradictions. The protocol further defines strict handling of
missing, fabricated, or non-responsive outputs, assigning zero scores where required elements are absent or invalid. To standardize assessment, the framework
enforces a constrained JSON output format consisting of a numerical score and
a concise justification.

## Page 32

OpenEarthAgent

13

Table A7: List of available tools with brief descriptions, inputs, and outputs.
Tool Name

Description

Input

Output

Calculator

Evaluates math expressions using Python.
Extract text from an
image.
Draws a box on an
image.
Adds text to an image.

Math expression
(Python syntax)
Image

Numeric result as text

OCR
DrawBox
AddText
GoogleSearch
Plot
Solver

TextToBbox
ImageDescription
RegionAttribute Description
CountGivenObject
ChangeDetection
SegmentObject Pixels
ObjectDetection
GetAreaBoundary
AddPoisLayer
ComputeDistance
DisplayOnMap
AddIndexLayer
ComputeIndex Change
ShowIndexLayer
GetBboxFrom Geotiff
DisplayOnGeotiff

Terminate

Image; box coordinates;
optional label
Image; text; position;
optional color
Returns search results
Query string; optional
from Google.
number of results
Plots data using Python Python code defining
code.
solution()
Solves equations using
Python code defining
sympy.
solution() and using
sympy
Finds object based on
Image; object descripdescription.
tion
Generates a caption for Image
an image.
Describes an attribute
Image; attribute; opin a region or image.
tional bounding box
Counts objects in an
Image; object name;
image.
optional bounding box
Describes changes beText query; pre- and
tween two images.
post-images
Segments objects, and
Image; object name;
count pixels.
optional flag
Detects objects in the
Image
image.
Gets the area boundary Place name or bounding
as a GeoPackage.
box; optional buffer
Adds POIs to a
GeoPackage; query;
GeoPackage.
layer name
Computes distance
GeoPackage; source
between layers.
layer; target layer
Renders the map image GeoPackage; layer
from layers.
names
Computes spectral inGeoPackage; index
dex layer.
type; year; name
Computes change beGeoPackage; index
tween index layers.
type; layer names
Generates a preview of GeoPackage; index
the raster index.
type; layer name
Extracts an area bound- GeoTIFF
ing box (W,S,E,N) from
a GeoTIFF.
Renders GeoPackage
GeoPackage; layers;
layers (with feature
GeoTIFF
names) over a given
GeoTIFF.
Ends task and returns
Final answer text
the final answer.

Text with bounding
boxes
Image with drawn box
Image with text overlay
Search result text
Generated plot image
Equation solution as
string
Bounding box coordinates
Text description
Text description of
attribute
Integer count
Description of changes
Pixel count(s)
Labels; boxes; scores
GeoPackage with
boundary
Confirmation with POI
count
Summary text and layer
name
PNG image path
Saved layer and class
statistics
Saved change layer and
statistics
Preview image path
GeoPackage with
boundary
Rendered GeoTIFF

None

Open-Source LLM Judge: A Comparative Evaluation
To examine the robustness of our evaluation framework, we replace the original proprietary judge with an open-source model, Qwen3-30B, while keeping

## Page 33

14

A. Shabbir et al.

the evaluation prompt, scoring criteria, and JSON-constrained output format
identical (Fig. A8). This controlled substitution enables a direct cross-judge
consistency analysis. As shown in Fig. A7, Qwen3-30B systematically assigns
slightly higher absolute Answer Accuracy scores across models. Despite this positive bias in absolute scoring, the relative ranking of models remains preserved,
with stronger agents consistently outperforming weaker baselines under both
judges. These findings indicate that while Qwen3-30B tends toward more lenient scoring, the structured evaluation prompt ensures consistent comparative
trends, demonstrating the robustness of the proposed Answer Accuracy framework across different LLM judges.

Fig. A7: Evaluation comparison for Geospatial Agent Answer Accuracy Assessment.
Although Qwen3-30B assigns slightly higher absolute scores, model rankings remain
consistent, demonstrating the robustness of the evaluation framework.

S8

Detailed Description of Dataset-Curation Components

This appendix provides additional implementation details for the data-curation
pipeline used to construct the OpenEarthAgent corpus. The goal of the pipeline
is to transform heterogeneous earth-observation sources into a unified set of
multimodal samples, natural-language queries, and executable reasoning trajectories. Each component in Fig. 2 performs a specific normalization, filtering, or
validation step to ensure that the final samples are spatially grounded, toolcompatible, and suitable for supervised trajectory learning.

## Page 34

OpenEarthAgent

15

Fig. A8: Evaluation Prompt for Geospatial Agent Answer Accuracy Assessment. The
figure shows the structured prompt used to compute an Answer Accuracy Score (0–1)
for a geospatial agent’s prediction. It defines criteria for numerical tolerance, semantic
equivalence, error handling, and required JSON output format for standardized evaluation.

RGB-SAR Data Ingestion
The RGB-SAR data ingestion module aggregates candidate samples from multiple open-access datasets containing optical RGB imagery and synthetic aperture
radar (SAR) imagery. These datasets provide complementary spatial resolutions,
sensor characteristics, and annotation types, including bounding boxes, category labels, segmentation masks, pixel counts, and geospatial metadata. We first

## Page 35

16

A. Shabbir et al.

download all datasets and parse their native metadata, image paths, annotation
files, and sensor-specific attributes. Since the sources differ in file organization,
coordinate availability, class taxonomies, and annotation style, this stage only
performs source-level extraction and indexing. The output is a pool of candidate
RGB and SAR samples that can be further filtered according to the requirements
of each reasoning category.
Sample Sufficiency Filter
Different reasoning tasks require different minimum annotation conditions. For
example, counting and comparison queries require a sufficient number of visible
objects, proximity and distance questions require at least two relevant entities,
direction or attribute questions require localized objects with valid boxes, and
change-detection questions require paired pre- and post-event inputs. The sample sufficiency filter enforces these task-dependent constraints before question
generation. Given the parsed annotations for each sample, it assigns the sample
to one or more predefined reasoning categories only if the required number and
type of objects are present. Samples with insufficient objects, ambiguous labels,
missing boxes, invalid masks, or incomplete paired inputs are discarded at this
stage. This prevents the question synthesizer from generating queries that cannot
be answered reliably from the available annotations.
Annotation Harmonizer
The annotation harmonizer converts heterogeneous annotation formats into a
unified representation used by the downstream tool registry. Source datasets
provide annotations in different forms, such as horizontal bounding boxes, oriented boxes, segmentation masks, pixel counts, category IDs, and dataset-specific
label names. We map these formats into a common JSON-compatible schema
containing image identifiers, object categories, bounding-box coordinates, masks
where available, spatial metadata, and task-relevant attributes. Label names are
normalized across datasets to reduce semantic duplication, and missing fields
are filled when they can be derived deterministically from existing annotations.
For samples that require additional object attributes not provided by the original dataset, we add manual or semi-automatic annotations. This harmonization
step ensures that all RGB and SAR samples can be used by the same perception
tools, including object localization, counting, region-attribute description, and
visual grounding.
Area Candidate Generator
The GIS branch begins with an area candidate generator that identifies valid
geographic regions for spatial reasoning tasks. Each candidate area is represented by a place name, boundary, bounding box, or GeoPackage-compatible
geometry. Candidate regions are selected to support GIS operations such as

## Page 36

OpenEarthAgent

17

point-of-interest retrieval, distance computation, buffering, area estimation, and
map visualization. The generator also considers whether the region is likely to
contain useful infrastructure, transportation, environmental, or urban entities.
For queries requiring local accessibility or spatial relationships, buffer distances
are added around the target area to create an appropriate region of interest. The
output of this module is a set of candidate geographic areas that can be checked
for available POI layers and converted into executable geospatial inputs.
Available POI Layers
For each candidate area, we identify point-of-interest layers that can support
meaningful GIS reasoning. These layers are derived from open geospatial sources
such as OpenStreetMap and include categories such as hospitals, doctors, schools,
colleges, parks, museums, malls, roads, transport nodes, industrial sites, and
other urban or infrastructure entities. Each layer is stored with its corresponding
tag structure, geometry type, and semantic category. The purpose of this component is to expose the question-generation pipeline to only those POI classes
that are compatible with the available tools and likely to produce executable
spatial queries.
POI Existence Filter
The POI existence filter verifies whether a candidate area contains the required
POI categories before query synthesis. For example, a distance query between
doctors and colleges is only retained if both POI layers exist in the selected region. Similarly, counting, proximity, and accessibility queries require that the requested entities are present in sufficient numbers. This module executes lightweight
geospatial checks over the candidate GeoPackage or boundary and discards areas
where relevant POIs are missing, too sparse, duplicated, or geometrically invalid.
This avoids generating natural-language questions whose tool execution would
return empty or uninformative outputs.
Index/Event Miner
The index-based branch constructs samples around physically meaningful spectral or temporal events. We mine candidate regions and time windows using
spectral indicators such as NDVI, NBR, and NDBI, which capture vegetation
condition, burn severity, built-up structure, and related environmental changes.
The module searches for regions where index values exhibit interpretable temporal patterns, such as vegetation loss, burn damage, regrowth, flooding, or urban
expansion. Each candidate event is associated with the required area boundary,
date range, index type, and raster source. This produces index-based samples
that can support reasoning over environmental change rather than only static
visual recognition.

## Page 37

18

A. Shabbir et al.

Index Change Gate
The index change gate filters mined events by checking whether the observed
spectral change is strong enough to support a valid reasoning query. For each
candidate event, the relevant index layers are computed or retrieved across the
selected time window, and the magnitude of change is measured using predefined
class thresholds. Samples are retained only when the change pattern is spatially
coherent and semantically meaningful, such as a measurable decrease in vegetation, an increase in burn severity, or a detectable shift in built-up area. This
step prevents weak or noisy temporal differences from entering the dataset and
ensures that index-based questions have verifiable answers through tool execution.
Unified Data Representation
After filtering, samples from the RGB-SAR, GIS, and index-based branches are
converted into a unified data representation. Each record stores the image path
or raster reference, GeoPackage information where applicable, object annotations, spatial metadata, candidate tool arguments, and task category. For GIS
and index samples, the representation also includes area names, boundaries, coordinate reference information, POI layer names, index type, temporal range,
and derived file references. This unified schema allows the question synthesizer
and dataset constructor to operate over all modalities with a consistent interface,
even though the original sources differ substantially in structure and annotation
format.
Image and GeoPackage Information
The image and GeoPackage information module stores the physical inputs required for tool execution. For image-based tasks, it records the image identifier,
file path, image size, sensor type, and annotation references. For geospatial tasks,
it stores GeoPackage paths, layer names, coordinate reference systems, boundary geometries, POI layers, and raster metadata. This information is passed to
the tool orchestrator so that generated reasoning traces can refer to executable
inputs rather than free-form descriptions. By keeping file references and spatial
metadata explicit, the dataset supports deterministic replay and validation of
tool-based trajectories.
Question Prompt Suite
The question prompt suite contains task-specific templates used to synthesize
natural-language queries. Each template corresponds to a reasoning category,
such as object counting, object localization, region-attribute reasoning, proximity comparison, GIS distance computation, area estimation, index mapping,
or temporal change analysis. The templates are designed to vary wording while
preserving the required tool dependencies. For example, a GIS distance template

## Page 38

OpenEarthAgent

19

specifies the target area, relevant POI classes, and distance relation, while an
index-change template specifies the index type, region, and temporal range. This
prompt suite encourages linguistic diversity while maintaining compatibility with
the available annotations and tools.
Question Synthesizer
The question synthesizer converts unified data records into natural-language
queries and initial tool-grounded task specifications. It uses the question prompt
suite together with the sample metadata to generate queries whose answers require one or more tool calls. For each generated query, the synthesizer also
prepares the expected input references and candidate tool arguments. The objective is to produce questions that are natural to users but still grounded in
the available imagery, annotations, GIS layers, or index products. Queries that
contain mismatched objects, invalid regions, missing dates, or unsupported tool
requirements are rejected or regenerated.
Conversational One-Shot Generator
The conversational one-shot generator produces structured examples that guide
the construction of reasoning trajectories. Each one-shot example demonstrates
how an agent should decompose a query into thoughts, actions, observations,
and a final answer. The generator is conditioned on the task category so that
RGB-SAR, GIS, and index-based queries receive different reasoning patterns. For
instance, an object-localization query may require detection followed by drawing a box, while a GIS query may require area-boundary extraction, POI-layer
creation, distance computation, and map display. This component encourages
consistent trajectory formatting across the corpus.
Dataset Prompt Suite
The dataset prompt suite provides the instruction format used to generate complete training instances. It defines how the query, multimodal inputs, tool registry, examples, and output constraints are presented to the generator. The
prompt suite enforces a structured reasoning format in which the agent alternates between thought, action, observation, and answer fields. It also constrains
the generator to use valid tool names, valid argument names, and input references from the unified data record. This is important because the final dataset
is intended not only for language supervision but also for executable tool-policy
learning.
Dataset Constructor
The dataset constructor combines the natural-language query, multimodal input references, unified metadata, and generated reasoning trace into a complete

## Page 39

20

A. Shabbir et al.

dataset entry. Each entry contains the user query, associated image or geospatial files, serialized tool calls, intermediate observations, and final answer. The
constructor also records the task category, modality type, tool sequence, and
reasoning length. This produces a standardized training or evaluation instance
that can be consumed directly by the OpenEarthAgent training pipeline. By preserving intermediate steps, the dataset supports supervision over the complete
reasoning process rather than only the final answer.
Validation Suite
The validation suite performs automatic and manual checks before an instance is
admitted into the final corpus. First, generated tool calls are parsed and checked
for syntactic validity, including tool names, argument names, argument types,
and file references. Second, the trajectory is replayed with the tool controller
to verify that each action can be executed and that the returned observation
is consistent with the next reasoning step. Third, spatial checks are applied to
validate coordinates, geometries, POI layers, distances, areas, and raster-index
outputs. Instances that fail validation are discarded or regenerated. For the heldout evaluation split, additional manual inspection is applied to remove unrealistic
measurements, ambiguous queries, and cases where the answer depends on invalid metadata. The resulting samples form the final OpenEarthAgent dataset
used for training and benchmarking.
