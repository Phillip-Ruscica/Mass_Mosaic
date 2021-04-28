#!/usr/bin/env python2.7
"""
Description: This Arcgis tool merges all raster tiles in a folder into mosaics
             of a given size.
Created by: Phillip Ruscica
"""

###############################################################################
import os
import arcpy
###############################################################################


def get_rasters(in_workspace):
    '''This function get a list of the rasters within the input folder'''
    # Set the workspace for the input folder
    arcpy.env.workspace = in_workspace

    # get the list of rasters in the in_workspace
    raster_list = arcpy.ListRasters()

    # Return the list of rasters
    return raster_list


def mosaic_chunks(in_workspace, number_of_tiles, out_workspace, raster_list):
    """This function loops through the files and mosaics them"""
    # Set the input workspace
    arcpy.env.workspace = in_workspace

    # Get the number of chunks needed to be processed
    num_of_chunks = round(len(raster_list) / int(number_of_tiles))

    # Set the index values for the rasters
    top_bound = number_of_tiles - 1
    bottom_bound = 0

    # Initiate the loop for identifying each chunk
    count = 0
    while count <= subclasses:
        # Set the bounds of the chunk
        sublist = raster_list[bottom_bound: top_bound]

        # Mosaic the chunk
        arcpy.MosaicToNewRaster_management(sublist,
                                           temp_workspace,
                                           "tiles" + str(bottom_bound) +
                                           str(top_bound) + ".tif",
                                           "#", "#", "#", "1")

        # Update the indicies
        top_bound = top_bound + number_of_tiles
        bottom_bound = bottom_bound + number_of_tiles
        count = count + 1
###############################################################################


if __name__ == "__main__":
    in_workspace = arcpy.GetParameterAsText(0)     # Folder containing rasters
    number_of_tiles = arcpy.GetParameterAsText(1)  # Num of tiles per mosaic
    out_workspace = arcpy.GetParameterAsText(2)    # Output folder

# Get the rasters for processing
rasters = get_rasters(in_workspace)

# Mosaic the raster into chunks
mosaic_chunks(in_workspace, number_of_tiles, out_workspace, rasters)
