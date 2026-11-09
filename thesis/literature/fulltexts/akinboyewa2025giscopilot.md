---
id: literature/fulltexts/akinboyewa2025giscopilot
type: fulltext
status: frozen
language: en
key: akinboyewa2025giscopilot
title: >-
  GIS Copilot: towards an autonomous GIS agent for spatial analysis
resource: https://doi.org/10.1080/17538947.2025.2497489
description: >-
  Recent advancements in generative artificial intelligence (AI), particularly Large Language Models (LLMs), offer promising capabilities for spatial analysis.
pages: 65
words: 15316
year: 2025
venue: >-
  International Journal of Digital Earth
authors: >-
  Akinboyewa, Temitope; Li, Zhenlong; Ning, Huan; Lessani, M. Naser
doi: 10.1080/17538947.2025.2497489
oa_status: gold
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# GIS Copilot: towards an autonomous GIS agent for spatial analysis

## Page 1

GIS Copilot: Towards an Autonomous GIS Agent for Spatial Analysis
Temitope Akinboyewa, Zhenlong Li*, Huan Ning, M. Naser Lessani
Geoinformation and Big Data Research Lab, Department of Geography, The Pennsylvania State
University, University Park, USA
*

zhenlong@psu.edu

Abstract
Recent advancements in generative artificial intelligence (AI) and particularly Large
Language Models (LLMs), offer promising capabilities for spatial analysis. Despite their
potential, the integration of generative AI with established GIS platforms remains underexplored.
In this study, we propose a framework for integrating LLMs directly into existing GIS platforms,
using the well-developed QGIS software as an example. Our approach leverages the reasoning
and programming capabilities of LLMs to autonomously generate spatial analysis workflows and
code through an informed agent that has comprehensive documentation of key GIS tools and
parameters. The framework also incorporates external tools such as GeoPandas to enhance the
system's geoprocessing capabilities. The implementation of this framework resulted in the
development of a "GIS Copilot" that allows GIS users to interact with QGIS using natural
language for spatial analysis. The GIS Copilot was evaluated with over 100 spatial analysis tasks
with three complexity levels: basic tasks that require one GIS tool and typically involve one data
layer to perform simple operations; intermediate tasks involving multi-step processes with
multiple tools, guided by user instructions; and advanced tasks which involve multi-step
processes that require multiple tools but not guided by explicit instructions, necessitating the
agent to independently decide on and executes the necessary steps. The evaluation reveals that
the GIS Copilot demonstrates strong potential in automating foundational GIS operations, with a
high success rate in tool selection and code generation for basic and intermediate tasks, while
challenges remain in achieving full autonomy for more complex tasks. This study contributes to
the emerging vision of autonomous GIS, providing a pathway for non-experts to engage with
geospatial analysis with minimal prior expertise. While full autonomy is yet to be achieved, the
GIS Copilot demonstrates significant potential for simplifying GIS workflows and enhancing
decision-making processes.
Keywords: Autonomous GIS, Spatial Analysis, QGIS, Copilot, Generative AI, LLM

Data, source code, and tool availability: The source code for the GIS Copilot is available on GitHub at
https://shorturl.at/vRcm6. The GIS Copilot can be downloaded from the official QGIS plugin page at
https://plugins.qgis.org/plugins/SpatialAnalysisAgent-master and installed by following the instructions provided in
the GIS Copilot User Manual. The datasets used for testing alongside with the 110 test case can be accessed through
https://shorturl.at/bI4Ep.

1

## Page 2

1

Introduction

Recent advancements of generative artificial intelligence (AI), particularly the Large
Language Models (LLMs), have gained significant attention in geographic information science
(GIScience) through their abilities in reasoning, natural language understanding, and code
generation. LLMs offer a wide range of potential applications within geographic information
systems (GIS), including spatial data analysis, geoprocessing automation, and geospatial
knowledge extraction. A pioneering study by Li and Ning (2023) introduced autonomous GIS as
a next-generation AI-powered GIS, demonstrating the potential of generative AI in generating
geoprocessing workflows and conducting spatial analysis autonomously. A number of studies
have further examined the integration of generative AI (LLMs) within GIS. For instance,
researchers have explored its applications in cartography (Tao and Xu, 2023; Zhang et al.,
2024a), disaster management (Akinboyewa et al., 2024; Hao et al., 2024), GIS-based question
answering (Mooney et al., 2023; Zhang et al., 2024b), location descriptions extraction (Hu et al.,
2023), and geospatial data retrieval (Ning et al., 2024). These efforts collectively demonstrate
that generative AI holds promise in enhancing and potentially transforming traditional GIS
workflows.
While the integration of generative AI in GIS has shown significant promise, one key
limitation is that these existing approaches have not fully embedded LLM capabilities within
established GIS platforms like QGIS (2024), ArcGIS Pro (ESRI, 2024), and GRASS GIS (2024).
Li and Ning (2023) suggest that implementing autonomous GIS based on existing GIS platforms
as a "co-pilot" is likely the most practical and efficient approach, as established GIS platforms
already provide extensive tools for spatial analysis, data management, and visualization.
However, the integration of LLMs into GIS platforms like QGIS presents several challenges.
First, GIS platforms are inherently complex, supporting diverse tools, libraries, and workflows
for data visualization, spatial analysis, geoprocessing, and cartographic rendering. These tools
often rely on diverse frameworks, data standards, and programming languages, complicating the
creation of a single, cohesive workflow that integrates AI smoothly. Second, effective
communication between the AI and existing GIS functions requires robust and error-free
interaction. This involves translating natural language queries into GIS commands and ensuring
that those commands align with GIS native tools and associated tool parameters. Such a process
demands extensive fine-tuning and specialized approaches to understand the full breadth of GIS
tools and operations. Additionally, GIS workflows are often highly customized and problem
specific. Developing an AI integration that can seamlessly adapt to these custom workflows,
while being flexible enough to handle various user-defined parameters, is challenging.
To address these challenges, we propose a framework to integrate generative AI into a wellestablished GIS platform that leverages the advanced capabilities of LLMs to interact with
existing geoprocessing tools. To implement this framework, we developed a user-friendly plugin
that serves as a "Copilot" in the QGIS software, allowing users to perform spatial analysis
through natural language queries. This GIS Copilot provides a graphic user interface where users
can input a task (spatial problem), which the agent analyzes by breaking it into steps and
selecting suitable GIS tools. It then generates and executes Python code for the task to produce
the final result. By leveraging the existing capabilities of GIS platforms and enhancing them with
AI-driven reasoning, this framework aims to overcome the limitations of previous efforts and
contribute to the advancement of autonomous GIS research.

2

## Page 3

The key contributions of this study can be summarized as follows: 1) This study introduces
an extensible and generalizable framework for integrating LLMs into established GIS platforms,
setting a precedent for future developments in GIS Copilot and autonomous GIS across multiple
platforms (e.g., ArcGIS, GRASS GIS). 2) This study creates pathways for GIS accessibility and
adoption. By enabling natural language interaction and expanding GIS capabilities to non-expert
users, this research demonstrates how AI-driven systems can potentially transform geospatial
analysis in non-traditional GIS domains like public health, disaster response, and urban planning.
3) To the best of our knowledge, this is the first GIS Copilot deeply integrated into a wellestablished GIS platform, supporting diverse geospatial tasks while enhancing transparency, realtime reasoning, and expandability for external tools. While full autonomy is not yet achieved, it
brings us closer to realizing autonomous GIS systems for complex geospatial tasks with minimal
human intervention.
The remainder of this paper is organized in this manner. Section 2 reviews related work on
autonomous GIS and the integration of generative AI into geospatial tasks. Section 3 details the
proposed framework and prototype workflow. Section 4 presents the results from case studies
and evaluation of the performance of the Copilot at different complexity levels of cases. Section
5 discusses the key findings and Section 6 discusses the limitations and potential future research
directions. Finally, Section 7 concludes the paper.
2

Related Work

2.1

Autonomous GIS and the integration of generative AI into geospatial tasks

The recent advancement of generative AI, particularly LLMs such as GPT-4 (OpenAI, 2023),
Llama (Meta, 2024), and Gemini (Gemini Team and Google, 2023), has opened the avenue for
researchers to explore autonomous GIS (Li and Ning, 2023; Wang et al., 2024). Researchers
have leveraged LLMs to conceptualize and develop various autonomous GIS agents from
geospatial data retrieval (Ning et al., 2024) to geospatial information extraction (Crooks and
Chen, 2024) to spatial analysis and mapping (Mansourian and Oucheikh, 2024; Zhang et al.,
2024b). Among the pioneering studies in autonomous GIS is the work by Li and Ning (2023),
who developed a prototype named LLM-Geo to demonstrate the potential of AI-powered GIS to
perform various geospatial operations such as numerical aggregation, chart generation, and map
presentations in an autonomous manner using GPT-4 API. In another study, Zhang et al. (2024b)
developed GeoGPT, which integrates the capabilities of LLMs with GIS tools to enhance the
efficiency of geospatial operations, including data collection, processing, and analysis. By
utilizing the LangChain framework, the LLM interprets user requests, plans the necessary steps,
and sequentially executes relevant GIS tools from a predefined tool pool, encompassing tools for
data collection, spatial analysis, and cartographic visualization. Additionally, Lin et al. (2024)
recently proposed a framework designed to automate shapefile processing tasks using a multiagent approach.
Furthermore, several other studies have integrated LLMs into specific spatial tasks. For
instance, Tao and Xu (2023) explored the integration of ChatGPT into cartography to automate
and enhance map-making tasks. Their study conducted experiments on generating thematic and
mental maps by using natural language prompts in ChatGPT, which produced Python codes for
geospatial visualization. In a relevant study, Zhang et al. (2024a) introduce MapGPT, an LLMbased mapping framework that integrates GPT-4 with multiple mapping tools that allow users to
interact through natural language descriptions, simplifying the mapping process. Mai et al.
3

## Page 4

(2024) examine the potential of foundation models, including LLMs, for geospatial artificial
intelligence (GeoAI). They evaluate the performance of existing pre-trained LLMs on a range of
geospatial tasks, such as toponym recognition and location description, as well as multimodal
tasks like urban use classification and remote sensing image analysis. Xu et al. (2024) developed
a comprehensive benchmark to evaluate large language models (LLMs) on spatial tasks. While
these studies revealed the potential of generative AI in geospatial operations, one of the key
limitations is that these approaches have not fully integrated generative AI capabilities within
established GIS platforms.
2.2

Integrating generative AI into existing GIS platforms

Recent efforts have been made to integrate generative AI with established GIS platforms.
Ning et al. (2024) introduced an autonomous GIS agent framework and a QGIS plugin to
facilitate the automated downloading of geospatial data. While this study represents significant
progress, it focuses primarily on data retrieval rather than the broader spectrum of spatial
analysis tasks. QChatGPT (2023) is another LLM-based QGIS plugin, but its functionality is
currently limited to offering guidance on performing tasks rather than automating the tasks
themselves. IntelliGeo (2024) is a QGIS plugin that leverages LLMs to automate geospatial
workflows. It is designed to assist GIS professionals by automatically performing GIS operations
through two primary methods: generating PyQGIS scripts or creating graphical models.
Although promising, it is limited to generating general code, requiring users to manually
configure parameters in the code, reducing the automation level.
Recently, Mansourian and Oucheikh (2024) introduced ChatGeoAI which utilizes a finetuned Llama2 model to generate code that can be used to perform spatial tasks. While this
approach shares the goal of creating a platform that integrates LLM with GIS for geospatial
analysis tasks, our study differs in several ways. First, our study proposes a framework that
deeply integrates LLMs within a well-established platform like QGIS, leveraging the full range
of GIS tools. This allows the LLM to be more informed and produce more accurate and contextspecific code. Second, our framework is implemented through the development of a GIS Copilot
that is fully integrated into the GIS software itself to support a wide range of operations across
various data types, including vector, raster, and attribute data in tabular files, which offers greater
flexibility in geospatial analysis. Third, the design of the GIS Copilot enhances transparency by
providing explanations of the tool selection process and a real-time display of the reasoning
process and generated code, offering users insights into the execution steps. Additionally, our
framework is not limited to QGIS tools alone; it is designed to be expandable, allowing the
integration of external libraries and tools. For example, the widely used Python package,
seaborn, can be used for advanced charting, making certain tasks more efficient. Lastly, we
incorporate a self-correcting mechanism aimed at minimizing errors to enhance the system’s
autonomy and adaptability during task execution.
ESRI, a leading global provider of GIS software, has also taken advances toward integrating
generative AI into ArcGIS, introducing AI-enhanced tools aimed at improving geoprocessing
workflows (Crawford et al., 2024). This includes functionality that recommends suitable tools
for specific operations, providing guidance but not automating tasks. Additionally, ESRI’s AI
Assistant allows users to initiate GIS tasks through natural language inputs (ESRI, 2024a).
However, this development is still in early stage at the time of writing. ESRI also introduced
Copilot for Microsoft 365 that allows users to search, access maps, apps, and geospatial data
within ArcGIS for Teams (ESRI, 2024b). More rencently, NASA and Microsoft have
4

