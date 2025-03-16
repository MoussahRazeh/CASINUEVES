from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from decimal import Decimal

app = Flask(__name__)
CORS(app)

class HiOptII_BlackjackCounter:
    def __init__(self, decks=6, bankroll=1000, base_bet=10):
        self.running_count = 0
        self.true_count = Decimal(0)
        self.decks_remaining = Decimal(decks)
        self.bankroll = Decimal(bankroll)
        self.base_bet = Decimal(base_bet)
        self.bet_spread = [1, 2, 5, 10, 15, 20]

    def update_count(self, card):
        card_values = {
            "2": +1, "3": +1, "4": +2, "5": +2, "6": +1,
            "7": +1, "8": 0, "9": 0,
            "10": -2, "J": -2, "Q": -2, "K": -2, "A": 0
        }
        if card in card_values:
            self.running_count += card_values[card]
        self.true_count = Decimal(self.running_count) / max(Decimal("0.5"), self.decks_remaining)

    def update_decks_remaining(self, decks_played):
        self.decks_remaining = max(Decimal("0.5"), self.decks_remaining - Decimal(decks_played))

    def suggest_bet():
        """Détermine la mise suggérée en fonction du True Count"""
        index = min(max(int(counter.true_count), 0), len(counter.bet_spread) - 1)
        return counter.base_bet * counter.bet_spread[index]

    def update_bankroll(self, outcome):
        bet = self.suggest_bet()
        if outcome == "win":
            self.bankroll += bet
        elif outcome == "loss":
            self.bankroll = max(Decimal("0"), self.bankroll - bet)

    def status():
        return {
           "Running Count": counter.running_count,
           "True Count": round(counter.true_count, 2),
           "Decks Remaining": round(counter.decks_remaining, 2),
           "Suggested Bet": suggest_bet(),  # Calcul de la mise en fonction du TC
           "Bankroll": round(counter.bankroll, 2)
        }

counter = HiOptII_BlackjackCounter()

@app.route('/')
def accueil():
    return render_template("accueil.html")

@app.route('/blackjack')
def index():
    return render_template("index.html", status=counter.status)

@app.route('/update_count', methods=['POST'])
def update_count():
    card_value = request.form.get("card")  # Récupère la carte

    if card_value is not None:
        try:
            # Convertir la valeur de la carte en int (car on reçoit un nombre du JavaScript)
            card_value = int(card_value)
            counter.running_count += card_value  # Ajouter directement la valeur
            counter.true_count = Decimal(counter.running_count) / max(Decimal("0.5"), counter.decks_remaining)
        except ValueError:
            return jsonify({"error": "Valeur de carte invalide"}), 400  # Gérer les erreurs

    return jsonify(counter.status())

@app.route('/update_decks', methods=['POST'])
def update_decks():
    decks_played = float(request.form.get("decks"))
    counter.update_decks_remaining(decks_played)
    return jsonify(counter.status())

@app.route('/update_bankroll', methods=['POST'])
def update_bankroll():
    outcome = request.form.get("outcome")
    counter.update_bankroll(outcome)
    return jsonify(counter.status())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
