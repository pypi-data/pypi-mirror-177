import pandas as pd
import numpy as np
import folium
import branca.element as br

class MapData:
    # Constructor
    def __init__ (self, width="800px", height="600px", coords=[48.82407334738646, 2.3583897202323505], zoom=12):
        # Attribute
        self.width = width
        self.height = height
        self.coords =  coords
        self.zoom = zoom
        self.map = folium.Map()
        self.figure = br.Figure()

        # Construct map
        self.construct()

        # Return
        return

    # METHODE
    def construct(self):
        '''
        Construct the MapData Object

        return MapData
        '''
        self.figure = br.Figure(width= self.width, height= self.height)
        self.map = folium.Map(location=self.coords)
        self.map.add_to(self.figure)

        return self

    def show(self):
        '''
        Display a map if it is the last line of a notebook cell

        return br.element.Figure
        '''

        return self.figure
    
    def addDataFromDf(self, dataframe, lat="lat", lon="lon", attributes="all", type="marker", center_map_on_data=True):
        '''
        Add data from a dataframe to this map

        Parameters:
            dataframe (pandas.DatFrame): Dataframe with geodata
            lat (str): Columns with latitude WGS84
            lon (str): Columns with longitude WGS84
            attributes (str, list): Array of columns name
            type (str): Type of the data on the map [marker,]
            center_map_on_data (bool): If true, center map on data

        Return
            MadData object
        '''

        # CHECK
        if attributes == "all":
            attributes = dataframe.columns.to_list()

        # MARKER
        if type == "marker":
            # Add marker for each point
            for index, row in dataframe.iterrows():
                folium.Marker(
                    location = [row[lat], row[lon]],
                    popup = dataframe[attributes].iloc[[index]].transpose().to_html(header=False)
                ).add_to(self.map)

        # Center map on data
        if center_map_on_data:
            self.map.location = [dataframe[lat].mean(),dataframe[lon].mean()]

        return self