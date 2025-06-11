from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clé secrète plus sécurisée

# Ajout de la date actuelle dans le contexte global de tous les templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Base de données utilisateurs simulée (à remplacer par une vraie base de données en production)
users_db = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html", nom_site="MaSanté")

@app.route("/liste-praticiens")
@app.route("/praticiens")
def liste_praticiens():
    return render_template("praticiens.html", nom_site="MaSanté")

@app.route("/appointments")
@login_required
def appointments():
    return render_template("appointments.html", nom_site="Mes Rendez-vous - MaSanté")

@app.route("/fiche-praticien")
@app.route("/fiche_praticien")
def fiche_praticien():
    # Données factices pour le praticien (à remplacer par une requête à la base de données)
    praticien = {
        "id": 1,
        "nom": "Dr Jaou Belkacem",
        "photo": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&q=80",
        "specialite": "Médecin généraliste",
        "adresse": "7 bis Avenue Gaston Chauvin, 93600 Aulnay-sous-Bois",
        "tarif": "Conventionné secteur 1",
        "description": "Médecin généraliste expérimenté avec plus de 15 ans d'expérience. Spécialisé dans les soins de famille et le suivi des patients chroniques.",
        "horaires": [
            {"jour": "Lundi", "horaire": "09:00 - 12:30, 14:00 - 18:00"},
            {"jour": "Mardi", "horaire": "09:00 - 12:30, 14:00 - 18:00"},
            {"jour": "Mercredi", "horaire": "09:00 - 12:30, 14:00 - 18:00"},
            {"jour": "Jeudi", "horaire": "09:00 - 12:30, 14:00 - 18:00"},
            {"jour": "Vendredi", "horaire": "09:00 - 12:30, 14:00 - 17:00"},
            {"jour": "Samedi", "horaire": "09:00 - 12:00"},
            {"jour": "Dimanche", "horaire": "Fermé"}
        ]
    }
    return render_template("fiche_praticien.html", nom_site=f"{praticien['nom']} - MaSanté", praticien=praticien)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", nom_site="Mon Profil - MaSanté")

@app.route("/reserver")
@login_required
def reserver_page():
    return render_template("reserver.html", nom_site="Réserver - MaSanté")

@app.route("/reset-password")
@app.route("/reset_password")
def reset_password():
    return render_template("reset_password.html", nom_site="Réinitialiser le mot de passe - MaSanté")

@app.route("/selection-services")
@app.route("/selection_services")
@login_required
def selection_services_page():
    return render_template("selection_services.html", nom_site="Sélection des services - MaSanté")

@app.route("/services/<int:id>")
def selection_services(id):
    praticien = {
        "id": id,
        "nom": "Dr Jaou Belkacem",
        "photo": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&q=80",
        "specialite": "Médecin généraliste",
        "adresse": "7 bis Avenue Gaston Chauvin, 93600 Aulnay-sous-Bois",
        "tarif": "Conventionné secteur 1",
        "services": [
            {
                "id": 1,
                "nom": "Consultation générale",
                "description": "Consultation de suivi général",
                "prix": "25"
            },
            {
                "id": 2,
                "nom": "Consultation urgente",
                "description": "Consultation pour cas urgents",
                "prix": "35"
            },
            {
                "id": 3,
                "nom": "Consultation de suivi",
                "description": "Suivi de traitement en cours",
                "prix": "20"
            }
        ]
    }

    # Récupérer la date et l'heure depuis l'URL
    date = request.args.get('date', '')
    heure = request.args.get('heure', '')

    return render_template("selection_services.html", praticien=praticien, date=date, heure=heure, nom_site="MaSanté")

@app.route("/reserver/<int:id>", methods=["GET", "POST"])
def reserver(id):
    praticien = {
        "id": id,
        "nom": "Dr Jaou Belkacem",
        "specialite": "Médecin généraliste",
        "adresse": "7 bis Avenue Gaston Chauvin, 93600 Aulnay-sous-Bois",
        "tarif": "Conventionné secteur 1"
    }

    planning = [
        {"nom": "lundi", "date": "10 juin", "creneaux": ["09:00", "09:30", "10:00"]},
        {"nom": "mardi", "date": "11 juin", "creneaux": ["09:45", "10:15", "10:45"]},
        {"nom": "mercredi", "date": "12 juin", "creneaux": ["09:30", "10:00"]},
        {"nom": "jeudi", "date": "13 juin", "creneaux": []},
        {"nom": "vendredi", "date": "14 juin", "creneaux": ["11:00", "11:30"]},
        {"nom": "samedi", "date": "15 juin", "creneaux": []},
        {"nom": "dimanche", "date": "16 juin", "creneaux": []}
    ]

    return render_template("reserver.html", praticien=praticien, planning=planning, nom_site="MaSanté")

