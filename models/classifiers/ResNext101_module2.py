#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zcy
# @Date:   2019-02-10 13:13:50
# @Last Modified by:   zcy
# @Last Modified time: 2019-02-10 13:14:43

import torch
import torch.nn as nn
from functools import reduce


__all__ = ['resnext101_64x4d_features']




class LambdaBase(nn.Sequential):
    def __init__(self, fn, *args):
        super(LambdaBase, self).__init__(*args)
        self.lambda_func = fn

    def forward_prepare(self, input):
        output = []
        for module in self._modules.values():
            output.append(module(input))
        return output if output else input

class Lambda(LambdaBase):
    def forward(self, input):
        return self.lambda_func(self.forward_prepare(input))

class LambdaMap(LambdaBase):
    def forward(self, input):
        return list(map(self.lambda_func,self.forward_prepare(input)))

class LambdaReduce(LambdaBase):
    def forward(self, input):
        return reduce(self.lambda_func,self.forward_prepare(input))

resnext101_64x4d_features = nn.Sequential(#Sequential,
    nn.Conv2d(3, 64, (7, 7), (2, 2), (3, 3), 1, 1, bias = False),
    nn.BatchNorm2d(64),
    nn.ReLU(),
    nn.MaxPool2d((3, 3), (2, 2), (1, 1)),
    nn.Sequential(#Sequential,
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(64, 256, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(256),
                        nn.ReLU(),
                        nn.Conv2d(256, 256, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(256),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(256, 256, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(256),
                ),
                nn.Sequential(#Sequential,
                    nn.Conv2d(64, 256, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(256),
                ),
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(256, 256, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(256),
                        nn.ReLU(),
                        nn.Conv2d(256, 256, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(256),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(256, 256, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(256),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(256, 256, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(256),
                        nn.ReLU(),
                        nn.Conv2d(256, 256, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(256),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(256, 256, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(256),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
    ),
    nn.Sequential(#Sequential,
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(256, 512, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(512),
                        nn.ReLU(),
                        nn.Conv2d(512, 512, (3, 3), (2, 2), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(512),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(512, 512, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(512),
                ),
                nn.Sequential(#Sequential,
                    nn.Conv2d(256, 512, (1, 1), (2, 2), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(512),
                ),
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(512, 512, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(512),
                        nn.ReLU(),
                        nn.Conv2d(512, 512, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(512),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(512, 512, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(512),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(512, 512, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(512),
                        nn.ReLU(),
                        nn.Conv2d(512, 512, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(512),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(512, 512, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(512),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(512, 512, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(512),
                        nn.ReLU(),
                        nn.Conv2d(512, 512, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(512),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(512, 512, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(512),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
    ),
    nn.Sequential(#Sequential,
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(512, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (2, 2), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                nn.Sequential(#Sequential,
                    nn.Conv2d(512, 1024, (1, 1), (2, 2), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                        nn.Conv2d(1024, 1024, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(1024),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(1024, 1024, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(1024),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
    ),
    nn.Sequential(#Sequential,
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(1024, 2048, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(2048),
                        nn.ReLU(),
                        nn.Conv2d(2048, 2048, (3, 3), (2, 2), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(2048),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(2048, 2048, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(2048),
                ),
                nn.Sequential(#Sequential,
                    nn.Conv2d(1024, 2048, (1, 1), (2, 2), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(2048),
                ),
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(2048, 2048, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(2048),
                        nn.ReLU(),
                        nn.Conv2d(2048, 2048, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(2048),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(2048, 2048, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(2048),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
        nn.Sequential(#Sequential,
            LambdaMap(lambda x: x, #ConcatTable,
                nn.Sequential(#Sequential,
                    nn.Sequential(#Sequential,
                        nn.Conv2d(2048, 2048, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                        nn.BatchNorm2d(2048),
                        nn.ReLU(),
                        nn.Conv2d(2048, 2048, (3, 3), (1, 1), (1, 1), 1, 64, bias = False),
                        nn.BatchNorm2d(2048),
                        nn.ReLU(),
                    ),
                    nn.Conv2d(2048, 2048, (1, 1), (1, 1), (0, 0), 1, 1, bias = False),
                    nn.BatchNorm2d(2048),
                ),
                Lambda(lambda x: x), #Identity,
            ),
            LambdaReduce(lambda x, y: x + y), #CAddTable,
            nn.ReLU(),
        ),
    )
)