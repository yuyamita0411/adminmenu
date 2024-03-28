<template>
  <div class="loadingcover w-100 pr-0 pl-0 pl-lg-1 float-lg-left d-inline-block text-center h-100">
    <div class="sk-chase">
      <div class="sk-chase-dot" v-for="dot in 6" :key="dot"></div>
    </div>
    <h4 id="LoadingStr" class="loading text-center d-inline-block w-100 mt-3">
      <span v-for="(letter, index) in letters" :key="index" :class="llClasses[index].value">{{ letter }}</span>
    </h4>
    <h5 class="loadingwait w-100 d-inline-block text-center">
      <span v-for="wait in 3" :key="wait" :class="`d-inline-block text-center ${loadingWaits[wait - 1].value}`">●</span>
    </h5>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';

export default defineComponent({
  name: 'LoadingIconview',
  setup() {
    const letters = ['L', 'o', 'a', 'd', 'i', 'n', 'g'];
    const llClasses = ref(letters.map(() => ref('op02 llhide')));
    const loadingWaits = ref([ref('op0'), ref('op0'), ref('op0')]);

    onMounted(() => {
      let count = 0;
      let waitincount = 0;

      setInterval(() => {
        waitincount += 1;
        const waitingwhichphase = waitincount % 3;

        for (let i = 0; i < loadingWaits.value.length; i++) {
          loadingWaits.value[i].value = i === waitingwhichphase ? 'color-blue' : 'color-white';
        }
      }, 600);

      setInterval(() => {
        count += 1;
        const whichphase = count % 7;
        
        for (let i = 0; i < llClasses.value.length; i++) {
          if(i === whichphase) {
            llClasses.value[i].value = "op1 llshow";
          } else if (i === (whichphase + 6) % 7) {
            llClasses.value[i].value = "op04 llhide";
          } else {
            llClasses.value[i].value = "op02 llhide";
          }
        }
      }, 150);
    });

    return {
      letters,
      llClasses,
      loadingWaits
    };
  }
});
</script>

<style lang="scss" scoped>
#LoadingStr{
    top: calc(50vh + 7rem);
    left: calc(50% - 4rem);
    color: #ffb75a;
    z-index: 1111;
    position: absolute;
}
.loadingwait{
    top: calc(50vh + 8rem);
    left: calc(50% - 3rem);
    letter-spacing: 1rem;
    position: absolute;
}
.loadingwait{
    letter-spacing:1rem;
}
.llhide{
    letter-spacing:2px;
    top: .5rem;
    transform:scale(0.8);
}
.llshow{
    letter-spacing:5px;
    top: 0;
    transform:scale(1.2);
}
.llhide,
.llshow,

.op0{
    opacity: 0;
}
.op02{
    opacity: 0.6;
}
.op04{
    opacity: .8;
}
.op1{
    opacity: 1;
}
.op0,
.op02,
.op04,
.op1{
    transition:all .3s;
}
.color-white,
.color-blue {
    transition:all .2s;
}
#LoadingStr span {
    font-size:2rem;
    position: relative;
}
.loadingwait span {
    font-size:2rem;
}
.color-white {
    color: #ffff;
}
.color-blue {
    color:#0069d9;
}
/* ローディング関連 */
.sk-chase {
    top:50vh;
    left:calc(50% - 35px);;
    width: 70px;
    height: 70px;
    position: relative;
    animation: sk-chase 2.5s infinite linear both;
}

.sk-chase-dot {
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0; 
    animation: sk-chase-dot 2.0s infinite ease-in-out both; 
}

.sk-chase-dot:before {
    content: '';
    display: block;
    width: 25%;
    height: 25%;
    background-color: #0069d9;
    border-radius: 100%;
    animation: sk-chase-dot-before 2.0s infinite ease-in-out both; 
}

.sk-chase-dot:nth-child(1) { animation-delay: -1.1s; }
.sk-chase-dot:nth-child(2) { animation-delay: -1.0s; }
.sk-chase-dot:nth-child(3) { animation-delay: -0.9s; }
.sk-chase-dot:nth-child(4) { animation-delay: -0.8s; }
.sk-chase-dot:nth-child(5) { animation-delay: -0.7s; }
.sk-chase-dot:nth-child(6) { animation-delay: -0.6s; }
.sk-chase-dot:nth-child(1):before { animation-delay: -1.1s; }
.sk-chase-dot:nth-child(2):before { animation-delay: -1.0s; }
.sk-chase-dot:nth-child(3):before { animation-delay: -0.9s; }
.sk-chase-dot:nth-child(4):before { animation-delay: -0.8s; }
.sk-chase-dot:nth-child(5):before { animation-delay: -0.7s; }
.sk-chase-dot:nth-child(6):before { animation-delay: -0.6s; }

.loadingcover{
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    background: rgb(0, 0, 0, 0.5);
    z-index: 1;
}
@keyframes sk-chase {
    100% { transform: rotate(360deg); } 
}

@keyframes sk-chase-dot {
    80%, 100% { transform: rotate(360deg); } 
}

@keyframes sk-chase-dot-before {
    50% {
    transform: scale(0.4); 
    } 100%, 0% {
    transform: scale(1.0); 
    } 
}
/* ローディング関連 */
</style>