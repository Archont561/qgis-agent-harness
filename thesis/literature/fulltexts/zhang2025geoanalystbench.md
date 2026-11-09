---
id: literature/fulltexts/zhang2025geoanalystbench
type: fulltext
status: frozen
language: en
key: zhang2025geoanalystbench
title: >-
  GeoAnalystBench : A GeoAI Benchmark for Assessing Large Language Models for Spatial Analysis Workflow and Code Generation
resource: https://doi.org/10.1111/tgis.70135
description: >-
  ABSTRACT Recent advances in large language models (LLMs) have fueled growing interest in automating geospatial analysis and GIS workflows, yet their actual capabilities remain uncertain.
pages: 34
words: 15151
year: 2025
venue: >-
  Transactions in GIS
authors: >-
  Zhang, Qianheng; Gao, Song; Wei, Chen; Zhao, Yibo; Nie, Ying; Chen, Ziru; Chen, Shijie; Su, Yu; Sun, Huan
doi: 10.1111/tgis.70135
oa_status: hybrid
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# GeoAnalystBench : A GeoAI Benchmark for Assessing Large Language Models for Spatial Analysis Workflow and Code Generation

## Page 1

arXiv:2509.05881v1 [cs.SE] 7 Sep 2025

RESEARCH ARTICLE

GeoAnalystBench: A GeoAI benchmark for
assessing large language models for spatial
analysis workflow and code generation
Qianheng Zhang1

|

Zhao1

|

Ying Nie1

Yu Su2

|

Huan Sun2

Song Gao *1
|

1 Geospatial Data Science Lab, ,

Department of Geography, University of
Wisconsin-Madison, Madison, WI, 53706,
United States
2 Department of Computer Science and

Engineering, The Ohio State University,
Columbus, OH, 43210, United States
Correspondence
Song Gao, PhD, Department of Geography,
University of Wisconsin-Madison, Madison,
WI, 53706, United States
Email: song.gao@wisc.edu
Funding information
NSF, Award Number: 2112606

Ziru Chen2

Chen Wei1

|
|

|

Shijie Chen2

Yibo
|

Recent advances in large language models (LLMs) have fueled growing interest in automating geospatial analysis and
GIS workflows, yet their actual capabilities remain uncertain. In this work, we call for rigorous evaluation of LLMs
on well-defined geoprocessing tasks before making claims
about full GIS automation. To this end, we present GeoAnalystBench, a benchmark of 50 Python-based tasks derived
from real-world geospatial problems and carefully validated
by GIS experts. Each task is paired with a minimum deliverable product, and evaluation covers workflow validity,
structural alignment, semantic similarity, and code quality
(CodeBLEU). Using this benchmark, we assess both proprietary and open source models. Results reveal a clear gap:
proprietary models such as ChatGPT-4o-mini achieve high
validity (95%) and stronger code alignment (CodeBLEU 0.39),
while smaller open source models like DeepSeek-R1-7B often generate incomplete or inconsistent workflows (48.5%
validity, 0.272 CodeBLEU). Tasks requiring deeper spatial
reasoning, such as spatial relationship detection or optimal
site selection, remain the most challenging across all mod-

1

## Page 2

2

Zhang et al.

els. These findings demonstrate both the promise and limitations of current LLMs in GIS automation and provide a
reproducible framework to advance GeoAI research with
human-in-the-loop support.
KEYWORDS

GeoAI, language agent, LLM, benchmark, spatial analysis

1

|

INTRODUCTION

Recent advances in geospatial artificial intelligence (GeoAI) have been driven by generative AI and foundation models
such as large language models (LLMs), vision-foundation models, and multimodal foundation models (Jakubik et al.,
2023; Wu et al., 2023; Huang et al., 2024; Mai et al., 2024; Wang et al., 2024). LLMs function as language assistants,
copilots, and agents, enabling various types of users to interact with complex systems through natural language. Numerous studies have examined the abilities of LLMs in planning, reasoning, and solving complex tasks across multiple
science domains as independent agents (Chen et al., 2024; Yue et al., 2024). Within the domain of Geographic Information Systems (GIS), researchers have investigated the ability of LLMs to understand inputs of spatial relationships
between geographic objects and generate various visual representations in formats such as maps, graphs, and WellKnown Text (WKT) outputs (Zhang et al., 2024a; Ji et al., 2025). These studies indicate a continuous improvement in
LLMs’ capabilities, demonstrating that advancing automation of complicated GIS workflows to collect, analyze, and
visualize GIS data is promising (Li and Ning, 2023; Zhang et al., 2024c; Wei et al., 2024; Jiang and Yang, 2024). In
particular, LLMs have been shown to be effective assistants for individuals without prior knowledge of GIS or spatial
contexts, lowering barriers to entry for spatial analysis by transforming traditional GIS workflows (Zhang and Gao,
2024). Although early studies are promising, there has not yet been a systematic test of whether LLMs can reproduce
human expert-designed GIS workflows. Existing studies mostly focus on isolated tasks (e.g., generating a buffer or
drawing a map), but few have examined whether LLMs can sequence multi-step geoprocessing operations, such as
spatial joins, overlays, or raster calculations, in a coherent spatial analysis workflow aligned with expert logic. This
leads to a fundamental question: How do LLMs conceptualize and execute GIS tasks compared to human experts?
This fundamental question is systematically divided into three specific research questions to be answered in Section
5.
•

RQ1: How do proprietary LLMs perform compared to open-source models in geospatial workflow and code

•

RQ2: What roles do domain knowledge (DK) and dataset description (DD) play in improving workflow generation

•

RQ3: How do LLMs handle different aspects of code generation, including syntax, logical structure, and spatial

generation?
accuracy?
data manipulation?
Beyond addressing technical challenges, the integration of LLMs into GIS workflows aims to democratize access
to spatial analysis tools by a broader audience. Historically, GIS has been a domain that requires specialized knowledge,
often creating barriers for people and communities with limited experience. Over the past decades, GIS technologies
and tools have evolved significantly, improving the use of spatial data to inform decision making across various fields

## Page 3

Zhang et al.

3

