# GmE 205 – Laboratory Exercise 2

## Overview

## Environment Setup

- Python 3.x

## How to Run

1. Activate the virtual environment

## Outputs

- lab2_preview.png - plot of lat and lon of the points.csv
- lab2_reports.json - summary of the points data in points.csv

## Reflection

### Object vs Geometry

Modeling points as objects made working with points easier by having functions that manipulate and use the points object easily accessible in the object. When working with points on rows in a table, logic and functions related to points are separate from the points table. When working with points as object, logic and fuctions related to points are attached to the Point object.

### Responsibility

For the lab exercise 2, Point object has responsibility related to the point data and functions and behaviors related to the point data, an example is lat lon validation that is related to the point coordinate. PointSet object has responsibility to the group of points and behaviors that involves the group of points in the PointSet. An example of this was the calculation of bbox which requires info on all the points in a PointSet. The Runner script was respoinsible for generating output using the Point and PointSet object. The runner script is responsible for generation of lat lon plot and summary json of the points in the csv.

### Modeling Insight

Separating geometry, meaning and behavior made spatial logic easier to understand. It compartmentalized smaller logics for working with spatial data into separate functions. It made code written with Objects be easier to understand since functions are written with verbs so we can generally understand what each function in an object does without looking to the code for that function.
