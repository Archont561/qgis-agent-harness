---
id: literature/fulltexts/diazireland2026geonatureagent
type: fulltext
status: frozen
language: en
key: diazireland2026geonatureagent
title: >-
  GeoNatureAgent Benchmark: Benchmarking LLM Agents for Environmental Geospatial Analysis Across Frontier and Open-Weight Foundation Models
resource: https://doi.org/10.48550/arxiv.2606.12821
description: >-
  Environmental scientists spend disproportionate effort on data wrangling rather than analysis.
pages: 4
words: 3592
year: 2026
venue: >-
  
authors: >-
  Diaz-Ireland, Gabriel; Prieto-Herráez, Diego; Peces, Mario García; Velázquez, Javier; Jain, Devika
doi: 10.48550/arxiv.2606.12821
oa_status: green
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# GeoNatureAgent Benchmark: Benchmarking LLM Agents for Environmental Geospatial Analysis Across Frontier and Open-Weight Foundation Models

## Page 1

arXiv:2606.12821v2 [cs.AI] 3 Sep 2026

GeoNatureAgent Benchmark: Benchmarking LLM Agents for
Environmental Geospatial Analysis Across Frontier and
Open-Weight Foundation Models
Gabriel Diaz-Ireland∗

Diego Prieto-Herráez

Mario García Peces

gdiazir1@jhu.edu
Universidad Católica de Ávila (UCAV)
Ávila, Spain
Johns Hopkins University
Baltimore, MD, USA

diego.prieto@ucavila.es
Universidad Católica de Ávila (UCAV)
Ávila, Spain

mario.garcia.peces@gmail.com
Independent Researcher
Madrid, Spain

Javier Velázquez

Devika Jain

javier.velazquez@ucavila.es
Universidad Católica de Ávila (UCAV)
Ávila, Spain

kakkar@fas.harvard.edu
Center for Geographic Analysis,
Harvard University
Cambridge, MA, USA

Abstract

Keywords

Environmental scientists spend disproportionate effort on data
wrangling rather than analysis. New AI agents can be a helpful tool,
but no benchmark exists to evaluate AI agents that automate environmental geospatial workflows through structured tool calling
against real APIs. We introduce the GeoNatureAgent Benchmark,
the first benchmark for environmental analysis agents that operate via structured tool calls to a production-style geospatial API.
The benchmark comprises 93 tasks across 18 categories. Tasks
are evaluated against an open, self-hostable geospatial API that
serves three environmental indicators across Spain and Portugal
via sixteen tools. We evaluate nine frontier and open-weight LLMs,
reporting capability and per-case cost as orthogonal axes. Results
manifest that (1) Claude Sonnet 4 achieves the highest capability at
60.8% ± 0.8%, followed closely by DeepSeek V3.2 at 56.3% ± 3.1%,
while no other model exceeds 51%; (2) the cost-accuracy Pareto frontier is occupied mostly by open-weight models, with DeepSeek V3.2
offering 93% of Claude’s capability at 11.6× lower cost; and (3) structured tool calling against a real API provides a more discriminative
measure of real-world agent capability, with mean accuracies 25–35
percentage points below those reported on general-purpose GIS
benchmarks.

Geospatial AI, Benchmarking, LLM Agents, Tool Calling, Environmental Analysis

CCS Concepts
• Computing methodologies → Neural networks; Intelligent
agents; Multi-agent systems; Information extraction; • General and
reference → Evaluation; • Information systems → Geographic
information systems; • Applied computing → Earth and atmospheric sciences.
∗ Corresponding author.

This work is licensed under a Creative Commons Attribution 4.0 International License.
SIGSPATIAL ’26, Riverside, CA, USA
© 2026 Copyright held by the owner/author(s).
ACM ISBN 979-8-4007-2950-8/2026/11
https://doi.org/10.1145/3841645.3844198

