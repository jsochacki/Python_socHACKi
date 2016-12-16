"""
Author: John Sochacki
This module is a collection of general utilities that make standard tasks
easier to manage and keep code cleaner.
"""
from tkinter import Tk
from tkinter import Listbox
from tkinter import Label
from tkinter import Button
from tkinter import Frame
from tkinter import TOP, RIGHT, BOTTOM, LEFT, Y, END, SINGLE
from tkinter import Scrollbar
from tkinter import font

import xml.dom.minidom

import os

from tabulate import tabulate

# Required imports if put in sepatate package
# from tabulate import tabluate


class PandasPrinter(object):
    def __init__(self):
        pass

    @staticmethod
    def pd_print(pd):
        print(tabulate(pd, headers='keys', tablefmt='fancy_grid'))


# Required imports if put in sepatate package
# from Sochacki.SochackiUtilityPackage import AttrDict
# from Sochacki.SochackiUtilityPackage import StringListCollector


class HRBOMInformation(object):
    """
    This is a your_company_name_here human readible bill of materials object
    model to facilitate bom creation and manipulation.

    Parameters
    ----------

        None : None
               None?

    Example
    -------

    >>> instance = HRBOMInformation()
    >>> instance.bom_dom.CPN.items = 1231231
    >>> instance.bom_dom.CPN.items = 'CL-00000031231'
    >>> instance.bom_dom.CPN.items = '   aggg text!  why?? '
    >>> instance.bom_dom.CPN
    <Sochacki.SochackiUtilityPackage.StringListCollector at 0xab73a58>
    >>> instance.bom_dom.CPN.items
    ['1231231', 'CL-00000031231', 'aggg text!  why??']
    or
    >>> instance = HRBOMInformation({'sheet1':'val1','sheet2':{}})
    >>> instance.bom_dom.sheet1.items = 1231231
    """
    def __init__(self, *args):
        self._document_name = ''
        self._sheet_names = []
        if len(args) == 2:
            self._column_names_and_order = args[0]
            self._column_names_and_default_values = args[1]
        elif len(args) == 1:
            self._column_names_and_order = args[0]
            self._column_names_and_default_values = {}
            for Key in self._column_names_and_order:
                self._column_names_and_default_values.update({Key: ''})
        else:
            self._column_names_and_order = {'CPN': 0,
                                            'Manufacturer_Name': 1,
                                            'Manufacturer_Part_Number': 2,
                                            'BOM_Quantity_Per_CPN': 3,
                                            'BOM_Quantity_Units': 4,
                                            'BOM_Reference_Designator': 5,
                                            'BOM_Special_Notes_About_CPN': 6,
                                            'General_Notes': 7}
            self._column_names_and_default_values = {'CPN': '',
                                             'Manufacturer_Name': '',
                                             'Manufacturer_Part_Number': '',
                                             'BOM_Quantity_Per_CPN': '',
                                             'BOM_Quantity_Units': ['EAC','LFT'],
                                             'BOM_Reference_Designator': '',
                                             'BOM_Special_Notes_About_CPN': '',
                                             'General_Notes': ''}
        self.create_empty_data_columns()

    @property
    def document_name(self):
        return self._document_name

    @document_name.setter
    def document_name(self, NewName):
        self._document_name = NewName

    @property
    def sheet_names(self):
        return self._sheet_names

    @sheet_names.setter
    def sheet_names(self, NewName):
        self._sheet_names.append(NewName)

    @property
    def column_names_and_order(self):
        return self._column_names_and_order

    @property
    def column_names_and_default_values(self):
        return self._column_names_and_default_values

    def create_empty_data_columns(self):
        for ColumnName in self.column_names_and_order:
            if hasattr(self, 'bom_dom'):
                self.bom_dom.update(
                               AttrDict({ColumnName: StringListCollector()}))
            else:
                self.bom_dom = AttrDict({ColumnName: StringListCollector()})

# Required imports if put in sepatate package
# from Sochacki.SochackiUtilityPackage import AttrDict


