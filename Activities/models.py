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
BPMN Package - Activities
'''

from Core.Foundation.models import BaseElement
from Core.Common.models import FlowNode, FlowElementsContainer
from Core.Common.fonctions import residual_args

class Activity(FlowNode):
    '''
    The Activity class is the abstract super class for all concrete Activity types.
    An Activity is work that is performed within a Business Process. An Activity can be atomic or non-atomic (compound).
    The types of Activities that are a part of a Process are: Task, Sub-Process, and Call Activity, which allows the inclusion of re-usable Tasks and Processes in the diagram.
    However, a Process is not a specific graphical object. Instead, it is a set of graphical objects.
    The following sections will focus on the graphical objects Sub-Process and Task.
    Activities represent points in a Process flow where work is performed.
    They are the executable elements of a BPMN Process.
    '''
    def __init__(self, id, **kwargs):
        '''
        isForCompensation:bool (default=False)
            A flag that identifies whether this Activity is intended for the purposes of compensation.
            If False, then this Activity executes as a result of normal execution flow.
            If True, this Activity is only activated when a Compensation Event is detected and initiated under Compensation Event visibility scope.

        loopCharacteristics:LoopCharacteristics
            An Activity MAY be performed once or MAY be repeated.
            If repeated, the Activity MUST have loopCharacteristics that define the repetition criteria
            (if the isExecutable attribute of the Process is set to True).
        
        resources:ResourceRole list
            Defines the resource that will perform or will be responsible for the Activity.
            The resource, e.g., a performer, can be specified in the form of a specific individual, a group, an organization role or position, or an organization.

        default:SequenceFlow
            The Sequence Flow that will receive a token when none of the conditionExpressions on other outgoing Sequence Flows evaluate
            to True. The default Sequence Flow should not have a conditionExpression. Any such Expression SHALL be ignored.
        
        ioSpecification:InputOutputSpecification
            The InputOutputSpecification defines the inputs and outputs and the InputSets and OutputSets for the Activity.

        properties:Property list
            Modeler-defined properties MAY be added to an Activity. These properties are contained within the Activity.
        
        boundaryEventRefs:BoundaryEvent list
            This references the Intermediate Events that are attached to the boundary of the Activity.

        dataInputAssociations:DataInputAssociation list
            An optional reference to the DataInputAssociations. A DataInputAssociation defines how the DataInput of the Activity's
            InputOutputSpecification will be populated.

        dataOutputAssociations:DataOutputAssociation list
            An optional reference to the DataOutputAssociations.
            
        startQuantity:int (default=1)
            The value MUST NOT be less than 1.
            This attribute defines the number of tokens that MUST arrive before the Activity can begin.
            Note that any value for the attribute that is greater than 1 is an advanced type of modeling and should be used with caution.
            
        completionQuantity:int (default=1)
            The value MUST NOT be less than 1.
            This attribute defines the number of tokens that MUST be generated from the Activity.
            This number of tokens will be sent done any outgoing Sequence Flow (assuming any Sequence Flow conditions are satisfied).
            Note that any value for the attribute that is greater than 1 is an advanced type of modeling and should be used with caution.
        '''
        super(Activity, self).__init__(id, **kwargs)
        #instance attribute default value
        self.state = 'None'
        
        self.isForCompensation = kwargs.pop('isForCompensation', False)
        self.loopCharacteristics = kwargs.pop('loopCharacteristics', None)
        self.resources = kwargs.pop('resources', [])
        self.default = kwargs.pop('default', None)
        self.ioSpecification = kwargs.pop('ioSpecification', None)
        self.properties = kwargs.pop('properties', [])
        self.boundaryEventRefs = kwargs.pop('boundaryEventRefs',[])
        self.dataInputAssociations = kwargs.pop('dataInputAssociations', [])
        start_quantity = kwargs.pop('startQuantity', 1)
        if start_quantity >= 1:
            self.startQuantity = int(start_quantity)
        else:
            raise Exception # à préciser
        completion_quantity = kwargs.pop('completionQuantity', 1)
        if completion_quantity >=1:
            self.completionQuantity = int(completion_quantity)
        else:
            raise Exception # à préciser
            
        if self.__class__.__name__ == 'Activity':
            residual_args(self.__init__, **kwargs)
            
class Task(Activity):
    def __init__(self, id, **kwargs):
        super(Task, self).__init__(id, **kwargs)
        if self.__class__.__name__ == 'Task':
            residual_args(self.__init__, **kwargs)

class ServiceTask(Task):
    '''
    A Service Task is a Task that uses some sort of service, which could be a Web service or an automated application.
    '''
    def __init__(self, id, implementation='##WebService', **kwargs):
        '''
        implementation:str (default='##WebService')
            This attribute specifies the technology that will be used to send and receive the Messages.
            Valid values are "##unspecified" for leaving the implementation technology open,
            "##WebService" for the Web service technology or a URI identifying any other technology or coordination protocol.
            A Web service is the default technology.
            
        operationRef:Operation
            This attribute specifies the operation that is invoked by the Service Task.
        '''
        super(ServiceTask, self).__init__(id, **kwargs)
        self.implementation = implementation
        self.operationRef = kwargs.pop('operationRef', None)
        
        #ServiceTask conditions to be add
        if self.__class__.__name__=='ServiceTask':
            residual_args(self.__init__, **kwargs)
    
class SendTask(Task):
    '''
    A Send Task is a simple Task that is designed to send a Message to an external Participant
    (relative to the Process). Once the Message has been sent, the Task is completed.
    '''
    def __init__(self, id, operationRef, implementation='##WebService', **kwargs):
        '''
        operationRef:Operation
            This attribute specifies the operation that is invoked by the Send Task.
        
        implementation:str (default='##WebService')
            This attribute specifies the technology that will be used to send and receive the Messages.
            Valid values are "##unspecified" for leaving the implementation technology open, "##WebService" for the Web service technology or a URI
            identifying any other technology or coordination protocol.
     
        messageRef:Message
            A Message for the messageRef attribute MAY be entered.
            This indicates that the Message will be sent by the Task.
            The Message in this context is equivalent to an out-only message pattern (Web service).
            The Message is applied to all outgoing Message Flows and the Message will be sent down
            all outgoing Message Flows at the completion of a single instance of the Task.
        '''
        super(SendTask, self).__init__(id, **kwargs)
        self.operationRef = operationRef
        self.implementation = implementation
        self.messageRef = kwargs.pop('messageRef', None)
        #Send Task conditions to ba add
        if self.__calss__.__name__=='SendTask':
            residual_args(self.__init__, **kwargs)
        
class ReceiveTask(Task):
    '''
    A Receive Task is a simple Task that is designed to wait for a Message to arrive from an external Participant
    (relative to the Process). Once the Message has been received, the Task is completed.
    '''
    def __init__(self, id, operationRef, implementation='##WebService', **kwargs):
        '''
        operationRef:Operation
            This attribute specifies the operation through which the Receive Task receives the Message.

        implementation:str (default='##WebService')
            This attribute specifies the technology that will be used to send and receive
            the Messages. Valid values are "##unspecified" for leaving the implementation
            technology open, "##WebService" for the Web service technology or a URI identifying any other
            technology or coordination protocol.

        messageRef:Message
            A Message for the messageRef attribute MAY be entered.
            This indicates that the Message will be received by the Task.
            The Message in this context is equivalent to an in-only message pattern (Web service).
            The Message is applied to all incoming Message Flows,
            but can arrive for only one of the incoming Message Flows for a single instance of the Task.
        
        instantiate:bool (default=False)
            Receive Tasks can be defined as the instantiation mechanism for the
            Process with the instantiate attribute.
            This attribute MAY be set to true if the Task is the first Activity (i.e., there are no incoming Sequence Flows).
            Multiple Tasks MAY have this attribute set to true.
        '''
        super(ReceiveTask, self).__init__(id, **kwargs)
        self.operationRef = operationRef
        self.implementation = implementation
        self.messageRef = kwargs.pop('messageRef', None)
        self.instantiate = kwargs.pop('instantiate', False)
        #ReceiveTask conditions to ba add
        if self.__class__.__name__=='ReceiveTask':
            residual_args(slf.__init__, **kwargs)
            
class BusinessRuleTask(Task):
    '''
    A Business Rule Task provides a mechanism for the Process to provide input to a Business Rules Engine and to get
    the output of calculations that the Business Rules Engine might provide.
    The InputOutputSpecification of the Task will allow the Process to send data to and receive data from the Business Rules Engine.
    '''
    def __init__(self, id, implementation='##unspecified', **kwargs):
        '''
        implementation:str (default='##unspecified')
            This attribute specifies the technology that will be used to implement the Business Rule Task.
            Valid values are "##unspecified" for leaving the implementation technology open, "##WebService"
            for the Web service technology or a URI identifying any other technology or coordination protocol.
        '''
        super(BusinessRuleTask, self).__init__(id, **kwargs)
        self.implementation = implementation
        
        if self.__class__.__name__=='BusinessRuleTask':
            residual_args(self.__init__, **kwargs)
            
class ScriptTask(Task):
    '''
    A Script Task is executed by a business process engine. The modeler or implementer defines a script in a language that
    the engine can interpret (typicaly python in this particular implementation). When the Task is ready to start, the engine will execute the script.
    When the script is completed, the Task will also be completed.
    '''
    def __init__(self, id, **kwargs):
        '''
        scriptFormat:str
            Defines the format of the script. This attribute value MUST be specified with a mime-type format.
            And it MUST be specified if a script is provided.
        
        script:str
            The modeler MAY include a script that can be run when the Task is performed (typicaly python in this particular implementation).
            If a script is not included, then the Task will act as the equivalent of an Abstract Task.
        '''
        super(ScriptTask, self).__init__(id, **kwargs)
        self.scriptFormat = kwargs.pop('scriptFormat', None)
        self.script = kwargs.pop('script', None)
        
        if self.__class__.__name__ == 'ScriptTask':
            residual_args(self.__init__, **kwargs)
            
            
class CallActivity(Activity):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        calledElementRef:???
        '''
        super(CallActivity, self).__init__(id, **kwargs)
        self.calledElementRef = kwargs.pop('calledElementRef', None) #?
        
        if self.__class__.__name__=='CallActivity':
            residual_args(self.__init__, **kwargs)
        
