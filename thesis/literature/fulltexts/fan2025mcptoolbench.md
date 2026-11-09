---
id: literature/fulltexts/fan2025mcptoolbench
type: fulltext
status: frozen
language: en
key: fan2025mcptoolbench
title: >-
  MCPToolBench++: A Large Scale AI Agent Model Context Protocol MCP Tool Use Benchmark
resource: https://doi.org/10.48550/arxiv.2508.07575
description: >-
  LLMs' capabilities are enhanced by using function calls to integrate various data sources or API results into the context window.
pages: 20
words: 8976
year: 2025
venue: >-
  
authors: >-
  Fan, Shiqing; Ding, Xichen; Zhang, Liang; Mo, Linjian
doi: 10.48550/arxiv.2508.07575
oa_status: arxiv 2508.07575
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# MCPToolBench++: A Large Scale AI Agent Model Context Protocol MCP Tool Use Benchmark

## Page 1

MCPT OOL B ENCH ++: A L ARGE S CALE AI AGENT
M ODEL C ONTEXT P ROTOCOL MCP T OOL U SE
B ENCHMARK

arXiv:2508.07575v1 [cs.AI] 11 Aug 2025

Shiqing Fan, Xichen Ding, Liang Zhang, Linjian Mo
Ant Group
{zuoran.fsq,xichen.dxc,zhuyue.zl,linyi01}@antgroup.com

A BSTRACT
LLMs’ capabilities are enhanced by using function calls to integrate various data
sources or API results into the context window. Typical tools include search, web
crawlers, maps, financial data, file systems, and browser usage, etc. Integrating these data sources or functions requires a standardized method. The Model
Context Protocol (MCP) provides a standardized way to supply context to LLMs.
However, the evaluation of LLMs and AI Agents’ MCP tool use abilities suffer
from several issues. First, there’s a lack of comprehensive datasets or benchmarks
to evaluate various MCP tools. Second, the diverse formats of response from
MCP tool call execution further increase the difficulty of evaluation. Additionally, unlike existing tool-use benchmarks with high success rates in functions like
programming and math functions, the success rate of real-world MCP tool is not
guaranteed and varies across different MCP servers. Furthermore, the LLMs’ context window also limits the number of available tools that can be called in a single
run, because the textual descriptions of tool and the parameters have long token
length for an LLM to process all at once.
To help address the challenges of evaluating LLMs’ performance on calling MCP
tools, we propose MCPToolBench++12 , a large-scale, multi-domain AI Agent tool
use benchmark. As of July 2025, this benchmark is build upon marketplace of
over 4k MCP servers from more than 40 categories, collected from the MCP marketplaces and GitHub communities. The datasets consist of both single-step and
multi-step tool calls across different categories. We evaluated SOTA LLMs with
agentic abilities on this benchmark and reported the results.

1

I NTRODUCTION

Modern LLMs (Anthropic (2025b); OpenAI (2025); Google DeepMind (2025); Yang et al. (2025))
are transforming from pure language-based models to models with more complicated reasoning and
agentic tool use capabilities (OpenAI Deep Research (2025a); Gemini Deep Research (2024); Anthropic (2025a); Moonshot AI (2025)). Many state-of-the-art LLMs are trained on function-calling
capabilities, such as searching, planning, and browse use, to access real-time information (e.g.,
weather, financial data) and perform complicated tasks like deep research, planning, and API usage (e.g., making reservations). To handle various data sources and function-calling results, Model
Context Protocol (MCP) (2025) provides a standardized way to provide context to LLMs and integrate data sources and tools from various MCP servers. A growing number of MCP servers and
clients are available in the marketplaces. However, despite the standardized protocol for LLM context, evaluating the performance of MCP Tool Function Calls remains very difficult due to several
aspects:
Lack of comprehensive benchmarks and datasets: Unable to cover highly diverse MCP tools and
schemas. Calling MCP tools requires LLMs to select from multiple available tools, which include
1
2

https://github.com/mcp-tool-bench/MCPToolBenchPP
https://huggingface.co/datasets/MCPToolBench/MCPToolBenchPP

1

## Page 2

15.7%

14.1%

9.2%
6.9%

6.3%

6.2%

3.0%
3.0%
3.2%
3.3%
3.6%
4.3%

DATABASE
SEARCH
COMMUNICATION
FINANCE
FILE SYSTEM
WEB
WORKFLOW
BLOCKCHAIN
ENTERTAINMENT
BROWSER
ART
MISCELLANEOUS

Figure 1: Distribution of MCP Servers Count by Category
JSON schemas for tools’ descriptions, parameter types, and value schemas. There is a lack of a
unified index for data source, tool schemas and server configurations across the marketplace.
Parameter Reasoning Capabilities Many tool descriptions and schemas help LLMs select the best
tool and decide appropriate parameter values. However, existing parameters require LLMs to reason
about parameter value codes and acronyms, such as stock ticker symbols (MSFT → Microsoft,
9988 → Alibaba in HKEX), driving modes (flight/train), and geocodes.
Difficulty in evaluating diverse responses The diverse nature of MCP API responses and user
queries goes beyond simple text or images, further increasing the complexity of evaluating the results. For example, when using browser-use MCPs, the take screenshot tool will fulfill a task and
save the screenshot image to local storage. Similarly, PayPal’s create invoice tool will create an invoice according to user input and send the URL for downloading the invoice to customers. For these
task-fulfillment tools, a message indicating the status of the task and related files and supplements
are usually provided.
Varied tool success rate and potential risks Some MCPs registered in communities, particularly
those provided by large corporations, offer guaranteed services, while others are less reliable or safe
and pose potential risks of prompt attacks and privacy leakage.
To overcome these issues and help scale the evaluation of MCP tool function call abilities, we
introduce a new comprehensive benchmark, MCPToolBench++, which consists of 1.5K questionanswer pairs covering 6 domains of MCP servers, including search, map, finance, pay, automatic
browser usage, file system and more. This benchmark has the following characteristics, making it
easy to use and evaluate:
Combination of Single-Step and Challenging Multiple-Steps Questions The dataset combines
single-step questions with more complicated and challenging multi-step tool usage questions. Solving multi-step problems requires a sequence of tool call chains, with some utilizing up to 10 tools in
a single user request.
Diverse and General Agent Capabilities Evaluation This benchmark dataset evaluates the highly
diverse and general capabilities of LLM models and agent systems. These capabilities vary greatly
and are invoked through MCP server integration, such as search, planning, browser usage, crawling,
API usage, and order creation/processing.
2

## Page 3

MCP Function Call
Label

Query Set

Post-Processing:
Rewriting & Validation
Query Generator

Code Dictionaries
(G eo Code,
Stock Symbols, etc)
...

Tool Call Chain Filter

Single-Step Call
Multi-Step Calls

Pro cess
LLM Calling

Database &
Files

Tool Sampler

MCP Tool
Schema

Storag e & Files

Datase t

MCP
Marketplace

