import config
import analysis 

import numpy as np
import matplotlib.pyplot as plt
import colorcet
from mpl_toolkits.axes_grid1 import make_axes_locatable
import scipy.stats

# import matplotlib.style as mplstyle
# mplstyle.use('fast')

plt.rc( 'font', ** { 'size' : 6 } ) 


kde_min = -5
kde_max = 5
n_kde_data = 100
n_cbar_ticks = 5

mcp_hitmap_cmap = colorcet.m_rainbow



# all 3 1d histograms have the same functionality.
# it is all implemented here.
class PlotterHist( object ) :

    def __init__( self, ax, title, data, cut_data_indices ) :

        self.ax = ax 
        self.title = title
        self.data = data
        self.cut_data_indices = cut_data_indices 
        self.plot = None
        self.plot_with_cuts = 0
        self.num_cut_data = 0
        self.num_events = 0
        self.n_bins = 0
        self.fit_params = None
        self.fit_bounds = None
        

    def update( self ) : 
        self.ax.clear() 
        self.ax.set_title( self.title )

        if self.plot_with_cuts :
            if self.is_live : 
                valid_indices = self.cut_data_indices[ : self.num_cut_data ]
            else :
                valid_indices = self.cut_data_indices 
            data = self.data[ valid_indices ] 
        else :
            data = self.data[ : self.num_events ]
        
        bins = self.n_bins
        if bins == 0 :
            bins = 'doane'

        if self.fit_params is not None :
            density = 0
            x = np.linspace( * self.fit_bounds, 100 ) 
            self.ax.plot( x, analysis.gaussian( self.fit_params, x ),
                              c = 'r' )
            # self.hist_fit_added = 1 
        else :
            density = 0 
            
        self.hist, self.bins, _ = self.ax.hist( data, bins = bins, density = density )

        
    def set_data_params( self, num_events, num_cut_data ) :
        self.num_events = num_events
        self.num_cut_data = num_cut_data

        
    def apply_fit( self, bounds ) :
        ret = analysis.fit_gaussian( self.bins[:-1], self.hist, bounds )
        print( ret )

        if ret is None :
            self.fit_params = None
            self.fit_bounds = None
            return 
        
        self.fit_params = ret[0]
        self.fit_bounds = bounds
        return ret 

    
    def remove_fit( self ) :
        self.fit_params = None


        

