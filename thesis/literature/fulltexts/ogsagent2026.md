---
id: literature/fulltexts/ogsagent2026
type: fulltext
status: frozen
language: en
key: ogsagent2026
title: >-
  OGSAgent: an MCP-based multi-agent collaboration framework for intelligent GIServices
resource: https://doi.org/10.1080/13658816.2026.2715051
description: >-
  The vision of intelligent GIServices (Geographic Information Services) is to automatically discover, compose and execute distributed GIServices to address global challenges.
pages: 16
words: 3199
year: 2026
venue: >-
  International Journal of Geographical Information Science
authors: >-
  Wang, Kaixuan; Yue, Peng; Wu, Haoru; Teng, Baoxin
doi: 10.1080/13658816.2026.2715051
oa_status: green
extracted: 2026-10-31
extractor: pdftotext (poppler), no -layout
note: >-
  Machine-extracted text. Tables, figures, equations and footnotes are
  unreliable — verify any quotation against the PDF.
---

# OGSAgent: an MCP-based multi-agent collaboration framework for intelligent GIServices

## Page 1

Appendix A. Mapping from OAPI endpoints to GeoMCP servers
A.1 OGC STA
OGC STA is the main standard for interconnecting the sensor devices and observation
data over the Web. At a high level, OGC STA provides two parts with Part1 for Sensing
and Part2 for Tasking. This paper focuses on the data retrieval part, while Part2 Tasking
is used for planning the devices for sensor activities. Therefore, this paper only
considers the Part1. The main sensing entities defined in OGC STA include:
•

Thing: a physical or virtual IoT device that contains one or more sensors.

•

ObservedProperty: an entity that describes the physical quantity or attribute being
measured, such as temperature, humidity, or light intensity.

•

Datastream: a collection of observations produced by the same IoT sensor
measuring the same observed property.

•

Observation: an entity associated with a DataStream that represents a specific
observation result at a particular point in time.

•

FeatureOfInterest: describes the spatial attributes of the observed Observation
entity.
Figure A.1 shows the mapping of the sensing entities defined in STA to a GeoMCP

sensing resource in structured metadata text. The resource includes the list of IoT things,
with each thing containing all associated data streams. Each data stream includes key
information such as the observed property, units, and observation duration.
Operations for retrieving the sensing entities are wrapped as GeoMCP tools, as
shown in Table A.1. When requesting data, the STA supports specifying the properties
to return by using the $expand and $filter query options. The $expand specifies which
related entities should be included inline in the response, while $filter can be used for
filtering a collection of entities by property value. These query options can be passed
to the tools through the params input. Some observation retrieval tasks require a
workflow that combines access to different sensing entities, such as retrieving
observations for a specific Thing and ObservedProperty. Table A.2 presents this
workflow and its mapping into a single GeoMCP tool.

## Page 2

Figure A.1 Mapping sensing entities to a GeoMCP resource
Table A.1 Mapping the resource URIs of sensing entities to GeoMCP tools
Http method

Resource URI

GeoMCP tools

GET

{root}/Things(id){?queryParameters}

getThings(th_id, params)

GET

{root}/Things(id)/Datastream(id){?queryPar
ameters}

getDatastream(th_id, ds_id,
params)

GET

{root}/Datastream(id)/ObservedProperty{?q
ueryParameters}

getObservedProperty(ds_id,
params)

GET

{root}/Datastream(id)/Observations(id){?qu
eryParameters}

getObservations(ds_id, ob_id,
params)

GET

{root}/Datastream(id)/Observations(id)/Fea
tureOfInterest{?queryParameters}

getFeatureOfInterest(ds_id, ob_id,
params)

## Page 3

Table A.2 Mapping the Observation retrieval workflow to a GeoMCP tool
Workflow1: Retrieving Observations for a specific Thing and ObservedProperty
MCP tool: getSpecificObservations(thing_name, observation_property_name, start_time, end_time)
Input: Thing name {thing_name}, Observation property name {observation_property_name}
time interval {start_time, end_time}
Output: Observations
Step1: Request Datastream for a specific Thing and ObservedProperty
1: HTTP GET Request:
{root}/Things?$filter=name eq {thing_name}&$expand=Datastreams($filter= ObservedProperty/name
eq {observation_property_name})

