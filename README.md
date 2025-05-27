## 1.  Repository des livres (`books.py`)

Ce module gère les requêtes liées aux livres dans la base de données.

### Méthodes disponibles :

- **`get_by_isbn(isbn)`**  
  Retourne le livre correspondant à l’ISBN exact, ou `None` si introuvable.

- **`get_by_title(title)`**  
  Recherche tous les livres dont le titre contient la chaîne fournie (recherche insensible à la casse).

- **`get_by_author(author)`**  
  Même fonctionnement que pour le titre, mais sur le nom de l’auteur.

---

## 2.  Repository des utilisateurs (`users.py`)

Ce module gère les accès aux données des utilisateurs.

### Importations :

- `Session` : connexion à la base de données  
- `BaseRepository` : repository générique  
- `User` : modèle de l’utilisateur

### Méthode principale :

- **`get_by_email(email)`**  
  Recherche un utilisateur par email.  
  → Utilise la session (`self.db`) pour interroger la table `User`.  
  → Retourne le premier utilisateur correspondant ou `None`.

---

## 3.  Repository des emprunts (`loans.py`)

Ce module gère les emprunts de livres.

### Importations :

- `Session` : gestion de la base de données  
- `List` : typage des listes de résultats  
- `datetime` : gestion des dates

### Méthodes disponibles :

- **`get_active_loans()`**  
  Retourne tous les emprunts non encore retournés (`return_date == None`).

- **`get_overdue_loans()`**  
  Retourne les emprunts en retard (la date limite est dépassée).

- **`get_loans_by_user(user_id)`**  
  Liste les emprunts d’un utilisateur donné.

- **`get_loans_by_book(book_id)`**  
  Liste les emprunts liés à un livre donné.

---

## 4.  Migration initiale (Alembic)

Permet de créer les tables à partir des modèles SQLAlchemy.

### Étapes :


- **`alembic revision --autogenerate -m "Initial migration `**

--autogenerate : détecte automatiquement les modèles SQLAlchemy et génère le code pour créer les tables manquantes.

-m "Initial migration" : ajoute un message descriptif pour identifier la migration.


- **`alembic upgrade head`**

- Cette commande crée les tables dans la base de données en fonction des modèles définis avec SQLAlchemy.

## 5. Test de l’API
Pour lancer l'application, exécutez : 

- **`python run.py`**

- Puis ouvrez votre navigateur et rendez-vous à l’adresse suivante :
http://localhost:8000/docs

-- Depuis cette interface, vous pouvez :

- Créer un utilisateur
- Vous connecter pour obtenir un token d’authentification
- Ajouter un livre ou un emprunt
- Consulter les listes de livres, utilisateurs et emprunts