## Page 5

collaborated to develop Earth Copilot, an AI-driven tool designed to simplify and democratize
access to NASA's extensive Earth science data through natural language queries, such as
assessing the impact of specific events or environmental changes (Microsoft, 2024).
3

Methodology

3.1

Framework of the GIS Copilot

The GIS Copilot is designed to interact with existing GIS platform (e.g., QGIS) via graphic
user interface, GIS toolbox, and documents for the toolbox, to assist GIS users in conducting
geospatial data processing and analysis tasks. The framework consists of four core modules,
including data understanding, GIS interface interaction, code review/debugging, and tool
documentation. The GIS Copilot is informed by the data insights from the data understanding
module and leverages documentation of the geoprocessing tools contained in the spatial analysis
toolbox, to conduct spatial analyses. It automatically determines the most suitable geospatial
processing tools for various tasks, manages data processing workflows, and executes spatial
analysis operations. It generates the necessary code for the selected tools and uses the code
review and debugging module to automatically correct errors that may arise during execution.

Figure 1: Framework of the GIS Copilot
3.1.1 Spatial analysis toolbox
QGIS is a widely used open-source GIS software for geospatial data management, analysis,
and visualization. It offers tools from various algorithm providers, including QGIS native
algorithms, GDAL/OGR, GRASS GIS, SAGA GIS, and Orfeo Toolbox, supporting diverse
geospatial workflows. Additionally, its Python API, PyQGIS, allows users to automate tasks,
create custom plugins, and access full QGIS functionality, making it highly adaptable for
advanced spatial analysis and tool development (QGIS, 2024b).
The spatial analysis toolbox in this framework comprises both built-in and customized
geoprocessing tools. Built-in tools include QGIS algorithms, such as native geoprocessing
5

## Page 6

algorithms (e.g., 'native:buffer' for buffering and 'qgis:selectbyattribute' for attribute selection)
and external providers like GDAL (e.g., 'gdal:slope' for slope analysis). The customized
geoprocessing tools, developed using external libraries like GeoPandas, PySAL, and Matplotlib.
These customized tools enable statistical analysis (e.g., correlation analysis), customized charts
(e.g., bar plot, scatter plot), and thematic map generation, offering flexibility in spatial analysis
workflows.
3.1.2 Toolbox documentation
The GIS Copilot is equipped with documentation of QGIS tools, allowing it to generate
PyQGIS code for specific geoprocessing tasks. Derived from the QGIS help documents, the
toolbox documentation primarily consists of tool descriptions, parameters, and code examples,
serving as a guide for the agent in generating code for selected tools. For instance, the QGIS
native "Clip" tool requires parameters such as the Input Layer (the dataset to be clipped),
Overlay (the boundary layer for clipping), and Output File (the path for saving the clipped data)
(Appendix 1). By specifying these parameters and providing a code example, the system is able
to generate more accurate and reliable code for the task.
In our current implementation, 390 native QGIS and GDAL tools have been systematically
compiled with reference to the resources available on the official QGIS documentation website
(QGIS, 2024b). In addition, this framework is not limited to QGIS tools and is designed to be
extensible in a plug-and-play style to allow users to add new customized tools to meet specific
tasks. For example, a tool used for performing kernel density estimation can be customized using
geopandas, scipy, and rasterio Python libraries and registered to the GIS Copilot (Appendix 2).
3.1.3 Data understanding module
The data understanding module enables the agent to extract and interpret the structure and
attributes of spatial data before being used for any analysis. It functions similarly as the initial
step a human analyst would take when approaching a spatial analysis task -understanding the
data to be analyzed. Specifically, it collects a wide range of critical information of the data for
spatial analysis, such as file format, field names of the attribute table, coordinate reference
system, data extent, and raster resolution. This information provides the GIS Copilot with a
thorough overview and understanding of the data inputs, which guides it in selecting appropriate
tools for the task and the right attributes for performing geospatial operations. As a result, users
are not required to specify data details such as field names in their task requests, making the
Copilot more user-friendly.
3.1.4 Code review/debugging module
The code review/debugging module is an essential component designed to enhance the
reliability and accuracy of generated code. This module enables the GIS Copilot to actively
review the generated code and monitor the execution of the generated code in real-time to
capture any errors that may arise. Upon detecting an error, it attempts to correct the error
automatically and re-generate the code for execution. This self-debugging functionality is
iterative, allowing for continuous refinement and improvement of the code to increase the
chances of successful execution.
3.1.5 GIS interface interaction
The GIS interface interaction module enables the GIS Copilot to engage directly with the
host GIS’ (QGIS) graphic user interface. It allows the Copilot to perform actions such as
6

## Page 7

dynamic loading and data handling within the GIS software. For example, data layers that users
load into GIS software can be automatically accessed by the Copilot. Additionally, results
generated from the Copilot are directly reloaded into the host GIS, which allows immediate
visualization and further processing or manipulation by the user.
3.2

Workflow of the GIS Copilot

The GIS Copilot is implemented as a plugin within QGIS. It interprets user requests in
natural language and translates them into executable geoprocessing commands. As shown in
Figure 2, the overall workflow begins by breaking down the user’s task into detailed steps. Once
the task is well understood, the system identifies the appropriate geoprocessing tool(s) from a
wide range of options, including QGIS native tools, GDAL, or customized tools.The tools are
selected based on the steps analyzed during the task breakdown to ensure each step of the
process is addressed by the most suitable tool. Based on the selected tool (s), the system
generates executable Python code that is specifically designed to solve the spatial task.
Throughout these steps, the system is guided by a set of predefined instructions, automatically
generated metadata and a comprehensive tool list to ensure reliable task analysis, tool selection,
and code generation. Finally, the code is executed, and the results are either loaded as map layers
into QGIS or presented as reports including tables and charts.

Figure 2: Workflow of the GIS Copilot
3.2.1 Task analysis and tool selection
When a user submits a spatial query in natural language, the first step is that the agent
processes the request to understand the underlying spatial problem. After the initial
interpretation, the agent performs a task breakdown to determine what is needed to achieve the
intended outcome. For instance, a user may request, "Identify all residential areas within a 5minute driving distance from hospitals." The agent first identifies the spatial entities involved residential areas, hospitals, and the concept of a 5-minute drive. Based on these insights, it
matches the request to a set of geoprocessing tools available within the spatial analysis toolbox.
The decision-making process for selecting the appropriate tool involves considering several
factors, such as the nature of the data (e.g., vector or raster), the geographic projection, and the

7

## Page 8

data structure (e.g., polygons, lines). Additionally, any user preferences specified during the
query, such as the choice of tools or specific processing techniques, are taken into account.
3.2.2 Code generation and parameter setting
Once the appropriate tools are selected, the next step in the workflow is the code generation
phase. The agent generates Python code to execute the operation based on the selected tools. The
generation process is guided by predefined documentation for each tool, which includes usage
guides, parameter requirements, and sample code templates so that the generated code is wellformed and ready for execution. To personalize the generated code to fit the user’s requirements,
the agent adjusts the parameters to align with the task’s specific details. For instance, suppose a
user request is to “select counties with a population greater than 50,000”. The agent customizes
the code based on the user’s specific requirement by setting the filter condition to “Population” >
50,000, where “population” is assumed to be the relevant attribute name.
3.2.3 Execution and visualization of results
After generating the code, the next step involves executing it to perform the spatial analysis.
This stage is facilitated by an execution and self-debugging module, which oversees the entire
process. The generated code is executed directly within the host GIS environment, allowing the
spatial analysis to be performed without leaving the QGIS interface. Depending on the nature of
the task, results can take various forms: the outputs of geoprocessing tasks, such as buffer zones,
intersected layers, or reclassified raster layers, are loaded and displayed directly in QGIS as map
layers, where they can be further analyzed, visualized, or exported. Analytical results that
involve summaries, charts, attribute statistics, or calculated metrics are displayed within the
plugin interface as tables, images, or textual reports. When appropriate or requested in the tasks,
the plugin may also generate visualizations, such as bar charts, histograms, or other graphical
representations to help users interpret the results. If an error is encountered during execution, the
self-debugging module is activated. This module reviews the code, identifies the errors, makes
necessary corrections, and re-executes the revised code.
3.3

User interface design

The graphic user interface of this GIS Copilot comprises six main tabs: Request Page,
Generated Code, Geoprocessing Workflow, Reports, Settings and Help. The Request Page is the
main interface where users can enter their requests. It includes key features like an AI-generated
code displayed in real-time, an information panel showing the agent's status, a request box for
user requests, and paths for datasets loaded into QGIS. To enable seamless integration with
QGIS, users can select datasets for analysis directly from the QGIS layer panel by checking the
layers they want to include and unchecking those to exclude. The Generated Code tab enables
users to manually execute the code generated by the agent and make edits as needed. This tab
also provides a platform to load saved code from the local machine or save generated code for
future use. The geoprocessing workflow tab illustrates the steps involved in completing the
user’s request in a visual flow. Reports tab allows users to view outputs like charts, plots, and
statistical summaries. The Settings tab lets users configure the plugin, such as setting API keys,
selecting the AI model, and defining the default workspace where results are saved. Help tab
offers the users the details on how to use the plugin.

8

## Page 9

Figure 3: The graphic user interface of the GIS Copilot
4

Case Studies

To demonstrate the capabilities of the GIS Copilot, cases are categorized into three levels of
complexity: basic, intermediate, and advanced.
4.1

Basic level tasks

At this level, the tasks are straightforward, involving a single tool along with one (or
occasionally two) data layers. The agent is expected to perform a straightforward operation that
usually requires a single step, such as calculating the area of polygons or selecting features based
on attributes.
4.1.1 Health facilities coverage zone in Washington D.C., USA
This case involves creating service zones around health facilities in Washington D.C, United
States. The input data was a vector layer of health facilities (hospitals, clinics, and pharmacies)
obtained from OpenStreetMap. In this task, the agent was prompted to create 2,000-foot zones
around each health facility to identify areas of service coverage (Figure 4). The agent
successfully selected the appropriate spatial analysis tool (the buffer tool) and generated
executable code, which includes setting the required parameters (e.g., distance) based on the user
query and executing the operation.

9

## Page 10

Figure 4: Health facilities coverage zone (Task: Can you please create 2000-feet zones around
each health facilities in Washington DC to identify areas of service coverage?)
4.1.2 Generating contour lines from the Digital Elevation Model (DEM)
In this case, the agent is tasked with generating contour lines from a Digital Elevation Model
(DEM) dataset, a raster data layer that represents terrain elevation. This is a foundational spatial
analysis task that is frequently used in geographic studies, such as topographical mapping,
environmental modeling, and landscape visualization. The agent selected the tool gdal:contour
from the available geoprocessing tools within the system. This tool is specifically designed to
convert elevation data (raster) into contour lines (vector), based on user-defined intervals. In
our case study, the output in vector format is shown in Figure 5.

