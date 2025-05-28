# 📚 Projet de Gestion de Bibliothèque avec FastAPI - TP3

Ce projet est une application de gestion de bibliothèque universitaire basée sur **FastAPI**, structurée selon une architecture **N-Tiers**.

---

## 🔐 Authentification (Connexion des utilisateurs)

📁 **Fichier : `src/api/routes/auth.py`**

On utilise ici un formulaire de connexion (`OAuth2PasswordRequestForm`) pour permettre aux utilisateurs de **se connecter avec un email et un mot de passe**. Si l'utilisateur est reconnu et actif, on lui génère un **jeton d'accès (token)**.

### Exemple de code :

```python
@router.post("/login", response_model=Token)
def login_access_token(...):
    ...
    user = service.authenticate(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    if not service.is_active(user=user):
        raise HTTPException(status_code=401, detail="Utilisateur inactif")

    return {
        "access_token": create_access_token(...),
        "token_type": "bearer",
    }
```

Ce jeton permettra ensuite d’accéder aux routes protégées.

---

## 🧪 Tests automatiques (avec `pytest`)

### 📁 `tests/conftest.py`

Ici, on prépare une **base de données en mémoire (SQLite)** spécialement pour les tests, sans affecter les vraies données.

```python
@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", ...)
    Base.metadata.create_all(engine)
    return engine
```

On configure aussi un **client de test FastAPI** :

```python
@pytest.fixture(scope="function")
def client(db_session):
    ...
    with TestClient(app) as client:
        yield client
```

### 📁 `tests/services/test_users.py`

Quelques exemples de tests :

#### ✅ Test de création d’un utilisateur

```python
def test_create_user(...):
    ...
    assert user.email == "test@example.com"
    assert user.hashed_password != "password123"
```

#### 🔐 Test de connexion

```python
def test_authenticate_user(...):
    ...
    assert authenticated_user.id == user.id
```

#### ✏️ Test de mise à jour

```python
def test_update_user(...):
    ...
    assert updated_user.full_name == "New Name"
```

Ces tests permettent de vérifier automatiquement que le code fait ce qu’on attend de lui.

---

## 📊 Statistiques (sur les livres et utilisateurs)

📁 **Fichier : `src/services/stats.py`**

Ce fichier contient un **service** qui calcule différentes statistiques sur la bibliothèque.

### Exemple de statistiques disponibles :

#### 📈 Statistiques globales

Nombre total de livres, nombre de titres différents, nombre d’utilisateurs, etc.

```python
def get_general_stats(self):
    return {
        "total_books": ...,
        "unique_books": ...,
        ...
    }
```

#### 📚 Livres les plus empruntés

```python
def get_most_borrowed_books(self, limit=10):
    ...
    return [{"id": ..., "title": ..., "loan_count": ...}, ...]
```

#### 👥 Utilisateurs les plus actifs

```python
def get_most_active_users(self, limit=10):
    ...
```

---

## 🌐 Routes API pour les statistiques

📁 **Fichier : `src/api/routes/stats.py`**

Exemple : afficher les statistiques générales :

```python
@router.get("/general")
def get_general_stats(...):
    return StatsService(db).get_general_stats()
```

📁 **Ajout dans le routeur principal** (`src/api/routes/__init__.py`) :

```python
api_router.include_router(stats_router, prefix="/stats", tags=["stats"])
```

---

## 🧪 Lancer les tests

On peut lancer tous les tests avec cette commande dans le terminal :

```bash
pytest
```

---

## 📸 Est-ce que l'application fonctionne ?

![alt text](image.png)

Non.