import pandas as pd
import numpy as np

class BrainRegionSignalStatisticsCalculator:

    def __init__(self, annotation_volume_path, signal_volume_path, structures_df_path, statistics_df_path):
        self.annotation_volume = np.load(annotation_volume_path)['arr_0']
        self.signal_volume = np.load(signal_volume_path)['arr_0']
        structures_df = pd.read_csv(structures_df_path, index_col=0).set_index(['id'])
        self.statistics_df_path = statistics_df_path
        
        self.all_labels = list(set(structures_df.index.values.tolist()))
        self.children_map, self.parents_map, self.children_count_map = self._construct_graph(self.all_labels, structures_df)
        self.leaf_nodes = [ label for label in self.all_labels if self.children_count_map[label] == 0 ]
        print("# of leaf nodes without any children:", len(self.leaf_nodes))
        
        self.digits = 4

    def calculate(self):
        """
        Compute statistics in child-->parent-->grandparent order
        """
        statistics = self._compute_leaf_region_stat()

        queue = [ node for node in self.leaf_nodes]
        while queue:
            cur = queue.pop()

            children_stat = {}
            for child in self.children_map[cur]:
                if statistics[child]['count'] != None:
                    children_stat[child] = statistics[child]

            if children_stat:
                statistics[cur] = self._compute_children_stat(children_stat)

            for parent in self.parents_map[cur]:
                self.children_count_map[parent] -= 1
                if self.children_count_map[parent] == 0:
                     queue.append(parent)

        # save statistics to csv file   
        statistics_df = pd.DataFrame.from_dict(statistics, orient ='index')
        statistics_df.index.name = 'id'
        statistics_df.to_csv(self.statistics_df_path, header=True)

        return statistics

    def _construct_graph(self, all_labels, structures_df):
        """ 
        Construct graph
            children_map: store descendants that one-level away from current node 
            parents_map: store parent nodes that one-level away from current node 
            children_count_map: the number of children of each node
        """
        pathes = ([' '.join(path.split('/')).split() 
            for path in structures_df['structure_id_path'].tolist()])

        children_map = {label: set() for label in all_labels}
        parents_map = {label: set() for label in all_labels}
        children_count_map = {label: 0 for label in all_labels}

        for path in pathes:
            for index in range(len(path) - 1):
                parent = int(path[index])
                child = int(path[index + 1])
                children_map[parent].add(child)
                parents_map[child].add(parent)
                
        for label in children_count_map:
            children_count_map[label] = len(children_map[label])
                
        return children_map, parents_map, children_count_map

    def _compute_leaf_region_stat(self):
        """
        Compute the brain statistics for leaf nodes
        Assign None to missing regions
        """
        if self.annotation_volume.shape != self.signal_volume.shape:
            print("The size of input singal volume doesn't match the annotation volume! ")
        
        labels = np.unique(self.annotation_volume)
        print("# of unique labels in anaotation volume:", len(labels))

        # examine the correctness of labels in anaotation volume 
        # valid_labels: removing the non-leaf nodes 
        valid_labels = []
        invalid_labels = []
        
        for i in labels:
            if i in self.leaf_nodes:
                valid_labels.append(i)
            else:
                invalid_labels.append(i)
        print("# of valid labels in anaotation volume:", len(valid_labels))
        print("# of invalid labels in anaotation volume:", len(invalid_labels))
        
        statistics = { label: {
            'mean':None, 
            'min': None, 
            'max': None, 
            'sum': None, 
            'count': None
        } for label in self.all_labels }

        for label in valid_labels:
            if label < 1:
                continue

            volume = self.signal_volume[self.annotation_volume == int(label)]
            if len(volume) > 0:
                statistics[label]['mean'] = round(np.mean(volume), self.digits)
                statistics[label]['min'] = round(np.min(volume), self.digits)
                statistics[label]['max'] = round(np.max(volume), self.digits)
                statistics[label]['sum'] = round(np.sum(volume), self.digits)
                statistics[label]['count'] = np.count_nonzero(
                    self.annotation_volume == label)
                
        return statistics

    def _compute_children_stat(self, children):
        """
        Compute the statistics of the given node based on its descendants        
        """
        children_values = children.values()
        
        cur_min = round(min([child['min'] for child in children_values]), self.digits)
        cur_max = round(max([child['max'] for child in children_values]), self.digits)
        cur_sum = round(sum([child['sum'] for child in children_values]), self.digits)
        cur_count = sum([child['count'] for child in children_values])        
        cur_mean = round(cur_sum/cur_count, self.digits)

        return { 
            'mean': cur_mean, 
            'min': cur_min, 
            'max': cur_max, 
            'sum': cur_sum, 
            'count': cur_count,
        }