---
id: literature/fulltexts/gis-mcp-server-cluster-2026
type: fulltext
status: frozen
language: en
key: gis-mcp-server-cluster-2026
title: >-
  MapHub: an OGC web GIS service aggregation and query MCP server for AI agents
resource: https://doi.org/10.1117/12.3091756
description: >-
  Geographic Information Systems (GIS) are evolving from specialized tools into inclusive spatial intelligence infrastructure, yet non-professional users still face core challenges: inefficient geospatial data discovery and high barriers to complex spatial analysis.
pages: 15
words: 5540
year: 2026
venue: >-
  SPIE
authors: >-
  Liu, Su; Zheng, Weipeng; Xiao, Yufeng; Weng, Yamin; Yuan, Ying; Yu, Qipeng; Zeng, Zhiqiang
doi: 10.1117/12.3091756
oa_status: OA landing only
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# MapHub: an OGC web GIS service aggregation and query MCP server for AI agents

## Page 1

MapHub: An OGC Web GIS Service Aggregation and Query MCP
Server for AI Agents
Su Liua, Weipeng Zhengb, Yufeng Xiaoc, Yamin Wengd,Ying Yuane,1, Qipeng Yue, Zhiqiang Zenge
a
Fujian Provincial Tobacco Monopoly Bureau
b
Putian Municipal Tobacco Monopoly Bureau
c
Fuzhou Municipal Tobacco Monopoly Bureau
d
Xiamen Haisheng Rongchuang Information Technology Co., Ltd.
e
Xiamen University of Technology
ABSTRACT
Geographic Information Systems (GIS) are evolving from specialized tools into inclusive spatial intelligence
infrastructure, yet non-professional users still face core challenges: inefficient geospatial data discovery and high barriers
to complex spatial analysis. Traditional Web GIS platforms struggle to accurately match natural language intents (e.g.,
"Which states border the Mississippi River?") with distributed OGC services (WMS/WFS/WMTS) and execute relevant
spatial queries. While Large Language Models (LLM) and Model Context Protocol (MCP) maturity provide the
technical foundation for intelligent interaction, current GIS ecosystems lack a unified framework to integrate distributed
OGC services and expose them for LLM agent invocation, resulting in a "semantic-spatial disconnect." To address this,
we propose MapHub , an OGC service aggregation and query MCP Server for AI Agents. This lightweight, crossplatform deployable MCP Server, built on FastMCP, enables dynamic registration, aggregation, and transformation of
OGC services into MCP resources and tools, supporting plug-and-play integration of heterogeneous WMS/WFS/WMTS
services. By closing the loop between intent understanding, resource discovery, and tool invocation, it constructs an
intelligent layer scoring system to enhance accuracy in identifying primary layers during queries. Additionally, it designs
a visualization pipeline using a declarative HTML generation framework, seamlessly interfacing with Leaflet to
automate the conversion of query results into interactive maps. MapHub’s open-source implementation
(https://github.com/YQP-2511/maphub-core) provides a reference for natural language-driven spatial intelligence
applications, propelling Web GIS into the era of "conversation-as-map." Future work will extend WPS support for
complex analyses and explore distributed architectures for million-layer scheduling.
Keywords: OGC Web GIS Service, Model Context Protocol(MCP), AI Agent,Large Language Models(LLM), ​
Semantic-Spatial Integration, Dynamic Service Registration, Intelligent Layer Scoring, Geo visualization

1. INTRODUCTION
Geographic Information Systems (GIS) are undergoing a profound evolution—transitioning from specialized domainspecific tools toward inclusive spatial intelligence infrastructure. Nevertheless, Web GIS applications for non-expert
users continue to confront critical challenges, centering on two core pain points: inefficient discovery and acquisition of
geospatial data, and prohibitively high barriers to spatial analysis operations.User intents struggle to precisely match
fragmented geospatial layer services scattered across platforms and diverse protocols (WMS/WFS/WMTS). Users drown
in isolated islands of heterogeneous services, unable to efficiently locate suitable, accessible, and authoritative
underlying data sources for their analytical needs.Even when layers are acquired, traditional Web GIS platforms lock out
most non-experts through complex map operation interfaces (overlay analysis, buffer queries, attribute filtering) and
specialized spatial query languages (Spatial SQL, CQL). Users lack both the knowledge and tools to translate natural
language spatial questions (e.g., "Which cities along the Mississippi River have populations exceeding one million?")
into executable spatial workflows.

1

Corresponding Author.Ying Yuan,E-mail:yuanying@xmut.edu.cn.

International Conference on Mechanical, Engineering, and Interaction Design (ICMEID 2025), edited by Lakhmi C. Jain,
Qun Wu, Fuqian Shi, Valentina E. Balas, Proc. of SPIE Vol. 14018, 140184B · © The Authors. Published under
a Creative Commons Attribution CC-BY 4.0 License · doi: 10.1117/12.3091756
Proc. of SPIE Vol. 14018 140184B-1

## Page 2

Simultaneously, two major technological advancements present unprecedented opportunities to overcome these
challenges. 1.Explosive Growth and Enhanced Accessibility of Large Language Models (LLMs): Models like ChatGPT
and DeepSeek now exhibit exceptional intent comprehension, knowledge integration, and tool invocation capabilities.
They can accurately parse spatial intents from natural language descriptions while unlocking the potential to orchestrate
external tools for complex tasks, establishing the technical foundation for an intelligent “conversation-as-service” GIS
paradigm. 2.Maturation of Model Context Protocol (MCP) Ecosystem and Toolchain Refinement:The rapid evolution of
MCP and its frameworks (e.g., FastMCP) delivers standardized, structured interaction protocols between LLMs and
external systems (e.g., web services). This enables the construction of LLM-powered agents (AI Agents) capable of
coordinating intricate calls to distributed functional services.
However, a critical gap currently impedes LLMs from reaching their full potential in the GIS domain: the absence
of a unified framework capable of seamlessly integrating distributed, standardized OGC Web Services
(WMS/WFS/WMTS) while efficiently exposing their capabilities to LLM agents for invocation. Existing solutions are
either confined to proprietary platforms (unable to incorporate external resources) or suffer from monolithic visualization
schemes that fail to support intuitive presentation of composite spatial queries. More critically, they lack robust bridging
between natural language semantics and underlying spatial data/operations - resulting in a "semantic-spatial gap".
To address this, we present MapHub—an OGC Web GIS service integration and query tool designed for AI Agents.
Its core mission is to resolve two fundamental user pain points - "inaccessible geospatial layers" and "unactionable
analytical queries" - by constructing an intelligent bridge between LLM agents and distributed OGC Web services. The
innovations encompass:
1.

Enables plug-and-play integration of heterogeneous WMS/WFS/WMTS services, transforming fragmented
geospatial resources into LLM-comprehensible MCP resources and tools.

2.

Combines intent comprehension, resource discovery, and tool invocation in a closed loop, enhanced by a global
layer cache and intelligent primary-layer scoring algorithm to execute composite spatial queries with precision.

3.

Leverages a declarative HTML generation framework to seamlessly interface with mainstream engines (Leaflet),
automating the conversion from configuration to interactive maps for intuitive multidimensional spatial analysis.

MapHub achieves three pivotal breakthroughs: implementing an OGC service registration mechanism
encompassing service discovery → protocol parsing → resource mapping → tool generation, dramatically enhancing
GIS service registration efficiency and LLM accessibility to geospatial capabilities; establishing an intelligent layer
scoring system that automatically prioritizes primary views based on multidimensional metrics including data richness
and spatial rationality; and engineering a responsive visualization pipeline that dynamically publishes interactive
analytical results through unique ephemeral visualization IDs.
Benchmarked on DeepSeek V3 and Cherry Studio, MapHub demonstrated perfect query accuracy across 30 realworld tasks, including "Distribution of U.S. States Exceeding 20 Million Population" (detailed in Section 4.2)..This work
provides open-source implementation (https://github.com/YQP-2511/maphub-core) to pioneer natural language-driven
spatial intelligence applications, ushering Web GIS into the "conversation-as-map" era.

2. RELATED WORK
2.1 OGC Web GIS Services
Cross-platform interoperability in Geographic Information Systems (GIS) has long been constrained by data
heterogeneity and technological siloing. To address this fundamental challenge, the Open Geospatial Consortium (OGC)
launched the OGC Web Services (OWS)[1] initiative in 2001, progressively establishing an open service standard
framework based on the HTTP protocol. This system revolutionizes traditional GIS's tightly coupled architectures by
defining unified service interfaces and data exchange specifications, enabling decoupled spatial data publishing, dynamic
integration, and cross-platform interoperability.
Between 2006 and 2009, OGC formally released and iterated its core map service specifications, including
WMTS(Web Map Tile Service)[2],WMS (Web Map Service)[3],WFS (Web Feature Service)[4] and WPS(Web Processing
Service)[5] and so on. WMTS is designed for high-concurrency raster basemap access, it defines a pre-tiled transmission
mechanism using standardized column-row indexing and zoom levels to enable sub-second global imagery loading,
establishing itself as the cornerstone of web mapping infrastructure. WMS provides dynamic map rendering capabilities

Proc. of SPIE Vol. 14018 140184B-2

## Page 3

with SLD (Styled Layer Descriptor) support for layer symbology customization. It leverages BBOX (Bounding Box)
parameters for spatial extent definition and CRS (Coordinate Reference System) parameters for coordinate system
specification, enabling multi-source data overlay for on-demand thematic map generation. WFS breaks through imagebased map limitations by offering vector feature-level operations. Supports spatial/attribute filtering via CQL (Common
Query Language)[6], enables feature CRUD (Transaction operations), and facilitates GML/GeoJSON format exchanges
to establish structured data foundations for spatial analysis.
These specifications enforce mandatory conventions for service metadata descriptions (GetCapabilities), requestresponse protocols (KVP/SOAP), and coordinate reference system mapping (EPSG codes)[7], enabling unified clients
(e.g., OpenLayers, Leaflet) to integrate and invoke GIS servers from diverse vendors (e.g., ArcGIS Server, GeoServer),
thereby resolving "protocol silos" across multi-source services. They further support service chaining (e.g., WMS
consuming WFS data sources), driving the evolution of spatial data processing from centralized to distributed
microservice architectures. Users can aggregate cross-domain services (e.g., meteorological WMS + transportation WFS)
through unified views to build cross-institutional collaborative applications. Global GIS leaders (ESRI, SuperMap, etc.)
universally comply with OGC service interfaces, fostering a millions-strong open service resource pool that tangibly
matures the geospatial service ecosystem.
Driven by web technology advancements, OGC has further introduced RESTful APIs (e.g., OGC API-Features)[8] to
replace legacy XML protocols while strengthening integration with cloud-native architectures. Nevertheless, critical
challenges persist—including the absence of dynamic service discovery mechanisms and inadequate support for complex
analyses—urgently demanding next-generation frameworks to enable intelligent service resource scheduling and ondemand aggregation.
2.2 LLM, AI Agent and MCP
Large Language Models (LLMs) drive intelligent interactive systems by leveraging powerful semantic comprehension
and generation capabilities to precisely transform human instructions into machine-executable intents, functioning
through three core mechanisms: semantic comprehension utilizes word embeddings, syntactic analysis , and deep
contextual modeling to identify user intents and critical entities (e.g., parsing "check" as intent and "Seattle/next
Monday" as slots from "What’s Seattle’s weather next Monday?"); dynamic generation employs Transformer-based[9]
architectures to produce coherent responses and decomposes complex tasks via Chain-of-Thought[10] prompting for
stepwise reasoning (e.g., generating Python scripts for data analysis workflows); tool invocation interfaces convert
natural language commands into structured API parameters through function calling, such as triggering calendar
scheduling tools for "Schedule a meeting with Alex at 3 PM tomorrow" directives.
AI Agents[11], powered by LLMs as their "cognitive core," are intelligent systems with perception, decision-making,
and execution capabilities that autonomously achieve defined objectives. Through modular architectures integrating
LLMs' reasoning with external tools, they establish perception-planning-action loops to transcend conversational
limitations. Functionally, agents leverage standardized protocols (e.g., MCP) to invoke external APIs, databases, or
sensors—obtaining real-time information (e.g., stock quotes) and executing operations (e.g., smart home control)—thus
overcoming LLMs' constraints in timeliness and agency. For memory augmentation, they employ vector databases[12] to
store user preferences and dialogue histories, enabling long-term context management that bypasses LLMs' token limits.
Agents further demonstrate collaborative workflow intelligence: LLMs decompose complex goals (e.g., "plan a trip")
into subtasks (book flights/select hotels), while agents orchestrate tools via workflow engines and dynamically adjust
plans based on outcomes. This evolution transforms LLMs from reactive systems into proactive autonomous entities,
achieving a qualitative leap from "reasoning" to "action." Rapid advancements have spawned numerous code-oriented
agent architectures—including Cursor, Claude Code, and TRAE—which automatically generate and execute code based
on user requirements.
The Model Context Protocol (MCP)[13] was formally introduced by Anthropic in November 2024 to address
interoperability challenges between large language models (LLMs) and external data sources/tools. Its design emerged
from recognizing AI development fragmentation—previously, developers wrote redundant adapter code for different
models (e.g., GPT, Claude), whereas MCP standardizes resource invocation through unified interfaces, significantly
reducing integration costs. The protocol gained rapid industry traction: OpenAI announced MCP support for ChatGPT
desktop and APIs in March 2025, establishing it as a de facto standard, while Alibaba Cloud's Bailian launched full
lifecycle MCP services enabling 5-minute agent deployment, validating enterprise viability. GitHub saw MCP-related
projects surge within six months, with frameworks like FastMCP[14] empowering vertical-domain tool development. The

Proc. of SPIE Vol. 14018 140184B-3

## Page 4

MCP.so[15] now hosts over 13,000 MCP servers. However, MCP Servers for Web GIS remain scarce, particularly lacking
implementations for multi-source data integration and geospatial visualization.
2.3 Integration Studies of AI Agents with GIS
With the continuous advancement of AI Agent technologies, increasing numbers of GIS vendors have initiated
integration research to incorporate AI Agents into their products. Ageospatial[16] pioneered the industry in 2024 with its
GeoLLM platform—an agent system deeply integrating geospatial large language models (fine-tuned from GPT-4) with
GIS. Through direct interaction with GeoLLM, it enables dynamic map adjustments, base map style customization,
automated camera calibration, and interactive visualizations, while providing high-quality datasets for geospatial
analytics. This platform has been deployed in disaster response, urban planning, and public services. In June 2025,
SuperMap launched SuperMap AgentX Server[17], which interfaces with multiple LLMs to deliver comprehensive
capabilities—including intent understanding, logical reasoning, task planning, and decision execution—for complex GIS
operations via conversational interfaces. It serves applications across natural resources management, smart construction,
and digital twin water conservancy. From 2024 to 2025, Esri's ArcGIS AI Assistants[18] have reengineered GIS
workflows through natural language interaction, offering code generation, document Q&A, and offline operational
support. This closed-loop system (intent comprehension → tool orchestration → autonomous execution) significantly
lowers operational barriers, with implementations in municipal governance (e.g., Washington D.C. civic Q&A) and
disaster assessment (e.g., flood damage form automation).
However, these solutions predominantly rely on proprietary platforms and datasets, deploying custom-built AI
Agents for geospatial data management and analysis, exhibiting weak support for generic agents and limited
interoperability as external tools. They prioritize internal tool orchestration while neglecting cross-vendor tool
registration and coordination standards, impeding multi-agent collaboration. Insufficient OGC Web Service
compatibility—particularly non-standardized integration with WFS/WMS protocols—creates cross-platform data
scheduling barriers. These limitations constitute the primary motivation for MapHub’s development.

3. TECHNICAL APPROACH
3.1 Architecture and Workflow
MapHub MCP Server bridges general OGC Web GIS services and AI Agents by enabling natural language-driven
map operations and visualizing conversational outputs. The workflow operates as follows: As an AI-oriented mapping
component, MapHub converts published GIS services (WMS, WFS, WMTS) into MCP Resources via a registration
center (1), while transforming common map operations into MCP Tools (2). During AI Agent interactions, clients
interpret user intent through natural language dialogue and access MapHub's resources/tools(3). Agents then
autonomously invoke external map services via MCP Tools (4,5,6) with MCP Resouces, process returned geospatial data
(7), organize results, and push interactive map viewer links to chat interfaces for direct query result exploration(9,10).

Figure 1. Architecture and workflow of MapHub

Proc. of SPIE Vol. 14018 140184B-4

## Page 5

3.2 Registration of OGC Web GIS Services for MCP Resources and Tools
Web GIS has evolved a mature suite of OGC service specifications (e.g., WMS, WFS, WMTS), establishing
foundational interoperability across GIS platforms. However, traditional service integration requires manual parsing of
capability documents and custom adapter coding, leading to configuration complexity and cross-platform compatibility
issues. This work proposes an MCP-based dynamic service registration mechanism enabling automatic adaptation of
WMTS/WMS/WFS services and mapping of layer resources.The registration workflow comprises:

Figure 2. Workflow of OGC Web GIS services regisration in MapHub

Service Discovery:Identify potential map services via Web GIS server endpoints.
Protocol Parsing:Invoke OGC GetCapabilities interfaces (WMS/WFS/WMTS), parse returned XML documents to
determine service types, and extract MCP resources.
Resource Mapping: Convert diverse Web GIS server layers into Tools and Resources within the MCP Server (as
detailed in Tables 1), specifically transforming WMS Layers, WFS FeatureTypes, and WMTS MatrixSets into MCP
resources or resource templates.
Table 1. MCP Resources in MapHub

Resources Name

URI Pattern

Description

Layers list

ogc://layers

List all registered Web GIS Layers

Layer Details

ogc://layer/{layer_name}

Returns detailed metadata of a specific Web
GIS layer

Proc. of SPIE Vol. 14018 140184B-5

## Page 6

Registration Execution: The mapped resources are updated and merged into the MapHub MCP Server, endowing
its Resources with registered map server metadata that enables AI Agents to utilize service-access tools—leveraging
MCP tools and resource information—for accessing relevant OGC-served layers.​
To enable AI Agents to discover optimal geospatial layers and generate map visualizations, we engineered an MCP
toolchain (as detailed in Table 2) performing dynamic OGC service registration (register_ogc_service) while executing
geospatial query workflows—resource discovery (search_and_list_geographic_data), context-aware layer integration
(add_wmts_layer/add_wms_layer/add_wfs_layer), attribute-driven data filtering (get_wfs_layer_attributes), and
ultimately orchestrating composite cartographic outputs (create_composite_visualization).
Table 2. MCP Tools in MapHub

Tool Name

Description

register_ogc_service

OGC map service registration

search_and_list_geographic_data

Query and list all registered geospatial data resources

add_wmts_layer

Add WMTS layer to the result map

add_wms_layer

Add WMS layer to the result map

add_wfs_layer

Add WFS layer (full or filtered dataset) to the result map

get_wfs_layer_attributes

Retrieve attributes of WFS featuretype

create_composite_visualization

Generate composite-layer visualization map

3.3 Geospatial Query Result Visualization Pipeline
MapHub, as an MCP server invoked by AI Agents, enables natural language-driven geospatial querying and
visualization, answering spatial queries such as "Which U.S. states have populations exceeding 20 million and where are
they distributed?" or "Which states border the Mississippi River?" through four core visualization steps: Layer Collection
aggregates relevant geodata resources; Algorithmic Configuration intelligently optimizes map parameters; HTML
Generation produces declarative map rendering code; and Result Publishing deploys interactive visualizations via unique
URLs (see Figure 3).

Figure 3. Pipeline of Geospial Query result in MapHub

Layer Collection:Initiates with the LLM interpreting user intent and invoking search_and_list_geographic_data to
retrieve relevant layer inventories, followed by protocol-specific metadata acquisition (validating integrity/availability),
generating standardized abstracts categorized by service type (see table 3), and populating a global layer cache with
layers and abstracts for subsequent processing.
Table 3. MCP Tools in MapHub

Layer Type

Layer Abstract Specifications

WMS

Service URL, dynamic BBOX status, SLD style count

WFS

Feature count, geometry types, filter status, attribute schema

WMTS

Tile matrix sets, formats, style info

​

Proc. of SPIE Vol. 14018 140184B-6

## Page 7

Layer Configuration: Employing a scoring strategy across AI-selected task-relevant layers, this phase determines
the primary layer and computes automated cartographic configuration based on its metadata abstract. The computational
workflow encompasses: primary layer selection, centroid calculation, zoom-level optimization, and bounding box
consolidation—intelligently determining layer rendering order and initial map extent. Primary layer selection applies
weighted scoring across five dimensions: layer protocol type (WMS/WFS/WMTS), data richness , spatial coverage
coherence , semantic keyword relevance and special capabilities ( see Figure 4).

Figure 4. Layer Evaluation Criteria in MapHub

HTML Generation: After layer configuration is completed, based on existing map display frameworks such as
OpenLayers and Leaflet, the HTML page for map query results is generated according to the following process. Detailed
steps include JavaScript code generation for layers, page layout construction, and interactive function integration.
JavaScript code generation for different layer types:for WMS, generate layer configurations including service URL,
layer name, style, transparency, etc;for WFS, generate layer configuration information in GeoJSON format, including
feature data, styles, pop-up boxes, etc; for WMTS, generate tile layer configurations including matrix sets, zoom levels,
formats, etc.
Page layout structure generation: generate page layout structures based on elements such as layer information
panels, toolbars, main map areas, and control information. This page layout structure forms a universal template for
assembling OGC service data sources according to layer configuration information.
Further, integrate common interactive functions into the page using responsive design principles, including fullscreen toggle, zoom, measurement tools, coordinate display, and layer control, enabling adaptation to different screen
sizes.

Proc. of SPIE Vol. 14018 140184B-7

## Page 8

Result Publishing:Construct an ephemeral directory for the HTML page generated in the previous step, configure
necessary static resources for proper page rendering, assign a unique visualization ID to each request, launch an HTTP
service within MAPHUB to generate a dedicated accessible URL for the page, and finalize the publication of visualized
query results.

4. IMPLEMENTATION AND EVALUATION
Following the technical roadmap outlined above, this study leverages the FastMCP framework as the foundational
infrastructure for the MCP Server development. Utilizing diverse online and local OGC-compliant endpoints (WMS,
WFS, WMTS) as test services, we engineered a functional MapHub prototype system. Validation was conducted through
integration with the Cherry Studio platform as the AI Agent client, connected to the DeepSeek V3 0324 API to assess
MapHub's functional viability.
4.1 Prototype System Implementation

System Architecture and Technology Stack Overview

The prototype system architecture is illustrated below (see Figure 5), with core components constructed within the
dashed-line box. The foundational layer consists of external ​ OGC-compliant map services, while the upper layer
interfaces with universal AI Agent clients such as Cherry Studio​ and Cursor. Built upon the FastMCP framework, the
system implements MapHub's core services—service registration, resource management, tool invocation, and
visualization engine—to address OGC web service aggregation, querying, and visualization demands. Service metadata
and ephemeral visualization dependencies are persistently stored and managed via SQLite databases and file systems.

Figure 5. Architectural Framework of MapHub Prototype System

We implemented this prototype system in Python using the following technology stack:
•​

Core Framework: FastMCP 2.0 for AI Agent communication and invocation

•​

OGC Service Integration: OWSLib 0.29 for automated service registration and metadata parsing

•​

Data Validation: Pydantic 2.0 for structured data modeling

•​

Service Deployment: Uvicorn + Starlette for API hosting and visualization publishing

Proc. of SPIE Vol. 14018 140184B-8

## Page 9

•​

Database Operations: aiosqlite 0.19 for asynchronous SQLite interactions

Within the FastMCP Server architecture, MapHub's business logic is modularized into:
•

Management Tools Server (mgmt_*)

•

WMS Layer Tools Server (wms_*)

•

WMTS Tools Server (wmts_*)

•

Visualization Tools Server (viz_*)

•

Layer Resource Server (ogc://)

These components are integrated into the primary MapHub server, delivering online layer tooling services for
diverse AI Agents. Implementation code available at (https://github.com/YQP-2511/maphub-core).

Key Module Implementation

1. OGC Web GIS Service Registration Module Implementation

This module implements OGC service registration through three sequential phases:
OGC Service URL Sanitization Phase:
Standardizes user-input OGC service URLs by removing query parameters and fragment identifiers, normalizes
URLs to obtain complete capabilities request URLs, probes potential endpoints via predefined endpoint detection
strategies using HTTP HEAD requests to identify available endpoints, then extracts service names to identify domain
names and service identifiers.
Service Parsing Phase:
Utilizes validated service endpoint URLs to construct capability documents via OGC's GetCapabilities interface.
After validating Capabilities documents, it parses OGC service capabilities using OWSLib to extract service metadata
(title, description, version, etc.), then iterates through service layers (FeatureTypes or MatrixSets) to obtain layer names,
titles, descriptions, bounding boxes, and coordinate reference systems.
Database Storage Phase:
Stores parsed service information uniformly in an SQLite database (see Figure 6), implementing deduplication and
expired layer cleanup strategies during storage, and finally returns registration results and current status.

Figure 6. OGC Web GIS Service Registration in Cheery Studio

Proc. of SPIE Vol. 14018 140184B-9

## Page 10

2. Layer Resource Transformation Implementation
For OGC layer resources
stored in the SQLite database, this module converts them into MCP resources (see Figure 7)
​
accessible to AI Agents through two primary methods:
Layer List Resource
Returns all registered layers in MapHub via the resource URL ogc://layers, providing a comprehensive catalog of
available geospatial datasets.

Figure 7. Transfer Layers Into MCP Resources

Layer Detail Resource Template

​
Returns detailed information for each layer via the resource URL ogc://layer/{layer_name}, enabling AI Agents to
programmatically access service metadata during tool invocation. When multiple service types (WMTS, WMS, WFS)
share identical layer names, this endpoint returns protocol-specific metadata including Foundational Metadata ,
Capability Metadata and Access Parameters (see Figure 8). The structured metadata enables AI Agents to dynamically
construct valid service requests for online layer invocation.

Figure 8. Access Parameters for WMS/WFS/WMTS Returned From Layer Detail Resource Template

Proc. of SPIE Vol. 14018 140184B-10

## Page 11

3. Visualization Implementation for Query Results
During the visualization phase, Leaflet is employed as the mapping engine to render overlaid layers according to the
Section 3.3 design. Upon receiving user queries, the AI Agent autonomously retrieves layer resources from MapHub,
selects appropriate layers based on query requirements, performs data filtering, constructs visualization scripts, publishes
them within the MapHub MCP Server, and ultimately outputs an accessible URL for users to view the final interactive
results. Figures 9 through 12 demonstrate two visualization examples of map query results in Cherry Studio .
Case 1:Retrieve all U.S. states with land areas between 100,000 and 500,000 square kilometers.

Figure 9. Dialogue Content of Case 1 in Cheery Studio

Figure 10. Map Visualization Results for Case 1

Proc. of SPIE Vol. 14018 140184B-11

## Page 12

Case 2:Query population data for states traversed by the Mississippi River.

Figure 11. Dialogue Content of Case 2 in Cheery Studio

Figure 12. Map Visualization Results for Case 2

4.2 MapHub Capability Validation
To validate MapHub's capabilities in geospatial data discovery, analysis, and visualization, we registered 61 layer
resources across online and offline environments and designed 30 map query tasks. Using DeepSeek-V3 0324 as the
core large language model (LLM), all tasks were successfully executed and visualized within Cherry Studio,
preliminarily confirming MapHub's functional feasibility.
Data source URLs of OGC Web GIS services used in testing:
• https://ows.terrestris.de/osm
• http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi?service=wms\&request=getcapabilities
• http://localhost:8090/geoserver
• http://gisserver.tianditu.gov.cn/TDTService/wfs

Proc. of SPIE Vol. 14018 140184B-12

## Page 13

• http://gisserver.tianditu.gov.cn/TDTService/wms
• http://gisserver.tianditu.gov.cn/TDTService/wmts
We designed two task categories, including single-layer retrieval & visualization and spatial query filtering &
visualization. The task list is as follows:
Single-Layer Retrieval Tasks
1.Manhattan Road Network, New York, USA
2.Tasmania Road Infrastructure
3.Landmarks in Manhattan, USA
4.Global National Boundaries
5.World Disputed Territories Data
6.Global Coastlines
7.Tasmania Water Bodies
8.Points of Interest in Manhattan, New York
9.International Boundary Lines
10.Global Human Settlements Data
11.U.S. State Population Statistics
12.Global Urban Areas Dataset
13.Tasmania City Data
14.Tasmania Administrative Boundary
15.World Basemap Data
Spatial Filter Query Tasks​
1.Highlight U.S. states with population >10 million
2.Visualize states where male population > female population
3.Show states with names starting with 'A'
4.Display states with land area >100,000 km2
5.Visualize states with workforce size >1 million
6.Highlight states with water area >2,000 km2
7.Show states with >500,000 households
8.Visualize states with employed population >5 million
9.Highlight states with unemployed population <100,000
10.Show states with >1 million housing units
11.Display states with population <1 million
12.Visualize U.S. West Coast states (CA, OR, WA)
13.Show states where male population < female population
14.Highlight states traversed by the Mississippi River
15.Display states adjacent to California

Proc. of SPIE Vol. 14018 140184B-13

## Page 14

Finally, we designed the following prompt for the LLM in Cherry Studio to ensure proper usage of MapHub:
You are an expert in world geography information and tool usage, possessing geographical knowledge without
describing tool invocation details—directly call tools instead. You must strictly follow the visualization workflow below
in sequence:
1.

Call the tool mgmt_search_and_list_geographic_data.

2.

Call wms_add_wms_layer or wmts_add_wmts_layer or both once to add relevant layers.

3.

Call the tool mgmt_get_wfs_layer_attributes, then call wfs_add_wfs_layer: Filter if needed based on user
requirements, and sort by specified attributes when filtering.

4.

Wait until all layers are successfully added (failed WFS layer filtering does not count as success). Then call
the tool: viz_create_composite_visualization.

5.

After execution, you must call the tool in the fifth step and output the visualization result and its link.

5. DISCUSSION
5.1 Core Advantages
Addressing the challenge of non-experts struggling to discover and analyze geospatial data, this paper proposes
MapHub—an MCP Server that aggregates OGC Web GIS services and enables cartographic visualization for AI Agents.
We developed a prototype system validating this approach, achieving three key innovations:
This work pioneers plug-and-play integration of OGC Web GIS services (WMS/WFS/WMTS) within MCP
environments, significantly lowering the technical barriers for connecting GIS services to LLM AI agents.
We proposed an intelligent layer scoring system that integrates multiple dimensions—including data richness ,
spatial rationality and semantic relevance — to implement a primary layer selection strategy. This approach achieved
100% accuracy in selecting optimal primary layers across 30 test tasks, preliminarily resolving the "semantic-spatial
disconnect" issue inherent in traditional GIS.
We designed a streamlined visualization pipeline for map query results, leveraging a declarative HTML generation
framework to automate the conversion from query outputs to interactive maps. By dynamically publishing analytical
outcomes through unique ephemeral visualization IDs, this system enables direct integration of visualization links into
general-purpose AI Agent chat interfaces, thereby validating the feasibility of the "conversation-as-map" paradigm.
5.2 Limitation
As a conceptual research prototype, MapHub exhibits limitations in the following aspects:
Service Integration Scope: Currently supports only OGC data services (WMTS/WMS/WFS) with basic spatial
queries, lacking geographic processing service (WPS) integration—a critical direction for future work.
Visualization Capabilities: Limited to layer-overlay rendering, requiring expansion to advanced cartographic
representations (heatmaps, density surfaces, flow maps, grid visualizations) to enhance AI Agent support.
5.3 Comparison with Related Work
Compared to solutions from SuperMap and ESRI, MapHub distinguishes itself through universal compatibility and
openness by supporting integration with all OGC-compliant layer services while being deployable across any cloud or
desktop environment, and accessible to any general-purpose AI Agent for geospatial Q&A; however, we acknowledge
limitations in spatial analysis and visualization capabilities compared to dedicated Geo AI agents—gaps targeted for
future improvements.

6. CONCLUSION
MapHub pioneers a natural language-driven paradigm for intelligent OGC service aggregation and interaction,
establishing an open bridge between AI Agents and distributed geospatial resources. Experiments confirm its
effectiveness in resolving dual bottlenecks of "difficult layer discovery" and "high barriers to spatial analysis" in
traditional Web GIS. Our current work implements a dynamic registration mechanism for OGC Web GIS services,

Proc. of SPIE Vol. 14018 140184B-14

## Page 15

enabling plug-and-play integration of WMS/WFS/WMTS services; proposes a scoring strategy that accurately identifies
primary layers among multiple candidates; and designs a visualization approach that empowers AI Agents to effectively
deliver map query results within conversations, validating the "conversation-as-map" concept. MapHub's open-source
implementation accelerates the evolution of Web GIS toward intelligent, democratized accessibility in the AI era. Future
work will extend MapHub's support for Web Processing Service (WPS), enhance cartographic visualization capabilities,
and explore distributed architectures to enable million-layer scheduling—reinforcing foundational support for spatial
intelligence infrastructure.

ACKNOWLEDGEMENTS
This study was financially supported by the Science and Technology Program of Fujian Branch, China National Tobacco
Corporation (Grant No. 202425000240030).

REFERENCES
[1] Harrison, Jeff, and Mark Reichardt. "Introduction to OGC web services." An OGC White Paper (2001).
[2] Open Geospatial Consortium, "OpenGIS Web Map Tile Service Implementation Standard 1.0.0," OGC 07-057r7,
2007. [Online]. Available: https://www.ogc.org/standards/wmts/. Accessed: Aug 6, 2025.
[3] Open Geospatial Consortium, "Web Map Server Implementation Specification 1.3.0," OGC 06-042, 2006. [Online].
Available: https://www.ogc.org/standards/wms/. Accessed: Aug 6, 2025.
[4] Open Geospatial Consortium, "Web Feature Service 2.0 Interface Standard 2.0.2," OGC 09-025r2, 2009. [Online].
Available: https://www.ogc.org/standards/wfs/. Accessed: Aug 6, 2025.
[5] Open Geospatial Consortium, "OGC Web Processing Service (WPS) Interface Standard," OGC Standard 14-065r2,
version 2.0.2, 2018. [Online]. Available: https://www.ogc.org/standards/wps. Accessed: Aug. 10, 2025.
[6] Open Geospatial Consortium, "Common Query Language (CQL2) Part 1: Core Specification," OGC Standard 21065r2, version 1.0.0, Jul. 26, 2024. [Online]. Available: http://www.opengis.net/doc/IS/cql2/1.0. Accessed: Aug 1,
2025.
[7] EPSG.io, "Coordinate Systems Worldwide: EPSG Database Search and Conversion," EPSG.io. 2024. [Online].
Available: https://epsg.io/. Accessed: Aug. 3, 2025.
[8] Open Geospatial Consortium, "OGC API - Features: Standard for Web-Based Feature Data Access and
Management," OGC Standard 17-069r5, Feb. 2021. [Online]. Available: https://ogcapi.ogc.org/features/. Accessed:
Aug 3, 2025.
[9] A. Vaswani et al., “Attention is All you Need,” in Advances in Neural Information Processing Systems, Curran
Associates,Inc.,2017.[Online].Available:https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee
91fbd053c1c4a845aa-Abstract.html.
[10] J. Wei et al., “Chain-of-Thought Prompting Elicits Reasoning in Large Language Models”. in Advances in neural
information processing systems 35 (2022): 24824-24837
[11] T. Masterman, S. Besen, M. Sawtell, and A. Chao, "The Landscape of Emerging AI Agent Architectures for
Reasoning, Planning, and Tool Calling: A Survey," arXiv:2404.11584 [cs.AI], Apr. 2024. [Online].
Available: https://arxiv.org/abs/2404.11584.
[12] Han, Yikun, Chunjiang Liu, and Pengfei Wang. "A comprehensive survey on vector database: Storage and retrieval
technique, challenge." arXiv preprint arXiv:2310.11703 (2023).
[13] Anthropic Inc., "Introducing the Model Context Protocol (MCP)," 2024. [Online]. Available:
https://www.anthropic.com/news/model-context-protocol. Accessed: Aug 7, 2025.
[14] Prefect, "FastMCP Documentation: Model Context Protocol Framework," FastMCP, version 2.0 Beta, 2025.
[Online]. Available: https://gofastmcp.com/. Accessed: Jul. 10, 2025.
[15] mcp.so, "MCP Servers: Community Directory for Model Context Protocol Tools and Integrations," mcp.so. 2025.
[Online]. Available: https://mcp.so/. Accessed: Aug. 10, 2025
[16] Ageospatial Sàrl, "Ageospatial - Accessible Location Intelligence," Ageospatial. 2025. [Online].
Available: https://ageospatial.com/. Accessed: Jul. 10, 2025.
[17] SuperMap Software, "Geospatial AI Technology System", SuperMap Official Website. [Online]. Available:
https://www.supermap.com/cn/technology/geoai. Accessed: Aug. 8, 2025.
[18] Esri Inc., "ArcGIS Pro AI Assistants: Technical Documentation (Version 2.3)," Doc. ID: AIA-2025PRO, 2025.
[Online]. Available: https://www.esri.com/en-us/products/arcgis-pro/ai-assistants. Accessed: Aug. 10, 2025.

Proc. of SPIE Vol. 14018 140184B-15
