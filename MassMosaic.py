import os
import arcpy


def main(in_workspace, number_of_tiles, temp_workspace, out_workspace, raster_list):
    arcpy.env.workspace = in_workspace
    raster_len = len(raster_list)
    subclasses = raster_len/number_of_tiles

    # merge them into larger tiles
    top_bound = number_of_tiles - 1
    bottom_bound = 0
    count = 0
    while count <= subclasses:

        sublist = raster_list[bottom_bound: top_bound]

        arcpy.MosaicToNewRaster_management(sublist, temp_workspace, "tiles" + str(bottom_bound) + str(top_bound) + ".tif", "#", "#", "#", "1")

        top_bound = top_bound + number_of_tiles
        bottom_bound = bottom_bound + number_of_tiles
        count = count + 1

    # merge the larger tiles into the final mosiac
    arcpy.env.workspace = temp_workspace
    final_list = arcpy.ListRasters()
    arcpy.MosaicToNewRaster_management(final_list, out_workspace, "finalmosaic.tif", "#", "#", "#", "1")


if __name__ == "__main__":
    in_workspace = arcpy.GetParameterAsText(0)
    number_of_tiles = arcpy.GetParameterAsText(1)
    temp_workspace = arcpy.GetParameterAsText(2)
    out_workspace = arcpy.GetParameterAsText(3)

    arcpy.env.workspace = in_workspace

    # get the list of rasters in the in_workspace
    raster_list = arcpy.ListRasters()
    main(in_workspace, number_of_tiles, temp_workspace, out_workspace, raster_list)