such as urban planning, environmental conservation, and disaster management (Cervone et al., 2015; Pham et al.,
2011; Andrew et al., 2015). However, these advancements have also introduced complexities, as researchers today
can be confused with various data formats, programming environments, and software platforms (Toms, 2015). Using
LLMs, these barriers can be mitigated, allowing a broader user community to engage with spatial data and derive actionable geospatial insights. More importantly, it has always been the wish for autonomous GIS analysts (GeoMachina)
to become real towards artificial general intelligence (AGI) that can pass the Turing test (Janowicz et al., 2020). Realizing this vision requires rigorous evaluation: Can LLMs reliably replicate the logical sequencing, parameter selection,
and domain-aware reasoning that human experts apply to GIS tasks?
A key challenge in applying LLMs to geospatial workflows lies in their ability to replicate structured, domaininformed reasoning. Can LLMs determine a logical sequence of spatial operations? When addressing geospatial data
analysis tasks, GIS experts typically decompose geoprocessing problems into logically ordered subtasks under a central topic, executing them in a logical sequence often based on domain knowledge and reasoning. For spatial data
scientists, the primary workflow of finding optimal future fire stations includes: loading current fire stations and
neighborhoods’ data, buffering the location of current fire stations based on travel time/distance, and clipping them
out to highlight the neighborhoods without sufficient fire station coverages. This sequential reasoning of workflow
is intuitive to humans because each step builds on the previous one, forming a coherent geoprocessing workflow.
In contrast, it remains unclear whether LLMs naturally follow the same structured reasoning process when solving
spatial analysis problems with GIS tools. If a geoprocessing task requires spatial joins, geometric operations, and attribute queries, how does an LLM decide the sequence of operations? Furthermore, do LLMs understand the implicit
relationships between data inputs and processing steps, such as recognizing that a JSON file stores point data in a
GeoDataFrame format? Structured reasoning with logical sequences can help reduce hallucination in tools and parameter assignments while improving LLMs’ reasoning abilities (Wei et al., 2022). To systematically evaluate this capability,
we introduce the GeoAnalystBench, a benchmark designed to assess how closely LLM-generated workflows align with
GIS expert-designed processes in both structure and logic.
To systematically address these challenges, this study presents a GeoAI benchmark dataset GeoAnalystBench
(https://github.com/GeoDS/GeoAnalystBench) to examine the abilities to solve spatial data science problems of
LLM-powered AI agents compared to human experts. The benchmark dataset includes 50 major geoprocessing tasks
derived from online GIS tutorials and academic publications, which focus on GIS experiments and exploratory spatial
data analysis. Each major task can be divided into around 3 to 10 sub-level tasks. Then, concise human language
prompts are passed to the LLMs for deriving the results. The ability of LLMs to generate geoprocessing workflows
similar to those carefully designed by human experts was evaluated, with differences in workflow step length and
structure being systematically measured. GIS expert annotators then assess the quality of the workflow outputs, while
tools such as CodeBLEU (Ren et al., 2020) were used to evaluate the accuracy and effectiveness of LLM-generated
code. By examining the alignment between human-designed and AI-generated workflows, this research provides a
foundation to uncover the differences in logical structuring and explore whether these differences can be leveraged for
improved geospatial analysis. Our findings will contribute to the design of more effective prompting strategies, future
GIS automation tools, and hybrid GeoAI workflows that integrate foundation models and human thinking processes.
Figure 1 illustrates the overall evaluation framework, including task prompting, code generation, execution, and expert
comparison.
In summary, this study makes the following key contributions:
•

We develop the GeoAnalystBench, a GeoAI benchmark dataset designed to systematically compare GIS workflows
generated by LLMs with human-designed and annotated workflows.

## Page 4

4

Zhang et al.

F I G U R E 1 A conceptual framework for creating geoanalyst benchmark datasets and evaluating the ability of
LLMs to autonomously generate GIS workflows and code for spatial analysis tasks.

•

We analyze the logical structure of GIS tasks by LLMs, identifying key differences in performance across various

•

We evaluate LLM-generated codes using both human annotators and automated metrics (e.g., CodeBLEU) to quan-

•

Our findings contribute to future development of improved prompting strategies, GIS automation tools, and hy-

GIS application domains.
tify the generated workflow accuracy and effectiveness.
brid human-AI workflows.

2

|

RELATED WORKS

The recent surge in LLM research has led to a variety of benchmarks and applications across domains, yet limited
unified evaluation protocol exists for assessing LLM performance in spatially grounded reasoning and geoprocessing.
Within GeoAI, researchers have focused on understanding how LLMs interpret spatial concepts, manage complex
data formats, and produce meaningful spatial outputs. This section reviews two complementary research directions:
(1) the application or development of spatially-aware large language models tailored for GIS tasks and (2) GIS related
benchmarks designed to systematically evaluate LLM performance in geospatial problem solving.

## Page 5

Zhang et al.

2.1

|

5

Integration of Large Language Models with GIS

A key strength of LLMs is their generalizability and adaptability, which allows them to be fine-tuned through prompt
engineering and domain-specific training data. Recent works have taken such advantages to enhance GIS automation
and spatial reasoning capabilities.
LLM-Geo (Li and Ning, 2023) is a pioneering work on autonomous GIS and introduces a structured framework that
decomposes spatial analysis tasks into discrete components: inputs, operations, intermediate data, and final outputs.
These components are organized into a directed graph, enabling LLMs to reason through workflows step-by-step.
This framework examines the chain-of-thought and planning capabilities of LLMs, emphasizing their ability to map
complex geospatial queries into structured and executable operations. LLM-Geo’s focus on workflow automation
demonstrates the potential for LLMs to transition from general-purpose language models to domain-specific problem
solvers with sophisticated planning and reasoning skills.
Further advancing the integration of LLMs in GIS, GeoGPT (Zhang et al., 2024c) represents an early effort to utilize LLMs for solving spatial analysis tasks in GIS. This study introduces a framework for the generation, collection, and
execution of GIS workflows via natural language prompts. This pioneering approach integrates LLMs with GIS tools
to address end-to-end geospatial workflows and problem solving tasks, showcasing the potential of LLMs to serve as
flexible assistants for GIS professionals. In a follow-up work, a fine-tuned GeoTool-GPT was developed using annotated GIS instruction-solution evaluation data and demonstrated its effectiveness in operating GIS tools (Wei et al.,
2024). Building on this foundation, BB-GeoGPT (Zhang et al., 2024b) focuses on fine-tuning smaller LLMs to improve
domain-specific performance. By using a curated dataset of GIS-related academic publications and Wikipedia articles,
BB-GeoGPT enhances the performance in question-answering (QA) tasks across various GIS domains. This approach
highlights how LLMs can be tailored to "understand" GIS as a subject, emphasizing the intersection of natural language and geospatial semantics. Unlike general-purpose models, BB-GeoGPT demonstrates how domain adaptation
can bridge gaps in spatial reasoning and applications. While these systems demonstrate the feasibility of integrating
LLMs with geospatial tools, they typically focus on specific tasks or narrow capabilities, rather than providing a unified evaluation framework that systematically compares LLM performance across diverse GIS workflows and spatial
reasoning steps.
More recently, Xu et al. (2025) introduced a multi-task geospatial benchmark covering twelve spatial reasoning tasks, revealing substantial variability in LLM performance across domains. Akinboyewa et al. (2025) developed
GIS Copilot, an autonomous GIS agent integrated with QGIS that generates and executes spatial analysis workflows,
achieving high success rates in tool selection and output correctness. Krechetova and Kochedykov (2025) proposed
the GeoBenchX, a multistep geospatial task benchmark incorporating tool invocation and hallucination-avoidance
challenges. Complementing these, Ning et al. (2025) designed an autonomous GIS agent framework for geospatial
data retrieval, enabling LLMs to select data sources, generate code, and execute retrieval pipelines. Li et al. (2025) presented a research agenda towards autonomous GIS with LLMs and a conceptual framework that defines autonomous
goals, autonomous levels, core functions, and operational scales of autonomous GIS. Van de Weghe et al. (2025)
discussed opportunities and challenges of integrating GIS and LLMs. Collectively, these works demonstrate rapid
advances in integrating LLMs with GIS and developing targeted benchmarks, while underscoring the need for unified, comprehensive evaluation protocols and social responsibilities. Additionally, Janowicz et al. (2025) provided a
comprehensive review on how will LLMs and geo-foundation models reshape spatial data science and GeoAI.

## Page 6

6

Zhang et al.

|

2.2

Benchmarks for the evaluation of LLMs in GIS

While the above studies focus on the development of GIS-oriented LLMs, another line of research emphasizes systematic evaluation on benchmarks to uncover the pro and cons of current LLMs.
For example, GeoGLUE (Li et al., 2023) introduces a geographic language understanding benchmark, which evaluates LLMs’ abilities in geographic textual similarity searching, geographic element tagging, and geographic entity
alignment, which are essential for understanding natural language and semantic reasoning within geographic contexts. This benchmark highlights the nuances of geographic expressions, including hierarchical naming and colloquial
usage, offering diverse challenges for model evaluation on spatial relationships.
Focusing on multimodal reasoning, GeoQA (Chen et al., 2021) is a benchmark comprising 4,998 geometric problems, annotated with solving programs for transparency and evaluation. GeoQA demonstrates that LLMs achieve
better results when textual and graphical inputs are combined. GeoQA establishes a robust benchmark sets a high
standard for assessing numerical reasoning and multimodal data integration.
Focusing on code generation, Gramacki et al. (2024) addresses the automation of geospatial analysis code generation in Python. This benchmark includes 20 unique tasks and 77 examples that are used to test various levels of
complexity across GIS tools and data formats such as GeoPandas, ESRI Shapefiles, and GeoJSON. It finds that the
performance of the LLMs’ code generation is highly dependent on the difficulty of the task, the layout of the input,
and the usage of the library. However, the model capabilities are constrained by the functions and libraries implemented within the benchmark, necessitating a broader tool integration. At the same time, GEE-OPs (Hou et al., 2024)
proposes the use of Google Earth Engine (GEE) platform on collecting 185,236 pieces of GEE code and using the Abstract Syntax Tree (which represent the structure of a code snippet) to extract the explicit operator relationships. The
dataset noted with high-quality operator instructions improves LLMs’ ability on understanding programming syntax
as well as producing high-accuracy codes specific to GEE.
In sum, although several benchmarks have evaluated LLMs on geospatial tasks, most focus on textual understanding, question answering, or single-step operations. Recently, benchmarks such as GeoBenchX (Krechetova and
Kochedykov, 2025) and GEOBench-VLM (Danish et al., 2024) expand this landscape by tackling multi-step, multimodal, and tool-based reasoning challenges in geospatial tasks. ScienceAgentBench (Chen et al., 2024) offers 102
tasks across four scientific disciplines, including Geographical Information Science, with rigorous execution based
evaluation on self contained Python programs, making it directly relevant as a GIS benchmark. Its task distribution
explicitly includes geospatial analysis and map visualization subtasks, underscoring coverage of practical cartographic
and analytical workflows. However, interpretability remains a challenge, especially when reasoning steps are opaque
or hallucinated (Singh et al., 2024). Our work differs by introducing a multi-step, execution-based benchmark that emphasizes workflow structure, tool chaining, and alignment with human expert logic. GeoAnalystBench thus addresses
a unique evaluation gap at the intersection of code synthesis, spatial reasoning, and process automation.

3

|

GEOANALYST-BENCHMARK

The complexity of real-world geospatial data science tasks often requires benchmark datasets to evaluate model
performance on specific domains. To this end, this research developed 50 Python-based geoprocessing tasks derived
from GIS platforms, software, online tutorials, and academic literature. Each task comprises 3 to 10 subtasks, because
the simplest task still involves data loading, applying at least one spatial analysis tool, and saving the final outputs. The
list of those tasks with their geoprocessing step lengths are included in the Table S-1, Table S-2, and Table S-3.
The decision to focus on Python libraries stems from their suitability for automating GIS tasks. These tasks span

## Page 7

Zhang et al.

7

various domains, including remote sensing, ecology, climate change, social science, and various application areas of
spatial data science. Although the topics extend beyond traditional GIS, all tasks remain grounded in the practicalities
of research experiences. Moreover, the tasks and their associated workflows and codes are designed to respect open
source or copyrights generated by the annotators. By addressing a variety of scenarios, this research aims to evaluate
how well the state-of-the-art LLMs can generate geoprocessing workflows and solutions for geospatial problems
while highlighting the evolving role of these models in automation of spatial data science.

3.1

|

Annotation Process

To construct the benchmark tasks, we curated geospatial problem-solving examples from a combination of publicly
available GIS tutorials (e.g., Esri Learn platform, university lab instructions) prior to year 2025. This approach aims to
collect as many tasks as possible while providing high quality annotations. Each task was manually paraphrased, abstracted, and annotated by GIS experts to ensure distinct phrasing and structural independence from original sources.
As shown in Figure 2, the annotators first carefully executed each task with GIS software such as ArcGIS or QGIS
following the tutorials. Then, they systematically converted long tutorials into short-phrase formats of geoprocessing workflows. After that, these workflows will be translated into operational Python scripts. Finally, the annotators
documented the essential domain knowledge and data description. This multi-step curation process helps reduce circularity risk and enhances the benchmark’s validity for evaluating LLM reasoning. We also verified that the selected
sources exhibit clear authorship and human editing history. A subset of tasks is derived from ESRI’s ModelBuilder examples, which produce deterministic outputs that serve as a basis for comparing LLM-generated code. Tasks include
structured metadata and are designed to simulate authentic spatial analysis workflows without relying on memorized
patterns.

F I G U R E 2 Annotators replicating the task, documenting workflow, programming the code, and consolidating
into instructions, dataset descriptions, and domain knowledge.
To guide LLMs, each task was paired with a concise natural language instruction enriched with GIS domain-specific
knowledge and detailed dataset descriptions. The instructions, on average around 100 words, outlined the desired
methods or tools for spatial data processing and analysis. GIS domain knowledge clarifies specialized terms, algorithms,
or classification methodologies, such as buffering, spatial statistics, or estimating property loss due to flood damage
(case number 3, 8, 7 in table S-1). This approach, similar to aspects of Retrieval-Augmented Generation (RAG) (Lewis
et al., 2020), was simplified to improve its utility in evaluating LLMs’ performance in different stages.

## Page 8

8

Zhang et al.

Dataset descriptions in Table 1 provide critical context, detailing file formats (e.g., CSV, GeoJSON, GeoTIFF), column definitions, file sizes, and key attributes. For data files with multiple key feature columns, descriptions of the
columns are specified because there are column names that are abbreviations or code names for specific features.
This information addresses the complexity of the datasets and aimed to test whether equipping LLMs with detailed
data descriptions could improve their ability to generate accurate workflows and solutions.
Three annotators read through the GIS online materials, replicated the processes outlined in the tutorials, and ensured that each task was suitable for automation using Python code. The instructions specify input files, intermediate
tools, and final output formats, enabling evaluation of the LLMs’ ability to connect inputs to outputs with the correct
logical sequence and number of intermediate steps. This design facilitated the assessment of LLMs’ capabilities in
accurately understanding and replicating complex geoprocessing workflows.
The concise summary of knowledge in the GeoAnalystBench is a modified version of ScienceAgentBench (Chen
et al., 2024), which aims to test LLMs’ abilities to solve data-driven scientific tasks in multiple science domains. This
study refines the dataset description section to match the condition of spatial data layers. The approach in ScienceAgentBench was trying to provide supplementary information to the LLM agents with first three rows of data,
which doesn’t fit to the large sized and abstract geospatial data. Because the geospatial data are relatively challenging to be informative in command-line style previews. Thus, this study only includes the data types, sizes, and key
columns for the essential files. This approach aims to simulate the stage of exploratory data analysis stage for spatial
analysis tasks.
TA B L E 1

The Key columns and descriptions for GeoAnalystBench

Key Columns

Descriptions

id

Unique identifier for each task

Open or Closed Source

Use open source or closed source library

Task

Brief description of the task

Instruction

Natural language instruction for completing the task

Domain Knowledge

Domain specific knowledge related to task

Dataset Description

Data name, format, descriptions, and key columns

Human Designed Workflow

Numbered list of human designed workflow

Task Length

The length of the human designed workflow

Code

Human designed code for the task and dataset

3.2

|

Spatial Analysis Categorization

The GeoAnalystBench dataset encompasses a wide range of spatial analysis topics while utilizing diverse Python toolkits. All tasks in this study are categorized as applied sciences of GIS and follow slightly modified ESRI’s category
definitions in the taxonomy of spatial analysis (ESRI, 2013):

1.

Understanding where: Tasks focused on identifying, classifying, and characterizing geographic locations and their
attributes.

## Page 9

Zhang et al.

2.

9

Measuring size, shape, and distribution: Tasks that measure and evaluate the size, shape, orientation, and spatial
distribution of geographic phenomena.

3.

Determining how places are related: Tasks that examine interactions, dependencies, and spatial correlations
between different locations or geographic features.

4.

Finding the best locations and paths: Tasks related to spatial decision making, including site selection, route
optimization, and spatial accessibility analysis.

5.

Detecting and quantifying patterns: Tasks focused on detecting spatial clusters, trends, anomalies, and spatial
heterogeneity within datasets.

6.

Spatial interpolation and predictive modeling: Tasks that estimate unknown values at unsampled locations using
spatial data, as well as forecasting spatiotemporal trends based on historical patterns.
This categorization organizes spatial analysis/geoprocessing tasks based on their methodological and domain-

specific approaches, ensuring both functional coherence and technical consistency. Given that all tasks in this benchmark are designed to simulate real-world scenarios with well-defined geospatial workflows within ten steps, it is
crucial to adopt the applied science definitions to evaluate LLM performance from multiple perspectives.
Understanding where involves identifying the relative locations of geographic objects within a given space, facilitating spatial awareness and navigation. Measuring size, shape, and distribution extends beyond simple measurements to incorporate both quantitative properties and abstract spatial patterns. Determining how places are related
focuses on identifying shared attributes and interconnections between multiple locations within the same space. Detecting and quantifying patterns involves analyzing recurring spatial structures, enabling the classification and grouping of related geographic entities. Finding the best locations and paths pertains to spatial optimization tasks, including
site selection, route planning, and network analysis to determine optimal configurations based on predefined criteria.
Spatial interpolation and predictive modeling involve estimating unknown values in spatial datasets or forecasting
future trends based on spatial dependencies and historical data patterns.
This categorization simplifies the identification of tasks that share methodological similarities, such as spatial analysis, machine learning, or data visualization. Additionally, tasks may belong to at most three different categories to
reflect their complexity and enhance diversity. By employing this structured approach, this study ensures a comprehensive coverage of spatial analysis/geoprocessing methodologies while maximizing the applicability of the benchmark in a wide range of real-world scenarios. At the same time, it’s critical for unveiling the performance of LLMs on
different aspects of spatial analysis. The topic distribution of the spatial analysis/geoprocessing tasks included in the
GeoAnalystBench is shown in Figure 3.

4

|

EVALUATION METRICS

Evaluating this benchmark dataset across various LLMs enables a comprehensive understanding of the key capabilities of LLMs as autonomous agents in solving spatial analysis/geoprocessing tasks: workflow generation and code
generation. Since the task instructions are provided in natural language without explicitly specifying the GIS tools or
programming languages, this benchmark dataset allows evaluation under different experimental settings. In our study,
we specify Python as the primary programming language for execution.
For each task, we generate four different prompts: task alone, task with domain knowledge, task with dataset descriptions, and task with extra information. The responses are generated using an online API from three proprietary LLMs
(i.e., ChatGPT-4o mini, Claude 3.5 Sonnet, and Gemini 1.5) and three open-source ones (i.e., Llama 3.1, CodeLlama,

## Page 10

10

Zhang et al.

F I G U R E 3 The distribution of task categories included in the GeoAnalystBench: U: Understanding where; M:
Measuring size, shape, and distribution; DR: Determining how places are related; F: Finding the best locations and
paths; DP: Detecting and quantifying patterns; S: Spatial interpolation and predictive modeling.

and DeepSeek-R1). Three outputs per prompt are collected for evaluation.
The evaluation framework was implemented using both cloud-based APIs and local inference environments. Proprietary LLMs such as ChatGPT 4o mini(2024-07-18), Claude 3.5 Sonnet(2024-6-20), and Gemini 1.5 Flash(2024-514) were accessed through their official APIs with a temperature setting of 0.7 to balance consistency and response
diversity. Open-source models including Llama 3.1 8B(2024-7-23), DeepSeek R1 7B(2025-1-20), and CodeLlama
7B(2023-7-18) were run locally using the vLLM inference engine on a workstation with an NVIDIA RTX 2080 Super
GPU and an Intel Core i7 processor. All models generated geoprocessing workflows and ArcPy code in response to
structured prompts. These outputs were assessed using evaluation metrics such as task validity, mean absolute deviation in workflow length, and CodeBLEU scores. A separate system with an NVIDIA Tesla P40 GPU was used only
for visualizing case study examples and validating reference code. This setup ensures a controlled and reproducible
environment for performance comparison across model types.
In designing the benchmark, certain task instructions were intentionally left with ambiguous parameters (such
as buffer size or clustering thresholds) to evaluate the LLMs’ ability to make reasonable assumptions and defaults
in the absence of explicit guidance. This decision reflects realistic user behavior, where non-expert users may issue
incomplete or underspecified queries. Allowing models to resolve such ambiguities provides insight into their domain
intuition, default-setting behavior, and overall robustness. For example, if a prompt asks to "buffer schools in an urban
area" without specifying the distance, the model’s choice reveals how well it understands standard practices in urban
GIS applications. These domain-informed assumptions and decisions are then evaluated based on how closely they
align with expert-designed workflows or plausible GIS conventions. While we do not explicitly label or isolate these
tasks in the current study, this dimension of prompt ambiguity offers a promising direction for future research on LLM
reasoning under uncertainty.

## Page 11

Zhang et al.

4.1

|

11

Workflow Evaluation

The workflow evaluation assesses how well the generated geoprocessing workflows align with human-designed workflows, reflecting the ability of LLMs to structure geospatial problem-solving processes. Three key dimensions are
considered:
•

Validity – The percentage of valid responses relative to the total number of LLM responses. A response is considered valid if it contains an extractable workflow list. Higher valid rates indicate better abilities to follow instructions and maintain coherence. In our implementation, validity is assessed through a combination of automated
parsing and manual checking to ensure that the generated workflow constitutes a coherent and complete sequence of geoprocessing steps that satisfy the task instruction.

•

Complexity – Measured by the length of the workflow, indicating how LLMs structure problem-solving steps.
Most tasks are solvable within 6 steps, making workflow length a critical factor in evaluating the efficiency of
LLM design. We use Mean Absolute Deviation (MAD) to quantify how much the LLM-generated workflow length
deviates from the human-designed reference. It is calculated as:

N

MAD =

1 Õ i
L LLM − L ihuman
N
i =1

where L iLLM and L ihuman represent the number of steps in the i -th workflow generated by the LLM and the expert,
respectively. A smaller MAD suggests a closer match to expert logic, while a larger value may indicate that the

LLM either overcomplicates or oversimplifies the task. In this study, MAD serves as an interpretable and taskagnostic measure of structural alignment between human and machine reasoning.
•

Text Similarity Score – Assessed through text similarity scores using pre-trained sentence transformers. The allMiniLM-L6-v2 model, a fine-tuned version of MiniLM (Wang et al., 2020), encodes the workflows in semantic
embeddings and we use the embeddings to calculate the cosine similarity. The cosine similarity score results
within 1 and -1, when a higher value indicates a higher similarity. This approach evaluates how closely machinegenerated workflows align with human-created workflows in terms of semantic similarity. A high and positive
similarity score suggests that the LLM’s decisions successfully align with expert reasoning and step dependencies.
By integrating these three dimensions, the evaluation framework aims to assess (1) how valid the LLM-generated

workflows are, (2) whether LLMs can replicate GIS experts’ decision making in structuring spatial analysis/geoprocessing
tools as solutions, and (3) maintaining workflow efficiency. The following prompt template limits LLMs to output codes
and tasks that are easy to visualize and process.
#Workflow Generation Prompt Templates
[Task Instructions]
[key Notes]
1.Use **automatic reasoning** and clearly explain each step.
2.Using **NetworkX** package for workflow graph visualization.
3.Using **Graphviz** ‘dot’ for graph visualization layout.
4.Multiple subtasks can be proceeded simultaneously because

## Page 12

12

Zhang et al.

all of their outputs will be inputs for the next subtask.
5.Limiting your output to code, no extra information.
6.Only codes for workflow generation, no implementation.

4.2

|

Code Evaluation

In addition, we also evaluate LLMs’ capability in code generation for spatial analysis tasks. We employ the CodeBLEU (Ren et al., 2020), an automatic code evaluation metric based on both bilingual evaluation understudy (BLEU)
and abstract syntax trees (AST) in programming. The code evaluation includes the following aspects:
•

N-gram match scores - Comparing the occurrences of term pairs in the generated and reference code.

•

Weighted N-gram match scores – Assigning different weights to N-gram matches according to importance.

•

Syntax AST match scores – Assessing syntactic correctness in the programming code.

•

Semantic Data-flow match scores – Evaluating whether the generated code manipulates the data in ways that
are logically similar to human-written code.
These scores ensure that the evaluation captures both text similarity and syntactic correctness in Python pro-

gramming languages. Considering the focus on data-driven spatial analysis workflow, we decide to use the final score
with a weighted combination as shown in the following equation:
Score = 0.2 × N-gram + 0.2 × Weighted N-gram + 0.3 × Syntax AST Match + 0.3 × Semantic Data-flow Match (1)
It is important to note that human-designed code, especially in the post-LLM era, may have been influenced by
AI-generated solutions from online tutorials. To account for this, we compare AI-generated code with human-designed
code, including code examples from both pre-LLM and post-LLM periods. At the same time, the machine-generated
outputs generated from ArcGIS Pro are being compared for machine versus AI purposes.
The tasks in the benchmark are collected not only from online resources, but also are crafted and verified by
human experts. At the same time, ArcPy-oriented tasks employ a technique called ModelBuilder that chains multiple
geoprocessing tools in ArcGIS for solving spatial analysis tasks (in Figure 4). ModelBuilder has a graphic user interface
that allows users to visually connect geoprocessing tools/functions with specified data inputs and outputs. More importantly, the processing model can be output as python codes. These machine generated codes are more consistent
than human-crafted codes, given that the ModelBuilder always follows the same syntax on code format, which can
serve as a solid format of ground-truth code during the evaluation.
The following prompt template limits LLMs to output codes that are easy to analyze.
#Code Generation Prompt Templates
[Task Instructions]
[key Notes]
1.Use **automatic reasoning** and clearly explain each subtask before performing it.
2.Using latest python packages for code generation.
3.Put all code under main function, no helper functions.
4.Limit your output to code, no extra information.
5.Use latest open source **Arcpy** packages only.

## Page 13

Zhang et al.

13

FIGURE 4
Codes

5

|

ModelBuilder allows users to add and connect data input, geoprocessing tools, and output as ArcPy

RESULTS

This section presents how the GeoAnalystBench is used to evaluate the performance of spatial analysis/geoprocessing
workflow and code generation across various Large Language Models (LLMs) and LLMs-powered chatbots. These
LLMs are categorized into proprietary and open-source groups based on their accessibility and development frameworks. The proprietary and closed-source models include ChatGPT-4o mini (20240718), Claude-3.5-Sonnet (20241022),
and Gemini-1.5-Flash (20240924). These proprietary models are designed for general-purpose language understanding and reasoning. They are optimized for versatility, making them suitable for a wide range of tasks, including natural
language processing and code generation. Among them, the Claude 3.5 Sonnet has demonstrated strong performance
in zero-shot code generation tasks, as seen in prior benchmarks (Anthropic, 2024). At the same time, open-source
pretrained language models include DeepSeek-R1-7B and Llama-3.1-8B, which are among the most advanced publicly available LLMs. Llama 3.1-8B supports variety of natural language processing tasks, including reasoning and
code generation (Grattafiori et al., 2024). At the same time, DeepSeek-R1-7B is a knowledge distilled version of the
larger DeepSeek-R1-671B model, which is created based on the Qwen-2.5 series models (Yang et al., 2024) and finetuned by using 800k reasoning samples curated with the DeepSeek-R1-671B model. The DeepSeek-R1-7B is small
model but still with powerful reasoning abilities (DeepSeek-AI et al., 2025). These models allow for modification and
fine-tuning, enabling customization for geospatial applications. Additionally, we include the CodeLlama-7B, another
open-source model specifically fine-tuned for code generation on Llama-2 (?). In addition, all models are evaluated
with a temperature setting of 0.7 that keeps balance between creativity and consistency in their outputs.

5.1

|

Workflow Generation

To answer the research question RQ1 (see Introduction section), Table 2 demonstrates an evaluation of geospatial
workflow generation in the GeoAnalystBench across different LLMs, and it reveals the current gap between proprietary
and open-source LLMs. We found that ChatGPT-4o-mini, Claude-3.5-Sonnet, and Gemini 1.5 Flash, consistently
outperform the open-source LLMs in their valid rates (VR), mean absolute difference (MAD), and text similarity (TS) in
generating geospatial workflows. In particular, Gemini-1.5-Flash achieves the highest valid rate (96%) and TS score,
while all three models have over 93% valid rates and 0.54 TS score. At the same time, ChatGPT-4o-mini demonstrates

## Page 14

14

Zhang et al.

TA B L E 2 Performance evaluation of geospatial workflows generated by LLMs regarding their Valid Rates and
Absolute Mean Difference for WK (Without Knowledge), DK (Domain Knowledge), DD (Dataset Description)
Models

VR

TS

WK

DK

DD

With Both

Rates

Scores

MAD

Std

MAD

Std

MAD

Std

MAD

Std

95.0

0.55

1.81

1.49

1.79

1.10

1.38

1.03

1.49

1.22

Proprietary
ChatGPT-4o-mini
Claude-3.5-Sonnet

93.5

0.54

2.09

1.50

1.90

1.53

1.82

1.46

1.76

1.42

Gemini-1.5-Flash

96.0

0.56

2.30

1.76

1.89

1.58

1.70

1.47

1.33

0.97

DeepSeek-R1-7B

48.5

0.23

3.26

2.05

3.96

2.24

4.41

2.06

4.61

2.20

Llama-3.1-8B

95.3

0.39

2.0

1.64

2.01

1.51

2.03

1.41

1.81

1.32

CodeLlama-7B

32.7

0.08

4.88

2.09

4.72

2.08

4.75

2.11

4.98

2.09

Open Source

the lowest MAD across multiple knowledge settings, indicating a balance between accuracy and consistency. These
results may indicate that commercially pretrained LLMs are advantaged by large-scale and high-quality training data,
state-of-the-art fine-tuning techniques, and parameter optimization and thus can be extremely effective for geospatial
reasoning and workflow generation. Also, the lower standard deviations of these models show that they give more
consistent outputs with less variation, an important quality for GIS use cases necessitating the reproducible outputs.
In contrast, small-sized open-source LLMs have a wide variation in performance, with Llama-3.1-8B being the only
viable option compared to proprietary models. At a valid rate of 95.3% and similar MAD values, Llama-3.1 indicates
that open source LLMs are viable for geospatial workflow automation if additional refinements and domain-specific
training strategies are implemented. However, models like DeepSeek-R1-7B and CodeLlama-7B show significant
limitations on workflow generation, with valid rates as low as 32.7% and high MAD values over 4.5, suggesting that
their current architectures are less suitable for sophisticated geospatial reasoning tasks.
A finer-grained analysis of DeepSeek-R1-7B indicates that its training via knowledge distillation is one of the main
reasons for its poorer performance. Model distillation, which transfers knowledge from a larger teacher model to a
smaller student model, is generally known to improve computational efficiency at the cost of decreased reasoning
depth and generalization capacity (Hsieh et al., 2023). In contrast to fully trained end-to-end models with long multistep reasoning trajectories, distilled models may approximate responses based on statistical correlations instead of
strong, context-dependent logical computation. This is especially troublesome in geospatial analysis, where the tasks
require hierarchical decision making, spatial-contextual sensitivity, and exact logical ordering. As a result, DeepSeekR1-7B’s poorer generalization capacity probably accounts for its lower valid rate (48.5%) and larger MAD values for
all experimental settings because it is not able to create consistent geospatial workflows that satisfy domain-specific
logic. The full size of DeepSeek-R1 with 671 billion parameters is expected to have a better performance but would
require resource-intensive computing hardware.
Furthermore, regarding the RQ2, the addition of domain knowledge (DK) and dataset descriptions (DD) greatly
enhances accuracy across all proprietary LLMs, highlighting the value of structured contextual information for spatial
analysis and GeoAI applications. The results imply that domain knowledge related to the task and dataset is beneficial
to reduce the hallucination of models at all levels. Future work should prioritize further development of open-source
models through targeted GIS corpora pretraining, optimization of inference strategies, and evaluation of computational efficiency to improve their suitability for practical spatial analysis scenarios.

## Page 15

Zhang et al.

5.2

|

15

Code Generation

To answer RQ3, we compared the CodeBLEU scores among varying LLMs to demonstrate an evident performance
difference between open source and proprietary models in the generation of Python code for solving geospatial tasks
in the GeoAnalystBench. As shown in Table 3, ChatGPT, Claude, and Gemini consistently outperform open source
counterparts such as Llama, CodeLlama, and DeepSeek, with ChatGPT-4o-mini leading with the best average score
(0.390), which shows to be highly stable under varying conditions. Claude-3.5-Sonnet (0.370) and Gemini-1.5-Flash
(0.358) demonstrate a moderate performance, especially when given domain knowledge and dataset descriptions,
which signals their strengths in using extra context well for structured code generation. DeepSeek-R1-7B (0.272)
performs the worst among all the models. This suggests potential weaknesses of the knowledge distilled LLMs in
context retention and multi-step reasoning, which are critical for geospatial workflow and code generation.
Further examination of the impact of domain knowledge and dataset descriptions reveals that most models improve when additional contextual information is provided, but the extent of improvement varies. Claude shows the
highest adaptability, reaching a CodeBLEU score of 0.406 in the domain and dataset condition, while GPT remains
consistently high performing across all categories. open source models also exhibit greater variability, with Llama and
CodeLlama exhibiting moderate improvement, and DeepSeek exhibiting reduced performance. This variation indicates that proprietary models have been optimized based on more systematic programming data to better generalize.
Given more geospatial context, they can perform better.
TA B L E 3

Code evaluation results
Models

CodeBLEU

N-gram

Weighted N-gram

AST Syntax

Data-flow

ChatGPT-4o-mini

0.390

0.077

0.107

0.563

0.282

Claude-3.5-Sonnet

0.370

0.070

0.089

0.532

0.249

Gemini-1.5-Flash

0.358

0.071

0.096

0.544

0.299

Proprietary

Open Source
DeepSeek-R1-7B

0.272

0.032

0.044

0.405

0.265

Llama-3.1-8B

0.340

0.040

0.054

0.471

0.252

CodeLlama-7B

0.319

0.034

0.053

0.487

0.291

In addition, the CodeBLEU component scores show that although LLMs produce syntactically correct code (average syntax score: 0.501), they have difficulties with lexical similarity (average n-gram: 0.0539, average weighted
n-gram: 0.074) and logical correctness (average dataflow score: 0.274). The low n-gram scores imply that LLMs
generate varied implementations instead of identical replicas of reference solutions, which can cause inconsistencies in standard geospatial workflows. However, the relatively high syntax score implies that most outputs are structurally correct, even if functionally imperfect. The moderate dataflow score further suggests that logical dependencies
between variables and function calls are only partially preserved, highlighting the challenges in complex multi-step
geospatial processing and reasoning. Improving geospatial fine-tuning and enforcing stricter logical structure could
enhance both lexical accuracy and execution reliability in generated code for spatial analysis tasks. Execution time
can vary substantially across hardware and software environments, making it a less reliable metric for cross model
comparison, especially in cases where many LLM generated workflows fail to run due to syntax or semantic errors.
Instead, following insights from agent-based AI research (Wei et al., 2022), we emphasize reasoning quality and the

## Page 16

16

Zhang et al.

logical sequencing of operations. Since execution efficiency has already been examined in ScienceAgentBench (Chen
et al., 2024), we focus here on spatial reasoning and GIS tool usage.

5.3

|

Performance across Spatial Analysis Categories

The performances of LLMs across different categories of spatial analysis tasks reveals a consistent gap between proprietary and open source models. As shown in Figure 5, ChatGPT, Gemini, and Claude demonstrate superior accuracy and
lower MAD values across all the categories. Open source models, particularly DeepSeek-R1-7B and CodeLlama, struggle significantly with tasks requiring advanced spatial reasoning, such as determining spatial relationships (DR), finding
optimal locations and paths (F), and predictive modeling (S). Llama-3.1-8B performs better than other open source alternatives but still lags behind proprietary models, particularly in spatial pattern detection and decision-making tasks.
However, Llama-3.1-8B even outperforms Gemini and Claude in measuring size, shape, and distribution (M), indicating
its competence in spatial measurement and geometric reasoning.

FIGURE 5

The mean absolute differences (MAD) across spatial analysis categories

Both proprietary and open source LLMs perform worst in tasks of finding the best locations and paths (F) and
determining how places are related (DR), indicating that these tasks involve more spatial reasoning and multi-step
decision-making that the current LLMs are not able to perform well. The complexity of these tasks tends to include optimization, spatial network analysis, and hierarchical decision trees that may not be well captured in general-purpose
LLM training data. LLMs do reasonably well at detecting and quantifying spatial patterns (DP) and measuring size,
shape, and distribution (M) because these tasks depend on statistical pattern recognition and geometric reasoning.
However, detecting spatial patterns (DP) and spatial interpolation (S) outcomes are highly disparate between different
models, implying that certain proprietary LLMs may have been specifically optimized for pattern recognition tasks, but
open source models like DeepSeek-R1-7B and CodeLlama are poor at predictive spatial modeling. The great disparity
in spatial interpolation and predictive modeling indicates that these spatial analysis tasks need GIS domain-specific

## Page 17

Zhang et al.

17

knowledge, structured training on good quality of datasets. The performance divergence supports the necessity of
task-specific fine-tuning of LLMs and better spatially-aware embeddings or human-AI collaborative strategies to improve the performance in GIS-oriented spatial reasoning and location-based decision-making.

5.4

|

Open versus Closed Source

The above analyses reveal that ChatGPT, Claude, and Gemini consistently outperform other models across all evaluation criteria, making them strong candidates for GeoAI applications when integrating with LLMs. Open source
models, in general, exhibit diverse performance across different spatial analysis tasks. In contrast, ArcPy-based outcomes demonstrate a better performance in domain knowledge and dataset evaluations, suggesting they are optimized for specific GIS workflows within controlled environments. Although Llama and DeepSeek lag behind overall
performance, they still maintain respectable scores, indicating the potential for future improvement. The results suggest that ArcPy may be more suitable for specialized GIS tasks than open source packages. In summary, ChatGPT,
Gemini, and Claude are the most balanced choices, presenting a trade-off between general AI and geospatial capabilities, which makes them promising tools that can significantly aid for GIS automation and sophisticated spatial analysis
workflows.

FIGURE 6

ArcPy versus open-sourced Packages on CodeBLEU Scores

One possible reason behind the identified trend could be that the greater stability of ArcPy and its well-organized
function references online might account for its better performance in the GIS domain-specific tasks. Since ArcPy
is tightly integrated with the ArcGIS ecosystem, its standardized functions ensure consistent results across different processing workflows. Although ArcPy contains numerous tools, it has been well documented and are openly
available online for user learning and pretraining of LLMs. This study found that ArcPy codes generated by ArcGIS
ModelBuilders are similar to LLM generated code with relatively more stable structures and similar mindsets. In contrast, open source models rely on a variety of geospatial libraries such as GeoPandas, Shapely, and Rasterio, each
with different syntax, functionalities, and update cycles. This diversity, while beneficial for flexibility and adaptabil-

## Page 18

18

Zhang et al.

ity, may introduce inconsistencies in AI-generated workflows, potentially leading to minor variations in performance.
Consequently, ArcPy’s consistency probably makes it more efficient in advanced GIS operations, while open source
packages, although having good overall performance, can be inconsistent in their performance due to the dispersed
state of existing geospatial libraries.

6

|

CASE STUDIES

In the following, we present two case studies included in the GeoAnalystBench to demonstrate the capabilities of LLMs
in geospatial workflow and code generation.

6.1 | Case Study 1: Identification of Home Range and Spatial Clusters from Animal
Movements
6.1.1

|

Background

Understanding elk movement patterns is critical for wildlife conservation and management in the field of animal ecology. The task needs to identify elk home ranges in Southwestern Alberta, 2009 using GPS-tracking locations. In doing
so, researchers are able to analyze their space use and movement clusters for elk populations. Understanding the
home range of the elk population is essential for ensuring sustainability and stability of the wildlife. This case study is
based on the task 43 in Table S-3, which is created based on ESRI’s tutorial on modeling animal home range 1 .
This case study takes GPS-tracked locations and applies three geoprocessing operations including: minimum
bounding geometry, kernel density estimation, and density-based clustering to identify the home range, spatial concentration, and movement clusters of elk population groups, respectively. The final output is a map to overlay the
three types of spatial analysis results. As a result, the image on the right in Figure 7 shows that the elk population is
highly centric to the mountains and forest areas of the Piikani Reserve, while some separated elk groups extend their
home range to places with human activities on the east side.

6.1.2

|

Comparison of Human and LLM Approaches

To streamline the comparison, we present the expert-designed and LLM-generated workflows in a unified Table 4.
Both approaches aim to analyze elk movement and home range, but differ in step granularity, tool usage, and output
handling. While both approaches utilize core geospatial methods—minimum bounding geometry, kernel density, and
clustering—the LLM-generated workflow (see Appendix for detailed prompt design) includes additional preprocessing
and visualization steps, emphasizing completeness and documentation over efficiency. In contrast, the human expert
relies on ModelBuilder’s implicit visualization and streamlines the process with fewer, more targeted steps.
The workflow approaches in sections 6.1.2 and 6.1.3 are quite similar in methodology but with little difference in
mindset. When the human approach is a concise GIS workflow, the LLM approach follows a more detailed structured
pipeline. For example, it separates the loading and plotting process. while suggesting an analysis and storage process
for better data organization. In this case, such approaches can be beneficial for GIS automation. This example also
demonstrates the reason why we are considering both task lengths and text similarities: task length serves as a metric
for how differently humans and LLMs reason and process in problem-solving workflows, while text similarity helps
1 https://learn.arcgis.com/en/projects/model-animal-home-range/

## Page 19

Zhang et al.

19

F I G U R E 7 The geoprocessing workflow in ModelBuilder generates the ground truth result on the top right
corner. The Gpt4o-mini generated code resulted in the right-bottom corner.

TA B L E 4

Step-by-step Comparison of Human Expert vs. LLM Approach

Human Expert (ModelBuilder) Approach

LLM (ChatGPT-4o-mini) Approach

Load dataset

Load GPS Data

Minimum Bounding Geometry (Convex Hull)

Preprocess Data (Clean & Filter)

Kernel Density Estimation

Plot GPS Tracks

DBSCAN Clustering

Estimate Home Range (Convex Hull)

–

Compute Kernel Density Estimation

–

Apply DBSCAN Clustering

ModelBuilder auto-visualization

Analyze Home Range & Habitat Preferences

–

Store Outputs in Geodatabase

## Page 20

20

Zhang et al.

quantify the degree of alignment between their code outputs.
Evaluating the quality of LLM-generated workflows and codes remains a challenge. Although these models successfully outline the necessary steps for exploratory data analysis, their output often lacks optimization and highquality refinement. As shown in Figure 7, the result based on LLM-generated codes follows correctly the given instructions, successfully visualizing both the convex hull and the spatial clustering. However, the kernel density estimation
(KDE) step employs a cell size twice of the optimized value in the LLM generated code, resulting in a low-resolution
output. This discrepancy highlights the limitations of the LLMs in specific parameter selection, which can significantly
affect the precision of spatial analyses.
The results also highlight a critical challenge: while user-defined parameter optimization is essential for refining
spatial analysis outputs, the default settings used by LLMs often introduce randomness, which can be confusing for
users unfamiliar with spatial analysis techniques. For instance, varying default clustering parameters (minimum points
and search distance) in DBSCAN can lead to different interpretations of animal movement patterns. Non-expert GIS
users may struggle to interpret these outputs without prior knowledge, making it difficult to refine or adjust the analysis effectively. This underscores the need for enhanced tuning mechanisms or built-in guidance within LLM-generated
workflows to improve usability and interpretation. One potential solution is incorporating interactive parameter adjustments or AI-assisted explanations to help non-experts understand parameter choices and their implications in
spatial analysis.

|

6.2
6.2.1

Case Study 2: Spatial Hotspot Analysis of Car Accidents
|

Background

The second case study is about spatial hotspot analysis of car accidents. The Brevard County in Florida has one of the
deadliest interstate highways in the United States. This case study aims to identify the spatially distributed hot spots
along the road network. The dataset includes road network, crash locations from 2010 to 2015, and a network spatial
weighting matrix. Understanding the hot spots for car accidents is essential for the local transportation department
to make policies and quick responses for future accidents. This case study is based on the task 46 in table S-3 on
ESRI’s spatial analysis tutorial on determining the most dangerous roads for drivers 2 .
This task selects crash points to snap them onto roads, calculates the crash rates for each road, and creates a hot
spot map using the spatial statistical analysis (Getis-Ord Gi*). In Figure 8, the hot spots show the car accidents tend
to occur on major highways, bridges, and intersections, where traffic converges. In contrast, areas with intricate road
networks and complex urban layouts might be considered cold spots in Brevard County.

6.2.2

|

Comparison of Human and LLM Approaches

We summarize both the human-designed and LLM-generated workflows for crash hot spot detection in Table 5. While
the GIS expert relies on ArcGIS-specific tools that support reproducibility and precise execution, the LLM uses more
generalized descriptions to represent each step.
Although both workflows follow similar core logic(filtering crashes, associating them with roads, and performing hot
spot analysis), the human-designed version offers more operational granularity and tool specificity, making it immediately executable in ArcPy. The LLM-generated steps (see Appendix for detailed prompt design) abstract away from
tool names, aiming for broader adaptability at the cost of precision.
2 https://learn.arcgis.com/en/projects/determine-the-most-dangerous-roads-for-drivers/

## Page 21

Zhang et al.

21

F I G U R E 8 The left side persents the complicated workflow in the ArcGIS Pro Modelbuilder. Top right corner
presents two data inputs. The first image on the bottom right corner is the human designed workflow’s data. The
second image is the spatial hotspot analysis result from the ChatGPT-4o-mini generated codes

6.2.3

|

Result Comparision

The second case study presents a more complex workflow compared to the first one, incorporating more GIS terminologies to describe the details tools/functions used. This complexity arises from the emphasis of the human
editor on a transparent and tool-based workflow using ModelBuilder. In contrast, the LLM-generated approach in
this case study is more abstract, focusing on generalizing the workflow rather than detailing individual tool applications. However, the human-designed workflow in the first case study tends to be more abstract and concise than its
LLM-generated ones. This suggests that while human expertise adapts to different levels of details depending on the
context, LLMs may follow a standardized approach.
Interestingly, as shown in Figure 8, the outcome from LLM-generated code in the second case study is significantly
different from the GIS expert proposed approach while both workflows are quite similar. The impact of these differences is evident in the geovisual outputs. The human-designed workflow in Figure 8 produces a road-based crash
rate analysis, emphasizing the spatial patterns of car crashes along the road segments. This approach aligns with the
transportation safety studies that focus on high-risk roadways. On the other hand, the LLM-generated Python script
performs a point-based hotspot analysis, categorizing crash locations into statistically significant spatial hot and cold
spots. This geovisualization provides a broader spatial context, highlighting crash-prone regions rather than specific
road segments. The different results suggest that human experts prioritize structured spatial relationships between
geographic features (e.g., crashes and roads), while LLMs generalize spatial patterns through statistical clustering. Both
approaches follow the same instruction but diverge in focus due to differences in human understanding and LLMs’
domain knowledge, particularly in data analysis strategies and the interpretation of spatial relationships for analytical

## Page 22

22

Zhang et al.

TA B L E 5

Comparison of Human Expert vs. LLM Workflow for Crash Hot Spot Detection

Human Expert (ModelBuilder) Approach

LLM (ChatGPT-4o-mini) Approach

Load dataset

Select peak-time crashes

Define crash hot spots based on time

Create copy of selected crashes

Copy Feature to new layer

Snap crashes to road network

Snap crash points to roads

Spatial join crashes with roads

Spatial Join with road layer

Calculate crash rate per road segment

Add Fields for crash count

Perform hot spot analysis

Calculate Fields for crash rate

Generate crash hot spot map

Hot Spot Analysis (Getis-Ord Gi*)

–

purposes.

7

|

DISCUSSION

The comparative results from GeoAnalystBench highlight several consistent patterns in how LLMs approach spatial
analysis tasks. Proprietary models such as ChatGPT-4o-mini, Claude-3.5-Sonnet, and Gemini-1.5-Flash outperform
open-source counterparts in valid rate, workflow alignment, and code quality. This performance advantage likely
stems from their access to larger and more diverse training corpora, advanced instruction-tuning methods, and more
extensive reinforcement learning from human feedback. These factors appear to improve not only syntax correctness
but also the ability to incorporate domain knowledge and dataset descriptions into coherent geoprocessing pipelines.
Differences in performance across spatial analysis categories provide insight into LLM generalization. Tasks in
“Finding the best locations and paths” (F) and “Determining how places are related” (DR) consistently show higher
difficulty, suggesting that multi-step optimization, spatial network analysis, and hierarchical decision-making require
reasoning capabilities not yet well represented in general-purpose model training. In contrast, categories like “Measuring size, shape, and distribution” (M) or “Detecting and quantifying patterns” (DP) benefit from statistical pattern
recognition skills that LLMs appear to generalize more effectively. This unevenness points to the need for GIS-specific
pretraining that emphasizes relational and optimization-based reasoning.
The results also reveal important differences within the open-source group. While smaller models such as DeepSeekR1-7B and CodeLlama struggle to produce valid and efficient workflows, Llama-3.1-8B approaches proprietary performance in several scenarios. This indicates that with targeted fine-tuning on high-quality GIS corpora, open-source
models could offer competitive alternatives for users requiring transparency and customizability.
From a practical standpoint, the evaluation metrics (valid rate, MAD, and CodeBLEU) used here map to critical
qualities for real-world GIS automation. A high valid rate reflects reliability in producing runnable outputs; low MAD
indicates workflow efficiency and avoidance of unnecessary complexity; higher CodeBLEU scores imply better preservation of logical and syntactic integrity, reducing the risk of execution errors. Together, these measures provide an
interpretable framework for assessing robustness in operational settings, where reproducibility, efficiency, and correctness directly affect decision-making and project timelines.
These findings suggest a pathway toward more usable LLM-powered GeoAI systems: leveraging proprietary

## Page 23

Zhang et al.

23

model strengths where resources allow, while investing in domain-specific pre-training and fine-tuning to narrow
the gap for open-source models. Integrating retrieval-augmented generation and human-in-the-loop validation may
further improve generalization to complex, context-dependent spatial problems.

8

|

CONCLUSION

The results of this research showcase the strengths and weaknesses of the state-of-the-art Large Language Models
(LLMs) in the context of spatial analysis workflows and GIS automation. By comparing LLM-generated workflows and
code with GIS experts designed benchmarks, we offer important insights of these models in performing spatial analysis
tasks. The most advanced LLMs have similar levels of performance for spatial analysis tasks, which demonstrates a
powerful baseline for the current data-driven tasks in GeoAI. Importantly, spatial knowledge relate tasks (F and DR) are
more difficult than regular data analysis tasks for the LLMs, indicating the limitations for current models’ capabilities. At
the same time, it’s highly possible for fine-tuned LLMs to get better performance on spatial analysis tasks by adapting
GIS software documentations through retrieval-augmented generation (RAG) techniques.
At the same time, the proposed GeoAnalystBench is a valuable benchmark dataset for evaluating the workflow
and code generation capabilities of LLMs on spatial analysis tasks. The benchmark builds on real-world datasets
and domain-specific problems, each paired with a minimum deliverable product. While these tasks reflect complex,
practical scenarios that can contribute to larger projects, their value also lies in probing whether foundation models
approach problems similarly to human GIS analysts. This contrasts with recent work such as ScienceAgentBench (Chen
et al., 2024), which shares several overlapping tasks but emphasizes the optimization of LLM-agent pipelines through
domain expert feedback and detailed automation protocols. While both benchmarks explore LLM performance in
structured scientific workflows, our focus is specifically on spatial analysis—a domain traditionally considered resistant
to automation due to its complexity and reliance on geographic reasoning, spatial data formats, and context-aware interpretation. As such, GeoAnalystBench offers a complementary perspective by evaluating how well LLMs can support
spatial thinking and potentially democratize GIS practice for non-experts.
Despite the promising outcomes, there are several limitations that must be taken into account. First, the study
focused on evaluating LLM-generated workflows for certain GIS tasks with predefined parameters, and thus the
performance may vary when applied to new or more complicated real-world problems in different scientific domains.
This process requires clearer definitions and high-quality annotations from domain experts. Second, tasks in the
benchmark dataset varied in GIS tools being used, while limited by linear structures. In many cases, subtasks can
be done in parallel, creating a different shape of workflow and generating multiple outputs. Furthermore, LLMs are
also faced with data compatibility issues, such as incorrect parameter passing and incompatible data types, leading to
execution failures. There is a great deficiency in the handling of spatial referencing and transformation, often leading
to de-synchronized spatial data. Some tasks were adapted from publicly available tutorials, so we can’t completely
rule out the possibility that similar examples exist in LLM training data. As Figure 5, Table 2, and Table 3 suggested,
the noticeable performance differences across models and spatial analysis categories suggest that the tasks remain
sufficiently challenging and are not simply memorized. To overcome these deficiencies, it is necessary to enhance the
LLMs with a good validation procedure and enrich their pretraining datasets with more diverse GIS-specific scenarios.
Future research would focus on improving the spatial reasoning capabilities of LLMs in GIS by incorporating
more specialized training datasets that include spatial analysis case studies. Currently, the GeoAnalystBench is still
limited by the coverage of real-world scenarios, leaving space for future improvement on the dataset side. At the
same time, it is important to understand how the integration of the RAG technique will assist LLMs in automatically

## Page 24

24

Zhang et al.

planning and organizing the geoprocessing tools. Interestingly, LLMs also have gaps between them. Furthermore,
expanding the benchmark evaluation framework to include user studies would provide deeper insights into how GIS
practitioners interact with LLM-generated workflows and what improvements are necessary to make them more
effective in practical applications. The advancement in GeoAI research requires more community efforts on creating,
maintaining, and assessing domain-specific benchmarks.

Acknowledgements
We acknowledge the funding support from the National Science Foundation funded AI institute [Grant No. 2112606]
for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE). Any opinions, findings,
and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily
reflect the views of the funder(s).

