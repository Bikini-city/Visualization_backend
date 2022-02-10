from .models import Detections
from .setups import EXP_FILE,MODEL_PATH
from .YOLOX.tools.demo import main,make_parser,get_exp
from .codewriter import json_reader


def detect(src, *args):
    # Perform Transaction
    confidence = float(src.data['confidence'])
    image_to_detect = src.data['image_to_detect']

    detections = Detections.objects.create(image_to_detect=image_to_detect,confidence=confidence)
    VAL_IMG_PATH = f'media/{detections.image_to_detect}'

    # YOLOX PARAMETERS
    conf = confidence
    args = make_parser().parse_args()
    args.demo = "image"
    args.exp_file = EXP_FILE
    args.ckpt = MODEL_PATH
    args.path = VAL_IMG_PATH
    args.conf = conf
    args.nms = 0.45
    args.tsize = 640
    args.save_result = True
    exp = get_exp(args.exp_file, args.name)

    # YOLOX DETECTOR
    jfile = main(exp,args)
    # img,jfile = path_converter(img),path_converter(jfile)

    # PYQT CODE GENERATOR
    data = json_reader(jfile)
    
    down = data["down"]
    broken = data["broken"]
    return down, broken