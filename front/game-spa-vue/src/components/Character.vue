<template>
  <div>
  <Menu />
  <h1> CHAR </h1>
    <img src="https://lh4.googleusercontent.com/-hXBtR3F--CM/AAAAAAAAAAI/AAAAAAAAAjk/W6Ylpqj5y50/photo.jpg?sz=128" width="500">
  </div>
</template>

<script>
  export default {
      name: 'character',


  created(){
      console.log(this.$test)
      let character = this.getCharacter();
  },
  methods: {
      getCharacter() {
          return this.$call.get('/character');
      }
  }
}
</script>

<style scoped>

</style>