References
Akinboyewa, T., Li, Z., Ning, H. and Lessani, M. N. (2025) Gis copilot: Towards an autonomous gis agent for spatial analysis.
International Journal of Digital Earth, 18, 2497489.
Andrew, M. E., Wulder, M. A., Nelson, T. A. and Coops, N. C. (2015) Spatial data, analysis approaches, and information needs
for spatial ecosystem service assessments: a review. GIScience & Remote Sensing, 52, 344–373.
Anthropic (2024) Claude 3.5 sonnet. URL: https://www.anthropic.com/news/claude- 3- 5-sonnet. Accessed: 2025-02-12.
Cervone, G., Sava, E., Huang, Q., Schnebele, E., Harrison, J. and Waters, N. (2015) Using Twitter for tasking remote-sensing
data collection and damage assessment: 2013 Boulder flood case study. International Journal of Remote Sensing, 37, 100–
124. URL: https://doi.org/10.1080/01431161.2015.1117684.
Chen, J., Tang, J., Qin, J., Liang, X., Liu, L., Xing, E. P. and Lin, L. (2021) GeOQA: A geometric question answering benchmark
towards multimodal numerical Reasoning. arXiv (Cornell University). URL: https://arxiv.org/abs/2105.14517.
Chen, Z., Chen, S., Ning, Y., Zhang, Q., Wang, B., Yu, B., Li, Y., Liao, Z., Wei, C., Lu, Z. et al. (2024) Scienceagentbench: Toward
rigorous assessment of language agents for data-driven scientific discovery. arXiv preprint arXiv:2410.05080.
Danish, M. S., Munir, M. A., Shah, S. R. A., Kuckreja, K., Khan, F. S., Fraccaro, P., Lacoste, A. and Khan, S. (2024) GEOBench-VLM:
Benchmarking Vision-Language Models for geospatial tasks. URL: https://arxiv.org/abs/2411.19325.
DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P., Bi, X., Zhang, X., Yu, X., Wu,
Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A., Xue, B., Wang, B., Wu, B., Feng, B., Lu, C., Zhao, C., Deng, C., Zhang,
C., Ruan, C., Dai, D., Chen, D., Ji, D., Li, E., Lin, F., Dai, F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H., Bao, H., Xu, H., Wang,
H., Ding, H., Xin, H., Gao, H., Qu, H., Li, H., Guo, J., Li, J., Wang, J., Chen, J., Yuan, J., Qiu, J., Li, J., Cai, J. L., Ni, J., Liang,
J., Chen, J., Dong, K., Hu, K., Gao, K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L., Zhao, L., Wang, L., Zhang, L., Xu, L.,
Xia, L., Zhang, M., Zhang, M., Tang, M., Li, M., Wang, M., Li, M., Tian, N., Huang, P., Zhang, P., Wang, Q., Chen, Q., Du, Q.,
Ge, R., Zhang, R., Pan, R., Wang, R., Chen, R. J., Jin, R. L., Chen, R., Lu, S., Zhou, S., Chen, S., Ye, S., Wang, S., Yu, S., Zhou,
S., Pan, S., Li, S. S., Zhou, S., Wu, S., Ye, S., Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W., Zhao, W., Liu, W., Liang, W., Gao,
W., Yu, W., Zhang, W., Xiao, W. L., An, W., Liu, X., Wang, X., Chen, X., Nie, X., Cheng, X., Liu, X., Xie, X., Liu, X., Yang, X.,
Li, X., Su, X., Lin, X., Li, X. Q., Jin, X., Shen, X., Chen, X., Sun, X., Wang, X., Song, X., Zhou, X., Wang, X., Shan, X., Li, Y. K.,
Wang, Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li, Y., Zhao, Y., Sun, Y., Wang, Y., Yu, Y., Zhang, Y., Shi, Y., Xiong, Y., He, Y., Piao, Y.,
Wang, Y., Tan, Y., Ma, Y., Liu, Y., Guo, Y., Ou, Y., Wang, Y., Gong, Y., Zou, Y., He, Y., Xiong, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y.,
Zhu, Y. X., Xu, Y., Huang, Y., Li, Y., Zheng, Y., Zhu, Y., Ma, Y., Tang, Y., Zha, Y., Yan, Y., Ren, Z. Z., Ren, Z., Sha, Z., Fu, Z., Xu,
Z., Xie, Z., Zhang, Z., Hao, Z., Ma, Z., Yan, Z., Wu, Z., Gu, Z., Zhu, Z., Liu, Z., Li, Z., Xie, Z., Song, Z., Pan, Z., Huang, Z., Xu,
Z., Zhang, Z. and Zhang, Z. (2025) DeepSeek-R1: Incentivizing reasoning capability in LLMs via Reinforcement Learning.
URL: https://arxiv.org/abs/2501.12948.

