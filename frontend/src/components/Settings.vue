<template>
      <!-- <div class="flex flex-col align-center flex-spacer textI">
        <div style="text-align: start">
          Upload your images and efficiently generate labels <br />
          using an advanced Click Interactive Segmentation Tool
        </div>

        <img class="example-img" src="../assets/Picture.gif" />
      </div> -->

      <div class="wrapper">
      <div class="flex-spacer align-center font">
        <div
          class="flex align-center justify-center"
          style="text-align: start"
        >
          <form
            id="form-form"
            method="post"
            @submit.prevent="checkForm"
            novalidate="true"
          >
            <div v-if="form.error" class="form-group mt-1">
              <div class="alert alert-danger">{{ form.error }}</div>
            </div>
            <div class="form-group mt-3" style="text-align: left">
              <label for="title">Upload your zipped images</label>
              <input
                type="file"
                class="form-control"
                id="path"
                placeholder="Enter path"
                accept="application/zip"
                @change="onFileChange"
              />
            </div>
            <div class="form-group mt-3 flex flex-row">
              <b-button type="submit" variant="primary">Get Started</b-button>
              <div v-show="loading" class="ml-3 flex-spacer">
                <b-progress
                  :max="100"
                  variant="success"
                  class="flex-spacer"
                  style="width: 100%; height: 2rem"
                  ><b-progress-bar
                    :value="uploadProgress"
                    :label="`${uploadProgress.toFixed(0)}%`"
                  ></b-progress-bar
                ></b-progress>
              </div>
            </div>
          </form>
          </div>
        </div>
      </div>
</template>

<script>
import axios from 'axios';
import * as JSZip from 'jszip';
import { backendPrefix } from '../constants';

export default {
  /* eslint-disable */
  components: {},
  data() {
    return {
      uploadProgress: 0,
      zipFile: null,
      form: {
        path: '',
        mName: '',
        aModel: null,
        error: null,
      },
      aModels: [
        { text: 'Select One', value: null },
        'YoloV3 Model',
      ],
      loading: false,
    };
  },
  methods: {
    checkForm: async function checkForm(e) {
        try {
          // send data to the server
          this.loading = true;
          // eslint-disable-next-line
          await axios.post(backendPrefix + '/api/getting-started', {
          });
          const zip = await JSZip.loadAsync(this.zipFile);
          const files = Object.keys(zip.files)
          console.log(files)
          if (files.includes('ian.png')) {
            files.push(files.splice(files.indexOf('ian.png'), 1)[0]);
          }
          console.log(files)
          // eslint-disable-next-line
          for (let i = 0; i < files.length; i++) {
            const name = files[i];
            // eslint-disable-next-line
            const data = await zip.file(name).async('base64');
            const pathParts = name.split('/');
            const formData = new FormData();
            formData.append('file', data);
            formData.append('name', pathParts[pathParts.length - 1]);
            const config = {
              headers: {
                'content-type': 'multipart/form-data',
              },
            };
            // eslint-disable-next-line
            await axios.post(backendPrefix + '/api/upload/image', formData, config);
            this.uploadProgress = (i / files.length) * 100;
          }
          // set the message
          this.loading = false;
          this.$router.push('/ic');
          return;
        } catch (error) {
          this.form.error = error;
          return;
        }
    },
    onFileChange(event) {
      const [file] = event.target.files;
      this.zipFile = file;
    },
  },
};
</script>

<style>
/* .loading {
  position: absolute;
  z-index: 6;
  top: 505px;
  left: 1100px;
} */

.wrapper {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-image {
  height: auto;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
.textI {
  font-family: Helvetica Neue;
  font-style: normal;
  font-weight: bold;
  font-size: 22px;
  color: rgba(0, 0, 0, 1);
}
.font {
  font-family: Helvetica Neue;
  font-style: normal;
  color: rgba(0, 0, 0, 1);
}

.example-img {
  max-width: 600px;
  max-height: 400px;
  width: auto;
  height: auto;
}
.action {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

form select,
form input {
  max-width: 256px;
}
</style>
