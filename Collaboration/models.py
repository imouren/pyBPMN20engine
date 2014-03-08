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
BPMN Package - Collaboration

The Collaboration package contains classes that are used for modeling Collaborations, which is a collection of
Participants shown as Pools, their interactions as shown by Message Flows, and MAY include Processes within the
Pools and/or Choreographies between the Pools. A Choreography is an extended type of
Collaboration. When a Collaboration is defined it is contained in Definitions.
'''

from Core.Foundation.models import BaseElement, RootElement
from Core.Common.fonctions import residual_args

class Collaboration(RootElement):
    '''
    '''
    def __init__(self, id, name, isClosed=False, **kwarg):
        '''
        name:str
            Name is a text description of the Collaboration.
            
        isClosed:bool
            A boolean value specifying whether Message Flows not modeled in the Collaboration can occur when the Collaboration is carried out.
                If the value is True, they MAY NOT occur.
                If the value is False, they MAY occur.
        
        choreographyRef:Choreography list
            The choreographyRef model association defines the Choreographies that can be shown between the Pools of the Collaboration.
            A Choreography specifies a business contract (or the order in which messages will be exchanged) between interacting Participants.
            The participantAssociations (see below) are used to map the Participants of the Choreography to the Participants of the Collaboration.
            The MessageFlowAssociations (see below) are used to map the Message Flows of the Choreography to the Message Flows of the Collaboration.
            The conversationAssociations (see below) are used to map the Conversations of the Choreography to the Conversations of the Collaboration.
            Note that this attribute is not applicable for Choreography or GlobalConversation which are a subtypes of Collaboration.
            Thus, a Choreography cannot reference another Choreography.
        
        correlationKeys:CorrelationKey list
            This association specifies CorrelationKeys used to associate Messages to a particular Collaboration.
            
        conversationAssociations:ConversationAssociation list
            This attribute provides a list of mappings from the Conversations of a referenced Collaboration to the Conversations of another Collaboration.
            It is used when a Choreography is referenced by a Collaboration.
        
        conversations:ConversationNode list
            The conversations model aggregation relationship allows a Collaboration to contain Conversation elements,
            in order to group Message Flows of the Collaboration and associate correlation information,
            as is REQUIRED for the definitional Collaboration of a Process model.
            The Conversation elements will be visualized if the Collaboration is a Collaboration, but not for a Choreography.
        
        conversationLinks:ConversationLink list
            This provides the Conversation Links that are used in the Collaboration.
            
        artifacts:Artifact list
            This attribute provides the list of Artifacts that are contained within the Collaboration.
            
        participants:Participant list
            This provides the list of Participants that are used in the Collaboration.
            Participants are visualized as Pools in a Collaboration and
            as Participant Bands in Choreography Activities in a Choreography.

        participantAssociations:ParticipantAssociations list
            This attribute provides a list of mappings from the Participants of a referenced Collaboration to the Participants of another Collaboration.
            It is used in the following situations:
                When a Choreography is referenced by the Collaboration.
                When a definitional Collaboration for a Process is referenced through a Call Activity (and mapped to definitional Collaboration of the calling Process).
        
        messageFlow:MessageFlow list
            This provides the list of Message Flows that are used in the Collaboration.
            Message Flows are visualized in Collaboration (as dashed line) and hidden in Choreography.

        messageFlowAssoxiations:MessageFlowAssociation list
            This attribute provides a list of mappings for the Message Flows of the Collaboration to Message Flows of a referenced model.
            It is used in the following situation:
                When a Choreography is referenced by a Collaboration. This allows the "wiring up" of the Collaboration Message Flows to th eappropriate Choreography Activities.
        '''
        super(Collaboration, self).__init__(id, **kwargs)
        self.name = name
        self.isClosed = isClosed
        self.choreographyRef = kwargs.pop('choreographyRef',[])
        self.correlationKeys = kwargs.pop('correlationKeys',[])
        self.conversationAssociations = kwargs.pop('conversationAssociations',[])
        self.conversations = kwargs.pop('conversations',[])
        self.conversationLinks = kwargs.pop('conversationLinks',[])
        self.artifacts = kwargs.pop('artifacts',[])
        self.participants = kwargs.pop('participants',[])
        self.participantAssociations = kwargs.pop('participantAssociations',[])
        self.messageFlow = kwargs.pop('messageFlow',[])
        self.messageFlowAssociations = kwargs.pop('messageFlowAssociations:',[])
        
        if self.__class__.__name__=='Collaboration':
            residual_args(self.__init__, **kwargs)

class InteractionNode(object):
    '''
    The InteractionNode element is used to provide a single element as the source and target Message Flow associations instead of
    the individual associations of the elements that can connect to Message Flows.
    Only the Pool/Participant, Activity, and Event elements can connect to Message Flows.
    The InteractionNode element is also used to provide a single element for source and target of Conversation Links.
    '''
    pass
            
class Participant(BaseElement, InteractionNode):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        name:str
            Name is a text description of the Participant.
            The name of the Participant can be displayed directly or it can be substituted by the associated PartnerRole or PartnerEntity.
            Potentially, both the PartnerEntity name and PartnerRole name can be displayed for the Participant.

        processRef:Process
            The processRef attribute identifies the Process that the Participant uses in the Collaboration.
            The Process will be displayed within the Participant's Pool.
            
        partnerRoleRef:PartnerRole list
            The partnerRoleRef attribute identifies a PartnerRole that the Participant plays in the Collaboration.
            Both a PartnerRole and a PartnerEntity MAY be defined for the Participant.
            This attribute is derived from the participantRefs of PartnerRole.
            The partnerRoleRef attribute identifies a PartnerRole that the Participant plays in the Collaboration.
            Both a PartnerRole and a PartnerEntity MAY be defined for the Participant.
            This attribute is derived from the participantRefs of PartnerRole.
            
        partnerEntityRef:PartnerEntity list
            The partnerEntityRef attribute identifies a PartnerEntity that the Participant plays in the Collaboration.
            Both a PartnerRole and a PartnerEntity MAY be defined for the Participant.
            This attribute is derived from the participantRefs of PartnerEntity.
            
        interfaceRef:Interface list
            This association defines Interfaces that a Participant supports.
        
        participantMultiplicityRef:ParticipantMultiplicity
            The participantMultiplicityRef model association is used to define Participants that represent more than one
            instance of the Participant for a given interaction.
            
        endPointRefs:EndPoint list
            This attribute is used to specify the address (or endpoint reference) of concrete services
            realizing the Participant.
        '''
        super(Participant,self).__init__(id, **kwargs)
        self.name = kwargs.pop('name', None)
        self.processRef = kwargs.pop('processRef', None)
        self.partnerRoleRef = kwargs.pop('partnerRoleRef', [])
        self.partnerEntityRef = kwargs.pop('partnerEntityRef', [])
        self.interfaceRef = kwargs.pop('interfaceRef', [])
        self.participantMultiplicityRef = kwargs.pop('participantMultiplicityRef', None)
        self.endPointRefs = kwargs.pop('endPointRefs', [])
        
        if self.__class__.__name__=='Participant':
            residual_args(self.__init__, **kwargs)
            