## Page 25

Zhang et al.

25

ESRI (2013) The language of spatial analysis. ESRI. URL: https://www.esri.com/content/dam/esrisites/sitecore-archive/
Files/Pdfs/library/books/the-language-of-spatial-analysis.pdf.
Gramacki, P., Martins, B. and Szymański, P. (2024) Evaluation of code llms on geospatial code generation. In Proceedings of the
7th ACM SIGSPATIAL International Workshop on AI for Geographic Knowledge Discovery, 54–62.
Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A., Vaughan, A.,
Yang, A., Fan, A., Goyal, A., Hartshorn, A., Yang, A., Mitra, A., Sravankumar, A., Korenev, A., Hinsvark, A., Rao, A., Zhang,
A., Rodriguez, A., Gregerson, A., Spataru, A., Roziere, B., Biron, B., Tang, B., Chern, B., Caucheteux, C., Nayak, C., Bi, C.,
Marra, C., McConnell, C., Keller, C., Touret, C., Wu, C., Wong, C., Ferrer, C. C., Nikolaidis, C., Allonsius, D., Song, D., Pintz,
D., Livshits, D., Wyatt, D., Esiobu, D., Choudhary, D., Mahajan, D., Garcia-Olano, D., Perino, D., Hupkes, D., Lakomkin, E.,
AlBadawy, E., Lobanova, E., Dinan, E., Smith, E. M., Radenovic, F., Guzmán, F., Zhang, F., Synnaeve, G., Lee, G., Anderson,
G. L., Thattai, G., Nail, G., Mialon, G., Pang, G., Cucurell, G., Nguyen, H., Korevaar, H., Xu, H., Touvron, H., Zarov, I., Ibarra,
I. A., Kloumann, I., Misra, I., Evtimov, I., Zhang, J., Copet, J., Lee, J., Geffert, J., Vranes, J., Park, J., Mahadeokar, J., Shah, J.,
Jelmer, V. D. L., Billock, J., Hong, J., Lee, J., Fu, J., Chi, J., Huang, J., Liu, J., Wang, J., Yu, J., Bitton, J., Spisak, J., Park, J., Rocca,
J., Johnstun, J., Saxe, J., Jia, J., Alwala, K. V., Prasad, K., Upasani, K., Plawiak, K., Li, K., Heafield, K., Stone, K., El-Arini, K.,
Iyer, K., Malik, K., Chiu, K., Bhalla, K., Lakhotia, K., Rantala-Yeary, L., Laurens, V. D. M., Chen, L., Tan, L., Jenkins, L., Martin,
L., Madaan, L., Malo, L., Blecher, L., Landzaat, L., Luke, D. O., Muzzi, M., Pasupuleti, M., Singh, M., Paluri, M., Kardas, M.,
Tsimpoukelli, M., Oldham, M., Rita, M., Pavlova, M., Kambadur, M., Lewis, M., Si, M., Singh, M. K., Hassan, M., Goyal, N.,
Torabi, N., Bashlykov, N., Bogoychev, N., Chatterji, N., Zhang, N., Duchenne, O., Çelebi, O., Alrassy, P., Zhang, P., Li, P.,
Vasic, P., Weng, P., Bhargava, P., Dubal, P., Krishnan, P., Koura, P. S., Xu, P., He, Q., Dong, Q., Srinivasan, R., Ganapathy, R.,
Calderer, R., Cabral, R. S., Stojnic, R., Raileanu, R., Maheswari, R., Girdhar, R., Patel, R., Sauvestre, R., Polidoro, R., Sumbaly,
R., Taylor, R., Silva, R., Hou, R., Wang, R., Hosseini, S., Chennabasappa, S., Singh, S., Bell, S., Kim, S. S., Edunov, S., Nie,
S., Narang, S., Raparthy, S., Shen, S., Wan, S., Bhosale, S., Zhang, S., Vandenhende, S., Batra, S., Whitman, S., Sootla, S.,
Collot, S., Gururangan, S., Borodinsky, S., Herman, T., Fowler, T., Sheasha, T., Georgiou, T., Scialom, T., Speckbacher, T.,
Mihaylov, T., Xiao, T., Karn, U., Goswami, V., Gupta, V., Ramanathan, V., Kerkez, V., Gonguet, V., Do, V., Vogeti, V., Albiero,
V., Petrovic, V., Chu, W., Xiong, W., Fu, W., Meers, W., Martinet, X., Wang, X., Wang, X., Tan, X. E., Xia, X., Xie, X., Jia, X.,
Wang, X., Goldschlag, Y., Gaur, Y., Babaei, Y., Wen, Y., Song, Y., Zhang, Y., Li, Y., Mao, Y., Coudert, Z. D., Yan, Z., Chen, Z.,
Papakipos, Z., Singh, A., Srivastava, A., Jain, A., Kelsey, A., Shajnfeld, A., Gangidi, A., Victoria, A., Goldstand, A., Menon,
A., Sharma, A., Boesenberg, A., Baevski, A., Feinstein, A., Kallet, A., Sangani, A., Teo, A., Yunus, A., Lupu, A., Alvarado, A.,
Caples, A., Gu, A., Ho, A., Poulton, A., Ryan, A., Ramchandani, A., Dong, A., Franco, A., Goyal, A., Saraf, A., Chowdhury, A.,
Gabriel, A., Bharambe, A., Eisenman, A., Yazdan, A., James, B., Maurer, B., Leonhardi, B., Huang, B., Loyd, B., Beto, D. P.,
Paranjape, B., Liu, B., Wu, B., Ni, B., Hancock, B., Wasti, B., Spence, B., Stojkovic, B., Gamido, B., Montalvo, B., Parker,
C., Burton, C., Mejia, C., Liu, C., Wang, C., Kim, C., Zhou, C., Hu, C., Chu, C.-H., Cai, C., Tindal, C., Feichtenhofer, C., Gao,
C., Civin, D., Beaty, D., Kreymer, D., Li, D., Adkins, D., Xu, D., Testuggine, D., David, D., Parikh, D., Liskovich, D., Foss, D.,
Wang, D., Le, D., Holland, D., Dowling, E., Jamil, E., Montgomery, E., Presani, E., Hahn, E., Wood, E., Le, E.-T., Brinkman, E.,
Arcaute, E., Dunbar, E., Smothers, E., Sun, F., Kreuk, F., Tian, F., Kokkinos, F., Ozgenel, F., Caggioni, F., Kanayet, F., Seide,
F., Florez, G. M., Schwarz, G., Badeer, G., Swee, G., Halpern, G., Herman, G., Sizov, G., Guangyi, Zhang, Lakshminarayanan,
G., Inan, H., Shojanazeri, H., Zou, H., Wang, H., Zha, H., Habeeb, H., Rudolph, H., Suk, H., Aspegren, H., Goldman, H.,
Zhan, H., Damlaj, I., Molybog, I., Tufanov, I., Leontiadis, I., Veliche, I.-E., Gat, I., Weissman, J., Geboski, J., Kohli, J., Lam, J.,
Asher, J., Gaya, J.-B., Marcus, J., Tang, J., Chan, J., Zhen, J., Reizenstein, J., Teboul, J., Zhong, J., Jin, J., Yang, J., Cummings,
J., Carvill, J., Shepard, J., McPhie, J., Torres, J., Ginsburg, J., Wang, J., Wu, K., U, K. H., Saxena, K., Khandelwal, K., Zand,
K., Matosich, K., Veeraraghavan, K., Michelena, K., Li, K., Jagadeesh, K., Huang, K., Chawla, K., Huang, K., Chen, L., Garg,
L., A, L., Silva, L., Bell, L., Zhang, L., Guo, L., Yu, L., Moshkovich, L., Wehrstedt, L., Khabsa, M., Avalani, M., Bhatt, M.,
Mankus, M., Hasson, M., Lennie, M., Reso, M., Groshev, M., Naumov, M., Lathi, M., Keneally, M., Liu, M., Seltzer, M. L.,
Valko, M., Restrepo, M., Patel, M., Vyatskov, M., Samvelyan, M., Clark, M., Macey, M., Wang, M., Hermoso, M. J., Metanat,
M., Rastegari, M., Bansal, M., Santhanam, N., Parks, N., White, N., Bawa, N., Singhal, N., Egebo, N., Mehta, N., Laptev,
N. P., Dong, N., Cheng, N., Chernoguz, O., Hart, O., Salpekar, O., Kalinli, O., Kent, P., Parekh, P., Saab, P., Balaji, P., Rittner,
P., Bontrager, P., Roux, P., Dollar, P., Zvyagina, P., Ratanchandani, P., Yuvraj, P., Liang, Q., Alao, R., Rodriguez, R., Ayub, R.,
Murthy, R., Nayani, R., Mitra, R., Parthasarathy, R., Li, R., Hogan, R., Battey, R., Wang, R., Howes, R., Rinott, R., Mehta,
S., Siby, S., Bondu, S. J., Datta, S., Chugh, S., Hunt, S., Dhillon, S., Sidorov, S., Pan, S., Mahajan, S., Verma, S., Yamamoto,
S., Ramaswamy, S., Lindsay, S., Lindsay, S., Feng, S., Lin, S., Zha, S. C., Patil, S., Shankar, S., Zhang, S., Zhang, S., Wang, S.,
Agarwal, S., Sajuyigbe, S., Chintala, S., Max, S., Chen, S., Kehoe, S., Satterfield, S., Govindaprasad, S., Gupta, S., Deng, S.,
Cho, S., Virk, S., Subramanian, S., Choudhury, S., Goldman, S., Remez, T., Glaser, T., Best, T., Koehler, T., Robinson, T., Li,