2: Receive response → DatastreamWithThing (DT)
Step2: Request Observations
3: HTTP GET Request:
{root}/Things({DT.thing_id})/Datastreams({DT.datastream_id})/Observations?$filter= resultTime ge
{start_time} and resultTime le {end_time}

4: Receive response → Observations
Output Observations

A.2 OAPI – Common-Part2 and Records
OAPI-Common-Part2 and Records are standards for providing geospatial metadata.
Modern discovery services, such as OAPI – Records, tend to bind metadata catalogs
with the resources themselves. This allows clients to retrieve the metadata and harvest
the resource at the same time. OAPI – Records achieves this by ensuring compatibility
with OAPI-Common. The draft standard OAPI – Common – Part2 defines the shared
endpoints, i.e., '{root}/collections' and '{root}/collections/{collectionId}', for all OAPI
family standards. Through a GET request, the former URI returns a Collections, which
is a list of Collection, while the latter provides details of a specific Collection with a
given collectionId. Each Collection is a summary metadata for a geospatial collection
and includes links for accessing the actual data. The other resource-specified OAPI
standards belonging to data services and visualization services inherit Collections and
Collection, and further enrich their associated metadata (e.g., querables in
FeatureCollection). In OAPI – Records, these shared URIs are called local resource
endpoints. Collections and Collection correspond to Catalog and Record in OAPIRecords, respectively. The other OAPI standards for geospatial data retrieval (e.g.,
OAPI – Features) are derived from OAPI-Common, thus inherently provide discovery
capabilities as well. Figure A.2 illustrates the mapping of the discovery entity

## Page 4

(Collection/Record) to a GeoMCP resource for a common geospatial collection. Other
specialized types of GeoMCP resources can be extended on this basis.

Figure A.2 Mapping discovery entities to a GeoMCP resource

A.3 OAPI – Features and Coverages
OAPI – Features and OAPI – Coverages respectively define RESTful interoperable
interfaces for accessing feature (e.g., vector data) and coverage (e.g., image data)
resources. These standards are in conformance with OAPI-Common and organize
geospatial data into collections, including FeatureCollections and Coverages. Data
items within a collection can be accessed through the URI of the corresponding view:
‘/collections/{collectionId}/{viewId}’. For instance, the viewId for feature collections
is items, while that for raster coverages is coverage.
OAPI – Features and OAPI – Coverages extend the Collection model defined in
OAPI – Common-Part 2 by adding new properties specific to their respective data types.
Specifically, OAPI – Features defines the queryables property. It contains a dictionarytype element named properties, which provides the feature’s attributes that can be used
in filter expressions. OAPI – Features supports the Common Query Language (CQL2)

## Page 5

to filter features. OAPI – Coverages, on the other hand, introduces schema to describe
the fields (e.g., bands and variables) of the coverages. It reuses the schema of properties
from OAPI – Features and supports the field selection.
The metadata of FeatureCollections and Coverages returned by OAPIs can be
mapped to GeoMCP resources (see Figure A.3), while their data access interfaces can
be encapsulated as GeoMCP tools (see Table A.3).

Figure A.3 Mapping feature and coverage entities to GeoMCP resources
Table A.3 Mapping the resource URIs of feature and coverage entities to GeoMCP tools
Http method

Resource path

GeoMCP tools

GET

{root}/collections/{collectionId}/items?bbo
x={bbox}&datetime={datetime}&filter={cq
l2}
{root}/collections/{collectionId}/coverage?p
roperties={properties}&bbox={bbox}&datet
ime={datetime}

getFeatures(co_id, bbox, datetime,
filter)

GET

getCoverage(co_id,
bbox, datetime)

properties,

## Page 6

