<template >
    
    
    <div>
        <NewCard @cardaddclose="cardaddpopcloseref" v-if="NewCardPopup.show" :lname=NewCardtoList.lname
            :lid=NewCardtoList.lid :userc=user> <button class="btn btn-secondary" @click="ClosePopup">Close</button>
        </NewCard>
    </div>

    <div v-for="names in a" :key="names">

        <div>
            <h2 class="LLL">{{ names.lname }}</h2>
            <i>{{ names.ldescription }}</i>
            <div>
                <button class="btn btn-light" @click="NewCardPopupViewOpen(names.lname, names.lid)">Add New
                    Card</button>

            </div>

        </div>
        <div>
            <Cards :userc=user :lid=names.lid />
        </div>

        <button class="btn btn-danger" @click="DelWarnPop(names.lid)">delete list</button>
        <DeleteWarning v-if="DelWarn"><button class="btn btn-danger"
                @click.prevent="DeleteList()">Yes</button><br><button class="btn btn-secondary"
                @click="DelWarn = false">No</button></DeleteWarning>

        <hr>
    </div>
    <button @click="AddNewClicked" type="button" class="btn btn-light">Add New List</button>
    <form v-if="AddNew">
        <label for="name">Name of the new list</label>
        <input type="text" id="name" v-model="NewList.name">
        <label for="description">Description of the new list</label>
        <input type="text" id="description" v-model="NewList.description">
        <button class="btn btn-light" @click.prevent="AddtoApi">Add</button>
    </form>
    <br>
    <br>
    <br>
    
    



</template>

<script>
import Cards from './Cards.vue'
import NewCard from './CardAddNew.vue'
import CardEditPopup from './CardEditPopup.vue'
import DeleteWarning from './DeleteWarning.vue'

export default {
    name: 'Lists',
    props: { user: Number },
    components: { Cards, NewCard, CardEditPopup, DeleteWarning },
    data() {
        return {
            a: {},
            ListToDelete: { id: "" },
            AddNew: false,
            ListEditD: false,
            pq: "",
            NewList: { name: "", description: "" },
            NewCardPopup: { show: false },
            NewCardtoList: { lname: "", lid: "" },
            DelWarn: false

        }

    },
    async created() {

        await fetch("http://127.0.0.1:5000/" + this.user, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }).then((response) => response.json()).then(data => this.a = data).catch((error) => { console.log(error) })
    },

    methods: {

        AddNewClicked() {
            this.AddNew = !this.AddNew
        },
        DelWarnPop(id){
            this.ListToDelete.id = id
            this.DelWarn = true

        },
        async AddtoApi() {
            this.pq = this.NewList
            await fetch('http://127.0.0.1:5000/' + this.user, {
                method: 'PUT',
                credentials: 'include',
                body: JSON.stringify(this.pq),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then((json) => console.log(json)).catch((err) => console.log(err));

            await fetch("http://127.0.0.1:5000/" + this.user, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                }
            }).then((response) => response.json()).then(data => this.a = data).catch((error) => { console.log(error) })

            this.AddNew = !this.AddNew


        },
        reloadpage() {
            var delayInMilliseconds = 1000; //1 second

            setTimeout(function () {
                window.location.reload()
            }, delayInMilliseconds)

        },

        EditListDChange() {
            this.ListEditD = !this.ListEditD
        },

        async DeleteList() {
            await fetch('http://127.0.0.1:5000/' + this.user, {
                method: 'DELETE',
                credentials: 'include',
                body: JSON.stringify(this.ListToDelete),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then((json) => console.log(json)).catch((err) => console.log(err));

            await fetch("http://127.0.0.1:5000/" + this.user, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                }
            }).then((response) => response.json()).then(data => this.a = data).catch((error) => { console.log(error) })

            this.DelWarn = false

        },
        NewCardPopupViewOpen(name, id) {
            this.NewCardtoList.lid = id
            this.NewCardtoList.lname = name
            this.NewCardPopup.show = true
        },
        ClosePopup() {
            this.NewCardPopup.show = false
        },
        async cardaddpopcloseref(event) {
            this.NewCardPopup.show = event

            await fetch("http://127.0.0.1:5000/" + this.user, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                }
            }).then((response) => response.json()).then(data => this.a = data).catch((error) => { console.log(error) })



        }


    }

}
</script>

<style scoped>
.LLL {

    text-align: Left;
    font-size: 30px;
    font-weight: 300;
    color: black;
    letter-spacing: 1px;
    text-transform: uppercase;

    align-items: Left;
}

</style>