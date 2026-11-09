---
id: literature/fulltexts/mastouri2025automcp
type: fulltext
status: frozen
language: en
key: mastouri2025automcp
title: >-
  From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents
resource: https://arxiv.org/abs/2507.16044
description: >-
  The Model Context Protocol (MCP) is emerging as a standard interface through which LLM agents invoke external tools, and a growing ecosystem of MCP servers now mediates access to vendor services.
pages: 44
words: 22605
year: 2025
venue: >-
  
authors: >-
  Mastouri, Meriem; Ksontini, Emna; Barrak, Amine; Kessentini, Wael
doi: 
oa_status: arxiv 2507.16044
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

## Page 1

From REST to MCP: An Empirical Study of API Wrapping and
Automated Server Generation for LLM Agents

arXiv:2507.16044v4 [cs.SE] 6 Apr 2026

MERIEM MASTOURI, Grand Valley State University, USA
EMNA KSONTINI, University of North Carolina Wilmington, USA
AMINE BARRAK, Oakland University, USA
WAEL KESSENTINI, DePaul University, USA
The Model Context Protocol (MCP) is emerging as a standard interface through which LLM agents invoke
external tools, and a growing ecosystem of MCP servers now mediates access to vendor services. Most of these
servers target vendors that already expose REST APIs, yet the relationship between MCP tool interfaces and
the underlying API surface has not been empirically characterised. This paper presents the first large-scale
study of MCP server construction. We analyse 116 official servers to determine REST reliance and integration
strategies (RQ1); examine servers paired with OpenAPI specifications to quantify operation exposure, omission,
and mapping patterns (RQ2); evaluate automated generation from 80 real-world OpenAPI contracts (RQ3);
and assess specification repair and tool-set transformations to improve correctness and reduce complexity
(RQ4). We find that 88.6% of servers are fully or partially REST-backed, with 92% implementing tools as bare
API wrappers. MCP servers expose a median of 19% of available operations, following systematic patterns
predictable from the specification. Baseline generation succeeds for 76% of sampled tools; automated repair
raises this to 94.2%, while filtering and regrouping reduce the median tool count per API by one-third. We
release AutoMCP, an end-to-end pipeline integrating specification repair and empirically grounded tool-set
transformations.
Additional Key Words and Phrases: Model Context Protocol, MCP, OpenAPI, REST API, tool-augmented LLMs,
Agents, specification repair
ACM Reference Format:
Meriem Mastouri, Emna Ksontini, Amine Barrak, and Wael Kessentini. 2026. From REST to MCP: An Empirical
Study of API Wrapping and Automated Server Generation for LLM Agents. ACM Trans. Softw. Eng. Methodol.
0, 0, Article 0 ( 2026), 44 pages. https://doi.org/XXXXXXX.XXXXXXX

1

INTRODUCTION

Large language models are increasingly deployed as autonomous agents that plan, reason, and act
by invoking external tools [61, 74]. The breadth of services an agent can operate on is determined by
the tool interfaces available to it: machine-readable contracts that specify what each tool does, what
arguments it accepts, and how it authenticates. As the number and diversity of target services grow,
constructing and maintaining these interfaces has become a recognised engineering bottleneck [13],
motivating protocol-level solutions that standardise how tools are described, discovered, and
invoked.
Authors’ addresses: Meriem Mastouri, Grand Valley State University, MI, USA, mastourm@mail.gvsu.edu; Emna Ksontini,
University of North Carolina Wilmington, NC, USA, ksontinie@uncw.edu; Amine Barrak, Oakland University, MI, USA,
aminebarrak@oakland.edu; Wael Kessentini, DePaul University, IL, USA, wkessent@depaul.edu.
Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and
the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored.
Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
prior specific permission and/or a fee. Request permissions from permissions@acm.org.
© 2026 Association for Computing Machinery.
1049-331X/2026/0-ART0 $15.00
https://doi.org/XXXXXXX.XXXXXXX
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 2

0:2

Mastouri et al.

1 # GET /search/repositories
2 parameters:
3
- name: q
4
in: query
5
required: true
6
schema: { type: string }
7
- name: sort
8
in: query
9
required: false
10
schema:
11
type: string
12
enum: [stars, forks,
13
help-wanted-issues, updated]
14
- name: order
15
in: query
16
schema:
17
type: string
18
enum: [desc, asc]

(a)
GitHub
/search/repositories [24]

1 Tool{
2
Name: "search_repositories",
3
Description: "Find GitHub repositories by name,
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

OpenAPI—GET

description, or topics.",
ReadOnlyHint: true,
InputSchema: Schema{
Type: "object",
Properties: {
"query":
{Type: "string",
Required: true},
"sort":
{Type: "string",
Enum: ["stars","forks", "help-wantedissues", "updated"]},
"order":
{Type: "string",
Enum: ["asc","desc"]},
},
},

14
15
16
17
18
19 }
20 // Handler:
21 result, _, _ :=
22
client.Search.Repositories(
23
ctx, query, opts)

(b) GitHub
tool [23]

MCP

tool—search_repositories

Fig. 1. The GET /search/repositories endpoint from GitHub’s OpenAPI specification (a) and the corresponding MCP tool from the official GitHub MCP server (b) [23]. Parameter names, types, and enumerations
are preserved across both representations; the tool handler delegates directly to the vendor REST API.

The Model Context Protocol (MCP) [5] is the most widely adopted of these solutions. MCP
defines a schema-driven JSON-RPC interface through which servers expose callable tools and
clients invoke them in a uniform message format, decoupling agent logic from service-specific
implementation. Major platforms, such as GitHub, Notion, Slack, among others, now publish official
MCP servers, and public registries [18, 45] catalogue hundreds more.
A closer look at publicly available MCP servers reveals a striking resemblance to existing
service APIs. Figure 1 juxtaposes a snippet from GitHub’s OpenAPI specification for the GET
/search/repositories endpoint with the corresponding tool definition from the official GitHub
MCP server [23]. The structural correspondence is immediate: parameter names, types, and enumerations are preserved almost verbatim, and the tool handler delegates directly to the vendor REST
API. More broadly, the capabilities that MCP servers advertise, managing repositories, sending
messages, querying dashboards, closely mirror what these vendors already expose through their
public REST APIs. At the same time, the scale of the two interfaces differs markedly. GitHub’s REST
API defines over 600 operations1 , while its MCP server exposes 51 tools2 . Slack’s API comprises
over 200 methods3 , yet its MCP server surfaces only 8 tools4 . These observations raise questions
that have not been empirically investigated: what is the relationship between MCP servers and the
REST APIs offered by the same vendors? What determines which operations are surfaced as tools
and which are not? And do the resulting tool sets reflect systematic design principles or ad hoc
developer choices?
1 https://github.blog/news-insights/product-news/introducing-githubs-openapi-description/
2 https://github.com/github/github-mcp-server
3 https://api.slack.com/methods
4 https://github.com/modelcontextprotocol/servers/tree/main/src/slack

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 3

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:3

The answers to these questions have practical implications beyond documentation of developer
practice. Real-world REST APIs routinely define large operation surfaces, with public corpora
reporting medians in the tens and long tails reaching hundreds of endpoints [25, 51]. Recent
evaluations consistently show that LLM tool-selection accuracy degrades as the number of available
tools grows, with reported losses of up to 85% [36, 65]. How MCP server developers navigate
the tension between API coverage and agent usability is therefore a design problem with direct
implications for agent reliability.
Moreover, the structural resemblance between OpenAPI endpoint definitions and MCP tool
schemas echoes a pattern that software engineering has exploited before: tools such as Swagger
Codegen and OpenAPI Generator already compile API specifications into clients, server stubs,
and SDKs [54, 68]. Whether the correspondence extends to MCP tool generation, and whether it
survives the diversity of real-world APIs and the known quality issues of their specifications, is a
question that requires empirical investigation.
A growing body of work has begun to examine the MCP ecosystem, but from complementary angles that leave these questions open. Security analyses have catalogued threats across the
server lifecycle [35]. Fault taxonomies have classified recurring defect patterns in server implementations [70]. Measurement studies have profiled ecosystem health and transport adoption [29].
Description-quality studies have identified smells in tool metadata [31]. However, the relationship
between MCP servers and the service APIs they target, the exposure and mapping decisions their
developers make, and whether the construction process can be systematised remain unstudied.
This paper provides the first empirical investigation of MCP server construction. We analyse
116 real-world MCP servers drawn from official listings and community registries, characterising
their architecture, service-integration strategies, and configuration practices (RQ1). For the servers
whose vendor APIs have publicly available OpenAPI specifications, we examine how REST operations are translated into MCP tools, quantifying coverage, documenting omission patterns, and
identifying the mapping structures developers employ (RQ2). Building on these empirical findings,
we investigate whether MCP server construction can be derived from OpenAPI specifications
by generating servers from 77 real-world specifications and cataloguing the defects that prevent
faithful generation (RQ3). Guided by the design patterns uncovered in RQ1–RQ2 and the defect taxonomy from RQ3, we introduce AutoMCP, an end-to-end pipeline combining specification-driven
generation, specification repair, and empirically grounded tool-set transformations (RQ4).
The remainder of this paper is organised as follows. Section 2 reviews related work. Section 3
describes the study design, dataset construction, and the AutoMCP framework. Section 6 presents
findings across the four research questions. Section 7 discusses threats to validity. Section 8 concludes.
Replication Package. All materials are available at [43].
2

RELATED WORK

This section reviews three areas of prior work relevant to our study.
2.1

MCP Protocol-Based Tool Invocation for Language Model Agents

Recent work has begun to examine the MCP ecosystem from several complementary perspectives.
Hou et al. [35] analyse security threats across the MCP server lifecycle, showing that protocol
standardisation alone does not produce a uniform security posture; risks arise from server-level
implementation, credential management, and capability-exposure decisions. Hasan et al. [30]
conduct the first large-scale assessment of MCP server health, evaluating 1,899 open-source servers
for security vulnerabilities and maintainability concerns. Taraghi et al. [70] present the first fault
taxonomy for MCP software, identifying five high-level categories of defects through analysis of
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 4

0:4

Mastouri et al.

server implementations and practitioner surveys. Guo et al. [29] profile the ecosystem at scale,
collecting 17,630 entries across six registries and analysing 8,401 valid projects for structural health,
transport adoption, and client–server distribution patterns. Hasan et al. [31] study tool description
quality, finding that 97.1% of the 856 tools analysed contain at least one description smell, with 56%
failing to state their purpose clearly.
These studies collectively address the security, reliability, ecosystem health, and description
quality of MCP servers. None, however, examines how MCP servers relate to the service APIs they
target: what operations they expose or omit, what mapping patterns their developers apply, or
whether their construction follows regularities amenable to automation. Our work addresses this
gap through the first empirical characterisation of MCP server construction and its relationship to
vendor REST APIs.
2.2

LLM Tool Use and Selection at Scale

Enabling language models to invoke external tools has been a central focus of recent research.
Schick et al. [61] demonstrate that language models can learn to use tools autonomously through
self-supervised training, while Yao et al. [74] show that interleaving reasoning traces with toolinvocation actions improves task completion in multi-step settings. These foundational results have
motivated a line of work on scaling tool use to large and heterogeneous inventories. Patil et al. [56]
train a model to select and parameterise calls from a corpus of over 1,600 API endpoints, focusing on
reducing hallucinated or malformed invocations. Qin et al. [59] extend this direction to over 16,000
real-world APIs, introducing a decision-tree search strategy for multi-tool planning. Du et al. [19]
propose a hierarchical agent architecture that decomposes complex tasks into API call sequences
using self-reflection.
Benchmarking efforts have formalised the evaluation of tool-use capabilities. Li et al. [41]
introduce API-Bank, a benchmark requiring models to select, invoke, and compose API calls to
complete multi-step tasks. Chen et al. [14] propose T-Eval, which decomposes tool utilisation into
fine-grained sub-skills: plan generation, argument completion and response interpretation, and
evaluates each independently.
A recurring finding across this literature is that tool-selection accuracy degrades as the number
of available tools grows. Kate et al. [36] report performance losses of 7–85% as tool catalogue
size increases. Shi et al. [65] show that even strong retrieval models fail on tool retrieval tasks,
degrading downstream task completion. These results establish that the size and composition of
the tool set presented to a model directly affect agent reliability.
This body of work treats the tool interface as a given input and studies how models interact
through it. Our work is complementary: we study how that interface is designed and constructed,
and we address the tool-set scalability problem from the supply side by introducing empirically
grounded filtering and grouping transformations that reduce the number of tools presented to the
model.
2.3

REST-to-Tool Construction and Specification Quality

Research on connecting language models to REST APIs has focused on consumption: translating
intent into request sequences [69], modelling inter-endpoint dependencies [38, 40], and selecting
endpoints from large inventories [56]. These approaches assume the tool interface exists.
On the construction side, Ni et al. [52] propose ToolFactory, which synthesises callable wrappers from natural-language API documentation, targets non-MCP interfaces and does not address
tool-set scalability. Within the MCP ecosystem, FastMCP [58], the most starred adopted community framework, supports OpenAPI-to-MCP translation, but as a development library rather
than an end-to-end pipeline. Developers must manually specify server base url, authentication
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 5

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:5

Table 1. Comparison with existing approaches.

Approach type
Produces MCP server
Uses OpenAPI as input
Auth. & server config.
No API knowledge required
Spec. defect handling
Tool-set reduction
Evaluation scope

ToolFactory [52]

FastMCP [58]

AutoMCP

LLM-based
×
×
Manual
×
×
×
1 domain

Dev. library
✓
✓
Manual
×
×
×
×

End-to-end pipeline
✓
✓
Automated
✓
Detect + repair
Filter + group
77 APIs

schemes, and transport settings, information already encoded in the specification’s servers and
securitySchemes fields, making the process impractical across multiple APIs. FastMCP performs
one-to-one endpoint-to-tool translation without filtering or grouping, and does not handle specification defects. Users report generation failures for POST endpoints with complex payloads [2, 3],
crashes on circular schema references [4], and context-window overflow from verbose tool descriptions [1]. Table 1 summarises the differences.
Any specification-driven approach depends on specification quality, which empirical research
has shown to be uneven [7, 25]. Incomplete security declarations, undocumented parameters, and
specification–implementation mismatches are documented across public OpenAPI corpora [72].
The same defect classes impede MCP server generation, yet no prior work has addressed their
detection and repair in this context. AutoMCP bridges this gap: it requires no API-specific developer
knowledge, extracts all configuration from the specification, repairs its defects automatically, and
applies empirically grounded tool-set transformations, evaluated across 77 real-world APIs.
3
3.1

STUDY DESIGN
Research Questions and Study Overview

In this paper, we investigate four research questions (RQs) designed to provide a structured examination of MCP server design and automation. Specifically, we seek to answer the following
questions:
• RQ1: To what extent do MCP servers rely on vendor REST APIs, and what integration
strategies and configuration practices do they adopt?
• RQ2: How are vendor REST API operations translated into MCP tools, in terms of exposure,
omission, and mapping patterns?
• RQ3: To what extent can REST-backed MCP servers be automatically generated from OpenAPI specifications, and what factors prevent faithful tool generation?
• RQ4: How effective are automated specification repair and tool-set transformations in
addressing generation failures and tool-set explosion?
Figure 2 presents an overview of our study design, outlining the multi-stage analysis conducted
to answer the four research questions. (RQ1) characterizes how MCP servers rely on and integrate
REST APIs in practice. (RQ2) builds on this by examining how API functionality is exposed at the
tool level. (RQ3) then evaluates the extent to which such servers can be generated automatically
from OpenAPI specifications. Finally, (RQ4) addresses the limitations identified in RQ3 through
specification repair and tool-set transformations.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 6

0:6

Mastouri et al.

Characterizing
integration
strategies

87 REST-backed
MCP server
345 Official MCP
server repo

Filtering
Open source
>10 Github stars
Vendor has Rest API

Determining
REST reliance

116 MCP
server repo

14 Partially REST-backed
MCP server

13 Non-REST-backed
MCP server

42 MCP server repo
87 REST-backed
MCP server

Filtering
REST API has a
published OpenAPI spec

42 OpenAPI Spec

APIs Stratified
Sampling
Auth + Size

Characterizing
REST
configuration

Characterizing
Mapping Structure

#Tools

77 APIs
8890 Operation

AutoMCPbasline

77 Servers
8890 Tool

42 OpenAPI (RQ2)

6966 operations

Else

20

Measuring
inclusion and
omission per category

22 Servers
177 Tools

Tools Call
Sequence
Generation

55 Servers
8713 Tools

55 Servers
2013 Tools

RQ1: REST reliance,
integration, and
configuration in
MCP servers

Transport mechanism
tool selection capability

One-to-one
many-to-one

Extracting Operation
Categories
(Structural & Semantic)

Extracting
Augmentation
taxonomy

API access configuration

968 Tools

6966 operations

50 OpenAPI
5 070 endpoints

Establishing
Tool–Operation
alignment

7 Custom API client
MCP server
80 Bare API consumption
MCP server

one-to-many

77 Servers
2190 Tools

RQ2: REST operation
exposure, omission,
and mapping patterns
in MCP tools

Identifying
Aggregation
patterns

