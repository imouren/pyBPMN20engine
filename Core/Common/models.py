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
Core BPMN Package - Common
'''

from Foundation.models import RootElement, BaseElement
from fonctions import residual_args


##########################################################
# Artifacts

AssociationDirection = ['None', 'One', 'Both']

class Artifact(BaseElement):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        '''
        super(Artifact, self).__init__(id, **kwargs)
        if self.__class__.__name__=='Artifact':
            residual_args(self.__init__, **kwargs)

class Association(Artifact):
    '''
    The Association element inherits the attributes and model associations of BaseElement.
    '''
    def __init__(self, id, sourceRef, targetRef, associationDirection='None', **kwargs):
        '''
        sourceRef:BaseElement
            The BaseElement that the Association is connecting from.
        
        targetRef:BaseElement
            The BaseElement that the Association is connecting to.
            
        associationDirection:AssociationDirection enum (default='None') {'None'|'One'|'Both'}
            associationDirection is an attribute that defines whether or not the Association shows any directionality with an arrowhead.
            A value of One means that the arrowhead SHALL be at the Target Object.
            A value of Both means that there SHALL be an arrowhead at both ends of the Association line.
        '''
        super(Association,self).__init__(id, **kwargs)
        self.sourceRef = sourceRef
        self.targetRef = targetRef
        if associationDirection in AssociationDirection:
            self.associationDirection = associationDirection
        else:
            raise Exception #to be precised
        
        if self.__class__.__name__=='Association':
            residual_args(self.__init__, **kwargs)
        
class Group(Artifact):
    '''
    The Group object is an Artifact that provides a visual mechanism to group elements of a diagram informally.
    The grouping is tied to the CategoryValue supporting element.
    That is, a Group is a visual depiction of a single CategoryValue.
    The graphical elements within the Group will be assigned the CategoryValue of the Group.
    '''
    def __init__(self, id, **kwargs):
        '''
        categoryValueRef:CategoryValue
            The categoryValueRef attribute specifies the CategoryValue that the Group represents.
            The name of the Category and the value of the CategoryValue separated by delineator "." provides the label for the Group.
            The graphical elements within the boundaries of the Group will be assigned the CategoryValue.
        '''
        super(Group,self).__init__(id, **kwargs)
        self.categoryValueRef = kwargs.pop('categoryValueRef', None)
        if self.__class__.__name__=='Group':
            residual_args(self.__init__, **kwargs)

class Category(RootElement):
    '''
    '''
    def __init__(self, id, name, **kwargs):
        '''
        name:str
            The descriptive name of the element.
            
        categoryValue: CategoryValue list
            The categoryValue attribute specifies one or more values of the Category.
        '''
        super(Category, self).__init__(id, **kwargs)
        self.name = name
        self.categoryValue = kwargs.pop('categoryValue',[])
        
        if self.__class__.__name__=='Category':
            residual_args(self.__init__, **kwags)
        
class CategoryValue(BaseElement):
    '''
    '''
    def __init__(self, id, value, **kwargs):
        '''
        value:str
            This attribute provides the value of the CategoryValue element.
            
        category:Category
            The category attribute specifies the Category representing the Category as such and contains the CategoryValue.
        
        categorizedFlowElements:FlowElement list
            The FlowElements attribute identifies all of the elements (e.g., Events,
            Activities, Gateways, and Artifacts) that are within the boundaries of the Group.
        '''
        super(CategoryValue, self).__init__(id, **kwargs)
        self.value = value
        self.category = kwargs.pop('category',None)
        self.categorizedFlowElements = kwargs.pop('categorizedFlowElements',[])
            
class TextAnnotation(Artifact):
    '''
    '''
    def __init__(self, id, text, textFormat='text/plain', **kwargs):
        '''
        text:str
            Text is an attribute that is text that the modeler wishes to communicate to the reader of the Diagram.
        
        textFormat:str (default='text/plain')
            This attribute identifies the format of the text.
            It MUST follow the mimetype format.
        '''
        super(TextAnnotation, self).__init__(self, id, **kwargs)
        self.text = text
        self.textFormat = textFormat
        
##########################################################
# Correlations

