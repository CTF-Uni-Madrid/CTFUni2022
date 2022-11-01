const jwt = require('jsonwebtoken');
const fs = require('fs');
const express = require('express');
const app = express();
const path = require("path");
app.disable("x-powered-by");
const cookieParser = require("cookie-parser");
const bodyParser = require("body-parser");
const morgan = require('morgan')
const PRIVATE_KEY = fs.readFileSync(path.join(__dirname, 'jwtRS256.key'), 'utf8');
const PUBLIC_KEY = fs.readFileSync(path.join(__dirname, 'jwtRS256.key.pub'), "utf-8");
const PUBLIC = "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA0cAtkr5cNrhq3PiFuCpL\n1y1hNwzm0Mf4GFXozKXDNIdlwZ8YNMinjZil/rtfOEaOsvMfRE+qhx51MfS0BEPe\ncmQZ1Ld/YHFfJpraFqDB2WyCCgAAW4kbiTW3eLpBNMoZtw1qhMl/wIkjCZNaSWRm\nYVUjsqLLJVfDZzfmMNv3DOOQ4EH4CODMYNuh76R0ELxCF2VhbFYTes4/P91MlMVE\nxYgs6nsnnf4spKUBZxrfdnMN7PeTm/Tp0tNsOTkYLj7YTE3ZRRwONVQ1i804lr31\nDwYk5gHc76CFedKc9pDvjK3ZJaS/TbmZRxcG3kCSk25ljODK9M2ndTmxendZbmCD\nJzvhb+W0o3pWz/uHLNgvAnftzqT/bG/TJ8mCr4pVojewLROILzSLK58/H1rsZmcf\nbZKY45EmU/RgMXVC4m1DrbI0lEnAeSjGQBFIFoGWoGs30WCkO1IrSMzqVQwdQs/3\nLr0lYiFMDx6+lRUtMVbKRx9FO6rGHPHlfwR8adZGAQUUsVX8k7H9Gij199i8Xxjq\nqZ1BMiIa2nliTOGSlMraz58q4YiSZ88LKPKhtcNbN2v8ydQBV4n9n/TazraOjUCw\n9Lp72CmdyUauet6U7iiqBnywEwAZkyQqGHSai3whluXU8877VfcTPIjCk1xjEUaa\nU0JYBz2f3l38YUpkNrTWHjMCAwEAAQ==\n-----END PUBLIC KEY-----\n"
const database = require("./db.json");
require('dotenv').config()
app.disable("x-powered-by");
app.use(bodyParser.json());
app.use(
    bodyParser.urlencoded({
        // to support URL-encoded bodies
        extended: true,
    })
);
app.use(cookieParser());
app.use(morgan('tiny'))

const checktoken = (req, res, next) => {
    const token = req.cookies.jwt;
    if (token) {
        jwt.verify(token, PUBLIC, (err, decoded) => {
            if (err) {
                console.log(err)
                return res.status(501).json({
                    success: false,
                    message: 'Token is not valid'
                });
            } else {
                req.decoded = decoded;
                next();
            }
        });

    } else {
        return res.status(403).json({
            success: false,
            message: 'Auth token is not supplied'
        });
    }
};

app.get("/", (req, res) => {
    res.redirect("/index.html");
});
app.post("/login", (req, res) => {
    res.status(403).send("Error en los credenciales por favor intente de nuevo <script>setTimeout(function(){window.location.href = '/';}, 3000);</script>");
});
app.post("/anonlogin", (req, res) => {
    let token = jwt.sign({ user: "anon" }, PRIVATE_KEY, { algorithm: "RS256", noTimestamp: true });
    res.cookie("jwt", token);
    res.send("ok")
});
app.get("/getreg/:id", checktoken, (req, res) => {
    let { id } = req.params;
    id = id.toLowerCase();
    if (id in database) {
        res.status(200).json({ data: database[id], success: true, public: true, user: "anon" });
    } else if (id === "flag") {
        if (req.decoded.user == "admin") {
            res.status(200).json({ data: process.env.FLAG, success: true, public: false, user: "admin" });
        } else {
            res.status(403).json({ data: undefined, success: false, public: false, user: "admin" });
        }
    } else {
        res.status(404).json({ data: undefined, success: false, public: false, user: undefined });
    }


});
app.get("/MainMenu", (req, res) => {
    res.redirect("/maintenance.html");
})
app.post("/verifyToken", (req, res) => {
    const { token, key } = req.body;
    if (token && key) {
        jwt.verify(token, Buffer.from(key, "utf-8"), (err, decoded) => {
            if (err) {
                res.json({
                    success: false,
                    message: 'Token is not valid'
                });
            } else {
                res.json({
                    success: true,
                    message: 'Token is valid'
                });
            }
        });
    } else {
        res.status(403).json({
            success: false,
            message: 'Auth token or key is not supplied'
        })
    }

    //res.redirect("/maintenance.html");
})
app.post("/signToken", (req, res) => {
    let data
    let cypher
    let key
    try {
        data = JSON.parse(req.body.data);
        cypher = JSON.parse(req.body.cypher);
        key = req.body.key;
    } catch (e) {
        res.status(500).json({
            success: false,
            message: 'data, cypher or key is not supplied or has an incorrect format'
        })
        return
    }

    if (data && cypher && key) {
        try {
            let token = jwt.sign(data, Buffer.from(key, "utf-8"), { algorithm: cypher.alg, noTimestamp: true });
            res.json({
                success: true,
                message: token
            });
        } catch (e) {
            res.status(500).json({
                success: false,
                message: 'Sign proccess failed'
            })
        }
    } else {
        res.status(500).json({
            success: false,
            message: 'data, cypher or key is not supplied'
        })
    }
    //console.log(token)

})
app.use(express.static(path.join(__dirname, "/public")));
app.use("*", function (req, res) {
    res.status(404);

    // respond with html page
    if (req.accepts("html")) {
        res.send("404 Not Found");
        return;
    }

    // respond with json
    if (req.accepts("json")) {
        res.json({ error: "Not found" });
        return;
    }

    // default to plain-text. send()
    res.type("txt").send("Not found");
});
app.listen(process.env.PORT || 4235, () => {
    console.log("Server is running on port", process.env.PORT || 4235);
});
