import { defineStore } from 'pinia';
import axios from 'axios';
import { backendPrefix } from '../constants';

export default defineStore('editor', {
  state: () => ({
    // Variables set in PreviousNext and used in ... Components
    objects: [],

    // Variables set in ToolSelection and used in ... Components
    isActiveBB: true,
    isActiveWand: false,
    isActiveRec: false,

    // Variables set in ImageEditor and used in (ToolSelection) Components
    editor: null,

    // Variables set in Labelling and used in ()
    buttonLabels: [],
    activeObj: null,

    // Variables set in Progressbar used in ()
    IDs: 0,
    i: 1,

    // Variables for Previous and Next used in ()
    imagePath: '',
    assistiveObjects: [],
    oneshotObjects: [],
    cocoCategories: [],
    labels: [],
    labelCount: {},
    saveMaskError: '',
    clickRadius: 3,
    imgLabels: [],
    appliedLabel: [],
  }),
  actions: {
    getObjects() {
      this.objects = this.editor.canvas.getObjects();
    },
    // Methods for ToolSelection component
    setBB(value) {
      this.isActiveBB = value;
    },
    setWand(value) {
      this.isActiveWand = value;
    },
    setRec(value) {
      this.isActiveRec = value;
    },

    // Methods for ImageEditor component
    setEditor(value) {
      this.editor = value;
    },

    // Methods for Labelling component
    resetButtonAll(value) {
      // eslint-disable-next-line
      for (var i = 0; i < this.buttonLabels.length; i++) {
        this.buttonLabels[i].state = value;
      }
    },
    resetAllButtonDeselect() {
      if (this.activeObj === null) {
        // eslint-disable-next-line
        for (var i = 0; i < this.buttonLabels.length; i++) {
          // eslint-disable-next-line
          this.buttonLabels[i].state = false;
        }
      }
      if (this.activeObj) {
        // eslint-disable-next-line
        for (var i = 0; i < this.buttonLabels.length; i++) {
          // eslint-disable-next-line
          if (this.activeObj.id === this.buttonLabels[i].caption) {
            // eslint-disable-next-line
            this.buttonLabels[i].state = true;
          } else {
            // eslint-disable-next-line
            this.buttonLabels[i].state = false;
          }
        }
      }
    },
    setActive(value) {
      this.activeObj = value;
    },

    // Methods for Progressbar component
    async getID() {
      try {
        // eslint-disable-next-line
        const response = await axios.get(backendPrefix + '/api/ids');
        this.IDs = response.data;
      } catch (error) {
        console.log(error);
      }
    },

    // Methods for Delete Bounding Box component
    activeOb() {
      this.activeObj = this.editor.canvas.getActiveObject();
      if (typeof this.activeObj !== 'undefined' && this.activeObj !== null) {
        if (this.activeObj.width === 0) {
          this.activeObj = null;
        }
      }
    },
    removeActive() {
      this.editor.canvas.remove(this.editor.canvas.getActiveObject());
    },

    // Methods for PreviousNext component
    // Method for getting bb computed by assistive model
    async getAssistiveBoxes() {
      try {
        const response = await axios.get(
          // eslint-disable-next-line
          backendPrefix + `/api/assistiveobjectsdetections/${this.i}`,
        );
        this.assistiveObjects = response.data;
      } catch (error) {
        this.error = error;
      }
    },
    // Method for getting bb computed by assistive model
    async getOneshotBoxes() {
      try {
        const response = await axios.get(
          // eslint-disable-next-line
          backendPrefix + `/api/oneshotobjectsdetections/${this.i}`,
        );
        this.oneshotObjects = response.data;
      } catch (error) {
        console.log(error);
      }
    },
    // Uses the method uploadBox() to maintain the created Bounding Boxes
    async uploadBoxes() {
      this.objects = this.editor.canvas.getObjects();
      // eslint-disable-next-line
      await axios.post(backendPrefix + `/api/remove-box/${this.i}`);
      // eslint-disable-next-line
      if (this.objects.length > 0) {
        // eslint-disable-next-line
        for (var i = 0; i < this.objects.length; i++) {
          // eslint-disable-next-line
          await this.uploadBox(this.objects[i]);
        }
      }
      this.editor.clear();
    },
    // Method for uploading each bounding box to the backend
    async uploadBox(object) {
      // send data to the server
      // eslint-disable-next-line
      await axios.post(backendPrefix + `/api/add-box/${this.i}`, {
        image_id: this.i,
        id: object.id,
        top: object.top,
        left: object.left,
        width: object.width * object.scaleX,
        height: object.height * object.scaleY,
      });
    },
    // Method for setting setting image background of Canvas associated with image i
    async uploadImg() {
      this.imagePath = `${backendPrefix}/api/image/${this.i}`;
      this.editor.setBackgroundImage(this.imagePath);
      // await this.loadImgLabels();
      // eslint-disable-next-line
      /* for (const key in this.labelCount) {
        const count = this.labelCount[key];
        const label = this.labels.find((it) => it.label === key);
        if (count === 200 && String(label.status_training) === 'not started') {
          // eslint-disable-next-line
          axios.get(backendPrefix + `/api/start-label-training/${key}`).then((response) => {
            if (response.data.success) {
              this.loadLabels();
            }
          });
        }
      } */
    },
    async loadImgLabels() {
      try {
        const response = await axios.get(
          // eslint-disable-next-line
          backendPrefix + `/api/image/labels/${this.i}`,
        );
        this.imgLabels = response.data;
        console.log(this.imgLabels);
      } catch (error) {
        console.log(error);
      }
    },
    async uploadImgWithMask() {
      this.imagePath = `${backendPrefix}/api/image/mask/${this.i}`;
      this.editor.setBackgroundImage(this.imagePath);
    },
    async clickImg(click) {
      await axios.post(`${backendPrefix}/api/image/${this.i}/click`, {
        image_id: this.i,
        x: click.x,
        y: click.y,
        positive: Boolean(click.positive),
        clickRadius: Number(this.clickRadius),
      });
      console.log(click);
      this.imagePath = `${backendPrefix}/api/image/mask/${this.i}`;
      console.log(this.imagePath);
      this.editor.setBackgroundImage(this.imagePath);
    },
    async setImage() {
      await axios.get(`${backendPrefix}/api/image/set/${this.i}`);
    },
    async saveMaskWithLabel(label) {
      console.log(label);
      try {
        await axios.post(`${backendPrefix}/api/mask/label/${this.i}/save/`, {
          label: label.label,
        });
      } catch (error) {
        this.saveMaskError = error;
      }
    },
    async undoClick() {
      this.imagePath = `${backendPrefix}/api/mask/click/undo/${this.i}`;
      console.log(this.imagePath);
      this.editor.setBackgroundImage(this.imagePath);
    },
    async resetClicks() {
      this.imagePath = `${backendPrefix}/api/mask/clicks/reset/${this.i}`;
      console.log(this.imagePath);
      this.editor.setBackgroundImage(this.imagePath);
    },
    // Method for getting all bounding boxes for image i
    async getBoxes() {
      try {
        // eslint-disable-next-line
        const response = await axios.get(backendPrefix + `/api/get-box/${this.i}`);
        this.objects = response.data;
        this.drawBoxes(this.objects);
      } catch (error) {
        console.log(error);
      }
    },
    // Method for drawing bounding boxes for assistive models and others
    drawBoxes(object) {
      // eslint-disable-next-line
      for (var i = 0; i < object.length; i++) {
        const paramsRect = {
          top: parseInt(this.objects[i].top, 10),
          left: parseInt(this.objects[i].left, 10),
          width: parseInt(this.objects[i].width, 10),
          height: parseInt(this.objects[i].height, 10),
          strokeWidth: 3,
          stroke: 'green',
          fill: 'rgba(144, 238, 144, 0.2)',
          opacity: 1,
          noScaleCache: false,
          selectionBackgroundColor: 'rgba(144, 238, 144, 0.4)',
          id: object[i].id,
        };
        this.editor.drawRect(paramsRect);
      }
    },
    async loadCocoCategories() {
      // eslint-disable-next-line
      const response = await axios.get(backendPrefix + '/api/assistiveobjects');
      this.cocoCategories = response.data;
    },
    async loadLabels() {
      // eslint-disable-next-line
      let response = await axios.get(backendPrefix + '/api/labels');
      this.labels = response.data;
      // eslint-disable-next-line
      for (let i = 0; i < this.labels.length; i++) {
        const label = this.labels[i];
        if (label.status_training === 'started' && !localStorage[`labelStart-${label.label}`]) {
          localStorage[`labelStart-${label.label}`] = new Date();
        } else {
          label.startTime = localStorage[`labelStart-${label.label}`];
        }
      }
      this.buttonLabels = response.data.map((it) => ({
        caption: it.label,
        state: false,
      }));
      // eslint-disable-next-line
      response = await axios.get(backendPrefix + '/api/label-count');
      this.labelCount = response.data;
    },
  },
});