## Page 26

26

Zhang et al.

T., Zhang, T., Matthews, T., Chou, T., Shaked, T., Vontimitta, V., Ajayi, V., Montanez, V., Mohan, V., Kumar, V. S., Mangla,
V., Ionescu, V., Poenaru, V., Mihailescu, V. T., Ivanov, V., Li, W., Wang, W., Jiang, W., Bouaziz, W., Constable, W., Tang, X.,
Wu, X., Wang, X., Wu, X., Gao, X., Kleinman, Y., Chen, Y., Hu, Y., Jia, Y., Qi, Y., Li, Y., Zhang, Y., Zhang, Y., Adi, Y., Nam, Y.,
Yu, Wang, Zhao, Y., Hao, Y., Qian, Y., Li, Y., He, Y., Rait, Z., DeVito, Z., Rosnbrick, Z., Wen, Z., Yang, Z., Zhao, Z. and Ma, Z.
(2024) The llama 3 herd of models. URL: https://arxiv.org/abs/2407.21783.
Hou, S., Liang, J., Zhao, A. and Wu, H. (2024) Gee-ops: An operator knowledge base for geospatial code generation on the
google earth engine platform powered by large language models. arXiv preprint arXiv:2412.05587.
Hsieh, C.-Y., Li, C.-L., Yeh, C.-K., Nakhost, H., Fujii, Y., Ratner, A., Krishna, R., Lee, C.-Y. and Pfister, T. (2023) Distilling stepby-step! outperforming larger language models with less training data and smaller model sizes. URL: https://arxiv.org/
abs/2305.02301.
Huang, W., Wang, J. and Cong, G. (2024) Zero-shot urban function inference with street view images through prompting a
pretrained vision-language model. International Journal of Geographical Information Science, 38, 1414–1442.
Jakubik, J., Roy, S., Phillips, C., Fraccaro, P., Godwin, D., Zadrozny, B., Szwarcman, D., Gomes, C., Nyirjesy, G., Edwards, B. et al.
(2023) Foundation models for generalist geospatial artificial intelligence. arXiv preprint arXiv:2310.18660.
Janowicz, K., Gao, S., McKenzie, G., Hu, Y. and Bhaduri, B. (2020) GeoAI: spatially explicit artificial intelligence techniques for
geographic knowledge discovery and beyond. International Journal of Geographical Information Science, 34, 625–636. URL:
https://doi.org/10.1080/13658816.2019.1684500.
Janowicz, K., Mai, G., Huang, W., Zhu, R., Lao, N. and Cai, L. (2025) GeoFM: how will geo-foundation models reshape spatial
data science and GeoAI? International Journal of Geographical Information Science, 39, 1849–1865.
Ji, Y., Gao, S., Nie, Y., Majić, I. and Janowicz, K. (2025) Foundation models for geospatial reasoning: assessing the capabilities of
large language models in understanding geometries and topological spatial relations. International Journal of Geographical
Information Science, 39, 1866–1903.
Jiang, Y. and Yang, C. (2024) Is chatgpt a good geospatial data analyst? exploring the integration of natural language into
structured query language within a spatial database. ISPRS International Journal of Geo-Information, 13, 26.
Krechetova, V. and Kochedykov, D. (2025) GeoBenchX: Benchmarking LLMs for Multistep geospatial Tasks. URL: https:
//arxiv.org/abs/2503.18129.
Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T. et al. (2020)
Retrieval-augmented generation for knowledge-intensive nlp tasks. Advances in Neural Information Processing Systems, 33,
9459–9474.
Li, D., Ding, R., Zhang, Q., Li, Z., Chen, B., Xie, P., Xu, Y., Li, X., Guo, N., Huang, F. and He, X. (2023) GeoGLUE: a GeoGraphic
Language Understanding Evaluation Benchmark. arXiv (Cornell University). URL: https://arxiv.org/abs/2305.06545.
Li, Z. and Ning, H. (2023) Autonomous gis: the next-generation ai-powered gis. International Journal of Digital Earth, 16,
4668–4686.
Li, Z., Ning, H., Gao, S., Janowicz, K., Li, W., Arundel, S. T., Yang, C., Bhaduri, B., Wang, S., Zhu, A. et al. (2025) Giscience in the
era of artificial intelligence: A research agenda towards autonomous gis. arXiv preprint arXiv:2503.23633.
Mai, G., Huang, W., Sun, J., Song, S., Mishra, D., Liu, N., Gao, S., Liu, T., Cong, G., Hu, Y. et al. (2024) On the opportunities and
challenges of foundation models for geoai (vision paper). ACM Transactions on Spatial Algorithms and Systems, 10, 1–46.
Ning, H., Li, Z., Akinboyewa, T. and Lessani, M. N. (2025) An autonomous gis agent framework for geospatial data retrieval.
International Journal of Digital Earth, 18, 2458688.
Pham, H. M., Yamaguchi, Y. and Bui, T. Q. (2011) A case study on the relation between city planning and urban growth using
remote sensing and spatial metrics. Landscape and Urban Planning, 100, 223–230.