ACM Reference Format:
Gabriel Diaz-Ireland, Diego Prieto-Herráez, Mario García Peces, Javier
Velázquez, and Devika Jain. 2026. GeoNatureAgent Benchmark: Benchmarking LLM Agents for Environmental Geospatial Analysis Across Frontier and
Open-Weight Foundation Models. In The 34th ACM International Conference
on Advances in Geographic Information Systems (SIGSPATIAL ’26), November 03–06, 2026, Riverside, CA, USA. ACM, New York, NY, USA, 4 pages.
https://doi.org/10.1145/3841645.3844198

1

Introduction

Environmental monitoring at scale requires multi-temporal geospatial analysis, including the detection of land cover change, the assessment of erosion risk, or the computation of vegetation indices;
furthermore, it requires the generation of statistical summaries for
regulatory compliance. Practitioners routinely spend the majority
of their effort on data wrangling, discovering datasets, reprojecting
coordinate systems, and debugging code against remote sensing
APIs [14, 22]. This expertise barrier limits the adoption of geospatial methods by domain scientists who understand environmental
systems but lack GIS programming skills.
Recent advances in large language models (LLMs) have led to the
development of AI agent systems that translate natural language
(NL) into executable geospatial operations. Architectures range
from LLMs with tool pools [1, 22] to fine-tuned specialists [20, 21]
to multi-agent systems achieving 85–97% accuracy [13, 15].
However, a critical evaluation gap persists. Public benchmarks
for LLM agents in geospatial settings remain scarce, and the few
that exist target general GIS tasks (GeoBenchX [11], ThinkGeo [16])
rather than environmental science workflows. Environmental knowledge benchmarks (EnviroExam [8]) evaluate knowledge, not agent
behavior. Code-generation benchmarks (UnivEARTH [9]) do not reflect the structured API interaction that production systems employ.

## Page 2

SIGSPATIAL ’26, November 03–06, 2026, Riverside, CA, USA

At the foundation model level, GEO-Bench [12] and GEO-Bench2 [17] evaluate pixel-level vision models, not the agent-level tool
orchestration that determines real-world usability.
This work fills this gap through three main contributions: (1) GeoNatureAgent Benchmark is the first benchmark for environmental
analysis agents using structured tool calling against a productionstyle geospatial API, comprising 93 tasks across 18 categories with a
sixteen-tool agent interface, evaluated by eight mechanistic checks
per case (no LLM-as-judge); (2) a systematic comparison of nine
LLMs spanning closed and open-weight models reports capability
and per-case cost as orthogonal axes; and (3) a cost-efficiency Pareto
analysis reveals that the cost-accuracy Pareto frontier is occupied
mostly by open-weight models.

2

Related Work

Agent tool-use can be evaluated by GeoBenchX [11], ThinkGeo [16],
and UnivEARTH [9]. GeoBenchX is the closest comparable work to
the GeoNatureAgent Benchmark, but uses low-level primitives on
local files rather than structured tool calls against a production-style
API.
GEO-Bench [12] and GEO-Bench-2 [17] evaluate pixel-level
model accuracy; GeoNatureAgent Benchmark evaluates agent-level
tool orchestration. Both are complementary.

Diaz-Ireland et al.

as a Cloud Optimized GeoTIFF (COG)), (2) Gully erosion probability [3] (Europe, continuous —0–100%—, served as a COG), and
(3) BigEarthNet V2 land cover [4] (Portugal, categorical —7-class
land cover distribution—, served as pre-computed JSON statistics).
Seven additional layers are available for visual display but not for
statistical analysis, creating natural hallucination traps.
The benchmark’s tools vary in geographic coverage: the CO2 and
gully-erosion indicators (raster COGs, Spain/Europe) are served
by the full toolset, whereas the BigEarthNet land-cover indicator (pre-computed district statistics, Portugal) is served only by
analyze_area.
For direct comparison with general-purpose GIS benchmarks, the
toolset integrates four canonical GIS operations from GeoBenchX [11]:
proximity buffering, spatial-relationship selection, centroid extraction, and explicit task rejection for out-of-scope queries.

3.2

User Query query
(NL + history)

