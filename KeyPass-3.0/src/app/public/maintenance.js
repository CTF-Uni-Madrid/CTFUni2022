const $ = (selector) => document.querySelector(selector)
const $$ = (selector) => document.querySelectorAll(selector)
function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
const tokenInfo = parseJwt(getCookie("jwt"))
$("#form").addEventListener("click", async (e) => {
    e.preventDefault()
    const { value: formValues } = await Swal.fire({
        title: 'Login',
        html:
            '<h4>User:</h4>' +
            `<input id="user" type="text" value="${tokenInfo.user}" readonly>` +
            '<h4>Identifier:</h4>' +
            '<input id="id" type="text" placeholder="Ejemplo: gmailpass" >',
        focusConfirm: false,
        preConfirm: () => {
            return {
                id: $('#id').value
            }
        }
    })
    fetch(`/getreg/${formValues.id}`, { method: "GET" })
        .then(res => {

            if (res.status == 501) {
                throw res.status
            } else {
                return res.json()
            }
        }
        )
        .then(json => {
            if (json.success) {
                Swal.fire({ "title": `${formValues.id} encontrado`, "text": `Registro encontrado\n valor: ${json.data}`, "icon": "success" })
            } else if (!json.success && !json.user) {
                Swal.fire("Error", "El recurso no existe", "alert")
            } else {
                Swal.fire("Error", `Este recurso no te pertenece, el propietario de este recurso es: ${json.user}`, "error")
            }
        }).catch(err => {
            if (err == 501) {
                Swal.fire("Error", "El token ha expirado o es invalido, por favor inicie sesion de nuevo", "error")
            } else {
                Swal.fire("Error", "Error desconocido", "error")
            }

        })

})