class StringListCollector(object):
    """
    This is a helper class for the BOMInformation class and is the data holding
    unit.
    It removes trailing and leading white space as the items it is intended
    to store should not have this but inevitibly will

    Parameters
    ----------
        is_empty : Bool
                   This is a bool that is True if there are not elements and
                   False otherwise.
        item_count : int
                     Returns the number of items in the StrinListCollector
                     instance.
        items : int, float, string
                You can assign this with ints, floats, or strings.
                All assignments will be typecast to string requardless
                and then stripped of trailing and leading whitespace and
                added to the item list.

    Returns
    -------
        items : string (list)
                This is a list of strings where each entry in the list is a
                multicharacter string (typically)

    Example
    -------
    >>> collector = StringListCollector()
    >>> collector.is_empty()
    True
    >>> collector.item_count()
    0
    >>> collector.items()
    0
    >>> collector.items = 1231231
    >>> collector.is_empty()
    False
    >>> collector.item_count()
    1
    >>> collector.items()
    ['1231231']
    >>> collector.items = 1233321
    >>> collector.item_count()
    2
    >>> collector.items()
    ['1231231', '1233321']
    >>> collector.items = ' 1233321 whoops '
    >>> collector.item_count()
    3
    >>> collector.items()
    ['1231231', '1233321', '1233321 whoops']

    TODO
    ----
    Nothing for now
    """
    def __init__(self):
        self._items = []

    # Equivalent to a stack peek
    @property
    def items(self):
        return self._items

    # Equivalent to a stack push
    @items.setter
    def items(self, new_value):
        self._items.append(str(new_value).strip())

    def reset(self, *args):
        self._items = []

    def is_empty(self):
        return self.items == []

    def item_count(self):
        return len(self.items)


class AttrDict(dict):
    """
    This is an attribute dictionary.  It adds dictionary keys to its self
    exposing them as attributes of the instance.  You can assign values
    to the attributes and the dictionary entries are updated or vica versa.
    Make sure that any sub attributes that you want to access from a
    parent attribute using the instance.parent.child syntax is created
    using an AttrDict.

    >>> instance = AttrDict({'parent':AttrDict({'child':'val'})})
    or
    >>> instance = AttrDict({'parent':{}})
    >>> instance.parent = AttrDict({'child':'val'})

    The functionality comes from the following:
        - All python objects internally store their attributes in a dictionary
          that is named __dict__.

        - There is no requirement that the internal dictionary __dict__ would
          need to be "just a plain dict", so we can assign any subclass
          of dict() to the internal dictionary.

        - In our case we simply assign the AttrDict() instance we are
          instantiating (as we are in __init__).

        - By calling super()'s __init__() method we made sure that it
          (already) behaves exactly like a dictionary,
          since that function calls all the dictionary instantiation code.

    Parameters
    ----------
    kwargs : Dict
             This is a single or multilevel dictionary for instantiation

    Example
    -------

    >>> attrinstance = AttrDict()
    >>> attrinstance.foo = 'bar'
    >>> attrinstance
    {'foo': 'bar'}
    >>> attrinstance.bar = 'baz'
    >>> attrinstance
    {'bar': 'baz', 'foo': 'bar'}
    >>> attrinstance.update({'foo': {'bar': 'baz'}})
    >>> attrinstance
    {'bar': 'baz', 'foo': {'bar': 'baz'}}
    >>> attrinstance.foo = {'bar': ['baz', 'huh?']}
    >>> attrinstance
    {'bar': 'baz', 'foo': {'bar': ['baz', 'huh?']}}
    >>> attrinstance.foo
    {'bar': ['baz', 'huh?']}
    >>> attrinstance.foo['bar']
    ['baz', 'huh?']
    >>> attrinstance.foo.bar
    AttributeError: 'dict' object has no attribute 'bar'
    >>> attrinstance.foo = AttrDict({'bar': ['baz', 'huh?']})
    >>> attrinstance
    {'bar': 'baz', 'foo': {'bar': ['baz', 'huh?']}}
    >>> attrinstance.foo.bar
    ['baz', 'huh?']

    Info
    ----

    The implementation used here is the preffered implementation over that over
    the implementation below for the following reasons:

        - No dictionary class methods are shadowed (e.g. .keys() work just fine)

        - Attributes and items are always in sync

        - Trying to access non-existent key as an attribute correctly raises
              AttributeError instead of KeyError

    >>> class AttributeDict(dict):
    >>> def __getattr__(self, attr):
    >>>     return self[attr]
    >>> def __setattr__(self, attr, value):
    >>>     self[attr] = value

    Warning
    -------

    However it does have the following dissadvantages/issues
    (some can be fixed) with a little extra work when you have the time

        - Methods like .keys() will not work just fine if they get
              overwritten by incoming data
              (e.g. instance.keys = {'dictkey':val} will shadow dict.keys)

        - Causes a memory leak in Python < 2.7.4 / Python3 < 3.2.3

        - Pylint goes bananas with E1123(unexpected-keyword-arg)
              and E1103(maybe-no-member)

    """
    def __init__(self, *args, **kwargs):
        # Equivalent in later versions of python but left in the old fashion
        # for backwards compadability
        # super().__init__(*args, **kwargs)
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# Required imports if put in sepatate package
# from tkinter import Tk
# from tkinter import Listbox
# from tkinter import Label
# from tkinter import Button
# from tkinter import Frame
# from tkinter import TOP, RIGHT, BOTTOM, LEFT, Y, END, SINGLE
# from tkinter import Scrollbar
# from tkinter import font


