from Vertex import Vertex
import logging

logging.basicConfig(filename='test.log', level=logging.DEBUG)


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    @property
    def project_duration(self):
        time_g = self.graph_time()
        return time_g

    def graph_time(self):
        all_paths = []
        s = "start"
        f = "finish"
        g_time = 0
        all_paths = self.find_all_paths(s, f, all_paths)
        critical_dic = self.find_critical_path(all_paths, False)
        for name in critical_dic:
            g_time = g_time + critical_dic[name]

        logging.debug('returning graph time : {}'.format(g_time))
        return g_time

    def add_vertex(self, name, duration):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(name, duration)
        self.vert_dict[name] = new_vertex
        logging.debug('Add: vertex {}'.format(name))
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to):
        # Check if activity exists
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)
        cost = self.vert_dict[to].duration
        self.vert_dict[frm].add_neighbor(self.vert_dict[to].name, cost)
        logging.debug('Add edge between: {} and {}'.format(frm, to))

    def get_vertices(self):
        return self.vert_dict.keys()

    def remove_edge(self, name):
        if name not in self.vert_dict:
            logging.debug('vertex: {} not in graph'.format(name))
            return

        if name == "start" or name == "finish":
            logging.debug('cannot remove start or finish vertex')
            return
        neighbors_list = list(self.vert_dict[name].adjacent.keys())
        if not neighbors_list:
            del self.vert_dict[name]
            logging.debug('edges from vertex: {} not exist, vertex {} successfully removed'.format(name, name))
            return

        predecessor_list = [n for n in self.vert_dict]
        edges_to_add = []
        for v in predecessor_list:
            if name in self.vert_dict[v].adjacent:
                for n in neighbors_list:
                    self.add_edge(v, n)
                del self.vert_dict[v].adjacent[name]

        del self.vert_dict[name]
        logging.debug('vertex: {} successfully removed'.format(name))
        self.num_vertices -= 1

    def find_isolate(self):
        item_list = [n for n in self.vert_dict]
        isolat_set = set()
        for i in item_list:
            if not self.vert_dict[i].adjacent:
                isolat_set.add(i)

        for i in item_list:
            found = False
            for n in self.vert_dict:
                if i in self.vert_dict[n].adjacent:
                    found = True
                    break
            if not found:
                isolat_set.add(i)

        logging.debug('isolated vertexs : {}'.format(isolat_set))
        return isolat_set

    def find_all_paths(self, start_vertex, end_vertex, path):
        graph = self.vert_dict
        path = path + [start_vertex]
        item_list = [n for n in self.vert_dict]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            logging.debug('there no start vertex')
            return []
        paths = []
        for v in graph[start_vertex].adjacent:
            if v not in path:
                extended_paths = self.find_all_paths(v,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        logging.debug('return all paths in graph from {} vertex to {} vertex'.format(start_vertex, end_vertex))
        return paths

    def find_critical_path(self, all_paths, is_cycle):

        max_sum = 0
        path_sum = 0
        location = {}
        if is_cycle:
            logging.debug('there is a cycle in the cpm so ciritical path does not exist')
            location = {}
            return location

        for temp_path in all_paths:
            for v in temp_path:
                path_sum = path_sum + self.vert_dict[v].duration
            if path_sum > max_sum:
                location = {}
                max_sum = path_sum
                for t in temp_path:
                    location[t] = self.vert_dict[t].duration
                # location = temp_path
            path_sum = 0

        logging.debug('returned critical path : {}'.format(location))
        return location

    def get_graph_simplified(self):
        res = {}
        for k, v in self.vert_dict.items():
            res[k] = list(v.adjacent.keys())
        logging.debug('returned simplified display of the graph for cycle method')
        return res

    def dfs(self, graph, start, end):

        fringe = [(start, [])]
        while fringe:
            state, path = fringe.pop()
            if path and state == end:
                yield path
                continue
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path + [next_state]))

    def slack_time(self, start_vertex, end_vertex, is_cycle):
        es = "early_start"
        ef = "early_finish"
        lf = "late_finish"
        ls = "late_start"
        all_paths = []
        all_paths = self.find_all_paths(start_vertex, end_vertex, all_paths)
        critical = self.find_critical_path(all_paths, is_cycle)
        temp_critical = list(critical.keys())
        slack_time_activity = {}
        item_list = [n for n in self.vert_dict]
        dic_es_ef = {}
        dic_ls_lf = {}
        for name in item_list:
            dic_es_ef[name] = {}
            dic_es_ef[name][es] = 0
            dic_es_ef[name][ef] = 0

            dic_ls_lf[name] = {}
            dic_ls_lf[name][ls] = 0
            dic_ls_lf[name][lf] = 0

        dic_es_ef[start_vertex][es] = 0
        dic_es_ef[start_vertex][ef] = self.vert_dict[start_vertex].duration

        for path in all_paths:
            for name_inedx in enumerate(path):
                if name_inedx[0] != 0:
                    if dic_es_ef[path[name_inedx[0]]][es] < dic_es_ef[path[name_inedx[0] - 1]][ef]:
                        dic_es_ef[path[name_inedx[0]]][es] = dic_es_ef[path[name_inedx[0] - 1]][ef]

                    dic_es_ef[path[name_inedx[0]]][ef] = dic_es_ef[path[name_inedx[0]]][es] + self.vert_dict[
                        path[name_inedx[0]]].duration

        dic_ls_lf[end_vertex][lf] = dic_es_ef[end_vertex][ef]
        dic_ls_lf[end_vertex][ls] = dic_ls_lf[end_vertex][lf] - self.vert_dict[end_vertex].duration

        for path in all_paths:
            for i in range(len(path) - 1, 0, -1):
                if i != len(path) - 1:
                    if dic_ls_lf[path[i]][lf] < dic_ls_lf[path[i + 1]][ls]:
                        dic_ls_lf[path[i]][lf] = dic_ls_lf[path[i + 1]][ls]

                    dic_ls_lf[path[i]][ls] = dic_ls_lf[path[i]][lf] - self.vert_dict[path[i]].duration

        slack_item = list(dic_ls_lf.keys())

        for name_inedx in slack_item:
            slack_time_activity[name_inedx] = dic_ls_lf[name_inedx][ls] - dic_es_ef[name_inedx][es]

        for name in temp_critical:
            del slack_time_activity[name]

        sorted(slack_time_activity.values())

        logging.debug('returned slack time  {}'.format(slack_time_activity))

        return slack_time_activity

    def check_cycle(self, check):
        if not check:
            logging.debug('returned false not have cycle')
            is_cycle = False
        else:
            logging.debug('returned true have cycle')
            is_cycle = True
        return is_cycle

    def __str__(self):
        output = "PERT&CPM: \n"
        for item in self.vert_dict:
            output += item + "," '%s' % self.vert_dict[item].duration
            output += "\n"

        output += "\n"
        output += "All vertex connections (edges): \n"
        for item in self.vert_dict:
            output += ('Vertex: %s : %s' % (item, self.vert_dict[item].adjacent))
            output += "\n"

        return output
