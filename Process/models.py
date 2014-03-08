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
BPMN Package - Process
'''

from Core.Foundation.models import BaseElement, RootElement
from Core.Common.models import FlowElementsContainer, CallableElement
from Core.Common.fonctions import residual_args

ProcessType = ['None', 'Private', 'Public']

class Process(FlowElementsContainer, CallableElement):
    '''
    '''
    def __init__(self, id, processType='None', **kwargs):
        '''
        processType: ProcessType (default='None') {'None'|'Private'|'Public'}
            The processType attribute Provides additional information about the level of abstraction modeled by this Process.
            A public Process shows only those flow elements that are relevant to external consumers.
            Internal details are not modeled. These Processes are publicly visible and can be used within a Collaboration.
            Note that the public processType was named abstract in BPMN 1.2.
            A private Process is one that is internal to a specific organization.
            'None' means undefined.
            
        isExecutable:bool
            An optional Boolean value specifying whether the Process is executable.
            An executable Process is a private Process that has been modeled for the purpose of being executed.
            Of course, during the development cycle of the Process, there will be stages where the Process does not have enough
            detail to be "executable". A non-executable Process is a private Process that has been modeled
            for the purpose of documenting Process behavior at a modeler-defined level of detail.
            Thus, information needed for execution, such as formal condition expressions are typically not included in a non-executable Process.
            For public Processes, no value has the same semantics as if the value were false.
            The value MAY not be true for public Processes.
            
        auditing:Auditing
            This attribute provides a hook for specifying audit related properties.
            
        monitoring:Monitoring
            This attribute provides a hook for specifying monitoring related properties.
        
        artifacts:Artifact list
            This attribute provides the list of Artifacts that are contained within the Process.
        
        isClosed:bool (default=False)
            A boolean value specifying whether interactions, such as sending and receiving Messages and Events, not modeled in the Process can
            occur when the Process is executed or performed.
            If the value is true, they MAY NOT occur.
            If the value is false, they MAY occur.
        
        supports:Process list
            Modelers can declare that they intend all executions or performances of one Process to also be valid for another Process.
            This means they expect all the executions or performances of the first Processes to also follow the steps laid out in the second Process.

        properties:Property list
            Modeler-defined properties MAY be added to a Process.
            These properties are contained within the Process. All Tasks and Sub-Processes SHALL have access to these properties.
        
        resources:ResourceRole list
            Defines the resource that will perform or will be responsible for the Process.
            The resource, e.g., a performer, can be specified in the form of a specific individual, a group,
            an organization role or position, or an organization.
            Note that the assigned resources of the Process does not determine the assigned resources of the Activities that are contained by the Process.
        
        correlationSubscriptions:CorrelationSubscription list
            correlationSubscriptions are a feature of context-based correlation.
            CorrelationSubscriptions are used to correlate incoming Messages against data in the Process context.
            A Process MAY contain several correlationSubscriptions.
        
        definitionalCollaborationRef:Collaboration
            For Processes that interact with other Participants, a definitional Collaboration can be referenced by the Process.
            The definitional Collaboration specifies the Participants the Process interacts with,
            and more specifically, which individual service, Send or Receive Task,
            or Message Event, is connected to which Participant through Message Flows.
            The definitional Collaboration need not be displayed.
            Additionally, the definitional Collaboration can be used to include Conversation information within a Process.
        '''
        super(Process, self).__init__(id, **kwargs) #il appelle les deux init ? Comment ?
        
        # instance attribute default value
        self.state = 'None'
        
        self.processType = processType
        self.isExecutable = kwargs.pop('isExecutable', None) #Means False
        self.auditing =  kwargs.pop('auditing', None)
        self.monitoring = kwargs.pop('monitoring', None)
        self.artifacts = kwargs.pop('artifacts', [])
        self.isClosed =  kwargs.pop('isClosed', False)
        self.supports = kwargs.pop('supports', [])
        self.properties =  kwargs.pop('properties', [])
        self.resources =  kwargs.pop('resources', [])
        self.correlationSubscriptions = kwargs.pop('correlationSubscriptions', [])
        self.definitionalCollaborationRef = kwargs.pop('definitionalCollaborationRef', None)
        
        if self.__class__.__name__=='Process':
            residual_args(self.__init__, **kwargs)