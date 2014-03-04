# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 Roland Bettinelli

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
Infrastrucure

The BPMN Infrastructure package contains two elements that are used for both abstract syntax models and diagram models.
'''

from Foundation.models import BaseElement
from Common.fonctions import residual_args

class Definitions(BaseElement):
    '''
    The Definitions class is the outermost containing object for all BPMN elements.
    It defines the scope of visibility and the namespace for all contained elements. The interchange of BPMN files will always be through one or more Definitions.
    '''
    def __init__(self, id, name, targetNamespace, **kwargs):
        '''
        name:str
            The name of the Definition.
            
        targetNamespace:str
            This attribute identifies the namespace associated with the Definition and follows the convention established by XML Schema.
        
        expressionLanguage:str (default='http://www.w3.org/1999/XPath')
            This attribute identifies the formal Expression language used in Expressions within the elements of this Definition.
            This value MAY be overridden on each individual formal Expression.
            The language MUST be specified in a URI format.
        
        typeLanguage:str (default='http://www.w3.org/2001/XMLSchema')
            This attribute identifies the type system used by the elements of this Definition.
            This value can be overridden on each individual ItemDefinition.
            The language MUST be specified in a URI format.
        
        rootElements:RootElement list
            This attribute lists the root elements that are at the root of this Definitions.
            These elements can be referenced within this Definitions and are visible to other Definitions.
       
        diagrams:BPMNDiagram list
            This attribute lists the BPMNDiagrams that are contained within this Definitions.
        
        imports:Import list
            This attribute is used to import externally defined elements and make them available for use by elements within this Definitions.
        
        extentions:Extension list
            This attribute identifies extensions beyond the attributes and model associations in the base BPMN specification.
        
        relationships:Relationship list
            This attribute enables the extension and integration of BPMN models into larger system/development Processes.
        
        exporter:str
            This attribute identifies the tool that is exporting the bpmn model file.
        
        exporterVersion:str
            This attribute identifies the version of the tool that is exporting the bpmn model file.
        '''
        super(Definitions, self).__init__(id, **kwargs)
        
        self.name = name
        self.targetNamespace = targetNamespace
        
        self.expressionLanguage = kwargs.pop(expressionLanguage,'http://www.w3/org/1999/XPath')
        self.typeLanguage = kwargs.pop('typeLanguage','http://www.w3.org/2001/XMLSchema')
        self.rootElements = kwargs.pop('rootElements',[])
        self.diagrams = kwargs.pop('diagrams',[])
        self.imports = kwargs.pop('imports',[])
        self.extentions = kwargs.pop('extentions',[])
        self.relationships = kwargs.pop('relationships',[])
        
        self.exporter = kwargs.pop('exporter',None)
        self.exporterVersion = kwargs.pop('exporterVersion',None)
        if self.__class__.__name__ == 'Definitions':
            residual_args(self.__init__, **kwargs)
        
    def _to_xml(self):
        '''
        <xsd:element name="definitions" type="tDefinitions"/>
        <xsd:complexType name="tDefinitions">
            <xsd:sequence>
                <xsd:element ref="import" minOccurs="0" maxOccurs="unbounded"/>
                <xsd:element ref="extension" minOccurs="0" maxOccurs="unbounded"/>
                <xsd:element ref="rootElement" minOccurs="0" maxOccurs="unbounded"/>
                <xsd:element ref="bpmndi:BPMNDiagram" minOccurs="0" maxOccurs="unbounded"/>
                <xsd:element ref="relationship" minOccurs="0" maxOccurs="unbounded"/>
            </xsd:sequence>
            <xsd:attribute name="id" type="xsd:ID" use="optional"/>
            <xsd:attribute name="targetNamespace" type="xsd:anyURI" use="required"/>
            <xsd:attribute name="expressionLanguage" type="xsd:anyURI" use="optional" default="http://www.w3.org/1999/XPath"/>
            <xsd:attribute name="typeLanguage" type="xsd:anyURI" use="optional" default="http://www.w3.org/2001/XMLSchema"/>
            <xsd:anyAttribute name="exporter" type="xsd:ID"/>
            <xsd:anyAttribute name="exporterVersion" type="xsd:ID"/>
            <xsd:anyAttribute namespace="##other" processContents="lax"/>
        </xsd:complexType>
        '''
        pass
    
class Import(object):
    '''
    '''
    shortTypes_map={'xml10':'http://www.w3.org/2001/XMLSchema',
                    'wsdl20':'http://www.w3.org/TRwsdl20/',
                    'bpmn20':'http://www.omg.org/spec/BPMN/20100524/MODEL',}
    def __init__(self, shortType, namespace, location=None)
        '''
        shortType:str
            Identifies the type of document being imported by providing an absolute URI that identifies the encoding language used in the document.
            Will set self.importType.
            Supported types are listed in Infrastructure.Import.shortTypes_map
                'xml10'  --> 'hhtp://www.w3.org/2001/XMLSchema'
                'wsdl20' --> 'http://www.w3.org/TRwsdl20/'
                'bpmn20' --> 'http://www.omg.org/spec/BPMN/20100524/MODEL'
        
        namespace:str
            Identifies the namespace of the imported element.
        
        location:str
            Identifies the location of the imported element.
        '''
        self.importType = self.shortTypes_map[shortType]
        self.namespace = namespace
        self.location = location
        
