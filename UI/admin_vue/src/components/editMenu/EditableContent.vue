<template>
  <div :class="`container `">
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'EditableContent',
  props: {
    sendkey: String,
    sendvalue: String
  }
});
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
h2,
.for-h2 {
    font-size: 1.5rem;
    margin: 0 0 .5rem 0;
}

h3,
.for-h3,
.for-box-h3 {
    font-size: 1.17rem;
    margin: 0 0 .5rem 0;
}

h4,
.for-h4 {
    font-size: 1.05rem;
    margin: 0 0 .5rem 0;
}

p,
.for-p,
.for-box-description {
    font-size: 1rem;
    margin: 0 0 .5rem 0;
}

.p-for-h2 {
    padding-left: 1rem;
}
.div-for-h3 {
    padding-left: 1rem;
}
.p-for-h3 {
    padding-left: 2rem;
}
.div-for-h4 {
    padding-left: 2rem;
}
.p-for-h4 {
    padding-left: 3rem;
}
.div-for-h5 {
    padding-left: 3rem;
}
.p-for-h5 {
    padding-left: 4rem;
}
.div-for-h6 {
    padding-left: 4rem;
}
.p-for-h6 {
    padding-left: 5rem;
}
</style>