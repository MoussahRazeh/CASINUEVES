
async function updateCount(value) {
    let response = await fetch("/update_count", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "card=" + value
    });

    let data = await response.json();
    document.getElementById("running_count").innerText = data["Running Count"];
    document.getElementById("true_count").innerText = data["True Count"];
    document.getElementById("decks_remaining").innerText = data["Decks Remaining"];
    document.getElementById("suggested_bet").innerText = data["Suggested Bet"];

    updateAdvice(data["True Count"]);
}

function updateAdvice(trueCount) {
    let advice = document.getElementById("bet_advice");
    if (trueCount < 1) {
        advice.innerHTML = "Mise minimale - <span style='color: #00FF00;'>Le jeu n'est pas favorable</span>";
    } else if (trueCount >= 1 && trueCount < 3) {
        advice.innerHTML = "Mise normale - <span style='color: #FFD700;'>Situation équilibrée</span>";
    } else {
        advice.innerHTML = "Mise agressive - <span style='color: red;'>Avantage joueur</span>";
    }
}

async function updateBankroll() {
    let newBankroll = parseFloat(document.getElementById("bankrollInput").value);
    if (!isNaN(newBankroll) && newBankroll > 0) {
        let response = await fetch("/update_bankroll", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: "outcome=set&bankroll=" + newBankroll
        });

        let data = await response.json();
        document.getElementById("bankroll").innerText = data["Bankroll"];
    }
}

async function updateGameResult(result) {
    let response = await fetch("/update_bankroll", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "outcome=" + result
    });

    let data = await response.json();
    document.getElementById("bankroll").innerText = data["Bankroll"];
}

async function updateDecks() {
    let decksValue = parseFloat(document.getElementById("deckInput").value);
    if (!isNaN(decksValue) && decksValue > 0) {
        let response = await fetch("/update_decks", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: "decks=" + decksValue
        });

        let data = await response.json();
        document.getElementById("decks_remaining").innerText = data["Decks Remaining"];
    }
}