A.4 OAPI - Processes
A process is a defined operation or function that takes input geospatial data, performs
computations or transformations, and generates output results within a geospatial
context. OAPI – Processes defines a process description model with attributes including
process id, description, job control options, inputs, and outputs. Each input or output
includes a verifiable schema to ensure that machines can correctly interpret the basic
data types or structures of a complex object. Process descriptions are mapped to
GeoMCP resources to inform the LLM of the available processing tools (see Figure
A.4).
OAPI – Processes offers the interfaces for obtaining process descriptions and
executing a process, which can be mapped to GeoMCP tools (see Table A.4). An
execute request body is a name/value pair that follows the input schema defined in the
process description. Each process provided by the processing service endpoint is
mapped to a single tool. This can be achieved by parsing the structured process
description to construct an executable function. Specifically, the process id, inputs, and
outputs are mapped to the function name, input parameters, and output parameters,
while the function body implements the process execution request. Such a function can
then be wrapped as a GeoMCP tool. Process execution is divided into two job control
options: synchronous and asynchronous, which are indicated by the jobControlOptions
attribute. For the former mode, the request returns the result directly. For the latter, the
job status must be continuously polled. The mapped MCP tools internally adapt their
execution based on the value of jobControlOptions, hiding this difference from the
LLM.

## Page 7

Figure A.4 Mapping processing entities to a GeoMCP resource
Table A.4 Mapping the resource URIs of processing entities to GeoMCP tools
Http method

Resource path

GeoMCP tools

GET

{root}/processes

getProcesses()

GET

{root}/processes/{processId}

getProcess(pr_id)

POST

{root}/processes/{processId}/execution

{processId}(input)

A.5 OAPI – Styles, Maps, and 3D GeoVolumes
OAPI – Styles, Maps and 3D GeoVolumes belong to the OAPI standards for providing
visualization resources. They offer the presentation of information to humans through
multiple geospatial portrayals, including maps and 3D models. A map is a twodimensional visual portrayal of geospatial data, typically in an image format. The
generation of map elements requires data (such as features and coverages) and styles.
A style defines the mapping rules between data and map symbols applied by the
rendering engine. In 3D visualization scenarios, 3D content with geospatial coordinates
serves as the primary visualization resource. There are existing solutions for accessing
and exchanging 3D geospatial content, including 3D Tiles, I3S, and CityGML.
The OGC has developed interoperable API specifications for accessing the above
visualization resources, including OAPI – Maps, Styles, and 3D GeoVolumes. These
standards are consistent with OAPI – Common and align with the Collection entity.
The maps can be generated from a specific geospatial data collection, rendered with

## Page 8

either a default or a specific style. The description of a map inherits the properties of its
source collection, including description, spatial extent, and temporal extent. The
available styles can be associated with specific collections and provide related style
descriptions, style sheets in specific encodings, and information about the layers
involved in symbolization. The offered metadata of maps and styles are mapped into
the GeoMCP resources (see Figure A.5). As for 3D models, OAPI – 3D GeoVolumes
defines a 3D Container as a collection of spatial volumes, where each volume either
contains sub-volumes (children) or a set of accessible 3D objects (content). These
spatial objects can be distributed in various formats, such as 3D Tiles, I3S, and
CityGML. When mapping to GeoMCP resources, the nested 3D containers are
traversed, and only those containers that actually contain links to 3D objects are
included (see Figure A.5). The interfaces for accessing style, map, and 3D container
resources are converted into GeoMCP tools (see Table A.5). Notably, when accessing
map resources, some operations can be achieved through additional parameters, such
as changing the background, scaling, adjusting display resolution, and spatial subsetting.
OAPI – 3D GeoVolumes also supports a bbox query, which applies filtering to the
contents within the 3D container.

Figure A.5 Mapping visualization entities to GeoMCP resources

## Page 9

Table A.5 Mapping the resource URI of visualization entities to GeoMCP tools
Http
method
GET

Resource path

GeoMCP tools

{root}/collections/{collectionId}/styles/{styleId}

getStyle(co_id, st_id)

GET

{root}/collections/{collectionId}/map{?queryParame

getMap(co_id, params)

ters}
GET

{root}/collections/{collectionId}/styles/{styleId}/ma
p{?queryParameters}

getMapWithStyle(co_id, st_id,
params)

GET

{root}/collections/{3DContainerId}?bbox={bbox}

Get3DContainer(co_id, bbox)

Appendix B. GeoMCP prompt design
B.1 Planner prompt

## Page 10

B.2 Router prompt

B.3 Replanner-without-reflection prompt

## Page 11

B.4 Replanner-with-reflection prompt

## Page 12

B.5 Processor prompt

Appendix C. Integrated OAPI endpoints
Endpoint

Resource id

Resource type

Resource description

GNOSIS
Server