class Plotter( object ) :

    def __init__( self, cpt_data ) :

        self.cpt_data = cpt_data

        self.f, self.axarr = plt.subplots( 2, 2 )
        self.f.subplots_adjust( hspace = 0.5, wspace = 0.5 )
        
        self.init_mcp_hitmap( self.axarr[0][0], self.f )
        
        self.tof_hist = PlotterHist( self.axarr[0,1], 'TOF', self.cpt_data.tofs,
                                     self.cpt_data.cut_data_indices )

        self.radius_hist = PlotterHist( self.axarr[1,0], 'Radius', self.cpt_data.radii, 
                                        self.cpt_data.cut_data_indices ) 
        
        self.angle_hist = PlotterHist( self.axarr[1,1], 'Angle', self.cpt_data.angles,
                                       self.cpt_data.cut_data_indices ) 

        self.all_hists = [ self.tof_hist, self.radius_hist, self.angle_hist ] 

        
        self.plot_with_cuts = 0

        self.use_kde = 0 
        self.kde_bandwidth = 0.003
        self.mcp_bin_width = 0.25
        self.mcp_x_bounds = [ -5.0, 5.0 ]
        self.mcp_y_bounds = [ -5.0, 5.0 ]

        self.tof_hist_nbins = 0
        self.r_hist_nbins = 0
        self.angle_hist_nbins = 0

        self.tof_fit_params = None
        self.radius_fit_params = None
        self.angle_fit_params = None



    # deallocate matplotlib resources 
    def release( self ) : 
        self.f.clear() 
    

        
    def update_mcp_hitmap( self ) :

        self.mcp_hitmap_plot = self.axarr[0][0]
        
        if self.plot_with_cuts : 
            valid_indices = self.cpt_data.cut_data_indices[ : self.cpt_data.num_cut_data ]
            data = self.cpt_data.mcp_positions[ valid_indices ] 
        else :
            data = self.cpt_data.mcp_positions[ : self.cpt_data.num_events ]

        xbins = np.arange( self.mcp_x_bounds[0], self.mcp_x_bounds[1]
                           + self.mcp_bin_width / 2,
                           self.mcp_bin_width )
        ybins = np.arange( self.mcp_y_bounds[0], self.mcp_y_bounds[1]
                           + self.mcp_bin_width / 2,
                           self.mcp_bin_width )

        if self.rebuild_mcp_plot :
            self.rebuild_mcp_plot = 0
            self.mcp_hitmap_plot.clear()
            if  self.mcp_hitmap_cbar : 
                self.mcp_hitmap_cbar.ax.clear() 
            # if self.mcp_hitmap_cbar is not None : 
            #     self.mcp_hitmap_cbar.clear() 
            
            title = 'MCP Hitmap'
            self.mcp_hitmap_plot.set_title( title )
            self.mcp_hitmap_plot.set_xlabel( 'X' )
            self.mcp_hitmap_plot.set_ylabel( 'Y' ) 

            image, xedges, yedges, self.mcp_hitmap_im = self.mcp_hitmap_plot.hist2d(
                data[:,0], data[:,1], ( xbins, ybins ),
                cmap = mcp_hitmap_cmap # , range = ( (-100,100), (-100,100) )
            )
            
            xticks = xedges[:: len(xedges) // 5 ]
            yticks = yedges[:: len(yedges) // 5 ]
            
            self.mcp_hitmap_plot.set_xticks( xticks ) 
            self.mcp_hitmap_plot.set_yticks( yticks ) 
            self.mcp_hitmap_plot.set_xlim( xedges[0], xedges[-1] ) 
            self.mcp_hitmap_plot.set_ylim( yedges[0], yedges[-1] )
            
        
            self.mcp_hitmap_plot.grid()

            if not self.mcp_hitmap_cbar :
                divider = make_axes_locatable( self.mcp_hitmap_plot ) 
                self.mcp_hitmap_cax = divider.append_axes("right", size="5%", pad=0.05)
                self.mcp_hitmap_cbar = self.mcp_hitmap_f.colorbar( self.mcp_hitmap_im,
                                                               cax = self.mcp_hitmap_cax )
            else :
                self.mcp_hitmap_cbar = self.mcp_hitmap_f.colorbar( self.mcp_hitmap_im,
                                                               cax = self.mcp_hitmap_cbar.ax )
                
            # self.mcp_hitmap_cbar.set_ticks( np.arange( n_cbar_ticks ) )
            # self.mcp_hitmap_cbar.set_clim( 0, 0 )
        
        else : 
            if not self.use_kde :
                # xbins = np.linspace( * self.mcp_x_bounds, self.mcp_bin_width + 1 ) 
                # ybins = np.linspace( * self.mcp_y_bounds, self.mcp_bin_width + 1 )                
                xbins = np.arange( self.mcp_x_bounds[0], self.mcp_x_bounds[1]  + self.mcp_bin_width / 2,
                                   self.mcp_bin_width )
                ybins = np.arange( self.mcp_y_bounds[0], self.mcp_y_bounds[1]  + self.mcp_bin_width / 2,
                                   self.mcp_bin_width )
                image, xedges, yedges = np.histogram2d( data[:,0], data[:,1], bins = ( xbins, ybins ) )
                
            else :
                # kernel = scipy.stats.gaussian_kde( [ [1]*4, [1]*4 ], bw_method = 0.005 )
                try : 
                    kernel = scipy.stats.gaussian_kde( data, bw_method = 0.003 )
                except :
                    print( 'Warning: KDE computation failed...' )
                    return
            
                x = np.linspace( kde_min, kde_max, n_kde_data + 1 )
                y = np.linspace( kde_min, kde_max, n_kde_data + 1 )
            
                xx, yy = np.meshgrid( x, y )
                positions = np.vstack([xx.ravel(), yy.ravel()])
                image = ( np.reshape( kernel( positions ).T, xx.shape)
                          * len( self.cpt_data.candidate_mcp_positions[0] ) )

            self.mcp_hitmap_im.set_data( image.T ) 
            
        image_min = np.min( image )
        image_max = np.max( image ) 
        ticks = np.linspace( image_min, image_max, n_cbar_ticks, dtype = int )
        
        self.mcp_hitmap_cbar.set_clim( image_min, image_max )
        self.mcp_hitmap_cbar.set_ticks( ticks )
        self.mcp_hitmap_cbar.draw_all()


         
        
        
    def init_mcp_hitmap( self, ax, f ) :
        
        self.mcp_hitmap_f = self.f
        self.rebuild_mcp_plot = 1
        self.mcp_hitmap_cbar = None
        self.mcp_hitmap_cax = None


    # def init_r_plot( self, ax ) :
    #     self.r_plot = self.axarr[1][0]
        

        
    # def update_r_plot( self ) :
        

    
    
    # def init_theta_plot( self, ax ) :
    #     self.theta_plot = self.axarr[1][1]
        

        
    # def update_theta_plot( self ) :
    #     self.theta_plot = self.axarr[1][1]
    #     self.theta_plot.clear()

    #     if self.plot_with_cuts : 
    #         valid_indices = self.cpt_data.cut_data_indices[ : self.cpt_data.num_cut_data ]
    #         data = self.cpt_data.angles[ valid_indices ] 
    #     else :
    #         # valid_indices = self.cpt_data.candidate_indices[ : self.cpt_data.num_candidate_data ]
    #         data = self.cpt_data.angles[ : self.cpt_data.num_events ]
            
    #     bins = self.angle_hist_nbins
    #     if bins == 0 :
    #         bins = 'fd'

    #     self.theta_plot.set_title( r'Angle (deg)' ) 
    #     self.theta_plot.hist( data, bins = bins )


    # def apply_angle_fit( self, bounds ) :
    #     pass

    # def remove_angle_fit( self, bounds ) :
    #     pass 
        
    def update_all( self ) :
        self.update_mcp_hitmap()
        for hist in self.all_hists :
            if self.cpt_data.is_live : 
                hist.set_data_params( self.cpt_data.num_events, self.cpt_data.num_cut_data ) 
            hist.update()

            
    def set_plot_with_cuts( self, plot_with_cuts ) :
        self.plot_with_cuts = plot_with_cuts 
        for hist in self.all_hists : 
            hist.plot_with_cuts = plot_with_cuts 

        
        
    # def init_coords_plots( self, axarr ) :
    #     self.coords_plots = axarr

        
    # def update_coords_plots( self ) :

    #     titles = [ [ 'X1', 'X2' ], [ 'Y1', 'Y2' ] ]

    #     for i in range(2) :
    #         for j in range(2) :
    #             self.coords_plots[i,j].clear()
    #             self.coords_plots[i,j].set_title( titles[i][j] ) 
                
        