class CorrelationKey(BaseElement):
    '''
    A CorrelationKey represents a composite key out of one or many CorrelationProperties that essentially specify extraction Expressions atop Messages.
    As a result, each CorrelationProperty acts as a partial key for the correlation.
    For each Message that is exhanged as part of a particular Conversation, the CorrelationProperties need to provide
    a CorrelationPropertyRetrievalExpression which references a FormalExpression to the Message payload.
    That is, for each Message (that is used in a Conversation) there is an Expression, which extracts portions of the respective Message's payload.
    '''
    def __init__(self, id, **kwargs):
        '''
        name:str
            Specifies the name of the CorrelationKey.
            
        correlationPropertyRef:CorrelationProperty list
            The CorrelationProperties, representing the partial keys of this CorrelationKey.
        '''
        super(CorrelationKey,self).__init__(id, **kwargs)
        self.name = kwargs.pop('name',None)
        self.correlationPropertyRef = kwargs.pop('correlationPropertyRef',[])
        
        if self.__class__.__name__=='CorrelationKey':
            residual_args(self.__init__, **kwargs)
        
class CorrelationProperty(RootElement):
    '''
    '''
    def __init__(self, id, correlationPropertyRetrievalExpression, **kwargs):
        '''
        name:str
            Specifies the name of the CorrelationProperty.
            
        type:str
            Specifies the type of the CorrelationProperty.
        
        correlationPropertyRetrievalExpression:CorrelationPropertyRetrievalExpression list (min len = 1)
            The CorrelationPropertyRetrievalExpressions for this CorrelationProperty, representing the associations
            of FormalExpressions (extraction paths) to specific Messages occurring in this Conversation.
        '''
        super(CorrelationProperty,self).__init__(id, **kwargs)
        self.name = kwargs.pop('name',None)
        self.type = kwargs.pop('type',None)
        self.correlationPropertyRetrievalExpression = correlationPropertyRetrievalExpression
        
class CorrelationPropertyRetrievalExpression(BaseElement):
    '''
    '''
    def __init__(self, id, messagePath, messageRef, **kwargs):
        '''
        messagePath:FormalExpression
            The FormalExpression that defines how to extract a CorrelationProperty from the Message payload.
            
        messageRef:Message
            The specific Message the FormalExpression extracts the CorrelationProperty from.
        '''
        super(CorrelationPropertyRetrievalExpression,self).__init__(id, **kwargs)
        self.messagePath = messagePath
        self.messageRef = messageRef
        
        if self.__class__.__name__=='CorrelationPropertyRetrievalExpression':
            residual_args(self.__init__, **kwargs)
            
class CorrelationSubscription(BaseElement):
    '''
    '''
    def __init__(self, id, correlationKeyRef, **kwargs):
        '''
        correlationKeyRef:CorrelationKey
            The CorrelationKey this CorrelationSubscription refers to.
            
        correlationPropertyBinding:CorrelationPropertyBinding list
            The bindings to specific CorrelationProperties and FormalExpressions (extraction rules atop the Process context).
        '''
        super(CorrelationSubscription,self).__init__(id, **kwargs)
        self.correlationKeyRef = correlationKeyRef
        self.correlationPropertyBinding = kwargs.pop('correlationPropertyBinding',[])
        
        if self.__class__.__name__=='CorrelationSubscription':
            residual_args(self.__init__, **kwargs)
            
class CorrelationPropertyBinding(BaseElement):
    '''
    '''
    def __init__(self, id, dataPath, correlationPropertyRef, **kwargs):
        '''
        dataPath:FormalExpression
            The FormalExpression that defines the extraction rule atop the Process context.
            
        correlationPropertyRef:CorrelationProperty
            The specific CorrelationProperty, this CorrelationPropertyBinding refers to.
        '''
        super(CorrelationPropertyBinding,self).__init__(id, **kwargs)
        self.dataPath = dataPath
        self.correlationPropertyRef = correlationPropertyRef
        
        if self.__class__.__name__=='CorrelationPropertyBinding':
            residual_args(self.__init__, **kwargs)
            
##########################################################
# Error (as Error Event)