@app.route("/confirmer/<int:id>", methods=["POST"])
def confirmer_rdv(id):
    # Récupérer les données du formulaire
    date = request.form.get('date')
    heure = request.form.get('heure')
    service_id = request.form.get('service')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')

    # Simuler la sauvegarde du rendez-vous
    flash("Votre rendez-vous a été enregistré avec succès !", "success")

    # Récupérer les informations du praticien
    praticien = {
        "id": id,
        "nom": "Dr Jaou Belkacem",
        "specialite": "Médecin généraliste",
        "adresse": "7 bis Avenue Gaston Chauvin, 93600 Aulnay-sous-Bois",
        "tarif": "Conventionné secteur 1"
    }

    # Récupérer les informations du service sélectionné
    services = {
        "1": {"nom": "Consultation générale", "prix": "25"},
        "2": {"nom": "Consultation urgente", "prix": "35"},
        "3": {"nom": "Consultation de suivi", "prix": "20"}
    }
    service = services.get(service_id, {"nom": "Service non spécifié", "prix": "0"})

    return render_template("confirmation.html", praticien=praticien, service=service,
                         date=date, heure=heure, nom=nom, prenom=prenom, email=email,
                         nom_site="MaSanté")

@app.route("/confirmation")
def confirmation():
    # Données de démonstration pour tester la page
    praticien = {
        "id": 1,
        "nom": "Dr Jaou Belkacem",
        "specialite": "Médecin généraliste",
        "adresse": "7 bis Avenue Gaston Chauvin, 93600 Aulnay-sous-Bois",
        "tarif": "Conventionné secteur 1"
    }
    service = {
        "nom": "Consultation générale",
        "prix": "25"
    }
    return render_template("confirmation.html", praticien=praticien, service=service,
                         date="10 juin", heure="09:00", nom="Dupont", prenom="Jean",
                         email="jean.dupont@example.com", nom_site="MaSanté")
    # Tu peux ici enregistrer le rdv (dans un fichier, BDD ou juste afficher un message)
    flash(f"Rendez-vous confirmé pour {prenom} {nom} le {date} à {heure} avec le praticien #{id}", "success")
    return redirect(url_for("index"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Vérification des identifiants (à remplacer par une vraie vérification en base de données)
        user = users_db.get(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['name']
            
            if remember:
                session.permanent = True
                
            flash('Connexion réussie !', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')
    
    return render_template("login.html", nom_site="MaSanté")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation des données
        if not all([name, email, password, confirm_password]):
            flash('Tous les champs sont obligatoires.', 'error')
        elif password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
        elif email in users_db:
            flash('Un compte existe déjà avec cette adresse email.', 'error')
        else:
            # Création du compte utilisateur
            user_id = str(len(users_db) + 1)
            users_db[email] = {
                'id': user_id,
                'name': name,
                'email': email,
                'password': generate_password_hash(password)
            }
            
            flash('Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
    
    return render_template("register.html", nom_site="MaSanté")

@app.route("/logout")
def logout():
    session.clear()
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dashboard():
    # Page tableau de bord à implémenter
    return render_template("dashboard.html", nom_site="Tableau de bord - MaSanté")

@app.route("/cgu")
def cgu():
    return render_template("cgu.html", nom_site="MaSanté")

@app.route("/mentions-legales")
def mentions_legales():
    return render_template("mentions-legales.html", nom_site="MaSanté")

@app.route("/confidentialite")
def politique_confidentialite():
    return render_template("confidentialite.html", nom_site="MaSanté")

@app.route('/parametres-cookies')
def parametres_cookies():
    return render_template('parametres_cookies.html', nom_site="MaSanté")

@app.route('/mes-documents')
@login_required
def mes_documents():
    # Données factices pour la démonstration
    documents = [
        {
            'id': 1,
            'nom': 'Ordonnance du 15/06/2023',
            'type': 'ordonnance',
            'date_ajout': '2023-06-15',
            'taille': '150 Ko',
            'url': '#'
        },
        {
            'id': 2,
            'nom': 'Analyse sanguine complète',
            'type': 'analyse',
            'date_ajout': '2023-05-28',
            'taille': '420 Ko',
            'url': '#'
        },
        {
            'id': 3,
            'nom': 'Compte-rendu IRM lombaire',
            'type': 'compte-rendu',
            'date_ajout': '2023-04-12',
            'taille': '1.2 Mo',
            'url': '#'
        },
        {
            'id': 4,
            'nom': 'Radiographie du genou',
            'type': 'imagerie',
            'date_ajout': '2023-03-22',
            'taille': '2.5 Mo',
            'url': '#'
        },
        {
            'id': 5,
            'nom': 'Certificat médical',
            'type': 'autre',
            'date_ajout': '2023-02-15',
            'taille': '320 Ko',
            'url': '#'
        }
    ]
    return render_template('documents.html', documents=documents, nom_site="Mes Documents - MaSanté")

@app.route('/plan-du-site')
def sitemap():
    return render_template('sitemap.html', nom_site="Plan du site - MaSanté")



if __name__ == "__main__":
    app.run(debug=True)