Figure 2: Overview of the MCPToolBench++ Data Preparation Process
Multiple Domains and Multilingual Support To cover more domains of tasks and scale the size
of dataset, the benchmarks are prepared using a pipeline process, which involves selecting MCP
tools from over 40 categories in the marketplace as in Figure 1, cleaning MCP configurations and
tool schemas, and retaining high-quality MCP servers and tools. Typical categories include browser
use, file system, finance, pay, etc. Additionally, agents and LLMs should have multilingual ability,
making decision on which tool to choose considering the preferred language the question is using
automatically. We prepared several multilingual datasets, such as finding routes using maps worldwide, seeking financial data from global financial markets, etc.
MCP Tool Call Run Environment and Success Rate Evaluation Most official and community
MCP servers require specific environments to execute tool calls, such as MCP Clients to initiate
the service and agents’ workflow to process queries and start the tool calls. We have thoroughly
analyzed all tools in the benchmark and verified that those we utilize are tested and offer either free
access or sufficient free call quotas from the MCP service provider to enable reproduction of our
results on the benchmarks.

2

MCPT OOL B ENCH ++ F RAMEWORK

2.1

OVERVIEW

In this section, we will give an overview of the MCPToolBench++ benchmark preparation process
in Figure 2. Firstly, we will discuss the data preparation process, including how we collect the MCP
servers’ meta-information, MCP configuration files, and tool schemas from various MCP marketplaces. Secondly, based on the MCP tool schema, a tool sampler will sample tools from the schema
index, covering both single-step tool calls and multi-step tool calls (or chain of tool calls). For
example, query “Get real-time stock prices of Tesla and Microsoft, plot the chart, and calculate todays’ change” requires usage of tools getting stock data, plot chart, and calculator. An LLM will
generate meaningful prompt templates with slot values (origin, destination, mode), as well as candidates for these slots, e.g., {”origin”: ”JFK Airport”, ”destination”: ”Times Square”}. The top-K
valid slot values will be selected according to the description of the parameters. Thirdly, a Query
3

## Page 4

Generator will take the sampled tools, the prompt template and parameters’ value are generated from
the sampled tools’ schema. After slot-filling the queries will be further rewritten. Finally, after several reasonability filtering steps in the post-processing, rewrite and validation process, the generated
queries are filtered, and a valid query set and the ground-truth labels in JSON format are generated.
2.2

MCP S ERVERS AND T OOLS S CHEMA C OLLECTION

MCP servers are gathered from the open MCP marketplace across various websites, including smithery.ai3 , deepnlp.org4 , pulsemcp.com5 , and modelscope.cn6 . Some of these marketplaces offer direct
API support. For schema JSON files, we utilize the mcp-marketplace Python SDK7 to search and
filter relevant MCPs by categories such as map and browser-related MCPs. We collected three types
of MCP schemas: mcp config.json, server meta.json, and tool schema.json, and indexed them locally for listing and retrieval. For detailed definitions of these MCP server JSON files, please refer
to the appendix A.1.
2.3

T OOL S AMPLER

After collecting tool schemas from the marketplace, we apply the Tool Sampler to generate singlestep tool calls (e.g., sampling the get weather tool) and multi-step tool calls (e.g., navigate →
screenshot).
Given a total of N tools collected from M MCP servers and C categories, we let Nc denote the
number of tool schemas collected from the c-th category. We apply different sampling strategies for
single-step and multi-step tool calls.
For single-step tool calls, we sample tool ti from Nc candidates. We use a sampling with replacement strategy, where each tool is sampled with equal probability pi .
For multi-step tool calls, which require multiple tool calls to fulfill a user’s request, we divide the
tool call generation into different bins. Each bin represents a different number of tool calls, ranging
from count = 2 to count = K (we set the maximum count K to 10).
Within the same category c, we use a sampling without replacement strategy to obtain a nonduplicated list of sampled tools [t1 , . . . , tk , . . . , tK ], where tk denotes the k-th sampled tool up
to K. The distribution of queries in different bins is illustrated in the evaluation section.
Cross-categories multi-step tool calls: Sometimes, a user’s query requires tool calls with different
features from various categories. For example, the prompt ”get the stock price from magnificent 7
stocks within last week and plot a time-series chart” requires a financial tool call and a chart plotting
tool. We first use a Large Language Model (LLM) to generate meaningful category combinations,
such as [. . . , cs , ct , . . . ] (e.g., (finance, plot), (search, map), etc.). We then apply the same sampling
without replacement strategy used for within-category sampling to the tools from these generated
category combinations.
2.4

Q UERY G ENERATOR

The query generator process contains several consecutive steps: Tool Call Template generation, Parameter Values Generation, Slot Filling, and Query Rewriting. We will use the tool
maps directions(origin, destination, mode) as an example to illustrate this process.
Tool Call Template generation: A template is generated from sampled tool list [t1 , . . . , tk , . . . , tK ].
For example, for the single-step tool maps directions from Google Maps, a diverse batch of templates like ”Can you help me plan the best route from {origin} to {destination}?” are generated by
an LLM.
3

https://smithery.ai
https://www.deepnlp.org/store/ai-agent/mcp-server
5
https://www.modelscope.cn/mcp
6
https://www.pulsemcp.com
7
https://github.com/AI-Agent-Hub/mcp-marketplace
4

4

## Page 5

Category
Browser
File System
Search
Map
Finance
Pay
Total

Table 1: Statistics of Dataset Instance MCP Tools Count and Tokens
Number Instance MCP Tool Count Tokens Per Tool Total Tokens
187
32
107.4
3.4 K
241
11
143.8
1.6 K
181
5
555.6
2.8 K
500
32
401.3
13 K
90
1
505.0
0.5 K
310
6
656.5
3.9 K
1509
87
288.3
25 K

Parameters Value Generation: To fill the parameters in the template, valid and meaningful parameters values are generated according to the field description in the tool schema JSON file. For
instance, {”origin”:”JFK Airport”} and {”destination”:”Times Square”} are Point of Interest (POI)
names generated by the inherent knowledge of the LLM.
Code Dictionaries are feed to the context of the LLM to help generate the desired parameters.
Some MCP tools require specific codes as input to the functions instead of natural language, such
as geo code, stock symbols, acronyms, etc. For example, the weather tool takes input of city and
state as geo-code (CA → California), global stock data API requires correct symbols ( TSLA →
Tesla, 700 → Tencent, 600519 → Kweichow Moutai), etc.
Slot Filling: The generated parameter values are filled into the template to complete a query.
Query Rewrite: The generated queries sometimes have grammatical issues and need to pass through
a query rewrite stage to become meaningful queries. For example, a generated query after slot
filling might be ”Compare today’s stock price change of MSFT and TSLA,” where the stock ticker
is generated and filled. This would then be rewritten to ”Compare today’s stock price change of
Microsoft and Tesla.”
2.5

P OST P ROCESSING & VALIDATION

Post-processing and validation steps are crucial for the synthetic dataset. In our MCPToolBench++
benchmark, we applied several post-processing steps to filter out low-quality queries.
Semantic check: Queries that are not properly rewritten will be removed in the semantic check step.
For example, ”Find good restaurants near 40.7°, 70.3°” would be removed because the tools require
raw (longitude, latitude) coordinates as input, and the query rewrite steps were unable to convert the
coordinates to a POI name.
Reasonableness check: The reasonableness of the generated queries is checked. Any counterfactual
queries will cause the API to fail and need to be removed from the dataset. For example, ”How can
I travel from New York to Tokyo by train?” is counterfactual because Japan is an island, and there is
no way to travel from New York to Tokyo by train.