Manual
Testing

Failure
Analysis

RQ3: Feasibility and
Limitations of
Automatic MCP Tool
Generation from
OpenAPI Specifications

1666 Tools Success
524 Tools Failure )

Tools
Sampling
SpecFix

77 APIs

8890 tools (RQ3)

Tool-Set
Transformations

AutoMCPbasline

77 servers
6768 tools

Tools
Sampling
(RQ3)

77 Servers
2190 Tools

Manual
Testing

2063 Tools Success
127 Tools Failure

RQ4: Effectiveness of
Automated Repairs
and Tool-Set
Transformation for
OpenAPI-Driven MCP
Generation

Fig. 2. Approach overview and addressed RQs.

3.2

Data Collection

Our study relies on three related datasets constructed to support the analyses for RQ1 through
RQ4.
For RQ1, we started from the official MCP server catalogue maintained by Anthropic as of
July 31, 2025 [46], which listed 345 publicly accessible MCP servers. After removing entries that did
not correspond to actual source-code repositories (e.g., documentation stubs, placeholder listings,
or non-functional demonstrations), 279 repositories remained. We then restricted the dataset to
the 165 repositories whose vendors publish a publicly documented REST API, since these systems
are capable of expressing REST functionality through MCP tools. To focus on mature and nontrivial implementations, we excluded repositories with fewer than 10 GitHub stars. Prior empirical
software engineering studies commonly use star counts as indicators of project maturity and
community engagement [9, 73]. This filtering step yielded a final dataset of 116 MCP server
repositories for RQ1.
For RQ2, we required both an MCP server implementation and a machine-readable API specification. We therefore selected the subset of the RQ1 corpus for which the vendor publishes an official
OpenAPI specification. This process resulted in 42 MCP servers with corresponding OpenAPI
contracts, forming the dataset used for all mapping analyses.
RQ3 and RQ4 evaluate AutoMCP, which requires a broader and more diverse set of API
specifications than the MCP-focused dataset used in RQ1–RQ2. To construct this extended dataset,
we combined the 42 APIs from RQ2 with a stratified random sample of 50 OpenAPI 3.x specifications
drawn from two large public API collections: APIs.guru and the Konfig dataset. After deduplication
and removal of syntactically invalid specifications, these sources provided 3,784 unique machinereadable OpenAPI contracts.
We performed stratified sampling based solely on metadata that can be computed automatically:
authentication scheme (none, API key, basic/bearer, OAuth 2.0) and specification size. Size buckets
were defined empirically using endpoint-count percentiles: small (≤20 operations), medium (21–
100), and large (>100). Random sampling without replacement continued until each {authentication,
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 7

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:7

size} cell was represented and the target sample size of 50 specifications was reached. To support
reconstruction-fidelity evaluation, we augmented the stratified sample with the 42 APIs from
RQ2. After deduplication, the resulting evaluation corpus for RQ3–RQ4 consisted of 80 unique
OpenAPI specifications.
4
4.1

RQ-SPECIFIC METHODOLOGY
RQ1: To what extent do MCP servers rely on vendor REST APIs, and what REST
integration strategies and configuration practices do they adopt?

Motivation. As MCP is promoted as an open standard for connecting LLM applications to external
tools and data sources via MCP servers, a growing set of “official integrations” is being published
as reference/maintained servers in public repositories and registries [46]. In practice, many of
these official servers appear to target the same underlying vendor capabilities already available
via their public REST APIs. Yet, we lack empirical evidence on whether official MCP servers are
predominantly REST-backed wrappers (and whether REST is used uniformly across tools or only
selectively) or whether other backends dominate. Moreover, even among REST-backed servers, it is
unclear how REST capabilities are integrated into tool implementations, specifically, whether tools
primarily perform bare API access or instead incorporate additional adaptation/augmentation logic
beyond routine API access, and which configuration practices (e.g., authentication and transport
setup, tool filtering) are adopted in practice.
Approach. To answer RQ1, we analyze the 116 MCP servers described in Section 3.2. We
conducted a two-stage manual analysis to (i) determine the extent to which each server relies on
the vendor REST API and (ii) characterize, for REST-backed servers, the concrete REST integration
strategies and configuration practices used in implementation.
Stage 1: Determining REST reliance. Two authors independently inspected each repository using
a fixed trace procedure, with a third author involved in the adjudication. First, we identified all
tools exposed by the server by locating tool registration and handler dispatch points. Second, for
each tool, we traced the implementation from the handler entry point to the first external-service
interaction by following function calls and imported modules. Third, we determined whether the
interaction targets the vendor’s REST API by inspecting request destinations (e.g., base URLs/hosts),
API client initialization code, and dependencies indicative of vendor SDKs or HTTP clients. Based
on these tool-level traces, each repository was labeled as REST-backed (all tools invoke the vendor
REST API), partially REST-backed (only a subset of tools invoke the vendor REST API), or non-RESTbacked (no tool invokes the vendor REST API). Inter-rater reliability on the pre-consensus labels
was assessed using Cohen’s kappa for nominal categories (κ = 0.87). Disagreements were resolved
through an evidence-based adjudication workflow: the two raters exchanged written justifications
grounded in concrete code artifacts (file paths, functions, imports, and call sites) and then held a
reconciliation meeting.
Stage 2: Characterizing REST configuration and integration strategies. For repositories labeled RESTbacked, we analyzed two complementary aspects: (i) configuration practices governing authentication, transport, and tool exposure, and (ii) integration strategies describing how REST API calls are
incorporated into tool implementations. We conducted an exhaustive manual review using a structured coding protocol and a shared codebook. From the 87 REST-backed servers identified in Stage 1,
we randomly selected 25 for a Stage 2 pilot and had all three authors code them independently. We
compared pilot results to refine the protocol’s operational definitions and decision rules. Coders
inspected each repository in a fixed order: (1) tool handler implementations, (2) end-to-end call
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 8

0:8

Mastouri et al.

paths from handlers to external interactions (including client construction and request execution),
and (3) configuration artifacts and initialization code. We then split the remaining 62 repositories
across authors (≈ 20 each), holding periodic calibration meetings and escalating ambiguous cases
for consensus.
(i) Configuration practices. Across all REST-backed repositories, we first documented configuration practices relevant to API access and execution context by examining configuration files,
environment variable templates, and initialization code. Concretely, we coded (i) API access configuration (credential provisioning/authentication setup and how credentials are supplied), (ii) transport
mechanism support (STDIO, HTTP, SSE, or combinations), and (iii) tool selection/filtering capability
(whether subsets of tools can be enabled, disabled, or filtered via configuration or registration
logic). Reliability for these repository-level labels was assessed on pre-consensus pilot labels using
Krippendorff’s α (α auth-config = 0.94, α transport = 0.96, α tool-filtering = 0.90), after which disagreements
were reconciled using code-grounded evidence.
(ii) Integration strategies (bare vs. custom). We then characterized REST integration strategies
at the tool level by distinguishing whether a tool’s implementation performs only API access or
API access plus additional custom logic. A tool was labeled bare API consumption when its logic
primarily (i) maps tool parameters to an external operation, (ii) issues the request/command, and
(iii) returns the external response with at most routine client concerns (e.g., authentication setup,
request formatting, pagination traversal, and error handling). In contrast, a tool was labeled custom
API client when it routes external interactions through a repository-defined client/wrapper that
performs non-trivial integration logic beyond routine API access, i.e., intermediate processing that
materially alters how vendor capabilities are invoked or combined beyond standard request/response
handling. Reliability for the bare vs. custom tool label was assessed on pre-consensus pilot labels
(Krippendorff’s α bare/custom = 0.85), followed by reconciliation among the three authors using
concrete call sites, imports, and execution traces as evidence. Finally, we lifted tool-level labels to
the server level using an existence rule: a server was labeled custom API client if it contained at
least one tool labeled custom API client; otherwise, it was labeled bare API consumption.
(ii-a) Invocation mechanisms for bare API consumption MCP servers. For MCP servers
labeled bare API consumption, we further coded the concrete invocation type used to access vendor capabilities as direct HTTP (e.g., fetch, requests), SDK-based (vendor/third-party SDKs),
specification-driven (e.g., OpenAPI-generated clients), or CLI-based (invoking vendor CLIs via subprocess execution). Reliability for this multi-class label was assessed on pre-consensus pilot labels
(Krippendorff’s α bare-subtype = 0.83), followed by consensus reconciliation grounded in concrete call
sites and dependency evidence.
(ii-b) Augmentation taxonomy for custom API client MCP servers. Finally, tools labeled
custom API client were flagged for additional characterization to capture augmentation logic beyond
routine API access. While coding the non-pilot repositories, coders marked every custom API client
tool for follow-up. After primary coding of all REST-backed repositories, we pooled the flagged
tools and derived an augmentation taxonomy via open coding. For each flagged tool, all three
authors independently traced (i) the repository-defined client/wrapper and (ii) its call sites in tool
handlers to identify any intermediate processing between tool invocation and external interactions,
and assigned descriptive labels for the observed augmentation behaviors. We then consolidated
these labels into a provisional taxonomy by merging semantically equivalent labels and splitting
overly broad labels. Using this provisional taxonomy, we mapped each author’s labels to taxonomy
categories and computed pre-consensus agreement on category assignments across all flagged tools
(Krippendorff’s α custom_category = 0.81). We resolved disagreements in code-grounded reconciliation
meetings and refined category names and definitions to produce the final augmentation taxonomy.

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 9

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

4.2

0:9

RQ2: How do MCP servers translate vendor REST API operations into tools,
specifically, what proportion of available operations is exposed, which classes of
operations are omitted, and what mapping patterns are used to group operations
into tools?

Motivation. RQ1 shows that the majority of official MCP servers act as REST API wrappers, but
this observation alone does not characterize the practical functionality that these servers make
available to MCP clients. Prior work has shown that APIs can be difficult to use at scale, and that the
level of abstraction and the structuring of operations are central factors influencing API usability
and developer experience [48, 60]. At the same time, studies on API operation design show that
APIs often move beyond a strictly CRUD-based representation of underlying resources, instead
offering operations that are organized around specific tasks [67]. Moreover, security guidance
emphasizes minimizing exposed capabilities and avoiding unnecessarily privileged or sensitive
endpoints, since API interfaces can expand an application’s attack surface if not carefully scoped
[55]. Together, these strands suggest that MCP servers should not be assumed to expose vendor
APIs verbatim: instead, they likely implement systematic selection (what is exposed vs. omitted)
and abstraction (how endpoints are grouped into tools). RQ2 therefore, examines the operation-totool mapping to quantify exposure and omission across operation/feature classes and to identify
recurring one-to-one, many-to-one and one-to-many mapping structures.
Approach. To answer RQ2, we analyze how MCP servers map vendor REST operations to tools.
We restrict this analysis to REST-backed and Partially-REST-backed MCP servers, excluding nonREST-backed servers identified in RQ1, and focus on the subset of 42 servers with corresponding
OpenAPI specifications described in Section 3.2. On this subset, we perform a three-stage analysis
to (i) establish a mapping between MCP tools and REST operations, (ii) quantify operation exposure
and omission across operation classes (e.g., read/create/update/delete) and endpoint categories
(e.g., authentication/security and analytics), and (iii) characterize mapping structures, including
one-to-one mappings, many-to-one aggregation, and one-to-many reuse.
Stage 1: Establishing tool–operation alignment. We establish an alignment between MCP tools
and vendor REST operations by combining manual mapping on a gold-standard subset with an
LLM-assisted semantic matching. We reuse the artifacts extracted during RQ1: for each MCP server
we have the set of exposed tools (from tool registration/handler definitions) and, for each tool, its
name, natural-language description, and parameter schema when available, together with evidence
about how the tool invokes the vendor (e.g., HTTP vs. SDK vs. CLI, and any explicit method/path
or URL templates observable at HTTP call sites). In parallel, we parse each vendor’s OpenAPI
specification to extract the set of REST operations, treating an operation as an HTTP method
bound to a path template (e.g., GET /users/id), and record operation metadata (e.g., operationId,
summary/description, tags, and request schema when present).
To construct a gold-standard alignment, we randomly sampled 10 MCP servers from the 42server corpus using a fixed seed. This subset contains 298 MCP tools and 857 REST operations. For
each tool in the gold set, three authors independently mapped the tool to one or multiple REST
operations. Because many tools invoke vendor functionality through SDKs or CLIs that abstract
away the underlying REST endpoints, we treat tool–operation alignment as a semantic mapping
problem and base the mapping primarily on textual and structural metadata (tool name/description
and parameter schema; OpenAPI operation summary/description, operationId, HTTP method,
and path template). When the tool’s HTTP call sites explicitly reveal endpoint information (e.g.,
method/path fragments or URL templates), we used this evidence to rule out non-matching OpenAPI
operations and prioritize candidates consistent with the observed endpoint.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 10

0:10

Mastouri et al.

We assessed agreement at two levels on the pre-consensus annotations. First, we measured
agreement on mapping cardinality, whether annotators selected a single operation versus multiple
operations for a given tool, using a multi-rater nominal agreement statistic (Krippendorff’s α card =
0.82). Second, we measured agreement on mapping identity by comparing, for each tool, the sets of
operations selected by different annotators, computing a set-overlap similarity score per tool, and
macro-averaging this score across tools and annotator pairs (SetSim = 0.89). Disagreements were
then resolved through evidence-based reconciliation until consensus was reached.
To scale beyond the gold-standard alignment, we employ an LLM (GPT-4.1) as a semantic
labeler, following established practices in LLM-assisted annotation and coding workflows where
a human-derived protocol is operationalized as a structured prompt and validated against gold
labels before being applied at scale [20]. Concretely, we translate our manual mapping guidelines
into an instruction prompt. To reduce spurious matches and improve determinism, the prompt
requires the model to choose only from the operations provided in the prompt and to return the
selected operation identifiers in a structured format (accompanied by a brief justification to support
auditing).
We evaluate the LLM against the gold alignment at the tool level. For each tool, we compare
the predicted set of one or more operations to the gold set and report macro-averaged per-tool
precision, recall, and F1 . We additionally report micro-averaged precision/recall/F1 over all tool–
operation decisions, as well as exact-match accuracy and cardinality accuracy to capture whether
the model predicts the correct operation set and set size. On the gold set, the LLM achieves high
performance (per-tool precision is 0.90, recall is 0.84, F1 is 0.87; micro-F1 is 0.89; exact-match is
0.78 and cardinality accuracy is 0.82). After evaluation, we apply the same prompt and matching
procedure unchanged to the remaining servers to generate tool–operation alignments at scale.
Stage 2: Quantifying operations coverage and omission in MCP tools
Using the alignment results of Stage 1, we quantify the extent to which vendor REST APIs are
exposed through MCP servers and how exposure varies across operation classes.
A. Overall operation coverage. For each API s, let Os denote the set of REST operations defined in
its OpenAPI specification and let Ms ⊆ Os denote the subset mapped to at least one MCP tool. We
define per-API coverage as:
|Ms |
Covs (∗) =
.
(1)
|Os |
We analyze the distribution of Covs (∗) across APIs by reporting its median and mean, and
examine how coverage varies as a function of API size.
B. Coverage and omission by operation category. We next examine how coverage varies across
different types of API operations. Using the tool–operation alignment from Stage 1, we group
operations by structural and semantic categories derived from their OpenAPI specifications and
compute coverage/omission within each category. Accordingly, we label every REST operation
with two classes of features: structural and semantic.
Structural features, illstrated in Table 2, capture the interface role and structural complexity of
an operation and are computed deterministically from the OpenAPI specification, following prior
work on operation-level API analysis [8, 32, 63, 64]. We derive is_read_only, is_mutating, and
is_destructive from the HTTP method (GET vs. POST/PUT/PATCH vs. DELETE). We derive
has_parameters and has_request_body from the presence of declared parameters (path/query)
and a requestBody object, respectively. We label needs_authentication when the effective
operation specifies OpenAPI security requirements and is_deprecated when the operation is
marked as deprecated. Finally, we detect has_pagination when the operation declares common
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 11

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

Feature

Definition

is_read_only
is_mutating
is_destructive
has_parameters
has_request_body
has_pagination
needs_authentication
is_deprecated
deep_path

Operation uses HTTP GET.
Operation uses POST, PUT, or PATCH.
Operation uses HTTP DELETE.
Operation declares at least one path or query parameter.
Operation includes a request body.
Operation exposes pagination controls (e.g., page, offset, cursor).
Operation is protected by OpenAPI security requirements.
Operation is marked as deprecated in the specification.
Operation path depth exceeds an API-specific threshold.

0:11

Table 2. Structural operation-level features used to quantify coverage and omission.

