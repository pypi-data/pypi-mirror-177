from loko_client.utils.gobjects_utils import GObject


class Nodes:
    """
        Nodes contained by a Loko tab.

        Args:
            nodes (dict): Dictionary containing the nodes ids as keys. Each node is a
                :py:meth:`~loko_client.utils.gobjects_utils.GObject`.
    """
    def __init__(self, nodes):
        self.nodes = {node['id']: GObject('Node', **node) for node in nodes}

    def all(self):
        """ Return all nodes' ids. """
        return list(self.nodes.keys())

    def search(self, key, value):
        """ Search for specific nodes using a condition.

            Example:
                >>> GATEWAY = 'http://localhost:9999/routes/'
                >>> pclient = ProjectsClient(gateway=GATEWAY)
                >>> ### get all nodes contained by the project first_project and tab main
                >>> nodes = pclient.get_project('first_project').tabs.main.nodes
                >>> ### get all 'HTTP REQUEST' nodes
                >>> print(list(nodes.search('data.name', 'HTTP Request')))

            Args:
                key (str): Node's attribute. Use dot notation to concatenate nested keys.
                value: Value that the node's attribute must assume.
        """
        for _id,node in self.nodes.items():
            val = node
            for k in key.split('.'):
                val = val.get(k)
                if not val:
                    break
            if val==value:
                yield _id

    def __getitem__(self, item):
        return self.nodes[item]


class Edges:
    """
        Edges contained by a Loko tab.

        Args:
            edges (dict): Dictionary containing the edges ids as keys. Each edge is a
                :py:meth:`~loko_client.utils.gobjects_utils.GObject`.
        """
    def __init__(self, edges):
        self.edges = {edge['id']: GObject('Edge', **edge) for edge in edges}

    def all(self):
        """ Return all edges' ids. """
        return list(self.edges.keys())


class Project:
    """
        A Loko project.

        Attributes:
            name (str): The project name.
            id (str): The id of the project.
            description (str): The project description.
            created_on (str): The creation date: ``%d/%m/%Y, %H:%M:%S``.
            last_modify (str): The last modify date: ``%d/%m/%Y, %H:%M:%S``.
            graphs (dict): Tabs flows.
            open (List[str]): The opened tabs.
            active (str): The name of the active tab.
            version (str): Loko version.
            deployed (bool): `True` if the project is deployed.
            tabs (GObject): Object containing the name of the project's tabs as attributes. Each tab is a
                :py:meth:`~loko_client.utils.gobjects_utils.GObject` containing
                :py:meth:`~loko_client.model.projects.Nodes` and
                :py:meth:`~loko_client.model.projects.Edges` information.
            """
    def __init__(self, name, id, description, created_on, last_modify, graphs, open, active, version, deployed=None,
                 **kwargs):
        self.name = name
        self.id = id
        self.description = description
        self.created_on = created_on
        self.last_modify = last_modify
        self.open = open
        self.active = active
        self.version = version
        self.deployed = deployed

        self.graphs = graphs

        self.tabs = GObject('Tabs', **{name: GObject('Tab', nodes=Nodes(tab['nodes']), edges=Edges(tab['edges']))
                                       for name,tab in self.graphs.items()})