10

## Page 11

Figure 5: Generating contour lines from DEM (Task: Generate contour lines from the DEM of
Puerto Rico with a 50-meter interval.)
4.1.3 Selection of high population counties in the US.
This case demonstrates attribute query by selecting the US counties with a population
exceeding 50,000. The input dataset is a single vector layer that contains the population of all
counties in the contiguous US states. In response to the task, the agent effectively identified the
correct tool (extract by attribute) to filter the data. The agent then generated the necessary

11

## Page 12

executable code, which included setting the population threshold and applying the filtering
operation based on the specified condition (Figure 6).

Figure 6: Selection of high population counties in the contiguous U.S. (Task: Select the USA
counties that have more than 50,000 population.)
4.1.4 Extracting land cover data of Pennsylvania
This case focuses on extracting land cover data for Pennsylvania from a larger dataset covering
the contiguous US. The input data includes land cover raster data from the National Land Cover
Database (NLCD) and a shapefile containing the boundary of Pennsylvania. The agent accurately
selected the appropriate tool (the GDAL Clip Raster by Mask Layer tool) and generated the
executable code, configuring parameters such as the input layer, output path, and clipping
settings. The agent was able to produce the clipped raster layer showing the land cover specific
to Pennsylvania (Figure 7). The result provides a detailed view of various land cover categories
within the state’s boundary.

12

## Page 13

Figure 7: Extracting land cover information of Pennsylvania. (Task: Clip the land cover data of
the USA to the Pennsylvania boundary.)
4.2

Intermediate level tasks

At this level, tasks become more complex and involve multiple steps and tools. The agent is
guided with specific instructions or a list of steps to perform the task. Although the steps are
outlined, the agent still needs to generate the correct code for each step and link them together to
perform the analysis. The focus here is to test the agent’s ability to follow a given general
workflow while managing more than one process.
4.2.1 Zonal statistics of average elevation for counties in South Carolina
In this case, the agent is tasked with analyzing the average elevation for each county in South
Carolina (SC) based on the DEM. This involved a series of geoprocessing steps: clipping the
DEM to the boundary of SC, generating a histogram of the clipped DEM’s pixel values,
calculating zonal statistics, and creating a choropleth map. The input consists of three data
layers: a DEM covering a region larger than SC and two vector layers containing SC's boundary
and all SC counties.
The results of the request are shown in Figure 8. The choropleth map generated by the agent
clearly displays the average elevation values, with darker shades representing higher elevations.
Also, the histogram generated by the agent illustrates the distribution of pixel values from the
13

## Page 14

clipped DEM. Additionally, the geoprocessing workflow diagram illustrates the steps of the
analysis.

Figure 8: Zonal Statistics of average elevation for counties in South Carolina (Task: Perform the
following task: 1) Clip the DEM to SC boundary and load the clipped DEM. 2) Show me the
histogram for the clipped DEM pixel values. 3) Generate the zonal statistics for every county in
SC, focusing on average elevation. 4) Finally create a choropleth map showing the average
elevation of each county in SC.)

14

## Page 15

4.2.2 Richland County terrain analysis
In this case, the agent was tasked with performing a detailed terrain analysis for Richland
County, SC, by merging four DEM tiles obtained from the US Geological Survey (USGS) and
Shuttle Radar Topography Mission (SRTM) dataset (USGS, 2024). The generated geoprocessing
workflow shows the sequence of steps to complete the task. The workflow began by merging the
four individual DEMs to create an elevation model covering the area of interest. Once merged,
the agent calculated multiple terrain characteristics, including slope, aspect, hillshade, Terrain
Ruggedness Index (TRI), and Topographic Position Index (TPI). The outputs of each analysis
step were displayed, with each terrain attribute as a separate map (Figure 9).

15

## Page 16

Figure 9: Richland County raster analysis. (Task: Merge the four DEMs into a single raster and
perform terrain characteristic analysis for Richland County, including slope, aspect, hillshade,
terrain ruggedness index (TRI), and topographic Position Index (TPI).)
4.2.3 County-level obesity risk behavior index analysis
This task involves the calculation of an obesity risk behavior index across all counties in the
contiguous US. Two data layers – a shapefile containing the boundaries of all counties and a
CSV file containing the rate of visits to different places such as convenience stores, limitedservice restaurants, sport centers, fitness centers, and parks. The agent was able to join the
attributes to the shapefile and select the fields needed for the analysis without any instruction
16

## Page 17

from the user using the data understanding module. The thematic map and the geoprocessing
workflow generated by the agent is presented in Figure 10.

Figure 10: County-level obesity risk behavior index analysis (Task: Generate an obesity risk
behavior index of each county in the contiguous US by analyzing the rate of visits to unhealthy
food retailers (such as convenience store, alcoholic drinking places, and limited service
restaurant) and the visit rate to places that support physical activity (e.g., sports centers, parks,
fitness centers). Visualize the results in a thematic map to highlight the obesity risk behavior
index across counties.).
4.3

Advanced level tasks

In the advanced level, tasks are multistep, and the agent is expected to determine the
appropriate steps independently without explicit instructions, to devise the best approach for
achieving the desired outcome. In other words, tasks are more natural in nature presenting the
agent of “what” the users want with limited guidance on “how” to do it. The agent must select
the right tools, generate the necessary code, and execute the entire process independently.
4.3.1 Fast-food accessibility and obesity correlation analysis for Pennsylvania counties
This operation involves analyzing and visualizing the fast-food accessibility score for each
county in Pennsylvania and performing a correlation analysis between the fast-food accessibility
score and the prevalence of obesity. The agent’s workflow began by calculating the fast-food
accessibility score for each county based on the number of fast-food restaurants per capita by
performing a spatial join operation. This was followed by generating a thematic map that
displays counties with higher accessibility scores in darker shades of blue. Next, the agent
analyzed the correlation between county-level obesity rates and fast-food accessibility scores.
The results of this analysis are shown in Figure 11, where a scatter plot with a regression line
highlights the relationship between fast-food accessibility and obesity rates across the state. The
agent successfully managed the multistep process, calculating accessibility scores to perform
correlation analysis, and visualizing the results in both a thematic map and a scatter plot. It

17

## Page 18

should be noted that all the specific fields used in the analysis were automatically selected by the
agent without explicit user guidance enabled by the data understanding module.

Figure 11: Fast-food accessibility analysis for each county in Pennsylvania. (Task: Could you
analyze and visualize the fast food accessibility score for each county based on the number of
fast food restaurants and population using a thematic map with blue graduated colors. Then,
analyze the correlation between the county-level obesity rate and the fast food accessibility score
by drawing a scatter plot with a regression line.). Fast food restaurants data was downloaded
from OpenStreetMap. The population data (2022) was retrieved from the US census.
4.3.2 Spatial distribution of COVID-19 cases across US counties
This task asks, "Could you show the spatial distribution of the COVID-19 cases across US
counties? " This request involves visualizing the spatial distribution of COVID-19 cases across
US counties. The agent was provided with two datasets: shapefile of US county boundaries
obtained from the US Census Bureau (2024) and a CSV file containing COVID-19 data as of
18

## Page 19

December 2020, obtained from the New York Times (2023). The analysis involved joining the
attribute contained in the CSV data with the shapefile to create a thematic map that shows the
COVID-19 cases across all the counties in the US. The agent successfully completed the task,
automatically identifying the common fields, "GEOID" and "FIPS", for the join operation. It also
selected the "cases" field from the COVID-19 dataset to generate the thematic map. The
geoprocessing workflow diagram generated by the agent and the resulting thematic map is
shown in Figure 12. Counties with higher numbers of COVID-19 cases are represented by darker
shades of blue on the map.

Figure 12: Spatial distribution of COVID-19 cases in the USA. (Task: Could you show the
spatial distribution of the COVID-19 cases across US counties?)
4.3.3 Generating the Normalized Difference Vegetation Index (NDVI) from satellite
imageries
In this case, the agent was tasked with generating the Normalized Difference Vegetation
Index (NDVI) for the city of Akure, Nigeria using multispectral satellite imagery. The request is
"Generate the Normalized Difference Vegetation Index (NDVI) of Akure from these satellite
imageries". The input data comprises a shapefile of the Akure boundary and Landsat 8 satellite
products from the USGS, which includes multiple image bands. The agent demonstrated its
capability by automatically identifying and selecting the correct bands, specifically the NIR and
red bands, from the multispectral imagery. It then used these bands and applied the correct
formula to generate the NDVI layer. The output was visualized as a raster map. The agent
successfully managed the entire process, from band selection to calculation to ensure the correct
bands were used and that the NDVI was calculated accurately (Figure 13). Note that the initial
raster map generated by the agent used a black-and-white color ramp for symbology. The
symbology was manually adjusted to enhance visualization in order to provide a clearer
representation of the vegetation distribution in Akure, where areas of dense vegetation are
represented by higher NDVI values, as shown in green, while shades of blue represent lower
19

## Page 20

NDVI values. This example shows the agent’s ability to handle satellite imagery data and
perform key calculations with minimal user input.

Figure 13: Generating the Normalized Difference Vegetation Index (NDVI) of Akure. (Task:
Generate the Normalized Difference Vegetation Index (NDVI) of Akure from these satellite
imageries.).
4.4 Performance evaluation
The performance of the GIS Copilot was assessed systematically using 110 tasks across three
levels of complexity: basic, intermediate, and complex. Each level consisted of a set number of
tasks, selected according to predefined criteria for task complexity (in Sections 4.1, 4.2, and 4.3).
This structured approach ensured that the chosen tasks represented each complexity level to
provide a balanced and meaningful evaluation framework. While definitions of complexity may
vary, the selected tasks align closely with the GIS Copilot’s intended functionality and scope.
Success rates were recorded at each stage, tracking tasks completed on the first attempt as
well as those required multiple attempts. Tasks that remained unsuccessful after three attempts
were categorized as failures. The overall accuracy is determined by calculating the percentage of
successful cases. As shown in Table 1, with 60 cases at the basic level (Appendix 3), the success
rate recorded was 95%; among 30 intermediate-level tasks (Appendix 4), a success rate of 80%
was observed, and for the advanced level, which included 20 cases (Appendix 5), the success
rate was 75%.
20

## Page 21

Table 1: Performance evaluation of the GIS Copilot
Level of
complexities
Basic
Intermediate
Advanced

Total count
of tasks
60
30
20

Count of successful cases
First
attempt
52
13
10

Second
attempt
3
4
4

Third
attempt
8
1

Count of
failed cases

Overall
success rate

5
5
5

92 %
83 %
75 %

We further evaluated the performance by analyzing the reasons behind the failed cases to
understand the underlying issues. Overall, tool selection was accurate, as the appropriate tools
were consistently chosen for each task. However, most of the failed cases are attributed to the
following three major issues described below.
•

Incorrect parameter assignment: The most frequent cause of failure involved parameter
setting errors. Despite selecting the correct tool, some tasks failed due to incompatible or
incorrectly assigned parameters, leading to code execution issues. For example, when
attempting to identify areas suitable for camping, the agent was instructed to select locations
where the aspect of the area was greater than 100 and the distance to the closest road did not
exceed 1000 meters (Case 20 in Appendix 5). To achieve this, the agent used the
gdal:proximity tool to calculate distances to the nearest roads. However, the task failed
because the tool requires a raster input, while the agent assigned a vector layer as the input
data.

•

Field name mismatches and data compatibility: Another common issue arose from
mismatches in field names during data joins, particularly when joining CSV files with
shapefiles. Shapefiles often truncate field names to 10 characters, causing discrepancies that
the agent did not account for, leading to calculation errors. For example, when tasked with
calculating the population living in block groups containing hazardous waste sites, the agent
needed to join a CSV file containing population data to a shapefile representing block
groups. However, the agent encountered issues because the shapefile truncated longer field
names to 10 characters. This caused the field names in the shapefile to differ from those in
the CSV, leading to a failed join and, consequently, leading to a "field name error".