sentinel2-l2a
sentinel2-l2a
wildfire:fireDang
erIndices
wildfire:S2Vegeta
tionFuelTypes
gebco
water_body_china
city_china_bound
ary
waterway_china
wind_new_york

Coverage
Map
Coverage

Global sentinel-2 (ESA) data.
Global sentinel-2 (ESA) data.
ECMWF CEMS Fire Danger indices (Jan
2021 - July 2022).
Global Vegetation Fuel Types.

dem

Coverage

Dem data with 30m resolution.

lulc

Coverage

LULC data with 30m resolution.

poi_wuchang

FeatureCollection

The points of Interest Data in Wuchang

wuchang_resident
ial
rheinland_pfalz_
waterways

FeatureCollection

The residential polygons in wuchang.

FeatureCollection

The waterways in rheinland_pfalz,

rheinland_pfalz_tr
ansport

FeatureCollection

Pygeoapi
Server

Coverage
Coverage
FeatureCollection
FeatureCollection
FeatureCollection
Coverage

General Bathymetric Chart of the Oceans
Water bodies features in China.
This data displays boundary of every city of
China.
Water way features in China.
The wind image in new york city.

Germany.
The transport point in rheinland_pfalz,
Germany.

## Page 13

new_york_boroug
hs_boundary

FeatureCollection

eastern_china_sea

FeatureCollection

Polygon vector data of Eastern China Sea

touch

Process

Determine whether two features touch.

buffer

Process

Input a feature and a buffer distance, and

Polygon vector boundaries of New York
City’s boroughs

return the resulting buffer.
features_filter_by
_intersection

Process

Filter candidate_features to return features
that intersect with all features in
intersect_features_list.

get_bbox_of_feat
ure
detect_water_cha
nge

Process

Retrieve the bbox of a feature.

Process

Input NDWI images before and after; return

dew_point

Process

a water change image.
Input relative humidity data and
temperature data, return dew point
temperature.

apparent_tempera
ture

Process

Input temperature data, relative humidity
data, and wind velocity data; return
apparent temperature.

find_comfort_peri
ods

Process

Input apparent temperature data and dew
point temperature data, return time periods
of thermal comfort.

features_area

Process

Computes the geodetic area (in square
meters) of all features in a GeoJSON object.

find_extreme_pix
el

Process

Find the maximum or minimum pixel value
in a single-band image and return both the
value and geographic coordinates.

fuel_vegetation_d
ensity

Process

slope

Process

Calculate slope using DEM data.

filter_raster_by_p
ixel_value

Process

Filters raster pixels based on a threshold

Calculate fuel vegetation density based on
the fuel vegetation types.

condition and converts the resulting
segments into vector format.

add_area_to_featu
res

Process

Calculate geodesic area (m2) for each
feature and store it as a property. Return the
modified features.

filter_top_features

Process

Filter features by a property and keep the
top N features.

## Page 14

count_features

Process

Count the number of features in feature
data.

OGEMaps
Server

Steinbeis@
HFT
Stuttgart
Server

map:newyork_str
eets

Map

topp:states

Map

This is some census data on the states.

polygon

Style

Polygon style.

map:light

Style

Light style.

map:night

Style

Night style.

map:grey

Style

Grey style.

NewYork

3D container

All Supported 3D Containers for the city of

The map data of the street of New York,
with the buidling, roads, park, waterway.

NewYork.
Wuestenrot

3D container

All Supported 3D Containers for the city of
Wuestenrot, Germany.

California

3D container

All Supported 3D Containers for California
state, USA.

Stuttgart

3D container

All Supported 3D Containers for the city of
Stuttgart, Germany.

Ldproxy
Server

vineyards

OGE-STA
Server

Changi_Temperat
ure

Observation

Changi_Relative_
Humidity

Observation

Changi_Wind_Ve
locity

Observation

Jurong(West)_Te
mperature

Observation

Jurong(West)_Rel
ative_Humidity

Observation

Jurong(West)_Wi
nd_Velocity

Observation

Newton_Tempera
ture

Observation

Newton_Relative
_Humidity

Observation

Newton_Wind_V
elocity

Observation

FeatureCollection

