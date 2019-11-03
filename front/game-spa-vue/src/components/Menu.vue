<template>
  <div id="menu-wrapper">
    <div id="topbar">
      <div id="logo">
        <img src="../assets/logo.svg" id="logo-img" alt="Game logo on the top">
      </div>
      <div id="nav-bar">
        <button type="button">Character</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {

}

</script>

<style scoped>
  #logo {
    position: fixed;
    margin-left: 5%;
    width: 90%;
    height: 15%;
    border: 1px solid black;
    display: block;
  }

  #logo img {
    float: top;
    width: 100%;
    height: 80%;
    object-fit: contain;
    border: 1px solid red;
  }

  #nav-bar {
    width: 90%;
    height: 20%;
    margin-left: 5%;
    border: 1px solid green;

  }

</style>
