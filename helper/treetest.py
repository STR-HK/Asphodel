import os

os.environ["PATH"] += os.pathsep + "C:\\Program Files\\Graphviz 2.44.1\\bin"

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from graphviz.backend import view

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)


from anytree.dotexport import RenderTreeGraph

RenderTreeGraph(udo).to_picture("tree.png")