class Error(RootElement):
    '''
    '''
    def __init__(self, id, name, errorCode, **kwargs):
        '''
        name:str
            The descriptive name of the Error.
            
        errorCode:str
            For an End Event:
                If the result is an Error, then the errorCode MUST be supplied
                (if the processType attribute of the Process is set to executable)
                This "throws" the Error.
            For an Intermediate Event within normal flow:
                If the trigger is an Error, then the errorCode MUST be entered
                (if the processType attribute of the Process is set to executable).
                This "throws" the Error.
            For an Intermediate Event attached to the boundary of an Activity:
                If the trigger is an Error, then the errorCode MAY be entered.
                This Event "catches" the Error. If there is no errorCode, then
                any error SHALL trigger the Event. If there is an errorCode, then
                only an Error that matches the errorCode SHALL trigger the Event.

        structureRef:ItemDefinition
            An ItemDefinition is used to define the "payload" of the Error.
        '''
        super(Error,self).__init__(id, **kwargs)
        self.name = name
        self.errorCode = errorCode
        self.structureRef = kwargs.pop('structureRef', None)
        
        if self.__class__.__name__=='Error':
            residual_args(self.__init__, **kwargs)
        
##########################################################
# Escalation

class Escalation(RootElement):
    '''
    '''
    def __init__(self, id , name, escalationCode, **kwargs):
        '''
        name:str
            The descriptive name of the Escalation.
            
        escalationCode:str
            For an End Event:
                If the Result is an Escalation, then the escalationCode
                MUST be supplied (if the processType attribute of the Process
                is set to executable).
                This "throws" the Escalation.
            For an Intermediate Event within normal flow:
                If the trigger is an Escalation, then the escalationCode
                MUST be entered (if the processType attribute of the Process is
                set to executable).
                This "throws" the Escalation.
            For an Intermediate Event attached to the boundary of an Activity:
                If the trigger is an Escalation, then the escalationCode MAY
                be entered. This Event "catches" the Escalation. If there is no
                escalationCode, then any Escalation SHALL trigger the
                Event. If there is an escalationCode, then only an Escalation
                that matches the escalationCode SHALL trigger the
                Event.

        structureRef:ItemDefinition
            An ItemDefinition is used to define the "payload" of the Escalation.
        '''
        self.name = name
        self.escalationCode = escalationCode
        self.structureRef = kwargs.pop('structureRef', None)
        
        if self.__class__.__name__=='Escalation':
            residual_args(self.__init__, **kwargs)

##########################################################
# Expressions

class Expression(BaseElement):
    '''
    The Expression class is used to specify an Expression using natural-language text.
    These Expressions are not executable and are considered underspecified.
    The definition of an Expression can be done in two ways: it can be contained where it is used, or
    it can be defined at the Process level and then referenced where it is used.
    The Expression element inherits the attributes and model associations of BaseElement,
    but does not have any additional attributes or model associations.
    '''
    def __init__(self, id, **kwargs):
        '''
        '''
        super(Expression, self).__init__(id, **kwargs)
        if self.__class__.__name__=='Expression':
            residual_args(self.__init__, **kwargs)

class FormalExpression(Expression):
    '''
    The FormalExpression class is used to specify an executable Expression using a specified Expression
    language. A natural-language description of the Expression can also be specified, in addition to the formal specification.
    The default Expression language for all Expressions is specified in the Definitions element, using the
    expressionLanguage attribute. It can also be overridden on each individual FormalExpression using the same attribute.
    '''
    def __init__(self, id, body, evaluatesToTypeRef, **kwargs):
        '''
        body:Element
            The body of the Expression.
            
        evaluatesToTypeRef:ItemDefinition
            The type of object that this Expression returns when evaluated.
            For example, conditional Expressions evaluate to a boolean.
        
        language:str
            Overrides the Expression language specified in the Definitions.
            The language MUST be specified in a URI format.
        '''
        super(FormalExpression,self).__init__(self, id, **kwargs)
        self.body = body
        self.evaluatesToTypeRef = evaluatesToTypeRef
        self.language = kwargs.pop('language', None)
        
        if self.__class__.__name__=='FormalExpression':
            residual_args(self.__init__, **kwargs)
            
    def _to_xml(self):
        '''
        Note that this attribute is not relevant when the XML Schema is used for
        interchange. Instead, the FormalExpression complex type supports mixed
        content. The body of the Expression would be specified as element content.
        For example:
            <formalExpression id="ID_2">
                count(../dataObject[id="CustomerRecord_1"]/emailAddress) > 0
                <evaluatesToType id="ID_3" typeRef=“xsd:boolean"/>
            </formalExpression>
        '''
        pass

            
