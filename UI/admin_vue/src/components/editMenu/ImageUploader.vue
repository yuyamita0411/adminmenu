<template>
  <div 
    class="drop-area" 
    @dragover.prevent="isDragging = true" 
    @dragleave.prevent="isDragging = false" 
    @drop.prevent="handleDrop"
    :class="{ 'dragging': isDragging }"
  >
    <p v-if="!file">画像をアップロード</p>
    <input type="file" @change="handleFileChange" ref="fileInput" style="display:none;" />
    <img v-if="file" :src="fileUrl" alt="Uploaded Image" class="uploaded-image" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ImageUploader',
  setup() {
    const file = ref<File | null>(null);
    const fileUrl = ref<string>('');
    const isDragging = ref<boolean>(false);

    const handleDrop = (event: DragEvent) => {
      const droppedFiles = event.dataTransfer?.files;
      if (droppedFiles && droppedFiles.length > 0) {
        handleFile(droppedFiles[0]);
        isDragging.value = false;
      }
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
            };
            reader.readAsDataURL(fileObj);
            file.value = fileObj; // 修正点
        }
    };

    return {
      file,
      fileUrl,
      isDragging,
      handleDrop,
      handleFileChange
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