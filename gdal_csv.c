#include "ogr_api.h"
#include "cpl_conv.h" // for CPLMalloc()

int main()
{
    OGRRegisterAll();

    OGRDataSourceH hDS;
    OGRLayerH hLayer;
    OGRFeatureH hFeature;

    hDS = OGROpen("/vsizip/in.csv.zip/in.csv", FALSE, NULL);
    if(hDS == NULL)
    {
        printf("Open failed.\n");
        exit(1);
    }

    hLayer = OGR_DS_GetLayer(hDS, 0);

    OGRDataSourceH hDSOut;
    hDSOut = OGR_Dr_CreateDataSource(OGRGetDriverByName("CSV"), "out-gdal.c.csv", NULL);
    OGRLayerH hLayerOut = OGR_DS_CreateLayer(hDSOut, "out", NULL, wkbNone, NULL);

    OGRFieldDefnH hFieldDefn;

    const char * FIELDNAMES[] = {"anzsic06", "Area", "year", "geo_count", "ec_count"};
    const int NUM_FIELDS = 5;
    for (int i = 0; i < NUM_FIELDS; i++)
    {
        hFieldDefn = OGR_Fld_Create(FIELDNAMES[i], OFTString);
        OGR_L_CreateField(hLayerOut, hFieldDefn, TRUE);
        OGR_Fld_Destroy(hFieldDefn);
    }

    OGRFeatureDefnH *hLayerDefnOut = OGR_L_GetLayerDefn(hLayerOut);

    while((hFeature = OGR_L_GetNextFeature(hLayer)) != NULL)
    {
        OGRFeatureH hFeatOut = OGR_F_Create(hLayerDefnOut);
        for (int i = 0; i < NUM_FIELDS; i++)
        {
            OGR_F_SetFieldString(hFeatOut, i, OGR_F_GetFieldAsString(hFeature, i));
        }
        if(OGR_L_CreateFeature(hLayerOut, hFeatOut) != OGRERR_NONE)
        {
            printf("Failed to create feature in shapefile.\n");
            exit(1);
        }

        OGR_F_Destroy(hFeature);
        OGR_F_Destroy(hFeatOut);
    }

    OGR_DS_Destroy(hDS);
    OGR_DS_Destroy(hDSOut);

    return 0;
}