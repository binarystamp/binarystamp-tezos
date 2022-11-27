<template>
  <v-app dark>
    <v-app-bar fixed app>
      <v-spacer />
      <v-spacer />
      <v-img max-height="80"  max-width="80" style="margin-top: 10px" src="/mstile-150x150.png" class="float-sm-left" />
      <v-toolbar-title>
        <div class="float-sm-left"> BinaryStamp | Tezos</div>
      </v-toolbar-title>
      <v-spacer />
      <a class="link ml-2" about="_blank" href="https://github.com/BinaryStamp">
        <v-icon large>mdi-github</v-icon>
      </a>
      <a class="link ml-2" about="_blank" href="https://twitter.com/BinaryStamp">
        <v-icon large>mdi-twitter</v-icon>
      </a>
      <v-spacer />
      <v-spacer />
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
   a {
     text-decoration: none;
   }
  .link {
    text-decoration: none;
  }
</style>
