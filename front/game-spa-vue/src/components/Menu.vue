<template>
  <div id="menu-wrapper">
    <router-link class="link" :to="{ name: 'app' }">
    <div id="logo">
      <img src="../assets/logo.svg" alt="Game logo image">
    </div>
      </router-link>
    <div id="top-nav">
      <router-link class="link" :to="{ name: 'character' }">
      <button>Character</button>
      </router-link>
      <router-link class="link" :to="{ name: 'expedition'}">
        <button>Expedition</button>
      </router-link>
      <router-link class="link" :to="{ name: 'arena'}">
        <button>Arena</button>
      </router-link>
      <router-link class="link" :to="{ name: 'healer'}">
        <button>Healer</button>
      </router-link>
      <router-link class="link" :to="{ name: 'trader'}">
        <button>Trader</button>
      </router-link>
      <router-link class="link" :to="{ name: 'manage'}">
        <button>Manage</button>
      </router-link>
      <router-link class="link" :to="{ name: 'logout'}">
        <button>Logout</button>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Menu",
  data() {
      return {
      };
  },
}
</script>

<style scoped>
  #menu-wrapper {
    position: absolute;
    top: 0;
    display: block;
    width: 90%;
    margin-left: 5%;
    border: 1px solid black;
    height: 15%;
    clear: both;
  }

  #logo {
    height: 75%;
    width: 100%;
    /*border: 1px solid white;*/
  }

  #logo img {
    height: 100%;
    width: 100%;
  }

  #top-nav {
    background: #333;
    width: 100%;
    height: 25%;
    text-align: right;
  }

  #top-nav button {
    text-align: center;
    width: 12%;
    height: 100%;
    color: #ddd;
    background: inherit;
    border: none;
    font-size: 140%;
  }

  #top-nav button:hover {
    background-color: #ddd;
    color: inherit;
  }

  .link {
    color: inherit;
    outline: none;
  }

</style>
