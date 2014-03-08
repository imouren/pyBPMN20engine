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
BPMN Package - Conversations
'''

from Core.Foundation.models import BaseElement, RootElement
from Core.Common.fonctions import residual_args

from Collaboration.models import Collaboration

class ConversationNode(BaseElement):
    '''
    ConversationNode is the abstract super class for all elements that can comprise the Conversation elements of a Collaboration diagram,
    which are Conversation, Sub-Conversation, and Call Conversation (see page 131).
    '''
    def __init__(self, id, participantRefs, **kwargs):
        '''
        participantRefs:Participant list (min len = 2)
            This provides the list of Participants that are used in the ConversationNode from the list provided by the ConversationNode's parent Conversation.
            This reference is visualized through a Conversation Link.
            
        name:str
            Name is a text description of the ConversationNode element.
            
        messageFlowRefs:MessageFlow list
            A reference to all Message Flows (and consequently Messages) grouped by a Conversation element.
        
        correlationKeys:CorrelationKey list
            This is a list of the ConversationNode's CorrelationKeys, which are used to group Message Flows for the ConversationNode.
        '''
        super(ConversationNode, self).__init__(id, **kwargs)
        self.participantRefs = participantRefs
        self.name = kwargs.pop('name',None)
        self.messageFlowRefs = kwargs.pop('messageFlowRefs',[])
        self.correlationKeys = kwargs.pop('correlationKeys',[])
        
        if self.__class__.__name__=='ConversationNode':
            residual_args(self.__init__, **kwargs)
            

class Conversation(ConversationNode):
    pass
    
class SubConversation(ConversationNode):
    '''  
    '''
    def __init__(self, id, participantRefs, **kwargs):
        '''
        conversationNodes:ConversationNode list
            The ConversationNodes model aggregation relationship allows a SubConversation to contain other ConversationNodes,
            in order to group Message Flows of the Sub-Conversation and associate correlation information.
        '''
        super(SubConversation, self).__init__(id, participantRefs, **kwargs)
        self.conversationNodes = kwargs.pop('conversationNodes',[])

class CallConversation(ConversationNode):
    '''
    '''
    def __init__(self, id, participantRefs, **kwargs):
        '''
        calledCollaborationRef:Collaboratioin
            The element to be called, which MAY be either a Collaboration or a GlobalConversation.
            The called element MUST NOT be a Choreography or a GlobalChoreographyTask (which are subtypes of Collaboration)
            
        participantAssociations:ParticipantAssociation list
            This attribute provides a list of mappings from the Participants of a referenced GlobalConversation or Conversation to the
            Participants of the parent Conversation.

        //Note - The ConversationNode attribute messageFlowRef doesn't apply to Call Conversations.
        '''
        super(CallConversation, self).__init__(id, participantRefs, messageFlowRef=[], **kwargs)
        self.calledCollaborationRef = kwargs.pop('calledCollaborationRef', None)
        self.participantAssociations = kwargs.pop('participantAssociations', [])
        
        if self.__class__.__name__=='CallConversation':
            residual_args(self.__init__, **kwargs)

class GlobalConversation(Collaboration):
    '''
    A GlobalConversation is a restricted type of Collaboration, it is an "empty Collaboration".
    A GlobalConversation MUST NOT contain any ConversationNodes.
    Since a GlobalConversation does not have any Flow Elements, it does not require
    MessageFlowAssociations, ParticipantAssociations, or ConversationAssociations or Artifacts.
    It is basically a set of Participants, Message Flows, and CorrelationKeys intended for reuse.
    Also, the Collaboration attribute choreographyRef is not applicable to GlobalConversation.
    '''
    # control of the restriction to add.
    pass
    
class ConversationLink(BaseElement):
    '''
    '''
    def __init__(self, id, sourceRef, targetRef, **kwargs):
        '''
        sourceRef:InteractionNode
            The InteractionNode that the Conversation Link is connecting from.
            A Conversation Link MUST connect to exactly one ConversationNode.
            If the sourceRef is not a ConversationNode, then the targetRef MUST be a ConversationNode.
            
        targetRef:InteractionNode
            The InteractionNode that the Conversation Link is connecting to.
            A Conversation Link MUST connect to exactly one ConversationNode.
            If the targetRef is not a ConversationNode, then the sourceRef MUST be a ConversationNode.
        
        name:str
            This attribute specifies the name of the Conversation Link.        
        '''
        super(ConvesationNode, self).__init__(id, **kwargs)
        self.sourceRef = sourceRef
        self.targetRef = targetRef
        self.name = kwargs.pop('name', None)
        
        #ajouter le test d'une et une seule instance de ConversationNode dans source et target
        
        if self.__class__.__name__=='ConversationLink':
            residual_args(self.__init__, **kwargs)
            
class ConversationAssociation(BaseElement):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        innerConversationNodeRef:ConversationNode
            This attribute defines the ConversationNodes of the referenced element (e.g., a Choreography to be used in a Collaboration)
            that will be mapped to the parent element (e.g., the Collaboration).
        
        outerConversationNodeRef:ConversationNode list
            This attribute defines the ConversationNodes of the parent element (e.g., a Collaboration references a Choreography)
            that will be mapped to the referenced element (e.g., the Choreography).
        '''
        super(ConversationAssociation, self).__init__(id, **kwargs)
        self.innerConversationNodeRef = kwargs.pop('innerConversationNodeRef', None)
        self.outerConversationNodeRef = kwargs.pop('outerConversationNodeRef', [])
        
        if self.__class__.__name__=='ConversationAssociation':
            residual_args(self.__init__, **kwargs)
            