##########################################################
# Flows

class FlowElement(BaseElement):
    '''
    FlowElement is the abstract super class for all elements that can appear in a Process flow, which are FlowNodes.
    '''
    def __init__(self, id, **kwargs):
        '''
        name:str
            The descriptive name of the element.
            
        categoryValueRef:CategoryValue list
            A reference to the Category Values that are associated with this FlowElement.

        auditing:Auditing
            A hook for specifying audit related properties.
            Auditing can only be defined for a Process.
        
        monitoring:Monitoring
            A hook for specifying monitoring related properties.
            Monitoring can only be defined for a Process.
        '''
        super(FlowElement, self).__init__(id, **kwargs)
        self.name = kwargs.pop('name', None)
        self.categoryValueRef = kwargs.pop('categoryValueRef',[])
        self.auditing = kwargs.pop('auditing', None)
        self.monitoring = kwargs.pop('monitoring', None)
        
        if self.__class__.__name__=='FlowElement':
            residual_args(self.__init__, **kwargs)
        
class FlowElementContainer(BaseElement):
    '''
    FlowElementsContainer is an abstract super class for BPMN diagrams (or views) and defines the superset of elements that are contained in those diagrams.
    Basically, a FlowElementsContainer contains FlowElements, which are Events, Gateways, Sequence Flows, Activities and Choreography Activities.
    There are four types of FlowElementsContainers: Process, Sub-Process, Choreography, and Sub-Choreography.
    '''
    def __init__(self, id, **kwargs):
        '''
        flowElements:FlowElement list
            This association specifies the particular flow elements contained in a FlowElementContainer.
            Flow elements are Events, Gateways, SequenceFlows, Activities, Data Objects, Data Associations, and ChoreographyActivities.
            Note that:
                Choreography Activities MUST NOT be included as a flowElement for a Process.
                Activities, Data Associations, and Data Objects MUST NOT be included as a flowElement for a Choreography.

        laneSets:LaneSet list
            This attribute defines the list of LaneSets used in the FlowElementsContainer LaneSets are not used for Choreographies or Sub-Choreographies.
        '''
        super(FlowElementContainer,self).__init__(id, **kwargs)
        self.flowElements = kwargs.pop('flowElements',[])
        self.laneSets = kwargs.pop('laneSets',[])
        
        if self.__class__.__name__=='FlowElementContainer':
            residual_args(self.__init__, **kwargs) 

GatewayDirection = ['Unspecified','Converging','Diverging','Mixed']
            
class Gateway(FlowElement):
    '''
    The Gateway class is an abstract type.
    Its concrete subclasses define the specific semantics of individual Gateway types, defining how the Gateway behaves in different situations.
    '''
    def __init__(self, id, gatewayDirection='Unspecified', **kwargs):
        '''
        gatewayDirection:GatewayDirection enum (default='Unspecified') {'Unspecified'|'Converging'|'Diverging'|'Mixed'}
            An attribute that adds constraints on how the Gateway MAY be used :
                Unspecified: There are no constraints. The Gateway MAY have any number of incoming and outgoing Sequence Flows.
                Converging: This Gateway MAY have multiple incoming Sequence Flows but MUST have no more than one outgoing Sequence Flow.
                Diverging: This Gateway MAY have multiple outgoing Sequence Flows but MUST have no more than one incoming Sequence Flow.
                Mixed: This Gateway contains multiple outgoing and multiple incoming Sequence Flows.
        '''
        super(Gateway,self).__init__(id, **kwargs)
        if gatewayDirection in GatewayDirection:
            self.gatewayDirection = gatewayDirection
        else:
            raise Exception #to be detailed
        if self.__calss__.__name__=='Gateway':
            residual_args(self.__init__, **kwargs)

