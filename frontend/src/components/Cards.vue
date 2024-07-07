<template>
    <div>
        <div>
            <CardEdit @cardeditclose="cardeditpopcloseref" v-if="EditCardPopup.show" :usercc=userc :cname=CardtoEdit.cname :cid=CardtoEdit.cid :lidd=lid>
                <button @click="EditPopupClose" class="btn btn-secondary" >Close</button>
            </CardEdit>
        </div>

        <div>
            <div v-for="names in cards" :key="names">
                <div class="card" style="width: 18rem; margin: 10px;">

                    <div class="card-body">
                        <h6 class="card-subtitle mb-2 text-muted">Due in {{ this.due(names.deadline_date) }} day(s)</h6>
                        <h4 class="card-title">{{ names.cname }}</h4>
                        <h5 class="card-text">{{ names.cdescription }}</h5>
                        <br>
                        <p class="card-subtitle mb-2 text-muted">Created on, {{
                            this.datesmaller(names.creation_date)
                        }}</p> 
                        
                        <p class="card-subtitle mb-2 text-muted">Deadline, {{ this.datesmaller(names.deadline_date) }}
                        </p>
                        
                        
                        <p class="card-subtitle mb-2 text-muted">Status: {{ whether_completed(names.completed) }}</p>
                        
                        <a href="#" class="card-link" @click.prevent="showeditwindow(names.cid, names.cname)">Edit
                            Card</a>
                        <a href="#" class="card-link" @click.prevent="MarkAsDone(names.cid)">Mark As Done</a>
                        <br>

                        <a href="#" class="card-link" @click.prevent="DeleteCard(names.cid)">Delete Card</a>
                        
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import CardEdit from "./CardEditPopup.vue"

export default {
    name: 'Cards',
    props: { userc: Number, lid: Number },

    components: { CardEdit },
    data() {
        return {
            cards: [],
            completed: "",
            toDelete: { id: "" },
            EditCardPopup: { show: false },
            CardtoEdit: { cid: 0, cname: "" }
        }




    },
    computed: {

    },

    methods: {
        whether_completed(val) {
            if (val == 0) {
                return ("Pending")
            } else {
                return ("Completed")
            }


        },
        due(dl) {
            let da = new Date(dl)
            let db = new Date()
            let a = 86400000
            if (da - db >= 0) {
                return (String((da - db) / a).substr(0, 2))
            }
            else {
                return "DEADLINE PASSED"
            }


        },

        datesmaller(sdate) {
            let t = sdate.substr(0, 16)
            return t

        },
        reloadpage() {
            var delayInMilliseconds = 1000; //1 second

            setTimeout(function () {
                window.location.reload()
            }, delayInMilliseconds)

        },
        async DeleteCard(id) {
            this.toDelete.id = id
            await fetch('http://127.0.0.1:5000/' + this.userc + "/" + this.lid, {
                method: 'DELETE',
                credentials: 'include',
                body: JSON.stringify(this.toDelete),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then((json) => console.log(json)).catch((err) => console.log(err));

            alert("Card Deleted")

            await fetch("http://127.0.0.1:5000/" + this.userc + "/" + this.lid,
                {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Content-type': 'application/json; charset=UTF-8',
                    }
                }).then((response) => response.json()).then(data => this.cards = data).catch((error) => { console.log(error) })
            console.log(this.cards)

        },
        EditPopupClose() {
            this.EditCardPopup.show = false
        },
        showeditwindow(id, name) {
            this.CardtoEdit.cid = id
            this.CardtoEdit.cname = name
            this.EditCardPopup.show = true

        },
        async MarkAsDone(cid) {
            await fetch('http://127.0.0.1:5000/' + this.userc + "/" + this.lid + "/" + cid, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then((json) => console.log(json)).catch((err) => console.log(err));


            await fetch("http://127.0.0.1:5000/" + this.userc + "/" + this.lid,
                {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Content-type': 'application/json; charset=UTF-8',
                    }
                }).then((response) => response.json()).then(data => this.cards = data).catch((error) => { console.log(error) })
            console.log(this.cards)


        },
        async cardeditpopcloseref(event) {
            this.EditCardPopup.show = false
            await fetch("http://127.0.0.1:5000/" + this.userc + "/" + this.lid,
                {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Content-type': 'application/json; charset=UTF-8',
                    }
                }).then((response) => response.json()).then(data => this.cards = data).catch((error) => { console.log(error) })
            console.log(this.cards)

        }

    },
    async created() {
        await fetch("http://127.0.0.1:5000/" + this.userc + "/" + this.lid,
            {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                }
            }).then((response) => response.json()).then(data => this.cards = data).catch((error) => { console.log(error) })
        console.log(this.cards)
    }
}

</script>

<style>

</style>