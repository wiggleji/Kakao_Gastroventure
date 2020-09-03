<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" style="width: 100px; height: 100px">

    <div>
      <form v-on:submit="retrieveRstList">
        <b-input-group>
          <b-form-input type="text" v-model="keyword"></b-form-input>

          <b-input-group-append>
            <b-button variant="light" id="reset" @click="keyword=''">
              <b-icon icon="x"/>
            </b-button>
            <b-button variant="outline-primary" v-on:click="retrieveRstList" type="submit">검색</b-button>
          </b-input-group-append>
        </b-input-group>
      </form>
    </div>

    <Graph/>
    <template v-for="rst in rstList">
      <RestaurantBrief :id="rstList.indexOf(rst)" :key="rst.id" :rst="rst" v-on:click="console.log(this)"></RestaurantBrief>
    </template>
    <b-modal id="restaurant" title="BootstrapVue">
      <p class="my-4">Hello from modal!</p>
    </b-modal>
  </div>
</template>

<script>
  import Graph from './components/Graph.vue'
  import RestaurantBrief from "./components/RestaurantBrief";

  export default {
    name: 'App',
    data() {
      return {
        keyword: '',
        rstList: '',
        rst_id: '',
        curRst: null,
      }
    },
    methods: {
      async retrieveRstList(e) {
        e.preventDefault()

        const res = await this.axios.get('http://localhost:8000/api/v1/restaurant/', {
          params: {
            name: this.keyword
          }
        })
        console.log(res)
        this.rstList = res.data
      },
      updateCurrentRst(e) {
        // e.preventDefault()
        console.log(e.target.id)
      }
    },
    components: {
      RestaurantBrief,
      Graph
    }
  }
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  #reset {
    background-color: white;
    border-bottom-color: #CFD4D9;
    border-top-color: #CFD4D9;
    border-left-color: white;
  }
</style>
