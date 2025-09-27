# Documentació - Pràctica Java Servlets i Chatbot RAG

Aquest directori conté tota la documentació relacionada amb la pràctica de Java Servlets i Chatbot RAG.

## Estructura de Fitxers

### Informes Principals
- `informe_practica_servlets.tex` - **Informe complet en LaTeX (Català)** ⭐
- `informe_practica_servlets.md` - Informe en Markdown (Català)
- `Informe_Practica_Servlets.html` - Informe en HTML (Català)
- `Informe_Practica_Servlets.pdf` - Informe compilat en PDF

### Imatges
- `img/` - Directori amb totes les 14 imatges utilitzades en els informes

### Scripts i Utilitats
- `compile_latex.sh` - Script de compilació LaTeX amb gestió d'errors
- `README.md` - Aquest fitxer de documentació

## Contingut de l'Informe LaTeX Completat

### 📋 Secció 1: Introducció i Objectius
- Context general de la pràctica
- Objectius principals detallats
- Stack tecnològic utilitzat
- Funcionalitats implementades

### ⚙️ Secció 2: Entorn Tecnològic i Configuració
- Apache Tomcat 10.0.10
- Java Servlets
- Docker i Docker Compose
- SSL/TLS amb certificats

### 🔧 Secció 3: Implementació dels Servlets

#### 3.1 Objectius Principals de la Pràctica
- Nova sol·licitud de lloguer amb validació completa
- Consulta del registre amb autenticació admin/admin
- Estructura del projecte amb fitxers proporcionats

#### 3.2 CarRentalNew.java - Implementació Detallada
- **Validació de Dades d'Entrada** amb categories CO₂:
  - 54 (ExtraLow), 71 (Low), 82 (Medium), 139 (High)
  - Validació de valors numèrics i gestió d'errors
- **Funció saveRental()** completa:
  - Gestió de fitxers JSON existents i nous
  - Estructura JSONObject/JSONArray
  - Gestió robusta d'excepcions
- **Processament i Visualització** amb codi complet d'HTML dinàmic

#### 3.3 CarRentalList.java - Implementació Detallada
- **Autenticació** amb credencials admin/admin
- **Lectura i Visualització del JSON** amb iteració completa
- **Gestió d'errors** i fitxers inexistents

### 🔐 Secció 4: Configuració SSL/TLS
- Generació de certificats amb keytool
- Configuració server.xml detallada
- Verificació HTTPS a port 8443
- Imatges de verificació de seguretat

### 🐳 Secció 5: Containerització amb Docker
- **Configuració inicial** amb comandaments d'instal·lació
- **Dockerfile** detallat amb explicacions pas a pas
- **Construcció i execució** de contenidors
- **Docker Compose** per automatització

### 🚀 Secció 6: Extensions de la Pràctica
- **Docker Compose** per evitar docker run manual
- **Preparació entorn Python** amb venv i pip
- **Instal·lació d'Ollama** amb models Llama3.2, 3.2:1b, 3.1

### 🤖 Secció 7: Implementació del Chatbot RAG
- **Arquitectura RAG** amb pipeline detallat
- **Components del sistema** (models, embeddings)
- **Creació d'índex vectorial** amb LangChain
- **Model d'embeddings** per representació vectorial

### 📊 Secció 8: Mesures de Rendiment i Qualitat
- **Mesura de duració** amb timestamps Python
- **Taula comparativa** de rendiment per model:
  - Llama3.2: 11.12s index / 18.66s query
  - Llama3.2:1b: 6.13s index / 11.08s query  
  - Llama3.1: 26.05s index / 26.56s query
- **Avaluació qualitativa** per cada model
- **Conversió CSV a PDF** amb ReportLab per millorar contexte
- **Comparació RAG vs Non-RAG** amb implementació completa

### 🧪 Secció 9: Avaluació i Proves del Sistema
- Proves funcionals dels servlets
- Proves del sistema RAG amb múltiples consultes
- Mètriques de rendiment detallades
- Suite de proves comprensives amb resultats

### ⚖️ Secció 10: Anàlisi Comparativa Java Servlets vs Node.js
- **Context de la comparació** detallat
- **Avantatges de Java Servlets** (6 punts ampliats):
  - Comunitat extensa amb més suport
  - Facilitat d'aprenentatge superior
  - IDEs avançats (Eclipse, NetBeans, IntelliJ)
  - Concurrència nativa vs limitacions Node.js
  - Eines de desenvolupament de primer nivell
- **Avantatges de Node.js** (6 punts ampliats):
  - Codi més compacte i net
  - Rendiment 20% superior
  - I/O asíncrona nativa
  - JavaScript universal frontend/backend

### 🎯 Secció 11: Conclusions i Recomanacions
- Conclusions principals sobre Java Servlets i RAG
- Aprenentatges obtinguts durant la pràctica
- Recomanacions per a treballs futurs
- Valoració de l'efectivitat de la solució amb IA

## Millores Implementades

### ✨ Contingut Tècnic
- **+400 línies** de codi Java amb explicacions detallades
- **Validació completa** amb categories CO₂ i gestió d'errors
- **Implementació SSL/TLS** amb certificats i configuració
- **Docker workflow** complet des d'instal·lació fins execució
- **Mètriques de rendiment** amb comparació de 3 models
- **Anàlisi RAG vs Non-RAG** amb implementacions pràctiques

### 🎨 Format i Presentació
- **Sintaxi highlighting** per Java, Python, Shell, XML, YAML
- **Taules comparatives** amb booktabs professional
- **Caixes de text colorejades** per destacar pros/cons
- **14 imatges** integrades amb captions descriptius
- **Estructura jeràrquica** amb subseccions organitzades
- **Referències creuades** i numeració automàtica

### 📏 Estadístiques del Document
- **~800 línies** de LaTeX (vs 630 originals)
- **14 imatges** correctament referenciades
- **12 blocs de codi** amb diferents llenguatges
- **6 taules** comparatives i de resultats
- **20+ subseccions** organitzades temàticament

## Compilació del Document

```bash
# Navegar al directori de documentació
cd doc/

# Utilitzar script automàtic (recomanat)
./compile_latex.sh

# O compilació manual
pdflatex informe_practica_servlets.tex
pdflatex informe_practica_servlets.tex  # Segona passada per referències
```

## Tecnologies Documentades

### Backend i Infraestructura
- Apache Tomcat 10.0.10
- Java Servlets amb JSON persistence
- SSL/TLS amb certificats autosignats
- Docker i Docker Compose

### Intel·ligència Artificial
- Ollama amb models Llama (3.2, 3.2:1b, 3.1)
- LangChain per implementació RAG
- Embeddings vectorials locals
- Comparació rendiment i qualitat

### Desenvolupament i Proves
- Validació de dades d'entrada robusta
- Gestió d'errors i excepcions
- Suite de proves comprensives
- Mètriques de rendiment quantitatives

---

**Document completat per:** Sergio Shmyhelskyy Yaskevych & Alex Lafuente Gonzalez  
**Curs:** PTI-FIB - Universitat Politècnica de Catalunya  
**Data actualització:** 26 de Setembre de 2025  
**Estat:** ✅ COMPLET - Llest per compilació i presentació