3

DATASET D IVERSITY & A NALYSIS

3.1

T OOL S CHEMA C OMPLEXITY A NALYSIS

We conducted complexity analysis of the MCP function calls that LLM needs to process.
In the formulation, M denotes number of MCP servers installed on AI Agent systems, Nt denotes
the average number of tools that the server provides, and Ttool denotes the average token length of
the schema description of the tool and parameters. The tokens that each function call LLM needs
to process have complexity O(M Nt Ttool ). And Ttools usually has magnitude ranging from 0.1K
to 1K. The total number of available tools has the magnitude of a few hundreds before ranking or
relevance filtering. The statistics of some MCP servers from various domains are listed in Table 1.
Tool Dispatcher Retrieval and Relevant Tools Selection Tools Dispatcher is needed to retrieve
relevant tools from the tool schema description to avoid the explosion of unnecessary tools to LLMs.
Tool Dispatcher aims to select relevant tools given users’ original query, which can help reduce
5

## Page 6

the average number of tools consumed by LLM from Nt (∼ 100) to Nk (∼ 10), usually from a
few hundreds to the magnitude of 10. The overall complexity becomes O(M Nk Ttool ), which can
remove unnecessary tools schema and help increase the overall accuracy performance.

4

E VALUATION

We evaluated the MCPs’ function calling abilities across a wide range of models on the MCPToolBench++ benchmark, including models from the OpenAI OpenAI et al. (2024), Claude Anthropic
(2025a), Qwen Yang et al. (2025), Kimi Moonshot AI (2025) and others. The benchmark datasets
are further characterized by multilingual support (English, Chinese, French, Russion, etc), different
steps of tool calls (single-step vs. multi-steps), and various categories (search, browse, map, etc.) to
reflect performance across different levels of task difficulty.
4.1
4.1.1

M ETRICS
ACCURACY E VALUATION

Abstract Syntax Tree AST To evaluate the accuracy of MCP tool calls by LLMs, we adopted the
Abstract Syntax Tree (AST) metric. This metric compares the predicted output with ground truth
labels for function match, required parameters match, parameter type and value match (Patil et al.
(2024)).
Multi-Step AST DAG Accuracy: For multi-step tool executions, we apply a modified metric of
AST, and proposed the metric AST DAG Accuracy. The metric AST DAG-Accuracy denotes
the Directed Acyclic Graph (DAG) evaluation of AST score between the predicted multi-steps
tool call execution plan with the ground-truth tool call execution plan. This metric is useful because tool call executions have dependencies on previous tool call results. Some prompts have the
DAG structure, for example in prompt ”Find the top 10 stocks with highest price increase from
market of NASDAQ, NYSE and DOW and London Stock Exchange, and then plot the stock and
in a chart.”. The execution plans looks like: get top change stocks(”NASDAQ”) → plot chart,
get top change stocks(”NYSE”) → plot chart, get top change stocks(”DOW”) → plot chart,
get top change stocks(”LSE”) → plot chart. The get top change stocks tool runs in parallel and
the plot chart tool depends on the previous 4 tool call results. Note that for AST DAG Accuracy metric, label = 1 denote the children nodes (last execution nodes of each task) should match between
the prediction and the ground-truth, and label = 0 denotes otherwise. We also notice the phenomena
that different models tend to choose different paths of tool calls to finish the same tasks. For example
the route planning task, some LLMs tend to choose one step of direct tool call that takes in address
as input to the tool plan route(origin address, destination address), and other LLMs tend to divide
the task into three steps, converting the origin and destination address to geocodes or coordinates
first and then call the plan route(origin geocodes, destination geocodes).
AST DAG Accuracy = calculate dag accuracy(DAGpredict , DAGground truth )
4.1.2

T OOL C ALL E VALUATION

Pass@K Accuracy: To measure whether the execution result from the MCP tool call is correctly
aligned with the expected output, we use Pass@K to evaluate the accuracy of the MCP function
call. A successful MCP tool call run has many conditions, including the input parameters should
be correct, the tool call should be successful, the execution results should not be empty and align
with the expected ground-truth, etc. To evaluate whether the MCP tool call (API calling) succeeded
or failed with errors, we evaluate the response status of each MCP tool call. Sometimes, the MCP
server return a 200 success status code, but the detailed message is showing an internal parameter
error, such as {”success”: false, ”data”: null, ”error”: ”[’type’: ’text’, ’text’: ’Geocoding failed...
’]”}. To evaluate the detailed message and whether the expected output is aligned, we use an LLM
as judge to label the success status of each response. Some root-cause analysis of errors and related
prompts are provided in the appendix 4.
Tool Call Success Rate The tool call success rate is a dynamic metric that measures the ratio of
successful tool call runs to total runs for each MCP tool. In the MCP tool call scenario, this metric
6

## Page 7

AST Performance by Category
File System

er

ct

3-c

ns

od

tru

et

en
Qw

ax
Cla

0.732

0.716

de
r

tru
ct
2-I
ns

en
3-c
o

et
on
n
7-S

-3.

Cla

Qw

ud
e

Kim
i-K

o
Qw

Qw

GP

en
3-c
o

T4

de
r

tru
ct
2-I
ns

on
n

ud
e

Kim
i-K

-3.

7-S

en
2.5
-

GP

Qw

et

ma
x

T4

de
r

en
3-c
o

Qw

Cla

Cla

ud
e

Kim
i-K

-3.

7-S

2-I
ns

on
n

et

ma
x

en
2.5
-

o

0.00

tru
ct

0.25

0.00
o

0.740

0.50

ma
x

0.50

0.751

0.720

0.75

0.25
T4

e-3

en

0.724

0.00
GP

nn

GP

Qw

0.807

0.706

0.668

0.25

Qw

-m

er

Finance

AST

0.50

0.708

0.75
AST

0.609

0.582

0.718

1.00

en
2.5
-

0.783

0.737

0.612

3-c
en
Qw

i-K
Kim

Pay
1.00

0.75

od

tru
2-I

So

ns

nn

et

ax
e-3

Cla

ud

Qw

Qw

en

.7-

2.5

GP

-m

er
3-c

en

2-I
i-K

Kim

ud
Cla

od

tru
ns

nn

et

ax

So

-m

e-3

en

.7-

2.5

GP

Qw

Map

T4
o

0.00
ct

0.00
T4
o

0.00
ct

0.25

1.00
AST

0.50

0.25

2.5

0.50

0.25

0.732

0.728

0.628

0.520

.7-

AST

AST

0.50

0.75

2-I

0.842

0.75

0.650

So

0.886

Search
1.00

0.908

0.906

i-K

0.942

ud

0.887

0.818

0.726

0.652

T4
o

AST

0.75

1.00

Kim

Browser
1.00

Figure 3: MCP Tool Call Abstract Syntax Tree Score Performance

Pass@1 Performance by Category
File System

en

2-I

3-c

od

er

tru
ct
ns

t
nn
e
Kim

Qw

i-K

.7-

2.5
en
Qw

So

-m
a

x

o
T4
GP

od
3-c

en
Qw

Cla

Cla

er

tru
ct
2-I