Worked example. Case V5_21 (comparison): “Compare CO2 geological storage suitability between Murcia and Córdoba. Which
province is better suited?” The gold solution issues one compare_areas
call, returning Murcia 68.5% vs. Córdoba 68.4%; the expected answer
reports both values and notes they are within tolerance.
The benchmark covers three environmental indicators across
two countries: (1) CO2 absorption suitability [10] (Spain, categorical —Not Eligible, Eligible with Conditions, Eligible—, served

LLM Agent
(ReAct loop)

answer

Response
(NL + data)

API

Geospatial
API (COGs)

tool calls
results

3 GeoNatureAgent Benchmark
3.1 Benchmark Design

Tool Router
(16 tools)
log

GeoNatureAgent Benchmark comprises 93 tasks organized into
18 categories. The category structure is a capability taxonomy:
each category isolates one competency required for environmental
geospatial analysis—tool selection, spatial reasoning, multi-turn
memory, error handling and recovery, cross-indicator synthesis,
interpretation, and multilingual understanding, among others. Task
counts are weighted by capability importance and coverage rather
than balanced: tool selection receives the most tasks (21) because
choosing the right operation from a realistic toolset is the pivotal
agentic skill and the most discriminative across models (Section 4),
whereas niche capabilities such as cross-country temporal context
receive one or two.
Each task specifies a natural language query (optionally with
multi-turn history), expected tool calls, must-contain/must-notcontain strings, maximum rounds, cost budget, and domain-expert
ground truth. Error-handling tasks are deliberately unsolvable —
requesting analysis over non-existent municipalities, fabricating
statistics from display-only layers, or citing indicators that do not
exist — testing the agent’s ability to decline gracefully rather than
hallucinate.

Agent Architecture

Figure 1 shows the system architecture. The agent operates in
a ReAct-style loop [19]: it receives a query, reasons about tools,
executes calls, observes results, and generates a response. The agent
has access to sixteen tools: the twelve principal operations plus four
auxiliary tools for layer discovery and erosion time-series statistics.
Tools are published via a Model Context Protocol (MCP) server
Benchmark
System Architecture
exposingGeoNatureAgent
only tool primitives
[2].

Eval Harness
(scoring)
Figure 1: GeoNatureAgent Benchmark system architecture.
NL denotes natural language.

4

Experiments and Results

We evaluate nine LLMs on the GeoNatureAgent Benchmark v5
across Vertex AI Model-as-a-Service, OpenRouter, and the Anthropic Messages API. To control for run-to-run variance, every
model is evaluated under three random seeds {42, 1337, 2024}. Table 1 summarizes the main results aggregated across seeds. Three
findings stand out: (1) the top of the leaderboard is bimodal, (2) accuracy tracks scale strongly within our small open-weight sample,
and (3) closed-source frontier models do not categorically dominate open-weight peers. No model reaches 65%, confirming that
environmental geospatial tool orchestration remains a significant
challenge.
Failing cases often demonstrate partial competence: correct tool
selection but missing a keyword, or correct keywords but an extra

## Page 3

Cost-Accuracy Trade-off
(bubble size = total tokens)

GeoNatureAgent Benchmark

Table 1: Capability leaderboard

Claude Sonnet 4
DeepSeek V3.2
GLM-5
Gemini 2.5 Pro
GPT-4o
Qwen3-235B
GPT-OSS-120B
Llama 4 Scout
Gemma-3-27B

Pareto frontier

60

Params

Accuracy

Cost

$/case

—
671B MoE
—
—
—
235B MoE
120B
109B MoE
27B

60.8% ± 0.8%
56.3% ± 3.1%
50.2% ± 2.2%
48.0% ± 3.3%
41.6% ± 2.7%
41.2% ± 4.3%
34.1% ± 1.2%
26.9% ± 2.1%
15.8% ± 1.6%

$11.84
$1.05
$3.58
$4.87
$6.49
$0.89
$8.27
$0.32
$5.81

0.127
0.011
0.038
0.052
0.070
0.010
0.089
0.003
0.062

Claude Sonnet 4

50 DeepSeek V3.2

Accuracy (%)

Model

SIGSPATIAL ’26, November 03–06, 2026, Riverside, CA, USA

70

40

GLM-5
Gemini 2.5 Pro
GPT-4o

Qwen3-235B

30

GPT-OSS-120B

20 Llama 4 Scout
10
0

Gemma-3-27B

0

unnecessary tool call. This gap between binary accuracy and partialcredit scores (see Figure 2) suggests many failures are “near-misses”
addressable through prompt engineering.

2

4

6

8

10

Cost per Seed Run (USD, 93 cases)

12

14

Figure 3: Cost-accuracy trade-off.

Binary Accuracy vs Partial Credit (93 tasks)
100

Binary Accuracy (%)
Partial Credit (%)

60

87.6

86.5

86.3

82.2

79.3

77.1
66.3

60.8

56.3

40

50.2

48.0
41.6

41.2
34.1
26.9

20

Accuracy by Category (%) 18 categories, 9 models
Claude Sonnet 4 33 94 36 50 50 100 75 100 100 75 50 50 33 83 0 50 50 75
DeepSeek V3.2 30 83 29 39 44 71 78 100 89 83 0 44 78 89 33 33 100 17

5.7

-27
B

t
cou
4S

Ge

mm
a-3

0B
-12
SS

ma
Lla

T-O
GP

o

3-2
35B

ro

T-4

en
Qw

GP

5

2.5
P

MGe

mi

ni

GL

eek
epS
De

eS
on

ne

V3

t4

.2

0

Cla
ud

(63%). In contrast, models fail in tasks demanding multi-step numeric reasoning and precise tool orchestration, such as ranking
(26%), comparison (13%), and tool selection (22%). Furthermore,
models differ in consistency: while some exhibit severe competency
gaps, Claude Sonnet 4 and DeepSeek V3.2 maintain a more balanced
profile.

Figure 2: Binary accuracy vs partial-credit check score.

4.1

Failure Analysis

Accuracy varies substantially across different categories, revealing
that models handle certain tasks more effectively than others (see
Figure 4). Tasks requiring contextual retention or multilingual parsing prove relatively accessible, such as multi-turn memory (cohort
mean 75%), habitat analysis (65%), and language understanding

GLM-5 27 88 19 33 44 81 61 92 83 42 33 67 22 78 0 67 33 50
Gemini 2.5 Pro 37 58 24 39 72 86 61 67 78 33 0 56 11 67 0 0 17 67
GPT-4o 13 25 24 44 44 76 61 58 78 17 0 33 33 100 33 67 100 67

80

Qwen3-235B 17 54 14 56 44 76 39 58 83 25 33 44 44 100 0 17 50 0
GPT-OSS-120B 25 29 14 6 33 52 72 25 72 17 0 22 11 89 50 0 50 50
Llama 4 Scout 6 29 10 6 39 29 78 67 72 8 0 67 11 0 0 0 67 17

40

Gemma-3-27B 5

8

10

0

50 14 39 50 17

8

0

22 11 44

0

0

17

0

60

20
0

To
ol
Cro selec
ss- tion
i
Int ndica
erp tor
ret
a
D tion
Err eep d
or
iv
Ha han e
bit dlin
at a g
nal
Lan ysis
Mu guag
nic e
ipa
Spa Me lity
tial mo
Tem reas ry
por onin
a
g
E lc
Mu rror hange
lti- rec
mu ove
ni r ry
an
Th king
r
Co eshol
mp d
ari
s
R on
Pro Singl ankin
vin e an g
ce
agg alysis
reg
atio
n

Cost per case varies by more than an order of magnitude across
the different models (see Table 1). The cost-accuracy Pareto frontier (Figure 3) comprises four models: Llama 4 Scout (cheapest),
Qwen3-235B, DeepSeek V3.2, and Claude Sonnet 4 (highest
capability). Three of the Pareto-frontier models are open-weight;
the remaining five models are all dominated. The DeepSeek V3.2
entry is particularly notable: it delivers 93% of Claude’s capability
at 11.6× lower per-case cost, making it the strongest single-model
recommendation for cost-sensitive deployments.
Extending the cost analysis to the environmental footprint, we
estimate energy and carbon per query from token usage (blended
0.40 Wh per 1,000 tokens; global-average grid intensity 400 gCO2 /kWh;
an order-of-magnitude estimate, not a measurement): the per-case
footprint broadly rises with capability, from 3.1 gCO2 (Gemma-327B) to 6.4 gCO2 (Claude Sonnet 4).

100

Accuracy %

86.2

80

Score (%)

89.6

Figure 4: Mean accuracy by category across the nine models.

Across all 1,429 failed model–seed–case runs, failures concentrate in tool selection rather than data handling. Over two-thirds
of all errors (68.0%) stem from missing tool calls, while only 9.7%
are caused by extracting wrong data, indicating the bottleneck lies
in tool routing rather than data interpretation.

5

Discussion

GeoNatureAgent Benchmark’s 60.8% best-model accuracy is notably lower than GeoBenchX and GeoJSON Agents (85–97%). Four
factors explain the accuracy gap: (1) real API interaction vs. local file
operations; (2) environmental domain complexity; (3) multi-turn
conversation history; and (4) strict binary evaluation. Our results
align with harder benchmarks: MapEval (< 67%) [7], SpatiaLab
(55%) [18], and UnivEARTH (33%) [9].

## Page 4

SIGSPATIAL ’26, November 03–06, 2026, Riverside, CA, USA

The structured approach also constrains the output space, eliminating the 58% code execution failure rate that UnivEARTH reports [9] —further evidence that production environmental systems
should prefer structured APIs over free-form code generation.

6

Conclusion

GeoNatureAgent Benchmark is developed for evaluating AI agents
on environmental geospatial analysis through structured tool calling against an open, self-hostable API. The benchmark spans three
indicators across Spain and Portugal, demonstrating domain and
geographic extensibility. Evaluating nine LLMs on 93 tasks across
18 categories with sixteen tools, it can be concluded:
(1) Environmental geospatial tool orchestration remains
open. The capability leader (Claude Sonnet 4) achieves 60.8%±
0.8%, well below the 85–97% reported on general GIS benchmarks.
(2) Open-weight models occupy the cost-accuracy Pareto
frontier. Llama 4 Scout, Qwen3-235B, and DeepSeek V3.2.
(3) The capability-cost trade-off is steep. DeepSeek V3.2
delivers 93% of Claude’s capability at 11.6× lower per-case
cost.
(4) Systematic failures persist. Tool-selection variance remains the dominant inter-model spread, and parameter scale
alone does not predict capability.

Acknowledgments
We thank Darwin Geospatial for infrastructure support for this
research and for open-sourcing the code and experiments. The Portuguese land-cover statistics derive from BigEarthNet V2, which
contains modified Copernicus Sentinel data (2017–2018); we acknowledge the European Space Agency and the European Commission Copernicus programme. We also thank Guillermo Perez for
his contributions during his internship at Darwin Geospatial.

References
[1] Temitope Akinboyewa, Zhenlong Li, Huan Ning, and M. Naser Lessani. 2025. GIS
Copilot: Towards an Autonomous GIS Agent for Spatial Analysis. International
Journal of Digital Earth 18, 1 (2025), 2497489. doi:10.1080/17538947.2025.2497489
[2] Anthropic. 2024. Model Context Protocol. https://modelcontextprotocol.io. Open
standard for connecting language-model agents to external tools and data.
[3] Pasquale Borrelli, Francis Matthews, Christine Alewell, Konstantinos Kaffas,
Jean Poesen, Philipp Saggau, Răzvan Prăvălie, Matthias Vanmaercke, and Panos
Panagos. 2025. A hybrid in situ and on-screen survey to monitor gully erosion
across the European Union. Scientific Data 12 (2025), 755. doi:10.1038/s41597025-05074-w LUCAS 2022 gully erosion survey; data via ESDAC/JRC.
[4] Kai Norman Clasen, Leonard Hackel, Tom Burgert, Gencer Sumbul, Begüm Demir,
and Volker Markl. 2025. reBen: Refined BigEarthNet Dataset for Remote Sensing
Image Analysis. In IGARSS 2025 – 2025 IEEE International Geoscience and Remote
Sensing Symposium. 1264–1268. doi:10.1109/IGARSS55030.2025.11242834
[5] Gabriel Diaz-Ireland, Diego Prieto-Herráez, Mario García Peces, Javier Velázquez,
and Devika Jain. 2026. GeoNatureAgent Benchmark — Dataset (tasks, results,
derived environmental indicators). doi:10.5281/zenodo.20450995 Concept DOI;
resolves to the latest version.
[6] Gabriel Diaz-Ireland, Diego Prieto-Herráez, Mario García Peces, Javier Velázquez,
and Devika Jain. 2026. GeoNatureAgent Benchmark — Evaluation Harness, Agent
and Self-Hostable Geospatial API. doi:10.5281/zenodo.20450997 Concept DOI;
resolves to the latest version.
[7] Mahir Labib Dihan, Md Tanvir Hassan, Md Tanvir Parvez, Md Hasebul Hasan,
Md Almash Alam, Muhammad Aamir Cheema, Mohammed Eunus Ali, and
Md Rizwan Parvez. 2025. MapEval: A Map-Based Evaluation of Geo-Spatial
Reasoning in Foundation Models. In Proceedings of the 42nd International Conference on Machine Learning (Vancouver, Canada) (ICML’25). JMLR.org, Article 526,
40 pages.

Diaz-Ireland et al.

[8] Yu Huang, Liang Guo, Wanqian Guo, Zhe Tao, Yang Lv, Zhihao Sun, and Dongfang
Zhao. 2024. EnviroExam: Benchmarking Environmental Science Knowledge of
Large Language Models. arXiv:2405.11265 [cs.CL] doi:10.48550/arXiv.2405.11265
[9] Chia Hsiang Kao, Wenting Zhao, Shreelekha Revankar, Samuel Speas, Snehal
Bhagat, Rajeev Datta, Cheng Perng Phoo, Utkarsh Mall, Carl Vondrick, Kavita
Bala, and Bharath Hariharan. 2025. Towards LLM Agents for Earth Observation.
arXiv:2504.12110 [cs.AI] doi:10.48550/arXiv.2504.12110
[10] Kingdom of Spain. 2025. Real Decreto 214/2025 on the Regulation of the Carbon
Footprint Register. Boletín Oficial del Estado. https://www.boe.es/buscar/doc.
php?id=BOE-A-2025-7439
[11] Varvara Krechetova and Denis Kochedykov. 2025. GeoBenchX: Benchmarking
LLMs in Agent Solving Multistep Geospatial Tasks. In Proceedings of the 1st
ACM SIGSPATIAL International Workshop on Generative and Agentic AI for MultiModality Space-Time Intelligence (GeoGenAgent ’25). Association for Computing
Machinery, New York, NY, USA, 27–35. doi:10.1145/3764915.3770721
[12] Alexandre Lacoste, Nils Lehmann, Pau Rodriguez, Evan David Sherwin, Hannah
Kerner, Björn Lütjens, Jeremy Irvin, David Dao, Hamed Alemohammad, Alexandre Drouin, Mehmet Gunturkun, Gabriel Huang, David Vazquez, Dava Newman,
Yoshua Bengio, Stefano Ermon, and Xiao Xiang Zhu. 2023. GEO-Bench: Toward
Foundation Models for Earth Monitoring. In Proceedings of the 37th International
Conference on Neural Information Processing Systems (New Orleans, LA, USA)
(NIPS ’23). Curran Associates Inc., Red Hook, NY, USA, Article 2223, 14 pages.
[13] Chaehong Lee, Varatheepan Paramanayakam, Andreas Karatzas, Yanan Jian,
Michael Fore, Heming Liao, Fuxun Yu, Ruopu Li, Iraklis Anagnostopoulos, and
Dimitrios Stamoulis. 2025. Multi-Agent Geospatial Copilots for Remote Sensing
Workflows. In IGARSS 2025 – 2025 IEEE International Geoscience and Remote
Sensing Symposium. 1084–1089. doi:10.1109/IGARSS55030.2025.11243915
[14] Zhenlong Li and Huan Ning. 2023. Autonomous GIS: The Next-Generation
AI-Powered GIS. International Journal of Digital Earth 16, 2 (2023), 4668–4686.
doi:10.1080/17538947.2023.2278895
[15] Qianqian Luo, Qingming Lin, Liuchang Xu, Sensen Wu, Ruichen Mao, Chao Wang,
Hailin Feng, Bo Huang, and Zhenhong Du. 2026. GeoJSON Agents: A Multi-Agent
LLM Architecture for Geospatial Analysis—Function Calling vs. Code Generation.
Big Earth Data 0, 0 (2026), 1–55. doi:10.1080/20964471.2026.2615511
[16] Akashah Shabbir, Muhammad Akhtar Munir, Akshay Dudhane, Muhammad Umer Sheikh, Muhammad Haris Khan, Paolo Fraccaro, Juan Bernabe
Moreno, Fahad Shahbaz Khan, and Salman Khan. 2026. ThinkGeo: Evaluating Tool-Augmented Agents for Remote Sensing Tasks. arXiv:2505.23752 [cs.CV]
doi:10.48550/arXiv.2505.23752
[17] Naomi Simumba, Nils Lehmann, Paolo Fraccaro, Hamed Alemohammad,
Geeth De Mel, Salman Khan, Manil Maskey, Nicolas Longepe, Xiao Xiang Zhu,
Hannah Kerner, Juan Bernabe-Moreno, and Alexandre Lacoste. 2026. GEOBench-2: From Performance to Capability, Rethinking Evaluation in Geospatial
AI. arXiv:2511.15658 [cs.CV] doi:10.48550/arXiv.2511.15658
[18] Azmine Toushik Wasi, Wahid Faisal, Abdur Rahman, Mahfuz Ahmed Anik,
Munem Shahriar, Mohsin Mahmud Topu, Sadia Tasnim Meem, Rahatun Nesa
Priti, Sabrina Afroz Mitu, Md. Iqramul Hoque, Shahriyar Zaman Ridoy, Mohammed Eunus Ali, Majd Hawasly, Mohammad Raza, and Md Rizwan Parvez.
2026. SpatiaLab: Can Vision-Language Models Perform Spatial Reasoning in the
Wild? arXiv:2602.03916 [cs.CV] doi:10.48550/arXiv.2602.03916
[19] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language Models. In Proceedings of the 11th International Conference on Learning Representations,
ICLR 2023. doi:10.48550/arXiv.2210.03629
[20] Yifan Zhang, Jingxuan Li, Zhiyun Wang, Zhengting He, Qingfeng Guan, Jianfeng
Lin, and Wenhao Yu. 2025. Geospatial Large Language Model Trained with a
Simulated Environment for Generating Tool-Use Chains Autonomously. International Journal of Applied Earth Observation and Geoinformation 136 (2025), 104312.
doi:10.1016/j.jag.2024.104312
[21] Yuanxin Zhang, Sijie Lin, Yaxin Xiong, Nan Li, Lijin Zhong, Longzhen Ding,
and Qing Hu. 2025. Fine-Tuning Large Language Models for Interdisciplinary
Environmental Challenges. Environmental Science and Ecotechnology 27 (2025),
100608. doi:10.1016/j.ese.2025.100608
[22] Yifan Zhang, Cheng Wei, Zhengting He, and Wenhao Yu. 2024. GeoGPT: An
Assistant for Understanding and Processing Geospatial Tasks. International
Journal of Applied Earth Observation and Geoinformation 131 (2024), 103976.
doi:10.1016/j.jag.2024.103976

A

Online Resources

Code, evaluation harness, and self-hostable API: https://github.com/
gabrielireland/GeoNatureAgent_Benchmark. Benchmark dataset
and evaluation software: Zenodo DOIs 10.5281/zenodo.20450995 [5]
and 10.5281/zenodo.20450997 [6].
