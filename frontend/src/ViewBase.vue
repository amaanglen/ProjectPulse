<template>
    <ListEditPopup :user=p.a v-if="popupviews.ListEdit" @viewchange="LogEditListViewChange" />
    <SummaryPopup :user=p.a v-if="popupviews.Summary" @summaryclose="SummaryViewChange" />

    <NavBar :user=p.a @viewchange="LogEditListViewChange" @summaryview="SummaryViewChange" />
    <div class="wer"><Lists :user=p.a /></div>
  
  
  </template>
  
  <script>
  import NavBar from './components/NavBar.vue'
  import Lists from './components/Lists.vue'
  import ListEditPopup from './components/ListEditPopup.vue'
  import SummaryPopup from './components/SummaryPopup.vue'
  import { useRoute } from 'vue-router'
  
  
  
  export default {
    name: 'ViewBase',
    data() {
      return {
        p: { a: 1 },
        popupviews: { ListEdit: false, Summary: false },
        EditedList: {name:"", description:""}
  
      }
    },
  
    components: {
    NavBar,
    Lists,
    ListEditPopup,
    SummaryPopup
},
    methods : {
      LogEditListViewChange(event){
        this.popupviews.ListEdit = event
  
      } ,
      SummaryViewChange(event){
        this.popupviews.Summary = event

      }
    },
    created(){
        const routea = useRoute()
        console.log(routea.params)

        this.p.a = Number(routea.params.userid)
    }
  }
  </script>
  <style>
  .wer{
    display: flex;
    
  }
  
  </style>
  
  