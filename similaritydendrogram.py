"""
similaritydendrogram.py

Read sim matrix output and plot its equivalent dendrogram.

Requirements:
    python
    scipy
    matplotlib
    numpy 
"""

from scipy.cluster.hierarchy import dendrogram, linkage  
import matplotlib.pyplot as plt
import numpy as np


class Similarity():
    def __init__(self, matrix_fn):
        self.matrix_fn = matrix_fn
        
    def get_players(self):
        """ Returns player name list """  
        players = []
        read_line = False
        
        with open(self.matrix_fn) as f:
            for lines in f:
                line = lines.strip()
                if line == '':
                    if read_line:
                        break
                    else:
                        continue
                if line.startswith('1)'):
                    read_line = True
                
                if read_line:
                    a = line.split(')')[1].strip().split('(')[0].strip()
                    players.append(a)
                    
        return players
    
    def get_max_similarity(self):
        """
        Read matrix_fn file and returns the max sim value
        """
        sim_max = -1.0
        read_line = False
        
        with open(self.matrix_fn) as f:
            for lines in f:
                line = lines.strip()
                if line.startswith('1.'):
                    read_line = True
                
                if read_line: 
                    if line == '':
                        continue
                    sp = line.split()
                    for n in sp:
                        if '-' in n:
                            continue
                        if float(n) > sim_max:
                            sim_max = float(n)
                            
        return sim_max
    
    def get_similarity(self):
        """
        Read matrix_fn file and returns similarity matrix
        """
        sim_max = min(100.0, self.get_max_similarity() + 1.0)
        sim = []
        data = []
        read_line = False
        
        with open(self.matrix_fn) as f:
            for lines in f:
                a = []
                line = lines.strip()
                if line.startswith('1.'):
                    read_line = True
                
                if read_line: 
                    if line == '':
                        continue
                    sp = line.split()
                    for n in sp:
                        if '-' in n:
                            a.append(str(sim_max))  
                        else:
                            a.append(n)
                    data.append(a)
                
        for d in data:
            # Delete first element since it is not a similarity value.
            # It is only an index no. i.e 1 in [1, 50.0 ...]
            del d[0]
            b = [int(float(i)) for i in d]
            sim.append(b)
            
        return sim
    
    def get_dendrogram(self, dist_method='ward', fig_xlim=5, fig_ylim=9,
                       plot_xlim=None, image_fn='dendrogram.png',
                       image_dpi=600):
        """
        Plot dendrogram based from matrix_fn 
        """
        players = self.get_players()    
        similarity = self.get_similarity()
            
        np_data = np.array(similarity)
            
        # Methods [single, complete, average, weighted, ...] and others see
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
        linked = linkage(np_data, method=dist_method)
        
        nr = range(1, len(similarity)+1)
        
        label = ['[' + str(n) + '] ' + p for n, p in zip(nr, players)]
        
        plt.figure(figsize=(fig_xlim, fig_ylim))
        dendrogram(linked,  
                    orientation='right',
                    labels=label,
                    distance_sort='descending',
                    leaf_rotation=0.,
                    show_leaf_counts=True)
        plt.title('Hierarchical Clustering Dendrogram\nmethod={}'.
                  format(dist_method), size=14)
        plt.xlabel('Distance (lower more similar)', size=10)
        plt.xticks(fontsize=10, rotation=0)
        plt.yticks(fontsize=10)
        if plot_xlim is not None:
            plt.xlim(0, plot_xlim)

        plt.savefig(image_fn, bbox_inches='tight', dpi=image_dpi)
        plt.show()


def main():  
    matrix_fn = 'matrix.txt'
    s = Similarity(matrix_fn)
    s.get_dendrogram(dist_method='ward', fig_xlim=10, fig_ylim=8,
                     plot_xlim=None, image_fn='similarity_dendrogram.png',
                     image_dpi=300)


if __name__ == '__main__':
    main()
    