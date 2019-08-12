"""
similaritydendrogram.py

Read sim matrix output and plot its equivalent dendrogram.

Requirements:
    python 3
    scipy
    matplotlib
    numpy
"""

import logging
import argparse
from scipy.cluster.hierarchy import dendrogram, linkage  
import matplotlib.pyplot as plt
import numpy as np


APP_NAME = 'Similarity Dendrogram'
APP_DESC = 'Read engine similarity matrix and output dendrogram.'
APP_VERSION = '0.2'
APP_NAME_VERSION = APP_NAME + ' v' + APP_VERSION


class Similarity():
    def __init__(self, matrix_fn):
        self.matrix_fn = matrix_fn
        
    def get_test_info(self):
        """
        Read 1st line of input similarity from simex matrix output and return
        the epd test, num_pos of epd and the time in ms
        """
        ret_line = None
        
        with open(self.matrix_fn) as f:
            for lines in f:
                line = lines.strip()
                ret_line = line
                break
            
        return ret_line.split(',')
    
    def get_max_sim_value(self):
        """
        Read matrix file and returns the max sim value
        """
        sim_max = -1.0
        
        num_line = 0
        with open(self.matrix_fn) as f:
            for lines in f:
                num_line += 1
                
                # Skip first line of csv header
                if num_line == 1:
                    continue
                
                line = lines.strip()
                sp = line.split(',')
                
                # Delete the first entry, this is only an engine name.
                del sp[0]
                for n in sp:
                    if '-' in n:
                        continue
                    if float(n) > sim_max:
                        sim_max = float(n)
                                
        logging.info('sim_max: {}'.format(sim_max))

        return sim_max
    
    def get_simex_matrix(self):
        """
        Read matrix in csv and return matrix and players in a list.
        """
        sim_max = min(100.0, self.get_max_sim_value() + 1.0)
        players = []
        sim = []
        data = []
        num_line = 0
        
        with open(self.matrix_fn) as f:
            for lines in f:
                num_line += 1
                
                # Skip the header [epd],num_pos,ms
                if num_line == 1:
                    continue
                
                a = []
                line = lines.strip()
                sp = line.split(',')
                players.append(sp[0].strip())
                
                # Skip first element of n as this is the engine name
                for i, n in enumerate(sp):
                    if i == 0:
                        continue
                    if '-' in n:
                        a.append(str(sim_max))  
                    else:
                        a.append(n)
                data.append(a)
                
        for d in data:
            # Delete first element this is only the name of engine.
            del d[0]
            b = [int(float(i)) for i in d]
            sim.append(b)
            
        return sim, players
    
    def get_dendrogram(self, dist_method='ward', fig_xlim=5, fig_ylim=9,
                       plot_xlim=None, image_fn='dendrogram.png',
                       image_dpi=600):
        """
        Plot dendrogram based from matrix file. 
        """
        logging.info('Plotting dendrogram')
        ti = self.get_test_info()
        epdfn = ti[0].split('\\')[1]
        test_info = 'epd: {}, pos: {}, t(ms): {}'.format(epdfn, ti[1], ti[2])
        
        sim_matrix, players = self.get_simex_matrix()
            
        Z = np.array(sim_matrix)
            
        # Methods [single, complete, average, weighted, ...] and others see
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
        linked = linkage(Z, method=dist_method)
        
        nr = range(1, len(Z)+1)
        
        label = ['[' + str(n) + '] ' + p for n, p in zip(nr, players)]
        
        plt.figure(figsize=(fig_xlim, fig_ylim))
        dendrogram(linked,  
                    orientation='right',
                    labels=label,
                    distance_sort='descending',
                    leaf_rotation=0.,
                    show_leaf_counts=True)
        plt.title('Hierarchical Clustering Dendrogram, method={}\n{}'.
                  format(dist_method, test_info), size=14)
        plt.xlabel('Distance (lower more similar)', size=10)
        plt.xticks(fontsize=10, rotation=0)
        plt.yticks(fontsize=10)
        if plot_xlim is not None:
            plt.xlim(0, plot_xlim)

        plt.savefig(image_fn, bbox_inches='tight', dpi=image_dpi)
        plt.show()


def main():
    parser = argparse.ArgumentParser(description=APP_DESC, epilog=APP_NAME_VERSION)
    parser.add_argument('--input', help='input similarity matrix file',
                        required=True)
    parser.add_argument('--output', help='output dendrogram image file, ' +
                        'default=similarity_dendrogram.png',
                        default='similarity_dendrogram.png',
                        required=False)
    parser.add_argument('--log', help='Records program logging', action='store_true')
    
    args = parser.parse_args()
    inputf = args.input
    outputf = args.output
        
    if args.log:
        logging.basicConfig(filename='simtodendro_log.txt',
                filemode='w', level=logging.DEBUG,
                format='%(asctime)s :: %(levelname)s :: %(message)s')
        
    s = Similarity(inputf)
    s.get_dendrogram(dist_method='ward', fig_xlim=10, fig_ylim=9,
                     plot_xlim=None, image_fn=outputf,
                     image_dpi=300)


if __name__ == '__main__':
    main()
    