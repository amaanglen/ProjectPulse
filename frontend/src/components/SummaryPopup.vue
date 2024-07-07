<template>
  <div class="popup">
    <div class="popup-inner">
      <h2>Summary </h2>
      <div>
        <canvas id="myBarChart" width="400" height=" 400"></canvas>
        <canvas id="mypieChart" width="100" height="100"></canvas>
        <h3 style="margin-top=20px;">Time analysis for completed cards,</h3>
        <div v-for="names in b" :key="names">
          <h5 style="margin-bottom:10px;">{{ lname }}</h5>
          <table border="2">
            <tr>
              <th style="padding: 5px;">Card Name</th>
              <th style="padding: 5px;">Completion Date Time</th>
              <th style="padding: 5px;">Time Taken</th>
            </tr>
            <tr v-for="bames in names" :key="bames">
              <td style="padding: 5px;">{{ bames[1] }}</td>
              <td style="padding: 5px;">{{ bames[2] }}</td>
              <td style="padding: 5px;">{{ bames[3] }}</td>
              <br>
              <h5>{{firstele(bames[0])}}</h5>
            </tr>
          </table>
        </div>
      </div>
      <slot />
      <button class="btn btn-secondary" @click="summclose">Close</button>
    </div>
  </div>
</template>
  
<script>
import Chart from 'chart.js/auto'



export default {
  name: 'SummaryPopup',
  props: { user: Number },
  data() {
    return {
      a: [],
      b: [],
      listnames: [],
      noofcomplete: [],
      noofincomplete: [],
      tes: { 1: 33 },
      timegraphview: true,
      lname: "loading"


    }


  },


  methods: {
    summclose(event) {
      this.$emit("summaryclose", false)


    },
    firstele(ele){
      this.lname=ele
      return("")
    }
  },

  async created() {


  },


  async mounted() {
    await fetch("http://127.0.0.1:5000/summary/" + this.user,
      {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        }
      }).then((response) => response.json()).then(data => this.a = data).catch((error) => { console.log(error) })


    console.log(this.b)



    console.log(this.a)
    console.log(this.listnames)
    let m = this.a.length


    this.listnames = []
    for (let i = 0; i < this.a.length; i++) {
      this.listnames.push(this.a[i]["lname"])
      this.noofcomplete = this.noofcomplete + (Number(this.a[i]["completed"]))
      this.noofincomplete = this.noofincomplete + (Number(this.a[i]["incomplete"]))
    }

    console.log(this.a)
    console.log(this.listnames)
    console.log(this.noofcomplete)

    const ctx = document.getElementById('myBarChart');
    new Chart(ctx, {

      data: {

        labels: this.listnames,
        datasets: [{
          type: 'line',
          label: 'Complete Tasks',
          data: this.noofcomplete,
          borderWidth: 1
        },
        {
          type: 'line',
          label: 'Incomplete Tasks',
          data: this.noofincomplete,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })

    await fetch("http://127.0.0.1:5000/compdate/" + this.user,
      {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        }
      }).then((response) => response.json()).then(data => this.b = data).catch((error) => { console.log(error) })
    console.log(this.b)


    let totalcom = 0
    let totalincom = 0
    for (let i = 0; i < this.a.length; i++) {
      totalcom = totalcom + (Number(this.a[i]["completed"]))
      totalincom = totalincom + (Number(this.a[i]["incomplete"]))
    }

    const ctxx = document.getElementById('mypieChart');

    new Chart(ctxx, {
      type: 'doughnut',
      data: {

        labels: [

          'Completed',
          'Incomplete'
        ],
        datasets: [{
          label: '',
          data: [totalcom, totalincom],
          backgroundColor: [

            'rgb(54, 162, 235)',
            'rgb(255, 99, 132)'

          ],
          hoverOffset: 4
        }]
      }
    }
    )
  }

}
</script>
  
<style lang="scss" scoped>
.popup {
  overflow-y: scroll;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.popup-inner {
  background: #FFF;
  padding: 32px;
  padding-top: 50%;
}
</style>