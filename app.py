
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

    def update_count(self, card_value):
        try:
            card_value = int(card_value)
            self.running_count += card_value
            self.true_count = Decimal(self.running_count) / max(Decimal("0.5"), self.decks_remaining)
        except ValueError:
            pass

    def update_decks_remaining(self, decks_played):
        self.decks_remaining = max(Decimal("0.5"), self.decks_remaining - Decimal(decks_played))

    def suggest_bet(self):
        index = min(max(int(self.true_count), 0), len(self.bet_spread) - 1)
        return self.base_bet * self.bet_spread[index]

    def update_bankroll(self, outcome):
        bet = self.suggest_bet()
        if outcome == "win":
            self.bankroll += bet
        elif outcome == "loss":
            self.bankroll = max(Decimal("0"), self.bankroll - bet)

    def status(self):
        return {
            "Running Count": self.running_count,
            "True Count": round(self.true_count, 2),
            "Decks Remaining": round(self.decks_remaining, 2),
            "Suggested Bet": self.suggest_bet(),
            "Bankroll": round(self.bankroll, 2)
        }

counter = HiOptII_BlackjackCounter()

@app.route('/')
def accueil():
    return render_template("accueil.html")

@app.route('/blackjack')
def index():
    return render_template("index.html", status=counter.status())

@app.route('/update_count', methods=['POST'])
def update_count():
    card_value = request.form.get("card")
    if card_value is not None:
        counter.update_count(card_value)
    return jsonify(counter.status())

@app.route('/update_decks', methods=['POST'])
def update_decks():
    decks_played = request.form.get("decks")
    if decks_played is not None:
        try:
            counter.update_decks_remaining(float(decks_played))
        except ValueError:
            return jsonify({"error": "Valeur invalide"}), 400
    return jsonify(counter.status())

@app.route('/update_bankroll', methods=['POST'])
def update_bankroll():
    outcome = request.form.get("outcome")
    new_bankroll = request.form.get("bankroll")

    if new_bankroll and outcome == "set":
        try:
            counter.bankroll = Decimal(new_bankroll)
        except ValueError:
            return jsonify({"error": "Valeur de bankroll invalide"}), 400
    elif outcome in ["win", "loss"]:
        counter.update_bankroll(outcome)

    return jsonify(counter.status())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
