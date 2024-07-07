<template>
  <div>
    <div
      class="drop-area" 
      @dragover.prevent="onDragOver" 
      @dragleave.prevent="onDragLeave" 
      @drop.prevent="handleDrop($event, jsonkey)"
      :class="{ 'dragging': internalIsDragging}"
    >
        <input type="file" @change="handleFileChange" ref="fileInput" style="display:none;" />
        <div v-if="!file"><!-- ファイルがない時 -->
            <img
            v-if="isval && !loadError"
            :src="imgsrc"
            @dragover.prevent="onDragOver" 
            @dragleave.prevent="onDragLeave" 
            @drop.prevent="handleDrop($event, jsonkey)"
            @error="onImageError"
            alt="Uploaded Image" class="uploaded-image" 
            />
            <p v-if="!loadError && !isval">画像をアップロード</p>
            <p v-if="loadError && isval">画像アップロードに失敗しました {{imgsrc}}</p>
        </div>
        <div v-else><!-- ファイルがある時 -->
            <img v-if="file" :src="fileUrl" alt="Uploaded Image" class="uploaded-image" />
            <div class="w-100 d-flex">
                <label>画像に名前をつける</label>
                <input type="text" @input="setImgName($event, jsonkey)">
            </div>
        </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import {store} from '../../store/common/index';

export default defineComponent({
  name: 'ImageUploader',
  props: {
    initialImageUrl: {
      type: String,
      default: ''
    },
    jsonkey: {
      type: String,
      default: ''
    },
    imgsrc: {
      type: String,
      default: ''
    },
    imgUpdir: {
      type: String,
      default: ''
    },
    isval: {
      type: String,
      default: ''
    },
    isDragging: {
      type: Boolean,
      default: false
    }
  },
  setup(props, { emit }) {
    const file = ref<File | null>(null);
    const fileUrl = ref<string>(props.initialImageUrl);
    const internalIsDragging = ref<boolean>(props.isDragging);
    const loadError = ref<boolean>(false);

    const handleDrop = (event: DragEvent, keyname: string) => {
      const droppedFiles = event.dataTransfer?.files;
      if (droppedFiles && droppedFiles.length > 0) {
        handleFile(droppedFiles[0]);
        internalIsDragging.value = false;
        emit('updateDraggingState', false);
        console.log("ファイルアップ完了！！");
        console.log(props.jsonkey);
      }
    };

    const setImgName = (event: Event, keyname: string) => {
        const input = event.target as HTMLInputElement;
        store.commit('updateStoreObj', { target: 'jsondata', key: keyname, value: `${props.imgUpdir}${input.value}.png` });
        console.log(store.state.jsondata);
    };

    const handleFileChange = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files && input.files.length > 0) {
        handleFile(input.files[0]);
      }
    };

    const handleFile = (fileObj: File) => {
      if (fileObj && fileObj.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          fileUrl.value = e.target?.result as string;
          emit('updateImageUrl', fileUrl.value);
        };
        reader.readAsDataURL(fileObj);
        file.value = fileObj;
      }
    };

    const onDragOver = () => {
      internalIsDragging.value = true;
      emit('updateDraggingState', true);
    };

    const onDragLeave = () => {
      internalIsDragging.value = false;
      emit('updateDraggingState', false);
    };

    const onImageError = () => {
      loadError.value = true;
      internalIsDragging.value = true;
      emit('updateDraggingState', true);
    };

    watch(() => props.isDragging, (newVal) => {
      internalIsDragging.value = newVal;
    });

    return {
      file,
      fileUrl,
      internalIsDragging,
      loadError,
      handleDrop,
      setImgName,
      handleFileChange,
      onDragOver,
      onDragLeave,
      onImageError
    };
  }
});
</script>

<style scoped>
.drop-area {
    border: 2px dashed #ccc;
    padding: 20px;
    text-align: center;
    transition: border-color 0.3s;
}
.drop-area.dragging {
    border-color: #000;
}
.uploaded-image {
    max-width: 100%;
    margin-top: 20px;
}
</style>