Kim

0.75
0.50

Figure 4: MCP Tool Call Pass@K Score Performance

7

er

ct

od
3-c
en

2-I

ns

tru

t
nn
e
So
.7-

i-K
Kim

-m
a
2.5

e-3

Cla

ud

en

0.286

0.238

0.231

Qw

0.256

x

o
T4
GP

er

en

3-c

od

tru
Qw

ns
2-I

i-K
Kim

.7-

So

nn
e

t

x
-m
a
2.5

e-3
ud

Cla

ct

0.00

0.289

Qw

Pass@1

0.544

0.00
en

od
3-c
en

0.676

0.557

0.528

0.25
o

er

ct
Qw

i-K

2-I

ns

tru

t
nn
e
So
Kim

Cla

ud

e-3

.7-

2.5
en

GP

T4

-m
a

x

o

0.00

Finance

0.25
T4

0.305

0.201

0.574

0.50

GP

0.25

0.368

1.00

Qw

0.275

0.227

Pass@1

0.75

Qw

Pass@1

0.75

0.523

0.460

Pay
1.00

0.362

ns

nn
e
So

i-K

.7-

en

t

x

o
T4
GP

od
3-c

Qw

Kim

Qw

i-K

en

2-I

0.00

Map

0.620
0.472

0.50

0.00

1.00

0.50

0.75

0.25

er

tru
ct
ns

t
nn
e
So
.7-

e-3

Cla

ud

Qw

en

2.5

GP

T4

-m
a

x

o

0.00

0.868

0.25
-m
a

0.184

e-3

0.218

0.25

0.292

0.252

ud

0.275

0.877

0.818

0.50

2.5

0.50

0.887

0.823

e-3

0.75

ud

0.75

Search
1.00
Pass@1

1.00
Pass@1

Pass@1

Browser
1.00

## Page 8

8

t

0.00

rke

0.25

ma

1.00

al_

0.50

Figure 5: MCP Tool Run Success Rate By Category
Pay
1.00

0.75

0.50

0.25

0.00

Finance
ct

p

ma

ex
tra

ily-

tav

ily-

wl

Success Rate

Success Rate

File System

tav

cra

ily-

tav

h

se
arc

se
arc
h

ily-

tav

le-

0.00

lob

Map
go
og

fi
re les
ge ad_f
t_ ile
list
_d li file_
ire st_ inf
cto dir o
ry_ ect
wit ory
h_
siz
cre wri es
ate te_
_d file
ir
se ecto
arc ry
dir h_f
ec ile
tor s
y_
tre
e

0.25

_g

0.75

Success Rate

1.00
0.50

ce

0.00
e_

0.00
0.75

pri

0.25
ipl

0.25

ult

0.50

rea
d_
m

Success Rate

0.75

k_

0.50
1.00

toc

0.75

Success Rate

plaplayw
yw rig
pla plaright ht_p
_ u
playwrigywrigdele t
t
pu ywright_e ht_g e
pla ppe ht_ valu et
pla ywri teer navi ate
yw ght _na gat
rig _p v e
sta p ht_s ressigate
rt_ lay cre _k
co w en ey
de rig sh
ge ht_ ot
cle p pla n_se drag
ar_ lay yw ss
w
co rig righ ion
de h t_
ge t_s fill
n_ ele
se ct
ss
ion

Browser

t_s

Success Rate

1.00

ge

_s
c
m he
m a m
ma aps ps_wa_na
ps _r e vi
ma _se egeoathe
ps arc co r
m
ma a _tex h_d de
ps ps_ t_s eta
_a ip_ ea il
ro lo rc
m und ca h
ma
ps aps _se tion
_d ar
_
ma
m d
ps m aps irect ma istanch
_d a _d ion ps ce
ire ps ire _b _g
cti _d ct ic eo
on ire ion yc
_tr cti _d ling
an on_ riv
sit w ing
_in alk
teg ing
rat
ed
cre
ate
_s
ub
sc
rip
tio
n_
pla
cre
n
cre
ate
ate
_s
_
ord
hip
er
me
nt_
tra
ck
ing
cre
ate
_re
fun
cre
d
ate
_p
rod
uc
cre
t
ate
_in
vo
ice

ps

ma

Table 2: Evaluation of MCP Tool Call Abstract Syntax Tree (AST) and Pass@K
Browser
File System
Search
Model
AST Pass@1
AST Pass@1
AST Pass@1
GPT-4o
0.6524
0.2182 0.8863
0.8232 0.5200
0.4720
Qwen2.5-max
0.7262
0.2749 0.9419
0.8871 0.6280
0.4600
Claude-3.7-Sonnet 0.6503
0.1840 0.8415
0.8183 0.7280
0.6200
Kimi-K2-Instruct
0.8182
0.2524 0.9062
0.8772 0.7320
0.3680
Qwen3-coder
0.8866
0.2925 0.9080
0.8680 0.7180
0.5227
Map
Pay
Finance
Model
AST Pass@1
AST Pass@1
AST Pass@1
GPT-4o
0.6120
0.3616 0.7077
0.5742 0.7200
0.2889
Qwen2.5-max
0.7372
0.2272 0.6684
0.5277 0.7511
0.2556
Claude-3.7-Sonnet 0.5820
0.2748 0.7058
0.5574 0.7400
0.2311
Kimi-K2-Instruct
0.6088
0.2008 0.8071
0.6761 0.7156
0.2378
Qwen3-coder
0.7830
0.3054 0.7240
0.5440 0.7320
0.2860

MCP Tool Success Rate by Category

1.00

Search

0.75

0.50

0.25

0.00

## Page 9

is defined as whether the tool call is successfully executed, which is measured by several conditions
including whether the response status code contains success status codes (e.g., 200) and whether the
”success” key of the result dictionary in the MCP JSON RPC response is ”true”, etc. It is important
to note that the Tool Call Success Rate and Pass@K are closely related metrics. The key difference
between them lies in the following: Tool Call Success Rate only measures whether the tool call run
is successful without any errors, whereas Pass@K not only measures the success of the tool call run
but also the correctness of input parameters and whether the returned results (both the result data
and system messages) align with the expected ground truths.

4.2

R ESULTS

We reported the MCP tool call Abstract Syntax Tree (AST) and Pass@K scores on the evaluated
MCPToolBench++ benchmark in Table 2. We illustrate the AST results in Figure 3, Pass@K results
in Figure 4 and Tool Call Success Rate in Figure 5. From the result of Abstract Syntax Tree score
(function call tool choosing and parameters inferences), we can see that Qwen3-coder achieved top
AST accuracy performance in categories including Browser and Map. And Qwen2.5-max achieved
top AST accuracy performance in categories including File System and Finance. And Kimi-K2Instruct achieved top AST accuracy performance in categories of Search and Pay. To analyze the
Pass@1 tool call execution performance, Qwen3-coder achieved top Pass@1 score in the Browser
category. Qwen2.5-max achieved top Pass@1 score in the File System category. Claude-3.7-Sonnet
achieved top Pass@1 in Search category. GPT-4o achieved top Pass@1 in Map and Finance categories. And Kimi-K2-Instruct achieved the top Pass@1 in the Pay category.
4.2.1

AST S CORE VS . PASS @K