## Page 27

Zhang et al.

27

Ren, S., Guo, D., Lu, S., Zhou, L., Liu, S., Tang, D., Sundaresan, N., Zhou, M., Blanco, A. and Ma, S. (2020) Codebleu: a method
for automatic evaluation of code synthesis. arXiv preprint arXiv:2009.10297.
Singh, C., Inala, J. P., Galley, M., Caruana, R. and Gao, J. (2024) Rethinking interpretability in the era of large language models.
URL: https://arxiv.org/abs/2402.01761.
Toms, S. (2015) ArcPy and ArcGIS–Geospatial Analysis with Python. Packt Publishing Ltd.
Wang, S., Hu, T., Xiao, H., Li, Y., Zhang, C., Ning, H., Zhu, R., Li, Z. and Ye, X. (2024) GPT, large language models (LLMs) and
generative artificial intelligence (GAI) models in geospatial science: a systematic review. International Journal of Digital
Earth, 17, 2353122.
Wang, W., Wei, F., Dong, L., Bao, H., Yang, N. and Zhou, M. (2020) Minilm: Deep self-attention distillation for task-agnostic
compression of pre-trained transformers. URL: https://arxiv.org/abs/2002.10957.
Van de Weghe, N., De Sloover, L., Cohn, A., Huang, H., Scheider, S., Sieber, R., Timpf, S. and Claramunt, C. (2025) Opportunities
and challenges of integrating geographic information science and large language models. Journal of Spatial Information
Science, 93–116.
Wei, C., Zhang, Y., Zhao, X., Zeng, Z., Wang, Z., Lin, J., Guan, Q. and Yu, W. (2024) Geotool-gpt: a trainable method for
facilitating large language models to master gis tools. International Journal of Geographical Information Science, 1–25.
Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q. V., Zhou, D. et al. (2022) Chain-of-thought prompting
elicits reasoning in large language models. Advances in neural information processing systems, 35, 24824–24837.
Wu, M., Huang, Q., Gao, S. and Zhang, Z. (2023) Mixed land use measurement and mapping with street view images and
spatial context-aware prompts via zero-shot multimodal learning. International Journal of Applied Earth Observation and
Geoinformation, 125, 103591.
Xu, L., Zhao, S., Lin, Q., Chen, L., Luo, Q., Wu, S., Ye, X., Feng, H. and Du, Z. (2025) Evaluating large language models on
geospatial tasks: a multiple geospatial task benchmarking study. International Journal of Digital Earth, 18, 2480268.
Yang, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Li, C., Liu, D., Huang, F., Wei, H. et al. (2024) Qwen2. 5 technical report.
arXiv preprint arXiv:2412.15115.
Yue, X., Ni, Y., Zhang, K., Zheng, T., Liu, R., Zhang, G., Stevens, S., Jiang, D., Ren, W., Sun, Y. et al. (2024) Mmmu: A massive multidiscipline multimodal understanding and reasoning benchmark for expert agi. In Proceedings of the IEEE/CVF Conference
on Computer Vision and Pattern Recognition, 9556–9567.
Zhang, Q. and Gao, S. (2024) Automating geospatial analysis workflows using chatgpt-4. In Proceedings of the 32nd ACM
International Conference on Advances in Geographic Information Systems, 715–716.
Zhang, Y., He, Z., Li, J., Lin, J., Guan, Q. and Yu, W. (2024a) Mapgpt: an autonomous framework for mapping by integrating
large language model and cartographic tools. Cartography and Geographic Information Science, 51, 717–743.
Zhang, Y., Wang, Z., He, Z., Li, J., Mai, G., Lin, J., Wei, C. and Yu, W. (2024b) Bb-geogpt: A framework for learning a large
language model for geographic information science. Information Processing & Management, 61, 103808.
Zhang, Y., Wei, C., He, Z. and Yu, W. (2024c) Geogpt: An assistant for understanding and processing geospatial tasks. International Journal of Applied Earth Observation and Geoinformation, 131, 103976.