•

Projection issue: During testing, it was observed that the agent frequently omitted essential
reprojection steps unless specifically instructed. This oversight led to misaligned spatial data,
affecting the accuracy of the results, particularly in tasks that required consistent coordinate
systems across layers. For instance, when tasked with clipping an image using the extent of a
shapefile where the shapefile and the image were in different coordinate systems, the agent
did not reproject the shapefile to match the coordinate system of the image, the resulting clip
operation was misaligned, leading to an error (Case 27 in Appendix 4).

5

Discussion

This study proposes a novel framework for integrating generative AI (LLMs) into established
GIS platforms, using QGIS as a case study. Based on this framework, we implemented a GIS
Copilot through which GIS users interact with the software with natural language. A key feature
of this GIS Copilot is the extensive range of tools included, covering a broad spectrum of
geoprocessing functions such as vector and raster analyses. Additionally, the framework is
21

## Page 22

designed to be extensible by allowing GIS users to add custom tools following a predefined
template. This extensibility ensures that the Copilot remains adaptable to user needs and the
continuous development of new GIS tools and analyses. This work aligns with the increasing
recognition of the potential for AI-driven systems to automate and streamline geoprocessing
workflows. By automating these processes, the framework simplifies spatial analysis, making
GIS functionalities more accessible to both expert and non-expert users.
This GIS Copilot responds to the previous work of Li and Ning (2023), who envisioned the
need for a copilot-style system in GIS to enhance automation and interaction with geospatial
data. They demonstrated the potential for LLMs to autonomously generate geoprocessing
workflows and emphasized the importance of integrating these capabilities directly into existing
GIS software to unlock their full potential. By implementing a Copilot system within QGIS, this
study illustrates how LLMs can be used to generate executable spatial analysis algorithms using
existing well-developed GIS tools. A significant benefit of Copilot style integration with GIS
platform is that users have direct interaction with the agent directly within the GIS environment,
allowing them to load and select datasets, visualize results and select between manual operations
and agent-driven workflows based on their preferences. This flexibility enables users to combine
traditional manual GIS processes with the efficiency of AI-driven analysis, resulting in a hybrid
approach. For instance, users can load datasets into QGIS and perform analyses, generate results
by the agent and further perform analyses using either the Copilot or manual methods.
In evaluating the performance of the GIS Copilot, we analyzed its success rate for over 100
tasks across three levels of complexity: basic, intermediate, and advanced level. At the basic
level, tasks involved straightforward operations on one or two data layers, such as spatial
buffering, calculating areas or filtering features based on attributes. The agent demonstrated high
accuracy in selecting the appropriate tools and generating the necessary code. The reliability of
the GIS Copilot at this level highlights its competence in automating foundational tasks with
minimal intervention, offering an important utility for speeding up routine geospatial operations.
At the intermediate level, the tasks require multistep which are described for the agent. Here, the
agent not only needed to correctly select tools but also generate and execute the code in
sequence. In these scenarios, the agent showed strong performance in generating geoprocessing
workflows based on the multistep task description and managing the dependencies between
different steps. The success in these tasks suggests that the agent can effectively operate as an
assistant to handle more involved geospatial workflows, thereby reducing the need for users to
do step-by-step manual coding. The advanced level tasks involve the highest complexity, where
the tasks are more natural in nature, presenting the agent of “what” the users want with limited
guidance on “how” to do it. Here, the agent needs to understand and reason the question and
determine the geoprocessing workflow autonomously. This required the agent to interpret the
natural language instructions, decide on an appropriate series of actions, select the correct tools,
and execute the entire process without explicit guidance. While the agent showed promise at this
level, especially in the tool selection and code generation, the success rate for these complex
tasks was lower than simpler ones.
Explainability and trustworthiness are two critical concerns in generative AI applications,
including GIScience (Tlili et al., 2023; Kang et al.,2024). While LLMs can generate impressive
responses, their “black box” nature makes it difficult for users to understand how specific
outputs are produced. Without clear explanations of how outputs are generated, users may be
reluctant to fully adopt these models, especially when they play a significant role in data driven
22

## Page 23

analyses and recommendations. To reduce these concerns, this GIS Copilot has been designed to
enhance transparency at every step. Unlike traditional black-box models, the Copilot clearly
presents each stage of the process, including tool selection and code generation, with generated
code displayed in real time. Additionally, the generated code can be further edited and executed
manually as needed. This approach allows users to inspect and understand each action taken by
the Copilot, so that they can trace how results are achieved. Users are encouraged to review the
generated code and results actively, rather than relying on them blindly. This approach highlights
the collaborative nature of a “copilot” system that supports rather than replaces expert decisionmaking.
6

Limitations and Future Work

The GIS Copilot shows promising performance across the three levels of task complexities;
however, certain issues were observed. These challenges point to potential areas for
improvement and future research directions.
6.1

The need for a data validation module to reduce tool and parameter mismatch

The GIS Copilot shows potential in handling tasks of varying complexity, but issues like
incorrect parameter assignment were observed, hindering its performance. For instance, the agent
occasionally assigns vector data to parameters that require raster input. A good example of such
is the gdal:proximity tool, where the input layer should be raster; however, the agent assigns a
vector layer provided by the user without first converting it to raster, resulting in code failure.
Improving the alignment between data types and tool requirements is needed to enhance the
agent’s reliability. One way this can be achieved is by integrating a data validation module that
crosses-references each parameter with the data type required by the selected tool so that the data
will be converted automatically even if there is a mismatch.
6.2

Expanding LLMs knowledge in GIScience fundamentals

LLMs like GPT-4o, while capable of general-purpose reasoning, exhibit limited foundational
knowledge in GIScience, particularly in domain-specific requirements such as the need for data
reprojection under certain conditions. During the advanced level testing, it was observed that the
agent frequently omitted reprojection steps unless specifically instructed. This limitation affects
the usability of the Copilot, especially for non-expert users who may be unaware of when or why
reprojection is needed. These users may, therefore, unknowingly produce analyses based on
misaligned or incorrectly scaled spatial data, which can lead to incorrect interpretations and
reduced confidence in the results. Additionally, the agent demonstrated a lack of understanding
of some specific GIS tools, especially some GDAL tools. Even with the integration of these
tools’ documentation in the framework, the agent still struggles to select appropriate functions or
set accurate parameters for some tools, leading to execution errors. This may be due to
limitations in prompt length. Some tool documentation lengths may exceed the standard prompt
limit. To address these issues, future work could explore approaches like Retrieval-Augmented
Generation (RAG) (Lewis et al., 2020), which may address the length constraints within tool
documentation, by allowing the LLM to query and retrieve specific and relevant sections of
documentation as needed.
6.3

Building an experience-based knowledge system

The agent’s current knowledge is mostly derived from Internet sources, which lack the depth
of practical GIS experience necessary for accurately performing specialized tasks. For instance,
23

## Page 24

the agent may not recognize that data types in table joins must align across columns, such as
ensuring that strings match with strings and integers with integers, or that buffer distances should
be expressed in metric units rather than degrees. Without this foundational understanding, the
agent is prone to errors that are easily detectable by GIS professionals yet may remain
undetectable by less or non-experienced users. To address this issue, implementing an
experience-based knowledge system could improve the agent’s practical understanding and
adaptability. Such a system would act as a database that accumulates instances of errors and their
solutions during agent-user interactions. Over time, this “experience database” would function
similarly to a repository of case-based learning, enabling the agent to recognize recurring issues,
learn corrective actions, and apply these solutions autonomously in future tasks. This approach is
one way of achieving the “self-growing” goal of an autonomous GIS, allowing the agent to
continuously evolve and improve based on accumulated experience. For example, if the agent
encounters a table join error due to incompatible data types, it will reference its experience
database to identify and implement a solution, such as converting one of the columns to the
appropriate type.
6.4

Integration of a prompt-generation module

In this study, spatial tasks were provided directly to the agent as prompts. However, these
task descriptions are not necessarily the appropriate prompt as they may often lack the structure
and detail required, especially in technical contexts. For instance, a simple task description may
omit key parameters or methodological details that might help the agent to perform more
accurately. To address this, one potential approach is to introduce an intermediate step that
refines or rephrases task descriptions into optimized prompts. This step could involve analyzing
the initial task description, extracting essential elements such as data type specifications, required
tool parameters, and expected outcomes, and transforming them into a more detailed, structured
prompt specific to different types of geospatial tasks. By providing a richer context, the refined
prompt would guide the agent in selecting appropriate tools and parameters to ensure greater
alignment with the intended analysis. For instance, it could recognize when a task requires
specific spatial projections and then structure the prompt appropriately.
6.5

Integration with a geospatial data retrieval agent

To advance the GIS Copilot toward full autonomy, integrating an agent capable of retrieving
needed geospatial data is essential. An autonomous data retrieval agent would allow the Copilot
to access and use relevant datasets directly, thereby reducing user input requirements and
improving efficiency, especially for non-experts who may lack familiarity with data sourcing.
Recently, Ning et al. (2024) introduced an agent for retrieving geospatial data from different
sources, implemented as a QGIS plugin. Integrating such an agent could help the Copilot access
to the data needed for analysis without requiring the user to supply it, which could bring the GIS
Copilot closer to a fully spatial analysis agent.
6.6

Exploring the integration of open-source LLM models

In this study, OpenAI GPT has been used as the primary language model to power the GIS
Copilot to demonstrate the potential of the proposed approach. However, integrating open-source
LLM models such as Meta’s LlaMA (Meta, 2024) could offer notable advantages, especially in
terms of customization and accessibility, such as fine-tuning on GIS-specific tasks to further
improve performance and alignment with specialized geospatial needs. Future studies could
24

## Page 25

explore the integration of these open-source models into the GIS Copilot to provide a more
accessible and customizable alternative to commercial models.
7

Conclusions

The integration of generative AI into GIS represents a significant advancement in automating
spatial analysis tasks. This study presents a framework for integrating LLMs directly into
existing GIS platforms. The framework was implemented as a GIS Copilot in the QGIS
environment. Through case studies across different levels of task complexity, the GIS Copilot
proved effective in automating basic and intermediate geospatial tasks, reducing the need for
manual operations and coding. While the Copilot performed well in these simpler tasks,
challenges remain in achieving full autonomy for more advanced and multistep processes
without explicitly telling it “how”.
Despite the limitations, the GIS Copilot represents a promising step toward the development
of fully autonomous GIS and opens avenues for future exploration of AI-driven GIS solutions in
GIScience. This study contributes to the broader vision of autonomous GIS, where AI-powered
agents can autonomously perform spatial analysis to democratize access to geospatial analysis,
transforming how users engage with geospatial data and spatial problems. As advancements in
generative AI capabilities continue, further research will focus on improving the Copilot’s
performance in handling complex workflows, enhancing its error-correction mechanisms, and
expanding its adaptability to other GIS platforms.
Data and code availability statement: The source code for the GIS Copilot is available on
GitHub at https://shorturl.at/vRcm6. The GIS Copilot can be downloaded from the official QGIS
plugin page at https://plugins.qgis.org/plugins/SpatialAnalysisAgent-master and installed by
following the instructions provided in the GIS Copilot User Manual. The datasets used for
testing alongside with the testing cases can be accessed through https://shorturl.at/bI4Ep.
References
Akinboyewa, T., Ning, H., Lessani, M. N., & Li, Z. (2024). Automated floodwater depth
estimation using large multimodal model for rapid flood mapping. Computational Urban
Science, 4(1), 12. https://doi.org/10.1007/s43762-024-00123-3
Crooks, A., & Chen, Q. (2024). Exploring the new frontier of information extraction through
large language models in urban analytics. Environment and Planning B: Urban Analytics
and City Science, 51(3), 565–569. https://doi.org/10.1177/23998083241235495
Esri. (2024a). ArcGIS Desktop [Computer software]. https://pro.arcgis.com/. Last accessed on
11/9/2024
Esri. (2024b). ArcGIS for Microsoft 365. https://doc.arcgis.com/en/microsoft365/latest/teams/copilot-search-workflow.htm. Last accessed on 11/9/2024
Gemini Team, & Google. (2023). Gemini: A Family of Highly Capable Multimodal Models
(tech. Rep.). https://storage.googleapis.com/ deepmindmedia/gemini/gemini_1_report.pdf. Last accessed on 11/9/2024
GRASS GIS. (2024). Http://grass.osgeo.org [Computer software]. https://grass.osgeo.org/. Last
accessed on 11/9/2024

