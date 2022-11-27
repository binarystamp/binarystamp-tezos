<template>
  <v-app dark>
    <v-app-bar fixed app>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-toolbar-title>
        BinaryStamp | Tezos
      </v-toolbar-title>
      <v-spacer />
      <a class="link ml-2" about="_blank" href="https://github.com/BinaryStamp">
        <v-icon large>mdi-github</v-icon>
      </a>
      <a class="link ml-2" about="_blank" href="https://twitter.com/BinaryStamp">
        <v-icon large>mdi-twitter</v-icon>
      </a>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
    }
  }
}
</script>

<style>
  .link {
    text-decoration: none;
  }
</style>
