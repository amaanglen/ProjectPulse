<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">JanKanBan Board</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link">User ID: {{ user }} :)</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="viewchange2">Edit List</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="summary">Summary</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="ExpLists">Export Lists Table</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="ExpCards">Export Cards Table</a>
            </li>
            <li class="nav-item" style="margin-left:10in">
              <a class="nav-link" href="#" @click="logout()">Logout</a>
            </li>

          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  props: { user: Number },
  data() {
    return {
      summarytoggle: false,
    }
  },
  methods: {
    viewchange2() {
      this.$emit("viewchange", true)
    },
    summary() {
      this.$emit("summaryview", true)
    },

    async ExpLists() {

      await fetch("http://127.0.0.1:5000/listexport/" + this.user, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        }
      }).then(response => response.blob())
        .then(blob => {
          var url = window.URL.createObjectURL(blob);
          var a = document.createElement('a');
          a.href = url;
          a.download = "liststable.csv";
          document.body.appendChild(a); 
          a.click();
          a.remove();
        }
        )
      

    },



    async ExpCards() {
      await fetch("http://127.0.0.1:5000/cardexport/" + this.user, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        }
      }).then(response => response.blob())
        .then(blob => {
          var url = window.URL.createObjectURL(blob);
          var a = document.createElement('a');
          a.href = url;
          a.download = "cardstable.csv";
          document.body.appendChild(a); 
          a.click();
          a.remove();
        }
        )

    },




    async logout() {
      await fetch("http://127.0.0.1:5000/logout", {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        }
      }).then((response) => response.json()).then(data => console.log(data)).catch((error) => { console.log(error) })

      window.location = ('/login')

    }
  }
}
</script>


<style>

</style>