## Page 28

28

Zhang et al.

Appendix
A

A.1

| CASE STUDY 1: IDENTIFICATION OF HOME RANGE AND SPATIAL CLUSTERS FROM ANIMAL MOVEMENTS
|

Workflow Prompt

As a Geospatial data scientist, you will generate a workflow to a proposed task.
[Task]: Use animal GPS tracks to model home range to understand where they are and how they move over
time.
[Instruction]: Your task is to analyze and visualize elk movements using the provided dataset. The goal is to
estimate home ranges and assess habitat preferences using spatial analysis techniques, including Minimum
Bounding Geometry (Convex Hull), Kernel Density Estimation, and Density-Based Clustering (DBSCAN).
The analysis will generate spatial outputs stored in dataset/elk_home_range.gdb and dataset/.
[Domain Knowledge]: "Home range" can be defined as the area within which an animal normally lives and
finds what it needs for survival. Minimum Bounding Geometry creates a feature class containing polygons
that represent a specified minimum bounding geometry enclosing each input feature. "Convex hull" is the
smallest convex polygon that can enclose a group of objects. "Kernel Density Mapping" calculates and
visualizes feature density in a given area. "DBSCAN" (Density-Based Spatial Clustering of Applications with
Noise) clusters the points based on a density criterion.
[Dataset Description]: dataset/Elk_in_Southwestern_Alberta_2009.geojson, containing GPS
points of elk movements in Southwestern Alberta, 2009.
Columns: ’OBJECTID’, ’timestamp’, ’long’, ’lat’, ’comments’, ’external_t’, ’dop’,
’fix_type_r’, ’satellite_’, ’height’, ’crc_status’, ’outlier_ma’, ’sensor_typ’,
’individual’, ’tag_ident’, ’ind_ident’, ’study_name’, ’date’, ’time’, ’timestamp_Converted’,
’summer_indicator’, ’geometry’
[Key Notes]:
1. Use automatic reasoning and clearly explain each step (Chain of Thoughts approach).
2. Use NetworkX package for workflow visualization.
3. Use dot layout for graph visualization.
4. Subtasks may proceed in parallel; all outputs feed the next subtask.
5. Limit output to code only.
6. Only include workflow code, no implementation.
[Expected Sample Output Begin]
tasks = [Task1, Task2, Task3]
G = nx.DiGraph()
for i in range(len(tasks) - 1):
G.add_edge(tasks[i], tasks[i + 1])
pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")