Vineyards in Rhineland-Palatinate,
Germany.
The temperature datastream in Changi,
Singapore.
The relative humidity datastream in Changi,
Singapore.
The wind velocity datastream in Changi,
Singapore.
The temperature datastream in Jurong
(West), Singapore.
The relative humidity datastream in Jurong
(West), Singapore.
The wind velocity datastream in Jurong
(West), Singapore.
The temperature datastream in Newton,
Singapore.
The relative humidity datastream in
Newton, Singapore.
The wind velocity datastream in Newton,
Singapore.

## Page 15

Appendix D. Benchmark
Id

Questions

1

Retrieve the Retrieve the relative humidity for the Newton area on July 3, 2025.

2

Retrieve the dew point temperature at Changi on July 3, 2025.

3

Retrieve the apparent temperature at Changi on July 3, 2025.

4

Retrieve the optimal thermal comfort periods for Newton on July 3, 2025.

5

Retrieve all hospital located in Wuchang District.

6

Retrieve all schools within 500 meters of a restaurant in Wuchang District.

7

Find all the best residential areas within Wuchang District that are within 500 meters
of a school and a metro station.

8

Determine whether Dongting Lake and Poyang Lake touch each other.

9

Determine whether Dongting Lake is larger than Poyang Lake.

10

Retrieve Sentinel-2a data within the range [114.30754, 30.53009, 114.33070,
30.54771] on 2020-08-17.

11

Retrieve NDVI index data within the range [114.30754, 30.53009, 114.33070,
30.54771] on 2020-08-17.

12 Retrieve NDWI index data within the Liangzi Lake area on 2020-05-24.
13

Detect water body change within the spatial extent of Liangzi Lake on 2020-08-17
compared to 2020-05-24

14 Obtain 3D building data for Wuestenrot and visualise it.
15

Retrieve 3D building data for the NewYork area within the range [-74.01,40.70,11.89,-73.90,40.88,547.75] and visualize it.

16

Retrieve a night-style map of New York City with a size of 1080×1920 and visualize
it.

17

Visualize a digital twin of New York City, including 3D buildings, a light-themed 2D
new york street base map, and a wind field map

18 Retrieve the burning index within New York City, Manhattan.
19 Obtain the vegetation fuel density within New York City, Queens.
20 Retrieve the vineyard called Geisberg in the German state Rhineland-Palatinate.
21 Retrieve the deepest water depth in the Eastern China Sea.
22

Find the vineyards located within 1,000 meters of the Rhine River in the German state
Rhineland-Palatinate.

23

Find the vineyards that are within 1500 meters of both a railway station and the Mosel
River.

24 Retrieve the highest burning index within the extent of New York City, Manhattan.
25 I want to know the area of Poyang Lake.
26

Calculate the maximum NDWI index value within the Liangzi Lake area on 2020-0524.

27

Is the maximum NDWI value within the spatial extent of Liangzi Lake on 2020-08-17
greater than that on 2020-05-24?

## Page 16

28 Has the area of Poyang Lake exceeded 1,000 square kilometers?
29

Calculate the total area of residential zones in Wuchang that are within 1,000 m of
schools.

30

Calculate and visualize the top five residential zones in Wuchang by area that are
within 1,000 m of hospitals.

31 Can Poyang Lake be connected to the East China Sea via the Yangtze River?
32 Extract the waterways connected to Dongting Lake and visualize them.
33

In New York, is the average Burning Index within the spatial bounding box of the
Bronx higher than that within the spatial bounding box of Brooklyn?

34

Calculate the maximum Danger Risk Index value within the spatial bbox of the Bronx
in New York.

35

Find the residential area in Wuchang that is within 500 m of a metro station, has
hospitals and schools within 1,000 m nearby, and has the largest area.

36

Extract the vineyard with the largest area within 1,000 m of the Mosel River in the
German state of Rhineland-Palatinate and visualize it.

37 Count how many water bodies are there in Changsha City.
38 Does Wuhan City border Xinyu City?
39 Are there more water bodies in Xianning City than in Changsha City?
40 Obtain vector areas in Ezhou City with slopes less than 15°and visualize them.
41 What is the highest elevation value within Xianning City?
42 What is the average slope value within the bounding box of Xianning City?
43 What is the area of impervious surfaces in Ezhou City?
44

Within the bounding box of Ezhou City, is the area of impervious surfaces greater than
that of forest land?

45

Is the area of forest land within the spatial bounding box of Ezhou City greater than
that of Xinyu City?
