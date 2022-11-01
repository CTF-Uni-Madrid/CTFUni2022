const $ = (selector) => document.querySelector(selector)
const $$ = (selector) => document.querySelectorAll(selector)
let tokenInfo

function parseJwt(token) {
    let jsonPayload = []
    let base64Url = token.split('.')[0];
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    jsonPayload[0] = JSON.parse(decodeURIComponent(window.atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join('')));
    base64Url = token.split('.')[1];
    base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');

    jsonPayload[1] = JSON.parse(decodeURIComponent(window.atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join('')));


    return jsonPayload;
};
//TODO: fix cypher/key verificator
const verify = () => {
    try {
        fetch(`/verifyToken`,
            {
                method: 'POST',
                body: JSON.stringify({ token: $("#token").value, key: $("#key").value }),
                headers: new Headers({ "Content-type": "application/json" })
            })
            .then(async (res) => {
                if (res.status != 200) throw await res.json()
                return res.json()
            }).then((data) => {
                console.log(data)
                Swal.fire({
                    title: `${data.success ? "Token Valido" : "Token Invalido"}`,
                    html: `<div>${data.message}</div>`,
                })
            })
            .catch((e) => {
                console.error(e)
                Swal.fire({
                    title: `Error`,
                    html: `<div>${e.message}</div>`,
                })
            })
    } catch (e) {
        console.log(e)
    }
}

const sign = () => {
    try {
        fetch(`/signToken`,
            {
                method: 'POST',
                body: JSON.stringify({ data: $("#data").value, key: $("#key").value, cypher: $("#cypher").value }),
                headers: new Headers({ "Content-type": "application/json" })
            })
            .then(async (res) => {
                if (res.status != 200) throw await res.json()
                return res.json()
            }).then((data) => {
                Swal.fire({
                    title: `${data.success ? "Token was signed" : "Token was not signed"}`,
                    html: `<div>${data.message}</div>`,
                })
            })
            .catch((e) => {
                Swal.fire({
                    title: `Error`,
                    html: `<div>${e.message}</div>`,
                })
            })
    } catch (e) {
        console.log(e)
    }
}

$("#token").addEventListener("input", (e) => {
    try {
        console.log(parseJwt($("#token").value))
        tokenInfo = parseJwt($("#token").value)
        //console.log(tokenInfo)
        $("#data").value = JSON.stringify(tokenInfo[1])
        $("#cypher").value = JSON.stringify(tokenInfo[0])
    } catch (e) {
        $("#data").value = "Error"
    }
});

$("#verify").addEventListener("click", (e) => {
    e.preventDefault()
    verify()
})

$("#sign").addEventListener("click", (e) => {
    e.preventDefault()
    sign()
})