pagination controls as query parameters (e.g., page, offset, and cursor). To capture navigational
complexity, we compute path depth as the number of segments in the normalized OpenAPI path
template. Depth-/path-length notions have been used in prior REST/OpenAPI structural analyses to
characterize how “deep” an API’s resource structure becomes (e.g., via longest-path measures)[33].
Because APIs differ substantially in size and path conventions, we adopt an API-relative threshold
to identify unusually deep operations: an operation is labeled deep-path if its depth exceeds
max{Q 80, 5}, where Q 80 is the API-specific 80th percentile of path depth. This follows the general
idea of relative thresholds that define cutoffs from the distribution of values rather than a single
global constant, while the minimum cutoff of 5 prevents uniformly shallow APIs from labeling
ordinary endpoints as deep [53].
Semantic features capture higher-level functional groupings that are not directly encoded
by structural OpenAPI fields. We derive semantic categories by clustering OpenAPI tags into
higher-level groups. We extract all tag strings from the specifications and normalize them deterministically (lowercasing and trimming whitespace, standardizing separators, and removing version
tokens/stopwords). We embed each normalized tag using a pretrained sentence encoder (SentenceTransformers all-MiniLM-L6-v2 [62]). To reduce sensitivity to any single run, we use a bootstrap
consensus procedure with B = 30 rounds: in each round, we resample tags with replacement and
fit BERTopic [28] using the precomputed embeddings (UMAP [44] + HDBSCAN [11] internally),
yielding a clustering of the sampled tags (including an outlier label). Across rounds, we accumulate
a co-association score for each tag pair based on how often the two tags are assigned to the same
cluster when they co-appear; we then run HDBSCAN on the resulting consensus distance matrix to
obtain final tag groups. We treat outliers and low-stability clusters as unreliable and exclude them
from category-level reporting. Each REST operation inherits the semantic category (or categories) of
its OpenAPI tag(s); semantic categories are non-mutually-exclusive, and operations may contribute
to multiple categories when they carry multiple tags. To obtain human-interpretable category
names, Three authors independently reviewed each cluster’s most frequent tags and representative
operations, proposed a concise label, and reconciled naming disagreements in a meeting without
modifying cluster membership. Finally, to focus on broadly recurring categories, we retain only
semantic categories that appear in at least 25% of APIs in our corpus.
Category-Level Metrics For a given category c (structural or semantic) and API s, let Os,c ⊆ Os
be the operations exhibiting c, and let Ms,c = Ms ∩ Os,c be those mapped to at least one tool.
Let Sc ⊆ S denote the set of APIs for which category c is present, i.e., those with |Os,c | > 0.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 12

0:12

Mastouri et al.

Category-level coverage and omission are:
Covs (c) =

|Ms,c |
|Os,c |


|Os,c | > 0 ,

Omits (c) = 1 − Covs (c) .

(2)
(3)

We aggregate coverage across APIs using both macro and micro averages. The macro average
captures per-API behavior independent of size:
Covmacro (c) =

1
Σ Covs (c) ,
|Sc | s ∈Sc

(4)

while the micro average reflects operation-weighted coverage:
Σ |Ms,c |

micro

Cov

(c) =

s ∈Sc

Σ |Os,c |

,

(5)

s ∈Sc

To quantify whether a category is preferred for exposure relative to an API’s baseline, we compute
per-API lift:
Covs (c)
Lifts (c) =
,
(6)
Covs (∗)
where Lifts (c) > 1 indicates that operations in category c are mapped at a higher rate than the
API’s overall coverage. We summarize lift using macro aggregation:
Liftmacro (c) =

1
Σ Lifts (c) ,
|Sc | s ∈Sc

(7)

Stage 3: Characterizing grouping patterns in tool–operation mappings.
Mapping Structure Using the tool–operation alignment from Stage 1, we first quantify mapping
structure from both perspectives. From the tool perspective, we classify a tool as one-to-one if it
aligns to exactly one REST operation, and as many-to-one if it aligns to multiple operations. From
the operation perspective, we classify an operation as one-to-one if it aligns to exactly one tool, and
as one-to-many if it aligns to multiple tools.
Aggregation Pattern Identification We then investigate recurring grouping rationales for
many-to-one aggregation and one-to-many reuse through manual labeling. We treat each many-toone tool as one analysis instance and each one-to-many operation as one analysis instance. For
each instance, all three authors independently assigned a free-form pattern label capturing the
perceived rationale for the grouping, along with a short justification grounded in evidence from (i)
tool metadata, (ii) aligned operation metadata, and, when necessary, (iii) repository code evidence
indicating how multiple operations are orchestrated or reused.
To quantify agreement before reconciliation, we computed inter-annotator reliability over the
pre-consensus labels for many-to-one and one-to-many instances separately (Krippendorff’s α for
nominal labels; α m2o = 0.91 and α o2m = 0.94). We operationalized label agreement as assigning the
same instance to the same pattern category; disagreements were not reconciled prior to computing
α. After agreement measurement, we held synthesis meetings to resolve disagreements using
the recorded justifications and underlying evidence, and to consolidate synonymous labels and
standardize final pattern names. Finally, to focus on recurring design choices rather than APIspecific idiosyncrasies, we retain only patterns that appear in at least two distinct APIs; patterns
observed in exactly one API are excluded.

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 13

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

4.3

0:13

RQ3: To what extent can REST-backed MCP servers be automatically generated
from OpenAPI specifications, and what factors prevent faithful tool generation in
practice?

Motivation. Building on RQ1 and RQ2, our empirical characterization suggests that specificationdriven automation should be feasible in principle: most official MCP servers are REST-backed,
predominantly implement bare API consumption, and a substantial portion of tool–API relationships
follow direct one-to-one mappings. However, OpenAPI-based MCP generation appears rarely in
practice (≈ 4.5% of servers in our corpus), despite OpenAPI being explicitly intended as a machinereadable, language-agnostic interface description for HTTP APIs that enables consumers to discover
and understand service capabilities without access to source code [37]. Moreover, OpenAPI is widely
used as a foundation for downstream automation across the API lifecycle, including documentation,
client generation, and testing [21]. These observations motivate RQ3, which empirically evaluates,
under a fixed baseline translation, the extent to which real-world OpenAPI specifications suffice for
generating REST-backed MCP servers and tools, and identifies the recurring factors that prevent
faithful tool generation in practice.
Approach. To assess OpenAPI-driven MCP generation in a controlled, reproducible setting,
we developed AutoMCP-baseline (Section 5.1), a baseline generator that automatically translates
OpenAPI specifications into REST-backed MCP servers. AutoMCP-baseline implements a fixed
and transparent operation-to-tool translation: each OpenAPI operation (HTTP method bound
to a path template) is converted into a distinct MCP tool, and tool schemas and metadata are
derived solely from the specification. We adopt this prototype because our objective is not to
benchmark community-developed OpenAPI-to-MCP tools, but to measure what OpenAPI alone
enables under a uniform baseline translation. Existing open-source solutions are often provided
as libraries/frameworks that require user-authored integration code and configuration choices,
which would introduce uncontrolled variation across APIs and confound corpus-scale measurement.
AutoMCP-baseline therefore serves as a controlled measurement instrument with standardized
logging, enabling consistent evaluation and failure analysis across our specification corpus.
We conduct this study on a corpus of 80 real-world OpenAPI specifications described in Section 3.2.
For each specification, AutoMCP-baseline applies a baseline “operation-to-tool” translation: every
documented operation (HTTP method bound to a path template) is translated into a distinct MCP
tool, with operation inputs consolidated into a single tool schema and operation metadata used to
populate tool names and descriptions.
Because executing every generated tool across all APIs is infeasible, we construct an evaluation
set of executable operations using a two-phase sampling strategy inspired by resource-centric
REST testing and structural coverage principles [7, 15]. In the first phase, for APIs with at most 20
operations, we attempt to execute all operations. In the second phase, for APIs with more than 20
operations, we stratify operations by resource group, defined by the first semantic path segment
(e.g., /users, /repos), and select a structurally diverse subset within each group. Specifically, we
score each operation o by its contribution to uncovered diversity dimensions:
s(o) = 1verb + 1auth + 1params

(8)

where an operation earns one point if it introduces a previously unseen HTTP verb within the
group, one point if it introduces a new authentication scheme (from OpenAPI security requirements),
and one point if it introduces a new parameter modality (path/query/header/body). We then apply
a greedy pass that repeatedly selects the highest-scoring remaining operations until each diversity
axis observed in the group is covered at least once. Across both phases, endpoints that require
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 14

0:14

Mastouri et al.

paid subscriptions, geo-restricted credentials, or unavailable accounts are excluded. This sampling
procedure yields a final evaluation set of 2, 190 executable operations (i.e., generated MCP tools)
across the corpus.
We execute sampled tools using Claude as the MCP client, explicitly selecting tools from the
loaded manifest to avoid confounding results with free-form tool discovery. Because many tools
exhibit logical dependencies (e.g., a resource must be created before it can be updated or deleted),
execution order is non-trivial. We therefore first use GPT-4.1 to propose an initial dependencyrespecting sequence over the sampled tools based on tool names and descriptions, following recent
practice for planning API call sequences [38, 40]. We then partition the resulting sequence into
dependency blocks that group tools sharing state (e.g., create→read→update→delete for the same
resource family) and assign these blocks to one of three authors to balance workload while ensuring
state-dependent tools are executed by the same author. After the assignment, each author reviews
the plan for their block(s) and revises it when necessary (e.g., inserting missing prerequisites or
correcting ordering), logging all edits as part of the evaluation trace.
For each assigned tool, the author issues a minimal, template-based prompt intended to exercise
the MCP server rather than assess LLM reasoning. Prompts follow a consistent structure: they
explicitly name the tool to invoke, provide concrete, valid input values (reusing identifiers produced
earlier in the same dependency block when required), and state an observable expectation when
applicable (e.g., “create X, then verify via list/get”). A tool execution is considered successful if (1)
the tool appears in the manifest and loads without schema/configuration errors, (2) the invocation
receives a successful HTTP response from the upstream API, and (3) the intended effect is observed,
verified either by inspecting returned data (for read operations) or via a follow-up state query
within the same block (for update/write/delete operations). For every tool, we record the prompt,
concrete inputs, HTTP status codes, and response payloads, and a success/failure label. To assess
labeling consistency, a 10% random subset of executed tools is independently re-evaluated by a
second author using the same block plan and success criteria; Cohen’s κ on the re-evaluated subset
was 0.97. Disagreements were resolved by jointly reviewing the recorded prompts and HTTP
transcripts; remaining cases were adjudicated by a third author, and the adjudicated label was used
as final.
We analyze failed executions to identify recurring obstacles to faithful OpenAPI-driven MCP
generation. For each failed tool invocation, three authors independently inspected AutoMCPbaseline server logs, MCP client traces, and HTTP request/response transcripts and assigned a
provisional root-cause label capturing the primary reason for failure. We quantified inter-annotator
agreement on these pre-consensus labels using Krippendorff’s α for nominal data, where agreement
is defined by whether annotators assigned the same failure to the same root-cause category
(α = 0.93). The authors then held a synthesis meeting to reconcile disagreements and consolidate
synonymous labels into a shared taxonomy with explicit definitions. Using this finalized taxonomy,
each failure was assigned a single final root-cause label.

4.4

RQ4: How effective are automated OpenAPI repairs and tool-set transformations
(filtering and grouping) at addressing the failures and tool-set explosion observed
in OpenAPI-driven MCP generation?

Motivation. RQ3 demonstrates that OpenAPI-driven generation can fail to produce faithful MCP
servers in practice, and that even when generation succeeds, the resulting tool interfaces can be
impractically large for real MCP clients. These findings indicate two distinct barriers to automation.
First, generation failures often arise when OpenAPI specifications are incomplete or incorrect
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 15

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:15

relative to vendor behavior, preventing valid tool schemas or reliable request execution. Second,
baseline operation-to-tool translation tends to produce a tool per operation, which can yield
hundreds or thousands of tools for large APIs, exceeding practical client limits and undermining
usability. At the same time, RQ2 provides empirical evidence that real MCP servers do not expose
vendor APIs verbatim: they routinely omit certain categories of operations and often apply manyto-one grouping patterns to present higher-level tools. Together, these observations motivate RQ4:
we investigate whether the limitations revealed in RQ3 can be addressed automatically by repairing
OpenAPI specifications using vendor documentation cues and by transforming the generated tool
set using empirically grounded filtering and grouping strategies.
Approach. RQ4 assesses whether the correctness and usability of OpenAPI-driven MCP servers
can be improved automatically through two complementary strategies: (i) detecting and repairing
specification defects using SpecFix (Section 5.2), and (ii) reducing tool-set size through categorybased filtering and deterministic grouping (Section 5.3). Implementation details of both components
are provided in the respective framework sections; here we describe the evaluation methodology.
We use the same corpus of OpenAPI specifications as described in Section 3.2, as well as the same
baseline generation and execution harness introduced in RQ3, including the sampled operations
per API, the prompt templates, and the recorded execution transcripts, and proceeds in two
corresponding stages.
Stage 1: Specification defect detection and repair.
SpecFix (Section 5.2) operates in two modes on each specification. In detection mode, it analyses
the OpenAPI document together with vendor documentation cues and emits a structured issue
report identifying suspected defects and the operations they affect. In repair mode, it consumes the
issue report and synthesises a patch for each detected defect that minimally amends the OpenAPI
document while preserving its intended semantics. The evaluation targets defect categories A–C
(Table 17), which are specification-level defects identifiable through static analysis of the OpenAPI
document and its associated documentation. Categories D and E are excluded because they manifest
only at runtime and require dynamic request–response analysis to detect reliably [7, 25].
We evaluate detection quality on the 16 APIs whose RQ3 failure traces were attributed to
specification-level defect categories A–C (Section 5.2), encompassing 20 defect instances. Three
authors independently assess whether each reported defect corresponds to a real inconsistency or
omission in the OpenAPI document, given the referenced documentation evidence and the baseline
failure traces from RQ3. Inter-annotator agreement on the pre-consensus judgements is quantified
using Krippendorff’s α for nominal labels (α = 1.0).
We evaluate repair quality on the same 16 APIs by checking both validity and minimality of the
produced patches. At the specification level, we verify that patched documents remain parseable
and that modifications are localised to the reported defect context. At the semantic level, three
authors independently assess whether each patch plausibly resolves the reported issue while preserving intended behaviour, based on the original OpenAPI fragment, the documentation evidence
referenced in the issue report, and the patch diff. Agreement is quantified using Krippendorff’s α
(α = 0.93), followed by reconciliation.
We then measure end-to-end recovery by rerunning the RQ3 baseline pipeline on the full corpus
of 77 APIs after applying SpecFix repairs, and comparing generation and execution outcomes to
the original baseline. At the server level, we evaluate whether the regenerated MCP manifest loads
successfully. At the tool level, we re-execute, for each API, the same sampled operation set used in
RQ3, preserving tool intents and dependency ordering. Tool executions are judged using the same
success criteria as in RQ3, and we report improvements in execution success rate, reductions in
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 16

0:16

Mastouri et al.

specification-related failure categories, and regressions in which previously successful invocations
fail after repair. To verify labelling consistency, a second author independently re-assessed a random
10% sample of the repaired-tool execution outcomes using the same success criteria; inter-annotator
agreement was perfect (Krippendorff’s α = 1.0).
Stage 2: Tool-set reduction via filtering and grouping.
The second stage addresses tool-set explosion by transforming the baseline one-operationper-tool output into a smaller, more usable set of tools. The transformation pipeline—categorybased filtering followed by deterministic grouping—is described in Section 5.3; here we detail the
evaluation methodology.
Category labelling and validation. Filtering and grouping both require assigning structural and
semantic category labels to each OpenAPI operation. Structural labels are extracted directly from
the specification. For semantic labels, we use GPT-4.1 to classify each operation based on its tags
(following RQ2 semantic labeling), allowing multiple labels per operation. Operations that cannot
be mapped to any category in Table 12 receive the catch-all label Other. We validate this labelling
procedure against the manually annotated subset from RQ2 and report multi-label precision, recall,
and F 1 (precision = 0.92, recall = 0.86, F 1 = 0.89). The validated prompt is then applied unchanged
to all operations in the RQ3–RQ4 corpus.
Grouping evaluation. After filtering, we apply the Collection/Item Merge pattern (Section 5.3) to
reduce tool granularity. Because each merged tool replaces two distinct operations with a single
interface, we must verify that the new tool preserves the behaviour of both originals. For each of
the 232 endpoints in the RQ3 sample that match the Collection/Item Merge pattern, we exercise
the merged tool in both modes: once without an identifier argument to test collection retrieval,
and once with a valid identifier to test item retrieval. Each invocation is compared against the
corresponding original tool output and judged as pass or fail using the same execution criteria
as in RQ3. Evaluations were distributed across three authors, and 10% of merged tools were
independently re-assessed by a second author; inter-rater agreement on the pass/fail outcome was
perfect (Cohen’s κ = 1.0).

5

OPENAPI-TO-MCP GENERATION FRAMEWORK

This section presents our OpenAPI-to-MCP generation framework, which underlies the analyses
in RQ3 and RQ4. We distinguish between a baseline generation pipeline and an extended pipeline.
The baseline, implemented by AutoMCP-Baseline, is used in RQ3 to assess the extent to which MCP
servers can be generated directly from OpenAPI specifications. The extended pipeline, implemented
by AutoMCP, introduced in RQ4, augments this baseline with specification repair (SpecFix) and
tool-set transformations (filtering and groupping) to improve both execution correctness and
usability.
5.1

AutoMCP-Baseline: Compiling OpenAPI into an MCP Server

