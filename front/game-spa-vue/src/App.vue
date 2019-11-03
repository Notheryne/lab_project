<template>
  <div id="app">
    <header>
      <Menu />
    </header>
<!--    <div id="content">-->
<!--    <main>-->
<!--      <div class="content">-->
<!--        <div class="char_preview" v-bind="data">-->
<!--          <h3> {{ data['char_name'] }} </h3>-->
<!--          <img :src="data['image_path']" alt="character in game image">-->
<!--        </div>-->
<!--        </div>-->
<!--    </main>-->
<!--    </div>-->
  </div>
</template>

<script>
import axios from 'axios'
import Menu from './components/Menu.vue'

export default {
  name: 'app',
  components: {
    Menu,
  },
  data () {
    return {
        data: null,
        endpoint: 'http://127.0.0.1:5000/character/1',
    }
  },
  created() {
      this.getCharacter();
  },
  methods: {
      getCharacter() {
          axios.get(this.endpoint)
              .then(response => {
                  this.data = response.data;
              })
              .catch(error => {
                  console.log(error);
              })
      }
  }
}
</script>

<style scoped>
  #app {
    position: fixed;
    top: 0;
    left: 0;
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background-color: #A5D6D9;
  }

  /*header {*/
  /*  float: top;*/
  /*  overflow: hidden;*/
  /*}*/

  /*#content {*/
  /*  clear: both;*/
  /*  width: 90%;*/
  /*  margin: 5% auto;*/
  /*  border: 1px solid black;*/
  /*}*/
</style>