The AST score evaluates how well models choose among tools and make function calls by filling
parameters according to the tool schema and descriptions. After the LLM’s function call, Pass@1
further evaluates how well we actually run the MCP tool using the parameters inferred by the model.
We notice that the Tool Call Success Rate of MCP tool is one of the key variables influencing the
overall Pass@1 score, especially when the tools require API connections. To get more accurate
Pass@K score, we repeat the experiments multiple times and run multiple trials per each tool call.
In the experiments, we set the hyper-parameter of trials per tool call as 5.
Furthermore, we notice that the rankings of AST scores and Pass@K scores are not always positively
correlated. For example, in the Search category, Claude-3.7-Sonnet achieved second place in the
AST score (0.728) after Kimi-K2-Instruct (0.732). However, after actual tool call runs, Claude-3.7Sonnet achieved first place in Pass@1 (0.620) compared to Kimi-K2-Instruct (0.368). The results
showed that the Google Custom Search Tool (google-search) has a higher success rate than other
MCP search tool providers such as Tavily, etc. Additionally, Claude-3.7-Sonnet selects googlesearch more frequently than other tools compared to other models. This highlights situations, when
multiple tools with similar features (web-search, web-crawling, location-based map services) are
available, agent models may choose either of the tools and match the ground-truth labels for abstract
syntax tree scores, but have large gaps in final results after actually running the tools.

4.3

ERROR ROOT CAUSE ANALYSIS

We have done a detailed analysis of MCP tool call execution logs and categorize the error codes and
messages for each domain. The top ranked root causes of MCP tool call failures are summarized in
Figure 6, including ”Parameter Errors”, ”API Error”, ”Empty Result”, ”Session & Runtime Errors”,
etc. Also, each domain also has some specific errors. For example, the MCPs in ”MAP” domain
have errors ”parameters errors range invalid”, indicating the longitude and latitude values inferred
by LLM function calls are out of range, MCPs in ”Browser Use” domain have errors of ”No Such
File or Directory” when taking screenshots of webpage and saving to non-exist local filepaths, etc.
MCPs in ”Search” domain have URL processing errors from fetching and extracting the invalid
URL or URL needs second-time authentification of web contents, etc. We also list more detailed
examples of root causes of MCP tool call errors in the Appendix 4.
9

## Page 10

0.2

0.4
0.3
0.1

0.0

0.0

0.5
0.4
0.3

MAP
Errors
Parameters Error Value Invalid
API Error
Parameters Error Range Invalid
Http Request Fail

0.2

Errors
Edit File Error
Parameters Error
No Such File or Directory
Runtime Error

0.2

0.1

0.6

Percentage

0.5

FILE SYSTEM

0.6
0.5
0.4
0.3

0.6
0.5
Percentage

0.3

0.6

0.4
0.3

SEARCH
Errors
API Error
Empty Result
URL couldn't be processed
Parameters Error

0.2
0.1
0.0

PAY
Errors
API Error
Http Request Fail
Resource Not Found
Parameters Error

0.2

0.6

FINANCE

0.5
Percentage

0.4

Errors
Browser Executable Missing
Session Not Found
Parameters Error
Permission Directory Error
API Error

Percentage

Percentage

0.5

BROWSER

Percentage

0.6

0.4
0.3

Errors
API Error
Empty Result
Parameters Error
Runtime Error

0.2

0.1

0.1

0.1

0.0

0.0

0.0

Figure 6: MCP Tool Call Errors Root Cause Analysis

5

R ELATED W ORK

5.1

T OOL U SE AGENT

Tool use agents have accelerated the productivity and increase performance of many real-world
tasks. Coding agents8 (Gemini CLI (2025); OpenAI Codex (2025); Claude Code (2025)) apply
agentic function calls to manage, edit, generate codes using command lines to fulfill tasks. Deep
research agents (Gemini Deep Research (2025); OpenAI Deep Research (2025b)) utilize multiple
steps of tool uses including searching and crawling to generate detailed analysis of users’ complex
questions. Moreover, with the development of standardized model context protocol, more tools such
as search, browser use, location services can be integrated to LLM based systems.
5.2

F UNCTION C ALL AND MCP B ENCHMARKS

Function call benchmarks are crucial in evaluating tool use and function call capabilities of LLMs
and AI agent systems Mialon et al. (2023); Patil et al. (2024). GAIA is a benchmark to test Agent
tool use abilities of prompting and search Mialon et al. (2023). Berkeley Function Calling Leaderboard (BFCL) Patil et al. (2024) is a benchmark to test functions call of various programming languages, and uses Abstract Syntax Tree (AST) metric to evaluate the static accuracy of serial and
parallel functions. ComplexFuncBench Zhong et al. (2025) focus on the multi-step user constrained
function calling under long-context scenario. Some other research focus on generating high quality
datasets using pipelines from API repos (Liu et al. (2024)), and testing various capabilities such as
the browser use (Wei et al. (2025)).
With the adoption of model-context protocol, more MCP benchmarks are proposed (Luo et al.
(2025); Gao et al. (2025)) on different domain such as math, coding, etc.

6

C ONCLUSION

In this paper, we introduce MCPToolBench++ benchmark to evaluate LLM and AI Agents’ abilities
to use MCP tools correctly. The benchmark covers wide range categories of real world tools, which
provide multi-domains and multilingual supports. To scale the MCP tool benchmark preparation,
we introduce an automatic pipeline build upon mcp configs and tool schemas collected from open
MCP marketplaces. Additionally, multiple SOTA models are evaluated on the benchmarks. And
detailed success rate and root cause analysis of MCP tool call errors are conducted to highlight
future improvements.
8

https://www.deepnlp.org/store/ai-agent/coding-agent

10

## Page 11

