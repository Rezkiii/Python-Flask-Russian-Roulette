from flask import Flask, render_template, request, redirect, url_for, session  
import random  
  
app = Flask(__name__)  
app.secret_key = 'your_secret_key'  
  
def setup_game(num_players):  
    players = [f"Pemain {i+1}" for i in range(num_players)]  
    revolver = [0] * 6  
    revolver[random.randint(0, 5)] = 1   
    return players, revolver  
  
@app.route('/', methods=['GET', 'POST'])  
def index():  
    if request.method == 'POST':  
        try:  
            num_players = int(request.form['num_players'])  
            if num_players <= 0:  
                raise ValueError("Jumlah pemain harus lebih dari 0.")  
            session['players'], session['revolver'] = setup_game(num_players)  
            session['current_player_index'] = 0  
            session['game_over'] = False  
            return redirect(url_for('game'))  
        except ValueError as e:  
            return render_template('index.html', error=str(e))  
    return render_template('index.html')  
  
@app.route('/game', methods=['GET', 'POST'])  
def game():  
    if 'game_over' not in session or session['game_over']:  
        return redirect(url_for('index'))  
  
    players = session['players']  
    current_player_index = session['current_player_index']  
    player = players[current_player_index]  
  
    if request.method == 'POST':  
        choice = request.form['choice']  
        if choice not in ['ya', 'tidak']:  
            return render_template('game.html', player=player, error="Input tidak valid. Silakan masukkan 'ya' atau 'tidak'.")  
  
        if choice == 'ya':  
            revolver = session['revolver']  
            bullet = revolver.pop(0)  
            revolver.append(0)  # Menggeser revolver  
            session['revolver'] = revolver  
  
            if bullet == 1:  
                session['game_over'] = True  
                return redirect(url_for('result', winner=None, player=player))  
            else:  
                session['current_player_index'] = (current_player_index + 1) % len(players)  
                return redirect(url_for('game', sound='click'))  
  
        elif choice == 'tidak':  
            session['current_player_index'] = (current_player_index + 1) % len(players)  
            return redirect(url_for('game'))  
  
    return render_template('game.html', player=player)  
  
@app.route('/result')  
def result():  
    winner = request.args.get('winner')  
    player = request.args.get('player')  
    if winner:  
        return render_template('result.html', message=f"Semua pemain selamat! Permainan selesai.")  
    else:  
        return render_template('result.html', message=f"{player} kalah. Permainan selesai.", sound='shoot')  
  
if __name__ == '__main__':  
    app.run(debug=True)  
