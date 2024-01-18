from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin, CORS
import os
from PIL import Image as Im
from pathlib import Path
import base64
from controller import InteractiveController
import cv2
import numpy as np
import shutil
import uuid
from isegm.utils import exp
from isegm.inference import utils
# classifier
import os
import urllib
from argparse import Namespace
import torch
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
from src_files.semantic.semantics import ImageNet21kSemanticSoftmax
import timm

""" TODO: app, services, models and routes should be sperated """

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)

DIR_IMAGES = os.path.join('app', 'static', 'images')
DIR_IMAGES_WITH_MASKS = os.path.join('app', 'static', 'images_with_masks')
DIR_MASKS = os.path.join('app', 'static', 'masks')
INTERACTIVE_MODELS_PATH = "./weights"
CHECKPOINT_NAME = "hrnet18_cocolvis_itermask_3p"
DEVICE = 'cpu'
SCREEN = (640, 480)
ALPHA_BLEND = 0.5
CLICK_RADIUS = 3


# create interactive click model checkpoint
checkpoint_path = utils.find_checkpoint(INTERACTIVE_MODELS_PATH, CHECKPOINT_NAME)
model = utils.load_is_model(checkpoint_path, DEVICE, cpu_dist_maps=True)
controller = InteractiveController(model, DEVICE, predictor_params={'brs_mode': 'NoBRS'})

# download classifier weights and init
print("downloading weights...")
url, filename = (
    "https://miil-public-eu.oss-eu-central-1.aliyuncs.com/model-zoo/ImageNet_21K_P/resources/fall11/imagenet21k_miil_tree.pth",
    "./weights/imagenet21k_miil_tree.pth")
if not os.path.isfile(filename):
    urllib.request.urlretrieve(url, filename)
args = Namespace()
args.tree_path = filename
semantic_softmax_processor = ImageNet21kSemanticSoftmax(args)
print("done")
print("initilizing model...")
model = timm.create_model('vit_base_patch16_224_miil_in21k', pretrained=True)
model.eval()
config = resolve_data_config({}, model=model)
transform = create_transform(**config)
print("done")





### Image Table and Schema ###
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), unique=True)

    def __init__(self,path):
        # Add the data to the instance
        self.path = path

### Image_Mask Table and Schema ###
class Image_Mask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), unique=True)

    def __init__(self,path):
        # Add the data to the instance
        self.path = path

class Mask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), unique=True)
    label = db.Column(db.String(500), unique=True)

    def __init__(self,path,label):
        # Add the data to the instance
        self.path = path
        self.label = label

def rmdir(directory):
    directory = Path(directory)
    if not directory.exists():
        return
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

@app.route('/api/getting-started', methods=['POST'])
@cross_origin(origin='*', headers=['content-type'])
def add_path():

    db.drop_all()
    db.create_all()

    # delete images in images directory
    rmdir(DIR_IMAGES)
    os.makedirs(DIR_IMAGES)

    rmdir(DIR_IMAGES_WITH_MASKS)
    os.makedirs(DIR_IMAGES_WITH_MASKS)

    rmdir(DIR_MASKS)
    os.makedirs(DIR_MASKS)

    return jsonify({})

# Route for uploading images to backend
@app.route('/api/upload/image', methods=['POST'])
@cross_origin(origin='*', headers=['content-type'])
def upload_image():
    if not 'file' in request.form:
        raise Exception('no file found')

    file = request.form['file']
    name = request.form['name']
    filepath = os.path.join(DIR_IMAGES, name)
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(file))

    with Im.open(filepath) as image:
        db.session.add(Image(filepath))
        db.session.commit()
        try:
            # Transform images to match size (not necess. will be applied)
            new_image = image.resize(SCREEN)
            new_image.save(filepath)
            print("new image resized")
        except:
            pass

    return jsonify({'success': True})

