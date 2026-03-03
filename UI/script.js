const API = "http://127.0.0.1:8000"

let chart = null
let lastPrices = {}
let selectedProduct = null
let drops = []


async function loadProducts(){

    const response = await fetch(`${API}/products/`)
    const products = await response.json()

    const table = document.getElementById("products-body")
    const cards = document.getElementById("product-cards")

    table.innerHTML = ""
    cards.innerHTML = ""

    drops = []

    for(const p of products){

        const priceRes = await fetch(`${API}/prices/history/${p.id}`)
        const history = await priceRes.json()

        let latestPrice = "-"
        let changeClass = ""
        let changeText = ""

        if(history.length > 0){

            const latest = history[history.length - 1]
            latestPrice = latest.price

            if(lastPrices[p.id]){

                const oldPrice = lastPrices[p.id]
                const diff = latestPrice - oldPrice
                const percent = ((diff / oldPrice) * 100).toFixed(2)

                if(diff < 0){
                    changeClass = "price-down"
                    changeText = `↓ ${Math.abs(percent)}%`

                    drops.push({
                        name:p.name,
                        drop:oldPrice-latestPrice
                    })
                }

                if(diff > 0){
                    changeClass = "price-up"
                    changeText = `↑ ${percent}%`
                }
            }

            lastPrices[p.id] = latestPrice
        }


        /* FORMAT PRICE (safe currency formatting) */

        const formattedPrice =
        latestPrice === "-"
        ? "-"
        : new Intl.NumberFormat("en-IN",{
            style:"currency",
            currency:"INR"
        }).format(latestPrice)



        /* TABLE VIEW */

        const row = document.createElement("tr")

        row.innerHTML = `
        <td>${p.name}</td>
        <td class="${changeClass}">
        ${formattedPrice}
        <span class="change">${changeText}</span>
        </td>
        <td>
        <button onclick="showGraph('${p.id}')">Graph</button>
        <button onclick="deleteProduct('${p.id}')">Delete</button>
        </td>
        `

        table.appendChild(row)



        /* PRODUCT CARDS */

        const card = document.createElement("div")
        card.className = "card"

        card.innerHTML = `
        <div class="card-title">${p.name}</div>
        <div class="card-price">${formattedPrice}</div>
        <button onclick="showGraph('${p.id}')">Graph</button>
        `

        cards.appendChild(card)

    }



    /* LEADERBOARD */

    const leaderboard = document.getElementById("leaderboard")
    leaderboard.innerHTML = ""

    drops.sort((a,b)=>b.drop-a.drop)

    drops.slice(0,3).forEach(d=>{

        const item = document.createElement("div")
        item.className = "leader-card"

        item.innerHTML = `
        ${d.name}<br>
        Drop: ${new Intl.NumberFormat("en-IN",{
            style:"currency",
            currency:"INR"
        }).format(d.drop)}
        `

        leaderboard.appendChild(item)

    })

}



/* ADD PRODUCT */

async function addProduct(){

    const name = document.getElementById("name").value
    const url = document.getElementById("url").value

    if(!name || !url){
        alert("Enter product name and URL")
        return
    }

    await fetch(`${API}/products/?name=${encodeURIComponent(name)}&url=${encodeURIComponent(url)}`,{
        method:"POST"
    })

    document.getElementById("name").value = ""
    document.getElementById("url").value = ""

    loadProducts()
}



/* DELETE PRODUCT */

async function deleteProduct(id){

    await fetch(`${API}/products/${id}`,{
        method:"DELETE"
    })

    loadProducts()
}



/* SHOW GRAPH */

async function showGraph(productId){

    selectedProduct = productId

    const response = await fetch(`${API}/prices/history/${productId}`)
    const data = await response.json()

    const prices = data.map(p=>p.price)
    const times = data.map(p=>p.timestamp)

    const ctx = document.getElementById("priceChart")

    if(chart){
        chart.destroy()
    }

    chart = new Chart(ctx,{
        type:"line",
        data:{
            labels:times,
            datasets:[{
                label:"Price",
                data:prices,
                borderWidth:2,
                tension:0.3
            }]
        }
    })

}



/* DARK MODE */

function toggleDarkMode(){

    const body = document.body

    body.classList.toggle("dark")

    if(body.classList.contains("dark")){
        localStorage.setItem("theme","dark")
    }else{
        localStorage.setItem("theme","light")
    }

}


function loadTheme(){

    const theme = localStorage.getItem("theme")

    if(theme === "dark"){
        document.body.classList.add("dark")
    }

}

loadTheme()



/* INITIAL LOAD */

loadProducts()



/* AUTO REFRESH */

setInterval(()=>{

    loadProducts()

    if(selectedProduct){
        showGraph(selectedProduct)
    }

},30000)