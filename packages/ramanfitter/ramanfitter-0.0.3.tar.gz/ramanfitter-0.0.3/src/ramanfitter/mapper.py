'''
    Name:           Mapper

    Description:    Mapper takes in a text file from the Horiba Raman system and outputs a color map of similar areas, based on range inputs from the user

    Author:         John Ferrier, NEU Physics, 2022

'''

__author__  = "John Ferrier"
__email__   = "jo.ferrier@northeastern.edu"
__status__  = "planning"

import os
import numpy as np
from matplotlib import cm
from platform import system
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from ramanfitter import RamanFitter
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1 import make_axes_locatable


class Mapper:

    # Initializer
    def __init__( self, 
                file            = None, 
                delimiter       = '\t', 
                display_name    = "", 
                raman_range     = None, 
                colormap        = 'turbo',
                plotType        = 'contour',
                bins            = 20,
                resolution      = '4K',
                makeVideo       = False,
                makePlot        = True,
                FPS             = 60,
                xAxisTitle      = "x-position (μm)",
                yAxisTitle      = "y-position (μm)",
                xRamanTitle     = "cm^-1",
                yRamanTitle     = "A.U.",
                output_path     = "",
                provided_img    = None,
                alpha           = 0.7 ):

        '''
            __init__( self, file = None, colormap = 3 )

            Initializes the Mapper Class

            Parameters
            ----------
            file : str, default: None
                The .txt file of the map from LabSpec
            colormap : str, optional, default: 12
                Colormap name. Options can be found :ref:`here <https://matplotlib.org/3.5.0/tutorials/colors/colormaps.html>`
            PercentRange : float, optional, default: 0.2
                Must be between 0 and 1. The `PercentRange` determines what percent error the fit model can have in regards to the amplitude and position of fit curves under found peaks.
            Sigma : int, optional, default: 15
                The expected width of fit curves, in terms of data points
            SigmaMin : int, optional, default: 3
                The expected minimum width allowed of fit curves, in terms of data points
            SigmaMax : int, optional, default: 100
                The expected maximum width allowed of fit curves, in terms of data points
        '''

        self.file       = file
        self.cmp        = colormap
        self.delimiter  = delimiter
        self.range      = raman_range
        self.bins       = bins
        self.dispName   = display_name
        self.resolution = resolution            # Resolution of images and videos
        self.figsize    = (16,9)                # Default Image Ratio 16:9
        self.makeVideo  = makeVideo             # (bool) Make a video output
        self.makePlot   = makePlot              # (bool) Make a plot output
        self.DPI        = 0
        self.FPS        = FPS
        self.xAxisTitle = xAxisTitle
        self.yAxisTitle = yAxisTitle
        self.xRamanTitle= xRamanTitle
        self.yRamanTitle= yRamanTitle
        self.plotType   = plotType
        self.output_path= output_path
        self.image_given= False
        self.alpha      = alpha

        if not provided_img == None:
            self.image          = mpimg.imread( provided_img )
            self.image_given    = True

        self.data       = None
        self.x          = None
        self.y          = []
        self.datapoints = []

        self.strtIndice = 0
        self.stopIndice = 0

        self.X          = None
        self.Y          = None
        self.Z          = None

        self.min_x      = 0.
        self.min_y      = 0.
        self.max_x      = 0.
        self.max_y      = 0.
        self.animFrames = 0

        self.aveRaman   = []

        # Set DPI from input resolution
        if self.resolution == '4K' or self.resolution == '4k':
            self.DPI    = int( 3840/self.figsize[0] )
        elif self.resolution == '1080p' or self.resolution == '1080P':
            self.DPI    = int( 1920/self.figsize[0] )
        elif self.resolution == '720p' or self.resolution == '720P':
            self.DPI    = int( 1280/self.figsize[0] )
        elif self.resolution == '480p' or self.resolution == '480P':
            self.DPI    = int( 848/self.figsize[0] )
        elif self.resolution == '360p' or self.resolution == '360P':
            self.DPI    = int( 640/self.figsize[0] )
        elif self.resolution == '240p' or self.resolution == '240P':
            self.DPI    = int( 426/self.figsize[0] )
        else:
            # Default to 4K
            self.DPI        = int( 3840/self.figsize[0] )
            self.resolution = '4k'
            print( "The entered resolution is not an option!\nDefaulting to 4K" )


        # Check plot type
        if not self.plotType.lower() == 'contour' and not self.plotType.lower() == 'imshow':
            print( "The entered plot type is not supported!\nOnly 'contour' and 'imshow' are supported.\nDefaulting to 'contour'" )
            self.plotType = 'contour'

        # Open File
        self._readFile()

        # Find Indicides
        self.updateIndices()

        if self.makePlot:

            # Calculate Z values
            self._calculateMap( start = self.strtIndice, stop = self.stopIndice )

            # Plot map
            self._plot()

        if self.makeVideo:
            # Make video
            self.animate()

    # Parses file into useable data
    def _readFile( self ):

        self.data       = np.genfromtxt( self.file, delimiter = self.delimiter )

        #Get all x data points
        x_datapoints    = self.data[ 1:, 0 ]
        y_datapoints    = self.data[ 1:, 1 ]


        self.x          = self.data[ 0, 2: ]

        for i in range( len( x_datapoints ) ):

            self.y.append( self.data[ i+1, 2: ] )

        self.y          = np.array( self.y )
        
        # Get x and y range
        y_range         = np.count_nonzero( x_datapoints == x_datapoints[0] )
        x_range         = np.count_nonzero( y_datapoints == y_datapoints[0] )

        self.X          = x_datapoints.reshape( x_range, y_range ).T
        self.Y          = y_datapoints.reshape( x_range, y_range ).T
        self.Y          = self.Y[::-1]

        # Fix Y being upside down
        self.Y          = self.Y.T
        self.Y          = self.Y.T

        self.datapoints = np.array( [ x_datapoints, y_datapoints ] )

        # Initialize Z
        self.Z          = np.zeros( (y_range, x_range) )

    # Returns indice of closest value
    def getIndex( self, val = 0 ):

        return ( np.abs( self.x - val ) ).argmin()

    # Updates the global start and stop indices for the raman data
    def updateIndices( self ):
        
        if self.range is None:

            self.strtIndice     = 0
            self.stopIndice     = len( self.x )-1
            self.range          = [ self.x[self.strtIndice], self.x[self.stopIndice] ]

        else:
            # Find indices of closest values
            self.strtIndice     = self.getIndex( self.range[0] )
            self.stopIndice     = self.getIndex( self.range[1] )

        self.animFrames     = len( self.x[ self.strtIndice:self.stopIndice ] )-1

    def _calculateMap( self, start = 0, stop = 1 ):

        # Find average values in range
        temp_y          = self.y[:, start:stop ]
        ave_values      = np.mean( temp_y, axis = 0 )

        y_range         = len( self.Z )
        x_range         = len( self.Z[0] )

        # Calculate Z values
        for i in range( x_range ):
            for j in range( y_range ):
                self.Z[j][i]    = np.sum( ( temp_y[i*x_range + j] - ave_values )**2. )

    # Maximize Plot output
    def plt_maximize( self ):
        # See discussion: https://stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python
        backend = plt.get_backend()
        cfm     = plt.get_current_fig_manager()

        if backend == "wxAgg":
            cfm.frame.Maximize(True)

        elif backend == "TkAgg":
            if system() == "Windows":
                cfm.window.state( "zoomed" )  # This is windows only
            else:
                cfm.resize( *cfm.window.maxsize() )

        elif backend == "QT4Agg":
            cfm.window.showMaximized()

        elif callable(getattr(cfm, "full_screen_toggle", None)):
            if not getattr(cfm, "flag_is_max", None):
                cfm.full_screen_toggle()
                cfm.flag_is_max = True

        else:
            raise RuntimeError("plt_maximize() is not implemented for current backend:", backend)

    # Creates Plot of defined range
    def _plot( self ):
       

        self.fig, (self.ax1, self.ax2) = plt.subplots( 2, 1, figsize = self.figsize, dpi = self.DPI )

        self.ax1.set_xlabel( self.xAxisTitle )
        self.ax1.set_ylabel( self.yAxisTitle )

        self.ax2.set_xlabel( self.xRamanTitle )
        self.ax2.set_ylabel( self.yRamanTitle )
        
        for raman in self.y:

            self.ax2.plot( self.x[ self.strtIndice: self.stopIndice ], raman[ self.strtIndice: self.stopIndice ], lw = 0.5 )


        max_Z       = np.max( self.Z )
        min_Z       = np.min( self.Z )
        steps_size  = ( max_Z - min_Z )/self.bins
        levels      = np.arange( np.min( self.Z ), np.max( self.Z ), steps_size )
        norm        = cm.colors.Normalize( vmax = max_Z, vmin = min_Z )
        cmap        = self.cmp

        alpha       = 1.
        extent      = np.min( self.X ), np.max( self.X ), np.min( self.Y ), np.max( self.Y )
        if self.image_given:
            alpha   = self.alpha
            self.ax1.imshow( self.image, extent = extent, aspect = 'auto' )
        
        if self.plotType.lower() == 'contour':
            cset        = self.ax1.contourf(self.X, self.Y, self.Z, levels, norm = norm, cmap = cm.get_cmap( cmap, len( levels ) - 1), alpha = alpha )
            im = self.ax1.contour( self.X, self.Y, self.Z, cset.levels, colors = 'k', linewidths = 0.5 )
        else:
            
            im = self.ax1.imshow( self.Z, cmap = self.cmp, interpolation = 'gaussian', extent = extent, aspect = 'auto', alpha = alpha )

        divider     = make_axes_locatable( self.ax1 )
        cax         = divider.append_axes( 'right', size = '5%', pad = 0.05 )

        self.fig.colorbar( im, cax = cax, orientation = 'vertical' )

        self.fig.suptitle( f"{self.dispName} map from {self.x[self.strtIndice]} to {self.x[self.stopIndice]} cm^-1" )
        self.fig.savefig( f"{self.dispName}_2" )
        #mng = plt.get_current_fig_manager()
        #mng.frame.Maximize(True)  
        self.plt_maximize()
        plt.show()


    def updateAnimation( self, i ):
        
        # Update indices
        tmp_strtIndice  = self.strtIndice + i
        tmp_stopIndice  = tmp_strtIndice + 1

        # Update Range
        #self.range[0]   = self.x[ tmp_strtIndice ]
        #self.range[1]   = self.x[ tmp_stopIndice ]

        # Recalculate Z
        self._calculateMap( start = tmp_strtIndice, stop = tmp_stopIndice )

        alpha       = 1.
        extent      = np.min( self.X ), np.max( self.X ), np.min( self.Y ), np.max( self.Y )

        # Clear prior plots
        if i>0:
            self.ax1.clear()
            self.cbar.remove()

        if self.image_given:
            alpha   = self.alpha
            self.ax1.imshow( self.image, extent = extent, aspect = 'auto' )

        self.ax1.clear()
        if self.plotType.lower() == 'contour':
            im = self.ax1.contourf(self.X, self.Y, self.Z, cmap = self.cmp, alpha = alpha )
        else:
            im = self.ax1.imshow( self.Z, cmap = self.cmp, interpolation = 'gaussian', extent = extent, aspect = 'auto', alpha = alpha )
        
        divider     = make_axes_locatable( self.ax1 )
        cax         = divider.append_axes( 'right', size = '5%', pad = 0.05 )
        self.cbar   = self.fig.colorbar( im, cax = cax, orientation = 'vertical' )
        self.cbar.set_ticks([])

        self.line[0].set_data( [ self.x[tmp_strtIndice], self.x[tmp_strtIndice] ], [ 0, self.max_y ] )

        print( f"--- Frame {i+2}/{self.animFrames} - {round( 100.*(i+2)/( self.animFrames ), 2 )}% ---" )

        return self.line
    
    # Animates over the defined range to show differences
    def animate( self ):

        y_cpy       = self.y[ :, self.strtIndice: self.stopIndice ] 
        
        self.max_y  = np.max( y_cpy )

        self.fig, (self.ax1, self.ax2) = plt.subplots( 2, 1, figsize = self.figsize, dpi = self.DPI )

        self.ax1.set_xlabel( self.xAxisTitle )
        self.ax1.set_ylabel( self.yAxisTitle )

        self.ax2.set_xlabel( self.xRamanTitle )
        self.ax2.set_ylabel( self.yRamanTitle )

        # build first instance of Ax1


        line1,      = self.ax2.plot( [ self.x[self.strtIndice], self.x[self.strtIndice] ], [ 0, self.max_y ], lw = 1, ls = '--', color = 'r' )
        
        self.line   = [ line1 ]

        # Now append the static plots
        for raman in self.y:

            self.line.append( self.ax2.plot( self.x[ self.strtIndice: self.stopIndice ], raman[ self.strtIndice: self.stopIndice ], lw = 0.5 )[0] )

        # Initialize the animation function
        anim    = animation.FuncAnimation(self.fig, self.updateAnimation,
                               frames = self.animFrames-1, interval = 1, blit = True )

        # Set Encoder and FPS
        vid     = animation.FFMpegWriter( fps = self.FPS )
        
        anim.save( os.path.join( self.output_path, f"{self.dispName}.mp4"), writer = vid )

if __name__ == "__main__":

    here    = os.path.abspath( os.path.dirname( __file__ ) )
    fname   = os.path.join( here, 'sample_map', 'sample.csv' )
    img     = os.path.join( here, 'sample_map', 'image.JPG' )
    MP      = Mapper( file = fname, display_name = "K2CoS2 Sample 11", output_path = os.path.join( here, 'sample_map' ), delimiter = ',', provided_img=img, makePlot=False, makeVideo=True, plotType='imshow', resolution = '4k')
    #MP.animate()
    #MP._plot()