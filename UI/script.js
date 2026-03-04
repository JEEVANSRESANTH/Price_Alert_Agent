const API = "https://price-tracker-api.greenplant-9b018a93.southeastasia.azurecontainerapps.io"

let chart = null
let lastPrices = {}
let selectedProduct = null
let drops = []

// ------------------------------
// LOAD PRODUCTS
// ------------------------------

async function loadProducts(){

    const res = await fetch(`${API}/products/`)
    const products = await res.json()

    const table = document.getElementById("products")
    table.innerHTML = ""

    for(const p of products){

        const priceRes = await fetch(`${API}/prices/${p.id}`)
        const history = await priceRes.json()

        let latest = history.length ? history[history.length-1].price : "—"

        if(history.length >= 2){

            const old = history[history.length-2].price
            const diff = old - latest

            if(diff > 0){

                drops.push({
                    name:p.name,
                    drop:diff,
                    percent:((diff/old)*100).toFixed(2)
                })
            }
        }

        const row = document.createElement("tr")

        row.innerHTML = `
            <td>${p.name}</td>
            <td>₹ ${latest}</td>
            <td>
                <button onclick="viewHistory('${p.id}','${p.name}')">
                    History
                </button>
            </td>
        `

        table.appendChild(row)
    }

    renderDrops()
}

// ------------------------------
// ADD PRODUCT (FIXED)
// ------------------------------
async function addProduct(){

    const name = document.getElementById("name").value
    const url = document.getElementById("url").value

    const res = await fetch(`${API}/products/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            url: url
        })
    })

    if(!res.ok){
        console.error("Failed to add product", await res.text())
        return
    }

    document.getElementById("name").value = ""
    document.getElementById("url").value = ""

    loadProducts()
}
// ------------------------------
// VIEW PRICE HISTORY
// ------------------------------

async function viewHistory(id,name){

    selectedProduct = id

    const res = await fetch(`${API}/prices/${id}`)
    const history = await res.json()

    const labels = history.map(p => new Date(p.timestamp).toLocaleTimeString())
    const prices = history.map(p => p.price)

    const ctx = document.getElementById("chart").getContext("2d")

    if(chart) chart.destroy()

    chart = new Chart(ctx,{
        type:"line",
        data:{
            labels:labels,
            datasets:[{
                label:name,
                data:prices,
                borderColor:"#ff6b6b",
                backgroundColor:"rgba(255,107,107,0.2)",
                tension:0.2
            }]
        }
    })
}

// ------------------------------
// RENDER BIGGEST DROPS
// ------------------------------

function renderDrops(){

    const container = document.getElementById("drops")

    drops.sort((a,b)=>b.drop-a.drop)

    container.innerHTML=""

    for(const d of drops.slice(0,5)){

        const div = document.createElement("div")

        div.innerHTML=`
            🔥 ${d.name} dropped ₹${d.drop} (${d.percent}%)
        `

        container.appendChild(div)
    }
}

// ------------------------------
// DARK MODE
// ------------------------------

function toggleDark(){

    document.body.classList.toggle("dark")
}

// ------------------------------
// INIT
// ------------------------------

loadProducts()