R EFERENCES
Anthropic. Introducing claude 4, 2025a. URL https://www.anthropic.com/news/cla
ude-4.
Anthropic. System Card: Claude Opus 4 & Claude Sonnet 4. Technical report, Anthropic, 2025b.
URL https://www-cdn.anthropic.com/4263b940cabb546aa0e3283f35b68
6f4f3b2ff47.pdf. Accessed: July 4, 2025.
Claude Code. Claude Code: An agentic coding tool that lives in your terminal. https://gith
ub.com/anthropics/claude-code, 2025. Accessed: 2025-07-24.
Xuanqi Gao, Siyi Xie, Juan Zhai, Shqing Ma, and Chao Shen. Mcp-radar: A multi-dimensional
benchmark for evaluating tool use capabilities in large language models, 2025. URL https:
//arxiv.org/abs/2505.16700.
Gemini CLI. gemini-cli: An open-source ai agent that brings the power of gemini directly into your
terminal. https://github.com/google-gemini/gemini-cli, 2025. Accessed:
2025-07-24.
Gemini Deep Research. Gemini deep research overview, 2024. URL https://gemini.googl
e/overview/deep-research/.
Gemini Deep Research. Gemini Deep Research: Save hours of work with deep research as your
personal research assistant. https://gemini.google/overview/deep-research,
2025. Accessed: 2025-07-24.
Google DeepMind. Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality,
Long Context, and Next Generation Agentic Capabilities. Technical report, Google DeepMind,
2025. URL https://storage.googleapis.com/deepmind-media/gemini/ge
mini_v2_5_report.pdf. Accessed: July 4, 2025.
Zuxin Liu, Thai Hoang, Jianguo Zhang, Ming Zhu, Tian Lan, Shirley Kokane, Juntao Tan, Weiran
Yao, Zhiwei Liu, Yihao Feng, Rithesh Murthy, Liangwei Yang, Silvio Savarese, Juan Carlos
Niebles, Huan Wang, Shelby Heinecke, and Caiming Xiong. Apigen: Automated pipeline for
generating verifiable and diverse function-calling datasets, 2024. URL https://arxiv.or
g/abs/2406.18518.
Zhiling Luo, Xiaorong Shi, Xuanrui Lin, and Jinyang Gao. Evaluation report on mcp servers, 2025.
URL https://arxiv.org/abs/2504.11094.
Grégoire Mialon, Clémentine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun, and Thomas
Scialom. Gaia: a benchmark for general ai assistants, 2023.
Model Context Protocol (MCP). Model Context Protocol: Open protocol that standardizes how
applications provide context to llms. https://modelcontextprotocol.io/introd
uction, 2025. Accessed: 2025-07-24.
Moonshot AI. Kimi k2 instruct, 2025. URL https://huggingface.co/moonshotai/Ki
mi-K2-Instruct.
OpenAI. o3 and o4-mini System Card. System card, OpenAI, 2025. URL https://cdn.op
enai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-min
i-system-card.pdf. Accessed July 4, 2025.
OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red
Avila, Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul Baltescu, Haiming Bao, Mohammad Bavarian, Jeff Belgum, Irwan Bello, Jake Berdine, Gabriel Bernadett-Shapiro, Christopher
Berner, Lenny Bogdonoff, Oleg Boiko, Madelaine Boyd, Anna-Luisa Brakman, Greg Brockman, Tim Brooks, Miles Brundage, Kevin Button, Trevor Cai, Rosie Campbell, Andrew Cann,
Brittany Carey, Chelsea Carlson, Rory Carmichael, Brooke Chan, Che Chang, Fotis Chantzis,
Derek Chen, Sully Chen, Ruby Chen, Jason Chen, Mark Chen, Ben Chess, Chester Cho, Casey
11

## Page 12

Chu, Hyung Won Chung, Dave Cummings, Jeremiah Currier, Yunxing Dai, Cory Decareaux,
Thomas Degry, Noah Deutsch, Damien Deville, Arka Dhar, David Dohan, Steve Dowling, Sheila
Dunning, Adrien Ecoffet, Atty Eleti, Tyna Eloundou, David Farhi, Liam Fedus, Niko Felix,
Simón Posada Fishman, Juston Forte, Isabella Fulford, Leo Gao, Elie Georges, Christian Gibson, Vik Goel, Tarun Gogineni, Gabriel Goh, Rapha Gontijo-Lopes, Jonathan Gordon, Morgan
Grafstein, Scott Gray, Ryan Greene, Joshua Gross, Shixiang Shane Gu, Yufei Guo, Chris Hallacy, Jesse Han, Jeff Harris, Yuchen He, Mike Heaton, Johannes Heidecke, Chris Hesse, Alan
Hickey, Wade Hickey, Peter Hoeschele, Brandon Houghton, Kenny Hsu, Shengli Hu, Xin Hu,
Joost Huizinga, Shantanu Jain, Shawn Jain, Joanne Jang, Angela Jiang, Roger Jiang, Haozhun
Jin, Denny Jin, Shino Jomoto, Billie Jonn, Heewoo Jun, Tomer Kaftan, Łukasz Kaiser, Ali Kamali, Ingmar Kanitscheider, Nitish Shirish Keskar, Tabarak Khan, Logan Kilpatrick, Jong Wook
Kim, Christina Kim, Yongjik Kim, Jan Hendrik Kirchner, Jamie Kiros, Matt Knight, Daniel
Kokotajlo, Łukasz Kondraciuk, Andrew Kondrich, Aris Konstantinidis, Kyle Kosic, Gretchen
Krueger, Vishal Kuo, Michael Lampe, Ikai Lan, Teddy Lee, Jan Leike, Jade Leung, Daniel
Levy, Chak Ming Li, Rachel Lim, Molly Lin, Stephanie Lin, Mateusz Litwin, Theresa Lopez,
Ryan Lowe, Patricia Lue, Anna Makanju, Kim Malfacini, Sam Manning, Todor Markov, Yaniv
Markovski, Bianca Martin, Katie Mayer, Andrew Mayne, Bob McGrew, Scott Mayer McKinney,
Christine McLeavey, Paul McMillan, Jake McNeil, David Medina, Aalok Mehta, Jacob Menick,
Luke Metz, Andrey Mishchenko, Pamela Mishkin, Vinnie Monaco, Evan Morikawa, Daniel
Mossing, Tong Mu, Mira Murati, Oleg Murk, David Mély, Ashvin Nair, Reiichiro Nakano, Rajeev Nayak, Arvind Neelakantan, Richard Ngo, Hyeonwoo Noh, Long Ouyang, Cullen O’Keefe,
Jakub Pachocki, Alex Paino, Joe Palermo, Ashley Pantuliano, Giambattista Parascandolo, Joel
Parish, Emy Parparita, Alex Passos, Mikhail Pavlov, Andrew Peng, Adam Perelman, Filipe
de Avila Belbute Peres, Michael Petrov, Henrique Ponde de Oliveira Pinto, Michael, Pokorny,
Michelle Pokrass, Vitchyr H. Pong, Tolly Powell, Alethea Power, Boris Power, Elizabeth Proehl,
Raul Puri, Alec Radford, Jack Rae, Aditya Ramesh, Cameron Raymond, Francis Real, Kendra
Rimbach, Carl Ross, Bob Rotsted, Henri Roussez, Nick Ryder, Mario Saltarelli, Ted Sanders,
Shibani Santurkar, Girish Sastry, Heather Schmidt, David Schnurr, John Schulman, Daniel Selsam, Kyla Sheppard, Toki Sherbakov, Jessica Shieh, Sarah Shoker, Pranav Shyam, Szymon Sidor,
Eric Sigler, Maddie Simens, Jordan Sitkin, Katarina Slama, Ian Sohl, Benjamin Sokolowsky,
Yang Song, Natalie Staudacher, Felipe Petroski Such, Natalie Summers, Ilya Sutskever, Jie Tang,
Nikolas Tezak, Madeleine B. Thompson, Phil Tillet, Amin Tootoonchian, Elizabeth Tseng, Preston Tuggle, Nick Turley, Jerry Tworek, Juan Felipe Cerón Uribe, Andrea Vallone, Arun Vijayvergiya, Chelsea Voss, Carroll Wainwright, Justin Jay Wang, Alvin Wang, Ben Wang, Jonathan
Ward, Jason Wei, CJ Weinmann, Akila Welihinda, Peter Welinder, Jiayi Weng, Lilian Weng,
Matt Wiethoff, Dave Willner, Clemens Winter, Samuel Wolrich, Hannah Wong, Lauren Workman, Sherwin Wu, Jeff Wu, Michael Wu, Kai Xiao, Tao Xu, Sarah Yoo, Kevin Yu, Qiming
Yuan, Wojciech Zaremba, Rowan Zellers, Chong Zhang, Marvin Zhang, Shengjia Zhao, Tianhao
Zheng, Juntang Zhuang, William Zhuk, and Barret Zoph. Gpt-4 technical report, 2024. URL
https://arxiv.org/abs/2303.08774.
OpenAI Codex. OpenAI Codex: Lightweight coding agent that runs in your terminal. https:
//github.com/openai/codex, 2025. Accessed: 2025-07-24.
OpenAI Deep Research. Openai introducing deep research, 2025a. URL https://openai.c
om/index/introducing-deep-research/.
OpenAI Deep Research. OpenAI Deep Research: A new agentic capability that conducts multi-step
research on the internet for complex tasks. https://openai.com/index/introduci
ng-deep-research, 2025b. Accessed: 2025-07-24.
Shishir G. Patil, Huanzhi Mao, Charlie Cheng-Jie Ji, Fanjia Yan, Vishnu Suresh, Ion Stoica, and
Joseph E. Gonzalez. The berkeley function calling leaderboard (bfcl): From tool use to agentic
evaluation of large language models. In Advances in Neural Information Processing Systems,
2024.
Jason Wei, Zhiqing Sun, Spencer Papay, Scott McKinney, Jeffrey Han, Isa Fulford, Hyung Won
Chung, Alex Tachard Passos, William Fedus, and Amelia Glaese. Browsecomp: A simple yet
challenging benchmark for browsing agents, 2025. URL https://arxiv.org/abs/2504
.12516.
12

