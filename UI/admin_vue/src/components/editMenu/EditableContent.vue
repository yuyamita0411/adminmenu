<template>
  <div :class="`container ${className}`">
    <span
      v-if="!isEditing"
      @click="enableEditing"
      v-html="content"
    ></span>
    <textarea
      v-else
      :value="content"
      @input="updateContent"
      @blur="disableEditing"
    ></textarea>
  </div>
</template>

<script>
export default {
  props: {
    initialContent: String,
    className: String
  },
  data() {
    return {
      content: this.initialContent,
      isEditing: false
    };
  },
  methods: {
    enableEditing() {
      this.isEditing = true;
    },
    updateContent(e) {
      this.content = e.target.value;
      this.$emit('update', this.content);
    },
    disableEditing() {
      this.isEditing = false;
      this.$emit('editComplete', this.content);
    }
  }
};
</script>

<style lang="scss" scoped>
.content-wrapper {
    .editelem {
        width: 100%;
        float: left;
        margin: 1rem .5rem;
        position: relative;
        div {
            width: 98%;
            textarea {
                border: none;
                background: rgb(0, 0, 0, 0.05);
            }
        }
        div:not(.addcontent-wrapper) {
            margin: 0 auto;
            float: left;
            width: 100%;
            position: relative;
        }
    }
    .editelem > * {
        cursor: pointer;
    }
}
</style>