class ParticipantMultiplicity(object):
    '''
    ParticipantMultiplicity is used to define the multiplicity of a Participant.
    The multi-instance marker will be displayed in bottom center of the Pool, or the Participant Band of a Choreography
    Activity, when the ParticipantMultiplicity is associated with the Participant, and the maximum attribute is either not set,
    or has a value of two or more.
    '''
    def __init__(self, minimum=0, maximum=None):
        '''
        minimum:int (default=0)
            The minimum attribute defines minimum number of Participants that MUST be involved in the Collaboration.
            If a value is specified in the maximum attribute, it MUST be greater or equal to this minimum value.
            
        maximum:int (default=None)
            The maximum attribute defines maximum number of Participants that MAY be involved in the Collaboration.
            The value of maximum MUST be one or greater, AND MUST be equal or greater than the minimum value.
        '''
        self.minimum = minimum
        if (maximum is None) or (maximum>minimum and maximum>0):
            self.maximum = maximum
        else:
            raise Exception # to precise
        
        # instance attribute default value
        self.numParticipants = None
        
class ParticipantAssociation(BaseElement):
    '''
    '''
    def __init__(self, id, innerParticipantRef, outerParticipantRef, **kwargs):
        '''
        innerParticipantRef:Participant
            This attribute defines the Participant of the referenced element (e.g., a Choreography to be used in a Collaboration)
            that will be mapped to the parent element (e.g., the Collaboration).
            
        outerParticipantRef:Participant
            This attribute defines the Participant of the parent element (e.g., a Collaboration references a Choreography)
            that will be mapped to the referenced element (e.g., the Choreography).
        '''
        super(ParticipantAssociation, self).__init__(id, **kwargs)
        self.innerParticipantRef = innerParticipantRef
        self.outerParticipantRef = outerParticipantRef
        
        if self.__class__.__name__=='ParticipantAssociation':
            residual_args(self.__init__, **kwargs)


    
class MessageFlow(BaseElement):
    '''
    '''
    def __init__(self, id, name, sourceRef, targetRef, **kwargs):
        '''
        name:str
            Name is a text description of the Message Flow.

        sourceRef:InteractionNode
            The InteractionNode that the Message Flow is connecting from.
            Of the types of InteractionNode, only Pools/Participants, Activities, and Events can be the source of a Message Flow.

        targetRef:InteractionNode
            The InteractionNode that the Message Flow is connecting to.
            Of the types of InteractionNode, only Pools/Participants, Activities, and Events can be the target of a Message Flow.
            
        messageRef:Message
            The messageRef model association defines the Message that is passed via the Message Flow.
        '''
        super(MessageFlow, self).__init__(id, **kwargs)
        self.name = name
        self.sourceRef = sourceRef
        self.targetRef = targetRef
        self.messageRef = kwargs.pop('messagRef', None)
        
        if self.__class__.__name__=='MessageFlow':
            residual_args(self.__init__, **kwargs)
            
class MessageFlowAssociation(BaseElement):
    '''
    '''
    def __init__(self, id, innerMessageFlowRef, outerMessageFlowRef, **kwargs):
        '''
        innerMessageFlowRef:MessageFlow
            This attribute defines the Message Flow of the referenced element (e.g., a Choreography to be used in a Collaboration)
            that will be mapped to the parent element (e.g., the Collaboration).
        
        outerMessageFlowRef:MessageFlow
            This attribute defines the Message Flow of the parent element (e.g., a Collaboration references a Choreography) that will be
            mapped to the referenced element (e.g., the Choreography).
        '''
        super(MessageFlowAssociation, self).__init__(id, **kwargs)
        self.innerMessageFlowRef = innerMessageFlowRef
        self.outerMessageFlowRef = outerMessageFlowRef
        
        if self.__class__.__name__=='MessageFlowAssociation':
            residual_args(self.__init__, **kwargs)
            