class TkUserListSelect(object):
    """
    A simple box to pop up for user based item selection.
    This is not for file or file path selection, there is another class
    for that

    Example
    -------
    >>> user_list_box = TkUserListSelect(title='Title',
    >>>                                  message='Info For User',
    >>>                                  user_enum=dict(
    >>>      zip([1, 'hi', 'user sees these', 4],
    >>>          [1, 'user doesnt see these',
    >>>          'but they correspond with the keys that the user does see',
    >>>          ' 1:1 by location and are what are returned if desired'])))

    >>> user_list_box.open_frame()
    ...Interaction (user selects 'hi')
    >>> user_list_box.return_index()
    1
    >>> user_list_box.return_index_value()
    'hi'
    >>> user_list_box.return_enum()
    {'hi': 'user doesnt see these'}
    >>> user_list_box.return_value()
    'user doesnt see these'
    """
    def __init__(self, title, message, user_enum):
        self.master = Tk()
        self.value = None
        self._user_presented_list = list(user_enum.keys())
        self._short_bubble_sort()
        self._user_enum = user_enum
        self._current_font_type = 'Times'
        self._current_font_size = 10
        self.font_obj = font.Font(font=(
                            self._current_font_type, self._current_font_size))

        # self.modalPane = Toplevel(self.master)
        self.modalPane = self.master

        # self.modalPane.transient(self.master)
        self.modalPane.grab_set()

        self.modalPane.bind("<Return>", self._choose)
        self.modalPane.bind("<Escape>", self._cancel)

        if title:
            self.modalPane.title(title)

        if message:
            self.message_label = \
                Label(self.modalPane, text=message)
            self.message_label.pack(padx=5, pady=5)

        listFrame = Frame(self.modalPane)
        listFrame.pack(side=TOP, padx=5, pady=5)

        scrollBar = Scrollbar(listFrame)
        scrollBar.pack(side=RIGHT, fill=Y)
        self.listBox = Listbox(listFrame, selectmode=SINGLE)
        self.listBox.pack(side=LEFT, fill=Y)
        scrollBar.config(command=self.listBox.yview)
        self.listBox.config(yscrollcommand=scrollBar.set)
        # self.list.sort()
        for item in self._user_presented_list:
            self.listBox.insert(END, item)

        buttonFrame = Frame(self.modalPane)
        buttonFrame.pack(side=BOTTOM)

        chooseButton = Button(buttonFrame, text="Choose", command=self._choose)
        chooseButton.pack()

        cancelButton = Button(buttonFrame, text="Cancel", command=self._cancel)
        cancelButton.pack(side=RIGHT)

        self.set_font_size('Times', 10)
        self.autowidth(500)

    def set_font_size(self, FONT_TYPE, FONT_SIZE):
        self._current_font_type = FONT_TYPE
        self._current_font_size = FONT_SIZE
        self.font_obj = font.Font(font=(
                            self._current_font_type, self._current_font_size))
        self.message_label.config(font=(
                            self._current_font_type, self._current_font_size))
        self.listBox.config(font=(
                            self._current_font_type, self._current_font_size))

    def autowidth(self, maxwidth):
        pixels = 0
        for item in self.listBox.get(0, "end"):
            pixels = max(pixels, self.font_obj.measure(item))
        # bump listbox size until all entries fit
        pixels = pixels + 10
        width = int(self.listBox.cget("width"))
        for w in range(0, maxwidth+1, 5):
            if self.listBox.winfo_reqwidth() >= pixels:
                break
            self.listBox.config(width=width+w)

    def _short_bubble_sort(self):
        exchanges = True
        passnum = len(self._user_presented_list) - 1
        while (passnum > 0) and exchanges:
            exchanges = False
            for i in range(passnum):
                try:
                    if len(self._user_presented_list[i]) > \
                          len(self._user_presented_list[i + 1]):
                        exchanges = True
                        self._user_presented_list[i], self._user_presented_list[i + 1] = \
                        self._user_presented_list[i + 1], self._user_presented_list[i]
                except TypeError as e:
                    pass
            passnum = passnum-1

    def open_frame(self):
        self.master.mainloop()

    def _choose(self, event=None):
        try:
            firstIndex = self.listBox.curselection()[0]
            self.index = firstIndex
            self.index_value = self._user_presented_list[int(firstIndex)]
        except IndexError:
            self.index_value = None
        self.modalPane.destroy()

    def _cancel(self, event=None):
        self.modalPane.destroy()

    def return_index_value(self):
        return self.index_value

    def return_index(self):
        return self.index

    def return_enum(self):
        return {self.index_value: self._user_enum[self.index_value]}

    def return_value(self):
        return self._user_enum[self.index_value]

