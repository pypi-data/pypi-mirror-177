from functools import partial
import logging
import torch

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('torch_model_lancet')






def _attribute2buffer(instance: torch.nn.Module, name: str):
    try:
        attribute = instance.__getattribute__(name)
        instance.__delattr__(name)
        instance.register_buffer(name, attribute)
        del attribute

        logger.info(f'repaced {instance.__class__.__name__}\'s attribute {name} with a buffer')
    except:
        pass

def attribute2buffer(model: torch.nn.Module, name: str):
    _attribute2buffer_partial = partial(_attribute2buffer, name=name) 
    model.apply(_attribute2buffer_partial)



if __name__ == '__main__':
    
    import torch

    class Model(torch.nn.Module):
        def __init__(self,):
            super().__init__()
            self.pe = torch.ones(3,4)
            self.sub = SubModel()
    
    
    class SubModel(torch.nn.Module):
        def __init__(self,):
            super().__init__()
            self.pe = torch.ones(3,4)

    model = Model()
    model.half()
    print(model.pe, model.sub.pe)
    model.float()
    print('before transfrom')
    attribute2buffer(model, 'pe')
    print('after transfrom')
    model.half()
    print(model.pe, model.sub.pe)