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




//


# 📚 Gestion de Bibliothèque – FastAPI TP3



## 🔒 Exercice 7 : Mise à jour de la route d’authentification

### 📁 Fichier : `src/api/routes/auth.py`

Nous mettons en place un système d’authentification avec `OAuth2PasswordRequestForm`, en utilisant la couche métier `UserService`.

### 🧹 Code :

```python
@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    repository = UserRepository(UserModel, db)
    service = UserService(repository)

    user = service.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not service.is_active(user=user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur inactif",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
```

---

## 🧪 Exercice 8 : Tests unitaires – Couche métier utilisateur

### 📁 Fichier : `tests/conftest.py`

Mise en place d’une base SQLite en mémoire pour les tests automatisés :

```python
@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine
```

Client de test FastAPI :

```python
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}
```

### 📁 Fichier : `tests/services/test_users.py`

#### ✅ Exemple de test : création d’un utilisateur

```python
def test_create_user(db_session: Session):
    repository = UserRepository(User, db_session)
    service = UserService(repository)

    user_in = UserCreate(
        email="test@example.com",
        password="password123",
        full_name="Test User"
    )

    user = service.create(obj_in=user_in)

    assert user.email == "test@example.com"
    assert hasattr(user, "hashed_password")
    assert user.hashed_password != "password123"
```

#### 🔐 Exemple : authentification

```python
def test_authenticate_user(db_session: Session):
    user_in = UserCreate(
        email="auth@example.com",
        password="password123",
        full_name="Auth User"
    )

    user = service.create(obj_in=user_in)
    authenticated_user = service.authenticate(email="auth@example.com", password="password123")

    assert authenticated_user.id == user.id
```

#### 🔄 Exemple : mise à jour

```python
def test_update_user(db_session: Session):
    user = service.create(obj_in=UserCreate(...))
    update = UserUpdate(full_name="New Name")

    updated_user = service.update(db_obj=user, obj_in=update)

    assert updated_user.full_name == "New Name"
```

---

## 📊 Exercice 9 : Service de Statistiques

### 📁 Fichier : `src/services/stats.py`

Un service pour calculer des statistiques globales et détaillées sur les livres, utilisateurs et emprunts.

#### 📈 Statistiques générales

```python
def get_general_stats(self) -> Dict[str, Any]:
    return {
        "total_books": self.db.query(func.sum(Book.quantity)).scalar() or 0,
        "unique_books": self.db.query(func.count(Book.id)).scalar() or 0,
        ...
    }
```

#### 📚 Livres les plus empruntés

```python
def get_most_borrowed_books(self, limit: int = 10) -> List[Dict[str, Any]]:
    result = self.db.query(
        Book.id, Book.title, func.count(Loan.id).label("loan_count")
    ).join(Loan).group_by(Book.id).order_by(func.count(Loan.id).desc()).limit(limit).all()

    return [{"id": book.id, "title": book.title, "loan_count": book.loan_count} for book in result]
```

#### 👥 Utilisateurs les plus actifs

```python
def get_most_active_users(self, limit: int = 10) -> List[Dict[str, Any]]:
    ...
```

---

## 📊 Routes API pour les statistiques

### 📁 Fichier : `src/api/routes/stats.py`

```python
@router.get("/general", response_model=Dict[str, Any])
def get_general_stats(...):
    return StatsService(db).get_general_stats()
```

### 📁 Ajout au routeur principal : `src/api/routes/__init__.py`

```python
api_router.include_router(stats_router, prefix="/stats", tags=["stats"])
```
---

## 🚀 Lancer les tests

Utilisez `pytest` pour lancer les tests :

```bash
pytest
```

---

## 📸 Est-ce que ça marche ?

![alt text](image.png)

Non, pas encore.

