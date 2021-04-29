#!/usr/bin/env python2.7
"""
Description: This Arcgis tool merges all raster tiles in a folder into mosaics
             of a given size.
Created by: Phillip Ruscica
"""

###############################################################################
import os
import arcpy
import re
###############################################################################


def get_rasters(in_workspace):
    '''This function get a list of the rasters within the input folder'''
    # Set the workspace for the input folder
    arcpy.env.workspace = in_workspace

    # Get the list of rasters in the in_workspace
    raster_list = arcpy.ListRasters()

    # Sort the rasters in the list
    raster_list.sort(key=natural_keys)

    # Return the list of rasters
    return raster_list


def natural_keys(string):
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', string) ]


def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval


def mosaic_all(in_workspace, number_of_tiles, out_workspace, raster_list):
    # Set the input workspace
    arcpy.env.workspace = in_workspace
    # Update the user as to what is being processed

    arcpy.AddMessage('All rasters are being processed into mosaic.tif')

    # Mosaic the chunk
    arcpy.MosaicToNewRaster_management(raster_list,
                                       out_workspace,
                                       'mosaic.tif',
                                       "#", "#", "#", "1")

def mosaic_chunks(in_workspace, number_of_tiles, out_workspace, raster_list):
    """This function loops through the files and mosaics them"""
    # Set the input workspace
    arcpy.env.workspace = in_workspace

    # Get the number of chunks needed to be processed
    num_of_chunks = int(round(len(raster_list) / int(number_of_tiles)))


    # Convert number_of_tiles to an interget value
    number_of_tiles = int(number_of_tiles)

    # Set the indicies for the chunks bounds
    highest_index = number_of_tiles - 1
    top_bound = number_of_tiles
    bottom_bound = 0

    # Process all if the number of tiles larger than the number of tiles
    if number_of_tiles > len(raster_list):
        mosaic_all(in_workspace, number_of_tiles, out_workspace, raster_list)

    else:
        for chunk in range(num_of_chunks):
            # Set the bounds of the chunk
            sublist = raster_list[bottom_bound: top_bound]

            # Set the name of the output raster
            sublist_name = "tiles" + str(bottom_bound) + '_' + str(top_bound) + ".tif"
            # Update the user to which chunk is being worked on
            arcpy.AddMessage("Mosaicing " + str(sublist) + ' into ' + str(sublist_name))

            # Mosaic the chunk
            arcpy.MosaicToNewRaster_management(sublist,
                                               out_workspace,
                                               sublist_name,
                                               "#", "#", "#", "1")
            # Update the indicies
            top_bound += number_of_tiles
            bottom_bound += number_of_tiles

###############################################################################


if __name__ == "__main__":
    in_workspace = arcpy.GetParameterAsText(0)     # Folder containing rasters
    out_workspace = arcpy.GetParameterAsText(1)    # Output folder
    mosaic_all_at_once = arcpy.GetParameterAsText(2)
    number_of_tiles = arcpy.GetParameterAsText(3)  # Num of tiles per mosaic

# Set the input workspace
arcpy.env.workspace = in_workspace
# Get the rasters for processing

rasters = get_rasters(in_workspace)

if mosaic_all_at_once == 'true':
    mosaic_all(in_workspace, number_of_tiles, out_workspace, rasters)
else:
    if number_of_tiles == None:
        arcpy.AddMessage("For chunk processing, you need to input a processing interval")
    else:
        # Mosaic the raster into chunks
        mosaic_chunks(in_workspace, number_of_tiles, out_workspace, rasters)
