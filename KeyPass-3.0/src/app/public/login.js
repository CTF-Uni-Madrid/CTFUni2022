const $ = (selector) => document.querySelector(selector)
const $$ = (selector) => document.querySelectorAll(selector)


$("#login").addEventListener("click", async (e) => {
    e.preventDefault()
    const { value: formValues } = await Swal.fire({
        title: 'Login',
        html:
            '<h4>User:</h4>' +
            '<input id="user" type="text" value="admin" >' +
            '<h4>Password:</h4>' +
            '<input id="pass" type="password">',
        focusConfirm: false,
        preConfirm: () => {
            return {
                user: $('#user').value,
                password: $('#pass').value
            }
        }
    })
    fetch("/login", { method: "POST", body: JSON.stringify(formValues) }).then(res => { if (res.status == 200) { window.location.href = "/MainMenu" } else { Swal.fire("Error", "Error en los credenciales por favor intente de nuevo", "error") } })

})
$("#anonlogin").addEventListener("click", async (e) => {
    e.preventDefault()
    fetch("/anonlogin", { method: "POST" }).then((response) => {
        if (response.status == 200) {
            let timerInterval
            Swal.fire({
                title: "Login anonimo exitoso",
                html: "Redireccionando en <b></b> segundos.",
                timer: 2000,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading()
                    const b = Swal.getHtmlContainer().querySelector('b')
                    timerInterval = setInterval(() => {
                        b.textContent = Math.floor(Swal.getTimerLeft() / 1000)
                    }, 100)
                },
                willClose: () => {
                    clearInterval(timerInterval)
                }
            }).then((result) => {

                window.location.href = "/MainMenu"

            })

        } else {
            Swal.fire({ title: "Error", text: "Login anonimo fallido", icon: "error" })
        }
    }).catch(err => {
        Swal.fire({ title: "Error", text: "Login anonimo fallido", icon: "error" })
    })
})