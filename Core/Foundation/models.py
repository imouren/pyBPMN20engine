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
Core BPMN Package - Foundation

The Foundation package contains classes that are shared among other packages in the Core of an abstract syntax model.
'''

from Core.Common.fonctions import residual_args

RelationshipDirection = ['None','Forward','Backward','Both']

class BaseElement(object):
    '''
    BaseElement is the abstract super class for most BPMN elements.
    It provides the attributes id and documentation, which other elements will inherit.
    '''
    def __init__(self, id, **kwargs):
        '''
        id:str
            This attribute is used to uniquely identify BPMN elements.
            The id is REQUIRED if this element is referenced or intended to be referenced by something else.
            If the element is not currently referenced and is never intended to be referenced, the id MAY be omitted.
            
        documentation:Documentation list
            This attribute is used to annotate the BPMN element, such as descriptions and other documentation.
            
        extensionDefinition:ExtensionDefinition list
            This attribute is used to attach additional attributes and associations to any BaseElement.

        extentionValues:ExtentionAttributeDefinition list
            This attribute is used to provide values for extended attributes and model associations.
        '''
        super(BaseElement,self).__init__()
        self.id = id
        self.documentation = kwargs.pop('documentation',[])
        self.extensionDefinitions = kwargs.pop('extensionDefinition',[])
        self.extensionValues = kwargs.pop('extensionValues',[])
        if self.__class__.__name__ == 'BaseElement':
            residual_args(self.__init__, **kwargs)
    
class RootElement(BaseElement):
    '''
    RootElement is the abstract super class for all BPMN elements that are contained within Definitions.
    When contained within Definitions, these elements have their own defined life-cycle and are not deleted with the deletion of other elements.
    
    The RootElement element inherits the attributes and model associations of BaseElement, but does not have any further attributes or model associations.
    '''
    def __init__(self):
        super(RootElement,self).__init__()
    
class Relationship(BaseElement):
    '''
    The Relationship element inherits the attributes and model associations of BaseElement.
    '''
    def __init__(self, id, type, direction, sources, targets, **kwargs):
        '''
        type:str
            The descriptive name of the element.
            
        direction:RelationshipDirection enum {'None'|'Forward'|'Backward'|'Both'}
            This attribute specifies the direction of the relationship.
        
        sources:Element list (min len = 1)
            This association defines artifacts that are augmented by the relationship.
            
        targets:Element list (min len = 1)
            This association defines artifacts used to extend the semantics of the source element(s).
        '''
        super(Relationship, self).__init__(self, id, **kwargs)
        self.type = type
        if direction in RelationshipDirection:
            self.direction = direction
        else:
            raise Exception #to be detailed
        self.sources = sources
        self.targets = targets
    
class ExtensionAttributeValue(object):
    '''
    The ExtensionAttributeValue contains the attribute value.
    '''
    def __init__(self,extensionAttributeDefinition, **kwargs):
        '''
        extensionAttributeDefinition:ExtensionAttributeDefinition
            Defines the extension attribute for which this value is being provided.
        
        value:Element
            The contained attribute value, used when the associated ExtensionAttributeDefinition.isReference is false.
            The type of this Element object MUST conform to the type specified in the associated ExtensionAttributeDefinition.
        
        valueRef:Element
            The referenced attribute value, used when the associated ExtensionAttributeDefinition.isReference is true.
            The type of this Element MUST conform to the type specified in the associated ExtensionAttributeDefinition.
        '''
        super(ExtensionAttributeValue,self).__init__()
        self.extensionAttributeDefinition = extensionAttributeDefinition
        self.value = kwargs.pop('value',None)
        self.valueRef = kwargs.pop('valueRef',None)
        
        if self.__class__.__name__=='ExtensionAttributeValue':
            residual_args(self.__init__,**kwargs)
    
class Documentation(BaseElement):
    '''
    All BPMN elements that inherit from the BaseElement will have the capability, through the Documentation
    element, to have one or more text descriptions of that element.
    '''
    def __init__(self, id, **kwargs):
        '''
        text:str
            This attribute is used to capture the text descriptions of a BPMN element.
            
        textFormat:str (default='text/plain')
            This attribute identifies the format of the text.
            It MUST follow the mime-type format.
        '''
        super(Documentation,self).__init__(id, **kwargs)
        self.text = kwargs.pop('text','')
        self.textFormat = kwargs.pop('textFormat','text/plain')
        if self.__class__.__name__ == 'Documentation':
            residual_args(self.__init__, **kwargs)
    
class ExtensionDefinition(object):
    '''
    The ExtensionDefinition class defines and groups additional attributes.
    '''
    def __init__(self, name, **kwargs):
        '''
        name:str
            The name of the extension. This is used as a namespace to uniquely identify the extension content.
        
        extensionAttributeDefinitions:ExtensionAttributeDefinition list
            The specific attributes that make up the extension.
        '''
        super(ExtensionDefinition,self).__init__()
        self.name = name
        self.extensionAttributeDefinitions = kwargs.pop('extentionAttributeDefinitions',[])
        
        if self.__class__.__name__ == 'ExtensionDefinition':
            residual_args(self.__init__, **kwargs)
        
    
class ExtensionAttributeDefinition(object):
    '''
    The ExtensionAttributeDefinition defines new attributes.
    '''
    def __init__(self, name, type, isReference=False, **kwargs):
        '''
        name:str
            The name of the extension attribute.
        
        type:str
            The type that is associated with the attribute.
        
        isReference:bool
            Indicates if the attribute value will be referenced or contained.
        '''
        super(ExtensionAttributeDefinition,self).__init__()
        self.name = name
        self.type = type
        self.isReference = isReference
        
        if self.__class__.__name__=='ExtensionAttributeDefinition':
            residual_args(self.__init__, **kwargs)

class Extension(object):
    '''
    The Extension element binds/imports an ExtensionDefinition and its attributes to a BPMN model definition.
    '''
    def __init__(self, mustUnderstand=False, **kwargs):
        '''
        musUnderstand:bool (default=False)
            This flag defines if the semantics defined by the extension definition and its
            attribute definition MUST be understood by the BPMN adopter in order to
            process the BPMN model correctly.
        
        definition:ExtensionDefinition
            Defines the content of the extension.
        '''
        super(Extension,self).__init__()
        self.mustUnderstand = mustUnderstand
        self.definition = kwargs.pop('definition',None)
        if self.__class__.__name__ == 'Extension':
            residual_args(self.__init__,**kwargs)