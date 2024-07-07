<template>
    <div class="popup">
        <div class="popup-inner">
            <h3> Edit: {{ cname }}</h3>
            <label>New card name:</label>
            <input type="text" v-model="NewCardDetails.new_name">
            <br>
            <br>
            <label>New card Description:</label>
            <br>
            <input type="text" v-model="NewCardDetails.new_description">
            <br>
            <label>Move card to list:</label>
            <br>
            <select v-model="NewCardDetails.new_list_location" class="form-select" aria-label="Default select example">
                <option v-for="names in a" :key="names">{{ names.lname }}</option>
            </select>
            <br>
            <label>New deadline:</label>
            <input type="date" placeholder="dd-mm-yyyy" v-model="NewCardDetails.new_card_deadline">
            <br>
            <i>leave any field empty for no changes</i>
            <br>
            <button class="btn btn-light" @click.prevent="EditCard">Make Changes</button>
            <slot />

        </div>
    </div>
</template>
  
<script>
export default {
    name: 'CardEdit',
    props: { usercc: Number, cname: String, cid: Number, lidd: Number },
    data() {
        return {
            changeLidto: "",
            a: {},
            NewCardDetails: { id: this.cid, new_name: "", new_description: "", new_list_location: "", new_card_deadline: "" }
        }
    },
    methods: {
        async EditCard() {
            await fetch('http://127.0.0.1:5000/' + this.usercc + "/" + this.lidd, {
                method: 'PATCH',
                credentials: 'include',
                body: JSON.stringify(this.NewCardDetails),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then((json) => console.log(json)).catch((err) => console.log(err));

                if(this.NewCardDetails.new_list_location != ''){
                this.reloadpage()}
                this.ceditclose(false)
           

        },
        reloadpage() {
            var delayInMilliseconds = 1000; //1 second

            setTimeout(function () {
                window.location.reload()
            }, delayInMilliseconds)

        }, ceditclose(event) {
            this.$emit("cardeditclose", event)
        }
    },
    async created() {
        await fetch("http://127.0.0.1:5000/" + this.usercc, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }
        ).then((response) => response.json()).then(data => this.a = data).catch((error) => { console.log(error) })
    }
}
</script>
  
<style lang="scss" scoped>
.popup {
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
}
</style>