##########################################################
# Item Definition

ItemKind = ['Information','Physical']

class ItemDefinition(RootElement):
    '''
    An ItemDefinition element can specify an import reference where the proper definition of the structure is defined.
    In cases where the data structure represents a collection, the multiplicity can be projected into the attribute isCollection.
    If this attribute is set to "true", but the actual type is not a collection type, the model is considered as invalid.
    BPMN compliant tools might support an automatic check for these inconsistencies and report this as an error.
    The itemKind attribute specifies the nature of an item which can be a physical or an information item.
    '''
    def __init__(self, id, itemKind='Information', isCollection=False, **kwargs):
        '''
        itemKind:ItemKind enum (default='Information') {'Information'|'Physical'}
            This defines the nature of the Item. Possible values are physical or information.
        
        isCollection:bool (default=False)
            Setting this flag to true indicates that the actual data type is a collection.
        
        structureRef: Element
            The concrete data structure to be used.
            
        import:Import
            Identifies the location of the data structure and its format.
            If the importType attribute is left unspecified, the typeLanguage specified in
            the Definitions that contains this ItemDefinition is assumed.
        '''
        super(ItemDefinition,self).__init__(id, **kwargs)
        if itemKind in ItemKind:
            self.itemKind = itemKind
        else:
            raise Exception #tbd
        self.isCollection = isCollection
        self.structureRef = kwargs.pop('structureRef',None)
        #self.import is not valid in python, use of import_ instead
        self.import_ = kwargs.pop('import',None)
        
        if self.__class__.__name__=='ItemDefinition':
            residual_args(self.__init__, **kwargs)

##########################################################
# Message

class Message(RootElement):
    '''
    '''
    def __init__(self, id, name, **kwargs):
        '''
        name:str
            Name is a text description of the Message.
            
        itemRef:ItemDefinition
            An ItemDefinition is used to define the "payload" of the Message.
        '''
        super(Message, self).__init__(id, **kwargs)
        self.name = name
        self.itemRef = kwargs.pop('itemRef',None)
        
        if self.__class__.__name__=='Message':
            residual_args(self.__init__, **kwargs)

##########################################################
# Resource
            
class Resource(RootElement):
    '''
    The Resource class is used to specify resources that can be referenced by Activities.
    These Resources can be Human Resources as well as any other resource assigned to Activities during Process execution time.
    The definition of a Resource is "abstract", because it only defines the Resource, without detailing how e.g.,
    actual user IDs are associated at runtime. Multiple Activities can utilize the same Resource.
    '''
    def __init__(self, id, name, **kwargs):
        '''
        name:str
            This attribute specifies the name of the Resource.
        
        resourceParameters:ResourceParameter list
            This model association specifies the definition of the parameters needed at runtime to resolve the Resource.
        '''
        super(Resource, self).__init__(id, **kwargs)
        self.name = name
        self.resourceParameters = kwargs.pop('resourceParameters',[])
        
        if self.__class__.__name__=='Resource':
            residual_args(self.__init__, **kwargs)
            
class ResourceParameter(BaseElement): #inconsistency of OMG spec on inheritance of ResourceParameter (RootElement or BaseElement)
    '''
    The Resource can define a set of parameters to define a query to resolve the actual resources (e.g., user ids).
    '''
    def __init__(self, id, name, type, isRequired, **kwargs):
        '''
        name:str
            Specifies the name of the query parameter.
            
        type:ItemDefinition
            Specifies the type of the query parameter.
            
        isRequired:bool
            Specifies, if a parameter is optional or mandatory.
        '''
        super(ResourceParameter, self).__init__(id, **kwargs)
        self.name = name
        self.type = type
        self.isRequired = isRequired
        
        if self.__class__.__name__=='ResourceParameter':
            residual_args(self.__init__, **kwargs)

##########################################################
# Sequence Flow