AutoMCP-Baseline implements the baseline generation pipeline used in RQ3, where each OpenAPI
operation is translated into a corresponding MCP tool without additional transformations.
As shown in Algorithm 1, AutoMCP-Baseline is a static code generator that compiles an OpenAPI 2.0 or 3.0 specification into an executable MCP server stub. Each endpoint in the input
specification is transformed into a callable MCP tool, enabling LLM clients to invoke external REST
APIs through the Model Context Protocol.
AutoMCP-Baseline is designed for reproducibility and minimal developer intervention: it accepts
a specification, performs one-pass offline compilation, and outputs a ready-to-run Python project
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 17

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:17

with environment-based configuration. All operational details, endpoint schemas, parameter structures, and authentication mechanisms, are inferred directly from the OpenAPI specification. The
only required manual step is to provide credentials in the generated .env file.
Algorithm 1: AutoMCP-Baseline: OpenAPI → MCP server
Require : OpenAPI spec spec, output dir Dout
A. Parse and load specification
2 let raw ← LoadSpec(spec) ;
3 B. Normalize specification
4 let norm ← NormaliseVersion(raw) ;
5 let f lat ← InlineRefs(norm) ;
6 FixMalformedSchemas(f lat) ;
7 let eps ← ListEndpoints(f lat) ;
8 C. Extract authentication metadata
9 let sec ← ExtractSecurity(f lat) ;
10 let env ← BuildEnvMap(sec) ;
11 if RequiresOAuth2(sec) then
12
GenerateOAuth2(Dout, sec) ;
13 end
14 D. Generate MCP server stub
15 let ctx ← InitContext(Dout, sec, env) ;
16 foreach (p, m, op) ∈ eps do
17
let par ← ExtractParams(op) ;
18
let par ← SanitiseNames(par ) ;
19
let h ← CreateHandler(p, m, par, sec, ctx) ;
20
let s ← GenerateSchema(op) ;
21
RegisterTool(h, s, ctx) ;
22 end
23 E. Emit artifacts
24 WriteEnvFile(env, Dout) ;
25 SaveGenerated(ctx, Dout) ;
1

// load YAML/JSON
// unify dialect
// resolve $refs
// repair common issues
// extract operations
// infer auth schemes
// map credentials to .env
// generate helper if needed
// initialize server context
// extract parameters
// make names safe
// create tool handler
// derive tool schema
// register MCP tool
// generate .env
// write server stub

The compilation process follows the five phases shown in Algorithm 1.
Step A: Input parsing and dialect resolution. AutoMCP-Baseline parses the input specification and automatically detects the format (YAML or JSON) and dialect (OpenAPI 2.0 or 3.0) by
inspecting top-level fields. For OpenAPI 2.0, the base URL is composed from schemes, host, and
basePath; for OpenAPI 3.0, the first entry in servers is used. This base URL is injected into all
generated tool handlers.
Step B: Specification normalisation and flattening. All $ref references are recursively
resolved to produce a fully inlined version of the specification. AutoMCP-Baseline also performs
structural normalisation to reconcile differences between OpenAPI versions, sanitise identifiers,
and fix common inconsistencies (e.g., duplicate operation IDs, undefined path parameters).
Step C: Authentication analysis and .env generation. Declared security schemes (e.g.,
API key, HTTP Basic, Bearer token, OAuth2) are parsed and mapped to environment variables.
AutoMCP-Baseline generates a template .env file in the output directory, providing placeholders
for all required tokens, secrets, and credentials. If an OAuth2 flow is detected, AutoMCP-Baseline
additionally emits a Flask-based oauth_login_server.py, which handles the login and callback
steps, retrieves access tokens, and writes them into the .env file.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 18

0:18

Mastouri et al.

Step D: Stub generation and handler synthesis. Every endpoint is compiled into a Python
handler function decorated with @mcp.tool(...), conforming to the MCP runtime conventions.
Handlers validate input, inject authentication headers or query parameters, construct and dispatch HTTP requests using requests, and return the parsed response or raw fallback. When the
EXTRA_HEADERS environment variable is set, AutoMCP-Baseline automatically injects logic to parse
a JSON string from the environment and merge it into all HTTP requests, enabling API-specific
header customisations.
Step E: Output layout. AutoMCP-Baseline writes all generated artifacts to the specified output directory, including the server stub server_stub.py, the environment template .env, and
optionally oauth_login_server.py. The resulting stub runs as an MCP server without additional
manual editing.
End-to-End Illustration (Trello API). To illustrate the workflow, we compile Trello’s public
OpenAPI contract with AutoMCP-Baseline. The generator converts each documented API operation
into a corresponding MCP tool and produces handler functions that invoke the underlying REST
endpoints. Trello’s API-key–based authentication is automatically mapped to environment variables
in the generated .env file.
Client configuration. Claude Desktop (v2025.6) is configured to launch the generated stub as a
local MCP server. Listing 1 shows the minimal JSON entry required to register the server.
{

}

" mcpServers " : {
" trello " : {
" command " : " python " ,
" args " : [ " path / to / server_stub . py " ]
}
}

Listing 1. Claude configuration for the Trello MCP server generated by AutoMCPBaseline.

Runtime flow. At startup, Claude issues get_capabilities, receives the tool manifest from
the generated MCP server, and validates each tool schema. When the user issues a request such as
“Create a bug card in Trello,” Claude selects the appropriate tool (e.g., create_card), populates the
required JSON parameters, and sends a tool_call. The server stub injects credentials from the
.env file, dispatches the corresponding REST request (e.g., POST /1/cards) to Trello, and returns
the structured response. Claude then converts this result into natural-language feedback for the
user, as illustrated in Figure 3.
5.2

SpecFix: Automated OpenAPI Specification Repair

To address the specification-level deficiencies identified in RQ3, we extend the AutoMCP-baseline
pipeline with SpecFix, a preprocessing component for automated OpenAPI contract analysis and
repair. SpecFix executes prior to MCP server generation: it compares an OpenAPI specification
against its official documentation, detects global inconsistencies, and when enabled, produces a
minimally repaired specification for compilation. By separating contract repair from code generation,
AutoMCP-baseline operates on higher-quality specifications without modifying the underlying
compilation logic.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 19

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents
Human

Claude
( MCP Client )

Generated
MCP Server

0:19

Trello
REST API

Trello MCP
Server
1 get_capabilities ()
2

Tools & Schema

Load Tools
Start Interactive
Dialogue
3

“Read boards
and create ...”
4

