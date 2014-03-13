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
BPMN Package - HumanInteraction
'''

from Core.Foundation.models import BaseElement
from Activities.models import Task
from Process.models import Performer
# from Core.Common.models import FlowNode, FlowElementsContainer
from Core.Common.fonctions import residual_args

class ManualTask(Task):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        '''
        super(ManualTask, self).__init__(id, **kwargs)
        if self.__class__.__name__=='ManualTask':
            residual_args(self.__init__, **kwargs)
            
class UserTask(Task):
    '''
    A User Task is a typical “workflow” Task where a human performer performs the Task with the assistance of a
    software application. The lifecycle of the Task is managed by a software component (called task manager) and is
    typically executed in the context of a Process.
    '''
    def __init__(self, id , implementation='##unspecified', **kwargs):
        '''
        implementation:str (default='##unspecified')
            This attribute specifies the technology that will be used to implement the User Task.
            Valid values are "##unspecified" for leaving the implementation technology open, "##WebService"
            for the Web service technology or a URI identifying any other technology or coordination protocol.
                
        renderings:Rendering list
            This attributes acts as a hook which allows BPMN adopters to specify task rendering attributes
            by using the BPMN Extension mechanism.
        '''
        super(UserTask, self).__init__(id, **kwargs)
        self.implementation = implementation
        self.renderings = kwargs.pop('renderings', [])
        
        #instances attributes
        self.actualOwner = None
        self.taskPriority = None
        
        if self.__class__.__name__ == 'UserTask':
            residual_args(self.__init__, **kwargs)
            
class HumanPerformer(Performer):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        '''
        super(HumanPerformer, self).__init__(id, **kwargs)
        if self.__class__.__name__=='HumanPerformer':
            residual_args(self.__init__, **kwargs)
            
class PotentialOwner(HumanPerformer):
    '''
    '''
    def __init__(self, id, **kwargs):
        '''
        '''
        super(PotentialOwner, self).__init__(id, **kwargs)
        if self.__class__.__name__ == 'PotentialOwner':
            residual_args(self.__init__, **kwargs)