# Required imports if put in sepatate package
# import xml.dom.minidom


class XMLMinidomNavigator(object):
    """
    This is a class that makes working with XML data much more simple.  It
    uses the xml.dom.minidom package as the base for it's framework.

    The class init takes in a filename that is a full path filename to
    the xml file that the user wants to work with.

    Parameters
    ----------
    xml_file_name : string (Path)
                    This is the full file name path to the xml file.

    Example
    -------

    >>> visio_xml_dom = XMLMinidomNavigator('fullfilepath.xml')
    >>> visio_xml_dom.move_current_base_tree_to = 'Pages'
    >>> visio_xml_dom.current_xml_dom_tree_bass
    [<DOM Element: Pages at 0x98746d0>]
    >>> visio_xml_dom.current_xml_dom_sub_tree
    [<DOM Element: Pages at 0x98746d0>]
    >>> visio_xml_dom.current_element = 0
    >>> visio_xml_dom.current_attributes
    >>> visio_xml_dom.current_node_name
    'Pages'
    >>> visio_xml_dom.move_current_tree_to = 'Page'
    >>> visio_xml_dom.current_xml_dom_tree_bass
    [<DOM Element: Pages at 0x98746d0>]
    >>> visio_xml_dom.current_xml_dom_sub_tree
    [<DOM Element: Page at 0x9874768>, <DOM Element: Page at 0x995cb90>]
    >>> visio_xml_dom.current_node_name
    'Pages'
    >>> visio_xml_dom.current_element = 0
    >>> visio_xml_dom.current_attributes
    [('ID', '12'), ('NameU', 'Legend'), ('Name', 'Legend')]
    >>> visio_xml_dom.current_element
    <DOM Element: Page at 0x9874768>
    >>> visio_xml_dom.all_current_child_nodes()
    [<DOM Text node "'\n\t\t\t'">,
     <DOM Element: PageProps at 0x9874800>,
     <DOM Text node "'\n\t\t\t'">,
     <DOM Element: Shapes at 0x98749c8>,
     <DOM Text node "'\n\t\t'">]
    >>> visio_xml_dom.non_whitespace_current_child_nodes()
    {1: 'PageProps', 3: 'Shapes'}
    >>> visio_xml_dom.reset_current_tree()
    >>> visio_xml_dom.current_xml_dom_sub_tree
    [<DOM Element: Pages at 0x98746d0>]

    Returns
    -------
    _xml_dom_tree : DOM Tree
                         This is the top level of the xml file.

    """
    _xml_whitespace_identifier = ['#text']

    def __init__(self, xml_file_name):
        self._xml_dom_tree = xml.dom.minidom.parse(xml_file_name)
        self._current_xml_dom_tree_bass = xml.dom.minidom.parse(xml_file_name)
        self._current_xml_dom_sub_tree = xml.dom.minidom.parse(xml_file_name)
        self._xml_tag_list = self.get_complete_tag_list()
        self._current_element = None

    @property
    def xml_dom_tree(self):
        return self._xml_dom_tree

    @property
    def current_xml_dom_tree_bass(self):
        return self._current_xml_dom_tree_bass

    @current_xml_dom_tree_bass.setter
    def current_xml_dom_tree_bass(self, tag_name):
        self._current_xml_dom_tree_bass = \
            self._xml_dom_tree.getElementsByTagName(tag_name)
        self._current_xml_dom_sub_tree = \
            self._xml_dom_tree.getElementsByTagName(tag_name)

    @current_xml_dom_tree_bass.deleter
    def current_xml_dom_tree_bass(self):
        self._current_xml_dom_tree_bass = self._xml_dom_tree
        self._current_xml_dom_sub_tree = self._xml_dom_tree

    def current_xml_dom_tree_bass_reset(self):
        self._current_xml_dom_tree_bass = self._xml_dom_tree
        self._current_xml_dom_sub_tree = self._xml_dom_tree

    @property
    def current_xml_dom_sub_tree(self):
        return self._current_xml_dom_sub_tree

    @current_xml_dom_sub_tree.setter
    def current_xml_dom_sub_tree(self, NodeList):
        self._current_xml_dom_sub_tree = NodeList

    @current_xml_dom_sub_tree.deleter
    def current_xml_dom_sub_tree(self):
        self._current_xml_dom_sub_tree = \
            self.current_xml_dom_tree_bass

    def current_xml_dom_sub_tree_reset(self):
        self._current_xml_dom_sub_tree = \
            self.current_xml_dom_tree_bass

    @property
    def xml_tag_list(self):
        return self._xml_tag_list

    @property
    def current_element(self):
        return self._current_element

    @current_element.setter
    def current_element(self, NodeNumber):
        self._current_element = self.current_xml_dom_sub_tree[NodeNumber]

    @property
    def current_element_value(self):
        try:
            return self._current_element.firstChild.data
        except AttributeError as e:
            # This occurs when there are incomplete tags which there are in
            # visio
            return None

    @property
    def move_current_base_tree_to(self):
        pass

    @property
    def move_current_tree_to(self):
        pass

    def reset_base_tree(self):
        self.current_xml_dom_tree_bass_reset()

    def reset_current_tree(self):
        self.current_xml_dom_sub_tree_reset()

    @property
    def move_base_tree_to_nodelist(self):
        pass

    @move_base_tree_to_nodelist.setter
    def move_base_tree_to_nodelist(self, NodeList):
        self._current_xml_dom_tree_bass = NodeList

    @property
    def move_current_tree_to_nodelist(self):
        pass

    @move_current_tree_to_nodelist.setter
    def move_current_tree_to_nodelist(self, NodeList):
        self._current_xml_dom_sub_tree = NodeList

    @move_current_base_tree_to.setter
    def move_current_base_tree_to(self, tag_name):
        self.current_xml_dom_tree_bass = tag_name

    @move_current_tree_to.setter
    def move_current_tree_to(self, NodeList):
        self.current_xml_dom_sub_tree = \
            self.current_element.getElementsByTagName(NodeList)

    def all_current_child_nodes(self):
        try:
            if self.current_element.hasChildNodes():
                return self.current_element.childNodes
            else:
                return None
        except AttributeError as e:
            # This occurs if you are at the document tag level for whatever
            # reason (you should never be there but just in case)
            return None

    def non_whitespace_current_child_nodes(self):
        if self.current_element.hasChildNodes():
            non_whitespace_child_nodes = {}
            for Index, Node in enumerate(self.current_element.childNodes):
                if not XMLMinidomNavigator.is_xml_whitespace(Node):
                    non_whitespace_child_nodes[Index] = Node.nodeName
            if non_whitespace_child_nodes == {}:
                return None
            else:
                return non_whitespace_child_nodes
        else:
            return None

    @property
    def current_node_name(self):
        try:
            return self.current_element.nodeName
        except AttributeError as e:
            return None

    @property
    def current_attributes(self):
        try:
            # if self.current_element.attributes.length:
            if self.current_element.hasAttributes():
                return self.current_element.attributes.items()
            else:
                return None
        except AttributeError as e:
            # This occurs if you are at the document tag level for whatever
            # reason (you should never be there but just in case)
            return None

    def current_attribute_value(self, AttributeName):
        try:
            if self.current_element.hasAttributes():
                return ([Tuple[1] for Tuple in self.current_attributes
                         if Tuple[0] == AttributeName][0])
            else:
                return None
        except AttributeError as e:
            # This occurs if you are at the document tag level for whatever
            # reason (you should never be there but just in case)
            return None

    @classmethod
    def is_xml_whitespace(cls, node):
        try:
            if hasattr(node, 'data'):
                if node.data.startswith('\n'):
                    return True
                else:
                    return False
            else:
                return False
        except AttributeError as e:
            """
            This is to catch incomplete tags that pop up for whatever reason
            in the output of visio xml files for LayerMem tags with no layer
            attribute
            """
            return True

    def get_complete_tag_list(self):
        tag_list = set()
        for Node in self.xml_dom_tree.getElementsByTagName('*'):
            tag_list.add(Node.nodeName)
        return list(tag_list)