{"tool":"create_card"
,"arguments":
{"name":"Bug 123,..}}

8 “I’ve Succesfully 7 {"url":"https://trello
...”
.com/c/A14", ...}

POST/1/cards?
5 key=$KEY &
token=$TOKEN
6 {"url":"https://trell
o.com/c/A14", ...}

Fig. 3. End-to-end message flow for Trello card creation mediated by an AutoMCP-Baseline generated MCP
server.

SpecFix targets three categories of specification defects: (A) authentication misconfigurations,
(B) malformed or missing base URLs, and (C) undocumented runtime headers or authentication
prefixes. These correspond to global contract inconsistencies that directly prevent automated
invocation of otherwise valid endpoints. The rationale for scoping SpecFix to these three categories
is discussed in Section 4.4.
SpecFix supports two execution modes. In analysis mode, it performs non-destructive detection
and produces a structured issue report. In fix mode, detected issues are validated and, if confirmed, repaired through targeted structural modifications. The repaired specification preserves all unaffected
content and introduces only the corrections necessary to restore global contract consistency.
SpecFix takes two inputs: an OpenAPI specification and a URL pointing to the official API
documentation. It follows a three-phase architecture, where each phase produces well-defined
artifacts consumed by the next.
Phase 1: Documentation structuring. SpecFix constructs a structured representation of the
official API documentation. Because contemporary API portals frequently rely on client-side
rendering frameworks, static HTML retrieval is insufficient. We therefore employ Playwright in a
headless browser environment to execute JavaScript and capture the fully rendered DOM. During
extraction, the crawler expands collapsible sections, scrolls to trigger lazy-loaded content, and
waits for network-idle conditions so that asynchronous resources are fully resolved. Extracted
pages are normalised and cached to avoid repeated rendering in subsequent runs. Let S denote the
OpenAPI specification and D the structured documentation model derived from extraction.
Phase 2: Specification–documentation mismatch detection. SpecFix applies a set of deterministic rules that compare structural properties of the specification S against content extracted
from the documentation model D. Each rule targets a specific mismatch pattern within one of the
three supported defect categories (A–C); Table 3 formalises the six rules used. For example, an A-type
rule fires when the documentation indicates that authentication is required (D.auth_mentioned)
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 20

0:20

Mastouri et al.

Table 3. SpecFix detection rules for specification–documentation mismatches, grouped by defect category.
Issue type

Detection rule

Symbols used

(A) Authentication misconfiguration
Missing security
declaration

D.auth_mentioned ∧ SecS = ∅

Inconsistent secu- SecS ≠ ∅ ∧ ∃σ ∈
rity scheme type
¬mentioned D (σ.type)

SecS

Sec S : declared security schemes in specification S;
D.auth_mentioned: documentation indicates that
authentication is required.
: σ: a declared security scheme;
mentioned D (x): documentation explicitly mentions
authentication type x.

(B) Malformed or missing base URL
Missing
server
configuration

Swagger2(S): S conforms to Swagger 2.x;
OpenAPI3(S): S conforms to OpenAPI 3.x;
Serv S : declared server configuration in S.
: srv: a declared server entry;
valid_url(u): u is a valid base URL (protocol present,
no unresolved template variables).

(Swagger2(S) ∧ S.host = ∅) ∨
(OpenAPI3(S) ∧ ServS = ∅)

Malformed or in- ∃srv
∈
ServS
valid base URL
¬valid_url(srv.url)

(C) Undocumented runtime headers or authentication prefixes
Missing required
global header

∃h ∈ D.global_headers : h ∉ S

Authentication
prefix mismatch

D.auth_prefix
defined
prefix S ≠ D.auth_prefix

∧

D.global_headers: headers documented as globally
required;
h: a documented required header.
D.auth_prefix: documented authentication prefix
(e.g., Bearer);
prefix S : authentication prefix declared in the specification.

but the specification declares no security scheme (SecS = ∅). No LLM is involved at this stage:
detection is fully rule-based. For each triggered rule, SpecFix records the issue type, its location in
the specification, and the supporting specification and documentation fragments. These records
form a structured issue report that serves as input to Phase 3.
Phase 3: LLM-based validation and repair. In fix mode, SpecFix processes each issue in the
report produced by Phase 2. For each candidate issue, a single call to GPT-4.1 receives four inputs:
the issue type, the relevant specification fragment, the supporting documentation fragment, and a
set of structural constraints (e.g., valid OpenAPI security scheme formats, required server object
fields). The model first assesses whether the reported inconsistency is genuine; if rejected, no
modification is applied. If confirmed, the model returns a minimal corrective fragment, the smallest
structural change to the specification that resolves the inconsistency. Each corrective fragment
is associated with a location path in the specification tree. A deterministic patcher applies the
fragment at the identified location via JSON merge, preserving all unaffected structure. After all
patches are applied, SpecFix serialises the repaired specification in its original format (YAML or
JSON) and records the applied changes as a structured diff for traceability.
5.3

Tool-Set Transformations: Filtering and Grouping

AutoMCP-Baseline translates each OpenAPI operation into a separate MCP tool. For large APIs,
this one-to-one mapping can produce hundreds of tools, exceeding the context-window and toolselection capacity of current LLMs. To address this, AutoMCP incorporates two transformations—
category-based filtering and deterministic grouping—grounded in the empirical patterns identified
in RQ2.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 21

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:21

Step 1: Category-based filtering. Each OpenAPI operation is labelled with the structural and
semantic categories defined in RQ2 (Tables 11 and 12). Semantic labels are generated by GPT-4.1
from operation tags, allowing an operation to receive multiple labels when applicable. Operations
that cannot be mapped to any known category are assigned the label “Other.” To determine which
categories to filter, we derive a data-driven threshold from the omission statistics in RQ2. Rather
than using a fixed cutoff, we compute the 75th percentile (Q 75 ) of the omission distribution across
all feature categories. A category c is considered highly omitted if either its macro omission rate or
its micro omission rate exceeds the respective Q 75 threshold:
MO
mO
MO(c) ≥ Q 75
∨ mO(c) ≥ Q 75

(9)

This rule yields six filtered categories: four semantic—authorization, authentication, settings/configuration, and user management—and two structural—deprecated and destructive operations. An
operation is removed only if all of its assigned labels fall within this union, preserving operations
that serve multiple purposes including at least one commonly exposed capability.
Step 2: Collection/Item Merge grouping. After filtering, we reduce tool granularity by applying the Collection/Item Merge pattern (Table 14), the most frequent many-to-one aggregation
pattern observed in RQ2. For each API, we scan the remaining operations and identify pairs of
retrieval endpoints of the form GET /r (collection) and GET /r/{id} (item), where r denotes
the same normalised resource path prefix and {id} is a single path-parameter segment. For each
detected pair, we synthesise a single MCP tool with an optional identifier argument: when the
identifier is omitted, the tool executes the collection endpoint; when provided, it executes the item
endpoint.
5.4

AutoMCP: End-to-End Pipeline

AutoMCP integrates the three components described above—baseline generation (Section 5.1),
specification repair (Section 5.2), and tool-set transformations (Section 5.3), into a single pipeline
that compiles an OpenAPI specification into an executable MCP server. Figure 4 illustrates the
end-to-end workflow.
The pipeline takes two inputs: an OpenAPI specification describing a vendor API and, optionally, a
URL pointing to its official documentation. When a documentation URL is provided, SpecFix analyses
the specification for contract-level mismatches and, in fix mode, produces a minimally repaired
specification (Section 5.2). The repaired (or original) specification then enters the transformation
stage, where category-based filtering removes operations belonging to highly omitted categories and
Collection/Item Merge grouping consolidates endpoint pairs (Section 5.3). The resulting operation
set is compiled into MCP tools using the AutoMCP-Baseline code generation procedure (Section 5.1).
The generated server exposes these tools via the MCP protocol and can be invoked by any MCPcompatible client.
AutoMCP operates in three configurations of increasing capability, each corresponding to a
specific evaluation stage in this study:
• AutoMCP-Baseline (RQ3): direct one-operation-to-one-tool compilation, with no repair or
transformations.
• AutoMCP-baseline + SpecFix (RQ4, Stage 1): specification repair followed by baseline
compilation.
• AutoMCP-baseline + SpecFix + Transformations (RQ4, Stage 2): specification repair,
category-based filtering, Collection/Item Merge grouping, and compilation.

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 22

0:22

Mastouri et al.

Fill out
Credentials

Generated
MCP Server

OpenAPI
Specifications
(Optional)

API Operations
Structural
Labeling

Detection
mode

API
Documentation
(URL/Text)

Semantic
Labeling

.env
template
Server
Stub

Fix mode
Issues YES
detected?

Rules

Issues
report

Edit
config file

Category filtering

fixed

Operation Grouping

NO

Executable
MCP Server

Fig. 4. AutoMCP end-to-end pipeline. Optional stages are indicated with dashed borders.

6

RESULTS

This section presents the empirical findings for all research questions (RQ1–RQ4).
6.1

RQ1: REST reliance, integration, and configuration in MCP servers

6.1.1 RQ1.1 REST Reliance. Across the 116 official MCP servers in our corpus, 114 expose tool
configurations that can be statically enumerated and analyzed. We excluded two servers5 that
generate tool sets dynamically from user-specific configurations, preventing reproducible tool
enumeration and classification.
Most official MCP servers realize tool functionality through vendor REST API calls.
Using the Stage 1 procedure (Section 4.1), we find that 87 servers (76.3%) are REST-backed, meaning
that all tool handlers can be statically traced to one or more vendor REST API invocations. These
invocations occur via direct HTTP calls, SDKs wrapping REST endpoints, or equivalent REST
clients. An additional 14 servers (12.3%) are partially REST-backed, where only a subset of tools
relies on REST invocations. The remaining 13 servers (11.4%) are non-REST-backed, with tools
relying on alternative mechanisms such as direct database connections (e.g., SQL drivers, gRPC),
GraphQL APIs, binary protocols (e.g., Bolt, Lightning/NWC), or local application integrations (e.g.,
WebSocket, browser automation).
MCP Server Class

Servers

Total Tools

Median Tools/server

REST-backed
Partially REST-backed
Non-REST-backed

87 (76.3%)
14 (12.3%)
13 (11.4%)

2,636 (83.3%)
347 (11%)
180 (5.7%)

18
21
11

Total

114 (100%)

3,163 (100%)

18

Table 4. Corpus distribution of official MCP servers (n = 114).

Table 4 and Figure 5 summarizes the distribution at both repository and tool levels. REST-backed
servers dominate the ecosystem, while partially and non-REST-backed servers are comparatively
5 integromat/make-mcp-server and PipedreamHQ/pipedream

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 23

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents
  D 

## Page 24

  7 R R O  F R X Q W V  E \  L Q Y R F D W L R Q  W \ S H

  E 

## Page 25

  5 ( 6 7  U H O L D Q F H  G L V W U L E X W L R Q

   

 3 H U F H Q W D J H  R I  D O O  0 & 3  V H U Y H U V    

## Page 26

   

 7 R R O V  S H U  V H U Y H U

   

   

   

  

 
 G     

## Page 27

  E D F N H
 5 ( 6 7

 3 D

 D F N H
 ( 6 7  E
 U W L D O O \  5

 G     

## Page 28

 D F N H
 ( 6 7  E
 1 R Q  5

 G     

## Page 29

0:23

  

    

 5 ( 6 7  E D F N H G   E D U H  Z U D S S H U V
 5 ( 6 7  E D F N H G   F X V W R P  D X J P H Q W D W L R Q
 3 D U W L D O O \  5 ( 6 7  E D F N H G   Q R Q  5 ( 6 7    P H G L D Q
 3 D U W L D O O \  5 ( 6 7  E D F N H G   Q R Q  5 ( 6 7  !  P H G L D Q
 1 R Q  5 ( 6 7  E D F N H G

  

  

     

  

 

     
     
 5 ( 6 7  E D F N H G
    

## Page 30

 3 D U W L D O O \  5 ( 6 7  E D F N H G
    

## Page 31

 1 R Q  5 ( 6 7  E D F N H G
    

## Page 32

Fig. 5. Distribution of MCP servers by REST-reliance and tool counts. (a) Tool count distribution (violin plot).
(b) REST-reliance breakdown (stacked bars).

less common. Tool counts vary substantially across classes: REST-backed servers exhibit the widest
distribution, reflecting variation in the size of exposed vendor APIs, whereas partially and nonREST-backed servers tend to expose smaller and more uniform tool sets.
Departures from REST are comparatively rare and concentrated in a small set of recurring mechanisms. In partially REST-backed servers, non-REST functionality is typically confined
to a minority of tools (median share 22.5%, range 4.3%–90.9%). Only four repositories implement
more than one quarter of their tools via non-REST mechanisms (PortSwigger [57], Neo4j [49],
MongoDB [47], and Neon [50]). Across the 14 partially REST-backed servers, we identified 110
non-REST tools in total. These tools fall into a small set of recurring non-REST mechanism families.
The largest group uses database-native interfaces (49.1%), where tools interact through database
drivers or query/protocol stacks rather than vendor HTTP endpoints. A second group relies on local
or in-process interfaces (18.2%), in which tools invoke functionality via locally running applications,
plugins, or embedded libraries instead of remote REST calls. A third group uses RPC-style service
interfaces (10.0%). The remaining tools rely on a small number of vendor-specific mechanisms,
without forming consistent or widely adopted patterns.
¤ Finding-RQ1.1. Vendor REST APIs overwhelmingly dominate MCP server implementations: 88.6% of servers in our corpus (n = 114) are fully or partially REST-backed. Non-REST
mechanisms are rare and concentrated in a small number of specialized integration patterns.
6.1.2

RQ1.2 Configuration and Integration Practices.

(a) Configuration practices. We now analyze how REST-backed servers configure authentication,
communication, and tool exposure at runtime. Table 5 summarizes authentication mechanisms,
while Tables 6 and 7 report transport support and tool-selection capabilities.
Authentication is dominated by token-based credential provisioning. API-key authentication dominates (48.3%), followed by HTTP bearer tokens (17.2%) and OAuth 2.0 (10.3%), as shown
in Table 5. A smaller share of servers rely on multi-credential configurations (12.6%), such as API
key and secret pairs or client ID/secret combinations. The remaining servers (10.3%) use alternative
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 33

0:24

Mastouri et al.

approaches, including cloud credential chains or CLI-based authentication (e.g., AWS, Azure, and
Google Cloud identity systems). Overall, MCP servers predominantly rely on non-interactive,
token-based authentication that mirrors the credential models of the underlying vendor APIs.
Table 5. Authentication mechanisms used by MCP servers (n = 87).
Authentication type

Servers

%

API key
HTTP Bearer
OAuth 2.0
HTTP Basic
Multi-credential
Other (cloud IAM / CLI auth)

42
15
9
1
11
9

48.3%
17.2%
10.3%
1.1%
12.6%
10.3%

Total

87

100%

STDIO remains the modal transport, with substantial multi-transport support. STDIOonly transport is the most common (50.6%), reflecting the prevalence of local, subprocess-style
deployment in MCP integrations. In contrast, 40.2% of servers support multiple transports, typically combining STDIO with HTTP and/or SSE endpoints. HTTP-only deployments account for
8.0%, while SSE-only configurations are rare (1.1%). This distribution suggests a split between
servers optimized for local execution and those designed for flexible deployment across runtime
environments.
Table 6. Transport mechanisms supported by MCP servers (n = 87).
Transport type

Servers

%

STDIO only
Multiple transports
HTTP only
SSE only

44
35
7
1

50.6%
40.2%
8.0%
1.1%

Total

87

100%

Explicit tool filtering is uncommon, and most servers expose all tools by default. Only
26.4% of MCP servers provide configuration mechanisms to enable, disable, or selectively register
subsets of tools (e.g., via flags such as –tools, –enabled-tools, or environment variables like
MCP_ENABLED_TOOLS), as shown in Table 7. The majority (73.6%) expose all tools unconditionally at
initialization. This suggests that current implementations prioritize simplicity and immediate tool
availability over configurable capability scoping, although the presence of filtering in a non-trivial
minority indicates emerging attention to manageability.
¤ Finding-RQ1.2.a. REST-backed MCP servers prioritize low-friction configuration: tokenbased authentication dominates, STDIO is the most common transport, and most servers
expose all tools by default.

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 34

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:25

Table 7. Tool-selection capability among MCP servers (n = 87).
Tool selection support

Servers

%

Median tools/server

Yes (tools can be filtered)
No (all tools exposed)

23
64

26.4%
73.6%

35
16

Total

87

100%

–

(b) Integration strategies. We now examine how these servers incorporate REST calls into tool
implementations.
Bare API consumption is the dominant integration strategy in REST-backed MCP servers.
Among the 87 REST-backed servers, 80 repositories (92.0%) consist exclusively of tools that perform
bare API consumption. Across all REST-backed MCP servers, we identified 2,636 tools, of which
2,436 (92.4%) belong to bare-consumption servers.
Invocation type

Tools

%

Direct HTTP
SDK-based
OpenAPI-generated/client
CLI-based

1,579
705
111
41

64.8%
28.9%
4.6%
1.7%

Total

2,436

100%

Table 8. Invocation type distribution among Bare API consumption MCP servers and tools.

Direct HTTP requests dominate how bare API consumption tools call vendor APIs.
Among the 2,436 bare-consumption tools, direct HTTP invocation is the most prevalent mechanism (1,579 tools; 64.8%), as shown in Table 8. SDK-based invocation is the second most frequent
mechanism (705 tools; 28.9%), while OpenAPI-generated clients (111 tools; 4.6%) and CLI-based
invocation (41 tools; 1.7%) are comparatively rare.
Custom API client logic in REST-backed MCP servers is rare and concentrated in a
small minority of REST-backed servers. Only 7 of the 87 REST-backed repositories (8.0%)
introduce non-trivial augmentation logic beyond bare API consumption and are classified as custom
API client. These 7 repositories account for 200 tools (7.7% of REST-backed tools). In all cases, tools
still ultimately invoke vendor REST endpoints; the distinguishing characteristic is the presence of
additional computation or coordination layered on top of routine API access.
Augmentation behaviors in Custom API client tools cluster into a small set of recurring
patterns. Static inspection of Custom API client tools reveals three recurring augmentation patterns
that go beyond routine client REST API responsibilities (e.g., authentication handling, request
formatting, pagination traversal, and error processing). Table 9 summarizes the taxonomy and its
prevalence across servers. Workflow orchestration composes multiple upstream calls into a single
tool-level result, handling inter-call dependencies such as polling and aggregation internally. AImediated transformation interposes a secondary model invocation within the tool. Non-functional
controls embed cross-cutting safeguards (caching, rate limiting, response sanitization) directly in
the tool logic. The three patterns differ markedly in adoption granularity: non-functional controls
and workflow orchestration, once adopted, are applied broadly across a server’s tool surface (83
and 63 tools, respectively), whereas AI-mediated transformation is deployed selectively at specific
endpoints (28 tools across 5 servers).
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 35

0:26

Mastouri et al.

Table 9. Taxonomy of augmentation patterns in Custom API client servers (7 of 87 REST-backed servers).
Patterns are non-mutually exclusive.
Pattern

Definition (beyond routine request processing)

Workflow orchestration

A tool coordinates multiple upstream interactions to produce
one tool result (e.g., multi-call composition, aggregation, and
asynchronous completion via polling).
A tool invokes model-driven processing to synthesize or restructure artifacts (e.g., schema/artifact generation, assistantstyle translation, or retrieval-augmented suggestion).
A tool introduces execution semantics affecting performance/safety (e.g., caching, rate limiting, response sanitization
or prompt injection mitigation).

AI-mediated transformation

Non-functional controls

#Servers

#Tools

4

63

5

28

3

83

// MCP TOOL: extract
addTool({
3
name: 'extract',
4
description: 'Scrape webpage and extract structured JSON.',
5
parameters: z.object({
6
url: z.string().url(),
7
extraction_prompt: z.string().optional(),
8
}),
9
execute: tool_fn('extract', async ({ url, extraction_prompt }, ctx) => {
1
2

10
11
12
13
14
15

let scrape_response = await axios({
url: 'https://api.brightdata.com/request',
method: 'POST',
data: { url, format: 'markdown' },
});

// API call

16
17

let markdown_content = scrape_response.data;

18
19
20

let system_prompt = "Return ONLY valid JSON.";
let user_prompt = extraction_prompt || "Extract structured data.";

21
22
23
24
25
26
27
28
29

let sampling_response = await session.requestSampling({
messages: [{
role: "user",
content: { type: "text",
text: `${user_prompt}\n\n${markdown_content}` },
}],
systemPrompt: system_prompt,
});

// AI augmentation

30

return sampling_response.content.text;
}),
33 });
31
32

Listing 1. BrightData MCP example [10] with direct HTTP integration and AI-mediated transformation
augmentation.

Listing 1 illustrates one tool from the BrightData MCP server, which uses direct HTTP invocation
to retrieve webpage content in markdown format. However, the tool does not simply return the API
response. Instead, it introduces additional logic by invoking an LLM through a sampling interface,
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 36

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:27

using system and user prompts to transform the retrieved content into structured JSON. As captured
in Table 9, this corresponds to AI-mediated transformation.
Augmentation intensity in Custom API client servers is highly skewed, indicating both
repository-wide and targeted adoption modes. As illustrated in Table 10, within the 7 custom
API client repositories, augmentation is not uniformly applied: 5 server repositories augment more
than 95% of their tools, whereas the remaining 2 servers apply augmentation to only a small fraction
(less than 5%) of an otherwise bare tool set. This skew suggests that augmentation is typically
adopted either as a repository-wide design stance (systematically layering orchestration or controls
across tools) or as a targeted extension used for a small number of specialized tools.
Table 10. Augmentation in Custom API client MCP servers (7 of 87 REST-backed servers).
MCP Server

#Tools

#Aug. tools

Apify [6]
Honeycomb [34]
Astra DB [16]
AWS MCP [39]
BrightData [10]

17
14
16
2
63

17
14
16
2
60

Cashfree [12]
Firebase [26]

39
49

2
2

Total

200

113

% Aug.

Augmentation patterns

100 Workflow orchestration; AI-mediated transformation
100 Non-functional controls; Workflow orchestration
100 Non-functional controls
100 Workflow orchestration; AI-mediated transformation
orchestration;
AI-mediated
95 Workflow
transformation;Non-functional controls
5.1 AI-mediated transformation
4.1 AI-mediated transformation
—

¤ Finding-RQ1.2.b. REST-backed MCP servers act as thin adapters over vendor APIs: 92%
implement tools as lightweight REST pass-throughs, with functionality realized through
bare API consumption, predominantly via direct HTTP. Augmentation beyond routine API
access is rare (8%) and, when present, follows a small set of recurring patterns: workflow
orchestration, AI-mediated transformation, and non-functional controls.
6.2

RQ2: REST operation exposure, omission, and mapping patterns in MCP tools

6.2.1 RQ2.1: How much of the vendor REST API surface do MCP servers expose?
Across the 42 MCP servers paired with publicly available OpenAPI specifications, we extracted a
total of 6,966 REST operations. Using the alignment procedure described in section 4.2, we mapped
1,013 REST operations to 968 MCP tools.
Most MCP servers expose fewer than one in five operations available in vendor OpenAPI
specifications. Across APIs, the median operation-level coverage is 19%, indicating that MCP
servers typically surface only a subset of the vendor interface. The mean coverage is higher (32.4%),
indicating a right-skewed distribution(Figure 6a): a few servers expose a large share of their vendor’s
operations, while the majority surface only a narrow subset.
MCP servers expose proportionally fewer operations as vendor API size increases.Figure 6b
plots coverage against API size, showing a clear inverse trend. We partition APIs into size categories
using box-plot quartiles [71]. We partition APIs into size categories using box-plot quartiles [71]:
small (≤ Q 1 , i.e., ≤ 25 operations), medium (Q 1 –Q 2 ), large (Q 2 –Q 3 ), and very large (> Q 3 , i.e., > 300
operations). For small APIs (n = 10), the median coverage is 68% (mean = 63%). Coverage declines
sharply with scale: medium APIs (n = 11) exhibit a median of 14% (mean = 33%), large APIs (n = 13)
a median of 19% (mean = 18%), and very large APIs (n = 8) drop to a median of only 6%. Only 5
APIs (12%) expose every REST operation through MCP tools.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 37

0:28

Mastouri et al.
 1 R W L R Q  7 Z L O L R

 0 H D Q         
 0 H G L D Q         

  

 1 X P E H U  R I  $ 3 , V

  
  
  
 
 

 0 D S S H G  F R Y H U D J H    

## Page 38

   
  
  
  
  

 

 6 W U L S H  * L W + X E

 7 U H Q G
 

 
 

 7 Z H O Y H ' D W D

 

  

  

  

 0 D S S H G  F R Y H U D J H    

## Page 39

  

  

   

(a) Distribution of per-server coverage ratios.

 

  

 

 1 X P E H U  R I  R S H U D W L R Q V  L Q  $ 3 ,   O R J  V F D O H 

## Page 40

  

 

(b) Coverage ratio as a function of vendor API size
(log scale).

Fig. 6. Distribution and scaling of REST operation coverage across matched MCP servers.

¤ Finding-RQ2.1. MCP servers act as curated views over vendor APIs rather than complete
proxies, with coverage driven primarily by API size: larger API surfaces yield proportionally
narrower exposure.
6.2.2

RQ2.2: Which categories of REST operations are preferentially exposed or omitted?

(a) Structural Feature Analysis. We now report coverage of operations based on structural features.
Table 11 reports macro/micro-average coverage and lift across the 9 structural categories.
Structural feature

Macro Cov

Macro Omit

Macro Lift

# APIs

Micro Cov

Micro Omit

# Ops

is_read_only
is_listing_operation
is_mutating
is_destructive
needs_authentication
deep_path
has_request_body
has_pagination
is_deprecated

0.3816
0.4122
0.2805
0.2041
0.3555
0.2785
0.2964
0.2995
0.1074

0.6184
0.5878
0.7195
0.7959
0.6445
0.7215
0.7036
0.7005
0.8926

1.2596
1.4470
0.8694
0.6347
0.9989
0.7983
0.9277
1.0763
0.6592

42
40
39
32
41
38
37
23
13

0.1940
0.1847
0.1094
0.0657
0.1543
0.1115
0.1009
0.2544
0.0531

0.8060
0.8153
0.8906
0.9343
0.8457
0.8885
0.8991
0.7456
0.9469

3418
1538
2679
867
5949
2851
2536
456
226

Median
Q75

0.2964
0.3555

0.7036
0.7215

0.9277
1.0763

38
40

0.1115
0.1847

0.8885
0.8991

2536
2851

Table 11. Structural feature coverage, omission, and lift across APIs. Cells highlighted in blue indicate high
values (above the 75th percentile, Q75), while cells highlighted in orange indicate the highest omission values.

MCP servers preferentially expose retrieval operations and omit state-changing and
deprecated functionality. As illustrated in Table 11, read-only and listing operations are the only
features with macro lift above 1 (1.26 and 1.45, respectively), confirming that retrieval operations
are more likely to be included than other operation types. Mutating and destructive operations
fall below baseline (lift of 0.87 and 0.63), with destructive operations exhibiting the highest micro
omission rate among non-deprecated features (0.93). Deprecated operations are near-universally
excluded (macro omission 0.89, micro omission 0.95), suggesting that deprecation markers in
OpenAPI specifications serve as effective exclusion signals.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 41

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:29

Structurally complex operations tend to be under-exposed, with pagination as a notable
exception. Operations that signal invocation complexity namely, deep paths and request bodies,
are associated with below-baseline lift (0.80 and 0.93, respectively), suggesting that MCP server
developers favour simpler endpoint signatures. Pagination-bearing operations are the sole exception:
despite appearing in only 23 APIs, they exhibit above-baseline lift (1.08) and the highest micro
coverage among all features (0.25), likely because paginated endpoints correspond to high-value
listing operations that developers prioritise regardless of their added complexity.
¤ Finding-RQ2.2.1. MCP servers are more likely to expose operations related to information retrieval, while selectively omitting operations that are either higher impact
(mutating/destructive), structurally complex (deep paths, request bodies), or explicitly
marked as deprecated.

Semantic category

Representative tags

Inventory
management
Data / storage

billing, quota, invoices, products, pricing, payments, exchanges,
inventory, assets, vendors
search, database, query, migrations, datasets, indexes, export, statements,
federation
auth, oauth, tokens, credentials, access tokens, API keys, federated
authentication, grants
events, schedules, triggers, actions, workflows, automation, health
events, orchestration
users, accounts, service accounts, admin users, account members, user
tags, bundles
licensing, regulatory requirements, approvals, compliance, policies,
standards, disputes
metrics, analytics, time series, correlations, analysis, insights, trending,
statistics
roles, permissions, access control, RBAC, allowlist, domains, role
bindings
settings, SSO, preferences, configuration, session settings, sandbox,
tuning
encryption keys, signing keys, key management, API keys, keystore,
BYOK, certificates
audit logs, logging, monitoring, log export, workspace logs, subscriptions
organizations, orgs, enterprise, environments, site administration

Authentication
Event & workflow
management
User management
License / policy /
requirements
Analytics
Authorization
Settings /
configuration
Key management
Logs
Organizations

# APIs
20
17
17
17
17
16
15
15
11
11
10
10

Table 12. Semantic categories derived from consensus clustering of OpenAPI tags. Representative tags are
shown for each category. Only categories present in at least 10 APIs are retained.

(b) Semantic Category Analysis. We now analyze coverage patterns across semantic categories
derived from OpenAPI tags using the consensus BERT clustering procedure described in Stage 2.
Table 12 reports the resulting semantic categories together with representative tags and their
prevalence across the corpus. Table 13 reports macro/micro coverage and lift for these categories.
Operational and analytics categories are preferentially exposed as MCP tools. Table 12
lists the twelve semantic categories produced by consensus clustering. Event and workflow management, exhibits the strongest relative preference in the corpus (lift 2.24), followed by analytics
(1.50), logs (1.50), data/storage (1.34), and inventory management (1.27). These categories share a
common characteristic: they map to observability, orchestration, and data retrieval functionality.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 42

0:30

Mastouri et al.

Semantic Category

Macro Cov

Macro Omit

Macro Lift

# APIs

Micro Cov

Micro Omit

# Ops

Authorization
Authentication
Settings / configuration
User management
Key management
Organizations
Logs
License / policy / requirements
Data / storage
Inventory management
Event & workflow management
Analytics

0.0453
0.0563
0.0960
0.1125
0.1313
0.1576
0.2100
0.2267
0.2653
0.2914
0.3362
0.4107

0.9547
0.9437
0.9040
0.8875
0.8687
0.8424
0.7900
0.7733
0.7347
0.7086
0.6638
0.5893

0.3447
0.2660
0.1536
0.4011
0.5339
1.1187
1.5018
0.6093
1.3352
1.2702
2.2388
1.4960

15
17
11
17
11
10
10
16
17
20
17
15

0.0574
0.0547
0.0256
0.0413
0.1250
0.0691
0.0930
0.1383
0.2529
0.2990
0.0935
0.7258

0.9426
0.9453
0.9744
0.9587
0.8750
0.9309
0.9070
0.8617
0.7471
0.7010
0.9065
0.2742

209
201
117
242
88
269
43
188
348
311
460
186

Median
Q75

0.1838
0.2718

0.8162
0.8916

0.8640
1.3754

15.5
17.0

0.0933
0.1670

0.9068
0.9433

205.0
279.5

Table 13. Semantic category coverage, omission, and lift across APIs (macro and micro aggregates). Cells
highlighted in blue indicate high values (above the 75th percentile, Q75), while cells highlighted in orange
indicate the highest omission values.

Analytics further stands out with the highest micro coverage of any category (0.73), confirming
that its over-representation is not an artefact of per-API averaging.
Security-sensitive and administrative categories are rarely exposed as MCP tools.. At the
opposite end, settings/configuration (lift 0.15), authentication (0.27), authorization (0.34), and user
management (0.40) exhibit macro omission rates between 89% and 95% (Table 13). These categories
govern credential handling, access control, and administrative configuration, functionality whose
exposure through an LLM-facing interface carries inherent risk.
Exposure patterns reflect active filtering rather than uniform downsampling. Figure 7
plots macro omission against lift, combining both structural and semantic features. If MCP servers
were downsampling operations uniformly, all points would cluster near lift = 1. Instead, the plot
reveals a clear quadrant structure: retrieval and operational features concentrate in the bottomright (preferred, lower omission), while security and administrative features occupy the top-left
(disfavoured, higher omission). Structural complexity features, deep paths, request bodies, and
mutating operations, fall near the centre, indicating proportional reduction rather than active
filtering. This separation confirms that the coverage patterns reported above are the result of
deliberate curation, not an artefact of API size.
¤ Finding-RQ2.3. At the semantic level, observability, orchestration, and analytics categories are preferentially exposed, while authentication, authorization, and configuration
categories exhibit near-complete omission. Quadrant analysis confirms that these inclusion
and exclusion patterns are not a by-product of exposing a fixed fraction of each API, but
reflect targeted selection based on operation semantics.
6.2.3 RQ2.3: How Often Do MCP Tools Aggregate Multiple REST Operations? Following Stage 3,
we characterize mapping structure from both the tool and operation perspectives. From the tool
perspective, a tool is classified as one-to-one if it aligns to exactly one REST operation and many-toone if it aligns to multiple operations. From the operation perspective, an operation is classified as
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 43

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:31

Feature-Level Exposure Preference vs Omission
AuthZ

lift>1 & low omit
lift>1 & high omit
lift<=1 & high omit
lift<=1 & low omit

0.95

AuthN
Config
0.90

UserMgmt

Deprecated

Omission (Macro Omit)

KeyMgmt
Org

0.85

Destructive

0.80

Logs

Policy
0.75

Data
DeepPath

Pagination

Mutating
ReqBody

0.70

Inventory

Workflow

NeedsAuth

0.65

Read
0.60

Analytics

Listing
0.5

1.0

1.5

2.0

Relative Preference (Macro Lift)

Fig. 7. Feature-level omission versus relative exposure preference. Each point represents a feature category.
The vertical dashed line marks neutral preference (MacroLift = 1), and the horizontal dashed line indicates
the median macro omission (0.735), separating lower- and higher-than-typical omission levels.

one-to-many if it is referenced by multiple tools. Table 14 summarises the observed mapping types,
their prevalence, and representative examples from the corpus.
Most MCP tools map to a single REST operation. Among aligned tools, 869 (89.8%) map
to exactly one REST operation, while only 99 (10.2%) aggregate multiple operations (Table 14).
Aggregation appears in 32 of the 42 matched APIs; the remaining 10 rely exclusively on one-to-one
mappings. This confirms that MCP tools predominantly act as direct projections of individual REST
endpoints rather than composite abstractions.
When multiple REST operations are aggregated into a single MCP tool (Many-to-one),
the grouping follows a small number of recurring, well-motivated patterns. As Table 14
details, the five patterns differ in both frequency and abstraction strategy. The two most common,
Collection/Item Merge andMulti-View Read, account for over half of all aggregated tools and share a
retrieval-oriented motivation: both reduce the number of tools an LLM must select among when
exploring a resource. The remaining three patterns address state management Lifecycle Action
Bundle, scope resolution Scope Unification, and full lifecycle control CRUD Collapse; each appears
in at least two distinct APIs, indicating shared design strategies rather than isolated decisions.
Operation-level reuse (One-to-Many) is infrequent and concentrated on retrieval endpoints. Only 136 REST operations are referenced by more than one MCP tool. Reuse is modest
(mean 2.37 tools per operation, median 2) and strongly skewed toward retrieval: 68% of reused
operations are GET endpoints, and roughly one-third involve listing operations. In 60.3% of cases,
the reusing tools share a common verb prefix (e.g., get_*, list_*), which is consistent with
tools offering narrower, task-specific views of the same operation rather than introducing new
functionality.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 44

0:32

Mastouri et al.

Mapping Type /
Pattern

Tools – APIs

Description

Example (Tool → Operation(s))

One-to-One

869/968 tools
–
42 APIs

A single MCP tool delegates to exactly get-source-languages →
one REST operation, preserving a direct GET /v2/languages (DeepL)[17]
correspondence between the tool interface and the API endpoint.

Many-to-One (99/968 tools; 10.2% across 32 APIs)
Collection/Item Merge

33/99
tools –
18 APIs

Collapses the standard REST pair, workflows-get-default →
a collection endpoint (/resources) GET /api/v3/workflows,
and its corresponding item endpoint GET /api/v3/workflows/{id}
(/resources/{id}), into a single tool (Shortcut)[66]
with an optional identifier parameter.

Multi-View Read

20/99
tools –
13 APIs

Unifies three or more read-only endpoints that offer different views of the
same resource (e.g., list, detail, search,
filter) into a single retrieval tool.

list_users_by_org →
GET /orgs/{id}/users,
GET /org/users,
GET /orgs/{id}/users/search,
GET /org/users/lookup
(Grafana)[27]

Lifecycle Action Bundle

16/99
tools –
9 APIs

Groups operations that represent adjacent state transitions of the same resource (e.g., assign, resolve, reopen), exposed through a single tool parameterised by action type.

manage_incident →
POST .../assign,
POST .../unassign,
POST .../resolve,
POST .../ignore,
POST .../reopen
(GitGuardian)[22]

Scope Unification

12/99
tools –
8 APIs

Merges global and tenant-scoped variants of the same operation into a single
tool, with a scope parameter selecting
the target context.

get-v3-stats-total →
GET /v3/stats/total,
GET /v3/{domain}/stats/total,
GET /v3/stats/total/domains
(Mailgun)[42]

CRUD Collapse

6/99
tools –
4 APIs

Combines create, read, update, and/or
delete operations for a lightweight resource into a single tool, parameterised
by HTTP method or action. Observed
only for resources with simple, tightly
coupled lifecycles.

manage_repository_notif_subscription
→
GET/PUT/DELETE
/repos/{o}/{r}/subscription
(Github)[23]

Table 14. Tool-to-operation mapping types and aggregation patterns observed across 42 matched APIs.

¤ Finding-RQ2.3. MCP tools map to REST operations predominantly through one-to-one
correspondences (89.8%). When aggregation occurs, it follows five recurring patterns dominated by retrieval-oriented groupings. From the operation perspective, reuse is infrequent
and similarly concentrated on read endpoints.
6.3

RQ3: Feasibility and Limitations of Automatic MCP Tool Generation from OpenAPI
Specifications

6.3.1 Baseline Generation and Execution Success. To assess whether OpenAPI specifications contain
sufficient information for automatic MCP tool generation, we apply the AutoMCP baseline generator
to all 77 REST-backed APIs in the corpus and evaluate the executability of the resulting tools. Table 15
reports per-API outcomes.
Automatic generation from OpenAPI specifications succeeds for the majority of APIs,
but failure case tend to affect entire APIs rather than individual tools. At the API level, 59 of
77 APIs (76.6%) achieve fully successful execution, every sampled tool invocation completes without
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 45

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:33

error. The remaining 18 APIs (23.4%) exhibit at least one failure. At the tool level, 1,666 of 2,190
sampled invocations succeed, yielding an overall execution success rate of 76% (Table 15). Notably,
failures are not evenly spread: in 15 of the 18 failing APIs, failures affect all or most sampled tools,
indicating that the root causes are API-wide properties, such as missing authentication schemes or
incomplete server metadata, rather than individual endpoint defects.
¤ Finding-RQ3.1. OpenAPI specifications are frequently sufficient for automatic MCP tool
generation without manual integration code. When generation fails, the root causes are APIwide contract deficiencies rather than individual endpoint issues, suggesting that a small
number of targeted specification improvements could substantially increase automation
coverage.
Table 15. Automation outcomes for all 77 APIs (sorted by operation count).
Notes. Failure codes: A: Incorrect or missing security schemes; B: Malformed or relative base URLs; C: Undocumented
runtime headers and token prefixes; D: Parameter type mismatches; E: Missing endpoint authentication.

API

Auth

Operations

Success

Brave
apikey
Duckduckgo
none
Weather
none
Advice
none
Globalping
OAuth2+http bearer
WebScraping.AI
apikey
Airtable
http bearer
Firecrawl
http bearer
IPLocate
apikey
Jobsoid
none
Adp
none
Exa
apikey
Exchange_rate
none
Api Guru
none
Dropbox
OAuth2
Red Hat Insights
apikey
Milvus
http bearer
Huggingface
apikey
VictoriaMetrics
apikey
Notion
http bearer
Petstore
none+apikey
Graphhopper
apikey

1
1
1
3
4
4
5
5
5
6
7
7
7
7
9
9
10
12
16
19
19
20

1/1
1/1
1/1
2/2
4/4
4/4
5/5
5/5
5/5
6/6
0/7
7/7
7/7
7/7
9/9
0/9
0/10
12/12
0/16
1/19
19/19
20/20

–
–
–
–
–
–
–
–
–
–
B
–
–
–
–
A
B
–
B
E+C
–
–

–
–
–
–
–
–
–
–
–
–
7/7
–
–
–
–
0/9
0/10
–
0/16
1/19
–
–

2c2p
Ably
Token Metrics
Signwell
Keboola

22
22
22
23
23

2/2
11/11
2/2
5/5
10/10

–
–
–
–
–

–
–
–
–
–

none
http basic+none
none
apikey
apikey+none

Failure After Fix

Continued on next page.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 46

0:34

Mastouri et al.

API

Auth

Open_route
apikey (query)
Pappers
apikey
Buttondown
http bearer
Todoist
http bearer
Apaleo
OAuth2
Box
OAuth2
Twiliomessaging
http basic
Qdrant
apikey
Innoship
apikey
Chatkitty
OAuth2
Resend
http bearer
Gitlab
apikey
Meilisearch
http bearer
Modrinth
none+apikey
Multiversx
none
Circleci
apikey+http
Honeycomb
apikey+http bearer
Paddle
http bearer
Coingecko
apikey
Langfuse
http basic
Spotify
OAuth2
Pokeapi
apikey+http
Elasticsearch
apikey
Neon
apikey+http bearer
Webflow
OAuth2+http bearer
Bitrise
apikey
Apify
http bearer
SonarQube
http bearer
ThoughtSpot
http bearer
Redis
apikey
Shortcut
apikey
Supabase
http bearer
Redis Cloud API
apikey
GitGuardian
http bearer
Render
http bearer
Mailgun
http basic
Sentry
http bearer
Twelve Data
apikey
Discord
OAuth2+apikey
Openai
http bearer
Trello
apikey+none
Mailchimp
http basic
Bitbucket
OAuth2+apikey+http

Operations

Success

Failure After Fix

24
24
28
28
33
34
40
43
51
68
70
73
73
76
76
78
78
79
81
86
88
97
102
103
108
109
120
125
130
132
133
142
142
159
166
176
183
184
222
226
255
272
318

2/8
14/14
0/21
15/15
0/33
26/26
6/6
0/17
23/23
28/28
17/17
19/23
23/23
44/44
17/17
31/31
67/67
44/44
15/15
0/7
25/25
48/48
8/8
18/18
27/27
19/19
44/44
0/45
0/3
15/15
72/72
0/17
34/34
60/60
69/69
58/58
18/18
5/161
44/44
43/43
55/55
59/59
31/31

E
–
A+C
–
A+B
–
–
A
–
–
–
D
–
–
–
–
–
–
–
B
–
–
–
–
–
–
–
A
C
–
–
B
–
–
–
–
–
–
–
–
–
–
–

2/8
–
21/21
–
33/33
–
–
17/17
–
–
–
19/23
–
–
–
–
–
–
–
7/7
–
–
–
–
–
–
–
45/45
3/3
–
–
17/17
–
–
–
–
–
–
–
–
–
–
–

Continued on next page.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 47

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

API
Square
PagerDuty
Confluent
MongoDB
Clarifai
Stripe
Github
Total

Auth

Operations

Success

Failure After Fix

OAuth2+none
apikey
OAuth2+http basic
apikey+OAuth2
apikey
http bearer
OAuth2/http

327
386
405
462
489
583
1114

11/11
108/108
107/107
0/6
0/73
0/151
0/81

–
–
–
C
A+B+C
A
A

–
–
–
6/6
0/73
151/151
81/81

–

8,890

1,666/2,190

–

2,063/2,190

0:35

6.3.2 Failure analysis and defect taxonomy. While the baseline generator succeeds for the majority
of APIs, Table 15 reveals that certain OpenAPI specifications consistently produce tools that fail
at execution time. To understand what specification-level factors prevent faithful generation, we
analyse all failed invocations using open coding (Section 4.3).
Generation failures stem from discrepancies between the OpenAPI contract and the
runtime behaviour of the API. Across the 18 APIs (23.4%) that exhibit at least one execution
failure, we identify five root causes through open coding (Table 15 and Table 16). The most prevalent
is incorrect or missing security scheme declarations (A), where the specification either omits the
required authentication mechanism or declares one that differs from what the server enforces.
Malformed or relative base URLs (B) and undocumented runtime headers or token prefixes (C) follow,
each causing the generated tool to construct requests that the server cannot route or authenticate.
Parameter type mismatches (D) and missing endpoint-level authentication annotations (E) are less
frequent but produce the same effect: the generated request diverges from what the API expects
at execution time. All five causes share a common characteristic, they arise not from limitations
of the generator, but from incomplete or inaccurate specification of runtime requirements in the
OpenAPI contract.
Table 16. Root causes of automation failures observed in RQ3.
Failure Category

Affected APIs Affected Tools (in sample)

(A) Incorrect or missing security schemes
(B) Malformed or relative base URLs
(C) Undocumented runtime headers and token prefixes
(D) Parameter type mismatches
(E) Missing endpoint-level authentication annotations

8
7
5
1
2

18.9% (416/2,190)
6.8% (149/2,190)
5.5% (121/2,190)
0.2% (4/2,190)
1.1% (24/2,190)

Total

18

23.9% (524/2,190)

Below, we discuss each category and illustrate the minimal contract change (when applicable)
that would be sufficient to eliminate the failure under the baseline generator.
(A) Incorrect or missing security schemes. In 8 APIs, authentication metadata is missing
or incorrectly declared in the OpenAPI contract. Typical issues include absent entries under
components.securitySchemes, deprecated OAuth2 flow declarations, or missing token endpoints.
When such metadata is incomplete, AutoMCP cannot infer credential injection behavior, leading to
systematic authorization failures at runtime. A minimal correction involves restoring the missing
authentication fields required to complete the OAuth2 flow, as illustrated in Listing 2.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 48

0:36

Mastouri et al.

securitySchemes :
oauth2 :
type : oauth2
flows :
authorizationCode :
authorizationUrl : https :// identity .[..]/ authorize
+
tokenUrl : https :// identity [..]/ connect / token
Listing 2. Apaleo security scheme and patch (lines 7).

(B) Malformed or relative base URLs. Some specifications declare server URLs using unresolved templates or relative paths. Such declarations prevent correct request routing and result
in immediate connectivity failures for all endpoints. In these cases, a minimal repair consists of
replacing the placeholder with a fully qualified base URL, as shown in Listing 3.
Servers :
url : '{{ service - root }} '
+
url : ' https :// api . adp . com '
Listing 3. ADP base URL placeholder replaced with an absolute URL. (line 2).

(C) Undocumented runtime headers and token prefixes. Some APIs require metadata not captured in the OpenAPI specification, such as version-specific headers or non-standard token formats
(e.g., a mandatory Bearer prefix). Because this information appears only in prose documentation,
the generator cannot infer it, producing requests that are structurally valid but rejected by the
server. Declaring these requirements as explicit header parameters or security scheme properties
in the specification would close the gap.
/ v1 / users / me :
get :
summary : Retrieve your token 's bot user
[...]
parameters :
[...]
+
- name : Notion - Version
+
in : header
+
required : true
+
schema :
+
type : string
+
default : "2022 -06 -28"
+
description : The Notion API version to use
Listing 4. Notion: adding required Notion-Version header to align specification with runtime requirements.

(D) Parameter type mismatches. A small fraction of failures stem from mismatches between
parameter types declared in the OpenAPI schema and those accepted by the live API. For instance,
identifiers declared as integers may be treated as opaque strings in practice. Correcting the parameter
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 49

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:37

schema to reflect the actual accepted type is sufficient to restore correct request construction, as
illustrated in Listing 5.
parameters :
name : id
[...]
schema :
type : integer
+
type : string
Listing 5. GitLab: changing project id from integer to string.

(E) Missing endpoint-level authentication. Some specifications explicitly mark certain operations as public (security: []) even though the server enforces authentication on them at runtime.
The generator trusts the contract and omits credentials from these requests, which the server then
rejects. Removing the incorrect public override and allowing the global security scheme to apply
would resolve these cases. A potential repair involves inheriting the global security scheme for any
operation that does not declare its own, as illustrated in Listing 6.
# Global security ( applies to all endpoints )
security :
- bearerAuth : []
[...]
/ v1 / pages /{ page_id }:
get :
summary : Retrieve a page
[...]
security : []
Listing 6. Notion: removing incorrect endpoint-level security override to inherit global Bearer authentication.

¤ Finding-RQ3.2. Fully automated generation of MCP servers from OpenAPI specifications fails due to recurring, specification-level defects that systematically impact
many tools within an API. These deficiencies are identifiable through static analysis of
the openAPI contract and correctable through targeted edits, suggesting that specification
quality, is the primary bottleneck for automation scalability.
6.4

RQ4: Effectiveness of Automated Repairs and Tool-Set Transformations (filtering
and grouping) for OpenAPI-Driven MCP Generation

6.4.1 Specification Defect Detection and Repair. We evaluate SpecFix (Section 4.4) in three stages:
detection accuracy on validated defect instances, correctness of the generated patches, and end-toend impact on generation outcomes across the full corpus.
SpecFix detects targeted specification defects with high recall and precision. Of the 18
APIs with confirmed failures in RQ3 (Table 15), 16 contain at least one defect in the categories
targeted by SpecFix: authentication misconfigurations (A), malformed base URLs (B), and undocumented runtime headers or token prefixes (C). These 16 APIs comprise 20 defect instances in
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 50

0:38

Mastouri et al.

total. The remaining 2 APIs exhibit only out-of-scope defects (one D, one E) and are excluded from
the detection and repair evaluation. Table 17 reports outcomes for both stages. SpecFix correctly
identifies 19 of the 20 targeted instances (recall 95%), with perfect detection for categories A (8/8)
and B (7/7), and one missed instance in category C (4/5) where the required header appeared only
in external prose inaccessible to the analyser. The tool produced a single false positive, an A-type
flag for a specification declaring both bearer and basic authentication where the documentation
referenced only bearer, yielding an overall precision of 95%.
SpecFix produces correct repairs for the majority of detected defects, with failures
confined to cases with insufficient documentation evidence. All 19 patches produced from
true detections result in parseable OpenAPI specifications, confirming that the repair pipeline
preserves structural validity. However, three patches are incorrect (Table 17): two involve baseURL defects (B) where the LLM defaulted to a placeholder (https://api.example.com) because
no recoverable endpoint was present in the documentation, and one involves an authentication
defect (A) where the API expects a custom identity header but the repair replaced it with a standard
HTTP bearer scheme. The overall repair correctness rate is 16/19 (84.2%). These cases illustrate a
current limitation: when documentation evidence is insufficient or ambiguous, the LLM generates
plausible but incorrect patches rather than abstaining.
Most APIs with targeted defects achieve full recovery after repair. Of the 16 APIs evaluated,
11 (68.8%) achieve full recovery, every previously failing invocation now succeeds (Table 17, Table 15).
Two APIs achieve partial recovery: one contains an additional out-of-scope defect (E) that persists
after the targeted C-type defect is repaired, and the other has its A and B defects corrected but a
co-occurring C-type defect that was not detected. The remaining three APIs are not fixed due to
the three incorrect repairs identified above (one A, two B).
At the corpus level, specification repair substantially improves end-to-end generation
success. Table 18 reports end-to-end outcomes after rerunning the baseline pipeline (Section 4.4)
on all 77 APIs with SpecFix patches applied. At the API level, fully successful generation increases
from 59/77 (76.6%) to 67/77 (87.0%). At the tool level, successful invocations rise from 1,666/2,190
(76.0%) to 2,063/2,190 (94.2%), an improvement of 18.2 percentage points. The disproportionate
tool-level gain reflects the concentrated nature of failures: repairing a single API-wide defect
restores execution for all of its sampled tools simultaneously.
Repair introduces a small number of regressions on previously passing APIs. SpecFix
produced regressions in 3 of the 59 previously passing APIs, affecting 10 tool invocations (0.45% of
all sampled tools). In each case, SpecFix inferred an authentication requirement from documentation
fragments for endpoints that were either publicly accessible or required credentials only under
specific conditions. These over-constrained patches highlight a trade-off in documentation-driven
repair: when the specification is ambiguous about authentication scope, the repair logic defaults to
the more restrictive interpretation.
¤ Finding-RQ4.1. Automated specification repair raises tool-level execution success
from 76% to 94%, with the strongest gains on localised, well-documented defects. Residual
failures arise from defect classes outside the current repair scope and from ambiguities
in authentication semantics, where documentation-driven inference can produce overconstrained patches.
6.4.2 Tool Filtering and Operation Grouping. Repairing specification defects improves execution
reliability but does not address a second practical barrier: tool-space explosion. Large APIs can
produce hundreds of generated tools (Table 15), exceeding the context-window and tool-selection
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 51

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:39

Table 17. SpecFix pipeline outcomes: detection and repair quality across targeted defect categories (20 defect
instances across 16 APIs).
Detection
Defect category

Detected FP Recall Precision Correct Rate

Auth. misconfiguration (A)
Malformed base URL (B)
Undoc. header/token prefix (C)
Total (A–C)

Repair

8/8
7/7
4/5

1
0
0

100%
100%
80%

88.9%
100%
100%

7/8 87.5%
5/7 71.4%
4/4 100%

19/20

1

95%

95%

16/19 84.2%

Recovery outcomes (16 APIs with A–C defects)
Full recovery
Partial recovery (out-of-scope or undetected defect persists)
Not fixed (incorrect repair)

11/16
2/16
3/16

(68.8%)
(12.5%)
(18.8%)

Table 18. End-to-end generation outcomes before and after SpecFix (77 APIs).
Metric

Baseline

After repair Improvement

APIs with full execution success
59/77 (76.6%)
67/77 (87.0%)
+8 (+10.4 pp)
Successful tool invocations
1,666/2,190 (76.0%) 2,063/2,190 (94.2%) +397 (+18.2 pp)
Regressions (previously passing)
–
3/59 APIs (5.1%) 10 tools affected

capacity of current LLMs. We therefore apply two complementary transformations, category-based
filtering and deterministic grouping, grounded in the coverage and aggregation patterns identified
in RQ2 (Section 4.4).
Category-based filtering removes nearly one fifth of the generated tool space. As illustrated in Table 19, across the 77 APIs, filtering removes 1,636 of 8,890 candidate operations (−18.4%).
The per-API impact varies with API composition: the mean reduction is 21.2 operations (median 5).
Grouping preserves behavioural equivalence. All 232 endpoints evaluated under the Collection/Item Merge pattern passed both invocation modes, confirming that merged tools reproduce
the behaviour of their original counterparts without regressions.
Collection/Item Merge grouping removes 486 tools across 55 APIs. After filtering, we
apply the Collection/Item Merge pattern (Table 14) to consolidate list and detail endpoint pairs
(e.g., GET /items and GET /items/{id}) into single tools with an optional identifier parameter.
Across the corpus, 55 APIs contain mergeable patterns, yielding 485 merge groups that remove an
additional 486 tools, reducing the post-filtering total from 7,254 to 6,768.
Together, the two transformations reduce the median tool count by one third. Table 19
reports the cumulative effect. The total tool count decreases from 8,890 to 6,768 (−23.9%), and the
median per-API count drops from 73 to 49 (−32.9%). Figure 8a shows that both the median and
interquartile range shift downward, indicating consistent reductions across APIs rather than gains
driven by a few outliers. While these reductions are substantial, they remain higher than the level
of abstraction observed in real MCP servers, where developers often reduce hundreds of operations
to a much smaller set of tools. This gap reflects a deliberate design choice: our transformations
focus on operations that can be safely omitted or merged based on structural and semantic criteria,
without introducing assumptions about user intent. More aggressive reductions likely require
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 52

0:40

Mastouri et al.
Tool Count Reduction After Filtering and Merging
60

500

50

200

Reduction (%)

Tools per API (linear below 100, log above)

Effect of API Size on Tool Reduction

Typical client limit (80 tools)

1000

100
80

40
30
20

50

10

20
105
1

0
Original

After Filtering + Merging

(a) Distribution of tools per API before and after reduction.

101
102
API Size (Number of Operations)

100

103

(b) Per-API reduction as a function of original API
size.

Fig. 8. Effect of category-based filtering and Collection/Item Merge grouping on tool-space complexity.
Table 19. Tool-space reductions after category-based filtering and Collection/Item Merge grouping (77 APIs).
Metric

Value Change

Total tools (baseline)
After category-based filtering
After filtering + grouping

8,890
7,254
6,768

–
−18.4%
−23.9%

73
60
49

–
−17.8%
−32.9%

Median tools per API (baseline)
Median tools per API (after filtering)
Median tools per API (after filtering + grouping)

reasoning about user-facing functionality and LLM usability, such as identifying task-oriented
abstractions or high-level workflows. We leave this direction to future work.
Larger APIs benefit disproportionately from the reduction pipeline. Figure 8b plots perAPI reduction against original API size. APIs with larger initial tool sets exhibit higher absolute
reductions. The largest absolute reductions occur in GitHub (−325 tools), MongoDB (−197), and
Confluent (−176), while the highest relative reductions appear in Meilisearch (63.0%), PokeAPI
(49.5%), and GitGuardian (47.8%).
¤ Finding-RQ4.2. Empirically grounded filtering and grouping, reduce the generated
tool space by 23.9% and lower the median per-API tool count from 73 to 49. Reductions are
consistent across the distribution and most pronounced for large APIs, bringing tool sets
closer to the practical limits of current LLM-based agents.
7

THREATS TO VALIDITY

We discuss threats to validity following established guidelines for empirical software engineering
research [75].
Internal validity. Several analysis stages rely on manual coding (REST reliance classification,
tool–operation alignment, failure root-cause labelling, and repair validation). To control for subjectivity, all tasks were performed independently by at least two authors using shared protocols,
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 53

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:41

with inter-rater reliability measured before reconciliation (Cohen’s κ: 0.87–1.0; Krippendorff’s α:
0.81–1.0). Disagreements were resolved through code-grounded evidence review.
In RQ2, we use GPT-4.1 to scale tool–operation alignment beyond a 10-API gold standard. The
model achieved macro-F 1 = 0.87 and exact-match accuracy of 0.78 on the gold set, and the prompt
was applied without modification to remaining servers; nonetheless, residual labelling errors may
affect coverage statistics. We report both macro and micro aggregates to reduce the influence of
individual APIs.
Tool execution in RQ3–RQ4 is subject to transient upstream conditions (rate limiting, downtime,
stale state). We mitigated this through dependency-aware ordering, re-execution of suspected
transient failures, and independent re-evaluation of a random 10% subset (κ = 0.97; α = 1.0).
Additionally, SpecFix intentionally targets only three of five defect categories; the reported repair
effectiveness therefore represents a lower bound.
External validity. Our RQ1 corpus comprises 116 servers drawn from Anthropic’s official MCP
catalogue (July 2025), filtered to repositories with a publicly documented REST API and ≥10 GitHub
stars. This selection captures mature, officially listed servers but may not generalise to private,
enterprise-internal, or community-developed deployments.
8

CONCLUSION

This paper presented the first empirical study of how MCP servers relate to vendor REST APIs and
whether this relationship can be exploited for automated server generation. Through a multi-stage
analysis of 116 official MCP servers, 42 paired OpenAPI specifications, and an extended corpus
of 77 real-world API contracts, we addressed four complementary research questions spanning
architecture characterisation, operation-level mapping, generation feasibility, and automated repair.
Our findings paint a consistent picture. The vast majority of official MCP servers are RESTbacked, and most implement tools as thin wrappers that perform bare API consumption rather
than complex orchestration. Yet these servers expose only a selective fraction of the underlying API
surface, typically around one-fifth of documented operations, following systematic omission and
grouping patterns that are structurally and semantically predictable from the OpenAPI specification
alone.
This characterisation motivated and informed an automated generation pipeline. We showed
that a fixed, specification-driven translation already produces executable MCP tools for 76% of
sampled operations, and that the remaining failures concentrate in a small number of mechanically
identifiable specification defect classes. SpecFix, our automated repair component, raised tool-level
success to 94.2% by targeting the three most prevalent defect categories, while empirically grounded
filtering and regrouping reduced the median tool count per API by roughly one-third, mitigating
the tool-set explosion that degrades LLM tool selection at scale.
For practitioners, the study provides two concrete resources that are not currently available
in the MCP ecosystem. First, the omission and grouping patterns documented in RQ2 constitute
empirically grounded design heuristics for MCP server construction, offering a reference for which
operation categories to expose, which to suppress, and how to structure tool interfaces, based on
what experienced developers consistently do across dozens of independently authored servers.
Second, the defect taxonomy from RQ3 gives API providers a targeted checklist of specification
issues that silently break downstream automation.
REFERENCES
[1] 2025. FastMCP Issue #1449: Verbose Tool Descriptions Cause Context Window Overflow. https://github.com/PrefectHQ/
fastmcp/issues/1449.
ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 54

0:42

Mastouri et al.

[2] 2025. FastMCP Issue #3093: Tool Call Fails with Large Payload Parameters. https://github.com/PrefectHQ/fastmcp/
issues/3093.
[3] 2025. FastMCP Issue #3113: Tool Call Fails on POST Parameters. https://github.com/PrefectHQ/fastmcp/issues/3113.
[4] 2025. FastMCP Issue #3242: Circular Reference Crashes Generation. https://github.com/PrefectHQ/fastmcp/issues/3242.
[5] Anthropic. 2024. Model Context Protocol (MCP). https://docs.anthropic.com/claude/docs/model-context-protocol
[Online].
[6] Apify. 2025. Apify MCP Server. https://github.com/apify/apify-mcp-server. Accessed: 2026.
[7] Vaggelis Atlidakis, Patrice Godefroid, and Marina Polishchuk. 2019. RESTler: Stateful REST API fuzzing. In Proceedings
of the 41st International Conference on Software Engineering (ICSE).
[8] Justus Bogner, Stefan Wagner, and Alfred Zimmermann. 2020. Collecting Service-Based Maintainability Metrics from
RESTful API Descriptions: Static Analysis and Threshold Derivation. In Software Architecture, Henry Muccini, Paris
Avgeriou, Barbora Buhnova, Javier Camara, Mauro Caporuscio, Mirco Franzago, Anne Koziolek, Patrizia Scandurra,
Catia Trubiani, Danny Weyns, and Uwe Zdun (Eds.). Springer International Publishing, Cham, 215–227.
[9] Hudson Borges, Andre Hora, and Marco Tulio Valente. 2016. Understanding the Factors That Impact the Popularity of
GitHub Repositories. In 2016 IEEE International Conference on Software Maintenance and Evolution (ICSME). 334–344.
https://doi.org/10.1109/ICSME.2016.31
[10] Bright Data. 2025. Bright Data MCP Server. https://github.com/brightdata/brightdata-mcp. Accessed: 2026-03-13.
[11] Ricardo JGB Campello, Davoud Moulavi, and Jörg Sander. 2013. Density-based clustering based on hierarchical density
estimates. In Pacific-Asia conference on knowledge discovery and data mining. Springer, 160–172.
[12] Cashfree Payments. 2025. Cashfree MCP Server. https://github.com/cashfree/cashfree-mcp. Accessed: 2026-03-13.
[13] Xiang Chen, Chaoyang Gao, Chunyang Chen, Guangbei Zhang, and Yong Liu. 2025. An Empirical Study on Challenges
for LLM Application Developers. ACM Trans. Softw. Eng. Methodol. 34, 7, Article 205 (Aug. 2025), 37 pages. https:
//doi.org/10.1145/3715007
[14] Zehui Chen, Weihua Du, Wenwei Zhang, Kuikun Liu, Jiangning Liu, Miao Zheng, Jingming Zhuo, Songyang Zhang,
Dahua Lin, Kai Chen, et al. 2024. T-eval: Evaluating the tool utilization capability of large language models step by
step. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers).
9510–9529.
[15] Davide Corradini, Amedeo Zampieri, Michele Pasqua, and Mariano Ceccato. 2021. Restats: A Test Coverage Tool
for RESTful APIs. In 2021 IEEE International Conference on Software Maintenance and Evolution (ICSME). 594–598.
https://doi.org/10.1109/ICSME52107.2021.00063
[16] DataStax. 2025. Astra DB MCP Server. https://github.com/datastax/astra-db-mcp. Accessed: 2026-03-13.
[17] DeepL. 2025. DeepL MCP Server. https://github.com/DeepLcom/deepl-mcp-server. Online; accessed March 2026.
[18] Docker Inc. 2025. Docker MCP Catalog and Toolkit. https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/.
Accessed July 2025.
[19] Yu Du, Fangyun Wei, and Hongyang Zhang. 2024. Anytool: Self-reflective, hierarchical agents for large-scale api calls.
arXiv preprint arXiv:2402.04253 (2024).
[20] Zackary Okun Dunivin. 2025. Scaling hermeneutics: a guide to qualitative coding with LLMs for reflexive content
analysis. EPJ Data Science 14, 1 (2025), 28.
[21] Hamza Ed-Douibi, Javier Luis Cánovas Izquierdo, and Jordi Cabot. 2018. Automatic generation of test cases for REST
APIs: A specification-based approach. In 2018 IEEE 22nd international enterprise distributed object computing conference
(EDOC). IEEE, 181–190.
[22] GitGuardian. 2025. GitGuardian MCP Server (ggmcp). https://github.com/GitGuardian/ggmcp. Online; accessed
March 2026.
[23] GitHub. 2025. GitHub MCP Server. https://github.com/github/github-mcp-server. Online; accessed March 2026.
[24] GitHub, Inc. 2022. GitHub REST API OpenAPI Specification (2022-11-28). https://raw.githubusercontent.com/github/
rest-api-description/refs/heads/main/descriptions/api.github.com/api.github.com.2022-11-28.json. Accessed January
2026.
[25] Amid Golmohammadi, Man Zhang, and Andrea Arcuri. 2023. Testing restful apis: A survey. ACM Transactions on
Software Engineering and Methodology 33, 1 (2023), 1–41.
[26] Google Firebase. 2025. Firebase Tools MCP Integration. https://github.com/firebase/firebase-tools. Accessed: 2026-0313.
[27] Grafana Labs. 2025. Grafana MCP Server. https://github.com/grafana/mcp-grafana. Online; accessed March 2026.
[28] Maarten Grootendorst. 2022. BERTopic: Neural topic modeling with a class-based TF-IDF procedure. arXiv preprint
arXiv:2203.05794 (2022).
[29] Hechuan Guo, Yongle Hao, Yue Zhang, Minghui Xu, Peizhuo Lv, Jiezhi Chen, and Xiuzhen Cheng. 2025. A measurement
study of model context protocol ecosystem. arXiv preprint arXiv:2509.25292 (2025).

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 55

From REST to MCP: An Empirical Study of API Wrapping and Automated Server Generation for LLM Agents

0:43

[30] Mohammed Mehedi Hasan, Hao Li, Emad Fallahzadeh, Gopi Krishnan Rajbahadur, Bram Adams, and Ahmed E Hassan.
2025. Model context protocol (mcp) at first glance: Studying the security and maintainability of mcp servers. arXiv
preprint arXiv:2506.13538 (2025).
[31] Mohammed Mehedi Hasan, Hao Li, Gopi Krishnan Rajbahadur, Bram Adams, and Ahmed E Hassan. 2026. Model
Context Protocol (MCP) Tool Descriptions Are Smelly! Towards Improving AI Agent Efficiency with Augmented MCP
Tool Descriptions. arXiv preprint arXiv:2602.14878 (2026).
[32] Florian Haupt, Frank Leymann, Anton Scherer, and Karolina Vukojevic-Haupt. 2017. A Framework for the Structural
Analysis of REST APIs. In 2017 IEEE International Conference on Software Architecture (ICSA). 55–58. https://doi.org/10.
1109/ICSA.2017.40
[33] Florian Haupt, Frank Leymann, and Karolina Vukojevic-Haupt. 2018. API governance support through the structural
analysis of REST APIs. Computer Science-Research and Development 33, 3 (2018), 291–303.
[34] Honeycomb.io. 2025. Honeycomb MCP Server. https://github.com/honeycombio/honeycomb-mcp. Accessed: 2026-0313.
[35] Xinyi Hou, Yanjie Zhao, Shenao Wang, and Haoyu Wang. 2025. Model context protocol (mcp): Landscape, security
threats, and future research directions. ACM Transactions on Software Engineering and Methodology (2025).
[36] Kiran Kate, Tejaswini Pedapati, Kinjal Basu, Yara Rizk, Vijil Chenthamarakshan, Subhajit Chaudhury, Mayank Agarwal,
and Ibrahim Abdelaziz. 2025. LongFuncEval: Measuring the effectiveness of long context models for function calling.
arXiv preprint arXiv:2505.10570 (2025).
[37] Myeongsoo Kim, Davide Corradini, Saurabh Sinha, Alessandro Orso, Michele Pasqua, Rachel Tzoref-Brill, and Mariano
Ceccato. 2023. Enhancing rest api testing with nlp techniques. In Proceedings of the 32nd ACM SIGSOFT International
Symposium on Software Testing and Analysis. 1232–1243.
[38] Myeongsoo Kim, Tyler Stennett, Saurabh Sinha, and Alessandro Orso. 2025. A Multi-Agent Approach for REST API
Testing with Semantic Graphs and LLM-Driven Inputs. In Proceedings of the IEEE/ACM 47th International Conference on
Software Engineering (Ottawa, Ontario, Canada) (ICSE ’25). IEEE Press, 1409–1421. https://doi.org/10.1109/ICSE55347.
2025.00179
[39] AWS Labs. 2025. OpenAPI MCP Server. https://github.com/awslabs/mcp.
[40] Tri Le, Thien Tran, Duy Cao, Vy Le, Tien N Nguyen, and Vu Nguyen. 2024. KAT: Dependency-aware automated API
testing with large language models. In 2024 IEEE Conference on Software Testing, Verification and Validation (ICST).
IEEE, 82–92.
[41] Minghao Li, Yingxiu Zhao, Bowen Yu, Feifan Song, Hangyu Li, Haiyang Yu, Zhoujun Li, Fei Huang, and Yongbin Li.
2023. API-Bank: A comprehensive benchmark for tool-augmented LLMs. In Proceedings of the 2023 Conference on
Empirical Methods in Natural Language Processing (EMNLP). 3102–3116.
[42] Mailgun. 2025. Mailgun MCP Server. https://github.com/mailgun/mailgun-mcp-server. Online; accessed March 2026.
[43] Meriem Mastouri, Emna Ksontini, Amine Barrak, and Wael Kessentini. [n.d.]. Replication package TOSEM 2026.
https://sites.google.com/view/automcp.
[44] Leland McInnes, John Healy, and James Melville. 2018. Umap: Uniform manifold approximation and projection for
dimension reduction. arXiv preprint arXiv:1802.03426 (2018).
[45] MCP.so Community. 2025. MCP.so: Community MCP Server Directory. https://mcp.so/. Accessed July 2025.
[46] Model Context Protocol. 2024. Model Context Protocol Servers: Reference Implementations. https://github.com/
modelcontextprotocol/servers.
[47] MongoDB. 2025. MongoDB MCP Server. https://github.com/mongodb-js/mongodb-mcp-server. Accessed: 2026.
[48] Lauren Murphy, Mary Beth Kery, Oluwatosin Alliyu, Andrew Macvean, and Brad A. Myers. 2018. API Designers in
the Field: Design Practices and Challenges for Creating Usable APIs. In 2018 IEEE Symposium on Visual Languages and
Human-Centric Computing (VL/HCC), Lisbon, Portugal, October 1–4, 2018. IEEE Computer Society, 249–258. https:
//doi.org/10.1109/VLHCC.2018.8506523
[49] Neo4j. 2025. Neo4j MCP Server. https://github.com/neo4j/mcp. Accessed: 2026.
[50] Neon. 2025. Neon MCP Server. https://github.com/neondatabase/mcp-server-neon. Accessed: 2026.
[51] Andy Neumann, Nuno Laranjeiro, and Jorge Bernardino. 2018. An analysis of public REST web service APIs. IEEE
Transactions on Services Computing 14, 4 (2018), 957–970.
[52] Xinyi Ni, Qiuyang Wang, Yukun Zhang, and Pengyu Hong. 2025. ToolFactory: Automating Tool Generation by
Leveraging LLM to Understand REST API Documentations. https://doi.org/10.48550/arXiv.2501.16945
[53] Paloma Oliveira, Marco Tulio Valente, and Fernando Paim Lima. 2014. Extracting relative thresholds for source
code metrics. In 2014 Software Evolution Week-IEEE Conference on Software Maintenance, Reengineering, and Reverse
Engineering (CSMR-WCRE). IEEE, 254–263.
[54] OpenAPI Tools. 2025. OpenAPI Generator. https://github.com/OpenAPITools/openapi-generator. Accessed: 2025-0731.

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.

## Page 56

0:44

Mastouri et al.

[55] OWASP API Security Project Team. 2023. OWASP Top 10 API Security Risks – 2023. OWASP Foundation. https:
//owasp.org/API-Security/editions/2023/en/0x11-t10/
[56] Shishir G. Patil, Tianjun Zhang, Xin Wang, and Joseph E. Gonzalez. 2024. Gorilla: Large Language Model Connected
with Massive APIs. In Advances in Neural Information Processing Systems, A. Globerson, L. Mackey, D. Belgrave, A. Fan,
U. Paquet, J. Tomczak, and C. Zhang (Eds.), Vol. 37. Curran Associates, Inc., 126544–126565. https://proceedings.
neurips.cc/paper_files/paper/2024/file/e4c61f578ff07830f5c37378dd3ecb0d-Paper-Conference.pdf
[57] PortSwigger. 2025. Burp Suite MCP Server. https://github.com/PortSwigger/mcp-server. Accessed: 2026.
[58] PrefectHQ. 2025. FastMCP: Build MCP servers quickly. https://gofastmcp.com/integrations/openapi.
[59] Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, et al.
2023. Toolllm: Facilitating large language models to master 16000+ real-world apis. arXiv preprint arXiv:2307.16789
(2023).
[60] Martin P. Robillard. 2009. What Makes APIs Hard to Learn? Answers from Developers. IEEE Software 26, 6 (2009),
27–34. https://doi.org/10.1109/MS.2009.193
[61] Timo Schick, Jane Dwivedi-Yu, Roberto Dessí, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola
Cancedda, and Thomas Scialom. 2023. Toolformer: language models can teach themselves to use tools. In Proceedings of
the 37th International Conference on Neural Information Processing Systems (New Orleans, LA, USA) (NIPS ’23). Curran
Associates Inc., Red Hook, NY, USA, Article 2997, 13 pages.
[62] Sentence-Transformers. 2021. all-MiniLM-L6-v2: Sentence-Transformers model. https://huggingface.co/sentencetransformers/all-MiniLM-L6-v2.
[63] Souhaila Serbout, Fabio Di Lauro, and Cesare Pautasso. 2022. Web APIs Structures and Data Models Analysis. In 2022
IEEE 19th International Conference on Software Architecture Companion (ICSA-C). 84–91. https://doi.org/10.1109/ICSAC54293.2022.00059
[64] Souhaila Serbout and Cesare Pautasso. 2024. APIstic: A Large Collection of OpenAPI Metrics. 2024 IEEE/ACM 21st
International Conference on Mining Software Repositories (MSR) (2024), 265–277. https://api.semanticscholar.org/
CorpusID:270593554
[65] Zhengliang Shi, Yuhan Wang, Lingyong Yan, Pengjie Ren, Shuaiqiang Wang, Dawei Yin, and Zhaochun Ren. 2025.
Retrieval models aren’t tool-savvy: Benchmarking tool retrieval for large language models. In Findings of the Association
for Computational Linguistics: ACL 2025. 24497–24524.
[66] Shortcut. 2025. Shortcut MCP Server. https://github.com/useshortcut/mcp-server-shortcut. Online; accessed March
2026.
[67] Apitchaka Singjai, Uwe Zdun, Olaf Zimmermann, Mirko Stocker, and Cesare Pautasso. 2021. Patterns on Designing API
Endpoint Operations. In Proceedings of the 28th Conference on Pattern Languages of Programs (PLoP ’21), Virtual Conference, October 5–7, 2021. 1–29. https://eprints.cs.univie.ac.at/7194/1/patterns-on-designing-api-endpoint-operationsproceeding-version5.pdf
[68] SmartBear Software. 2025. Swagger Codegen. https://github.com/swagger-api/swagger-codegen. Accessed: 2025-07-31.
[69] Yifan Song, Weimin Xiong, Dawei Zhu, Wenhao Wu, Han Qian, Mingbo Song, Hailiang Huang, Cheng Li, Ke Wang,
Rong Yao, et al. 2023. RestGPT: Connecting large language models with real-world RESTful APIs. arXiv preprint
arXiv:2306.06624 (2023).
[70] Mina Taraghi, Mohammad Mehdi Morovati, and Foutse Khomh. 2026. Real Faults in Model Context Protocol (MCP)
Software: a Comprehensive Taxonomy. arXiv preprint arXiv:2603.05637 (2026).
[71] John W. Tukey. 1977. Exploratory Data Analysis. Addison-Wesley.
[72] Gias Uddin and Martin P Robillard. 2015. How API documentation fails. Ieee software 32, 4 (2015), 68–75.
[73] Marat Valiev, Bogdan Vasilescu, and James Herbsleb. 2018. Ecosystem-level determinants of sustained activity in
open-source projects: a case study of the PyPI ecosystem. In Proceedings of the 2018 26th ACM Joint Meeting on
European Software Engineering Conference and Symposium on the Foundations of Software Engineering (Lake Buena
Vista, FL, USA) (ESEC/FSE 2018). Association for Computing Machinery, New York, NY, USA, 644–655. https:
//doi.org/10.1145/3236024.3236062
[74] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language Models. In The Eleventh International Conference on Learning Representations.
https://openreview.net/forum?id=WE_vluYUL-X
[75] Robert K Yin. 2009. Case study research: Design and methods. Vol. 5. sage.

ACM Trans. Softw. Eng. Methodol., Vol. 0, No. 0, Article 0. Publication date: 2026.