## Page 29

Zhang et al.

29

plt.figure(figsize=(15, 8))
nx.draw(G, pos, with_labels=True, node_size=3000,
node_color=’lightblue’, font_size=10,
font_weight=’bold’, arrowsize=20)
plt.title("Workflow for Analyzing Urban Heat Using Kriging Interpolation", fontsize=14)
plt.show()
[Expected Sample Output End]

|

A.2

Code Generation Prompt

As a Geospatial data scientist, generate a Python file to solve the proposed task.
[Task]: Use animal GPS tracks to model home range to understand where they are and how they move over
time.
[Instruction]: Analyze and visualize elk movements using the dataset. Estimate home ranges and assess
habitat preferences using Minimum Bounding Geometry (Convex Hull), Kernel Density Estimation, and
DBSCAN. Save outputs to dataset/elk_home_range.gdb and dataset/.
[Domain Knowledge]: Explained in workflow section above.
[Dataset Description]: dataset/Elk_in_Southwestern_Alberta_2009.geojson
Columns: Same as listed above.
[Key Notes]:
1. Use automatic reasoning; explain each subtask before performing (ReAct approach).
2. Use latest Python packages.
3. Put all code under main().
4. Do not include helper functions.
5. Limit output to code only.
6. Use latest arcpy functions only.

B
B.1

|

CASE STUDY 2: SPATIAL HOTSPOT ANALYSIS OF CAR ACCIDENTS
|

Workflow Prompt

As a Geospatial data scientist, you will generate a workflow to a proposed task.
[Task]: Identify hot spots for peak crashes
[Instruction]: Your task is identifying hot spots for peak crashes in Brevard County, Florida, 2010–2015.
The first step is to select all the crashes based on the peak time zone. Create a copy of the selected crash
data. Then, snap the crash points to the road network and perform a spatial join with the roads. Calculate
the crash rate from the joined data and use hot spot analysis to generate a crash hot spot map.
[Domain Knowledge]: Traffic between 3:00 pm and 5:00 pm on weekdays is considered peak time. For the
snapping process, a buffer of 0.25 miles around roads is recommended. Hot spot analysis identifies spatial
clusters with high crash rates, so accurate road-network-based distance measurements are crucial.

## Page 30

30

Zhang et al.

[Dataset Description]:
• dataset/crashes.shp: Locations of crashes in Brevard County (2010–2015)
• dataset/roads.shp: Road network of Brevard County
• dataset/nwswm360ft.swm: Spatial weights matrix created from road polylines
[Key Notes]:
1. Use automatic reasoning and clearly explain each step (Chain of Thoughts approach).
2. Use NetworkX for visualizing the workflow.
3. Use dot layout for graph visualization.
4. Allow multiple subtasks to proceed in parallel if their outputs feed into the next step.
5. Limit the output to code only, with no additional explanation.
6. Only include workflow logic (no implementation).
[Expected Sample Output Begin]
tasks = [Task1, Task2, Task3]
G = nx.DiGraph()
for i in range(len(tasks) - 1):
G.add_edge(tasks[i], tasks[i + 1])
pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")
plt.figure(figsize=(15, 8))
nx.draw(G, pos, with_labels=True, node_size=3000,
node_color=’lightblue’, font_size=10,
font_weight=’bold’, arrowsize=20)
plt.title("Workflow for Peak Crash Hot Spot Detection", fontsize=14)
plt.show()
[Expected Sample Output End]

B.2

|

Code Generation Prompt

As a Geospatial data scientist, generate a Python file to solve the proposed task.
[Task]: Identify hot spots for peak crashes
[Instruction]: Your task is identifying hot spots for peak crashes in Brevard County, Florida, 2010–2015.
First, filter crashes during the peak time zone. Create a copy of selected crashes. Snap points to roads,
perform a spatial join, calculate crash rate, and apply hot spot analysis.
[Domain Knowledge]: Peak time is 3:00–5:00 pm on weekdays. Use a 0.25-mile buffer for snapping. Accurate road network distances are essential for meaningful hot spot analysis.
[Dataset Description]:
• crashes.shp

## Page 31

Zhang et al.

• roads.shp
• nwswm360ft.swm
[Key Notes]:
1. Use automatic reasoning (ReAct approach).
2. Use the latest Python packages.
3. Write all code inside a main() function.
4. Do not use helper functions.
5. Limit output to code only, with no explanatory text.
6. Use the latest arcpy functions exclusively.

31

## Page 32

32

C

Zhang et al.

|

SUPPLEMENTARY TABLES

TA B L E S - 1 Geospatial Tasks (1–20). The table presents various GIS-related tasks along with their geoprocessing
step lengths, access dates, and last update dates.
ID

Task Name

1

Find heat islands and at-risk populations in Madison, Wisconsin

2
3

Length

Access Date

Last Update

7

2024-7

2025-5

Find future bus stop locations in Hamilton

6

2024-7

2025-1

Assess burn scars and wildfire impact in Montana using satellite

6

2024-7

2024-12

imagery
4

Identify groundwater vulnerable areas that need protection

10

2024-7

2024-9

5

Visualize data on children with elevated blood lead levels while

5

2024-7

2024-10

6

2024-7

2025-1

protecting privacy
6

Use animal GPS tracks to model home range and movement over
time

7

Analyze the impacts of land subsidence on flooding

7

2024-9

2025-7

8

Find gaps in Toronto fire station service coverage

4

2024-6

2025-5

9

Find the deforestation rate for Rondônia

6

2024-8

2025-1

10

Analyze the impact of proposed roads on the local environment

5

2024-8

2025-1

11

Create charts in Python to explore coral and sponge distribution

7

2024-7

2023-10

3

2024-6

2025-1

6

2024-8

2025-7

4

2024-8

2025-7

3

2024-8

2025-7

5

2024-8

2025-7

3

2024-8

2022-12

around Catalina Island
12

Find optimal corridors to connect dwindling mountain lion populations

13

Understand the relationship between ocean temperature and
salinity at various depths in the South Atlantic Ocean

14

Detect persistent periods of high temperature over the past 240
years

15

Understand the geographical distribution of Total Electron Content (TEC) in the ionosphere

16

Analyze climate change trends in North America using spatiotemporal data

17

Analyze the geographical distribution of fatal car crashes in New
York City during 2016

18

Analyze street tree species data in San Francisco

4

2024-8

2022-12

19

Model spatial patterns of water quality

4

2024-10

2025-6

20

Predict the likelihood of tin-tungsten deposits in Tasmania

7

2024-8

2022-12

## Page 33

Zhang et al.

33

TA B L E S - 2 Geospatial Tasks (21–40). The table presents various GIS-related tasks along with their
geoprocessing step lengths, access dates, and last update dates.
ID

Task Name

21

Find optimal corridors to connect dwindling mountain lion pop-

Length

Access Date

Last Update

5

2024-6

2025-1

3

2024-6

2025-1

Assess Open Space to Lower Flood Insurance Cost

4

2024-7

2025-1

Provide a de-identified point-level dataset that includes all the

7

2024-10

2024-10

10

2024-11

2025-2

8

2024-11

2024-9

ulations(2)
22

Find optimal corridors to connect dwindling mountain lion populations(3)

23
24

variables of interest for each child, as well as their general location
25

Create risk maps for transmission, susceptibility, and resource
scarcity. Then create a map of risk profiles to help pinpoint targeted intervention areas

26

Use drainage conditions and water depth to calculate groundwater vulnerable areas

27

Identify undeveloped areas from groundwater risk zones

6

2024-11

2024-9

28

Estimate the origin-destination (OD) flows between regions

7

2025-1

2025-1

based on the socioeconomic attributes of regions and the mobility data
29

Calculate travel time for a tsunami

7

2024-7

2025-5

30

Designate bike routes for commuting professionals

7

2024-7

2021-12

31

Detect aggregation scales of geographical flows

7

2024-10

2019-6

32

Find optimal corridors to connect dwindling mountain lion pop-

8

2024-6

2025-1

ulation(4)
33

Analyze the impacts of land subsidence on flooding

5

2024-7

2025-7

34

Estimate the accessibility of roads to rural areas in Japan

7

2024-12

2025-2

35

Calculate landslide potential for communities affected by wild-

10

2024-10

2024-6

7

2024-11

2025-7

6

2024-11

2024-4

8

2024-11

2024-10

5

2024-11

2022-12

4

2024-11

2018-5

fires
36

Compute the change in vegetation before and after a hailstorm
with the SAVI index

37

Analyze of human sentiments of heat exposure using social media data

38

Calculate travel time from one location to others in a neighborhood

39

Train a Geographically Weighted Regression model to predict the
population’s Bachelor’s degree rate in Georgia

40

Calculate and visualize changes in malaria prevalence

## Page 34

34

Zhang et al.

TA B L E S - 3 Geospatial Tasks (41–50). The table presents various GIS-related tasks along with their
geoprocessing step lengths, access dates, and last update dates.
ID

Task Name

41

Improve campsite data quality using a relationship class

42
43

Length

Access Date

Last Update

4

2024-11

2024-10

Investigate spatial patterns for Airbnb prices in Berlin

8

2024-12

2024-8

Use animal GPS tracks to model home range to understand

4

2024-7

2025-1

where they are and how they move over time (ArcPy Version)
44

Find gap for Toronto fire station service coverage (ArcPy Version)

5

2024-6

2025-5

45

Find optimal corridors to connect dwindling mountain lion pop-

4

2024-6

2025-1

ulations (ArcPy Version)
46

Identify spatial hot spots for peak crashes

9

2024-12

2024-8

47

Calculate impervious surface area

4

2024-12

2025-2

48

Determine how location impacts interest rates

5

2024-12

2024-10

49

Mapping the Impact of Housing Shortage on Oil Workers

4

2024-12

2023-8

50

Predict sea grass habitats

6

2024-11

2025-5