#class XMLMinidomNavigator(object):
#    """
#    This is a class that makes working with XML data much more simple.  It
#    uses the xml.dom.minidom package as the base for it's framework.
#    """
#    _xml_whitespace_identifier = ['#text']
#
#    def __init__(self, xml_file_name):
#        """
#        This is the class init.
#
#        It takes in a filename that is a full path filename to the xml file
#        that the user wants to work with.
#
#        Parameters
#        ----------
#        xml_file_name : string (Path)
#                        This is the full file name path to the xml file.
#
#        Returns
#        -------
#        _xml_dom_tree_base : DOM Tree
#                             This is the top level of the xml file.
#
#        """
#        self._xml_dom_tree_base = xml.dom.minidom.parse(xml_file_name)
#        self._xml_dom_tree = xml.dom.minidom.parse(xml_file_name)
#        self._xml_dom_sub_tree = xml.dom.minidom.parse(xml_file_name)
#        self._xml_dom_sub_tree_nodelist = xml.dom.minidom.parse(xml_file_name)
#        self._xml_tag_list = self.get_complete_tag_list()
#        self._tag_list_hierarchy = self.get_tag_list_hierarchy()
#        self._current_element_data = {}
#        self._current_element_attributes = {}
#
#    @property
#    def xml_dom_tree(self):
#        return self._xml_dom_tree
#
#    @xml_dom_tree.setter
#    def xml_dom_tree(self, tag_name):
#        self._xml_dom_tree = \
#            self._xml_dom_tree_base.getElementsByTagName(tag_name)
#
#    @xml_dom_tree.deleter
#    def xml_dom_tree(self):
#        self._xml_dom_tree = self._xml_dom_tree_base
#
#    @property
#    def xml_dom_sub_tree(self):
#        return self._xml_dom_sub_tree
#
#    @xml_dom_sub_tree.setter
#    def xml_dom_sub_tree(self, node_number):
#        self._xml_dom_sub_tree = self.xml_dom_sub_tree_nodelist[node_number]
#
#    @xml_dom_sub_tree.deleter
#    def xml_dom_sub_tree(self):
#        self._xml_dom_sub_tree = self._xml_dom_tree_base
#
#    @property
#    def xml_dom_sub_tree_nodelist(self):
#        return self._xml_dom_sub_tree_nodelist
#
#    @xml_dom_sub_tree_nodelist.setter
#    def xml_dom_sub_tree_nodelist(self, tag_name):
#        self._xml_dom_sub_tree_nodelist = \
#            self.xml_dom_sub_tree.getElementsByTagName(tag_name)
#
#    @xml_dom_sub_tree_nodelist.deleter
#    def xml_dom_sub_tree_nodelist(self):
#        self._xml_dom_sub_tree_nodelist = self._xml_dom_tree_base
#
#    @property
#    def xml_tag_list(self):
#        return self._xml_tag_list
#
#    @property
#    def current_element_data(self):
#        return self._current_element_data
#
#    @property
#    def current_element_attributes(self):
#        return self._current_element_attributes
#
#    @classmethod
#    def is_xml_whitespace(cls, node):
#        try:
#            return node.data.startswith('\n')
#        except AttributeError as e:
#            """
#            This is to catch incomplete tags that pop up for whatever reason
#            in the output of visio xml files for LayerMem tags with no layer
#            attribute
#            """
#            return True
#
##    def get_element_data(self, Element):
##        self._current_element_data = {}
##        self._current_element_attributes = {}
##        for Node in Element.childNodes:
##            if Node.hasChildNodes():
##                self.get_element_data(Node)
##            else:
##                if not self.is_xml_whitespace(Node):
##                    self._current_element_data.update(
##                              {Node.parentNode.nodeName: Node.data})
##                    self._current_element_attributes.update(
##                      {Key: Value
##                       for Key, Value in Node.parentNode.attributes.items()})
#
#    def get_element_data(self, Element):
#        self._current_element_data = {}
#        self._current_element_attributes = {}
#        for Node in Element.childNodes:
#            if Node.hasChildNodes():
#                self.get_element_data(Node)
#            else:
#                if not self.is_xml_whitespace(Node):
#                    if Node.parentNode.nodeName not in self._current_element_data.keys():
#                        self._current_element_data.update(
#                                  {Node.parentNode.nodeName: Node.data})
#                        self._current_element_attributes.update(
#                          {Key: Value
#                           for Key, Value in Node.parentNode.attributes.items()})
#
#    def get_complete_tag_list(self):
#        tag_list = set()
#        for Node in self._xml_dom_tree_base.getElementsByTagName('*'):
#            tag_list.add(Node.nodeName)
#        return list(tag_list)
#
#    def get_tag_list_hierarchy(self):
#        tag_hierarchy = {}
#        for item in self.xml_tag_list:
#            tag_hierarchy[item] = []
#
##    def
##        reduced_tag_list = ['Prop']#, 'Text']
##        # for Tag in tag_hierarchy:
##        for Tag in reduced_tag_list:
##            visio_xml_dom.xml_dom_tree = Tag
##            for Element in visio_xml_dom.xml_dom_tree:
##                # print(Element)
##                visio_xml_dom.get_element_data(Element)
##                print({'attributes': visio_xml_dom.current_element_attributes})
##                print({'data': visio_xml_dom.current_element_data})
##        # Required imports if put in sepatate package
##        # import os