# A Sequence Flow is used to show the order of Flow Elements in a Process or a Choreography. Each
# Sequence Flow has only one source and only one target. The source and target MUST be from the set of the following
# Flow Elements: Events (Start, Intermediate, and End), Activities (Task and Sub-Process; for Processes),
# Choreography Activities (Choreography Task and Sub-Choreography; for Choreographies), and
# Gateways.
# A Sequence Flow can optionally define a condition Expression, indicating that the token will be passed down the
# Sequence Flow only if the Expression evaluates to true. This Expression is typically used when the source of
# the Sequence Flow is a Gateway or an Activity.

class SequenceFlow(FlowElement):
    '''
    '''
    def __init__(self, id, sourceRef, targetRef, **kwargs):
        '''
        sourceRef:FlowNode
            The FlowNode that the Sequence Flow is connecting from.
            For a Process: Of the types of FlowNode, only Activities, Gateways, and Events can be the source. However, Activities that are Event Sub-Processes are not allowed to be a source.
            For a Choreography: Of the types of FlowNode, only Choreography Activities, Gateways, and Events can be the source.
            
        targetRef:FlowNode
            The FlowNode that the Sequence Flow is connecting to.
            For a Process: Of the types of FlowNode, only Activities, Gateways, and Events can be the target. However, Activities that are Event Sub-Processes are not allowed to be a target.
            For a Choreography: Of the types of FlowNode, only Choreography Activities, Gateways, and Events can be the target.
            
        conditionExpression:Expression
            An optional boolean Expression that acts as a gating condition.
            A token will only be placed on this Sequence Flow if this conditionExpression evaluates to True.
            
        isImmediate:bool
            An optional boolean value specifying whether Activities or Choreography Activities not in the model containing the Sequence Flow
            can occur between the elements connected by the Sequence Flow.
            If the value is true, they MAY NOT occur.
            If the value is false, they MAY occur.
            Also see the isClosed attribute on Process, Choreography, and Collaboration.
            When the attribute has no value, the default semantics depends on the kind of model containing Sequence Flows:
                For non-executable Processes (public Processes and non-executable private Processes) and Choreographies no value has the same semantics as if the value were False.
                For an executable Processes no value has the same semantics as if the value were True.
                For executable Processes, the attribute MUST NOT be false.
        '''
        super(SequenceFlow, self).__init__(id, **kwargs)
        self.sourceRef = sourceRef
        self.targetRef = targetRef
        self.conditionExpression = kwargs.pop('conditionExpression', None)
        self.isImmediate = kwargs.pop('isImmediate', None)
        
        if self.__class__.__init__=='conditionExpression':
            residual_args(self.__init__, **kwargs)
            
class FlowNode(object): #one again unconsistency betweeen figures and text about inheritance in OMG spec
    '''
    The FlowNode element is used to provide a single element as the source and target Sequence Flow associations instead of the individual associations of the elements that can connect to Sequence Flows.
    Only the Gateway, Activity, Choreography Activity, and Event elements can connect to Sequence Flows and thus, these elements are the only ones that are sub-classes of FlowNode.
    Since Gateway, Activity, Choreography Activity, and Event have their own attributes, model associations, and inheritances; the FlowNode element does not inherit from any other BPMN element.
    '''
    def __init__(self, **kwargs):
        '''
        incoming:SequenceFlow list
            This attribute identifies the incoming Sequence Flow of the FlowNode.
        
        outgoing:SequenceFlow list
            This attribute identifies the outgoing Sequence Flow of the FlowNode.
            This is an ordered collection.
        '''
        super(FlowNode, self).__init__()
        self.incoming = kwargs.pop('incoming',[])
        self.outgoing = kwargs.pop('outgoing',[])
        
        if self.__class__.__name__=='FlowNode':
            residual_args(self.__init__, **kwargs)
            
            
            
##########################################################
# Events

# An Event is something that "happens" during the course of a Process. These Events affect the flow of the Process
# and usually have a cause or an impact. The term "event" is general enough to cover many things in a Process. The start
# of an Activity, the end of an Activity, the change of state of a document, a Message that arrives, etc., all could be
# considered Events. However, BPMN has restricted the use of Events to include only those types of Events that will
# affect the sequence or timing of Activities of a Process.


##########################################################
# TBD

class CallableElement(RootElement):
    pass
