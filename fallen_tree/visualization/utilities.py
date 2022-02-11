import subprocess
# from .setups import DEMO_PATH,EXP_FILE,MODEL_PATH,VAL_IMG_PATH

# Demo yolox path
DEMO_PATH = './visualization/YOLOX/tools/demo.py'
MODEL_PATH = "./visualization/YOLOX/weights/best_ckpt.pth"
EXP_FILE = "./visualization/YOLOX/exps/default/yolox_x.py"
# VAL_IMG_PATH = "C:/uiElementYolox/uidetectorapi/media/tmp/24.jpg"

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploads/{0}/{1}'.format(instance.id, filename)

def outputs_directory_path(instance, filename):

    return 'outputs/{0}/{1}'.format(instance.id, filename)

def callDetector(demo,exp,model,val,conf=str(0.25)):
    return subprocess.Popen(["detector.sh",demo,exp,model,val,conf], shell=True)