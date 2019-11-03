<template>
  <div id="app">
    <header>
      <Menu/>
    </header>
    <div id="content">
      <Character/>
    </div>
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
import Character from './components/Character.vue'

export default {
  name: 'app',
  components: {
    Menu,
    Character,
  },
  data () {
    return {
        data: null,
        endpoint: 'http://127.0.0.1:5000/character/1',
        active_btn: 'char',
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

<style>
  body {
    background-color: #3A7765;
  }

  #app {
    clear: both;
  }

  header {
    display: block;
  }

  main {
    display: block;
    position: absolute;
    top: 15%;
    border: 1px solid black;

  }


</style>