## Page 13

An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang
Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu,
Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin
Yang, Jiaxi Yang, Jing Zhou, Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang,
Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui
Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang
Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yinger
Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, and Zihan
Qiu. Qwen3 technical report. arXiv preprint arXiv:2505.09388, 2025.
Lucen Zhong, Zhengxiao Du, Xiaohan Zhang, Haiyi Hu, and Jie Tang. Complexfuncbench: Exploring multi-step and constrained function calling under long-context scenario, 2025. URL
https://arxiv.org/abs/2501.10132.

A

A PPENDIX

A.1

E XAMPLES OF MCP C ONFIGS AND S CHEMAS

In this section, we will use google-maps MCP to show you the format of the schema of servers, tools
and configurations.
1
2
3
4
5
6
7
8
9
10
11

{

1
2
3
4
5

{

6
7
8
9

1
2
3
4
5
6
7
8
9
10
11
12
13
14

"mcpServers": {
"google-maps": {
"command": "npx",
"args": ["-y", "@modelcontextprotocol/server-google-maps"],
"env": {
"Maps\_API\_KEY": "<YOUR\_API\_KEY>"
}
}
}
}

"id": "modelcontextprotocol/servers/google-maps",
"content_name": "Google Maps",
"category": "MAP",
"description": "The Google Maps MCP Server offers various tools for
interacting with the Google Maps API, including geocoding, place
searching, distance calculations, elevation data, and directions,
requiring a Google Maps API key for setup and usage with
platforms like Claude Desktop or VS Code.",
"website": "https://github.com/modelcontextprotocol/servers-archived",
"content": " .. README.md ...",
"github": "https://github.com/modelcontextprotocol/servers-archived"
}
{
"tools": [{
"name": "maps_directions",
"description": "Get directions between two points",
"input_schema": {
"type": "object",
"properties": {
"origin": {
"type": "string",
"description": "Starting point address or coordinates"
},
"destination": {
"type": "string",
"description": "Ending point address or coordinates"

13

## Page 14

},
"mode": {
"type": "string",
"description": "Travel mode (driving, walking, bicycling,
transit)",
"enum": [
"driving",
"walking",
"bicycling",
"transit"
]
}

15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33

},
"required": [
"origin",
"destination"
]
}
}]
}

A.2

MCP S ERVERS AND T OOLS B Y C ATEGORIES

In this section, we will list some of the top selected MCP servers and their tools by categories in the
MCPToolBench++ benchmark.
Table 3: MCP Servers By Various Categories
Category

Server

BROWSER

puppeteer/puppeteer

executeautomation/playwright

14

Tools
puppeteer navigate
puppeteer screenshot
puppeteer click
puppeteer fill
puppeteer select
puppeteer hover
puppeteer evaluate
playwright navigate
playwright screenshot
playwright click
playwright iframe click
playwright iframe fill
playwright fill
playwright select
playwright hover
playwright get
playwright post
playwright put
playwright press key
playwright save as pdf
playwright click and switch tab

## Page 15

Continue 3
Category

FILE SYSTEM
SEARCH

Server

modelcontextprotocol/filesystem
adenot/mcp-google-search

tavily/mcp tavily-mcp

mendableai/firecrawl-mcp-server

MAP

google-maps/google-maps

amap-amap-sse/amap-amap-sse

15

Tools
read file
read multiple files
write file
edit file
create directory
list directory
list directory with sizes
directory tree
search files
get file info
list allowed directories
search
read webpage
tavily-search
tavily-extract
tavily-crawl
tavily-map
firecrawl search
firecrawl scrape
firecrawl map
firecrawl crawl
firecrawl check crawl status
firecrawl extract
firecrawl deep research
firecrawl generate llmstxt
maps directions
maps geocode
maps reverse geocode
maps search places
maps place details
maps distance matrix
maps elevation
maps direction bicycling
maps direction driving
maps direction transit integrated
maps direction walking
maps distance
maps geo
maps regeocode
maps ip location
maps schema personal map
maps around search
maps search detail
maps text search
maps schema navi
maps schema take taxi
maps weather

## Page 16

Continue 3
Category

Server

baidu-maps/baidu-maps

PAY

FINANCE

A.3

paypal/paypal

alipay/alipay
AI-Hub-Admin/finance-agentmcp-server

Tools
map geocode
map reverse geocode
map search places
map place details
map directions matrix
map directions
map weather
map ip location
map road traffic
map poi extract
create invoice
create product
create subscription plan
create shipment tracking
create order
create refund
create-mobile-alipay-payment
create-web-page-alipay-payment
query-alipay-payment
refund-alipay-payment
query-alipay-refund
get stock price global market

MCP T OOL C ALL FAILURE ROOT C AUSE A NALYSIS

In this section, we will analyze the MCP Tool Call failure messages and summarize the results and
give the root cause analysis of the reasons MCP tool call failures.
Table 4: MCP Errors Root Causes Typical Examples
Category

Errors

BROWSER

Browser Executable Missing

FILE SYSTEM

Session Not Found
Parameters Error
Edit File Error
Parameters Error
No Such File or Directory
Runtime Error

SEARCH

API Error
Parameters Error
Empty Result

16

Logs
Failed to initialize browser: browserType.launch:
Executable doesn’t exist at ./xxx/ms-playwright/
chromium-1179/chrome-mac/Chromium.app/
Contents/MacOS/Chromium
Failed to end codegen session:
Session sessionXYZ not found
all values empty, missing values
Error: Could not find exact match for edit: Project Overview
all values empty, missing values []
Error: ENOENT: no such file or directory, open
’./test project root/data/test file txt 1.txt’
read() called while another coroutine
is already waiting for incoming data
Tavily API error: Request failed with status code 432
Error during query to tavily-mcp: Separator
is not found, and chunk exceed the limit
Internal error: Error calling tool ’tavily crawl’: 400
Error during query to tavily-mcp: Separator
is found, but chunk is longer than limit
Input validation error: ’url’ is a required property
””