25

## Page 26

Hao, Y., Qi, J., Ma, X., Wu, S., Liu, R., & Zhang, X. (2024). An LLM-Based Inventory
Construction Framework of Urban Ground Collapse Events with Spatiotemporal
Locations. ISPRS International Journal of Geo-Information, 13(4), 133.
https://doi.org/10.3390/ijgi13040133
Hu, Y., Mai, G., Cundy, C., Choi, K., Lao, N., Liu, W., Lakhanpal, G., Zhou, R. Z., & Joseph, K.
(2023). Geo-knowledge-guided GPT models improve the extraction of location
descriptions from disaster-related social media messages. International Journal of
Geographical Information Science, 37(11), 2289–2318.
https://doi.org/10.1080/13658816.2023.2266495
Kang, Y., Gao, S., & Roth, R. E. (2024). Artificial intelligence studies in cartography: a review
and synthesis of methods, applications, and ethics. Cartography and Geographic
Information Science, 1-32.
Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih,
W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks. In H. Larochelle, M. Ranzato, R. Hadsell, M. F.
Balcan, & H. Lin (Eds.), Advances in Neural Information Processing Systems (Vol. 33,
pp. 9459–9474). Curran Associates, Inc.
Li, Z., & Ning, H. (2023). Autonomous GIS: The next-generation AI-powered GIS. International
Journal of Digital Earth, 16(2), 4668–4686.
https://doi.org/10.1080/17538947.2023.2278895
Lin, Q., Hu, R., Li, H., Wu, S., Li, Y., Fang, K., Feng, H., Du, Z., & Xu, L. (2024).
ShapefileGPT: A Multi-Agent Large Language Model Framework for Automated
Shapefile Processing (arXiv:2410.12376). arXiv. http://arxiv.org/abs/2410.12376
Mai, G., Huang, W., Sun, J., Song, S., Mishra, D., Liu, N., Gao, S., Liu, T., Cong, G., Hu, Y.,
Cundy, C., Li, Z., Zhu, R., & Lao, N. (2024). On the Opportunities and Challenges of
Foundation Models for GeoAI (Vision Paper). ACM Transactions on Spatial Algorithms
and Systems, 10(2), 1–46. https://doi.org/10.1145/3653070
Microsoft. (2024, November 14). From questions to discoveries: NASA’s new Earth Copilot
brings Microsoft AI capabilities to democratize access to complex data. Microsoft Blogs.
https://blogs.microsoft.com/blog/2024/11/14/from-questions-to-discoveries-nasas-newearth-copilot-brings-microsoft-ai-capabilities-to-democratize-access-to-complex-data/
Mansourian, A., & Oucheikh, R. (2024). ChatGeoAI: Enabling Geospatial Analysis for Public
through Natural Language, with Large Language Models. ISPRS International Journal of
Geo-Information, 13(10), 348. https://doi.org/10.3390/ijgi13100348
Meta. (2024). Llama 3.2. https://www.llama.com/
Mooney, P., Cui, W., Guan, B., & Juhász, L. (2023). Towards Understanding the Geospatial
Skills of ChatGPT: Taking a Geographic Information Systems (GIS) Exam [Preprint].
Earth Sciences. https://doi.org/10.31223/X5P38P
New York Times. (2023). Coronavirus (Covid-19) Data in the United States (Archived).
https://github.com/nytimes/ covid-19-data. Last accessed on 11/9/2024
Ning, H., Li, Z., Akinboyewa, T., & Lessani, M. N. (2024). An Autonomous GIS Agent
Framework for Geospatial Data Retrieval (Version 2). arXiv.
https://doi.org/10.48550/ARXIV.2407.21024
26

## Page 27

OpenAI, Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D.,
Altenschmidt, J., Altman, S., Anadkat, S., Avila, R., Babuschkin, I., Balaji, S., Balcom,
V., Baltescu, P., Bao, H., Bavarian, M., Belgum, J., ... Zoph, B. (2023). GPT-4 Technical
Report (Version 6). arXiv. https://doi.org/10.48550/ARXIV.2303.08774
OpenStreetMap. (n.d.). OpenStreetMap. Retrieved October 18, 2024, from
https://www.openstreetmap.org/
QGIS. (2024a). Http://qgis.org [Computer software].Last accessed on 11/9/2024
QGIS. (2024b). QGIS Documentation v3.34.
https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/index.html. Last
accessed on 11/9/2024
Tao, R., & Xu, J. (2023). Mapping with ChatGPT. ISPRS International Journal of GeoInformation, 12(7), 284. https://doi.org/10.3390/ijgi12070284
Tlili, A., Shehata, B., Adarkwah, M. A., Bozkurt, A., Hickey, D. T., Huang, R., & Agyemang, B.
(2023). What if the devil is my guardian angel: ChatGPT as a case study of using
chatbots in education. Smart learning environments, 10(1), 15.
US Census Bureau. (2024). TIGER/Line Shapefiles.
https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
USGS. (2024). Shuttle Radar Topography Mission (SRTM).
https://www.usgs.gov/publications/shuttle-radar-topography-mission-srtm
Wang, S., Hu, T., Xiao, H., Li, Y., Zhang, C., Ning, H., ... & Ye, X. (2024). GPT, large language
models (LLMs) and generative artificial intelligence (GAI) models in geospatial science:
a systematic review. International Journal of Digital Earth, 17(1), 2353122.
Xu, L., Zhao, S., Lin, Q., Chen, L., Luo, Q., Wu, S., Ye, X., Feng, H., & Du, Z. (2024).
Evaluating Large Language Models on Spatial Tasks: A Multi-Task Benchmarking Study
(Version 3). arXiv. https://doi.org/10.48550/ARXIV.2408.14438
Zhang, Y., He, Z., Li, J., Lin, J., Guan, Q., & Yu, W. (2024a). MapGPT: An autonomous
framework for mapping by integrating large language model and cartographic tools.
Cartography and Geographic Information Science, 1–27.
https://doi.org/10.1080/15230406.2024.2404868
Zhang, Y., Wei, C., He, Z., & Yu, W. (2024b). GeoGPT: An assistant for understanding and
processing geospatial tasks. International Journal of Applied Earth Observation and
Geoinformation, 131, 103976. https://doi.org/10.1016/j.jag.2024.103976

27

## Page 28

Appendices
Appendix 1: Sample of QGIS native tool documentation (structured in TOML format)
tool_ID = 'native:clip'
tool_name = 'Clip'
brief_description = ''' Clips a vector layer using the features of an additional polygon layer.
'''
parameters ='''
INPUT: Layer containing the features to be clipped
OVERLAY: Layer containing the clipping features
OUTPUT: Specify the output (buffer) layer. One of: Create Temporary Layer
(TEMPORARY_OUTPUT); Save to File...; Save to Geopackage...; Save to Database Table...;
Append to Layer...
'''
code_example = '''
import processing
from qgis.core import QgsProject,QgsVectorLayer
def clip():
output_path ="D:/Output_path/Output_layer.shp"
# Define the parameters Example below:
parameters = {
'INPUT': 'D:/SpatialAnalysisAgent/Data/BG.shp',
'OVERLAY': 'D:/SpatialAnalysisAgent/Data/bd.shp',
'OUTPUT':output_path}
# Perform the extract by attribute operation
result = processing.run("native:clip", parameters)
# Load the selected features as a new layer
output_layer = QgsVectorLayer(result['OUTPUT'], 'Clipped Layer', 'ogr')
QgsProject.instance().addMapLayer(output_layer)
clip()
'''

28

## Page 29

