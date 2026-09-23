from flask import Flask, render_template, request, redirect
import os, subprocess, signal

app = Flask(__name__)
running_bots = {}

@app.route('/')
def home():
    return render_template('index.html', bots=running_bots)

@app.route('/deploy', methods=['POST'])
def deploy():
    bot_name = request.form.get('bot_name')
    token = request.form.get('token')
    code = request.form.get('code')
    os.makedirs(f"bots/{bot_name}", exist_ok=True)
    with open(f"bots/{bot_name}/main.py", "w") as f:
        f.write(code.replace("YOUR_TOKEN_HERE", token))
    proc = subprocess.Popen(["python", f"bots/{bot_name}/main.py"])
    running_bots[bot_name] = {"status": "Online", "pid": proc.pid}
    return redirect('/')

@app.route('/stop/<name>')
def stop(name):
    if name in running_bots:
        try:
            os.kill(running_bots[name]['pid'], signal.SIGTERM)
        except: pass
        running_bots[name]['status'] = "Offline"
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