class FileSystemNavigation(object):
    """
    This is a class that helps the user navigate the file system for files
    and paths
    """
    def __init__(self):
        """
        This is the class init.

        It has the following user accessible attributes that it stores the
        data that it works with in.

        Parameters
        ----------

            None

        Returns
        -------

            current_sub_directory_list : List
                                         List of the current subdirectories

            current_file_list : List
                                List of the current files in all
                                subdirectories

            current_full_path_names : List
                                      List of the current full path names to
                                      the current directory and all the
                                      subdirectories

        """
        self._initialization_directory = os.getcwd()
        self._current_working_directory = os.getcwd()
        self._current_sub_directory_list = []
        self._current_file_list = []
        self._current_full_path_names = []

    @property
    def current_sub_directory_list(self):
        return self._current_sub_directory_list

    @current_sub_directory_list.setter
    def current_sub_directory_list(self, new_sub_directory_list):
        self._current_sub_directory_list = new_sub_directory_list

    @current_sub_directory_list.deleter
    def current_sub_directory_list(self):
        del self._current_sub_directory_list

    @property
    def current_file_list(self):
        return self._current_file_list

    @current_file_list.setter
    def current_file_list(self, new_current_file_list):
        self._current_file_list = new_current_file_list

    @current_file_list.deleter
    def current_file_list(self):
        del self._current_file_list

    @property
    def current_full_path_names(self):
        return self._current_full_path_names

    @current_full_path_names.setter
    def current_full_path_names(self, new_full_path_names_list):
        self._current_full_path_names = new_full_path_names_list

    @current_full_path_names.deleter
    def current_full_path_names(self):
        del self._current_full_path_names

    @property
    def current_working_directory(self):
        return self._current_working_directory

    @current_working_directory.setter
    def current_working_directory(self, new_current_working_directory):
        # I ignore user parameter so you cant spoof the function ok?
        self._current_working_directory = os.getcwd()

    @current_working_directory.deleter
    def current_working_directory(self):
        del self._current_working_directory

    def get_folder_information(self):
        self._current_working_directory = os.getcwd()
        all_sub_directories_relative_path = []
        all_files_relative_path = []
        all_full_path_names = []

        for CwdPath, SubDirectories, Files \
                in os.walk(self._current_working_directory):
            all_sub_directories_relative_path.append(SubDirectories)
            all_files_relative_path.append(Files)
            all_full_path_names.append(CwdPath)

        self._current_sub_directory_list = all_sub_directories_relative_path
        self._current_file_list = all_files_relative_path
        self._current_full_path_names = all_full_path_names

    def find_files_with_extension(self, file_extension):
        file_list = []
        for DirectoryFiles in self._current_file_list:
            for Files in DirectoryFiles:
                # Must use | opperator as "or" opperator is short circuit
                if Files.endswith(file_extension):
                    file_list.append(Files[:-len(file_extension)])
        return file_list

    def verify_directory_exists(self, directory_names):
        directory_list = []
        for Directories in self._current_sub_directory_list:
            for Directory in Directories:
                if Directory in directory_names:
                    directory_list.append(Directory)
        return directory_list

    def return_full_path_to_directory(self, directory_names):
        directory_list_full_path = []
        for Directory in self.return_unique_entries(directory_names):
                for FullPathName in self._current_full_path_names:
                    if FullPathName.endswith(Directory):
                        directory_list_full_path.append(FullPathName)
        return directory_list_full_path

    def return_directories_closest_to_current_directory(self, directory_list, full_path_list):
        CUR_DIR_LEN = len(self.current_working_directory)
        full_paths = []
        for Directory in directory_list:
            temp = 1024
            for Index, FullPath in enumerate(full_path_list):
                if FullPath.endswith(Directory):
                    file_name_positiom = FullPath.find(Directory)
                    if abs(file_name_positiom - CUR_DIR_LEN) < temp:
                        file_name_positiom = Index
                        temp = abs(file_name_positiom - CUR_DIR_LEN)
            full_paths.append(full_path_list[file_name_positiom])
        return full_paths

    @staticmethod
    def return_unique_entries(non_unique_list):
        return list(set(non_unique_list))