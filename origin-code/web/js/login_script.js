let loginPage = new Vue({
    el: "#login",
    data: {
        user: {
            name: "",
            pwd: ""
        }
    },
    methods: {
        submit: function () {
            if (event.keyCode == 13) loginPage.login();
        },
        login: function () {
            $.ajax({
                url: rootsrc + 'api/log',
                type: 'post',
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(loginPage.user),
                async: false,
                success: function (msg) {
                    console.log(msg);
                }
            });
            console.log(loginPage.user);
        }
    }
});

window.onload = function () {
    loadEl();
}