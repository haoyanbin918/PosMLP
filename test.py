import torch
from thop import profile
import warnings
import models
# from timm import models 


import argparse
parser = argparse.ArgumentParser(description='ViP Training and Evaluating')
parser.add_argument('-t', '--type', default='', type=str,
                    help='check which type to summary model')
args = parser.parse_args()

models.list_models()
warnings.filterwarnings('ignore')
# input=torch.randn([1,3,224,224])
kwargs={'depth_conv': True,
        'gamma': 8,
        'pos_emb': True,
        'stem_name' :'PatchEmbed',# 'PatchEmbed' ,#'Nest_ConvolutionalEmbed',#'Nest_ConvolutionalEmbed'
        'blockwise': False,
        'blocksplit': False,
        'depth_conv' : True,
        'quadratic' : True,
        'channel_split': 24,
        'pos_only': True
  }
model = models.gmlp_s16_224()


if args.type == 'ptflops':
    from ptflops import get_model_complexity_info
    with torch.cuda.device(0):
        macs, params = get_model_complexity_info(model, (3, 224, 224), as_strings=True,
                                                print_per_layer_stat=True, verbose=True)
        print('{:<30}  {:<8}'.format('Computational complexity: ', macs))
        print('{:<30}  {:<8}'.format('Number of parameters: ', params))

elif args.type == 'torchsummary':
    from torchsummary import summary
    summary(model.cuda(),(3,224,224))


elif args.type == 'thop' :
    input=torch.randn([1,3,224,224])
    for name,parameters in model.named_parameters():
        print(name,':',parameters.size())
    
    flop,para = profile(model,inputs=(input,))
    print('with input size {}, model has para numbers {} and flops {} '.format(input.size(),para,flop))

else:
    import torch
    # from torchvision.models import resnet50
    from fvcore.nn import FlopCountAnalysis, parameter_count_table

    # 创建resnet50网络
    # 创建输入网络的tensor
    tensor = (torch.rand(1, 3, 224, 224),)
    for name,parameters in model.named_parameters():
        print(name,':',parameters.size())
    # 分析FLOPs
    flops = FlopCountAnalysis(model, tensor)
    print("FLOPs: ", flops.total())

    # 分析parameters
    print(parameter_count_table(model))