## Page 17

Category

MAP

PAY

Finance

A.4

Continue 4
Logs
origin or destination is invalid
Geocoding API error: input ‘origin‘ invaild,
Parameters Error Value Invalid
please reinput more detail address
API Error
API response error: unkown error
Parameters Error Range Invalid The range of input latitude and longitude is invalid
Error: request to https://maps.googleapis.com/maps
/api/geocode/json?xxxx failed, reason: Client
network socket disconnected before secure
Http Request Fail
TLS connection was established
PayPal API error (404): [object Object]
API Error
PayPal API error (400): [object Object]
Http Request Fail
Request failed with status code 400, type: paypal error
Parameters Error
Converting circular structure to JSON
Resource Not Found
The specified resource does not exist
API Error
Connection Timeout
Empty Result
”data”: []
{”symbol list”: [”NSE INDIA.RELIANCE”],
”market”: ”NSE INDIA”}
{”symbol list”: [”3690.HK”],
Parameters Error
”market”: ”HK”}
Errors

P ROMPT
Tool Call Chain Filter Prompt
## Role
You are an expert in tool call link identification. You can judge the rationality of the tool
list provided by the user. If a task of an ordinary user calls all the tools in the list, it is
logically unreasonable, and the judgment is no.
## Steps
1. The user provides a tool list, which contains N tools. Each tool contains three fields:
name, description, and parameters, which represent the name, description, and parameters
of the tool.
2. Determine whether there is any unreasonable place in the tool list provided by the user,
such as the existence of completely irrelevant tools. Generally, a task of a user does not
need them at the same time.
3. If it is reasonable, return ”1”, otherwise return ”0”.
## Output format
Only output one character, ”1” or ”0”, do not output anything else.

Query Generator Prompt
## Role
You are an expert in generating tool call agent samples, responsible for creating user questions and tool call samples based on the tools list provided by the user.
## Steps
1. The user provides a tools list containing N tools, which may include repetitions.
Carefully understand the purpose of each tool by examining its name and description.
”Required” indicates the necessary parameters for executing the tool, and ”type” specifies
the data type limitation for the parameter content.

17

## Page 18

2. Design a logical tool call sequence. Generate a suitable query template, placed in
the <query> field, that necessitates calling the user-provided tools to complete the task.
Utilize all provided tools collectively, and each tool can be called multiple times.
3. Hollow out some variables in the template, and then fill in different variable values.
The variable name format is <query xxx>, for example, ”How far is the distance from
<query locationA> to <query locationB> ?”
4. Specify the order and parameters for the tools that need to be called for each query
template. Ensure that the parameter content type matches the type specified in the tools
list. Adhere to the principle of parameter minimization, avoiding redundant parameters.
All ”required” parameters must be provided, along with any parameters necessary to
fulfill the query requirements. Variables involved in the query should retain the same
variable name. Place this information in the ”function call label” field.
5. Outline the tool calling steps, starting from ”1” to indicate the execution order. If tools
can be called concurrently, assign them the same <step> number.
6. Assign a unique tool number <id> , starting from ”1” to each tool, ensuring each tool
has a distinct index.
7. If there’s a dependency between tools requiring the output of a previous step as input,
use a variable name for the input, prefixed with the tool number. The variable name
format should be <id result>, such as <1 result>.
## Output format requirements
1. Strictly adhere to the following JSON format for the response, which includes three
fields: query template, call function list and its parameters, and all variable names with
their candidate values from the query template:
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32

{
"query": "How far is the distance from <query_locationA> to
<query_locationB>?",
"function_call_label": [{
"name": "Function Name 1",
"arguments": {
"Parameter 1": "<query_locationA>"
},
"step": "1",
"id": "1",
"mcp_server": "mcp1"
}, {
"name": "Function Name 1",
"arguments": {
"Parameter 1": "<query_locationB>"
},
"step": "1",
"id": "2",
"mcp_server": "mcp1"
}, {
"name": "Function Name 2",
"arguments": {
"Parameter 1": "<1_result>",
"Parameter 2": "<2_result>"
},
"step": "2",
"id": "3",
"mcp_server": "mcp2"
}],
"variable_optional_collection": {
"query_locationA": ["New York", "JFK International
Airport", "Los Angeles"],
"query_locationB": ["Potala Palace", "San Francisco"]
}

18

## Page 19

33

}

Post-Processing Query Rewriting and Validation Prompt
## Role You are an expert in user query rationality checks and rewriting, responsible for
two tasks based on the query and function call label provided by the user:
### Task 1. Rewrite the query to align with typical user questions
#### Steps
1. The user provides a query. Determine whether the sentence contains uncommon special
proper nouns (e.g., stock codes, geographic location numbers, longitude and latitude) that
do not conform to how a general user would ask a question. For instance, a common user
question for ”What is the current stock price of AAPL?” would be ”What is the current
stock price of Apple?”.
2. If there are special proper nouns that can be handled by the large model’s endogenous
knowledge (e.g., the correspondence between cities and postal codes), then map and
rewrite these uncommon special proper nouns into common words. For example, rewrite
postal codes into city names and POI ID into place names.
3. Rewrite the entire sentence to ensure the language is fluent and closer to everyday
user questions. Be careful not to alter the original meaning of the sentence or omit any
information. Return the complete, rewritten query.
#### Notes
1. If the query is already reasonable, output it as is without any changes.
2. Do not change the original meaning of the query, and do not expand or add other
content.
3. It is better not to change it than to make a mistake: Do not be overly confident. If
the information in the query cannot be determined by endogenous knowledge, or if the
information might be outdated, do not rewrite it; output it as is.
4. If function call list similar is empty, function call list similar rewritten should be
an empty JSON.
5. If some parameters of function call list do not exist in the format of similar tools, those
parameters will not be generated in the similar tools. Ensure that the tool’s parameters
conform to the specified format.
### Task 2. Determine the rationality of the query
#### Steps
1. Now we have the query after it has been rewritten by the first function. The original
query is often randomly generated by users based on certain templates, and it may contain
many unreasonable elements. You need to analyze it carefully and provide a judgment.
2. If this query is reasonable, return ”1”; otherwise, return ”0”.
3. Examples of unreasonable queries, Unreasonable requests, such as ”Driving from
Earth to Mars” or ”Walking from the United States to China”.
4. Made-up URLs, made-up locations, and other non-existent content, such as ”Extract
the basic content from https://***.com/”.
5. Logically unreasonable queries, such as ”Query the route from Hangzhou to Hangzhou”
where the starting point and endpoint are the same.
6. Asking questions using uncommon special codes, such as ”What are the details for the
location identified by postal code Q017?” or ”What is the current stock price of AAPL?”.
#### Notes
The reasonableness check is performed based on the rewritten query.

19

## Page 20

#### Output format
The output must be in standard parseable JSON format, and do not include explanations
or any other content.
1
2
3
4

{
"query_rewritten": "Rewritten query",
"reasonableness_checks": "1"
}

20
