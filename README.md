# Menù 9nove - Restaurant Menu Website

Un sito web elegante per visualizzare il menù del ristorante "Menù 9nove" con design iOS-inspired e funzionalità moderne.

## 🌟 Caratteristiche

- **Design Responsive** - Ottimizzato per mobile e desktop
- **5 Sezioni Menu** - Apericena, Bevande, Vini e Bollicine, Mixology, I Nostri Gin
- **Navigazione Smooth** - Scroll automatico tra sezioni
- **Backend API** - Gestione dinamica del menù
- **Database MongoDB** - Persistenza dati
- **UI Moderna** - Animazioni e hover effects

## 🏗️ Architettura

### Frontend
- **React** - Framework UI
- **Tailwind CSS** - Styling
- **Vercel** - Hosting

### Backend
- **FastAPI** - API REST
- **MongoDB** - Database
- **Railway** - Hosting

## 🚀 Deploy

### Frontend (Vercel)
```bash
# Build del frontend
cd frontend
yarn build

# Deploy automatico tramite GitHub
```

### Backend (Railway)
```bash
# Deploy automatico tramite GitHub
# Railway rileva automaticamente FastAPI
```

## 📱 Demo

Il sito è accessibile a:
- **Frontend**: [Da configurare su Vercel]
- **API**: [Da configurare su Railway]

## 🛠️ Sviluppo Locale

```bash
# Frontend
cd frontend
yarn start

# Backend
cd backend
uvicorn server:app --reload
```

## 📝 Configurazione

### Variabili di Ambiente

**Frontend (.env)**:
```
REACT_APP_BACKEND_URL=https://your-railway-backend.railway.app
```

**Backend (.env)**:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=menu_9nove
```

## 🍷 Sezioni Menu

1. **🍢 Apericena** - Bruschette, taglieri, antipasti
2. **🥤 Bevande** - Acque, bibite, succhi  
3. **🍷 Vini e Bollicine** - Prosecco, Chianti, Franciacorta
4. **🍸 Mixology** - Cocktails signature
5. **🍃 I Nostri Gin** - Selezione premium gin

## 🎨 Design

Design ispirato a iOS 26 con:
- Palette colori dorata/ambra
- Tipografia moderna
- Micro-animazioni
- Cards con shadow effects
- Navigazione sticky

## 📄 Licenza

Progetto creato per "Menù 9nove" - Tutti i diritti riservati.

---

*Creato con ❤️ da Emergent AI*