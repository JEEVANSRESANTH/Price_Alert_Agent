const API = "https://price-tracker-api.greenplant-9b018a93.southeastasia.azurecontainerapps.io"

let chart = null
let selectedProduct = null
let drops = []

// ------------------------------
// LOAD PRODUCTS
// ------------------------------

async function loadProducts(){

    drops = []

    const res = await fetch(`${API}/products/`)
    const products = await res.json()

    const table = document.getElementById("products-body")
    table.innerHTML = ""

    for(const p of products){

        const priceRes = await fetch(`${API}/prices/last/${p.id}`)

        let history = []

        if(priceRes.ok){
            history = await priceRes.json()
        }

        if(!Array.isArray(history)){
            history = []
        }

        let latest = history.price ?? "—"

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
// ADD PRODUCT
// ------------------------------

async function addProduct(){

    const name = document.getElementById("name").value
    const url = document.getElementById("url").value

    const res = await fetch(
        `${API}/products/?name=${encodeURIComponent(name)}&url=${encodeURIComponent(url)}`,
        {
            method: "POST"
        }
    )

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

    const res = await fetch(`${API}/prices/history/${id}`)

    if(!res.ok){
        console.log("No history yet")
        return
    }

    const history = await res.json()

    if(!Array.isArray(history) || history.length === 0){
        console.log("Empty history")
        return
    }

    const labels = history.map(p => new Date(p.timestamp).toLocaleTimeString())
    const prices = history.map(p => p.price)

    const ctx = document.getElementById("priceChart").getContext("2d")

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

    const container = document.getElementById("leaderboard")

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