# Load the selected features as a new layer
output_layer = QgsVectorLayer(result['OUTPUT'], 'Clipped Layer', 'ogr')
QgsProject.instance().addMapLayer(output_layer)
clip()
'''

Appendix 2: Sample of customized tool documentation (structured in TOML format)
tool_ID = 'densityMap_kerneldensityestimation'
tool_name = 'Heatmap (Kernel Density Estimation) '
brief_description = '''
Creates a density (heatmap) raster of an input point vector layer using kernel density estimation.
Heatmaps allow easy identification of hotspots and clustering of points.
The density is calculated based on the number of points in a location, with larger numbers of
clustered points resulting in larger values.
'''
parameters ='''
code_example = '''
import geopandas as gpd
import numpy as np
from scipy.stats import gaussian_kde
import rasterio
from rasterio.transform import from_origin
# Load the shapefile and ensure it's in a projected coordinate system
gdf =
gpd.read_file('D:/Case_Studies/Data/PA_restaurants/PA_fastfood_restaurants.shp').to_crs(epsg=2691
8)
# Extract coordinates for KDE
coords = np.vstack([gdf.geometry.x, gdf.geometry.y])
kde = gaussian_kde(coords)

29

## Page 30

# Define grid and calculate KDE density
xmin, ymin, xmax, ymax = gdf.total_bounds
xgrid = np.linspace(xmin, xmax, 200)
ygrid = np.linspace(ymin, ymax, 200)
x, y = np.meshgrid(xgrid, ygrid)
density = kde(np.vstack([x.ravel(), y.ravel()])).reshape(x.shape) * 1e6 # scaled density
# Export the KDE result as a GeoTIFF
output_file = r'C:\Users\Output\kde_output.tif'
transform = from_origin(xmin, ymax, xgrid[1] - xgrid[0], ygrid[1] - ygrid[0])
with rasterio.open(
output_file, 'w',
driver='GTiff', height=density.shape[0], width=density.shape[1],
count=1, dtype=density.dtype, crs=gdf.crs, transform=transform
) as dst:
dst.write(density, 1)
# Display the result in QGIS
output_layer = QgsRasterLayer(output_file, 'KDE_Output')
QgsProject.instance().addMapLayer(output_layer)

30

## Page 31

Appendix 3: Basic level test cases
Note that all datasets included here are for testing purposes only.

S/N

Task

Category

Tool(s) used

1

Select the counties that have
less than 10% increase in
population from 2005 to
2008.

Vector Selection

native:joinattributest
able

1

SC_Counties

Population_Increase2005_2
008

2

Create barchart showing
obesity prevalence in the
United States. Ensure all
labels are clear

Plot

seaborn

1

US_Counties

Obesity_Barchart

3

Clip the DEM to PA
Boundaries

Raster Analysis Clipping

gdal:cliprasterbymas
klayer

1

PA_DEM

PA_DEM_Clipping

4

Generate contour lines from
the DEM of Puerto Rico
with a 50-meter interval

Raster Analysis Contour
Generation

Gdal:contour

1

Puerto Rico DEM

Puerto_Rico_Contour

31

Number of
attempts

Dataset used

Screenshot

## Page 32

S/N

Task

Category

Tool(s) used

5

Add new fields for latitude
and longitude to the fast
food restaurants layer

Add Geometry
Attributes

Native:addxyfields

1

PA_Fastfoods

Add XY_to_Fastfood

6

Extract the counties with
Median household below
50,000 USD in
Pennsylvania.

Vector Selection Attribute Query

qgis:selectbyexpressi 1
on

US_Counties

PA_MedInc_below50000

7

How many damaged houses
were located within the San
Andreas Special Studies
Zones?

Spatial Query

native:extractbylocat
ion

DamagedHouses

DamagedHouses

Generate point features at
the intersections of railways
and the road features

Vector Overlay
Analysis

8

Number of
attempts

1

Dataset used

Screenshot

SAF_SpecialStudyZ
one.shp

native:lineintersectio
ns

1

Nigeria_Major_Roa
ds

Railway_Road_Intersection

Nigeria_Railways

9

Apply an affine
transformation to the

Geometric
Transformation

native:affinetransfor
m
32

1

Penn_State_Building Affine transform

## Page 33

S/N

Task

Category

Tool(s) used

Number of
attempts

Dataset used

Screenshot

building layer to scale by a
factor of 2 and rotate 30
degrees.

10

Based on the provided data
layers, draw a scatter plot
for the Obesity rate and
Covid-19 death rate.

Statistical
Analysis- plot

seaborn

1

US_Counties_Obesit
y_Covid

Covid_Obesity_ScatterPlot

11

Report the information for
this raster data in HTML.

Raster Data
Reporting

gdal:gdalinfo

1

SC_DEM

SC_Raster_Data_Report

12

Can you show me the
Raster Analysis histogram for the DEM pixel histogram
values?

seaborn

1

SC_DEM

SC_DEM_Histogram

13

Do a Fourier conversion for
the loaded image.

numpy

1

LandSat/LT05_L1TP Fourier1
_123042_20110928_
20200820_02_T1_B
5.TIF

Image processing

33

## Page 34

S/N

Task

Category

Tool(s) used

14

Composite the three bands
of LandSat 5 to a RGB
image using the most
commonly used band
composition.

Image processing

gdal:rearrange_band
s

Number of
attempts

2

Dataset used

Screenshot

LandSat/TM5_L2/L LandSat_band_composition
T05_L2SP_029030_ _success
20110605_20200822
_02_T1_SR_B3.TIF
LandSat/TM5_L2/L
T05_L2SP_029030_
20110605_20200822
_02_T1_SR_B2.TIF

15

Separate each band of the
image into a single TIF file.

Image processing

gdal:translate

1

16

Create a histogram of the
distance from the flood
event location to its nearest
river.

Vector overlay

qgis:distancetoneare
sthubpoints, seaborn

Failed.

LandSat/TM5_L2/L
T05_L2SP_029030_
20110605_20200822
_02_T1_SR_B4.TIF
LandSat\TM5_L2
separate_bands
\composited_rgb.tif

Flood2015may.shp
River.shp

34

## Page 35

S/N
17

18

Task
Compute the distance of
each flood to the nearest
river.
Draw the shortest line
between the flood locations
and rivers.

Category
Proximity
Analysis

Distance Analysis

Tool(s) used
['qgis:distancetonear
esthubpoints']
['native:hublines']
['native:shortestline']

Number of
attempts
Failed

1

Dataset used

Screenshot

rivers_ESRI102965.
shp,
flood2015may_ESRI
102965.shp
rivers_ESRI102965.
shp,
flood2015may_ESRI
102965.shp
flood_nearest_river.png

19

20

Reproject the loaded layers
to ESRI:102005
USA_Contiguous_Equidista
nt_Conic.

Reprojection

Reproject all loaded layers
into EPSG6569, and save
them into the same folder,
adding "EPSG6569" to the
current basenames.

reprojection

'gdal:warpreproject'

1

Flood2015may.shp,

Projection

River.shp

['native:reprojectlaye
r']

1

Columbia_schools.s
hp,
Columbia_sidewalk.
shp,

Snipaste_2024-11-04_1809-38.png

Columbia_roads
21

I want you to convert this
csv file into a shapefile. The
longitude is presented as 'X'

Data Conversion

['native:createpointsl
ayerfromtable',

35

1

HIV.csv

Level1_25

## Page 36

S/N

Task

Category

and the latitude is in column
'Y'.

Tool(s) used

Number of
attempts

Dataset used

Screenshot

'native:savefeatures',
'native:loadlayer']

I want you to only keep US
contiguous counties from
this input data.

Geographic
Filtering

['native:extractbyexp
ression']

2

US counties
shapefile

Level1_26

23

I want you to calculate the
length of each polyline and
then add a layer named
'length'.

Geometric
Calculation

['qgis:exportaddgeo
metrycolumns']

1

tl_2019_42_prisecro
ads

Length Calculation

24

I want you to buffer this
polyline and the buffer
distance should be 0.1m.

Buffering
Analysis

['native:reprojectlaye
r', 'native:buffer']

1

Network_Analysis/n
etwork_points

Buffer

25

I want you to clip all
counties of Pennsylvania
from this input data.

Clip Analysis

['native:extractbyattr
ibute', 'pdal:clip']

1

US counties

Level1_30

22

36

## Page 37

S/N

26

27

Task

Category

Tool(s) used

Number of
attempts

I want you to identify all
points that intersect with
Pennsylvania
_Counties_Clip data.

Spatial
Intersection
Analysis

['native:reprojectlaye
r',
'native:extractbyloca
tion']

1

I want you to find the
difference of the two
shapefiles that overlap.

Symmetrical
Difference
Analysis

['native:difference']

1

Dataset used

US counties

Screenshot

Level1_31

HIV csv file

Generated a
polygon,

Level1_32

PA counties

28

I want you to dissolve the
selected shapefile.

Dissolve
Operation

['native:dissolve']

1

PA counties

Dissolve

29

I want you to apply
symmetrical difference
operations on these two
selected shapefiles.

Symmetrical
Difference
Analysis

['native:symmetrical
difference']

1

PA counties and

Level1_34

generated polygon

37

## Page 38

S/N

Task

Category

Tool(s) used

30

I want you to apply union
operations on these two
selected shapefiles. .

Union Analysis

['native:union']

1

PA counties and the
generated polygon

Level1_35

31

I want you to apply
eliminate selected polygons
operations on these two
selected shapefiles.

Polygon
Elimination

['qgis:eliminateselect
edpolygons']

1

PA counties and the
generated polygon

Level1_36

32

I want you to generate the
centriod of all these counties
that are in this shapefile.

Centroid
Calculation

['native:centroids']

1

PA counties

Level1_37

33

Generate a shapefile from
the CSV file.

Data Conversion

['native:createpointsl
ayerfromtable']

2

Street_view_image\
Richland_jsons.csv

CSV to shapefile

34

Extract the boundary
polygon of Laramie County
and save it to the individual
shape file.

Boundary
Extraction

['native:extractbyattr
ibute']

1

Wyoming_Counties_ Extract_save_feature.png
projected.shp

38

Number of
attempts

Dataset used

Screenshot

## Page 39

S/N

Task

Category

Tool(s) used

35

From this input DEM data, I
want you to generate a
hillshade

Terrain Analysis

['native:hillshade']

1

n40_w078_1arc_v3

36

Sum all the pixel values
inside a Census tract
polygon for each tract.

Zonal Statistics

['native:zonalstatistic
sfb']

Failed

LandScan\ landscanusa-2021-conusnight.tif,

37

Provide pixel statistics
inside the polygon.

Zonal Statistics

['native:zonalstatistic
sfb']

Number of
attempts

1

Dataset used

Screenshot

Level1_40

tract_37_EPSG4326
LandScan\Laramie.s
hp,
LandScan/landscanusa-2021-conusnight.tif
Statistic_pixel.png

39

## Page 40

S/N

Task

38

Reproject the DEM to
EPSG6569, and set the cell
size to 30 * 30 meters.

Category
Raster
Reprojection

Tool(s) used
['gdal:warpreproject'
]

Number of
attempts
1

Dataset used

Screenshot

Richland_DEM.tif

DEM_reproject.png
39

Assign EPSG6569 to the
file.

Coordinate
System
Assignment

['pdal:assignprojecti
on']

1

40

Find out the number of
fastfood restaurants in each
county of Pennsylvania

Spatial Join
Analysis

native:joinbylocation Failed
summary

Richland_DEM_EP
SG6569.tif

DEM_assign_project.png

41

Generate 20 random points
inside this polygon

Random Point
Generation

42

Apply extract layer extent
Extent Extraction
operation based on these two
input shapefiles.

PennsylvaniaCountie
s

['qgis:randompointsi
nsidepolygons']

1

PA_Fastfoods
Circle.shp

['native:polygonfrom
layerextent']

1

Circle.shp

40

Level1_39

Level1_40_0

## Page 41

S/N

Task

Category

Tool(s) used

Number of
attempts

Dataset used

Screenshot

43

Generate grid inside this
Grid Generation
selected polygon and the cell
size should be 2 by 2 meters.

['native:creategrid']

1

Rectangle_grid.shp

Level1_41

44

Generate a distance matrix
table showing distances
between all DC health
facilities.

Distance Matrix
Calculation

qgis:distancematrix

1

DC health
center/DC_Health_F
acilities

Distance_Matrix

45

Based on these two input
shapefiles, please conduct
mean coordinate operation.

Mean Center
Calculation

['native:meancoordin
ates']

1

Point_inside_polygo
n.shp;

Level1_43

Rectangle_grid.shp

46
47

Identify the 5 nearest
neighbors to the center point
from the points dataset.
Generate regularly spaced
points inside the selected

Nearest Neighbor
Analysis

['native:joinbyneares
t']

failed

Points.shp;
Center.shp

Point Grid
Generation

['qgis:regularpoints']

1

Rectangle_grid.shp

41

Level1_46

## Page 42

S/N

Task

Category

Tool(s) used

Number of
attempts

Dataset used

Screenshot

polygon, ensuring that the
distance between each point
is 0.1 meters.

48

Using raster calculator,
Raster
convert the nighttime
calculation.
satellite image pixel digital
number (DN) to radiance (L)
using the formula:
L=DN^(1.5)*10e-10

49

Generate a raster distance
for the fastfood restaurants.

Distance Raster
Generation

50

Generate the roughness
index based on the DEM
data.

Terrain
Roughness
Analysis

['qgis:rastercalculato
r']

['gdal:roughness']

42

1

Nighttime/
LuoJnia101_LR20190314298
6_20190311145630_
HDR_0000_gec.tif

Nighttime radiance

1

Richland_SC_fastfo
od.shp

Raster_Distance_Result.png

1

Richland_SC_DEM.
tif

RoughnessIndex_Result.png

## Page 43

S/N

Task

Category

Tool(s) used

51

Generate the terrain
ruggedness index based on
the DEM data.

Terrain Analysis.

['gdal:triterrainrugge
dnessindex']

52

Reproject the building layer
to UTM Zone 17 and then
convert the projected data to
a raster

53

54

Dataset used

Screenshot

Richland_SC_DEM.
tif

terrain_ruggedness_index_R
esult.png

Data Management ['gdal:warpreproject', 1
and Rasterization 'gdal:rasterize']

PSU_b.shp

Screenshot 2024-10-24
233849

Use the raster calculator to
create a mask showing cells
greater than 1000 meters as
1, and cells less than 1000
meters as 0. Use the binary
mask expression.

Raster Analysis.

['qgis:rastercalculato
r']

1

srtm_41_19.tif

Screenshot.png

Set no data value for the
pixel values equal to 0

Raster Data
Management.

['qgis:rastercalculato
r']

1

elevation_mask.tif

Screenshot 2024-10-24
230407

43

Number of
attempts
1

## Page 44

S/N

Task

Category

Tool(s) used

55

Convert the mask layer to
vector.

Data Conversion

['gdal:polygonize']

1

elevation_mask_nod
ata.tif

Screenshot 2024-10-24
231951

56

Save the data as a shapefile

Data Export

['pdal:convertformat'
]

1

elevation_mask_nod
ata.tif

Screenshot 2024-10-24
233219

44

Number of
attempts

Dataset used

Screenshot

## Page 45

S/N

Task

57

Create Thiessen Polygons
for the point data

Geostatistical
Analysis.

['native:voronoipoly
gons']

1

Richland_SC_fastfo
od.shp

58

Please generate a detailed
report in HTML to describe
the nature of the two
datasets based on your
observation. In addition, in
the report, please suggest
some potential applications
or analysis scenarios using
the two datasets.

Report
Generation

['gdal:gdalinfo',
'native:hillshade']

1

Richland_SC_fastfo
od.shp

Generate a HTML table to
show the distance matrix in
the matrix style.

Matrix Analysis.

59

Category

Tool(s) used

Number of
attempts

Dataset used

Screenshot
Screenshot 2024-10-25
001058

Richland_SC_DEM
_UTM17.tif
Screenshot 2024-10-25
001856

['pandas',
'geopandas']

1

45

distance_matrix.shp

Screenshot 2024-10-25
002825

## Page 46

S/N

Task

60

Please draw a histogram for
the DEM data using plotly

Category
Statistical
Analysis

Tool(s) used
['Rasterio', 'NumPy',
'Plotly']

Number of
attempts

Dataset used

1
Richland_SC_DEM
_UTM17.tif

Screenshot
Screenshot 2024-10-25
003225

Appendix 4: Intermediate level test cases
S/N
1

Task

Category

Perform the following tasks: Spatial Analysis
1) Count the fast food
restaurants in each county
and store the result in a new
field named "Count". 2)
Calculate the fast food
accessibility score for each
county as (Count /
Population) * 1,000 and
store the result in a new
field named "Score". 3)

Tool(s) used
native:countpointsin
polygon,
thematic_map_creati
on

46

Number of
Dataset used
attempts
1
/Pennsylvania/PA_F
astfoods_XY.shp
/Pennsylvania/Penns
ylvaniaCounties.shp

Screenshot
Food_Accessibility

## Page 47

S/N

2

3

4

Task
Create a thematic map
showing the fast food
accessibility score for each
county.
Perform the following task:
1) Clip the DEM to SC
boundary and load the
clipped DEM. 2) Show me
the histogram for the
clipped DEM pixel values.
3) Generate the zonal
statistics for every county in
SC, focusing on average
elevation. 4) Finally create a
choropleth map showing the
average elevation of each
county in SC.
Can you please generate a
HTML report to show the
building area for each
building? You can look at
the columns information, if
no building area exists,
please calculate yourself.
Also make sure to use map
projection when calculating
area
Perform the following task:
1) Reproject this road vector
layer to NAD27/ UTM Zone
10 . 2) Create a new field

Category

Tool(s) used

Terrain Analysis

gdal:cliprasterbymas
klayer

Number of
attempts

Dataset used

Screenshot

1

SouthCarolinaData

SC_DEM Figure

1

/Pennsylvania/Penn_
State_Buildings.shp

Building report

1

SanFrancisco/Roads

Road_Length

seaborn
native:zonalstatistics
fb

Attribute
Management

native:reprojectlayer
qgis:exportaddgeom
etrycolumns

Geometric
Analysis

gdal:warpreproject
native:fieldcalculator

47

## Page 48

S/N

5

6

7

Task

Category

Tool(s) used

Number of
attempts

Dataset used

that contains the length of
the road features. Let the
name of the field be
"Length". 3) Use the
'Length' column and find
how many roads have length
shorter 100-meters .
Calculate the ruggedness
Terrain Analysis
index for Pennsylvania, then
summarize the ruggedness
index values for each
counties

native:extractbyattri
bute

['gdal:triterrainrugge 1
dnessindex',
'gdal:cliprasterbymas
klayer',
'native:zonalstatistics
fb']

Pennsylvania/PA_D
EM

Add new fields for latitude
Data Management
and longitude to the fast
food restaurants layer, then
extract the elevation values
from the DEM layer and
save the results in a new
layer.
Merge the four DEMs into a Raster Analysis
single raster and perform
terrain characteristic
analysis for Richland
County, including slope,
aspect, hillshade, terrain
ruggedness index (TRI), and
topographic Position Index
(TPI).

['native:addxyfields',
'native:rastersamplin
g']

Pennsylvania/PA_Fa
stfoods

1

Screenshot

PA_Ruggedness_index

Pennsylvania/Pennsy
lvaniaCounties
Add XY_to_Fastfood

Pennsylvania/PA_D
EM
pdal:merge,
gdal:cliprasterbymas
klayer, native:slope,
native:aspect
native:hillshade,
gdal:triterrainrugged
nessindex,
gdal:tpitopographicp
ositionindex

48

1

Richland

Richland_Raster_Analysis.p
ng

## Page 49

S/N

8

Task

Category

Tool(s) used

Number of
attempts

Dataset used

Screenshot

Count the number of
Attribute Query
hospitals and number of
and Data
fastfoods in each county and Management
save the results into a new
county layer by adding two
fields.

native:joinbylocation 2
summary

Pennsylvania/PA_Ho PA_FF_HospitalCount
spital

9

Reproject this hospital layer
to UTM Zone 17, and then
create a 1000 meters buffer
around each hospital

Geometric
Transformation
and Buffering
Analysis.

'gdal:warpreproject',
'native:buffer',

1

Pennsylvania/PA_Ho PA_Hospital_Buffer
spital

10

Project the Nigeria railways
into EPSG:26392 map
projection, then calculate
the total length.

Geometric
Transformation
and Measurement
Analysis.

['native:reprojectlaye
r',
'native:sumlinelengt
hs']

2

Nigeria/Nigeria_Maj
or_Roads.shp

PA_Counties
PA_Fastfoods

Railway_length
49

## Page 50

S/N

Task

Category

Tool(s) used

Number of
Dataset used
attempts
3
Walmart_site/Walma
rt_4_site_EPSG3211
1.shp

Distance_map.png

2

Washington_poverty.png

11

Generate a distance raster
Distance Analysis
map for each grocery store
and Raster
site within 15 km,
Generation
respectively; the resolution
is 50 m; use the “id” column
to name the raster files.

12

Select the Census tracts in
the Washington area, and
then save the tracts that
possess the top 10% of the
poverty ratio in the selected
tracts.

Attribute Query
and Statistical
Analysis

13

Create a centroid for each
polygon and export the
attributes as a table.

Geometric
Operations and
Data Export

['native:centroids',
'native:exporttosprea
dsheet']

1

US_counties

14

Conduct a hospital
accessibility analysis
following these steps: 1)
find out the nearest hospital
for each Census tract. 2)
compute the distance
between each tract’s
centroid and its nearest
hospital. 3) create a raster,
indicating the distance from

Network Analysis
and Distance
Analysis

'native:nearestneighb
ourhouranalysis',
'native:centroids',
'qgis:distancetoneare
sthubpoints',
'gdal:rasterize',
'gdal:proximity'

Failed

SanFrancisco_tracts
_central,

['native:extractbyexp
ression', 'pdal:clip']

PovertyData\Washin
gton.shp,

Screenshot

PovertyData/Poverty
.shp

50

SanFranciscoHospita
ls

Table_Result

## Page 51

S/N

Task

Category

Tool(s) used

Number of
attempts

Dataset used

Screenshot

each tract to its nearest
hospital.
15

Generate a raster map,
showing the distances from
San Francisco census tracts
to the nearest hospitals. The
map resolution is 100 m.

Distance Analysis
and Raster
Generation.

16

Aggregate the population
with obesity for each state.
The “obesity” column is the
prevalence in percentage.

Statistical
['native:aggregate']
Analysis and Data
Aggregation.

Find out the top 20 coffee
shops in New York City that
have the most bus stops or
metro entrances within 600
feet.

Proximity
Analysis and
Spatial Query

17

['gdal:rasterize',
'gdal:proximity']

['native:buffer',
'native:countpointsin
polygon']

3

3

3

San_Francisco/SanF
ranciscoHospitals.sh
p
,
San_Francisco/SanF
rancisco_tracts_centr
hospital_distance.png
al.shp
US_Counties/US_C Obesity_population.png
ounties.shp

New_York_coffee_s
hop\
bus_metro_stop_EP
SG6535.shp,
New_York_coffee_s
hop\
New_york_coffee_s
hops_EPSG6535.shp
,

51

NY_coffee.png

## Page 52

S/N

Task

Category

Tool(s) used

18

Compute the terrain slope
for each building: 1)
compute the slope; 2) create
centroid of building
footprints; 3) extract the
slope for building centroids.

Terrain Analysis
and Geometric
Operations

['native:slope',
'native:centroids',
'native:rastersamplin
g']

Generate centroids for each
building feature, extract the
elevation values from the
DEM at each building
centroid, and export the
elevation data to draw a
histogram with 50 bins
using Seaborn
Show the year of the street
view image location. You
can consider such steps: 1)
extract the year from the
“image_date” column; 2)
make a thematic map by
rendering the extracted year
using unique values.
Generate an obesity risk
behavior index of each
county in the USA by
analyzing the rate of visits
to unhealthy food retailers
(such as convenience store,
alcoholic drinking places,
and limited service

Geometric
Operations and
Data Extraction

19

20

21

Native:centroids,
native:resampling,
seaborn

Number of
Dataset used
attempts
3
Rolla_building_foot
prints,

Screenshot

Rolla_DEM_project
ed
1

Pennsylvania/PSU_
DEM

Rolla_building_slope.png
Penn State Building
Elevation

Pennsylvania/Penn_
State_Buildings

Data Extraction
and Thematic
Mapping

Index Creation
and Thematic
Mapping

['native:calculateexp
ression',
'thematic_map_creat
ion']

3

native:joinattributest 2
able,
qgis:advancedpython
fieldcalculator,
thematic_map_cretio
n

52

Street_view_image\s
treet_image.shp

Street_image_date.jpg
Obesity_Risk_Score/ Obesity_Risk_Figure_New
US_Counties
New
Obesity_Risk_Score/
Place_visit_rates

## Page 53

S/N

22

23

Task
restaurant) and the visit rate
to places that support
physical activity (e.g., sports
centers, parks, fitness
centers). Visualize the
results in a thematic map to
highlight the obesity risk
behavior index across
counties.
You need to compute the
location error between the
estimated tree trunk and the
ground truth: 1) for each
ground truth location, find
out its nearest estimated
location within 3 meters; the
nearest distance is the error.
2) compute the average
error for ground truth trunks
that have the associated
estimated location.
Link the street view image
location points into a path.
The image was obtained
using a mapping vehicle. All
points represent the location
of a street view image. Each
image has an identifier in
“panoId” column; the
column “link_f_pan”
indicates the panoId of the

Category

Tool(s) used

Accuracy
Assessment and
Distance Analysis

['qgis:distancetonear
esthubpoints']

Number of
attempts

Failed.

Dataset used

Screenshot

Street_view_image/t
runk_location_estim
ated_EPSG6569.shp,
Street_view_image/t
runk_location_groun
d_truth_EPSG6569.s
hp

Network Analysis
and Data
Integration

['GeoPandas',
'Shapely']

3

Street_view_image\s
treet_image.shp

path_linking

53

## Page 54

S/N

Task

Category

Tool(s) used

Number of
attempts

Dataset used

Screenshot

neighbor image in the
forward direction, the
column “link_b_pan”
indicates the panoId of the
neighbor image in the
backward direction. You can
link the location points by:
1) randomly pick up a point;
2) extract its forward and
backward neighbors, link
them together to form a line
segment; 3) find the
neighbors of the two ends of
the segment, and then link
the neighbors to the line
segment; 4) repeat step 3,
until no more neighbors for
the two ends, then start
another new path (repeat
step 1-4 until all points are
processed); 5) ignore points
cannot link to others. 6)
save the paths in an ERSI
shape file.
24

Join the U.S. Census block
group population table to
the block group boundaries.
Note that you must first
create the full block group
FIPS for the table by

Data Join and
Attribute
Management

['pandas',
1
'native:fieldcalculato
r',
'native:joinattributest
able']

54

Rolla_watershed/Rol Attribute_join.png
la_2021_population_
block_group.csv,
Rolla_watershed/
Rolla_downtown_bl

## Page 55

S/N

Task

Category

Tool(s) used

Number of
attempts

merging state, county, tract,
and block group short
FIPSs.

25

26

Dataset used

Screenshot

ock_groups_2021.sh
p

Allocate the Census block
Data Interpolation
group population to the
building footprint according
to the building area. For
example, in a block group of
30 residents, there are two
buildings with areas of 100
square meters and 200
square meters, respectively;
you need to allot 10
residents and 20 residents to
the two buildings
accordingly.

['native:joinattributes Failed.
table',
'qgis:exportaddgeom
etrycolumns',
'native:fieldcalculato
r']

Rolla_watershed/Rol
la_building_footprin
ts.shp,

Use the county boundary to
clip the land cover raster for
each county in Wyoming
State, US. These are steps
for your reference: 1) Select
the county boundary of a
county. 2) Clip the land
cover raster using the
county boundary. 3) Save
each county raster as TIF.

['native:extractbyattr 3
ibute',
'gdal:cliprasterbymas
klayer',
'gdal:translate']

Landcover
\US_Counties_proje
cted.shp,

Raster Clipping
and Data Export

55

Rolla_watershed/Rol
la_downtown_block
_groups_2019.shp

Landcover\
nlcd_2021_land_cov
er_l48_20230630.im
g

county_clip_landcover.png

## Page 56

S/N

Task

Category

Tool(s) used

Raster Clipping
and Geometric
Operations

['native:extenttolayer
',
'gdal:cliprasterbyext
ent']

Number of
attempts

Dataset used

Screenshot

Use “NAME” column as the
file name.
27

28

Clip the image using the
extent box of the shape file
using these steps: 1)
generate the extent box of
the shape file; 2) clip and
save the image.

Weighted
North Carolina will be
Analysis and
receiving funding from a car Decision Support
company for building
electric charging stations. A
group of experts have been
asked to determine the
factors and weights for
locating the new EV
charging stations in NC.
These experts have
determined the most
important factors in ranking
candidate locations for these
new facilities (Data.csv).
These experts have also
assigned weights to each of
the factors. Complete the
nominal group process
technique by calculating the
final weights in the csv file

['pandas']

Failed.

1

56

NoiseMap\
Columbia_image_po
ints_ESRI102039.sh
p,
NoiseMap/SC_road_
noise_2018.tif
Data.csv

An HTML output

## Page 57

S/N

Task

Category

Tool(s) used

Number of
attempts

Dataset used

on a 0 to 1.0 point scale
using the experts factors and
their individual weights.
29

Using the input DEM layer,
generate a watershed with
the outlet point specified by
the 'Outlet' shapefile.
Follow these steps to
complete the analysis:

Hydrological
Analysis and
Watershed
Modeling

['native:fillnodata',
Failed
'native:aspect',
'grass7:r.watershed',
'qgis:rastercalculator'
,'grass7:r.stream.extr
act']

1. Apply a fill
operation on the
DEM to remove
sinks and ensure
proper flow.
2. Perform a flow
direction analysis
based on the filled
DEM data.
3. Calculate the
watershed using the
flow direction output
and the specified
outlet point.
4. Run a flow
accumulation
analysis based on the
flow direction
output.
57

n40_w078_1arc_v3.t
if;
Outlet.shp

Screenshot

## Page 58

S/N

Task

Category

Tool(s) used

Spatial
Interpolation and
Raster Generation

['idw_interpolation']

Number of
attempts

Dataset used

Screenshot

5. Finally, generate
streamlines from the
flow accumulation
output, considering
only areas with flow
accumulation values
greater than 200.
30

Use Inverse Distance
Weighted (IDW)
interpolation to create a
DEM using the given point
data. The elevation column
is “elevatio_1”. The raster
resolution is 10 m. Please
only use the points having
the “image_date” column
values in year 2013 and
after.

1

Street_tree/Richland
_downtown_street_v
iew_image_location
_EPSG6569.shp

IDW.png

Appendix 5: Advanced level test cases
S/N

Task

Category

Tool(s) used

58

Number of
attempts

Dataset used

Screenshot

## Page 59

1

Identify the street tree count
within 20-meter buffer for
each street.

Proximity
Analysis and
Spatial Query

['gdal:buffervectors',
'native:joinbylocatio
nsummary']

2

Street_tree/Street_Tr
ee_EPSG6852
Street_tree/Roads_P
otland_EPSG6852_s
ubset

2

3

4

Compute the total highly
developed area of Orange
County, NY, according to the
land cover raster. The pixel
value of highly developed
area is 24. The unit of area is
square kilometer.

Area Calculation
and Raster
Analysis

Compute the road lengths
inside each protected region.
The identifier of projected
region is “fid”.

Spatial Analysis
and Length
Calculation

From PA_Counties dataset
select only those counties
that the number of data from
PA_DATA_EPSG4326 are
completely within their
boundaries but the count of
point is less than 10. Then

['gdal:cliprasterbyma 3
sklayer',
'qgis:rastercalculator'
,
'native:rasterlayerstat
istics']

Tree_count.png

nlcd_2021_land_cov
er_I48_20230630.tif
NewYork_Counties_
Projected
Developed_area.png

Spatial Query and
Data Extraction

['native:intersection', Failed.
'qgis:exportaddgeom
etrycolumns',
'native:aggregate',
'pandas', 'tabulate'],
['native:joinbylocatio
nsummary',
'native:exporttosprea
dsheet']
['native:countpointsinp 1
olygon',
'native:extractbyattribu
te']

59

Multicriteria Overlay
Analysis/roads_polyl
ine.shp,
Multicriteria Overlay
Analysis/Protected_r
egion.shp
PA counties
shapefile ;
PA_Data_EPSG4326

Level3_4

## Page 60

extract these counties and
load them into QGIS.
5

I want you to measure the
length of boundary of each
county in km based on this
input data. Then display your
result in an HTML file.

Boundary
Measurement and
Data Export

['qgis:exportaddgeome
trycolumns', 'Pandas
library']

1

PA counties

PA_Counties_BoundaryLen
gths.png

6

I want you to find all roads that
crossed the center county and
then extract them from
tl_2019_42_prisecroads.

Spatial Query and
Data Extraction

['qgis:selectbyattribute'
,
'native:extractbyattribu
te',
'native:extractbylocati
on']

2

TL_2019_42_PRISE
CROADS

Level3_6

7

For each county, 1) find the
weather stations inside the
county, and 2) list the
weather station names inside
the county.

Spatial Query and
Data Aggregation

['native:joinattributes 2
bylocation',
'native:extractbyattri
bute']

SC_weatherstations

I would like to identify
which counties in
Pennsylvania are suitable for
planting more trees, using
annual rainfall as a key
parameter. Counties
receiving more than 2.5
inches of rain per year
should be considered suitable
for tree planting.

Suitability
Analysis and
Statistical
Assessment

['native:extractbyattr 1
ibute',
'qgis:basicstatisticsfo
rfields']

Level3_30.shp

8

60

SC_county_boundari
es
weather_station.png
Tree_Plalnting_Suitability.p
ng

## Page 61

Based on your analysis,
please answer the following:
what percentage of
Pennsylvania is suitable for
planting more trees?
How many counties meet the
criteria for tree planting
suitability?
9

Calculate the population that
live in the block groups
having hazard wastes.

Population
Analysis and
Spatial Query

['native:reprojectlaye
r',
'native:joinattributes
bylocation']

Failed.

HW_Sites_EPSG43
26/North_Carolina_
blockgroup_boundar
ies.shp,
HW_Sites_EPSG43
26/HW_Sites_EPSG
4326.shp,

10

Based on this input data,
identify areas suitable for
solar farm installation based
on the slope and proximity to
power line (RandomPoint).
The slope should be less than
5 degrees, and the distance to
the nearest power line
(RandomPoint) should be
within 500 meters.

Suitability
Analysis and
Proximity
Analysis

['native:slope',
2
'qgis:rastercalculator'
, 'native:buffer',
'native:polygonize',
'pdal:clip']

61

Hazard_waste.png

HW_Sites_EPSG43
26/blockgroup_popu
lation_north_carolin
a.csv
n40_w078_1arc_v3.t Level3_9
if

## Page 62

11

For each school in Columbia, Proximity
calculate the length of
Analysis
sidewalks within 500 meters.

['gdal:buffervectors',
'gdal:clipvectorbypol
ygon',
'native:sumlinelengt
hs']

1

12

I want you to join these two
files and create one file that
counties contain HIV rates
based on this dataset 'HIV
Point'. Then generate a
symbology map based on
HIV rate.

Data Join and
Thematic
Mapping

['native:joinattributes 1
bylocation',
'thematic_map_creat
ion']

13

Could you analyze and
visualize the fast food
accessibility score for each
county based on the number
of fast food restaurants and
population using a thematic
map with blue graduated
colors. Then, analyze the
correlation between the
county-level obesity rate and
the fast food accessibility
score by drawing a scatter
plot with a regression line

Statistical
Analysis and
Thematic
Mapping

['thematic_map_crea
tion, 'seaborn']

62

1

Columbia_school_w
alkability/Columbia_
sidewalk_EPSG6569
.shp,
Columbia_school_w
school_sidewalk_length
alkability/Columbia_
schools_EPSG6569.
shp
HIV shapefile;
Level3_14
US counties

PA_Fastfoods_XY,
Pennsylvaniacountie
s

Fastfood_accessibility score

## Page 63

14

15

16

Based on this provided DEM
data and another observation
point (Random_Point), I
want you to conduct a
viewshade analysis from the
observation point. Set a
maximum radius for the
analysis of 5 kilometers.
Please conduct a visibility
analysis using the selected
datasets. Set the following
parameters for the analysis:
Observation Offset (Cell
Towers): 30 meters.
Surface Offset: 1.60 meters.
Outer Radius: 2000 meters.
After completing the
analysis, answer the
following questions: How
many buildings are visible
from a single cellular tower?
What percentage of all
buildings are visible from
five cellular towers?
Extract the DEM values at
the street view images’
locations, and then compare
them with the elevation in
the image’s metadata
(“elevatio_1” column), print
out the descriptive statistics
of the difference between the

Selected tool(s):
['gdal:viewshed']

1

n40_w078_1arc_v3;

Level3_26

Random_Point

Viewshed
Analysis and
Terrain Analysis

['gdal:viewshed',
'Intersect']

Data Extraction
and Statistical
Analysis

['native:rastersampli 1
ng', 'gdal:gdal2xyz',
'grass7:r.univar',
'native:importintopos
tgis']

63

Failed

Viewshade_analysis
file

Street_view_image/s
treet_image.shp,
Street_view_image/
Richland_DEM_EP
SG_6569.tif

street_image_DEM.png,

## Page 64

DEM and metadata in an
HTML file.
17

Propose a new Walmart store
location, which has similar
distances to the existing four
locations, while near the
roads within 300 meters.

Site Suitability
Analysis and
Proximity
Analysis

18

Generate the Normalized
Difference Vegetation Index
(NDVI) of Akure from these
satellite imageries.

Raster Analysis

['qgis:rastercalculato 1
r',
'native:reprojectlayer
',
'gdal:cliprasterbymas
klayer']

19

Use the given checkpoint
locations, extract the values
of the two DEM files, and
then compute the RMSE.

Data Extraction

['native:rastersampli
ng']

20

Can you help me identify the
areas that are suitable for
camping. I want the aspect of
the area to be greater than
100, and the distance to a
closest road not exceeding
1000 meters.

Suitability
Analysis and
Proximity
Analysis

['gdal:buffervectors',
'qgis:distancematrix',
'native:extractwithin
distance',
'native:intersection']

Failed

1

['native:aspect',
Failed
'qgis:rastercalculator'
, 'gdal:rasterize',
'gdal:proximity',
'qgis:rastercalculator'
]
64

Walmart_site/Walm
art_4_site_EPSG321
11.shp,
Walmart_site/
Motorway_EPSG32
111.shp
Landsat 8 imageries,
Akure_boundary

NDVI.png

Street_tree/idw_outp
ut.tif,
Street_tree/Checkpoi
nts_Columbia.shp,
Street_view_image/
Richland_DEM_EP
SG_6569.tif
PA_DEM.tif
PA_Roads

DEM_RMSE.png

## Page 65

65
