
from flask import Flask,render_template,request,session,redirect,url_for
from klasa import Korisnik
app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2021-2022"

@app.route('/register', methods=["POST","GET"])
def register():
	if request.method=="GET":
		return render_template(
			"register.html"
		)
	if request.method=="POST":
		index=request.form['index']
		email=request.form['email']
		ime_prezime=request.form['ime_prezime']
		sifra=request.form['sifra']
		potvrda_sifre=request.form['potvrda_sifre']
		godina_rodjenja=request.form['godina_rodjenja']

		if Korisnik.dohvati_korisnika(index)!=None:
			return render_template(
				"register.html",
				greska="Indeks vec postoji"
			)

		if index=="" or email=="" or ime_prezime=="" or sifra=="" or potvrda_sifre=="" or godina_rodjenja=="":
			return render_template(
				"register.html",
				greska="Sva polja moraju biti popunjena"
			)

		if '@' not in email:
			return render_template(
				"register.html",
				greska="Email mora da sadzri @"
			)

		if len(sifra)<3:
			return render_template(
				"register.html",
				greska="Sifra mora imati makar 3 karaktera"
			)
		
		if sifra!=potvrda_sifre:
			return render_template(
				"register.html",
				greska="Sifre se ne poklapaju"
			)
		
		Korisnik.insert(index,email,ime_prezime,sifra, godina_rodjenja)

		return redirect(url_for('show_all'))


@app.route('/login', methods=['POST','GET'])
def login():
	if request.method=="GET":
		if 'index' in session:
			return redirect(url_for('show_all'))
		return render_template(
			"login.html"
		)
	if request.method=='POST':
		index=request.form["index"]
		sifra=request.form['sifra']
		
		if index=="" or sifra=="":
			return render_template(
				"login.html",
				greska="Sva polja moraju biti popunjena"
			)


		korisnik=Korisnik.dohvati_korisnika(index)
		if korisnik==None:
			return render_template(
				"login.html",
				greska="korisnik sa tim indeksom ne postoji"
			)
		
		if sifra!=korisnik.get_sifra():
			return render_template(
				"login.html",
				greska="Netacna sifra"
			)

		session['index']=index
		return redirect(url_for('show_all'))


@app.route('/logout')
def logout():
	if 'index' not in session:
		return redirect(url_for(show_all))
	session.pop('index')
	return redirect(url_for('login'))

@app.route('/show_all')
def show_all():
	korisnici=Korisnik.dohvati_sve_korisnike()
	return render_template(
			"show_all.html",
			korisnici=korisnici
		)

@app.route('/update/<index>', methods=["GET", 'POST'])
def update(index):
	korisnik=Korisnik.dohvati_korisnika(index)
	if request.method=="GET":
		return render_template(
			"update.html",
			korisnik=korisnik
		)
	if request.method=="POST":
		email=request.form['email']
		ime_prezime=request.form['ime_prezime']
		sifra=request.form['sifra']
		godina_rodjenja=request.form['godina_rodjenja']

		if email=="" or ime_prezime=="" or sifra=="" or                    godina_rodjenja=="":
			return render_template(
				"update.html",
				greska='sva polja moraju biti popunjena',
				korisnik=korisnik
			)
		if '@' not in email:
			return render_template(
				"update.html",
				greska="Email mora da sadzri @",
				korisnik=korisnik
			)

		if len(sifra)<3:
			return render_template(
				"update.html",
				greska="Sifra mora imati makar 3 karaktera",
				korisnik=korisnik
			)
		
		if sifra!=korisnik.get_sifra():
			return render_template(
				"update.html",
				greska="Netacna sifra",
				korisnik=korisnik
			)

		korisnik.update(email,ime_prezime,godina_rodjenja,index)
		return redirect(url_for('show_all'))

@app.route('/profil/<index>')
def profil(index):
	korisnik=Korisnik.dohvati_korisnika(index)
	return render_template(
		'profil.html',
		korisnik=korisnik
	)

@app.route('/korisnik/<godiste>')
def korisnik(godiste):
	korisnici=Korisnik.stariji_od(godiste)
	if korisnici==None:
		return "Nema ni jedan korisnik stariji od tog godista"

	return render_template(
		'show_all.html',
		korisnici=korisnici
	)

app.run(debug=True)
