<template>
    <div class="popup">
        <div class="popup-inner">
            <h3>List: {{ lname }}</h3>
            <label>Card Name</label>
            <input type="text" v-model="NewCardDetails.name">
            <br>
            <label>Card Description</label>
            <input type="text" v-model="NewCardDetails.description">
            <label>Deadline</label>
            <input type="date" placeholder="dd-mm-yyyy" v-model="NewCardDetails.deadline">
            <button class="btn btn-light" @click.prevent="AddCard">Add Card</button>
            <slot />

        </div>
    </div>
</template>
  
<script>
export default {
    name: 'NewCard',
    props: { userc: Number, lname: String, lid: Number },
    data() {
        return {
            NewCardDetails: { name: "", description: "" , deadline: ""}
        }
    },
    methods: {
        async AddCard() {
            await fetch('http://127.0.0.1:5000/' + this.userc + "/" + this.lid, {
                method: 'PUT',
                credentials: 'include',
                body: JSON.stringify(this.NewCardDetails),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then((json) => console.log(json)).catch((err) => console.log(err));

                this.caddclose(false)
            
               

        },
        reloadpage() {
            var delayInMilliseconds = 1000; //1 second

            setTimeout(function () {
                window.location.reload()
            }, delayInMilliseconds)
            
        },
        caddclose(event) {
        this.$emit("cardaddclose", event)


    }
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