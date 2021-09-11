const got = require('got')
const express = require('express')
// import express from 'express'
app = express()



const port = process.env['port'] || 8080
const server = process.env['server'] || "http://localhost"
const server_port = process.env['server_port'] || 12345

app.get('/', (req, res) => {
    res.send('Hello World!')
})

app.get('/test', (req, res) => {
    res.send({ test: "hello world" });
})

app.get("/srv", (req, res, next) => {
    try {
        console.log(server_port)
        got.get(`${server}:${server_port}/test`).json().then(j => res.send(j));
    }catch(e){
        res.send(e)
    }

})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})