# Route for image labels
@app.route('/api/image/labels/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['content-type'])
def load_labels(id):

    image = Image.query.get(id)
    image_path = image.path
    img = Im.open(image_path).convert('RGB')
    tensor = transform(img).unsqueeze(0)  # transform and add batch dimension
    print("doing semantic inference...")   
    labels = []
    with torch.no_grad():
        logits = model(tensor)
        semantic_logit_list = semantic_softmax_processor.split_logits_to_semantic_logits(logits)

        # scanning hirarchy_level_list
        for i in range(len(semantic_logit_list)):
            logits_i = semantic_logit_list[i]

            # generate probs
            probabilities = torch.nn.functional.softmax(logits_i[0], dim=0)
            top1_prob, top1_id = torch.topk(probabilities, 1)

            if top1_prob > 0.5:
                top_class_number = semantic_softmax_processor.hierarchy_indices_list[i][top1_id[0]]
                top_class_name = semantic_softmax_processor.tree['class_list'][top_class_number]
                top_class_description = semantic_softmax_processor.tree['class_description'][top_class_name]
                labels.append(top_class_description)
        
    labels = labels[:3]

    print("labels found {}.".format(labels))

    return jsonify(labels)

@app.route('/api/ids', methods=['GET'])
@cross_origin(origin='*', headers=['content-type'])
def getIDs():
    all_images = Image.query.all()
    id_counter = len(all_images)
    return jsonify(id_counter)


@app.route('/api/images', methods=['GET'])
@cross_origin(origin='*', headers=['content-type'])
def get_images():
    all_images = Image.query.all()
    return jsonify(list(map(lambda v: v.id, all_images)))

@app.route('/api/image/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def send_image(id):
    image = Image.query.get(id)
    image_path = image.path
    return send_file(image_path.replace('app/', ''))


@app.route('/api/image/mask/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def send_image_mask(id):
    image = Image_Mask.query.get(id)
    image_path = image.path
    return send_file(image_path.replace('app/', ''))



@app.route('/api/image/set/<id>/', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def set_image(id):
    
    image = Image.query.get(id)
    image_path = image.path
    cv2_image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    
    controller.set_image(cv2_image)
    #unique_id = str(uuid.uuid4())
    filepath = DIR_IMAGES_WITH_MASKS + "/img" + id + ".png"
    print(filepath)
    if db.session.query(Image_Mask).filter_by(path=filepath).count() == 0:
        db.session.add(Image_Mask(filepath))
        db.session.commit()
        print("image mask added to db")

    return jsonify({'success': True})


num_clicks = 0

@app.route('/api/image/<id>/click', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def mask_image_with_click(id):
    global num_clicks
    print(id)
    # get click body
    print(request.json)
    click = request.json
    num_clicks += 1
    # add click to controller
    controller.add_click(click["x"], click["y"], click["positive"])
    filepath = DIR_IMAGES_WITH_MASKS + "/img" + id + ".png"
    print(filepath)
    vis = controller.get_visualization(ALPHA_BLEND, click["clickRadius"])
    
    image_with_mask = Im.fromarray(vis)
    image_with_mask.save(filepath)


    return jsonify({'success': True})

@app.route('/api/mask/label/<id>/save/', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def save_mask(id):
    global num_clicks

    if not request.json:
        return jsonify({'success': False, 'message': 'No label set'})

    label = request.json["label"]

    filepath = DIR_MASKS + "/" + label + id + "num_clicks" + str(num_clicks) + ".png"
    num_clicks = 0
    
    if db.session.query(Mask).filter_by(path=filepath).count() == 0:
        db.session.add(Mask(filepath, label))
        #db.session.add(Mask(label))

        db.session.commit()
    
    # if label is in db overwrite it
    if db.session.query(Mask).filter_by(label=label).count() > 0:
        mask = Mask.query.filter_by(label=label).first()
        mask.label = label
        db.session.commit()


    mask = controller.result_mask
    if mask.max() > 0:
        if mask.max() < 256:
            mask = mask.astype(np.uint8)
            mask *= 255
    else:
         return jsonify({'success': False, 'message': 'No mask found'})

    mask = Im.fromarray(mask)
    mask.save(filepath)

    return jsonify({'success': True})

@app.route('/api/mask/click/undo/<id>/', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def undo_click(id):
    global num_clicks
    if num_clicks > 0:
        num_clicks -= 1
    image = Image_Mask.query.get(id)
    image_path = image.path
    controller.undo_click()
    vis = controller.get_visualization(ALPHA_BLEND, CLICK_RADIUS)
    image_with_mask = Im.fromarray(vis)
    image_with_mask.save(image_path)
    return send_file(image_path.replace('app/', ''))

@app.route('/api/mask/clicks/reset/<id>/', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def reset_clicks(id):
    global num_clicks
    num_clicks = 0
    image = Image_Mask.query.get(id)
    image_path = image.path
    controller.reset_last_object()
    vis = controller.get_visualization(ALPHA_BLEND, CLICK_RADIUS)
    image_with_mask = Im.fromarray(vis)
    image_with_mask.save(image_path)
    return send_file(image_path.replace('app/', ''))

@app.route('/api/export.zip', methods=['GET'])
@cross_origin(origin='*', headers=['content-type'])
def export_data():
    random_name = str(uuid.uuid4())
    temp_path = os.path.join('app', 'temp', random_name)

    shutil.make_archive('masks-' + random_name, 'zip', DIR_MASKS)

    return send_file(os.path.join('masks-' + random_name + '.zip'))



if __name__ == '__main__':
    # run app in debug mode on port 5000
    print("server ready")
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
