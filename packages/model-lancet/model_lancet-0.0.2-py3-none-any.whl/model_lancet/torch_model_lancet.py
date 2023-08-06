import torch
from functools import partial
from typing import Any
from types import MethodType
import logging


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('torch_model_lancet')


class ModelLancet:
    def __init__(self, target_module_class_name: str, target_function_name: str = 'forward'):
        self.target_module_class_name = target_module_class_name
        self.target_function_name = target_function_name

    def __call__(self, function: Any):
        wrapped_fn = partial(
            ModelLancet._replace_function,
            target_module_class_name = self.target_module_class_name,
            target_function_name=self.target_function_name,
            function=function
        )
        return wrapped_fn
    
    @staticmethod
    def _replace_function(
        instance: torch.nn.Module, 
        target_module_class_name: str, 
        target_function_name: str, 
        function: Any
        ):
        # if instance's class is the target module class
        # or instance's class is inherited from the target module class
        # then set set the method else pass
        if target_module_class_name == instance.__class__.__name__ \
        or any(map(lambda x: target_module_class_name == x.__name__, instance.__class__.mro())):
            instance.__class__.__setattr__(
                instance, 
                target_function_name, 
                MethodType(function, instance)
            )
            logger.info(f'replaced {instance.__class__.__name__}\'s fn "{target_function_name}" with "{function.__name__}"')
        else:
            pass


if __name__ == '__main__':

    x = torch.randn(5,4)

    class SubLayer(torch.nn.Module):
        def __init__(self):
            super().__init__()

        def forward(self, x):
            return self.fake_forward(x)

        def fake_forward(self, x):
            logger.info('forwarding origin sub layer\'s fake_forward function')
            return x

    class NSubLayer(SubLayer):

        def __init__(self):
            super().__init__()

        def fake_forward(self, x):
            logger.info('forwarding origin new sub layer\'s fake_forward function')
            return x


    class SubModule(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.sub_layer = NSubLayer()

        def forward(self, x):
            logger.info('forwarding origin sub module\'s forward function')
            return self.sub_layer(x)

        
    class Model(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.sub_module = SubModule()

        def forward(self, x):
            return self.sub_module(x)

    model = Model()
    logger.info('origin model:')
    logger.info(model)
    logger.info('forwarding origin model')
    out = model(x)

    logger.info('-------\n')

    # decorate the function to replace
    @ModelLancet('SubModule')
    def new_forward(self, x):
        logger.info('forwarding new sub module\'s forward function')
        return self.sub_layer.fake_forward(x)
    # 
    model.apply(new_forward)
    out = model(x)
    logger.info('-------\n')


    @ModelLancet('SubLayer', 'fake_forward')
    def new_forward(self, x):
        logger.info('forwarding new_forward for sub_layer')
        return x + 1
    model.apply(new_forward)

    out = model(x)