class SubProcess(Activity, FlowElementsContainer):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        triggeredByEvent:bool (default=False)
        '''
        super(SubProcess, self).__init__(id, **kwargs) #comment ça se comporte en cas d'heritage multiple
        self.triggeredByEvent = kwargs.pop('triggeredByEvent', False)
        
        if self.__class__.__name__=='SubProcess':
            residual_args(self.__init__, **kwarg)

class ResourceRole(BaseElement):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        resourceRef:Resource
            The Resource that is associated with Activity.
            Should not be specified when resourceAssignmentExpression is provided.
        
        resourceAssignmentExpression:ResourceAssignmentExpression
            This defines the Expression used for the Resource assignment.
            Should not be specified when a resourceRef is provided.
        
        resourceParameterBindings:ResourceParameterBinding list
            This defines the Parameter bindings used for the Resource assignment.
            Is only applicable if a resourceRef is specified.
        '''
        super(ResourceRole, self).__init__(id, **kwargs)
        if kwargs.has_key('resourceRef') and kwargs.has_key('resourceAssignmentExpression'):
            raise Exception # à préciser
        self.resourceRef = kwargs.pop('resourceRef', None)
        self.resourceAssignmentExpression = kwargs.pop('resourceAssignmentExpression', None)
        self.resourceParameterBindings = kwargs.pop('resourceParameterBindings', [])
        
        if self.__class__.__name__=='ResourceRole':
            residual_args(self.__init__, **kwargs)
            
class ResourceAssignmentExpression(BaseElement):
    '''
    '''
    def __init__(self, id, expression, **kwargs):
        '''
        expression:Expression
            The element ResourceAssignmentExpression MUST contain an Expression which is used
            at runtime to assign resource(s) to a ResourceRole element.
        '''
        super(ResourceAssignmentExpression, self).__init__(id, **kwargs)
        self.expression = expression
        
        if self.__class__.__name__=='ResourceAssignmentExpression':
            residual_args(self.__init__, **kwargs)
            

class ResourceParameterBindings(BaseElement):
    '''
    '''
    def __init__(self, id, parameterRef, expression, **kwargs):
        '''
        parameterRef:ResourceParameter
            Reference to the parameter defined by the Resource.
        expression:Expression
            The Expression that evaluates the value used to bind the ResourceParameter.
        '''
        super(ResourceParameterBindings, self).__init__(id, **kwargs)
        self.parameterRef = parameterRef
        self.expression = expression
        
        if self.__class__.__name__=='ResourceParameterBindings':
            residual_args(self.__init__, **kwargs)


#LoopCharacteristics
#StandardLoopCharacteristics
#MultiInstanceLoopCharaceristics
