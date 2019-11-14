# mod3_project

This repo contains:
* Description of the project in a PDF
* Three python starter files
* Three test files
* A starter jupyter notebook

Authors:
Joe Read and Mohammed Hannan

Dataset:
London TfL Bikepoint data combined with London geographical data.
We want to look at how the location of the bikepoint influences the condition
of the bikepoint. We will use the geographical data to see if the population
statistics have an impact on the usage of the bikepoint.

Hypotheses:


1) A Faulty bikepoints will be less likely to have other faulty bikepoints near it 
H0 = Faulty bikepoints have the same number of faulty bikepoints nearby as general bikepoints
H1 = Faulty bikepoints have less likely to have more than 1 faulty bikepoints near them than general bikepoints

2) Bikepoints at a high elevation are smaller.
H0 = Bikepoints on hills have the same number of docks as general bikepoints
H1= Bikepoints on hills have fewer docks than general bikepoints

3) Bikepoints in high populated areas are more likely to be faulty.
H0 = Bikepoints in highly populated areas have the same probability of having a faulty dock as general bikepoints
H1 = Bikepoints in highly populated areas have a higher probability of having a faulty dock

4) Higher populated areas have larger bikepoints
H0 = Bikepoints in highly populated areas have the same number of docks as general bikepoints
H1 = Bikepoints in highly populated areas have more docks than general bikepoints

APIS:
TfL BikePoint API.
Data Science Toolkit Coords to Statistics API.
