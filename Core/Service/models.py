# -*- coding: utf-8 -*-

'''
Core BPMN Package - Service
'''

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

from Core.Foundation.models import RootElement, BaseElement
from Core.Common.fonctions import residual_args

class Interface(RootElement):
    '''
    An Interface defines a set of operations that are implemented by Services.
    '''
    def __init__(self, id, name, operations, **kwargs):
        '''
        name:str
            The descriptive name of the element.
            
        operations:Operation list (min len = 1)
            This attribute specifies operations that are defined as part of the Interface.
            An Interface has at least one Operation.
            
        callableElements:CallableElement list
            The CallableElements that use this Interface.
        
        implementationRef:Element
            This attribute allows to reference a concrete artifact in the underlying implementation technology representing
            that interface, such as a WSDL porttype.
        '''
        super(Interface, self).__init__(id, **kwargs)
        self.name = name
        self.operations = operations
        self.callableElements = kwargs.pop('callableElements',[])
        self.implementationRef = kwargs.pop('implementationRef', None)
        
        if self.__class__.__name__=='Interface':
            residual_args(self.__init__, **kwargs)
            
            
class EndPoint(RootElement):
    '''
    The actual definition of the service address is out of scope of BPMN 2.0. The EndPoint element is an extension point
    and extends from RootElement. The EndPoint element MAY be extended with endpoint reference definitions
    introduced in other specifications (e.g., WS-Addressing).
    EndPoints can be specified for Participants.
    '''
    def __init__(self, id, **kwargs):
        '''
        '''
        super(EndPoint).__init__(id, **kwargs)
        if self.__class__.__name__=='EndPoint':
            residual_args(self.__init__, **kwargs)
            
class Operation(BaseElement):
    '''
    An Operation defines Messages that are consumed and, optionally, produced when the Operation is called.
    It can also define zero or more errors that are returned when operation fails.
    '''
    def __init__(self, id, name, inMessageRef, **kwargs):
        '''
        name:str
            The descriptive name of the element.
            
        inMessageRef:Message
            This attribute specifies the input Message of the Operation.
            An Operation has exactly one input Message.
        
        outMessageRef:Message
            This attribute specifies the output Message of the Operation.
            An Operation has at most one input Message.
            
        errorRef:Error list
            This attribute specifies errors that the Operation may return.
            An Operation MAY refer to zero or more Error elements.
            
        implementationRef:Element
            This attribute allows to reference a concrete artifact in the underlying implementation
            technology representing that operation, such as a WSDL operation.
        '''
        super(Operation,self).__init__(id, **kwargs)
        self.name = name
        self.inMessageRef = inMessageRef
        self.outMessageRef = kwargs.pop('outMessageRef', None)
        self.errorRef = kwargs.pop('errorRef', [])
        self.implementationRef = kwargs.pop('implementationRef', None)
        
        if self.__class__.__name__=='Operation':
            residual_args(self.__init__, **kwargs)
            
